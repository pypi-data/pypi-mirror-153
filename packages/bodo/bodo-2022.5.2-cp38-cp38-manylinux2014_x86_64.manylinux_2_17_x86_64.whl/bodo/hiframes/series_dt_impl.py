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
        osp__wvu = 'SeriesDatetimePropertiesType({})'.format(stype)
        super(SeriesDatetimePropertiesType, self).__init__(osp__wvu)


@register_model(SeriesDatetimePropertiesType)
class SeriesDtModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        hflhq__uhecm = [('obj', fe_type.stype)]
        super(SeriesDtModel, self).__init__(dmm, fe_type, hflhq__uhecm)


make_attribute_wrapper(SeriesDatetimePropertiesType, 'obj', '_obj')


@intrinsic
def init_series_dt_properties(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        vgeru__hzptt, = args
        mibll__erazf = signature.return_type
        zxcmh__ywm = cgutils.create_struct_proxy(mibll__erazf)(context, builder
            )
        zxcmh__ywm.obj = vgeru__hzptt
        context.nrt.incref(builder, signature.args[0], vgeru__hzptt)
        return zxcmh__ywm._getvalue()
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
        luux__hxyk = 'def impl(S_dt):\n'
        luux__hxyk += '    S = S_dt._obj\n'
        luux__hxyk += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        luux__hxyk += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        luux__hxyk += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        luux__hxyk += '    numba.parfors.parfor.init_prange()\n'
        luux__hxyk += '    n = len(arr)\n'
        if field in ('is_leap_year', 'is_month_start', 'is_month_end',
            'is_quarter_start', 'is_quarter_end', 'is_year_start',
            'is_year_end'):
            luux__hxyk += '    out_arr = np.empty(n, np.bool_)\n'
        else:
            luux__hxyk += (
                '    out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n'
                )
        luux__hxyk += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        luux__hxyk += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        luux__hxyk += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
        luux__hxyk += '            continue\n'
        luux__hxyk += (
            '        dt64 = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arr[i])\n'
            )
        if field in ('year', 'month', 'day'):
            luux__hxyk += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            if field in ('month', 'day'):
                luux__hxyk += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            luux__hxyk += '        out_arr[i] = {}\n'.format(field)
        elif field in ('dayofyear', 'day_of_year', 'dayofweek',
            'day_of_week', 'weekday'):
            jke__usn = {'dayofyear': 'get_day_of_year', 'day_of_year':
                'get_day_of_year', 'dayofweek': 'get_day_of_week',
                'day_of_week': 'get_day_of_week', 'weekday': 'get_day_of_week'}
            luux__hxyk += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            luux__hxyk += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            luux__hxyk += (
                """        out_arr[i] = bodo.hiframes.pd_timestamp_ext.{}(year, month, day)
"""
                .format(jke__usn[field]))
        elif field == 'is_leap_year':
            luux__hxyk += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            luux__hxyk += """        out_arr[i] = bodo.hiframes.pd_timestamp_ext.is_leap_year(year)
"""
        elif field in ('daysinmonth', 'days_in_month'):
            jke__usn = {'days_in_month': 'get_days_in_month', 'daysinmonth':
                'get_days_in_month'}
            luux__hxyk += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            luux__hxyk += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            luux__hxyk += (
                '        out_arr[i] = bodo.hiframes.pd_timestamp_ext.{}(year, month)\n'
                .format(jke__usn[field]))
        else:
            luux__hxyk += """        ts = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(dt64)
"""
            luux__hxyk += '        out_arr[i] = ts.' + field + '\n'
        luux__hxyk += (
            '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        xig__ymqs = {}
        exec(luux__hxyk, {'bodo': bodo, 'numba': numba, 'np': np}, xig__ymqs)
        impl = xig__ymqs['impl']
        return impl
    return overload_field


def _install_date_fields():
    for field in bodo.hiframes.pd_timestamp_ext.date_fields:
        aeh__cedcx = create_date_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(aeh__cedcx)


_install_date_fields()


def create_date_method_overload(method):
    bpzbj__wqskh = method in ['day_name', 'month_name']
    if bpzbj__wqskh:
        luux__hxyk = 'def overload_method(S_dt, locale=None):\n'
        luux__hxyk += '    unsupported_args = dict(locale=locale)\n'
        luux__hxyk += '    arg_defaults = dict(locale=None)\n'
        luux__hxyk += '    bodo.utils.typing.check_unsupported_args(\n'
        luux__hxyk += f"        'Series.dt.{method}',\n"
        luux__hxyk += '        unsupported_args,\n'
        luux__hxyk += '        arg_defaults,\n'
        luux__hxyk += "        package_name='pandas',\n"
        luux__hxyk += "        module_name='Series',\n"
        luux__hxyk += '    )\n'
    else:
        luux__hxyk = 'def overload_method(S_dt):\n'
        luux__hxyk += f"""    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt, 'Series.dt.{method}()')
"""
    luux__hxyk += """    if not (S_dt.stype.dtype == bodo.datetime64ns or isinstance(S_dt.stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
"""
    luux__hxyk += '        return\n'
    if bpzbj__wqskh:
        luux__hxyk += '    def impl(S_dt, locale=None):\n'
    else:
        luux__hxyk += '    def impl(S_dt):\n'
    luux__hxyk += '        S = S_dt._obj\n'
    luux__hxyk += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    luux__hxyk += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    luux__hxyk += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    luux__hxyk += '        numba.parfors.parfor.init_prange()\n'
    luux__hxyk += '        n = len(arr)\n'
    if bpzbj__wqskh:
        luux__hxyk += """        out_arr = bodo.utils.utils.alloc_type(n, bodo.string_array_type, (-1,))
"""
    else:
        luux__hxyk += (
            "        out_arr = np.empty(n, np.dtype('datetime64[ns]'))\n")
    luux__hxyk += '        for i in numba.parfors.parfor.internal_prange(n):\n'
    luux__hxyk += '            if bodo.libs.array_kernels.isna(arr, i):\n'
    luux__hxyk += '                bodo.libs.array_kernels.setna(out_arr, i)\n'
    luux__hxyk += '                continue\n'
    luux__hxyk += (
        '            ts = bodo.utils.conversion.box_if_dt64(arr[i])\n')
    luux__hxyk += f'            method_val = ts.{method}()\n'
    if bpzbj__wqskh:
        luux__hxyk += '            out_arr[i] = method_val\n'
    else:
        luux__hxyk += """            out_arr[i] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(method_val.value)
"""
    luux__hxyk += (
        '        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    luux__hxyk += '    return impl\n'
    xig__ymqs = {}
    exec(luux__hxyk, {'bodo': bodo, 'numba': numba, 'np': np}, xig__ymqs)
    overload_method = xig__ymqs['overload_method']
    return overload_method


def _install_date_methods():
    for method in bodo.hiframes.pd_timestamp_ext.date_methods:
        aeh__cedcx = create_date_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            aeh__cedcx)


_install_date_methods()


@overload_attribute(SeriesDatetimePropertiesType, 'date')
def series_dt_date_overload(S_dt):
    if not (S_dt.stype.dtype == types.NPDatetime('ns') or isinstance(S_dt.
        stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
        return

    def impl(S_dt):
        qdin__api = S_dt._obj
        olae__icff = bodo.hiframes.pd_series_ext.get_series_data(qdin__api)
        mdvm__tpu = bodo.hiframes.pd_series_ext.get_series_index(qdin__api)
        osp__wvu = bodo.hiframes.pd_series_ext.get_series_name(qdin__api)
        numba.parfors.parfor.init_prange()
        kqcn__pai = len(olae__icff)
        vomb__aosj = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
            kqcn__pai)
        for hdo__gkr in numba.parfors.parfor.internal_prange(kqcn__pai):
            wxn__lzynh = olae__icff[hdo__gkr]
            lmg__qib = bodo.utils.conversion.box_if_dt64(wxn__lzynh)
            vomb__aosj[hdo__gkr] = datetime.date(lmg__qib.year, lmg__qib.
                month, lmg__qib.day)
        return bodo.hiframes.pd_series_ext.init_series(vomb__aosj,
            mdvm__tpu, osp__wvu)
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
            con__unnn = ['days', 'hours', 'minutes', 'seconds',
                'milliseconds', 'microseconds', 'nanoseconds']
            tke__lydvv = 'convert_numpy_timedelta64_to_pd_timedelta'
            limnv__klhln = 'np.empty(n, np.int64)'
            vsz__namma = attr
        elif attr == 'isocalendar':
            con__unnn = ['year', 'week', 'day']
            tke__lydvv = 'convert_datetime64_to_timestamp'
            limnv__klhln = (
                'bodo.libs.int_arr_ext.alloc_int_array(n, np.uint32)')
            vsz__namma = attr + '()'
        luux__hxyk = 'def impl(S_dt):\n'
        luux__hxyk += '    S = S_dt._obj\n'
        luux__hxyk += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        luux__hxyk += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        luux__hxyk += '    numba.parfors.parfor.init_prange()\n'
        luux__hxyk += '    n = len(arr)\n'
        for field in con__unnn:
            luux__hxyk += '    {} = {}\n'.format(field, limnv__klhln)
        luux__hxyk += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        luux__hxyk += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        for field in con__unnn:
            luux__hxyk += ('            bodo.libs.array_kernels.setna({}, i)\n'
                .format(field))
        luux__hxyk += '            continue\n'
        crjec__uwk = '(' + '[i], '.join(con__unnn) + '[i])'
        luux__hxyk += (
            '        {} = bodo.hiframes.pd_timestamp_ext.{}(arr[i]).{}\n'.
            format(crjec__uwk, tke__lydvv, vsz__namma))
        muwj__lpxy = '(' + ', '.join(con__unnn) + ')'
        kbcyx__kgts = "('" + "', '".join(con__unnn) + "')"
        luux__hxyk += (
            '    return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, index, {})\n'
            .format(muwj__lpxy, kbcyx__kgts))
        xig__ymqs = {}
        exec(luux__hxyk, {'bodo': bodo, 'numba': numba, 'np': np}, xig__ymqs)
        impl = xig__ymqs['impl']
        return impl
    return series_dt_df_output_overload


def _install_df_output_overload():
    lqs__zlq = [('components', overload_attribute), ('isocalendar',
        overload_method)]
    for attr, hgcmg__yxat in lqs__zlq:
        aeh__cedcx = create_series_dt_df_output_overload(attr)
        hgcmg__yxat(SeriesDatetimePropertiesType, attr, inline='always')(
            aeh__cedcx)


_install_df_output_overload()


def create_timedelta_field_overload(field):

    def overload_field(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        luux__hxyk = 'def impl(S_dt):\n'
        luux__hxyk += '    S = S_dt._obj\n'
        luux__hxyk += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        luux__hxyk += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        luux__hxyk += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        luux__hxyk += '    numba.parfors.parfor.init_prange()\n'
        luux__hxyk += '    n = len(A)\n'
        luux__hxyk += (
            '    B = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
        luux__hxyk += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        luux__hxyk += '        if bodo.libs.array_kernels.isna(A, i):\n'
        luux__hxyk += '            bodo.libs.array_kernels.setna(B, i)\n'
        luux__hxyk += '            continue\n'
        luux__hxyk += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if field == 'nanoseconds':
            luux__hxyk += '        B[i] = td64 % 1000\n'
        elif field == 'microseconds':
            luux__hxyk += '        B[i] = td64 // 1000 % 1000000\n'
        elif field == 'seconds':
            luux__hxyk += (
                '        B[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
        elif field == 'days':
            luux__hxyk += (
                '        B[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n')
        else:
            assert False, 'invalid timedelta field'
        luux__hxyk += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        xig__ymqs = {}
        exec(luux__hxyk, {'numba': numba, 'np': np, 'bodo': bodo}, xig__ymqs)
        impl = xig__ymqs['impl']
        return impl
    return overload_field


def create_timedelta_method_overload(method):

    def overload_method(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        luux__hxyk = 'def impl(S_dt):\n'
        luux__hxyk += '    S = S_dt._obj\n'
        luux__hxyk += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        luux__hxyk += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        luux__hxyk += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        luux__hxyk += '    numba.parfors.parfor.init_prange()\n'
        luux__hxyk += '    n = len(A)\n'
        if method == 'total_seconds':
            luux__hxyk += '    B = np.empty(n, np.float64)\n'
        else:
            luux__hxyk += """    B = bodo.hiframes.datetime_timedelta_ext.alloc_datetime_timedelta_array(n)
"""
        luux__hxyk += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        luux__hxyk += '        if bodo.libs.array_kernels.isna(A, i):\n'
        luux__hxyk += '            bodo.libs.array_kernels.setna(B, i)\n'
        luux__hxyk += '            continue\n'
        luux__hxyk += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if method == 'total_seconds':
            luux__hxyk += '        B[i] = td64 / (1000.0 * 1000000.0)\n'
        elif method == 'to_pytimedelta':
            luux__hxyk += (
                '        B[i] = datetime.timedelta(microseconds=td64 // 1000)\n'
                )
        else:
            assert False, 'invalid timedelta method'
        if method == 'total_seconds':
            luux__hxyk += (
                '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
                )
        else:
            luux__hxyk += '    return B\n'
        xig__ymqs = {}
        exec(luux__hxyk, {'numba': numba, 'np': np, 'bodo': bodo,
            'datetime': datetime}, xig__ymqs)
        impl = xig__ymqs['impl']
        return impl
    return overload_method


def _install_S_dt_timedelta_fields():
    for field in bodo.hiframes.pd_timestamp_ext.timedelta_fields:
        aeh__cedcx = create_timedelta_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(aeh__cedcx)


_install_S_dt_timedelta_fields()


def _install_S_dt_timedelta_methods():
    for method in bodo.hiframes.pd_timestamp_ext.timedelta_methods:
        aeh__cedcx = create_timedelta_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            aeh__cedcx)


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
        qdin__api = S_dt._obj
        bfctr__bzn = bodo.hiframes.pd_series_ext.get_series_data(qdin__api)
        mdvm__tpu = bodo.hiframes.pd_series_ext.get_series_index(qdin__api)
        osp__wvu = bodo.hiframes.pd_series_ext.get_series_name(qdin__api)
        numba.parfors.parfor.init_prange()
        kqcn__pai = len(bfctr__bzn)
        jnll__nau = bodo.libs.str_arr_ext.pre_alloc_string_array(kqcn__pai, -1)
        for nqor__bnwyr in numba.parfors.parfor.internal_prange(kqcn__pai):
            if bodo.libs.array_kernels.isna(bfctr__bzn, nqor__bnwyr):
                bodo.libs.array_kernels.setna(jnll__nau, nqor__bnwyr)
                continue
            jnll__nau[nqor__bnwyr] = bodo.utils.conversion.box_if_dt64(
                bfctr__bzn[nqor__bnwyr]).strftime(date_format)
        return bodo.hiframes.pd_series_ext.init_series(jnll__nau, mdvm__tpu,
            osp__wvu)
    return impl


@overload_method(SeriesDatetimePropertiesType, 'tz_convert', inline=
    'always', no_unliteral=True)
def overload_dt_tz_convert(S_dt, tz):

    def impl(S_dt, tz):
        qdin__api = S_dt._obj
        fwss__rph = get_series_data(qdin__api).tz_convert(tz)
        mdvm__tpu = get_series_index(qdin__api)
        osp__wvu = get_series_name(qdin__api)
        return init_series(fwss__rph, mdvm__tpu, osp__wvu)
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
        exe__rhh = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        pflsj__eelt = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args(f'Series.dt.{method}', exe__rhh, pflsj__eelt,
            package_name='pandas', module_name='Series')
        luux__hxyk = (
            "def impl(S_dt, freq, ambiguous='raise', nonexistent='raise'):\n")
        luux__hxyk += '    S = S_dt._obj\n'
        luux__hxyk += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        luux__hxyk += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        luux__hxyk += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        luux__hxyk += '    numba.parfors.parfor.init_prange()\n'
        luux__hxyk += '    n = len(A)\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            luux__hxyk += "    B = np.empty(n, np.dtype('timedelta64[ns]'))\n"
        else:
            luux__hxyk += "    B = np.empty(n, np.dtype('datetime64[ns]'))\n"
        luux__hxyk += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        luux__hxyk += '        if bodo.libs.array_kernels.isna(A, i):\n'
        luux__hxyk += '            bodo.libs.array_kernels.setna(B, i)\n'
        luux__hxyk += '            continue\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            meg__dlq = (
                'bodo.hiframes.pd_timestamp_ext.convert_numpy_timedelta64_to_pd_timedelta'
                )
            pefuq__flz = (
                'bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64')
        else:
            meg__dlq = (
                'bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp'
                )
            pefuq__flz = 'bodo.hiframes.pd_timestamp_ext.integer_to_dt64'
        luux__hxyk += '        B[i] = {}({}(A[i]).{}(freq).value)\n'.format(
            pefuq__flz, meg__dlq, method)
        luux__hxyk += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        xig__ymqs = {}
        exec(luux__hxyk, {'numba': numba, 'np': np, 'bodo': bodo}, xig__ymqs)
        impl = xig__ymqs['impl']
        return impl
    return freq_overload


def _install_S_dt_timedelta_freq_methods():
    mruiz__bawj = ['ceil', 'floor', 'round']
    for method in mruiz__bawj:
        aeh__cedcx = create_timedelta_freq_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            aeh__cedcx)


_install_S_dt_timedelta_freq_methods()


def create_bin_op_overload(op):

    def overload_series_dt_binop(lhs, rhs):
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs):
            bqrw__fevrg = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                nldg__rhgh = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                ewkvu__ecbw = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    nldg__rhgh)
                mdvm__tpu = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                osp__wvu = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                bypo__zkdp = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                cqwc__ral = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    bypo__zkdp)
                kqcn__pai = len(ewkvu__ecbw)
                qdin__api = np.empty(kqcn__pai, timedelta64_dtype)
                oonpw__xfdr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bqrw__fevrg)
                for hdo__gkr in numba.parfors.parfor.internal_prange(kqcn__pai
                    ):
                    phpsv__cxpr = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(ewkvu__ecbw[hdo__gkr]))
                    awb__wvc = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        cqwc__ral[hdo__gkr])
                    if phpsv__cxpr == oonpw__xfdr or awb__wvc == oonpw__xfdr:
                        gkbz__tnywa = oonpw__xfdr
                    else:
                        gkbz__tnywa = op(phpsv__cxpr, awb__wvc)
                    qdin__api[hdo__gkr
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        gkbz__tnywa)
                return bodo.hiframes.pd_series_ext.init_series(qdin__api,
                    mdvm__tpu, osp__wvu)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs):
            bqrw__fevrg = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                rtwvs__exckj = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                olae__icff = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    rtwvs__exckj)
                mdvm__tpu = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                osp__wvu = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                cqwc__ral = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                kqcn__pai = len(olae__icff)
                qdin__api = np.empty(kqcn__pai, dt64_dtype)
                oonpw__xfdr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bqrw__fevrg)
                for hdo__gkr in numba.parfors.parfor.internal_prange(kqcn__pai
                    ):
                    ywevl__xjnsv = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(olae__icff[hdo__gkr]))
                    jvmt__mbuxh = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(cqwc__ral[hdo__gkr]))
                    if (ywevl__xjnsv == oonpw__xfdr or jvmt__mbuxh ==
                        oonpw__xfdr):
                        gkbz__tnywa = oonpw__xfdr
                    else:
                        gkbz__tnywa = op(ywevl__xjnsv, jvmt__mbuxh)
                    qdin__api[hdo__gkr
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        gkbz__tnywa)
                return bodo.hiframes.pd_series_ext.init_series(qdin__api,
                    mdvm__tpu, osp__wvu)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs):
            bqrw__fevrg = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                rtwvs__exckj = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                olae__icff = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    rtwvs__exckj)
                mdvm__tpu = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                osp__wvu = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                cqwc__ral = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                kqcn__pai = len(olae__icff)
                qdin__api = np.empty(kqcn__pai, dt64_dtype)
                oonpw__xfdr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bqrw__fevrg)
                for hdo__gkr in numba.parfors.parfor.internal_prange(kqcn__pai
                    ):
                    ywevl__xjnsv = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(olae__icff[hdo__gkr]))
                    jvmt__mbuxh = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(cqwc__ral[hdo__gkr]))
                    if (ywevl__xjnsv == oonpw__xfdr or jvmt__mbuxh ==
                        oonpw__xfdr):
                        gkbz__tnywa = oonpw__xfdr
                    else:
                        gkbz__tnywa = op(ywevl__xjnsv, jvmt__mbuxh)
                    qdin__api[hdo__gkr
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        gkbz__tnywa)
                return bodo.hiframes.pd_series_ext.init_series(qdin__api,
                    mdvm__tpu, osp__wvu)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            bqrw__fevrg = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                rtwvs__exckj = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                olae__icff = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    rtwvs__exckj)
                mdvm__tpu = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                osp__wvu = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                kqcn__pai = len(olae__icff)
                qdin__api = np.empty(kqcn__pai, timedelta64_dtype)
                oonpw__xfdr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bqrw__fevrg)
                cozvz__gpboa = rhs.value
                for hdo__gkr in numba.parfors.parfor.internal_prange(kqcn__pai
                    ):
                    ywevl__xjnsv = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(olae__icff[hdo__gkr]))
                    if (ywevl__xjnsv == oonpw__xfdr or cozvz__gpboa ==
                        oonpw__xfdr):
                        gkbz__tnywa = oonpw__xfdr
                    else:
                        gkbz__tnywa = op(ywevl__xjnsv, cozvz__gpboa)
                    qdin__api[hdo__gkr
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        gkbz__tnywa)
                return bodo.hiframes.pd_series_ext.init_series(qdin__api,
                    mdvm__tpu, osp__wvu)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            bqrw__fevrg = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                rtwvs__exckj = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                olae__icff = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    rtwvs__exckj)
                mdvm__tpu = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                osp__wvu = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                kqcn__pai = len(olae__icff)
                qdin__api = np.empty(kqcn__pai, timedelta64_dtype)
                oonpw__xfdr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bqrw__fevrg)
                cozvz__gpboa = lhs.value
                for hdo__gkr in numba.parfors.parfor.internal_prange(kqcn__pai
                    ):
                    ywevl__xjnsv = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(olae__icff[hdo__gkr]))
                    if (cozvz__gpboa == oonpw__xfdr or ywevl__xjnsv ==
                        oonpw__xfdr):
                        gkbz__tnywa = oonpw__xfdr
                    else:
                        gkbz__tnywa = op(cozvz__gpboa, ywevl__xjnsv)
                    qdin__api[hdo__gkr
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        gkbz__tnywa)
                return bodo.hiframes.pd_series_ext.init_series(qdin__api,
                    mdvm__tpu, osp__wvu)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            bqrw__fevrg = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                rtwvs__exckj = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                olae__icff = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    rtwvs__exckj)
                mdvm__tpu = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                osp__wvu = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                kqcn__pai = len(olae__icff)
                qdin__api = np.empty(kqcn__pai, dt64_dtype)
                oonpw__xfdr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bqrw__fevrg)
                olg__cst = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                jvmt__mbuxh = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(olg__cst))
                for hdo__gkr in numba.parfors.parfor.internal_prange(kqcn__pai
                    ):
                    ywevl__xjnsv = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(olae__icff[hdo__gkr]))
                    if (ywevl__xjnsv == oonpw__xfdr or jvmt__mbuxh ==
                        oonpw__xfdr):
                        gkbz__tnywa = oonpw__xfdr
                    else:
                        gkbz__tnywa = op(ywevl__xjnsv, jvmt__mbuxh)
                    qdin__api[hdo__gkr
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        gkbz__tnywa)
                return bodo.hiframes.pd_series_ext.init_series(qdin__api,
                    mdvm__tpu, osp__wvu)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            bqrw__fevrg = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                rtwvs__exckj = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                olae__icff = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    rtwvs__exckj)
                mdvm__tpu = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                osp__wvu = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                kqcn__pai = len(olae__icff)
                qdin__api = np.empty(kqcn__pai, dt64_dtype)
                oonpw__xfdr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bqrw__fevrg)
                olg__cst = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                jvmt__mbuxh = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(olg__cst))
                for hdo__gkr in numba.parfors.parfor.internal_prange(kqcn__pai
                    ):
                    ywevl__xjnsv = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(olae__icff[hdo__gkr]))
                    if (ywevl__xjnsv == oonpw__xfdr or jvmt__mbuxh ==
                        oonpw__xfdr):
                        gkbz__tnywa = oonpw__xfdr
                    else:
                        gkbz__tnywa = op(ywevl__xjnsv, jvmt__mbuxh)
                    qdin__api[hdo__gkr
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        gkbz__tnywa)
                return bodo.hiframes.pd_series_ext.init_series(qdin__api,
                    mdvm__tpu, osp__wvu)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            bqrw__fevrg = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                rtwvs__exckj = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                olae__icff = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    rtwvs__exckj)
                mdvm__tpu = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                osp__wvu = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                kqcn__pai = len(olae__icff)
                qdin__api = np.empty(kqcn__pai, timedelta64_dtype)
                oonpw__xfdr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bqrw__fevrg)
                jpkws__pjwa = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(rhs))
                ywevl__xjnsv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    jpkws__pjwa)
                for hdo__gkr in numba.parfors.parfor.internal_prange(kqcn__pai
                    ):
                    afm__nwje = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        olae__icff[hdo__gkr])
                    if afm__nwje == oonpw__xfdr or ywevl__xjnsv == oonpw__xfdr:
                        gkbz__tnywa = oonpw__xfdr
                    else:
                        gkbz__tnywa = op(afm__nwje, ywevl__xjnsv)
                    qdin__api[hdo__gkr
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        gkbz__tnywa)
                return bodo.hiframes.pd_series_ext.init_series(qdin__api,
                    mdvm__tpu, osp__wvu)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            bqrw__fevrg = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                rtwvs__exckj = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                olae__icff = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    rtwvs__exckj)
                mdvm__tpu = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                osp__wvu = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                kqcn__pai = len(olae__icff)
                qdin__api = np.empty(kqcn__pai, timedelta64_dtype)
                oonpw__xfdr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bqrw__fevrg)
                jpkws__pjwa = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(lhs))
                ywevl__xjnsv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    jpkws__pjwa)
                for hdo__gkr in numba.parfors.parfor.internal_prange(kqcn__pai
                    ):
                    afm__nwje = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        olae__icff[hdo__gkr])
                    if ywevl__xjnsv == oonpw__xfdr or afm__nwje == oonpw__xfdr:
                        gkbz__tnywa = oonpw__xfdr
                    else:
                        gkbz__tnywa = op(ywevl__xjnsv, afm__nwje)
                    qdin__api[hdo__gkr
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        gkbz__tnywa)
                return bodo.hiframes.pd_series_ext.init_series(qdin__api,
                    mdvm__tpu, osp__wvu)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            bqrw__fevrg = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                olae__icff = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                mdvm__tpu = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                osp__wvu = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                kqcn__pai = len(olae__icff)
                qdin__api = np.empty(kqcn__pai, timedelta64_dtype)
                oonpw__xfdr = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(bqrw__fevrg))
                olg__cst = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                jvmt__mbuxh = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(olg__cst))
                for hdo__gkr in numba.parfors.parfor.internal_prange(kqcn__pai
                    ):
                    xbvsz__qmlj = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(olae__icff[hdo__gkr]))
                    if (jvmt__mbuxh == oonpw__xfdr or xbvsz__qmlj ==
                        oonpw__xfdr):
                        gkbz__tnywa = oonpw__xfdr
                    else:
                        gkbz__tnywa = op(xbvsz__qmlj, jvmt__mbuxh)
                    qdin__api[hdo__gkr
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        gkbz__tnywa)
                return bodo.hiframes.pd_series_ext.init_series(qdin__api,
                    mdvm__tpu, osp__wvu)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            bqrw__fevrg = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                olae__icff = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                mdvm__tpu = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                osp__wvu = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                kqcn__pai = len(olae__icff)
                qdin__api = np.empty(kqcn__pai, timedelta64_dtype)
                oonpw__xfdr = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(bqrw__fevrg))
                olg__cst = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                jvmt__mbuxh = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(olg__cst))
                for hdo__gkr in numba.parfors.parfor.internal_prange(kqcn__pai
                    ):
                    xbvsz__qmlj = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(olae__icff[hdo__gkr]))
                    if (jvmt__mbuxh == oonpw__xfdr or xbvsz__qmlj ==
                        oonpw__xfdr):
                        gkbz__tnywa = oonpw__xfdr
                    else:
                        gkbz__tnywa = op(jvmt__mbuxh, xbvsz__qmlj)
                    qdin__api[hdo__gkr
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        gkbz__tnywa)
                return bodo.hiframes.pd_series_ext.init_series(qdin__api,
                    mdvm__tpu, osp__wvu)
            return impl
        raise BodoError(f'{op} not supported for data types {lhs} and {rhs}.')
    return overload_series_dt_binop


def create_cmp_op_overload(op):

    def overload_series_dt64_cmp(lhs, rhs):
        if op == operator.ne:
            xwbu__ndz = True
        else:
            xwbu__ndz = False
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            bqrw__fevrg = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                olae__icff = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                mdvm__tpu = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                osp__wvu = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                kqcn__pai = len(olae__icff)
                vomb__aosj = bodo.libs.bool_arr_ext.alloc_bool_array(kqcn__pai)
                oonpw__xfdr = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(bqrw__fevrg))
                dmqs__khak = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                nqewp__jvie = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(dmqs__khak))
                for hdo__gkr in numba.parfors.parfor.internal_prange(kqcn__pai
                    ):
                    rizt__winx = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(olae__icff[hdo__gkr]))
                    if rizt__winx == oonpw__xfdr or nqewp__jvie == oonpw__xfdr:
                        gkbz__tnywa = xwbu__ndz
                    else:
                        gkbz__tnywa = op(rizt__winx, nqewp__jvie)
                    vomb__aosj[hdo__gkr] = gkbz__tnywa
                return bodo.hiframes.pd_series_ext.init_series(vomb__aosj,
                    mdvm__tpu, osp__wvu)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            bqrw__fevrg = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                olae__icff = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                mdvm__tpu = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                osp__wvu = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                kqcn__pai = len(olae__icff)
                vomb__aosj = bodo.libs.bool_arr_ext.alloc_bool_array(kqcn__pai)
                oonpw__xfdr = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(bqrw__fevrg))
                uzu__qwr = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                rizt__winx = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(uzu__qwr))
                for hdo__gkr in numba.parfors.parfor.internal_prange(kqcn__pai
                    ):
                    nqewp__jvie = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(olae__icff[hdo__gkr]))
                    if rizt__winx == oonpw__xfdr or nqewp__jvie == oonpw__xfdr:
                        gkbz__tnywa = xwbu__ndz
                    else:
                        gkbz__tnywa = op(rizt__winx, nqewp__jvie)
                    vomb__aosj[hdo__gkr] = gkbz__tnywa
                return bodo.hiframes.pd_series_ext.init_series(vomb__aosj,
                    mdvm__tpu, osp__wvu)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            bqrw__fevrg = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                rtwvs__exckj = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                olae__icff = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    rtwvs__exckj)
                mdvm__tpu = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                osp__wvu = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                kqcn__pai = len(olae__icff)
                vomb__aosj = bodo.libs.bool_arr_ext.alloc_bool_array(kqcn__pai)
                oonpw__xfdr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bqrw__fevrg)
                for hdo__gkr in numba.parfors.parfor.internal_prange(kqcn__pai
                    ):
                    rizt__winx = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(olae__icff[hdo__gkr]))
                    if rizt__winx == oonpw__xfdr or rhs.value == oonpw__xfdr:
                        gkbz__tnywa = xwbu__ndz
                    else:
                        gkbz__tnywa = op(rizt__winx, rhs.value)
                    vomb__aosj[hdo__gkr] = gkbz__tnywa
                return bodo.hiframes.pd_series_ext.init_series(vomb__aosj,
                    mdvm__tpu, osp__wvu)
            return impl
        if (lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type and
            bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs)):
            bqrw__fevrg = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                rtwvs__exckj = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                olae__icff = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    rtwvs__exckj)
                mdvm__tpu = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                osp__wvu = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                kqcn__pai = len(olae__icff)
                vomb__aosj = bodo.libs.bool_arr_ext.alloc_bool_array(kqcn__pai)
                oonpw__xfdr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bqrw__fevrg)
                for hdo__gkr in numba.parfors.parfor.internal_prange(kqcn__pai
                    ):
                    nqewp__jvie = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(olae__icff[hdo__gkr]))
                    if nqewp__jvie == oonpw__xfdr or lhs.value == oonpw__xfdr:
                        gkbz__tnywa = xwbu__ndz
                    else:
                        gkbz__tnywa = op(lhs.value, nqewp__jvie)
                    vomb__aosj[hdo__gkr] = gkbz__tnywa
                return bodo.hiframes.pd_series_ext.init_series(vomb__aosj,
                    mdvm__tpu, osp__wvu)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (rhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(rhs)):
            bqrw__fevrg = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                rtwvs__exckj = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                olae__icff = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    rtwvs__exckj)
                mdvm__tpu = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                osp__wvu = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                kqcn__pai = len(olae__icff)
                vomb__aosj = bodo.libs.bool_arr_ext.alloc_bool_array(kqcn__pai)
                oonpw__xfdr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bqrw__fevrg)
                hnnns__txt = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    rhs)
                sesp__xbc = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    hnnns__txt)
                for hdo__gkr in numba.parfors.parfor.internal_prange(kqcn__pai
                    ):
                    rizt__winx = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(olae__icff[hdo__gkr]))
                    if rizt__winx == oonpw__xfdr or sesp__xbc == oonpw__xfdr:
                        gkbz__tnywa = xwbu__ndz
                    else:
                        gkbz__tnywa = op(rizt__winx, sesp__xbc)
                    vomb__aosj[hdo__gkr] = gkbz__tnywa
                return bodo.hiframes.pd_series_ext.init_series(vomb__aosj,
                    mdvm__tpu, osp__wvu)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (lhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(lhs)):
            bqrw__fevrg = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                rtwvs__exckj = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                olae__icff = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    rtwvs__exckj)
                mdvm__tpu = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                osp__wvu = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                numba.parfors.parfor.init_prange()
                kqcn__pai = len(olae__icff)
                vomb__aosj = bodo.libs.bool_arr_ext.alloc_bool_array(kqcn__pai)
                oonpw__xfdr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bqrw__fevrg)
                hnnns__txt = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    lhs)
                sesp__xbc = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    hnnns__txt)
                for hdo__gkr in numba.parfors.parfor.internal_prange(kqcn__pai
                    ):
                    jpkws__pjwa = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(olae__icff[hdo__gkr]))
                    if jpkws__pjwa == oonpw__xfdr or sesp__xbc == oonpw__xfdr:
                        gkbz__tnywa = xwbu__ndz
                    else:
                        gkbz__tnywa = op(sesp__xbc, jpkws__pjwa)
                    vomb__aosj[hdo__gkr] = gkbz__tnywa
                return bodo.hiframes.pd_series_ext.init_series(vomb__aosj,
                    mdvm__tpu, osp__wvu)
            return impl
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_series_dt64_cmp


series_dt_unsupported_methods = {'to_period', 'to_pydatetime',
    'tz_localize', 'asfreq', 'to_timestamp'}
series_dt_unsupported_attrs = {'time', 'timetz', 'tz', 'freq', 'qyear',
    'start_time', 'end_time'}


def _install_series_dt_unsupported():
    for thv__zop in series_dt_unsupported_attrs:
        rhzm__rza = 'Series.dt.' + thv__zop
        overload_attribute(SeriesDatetimePropertiesType, thv__zop)(
            create_unsupported_overload(rhzm__rza))
    for ayql__fsoe in series_dt_unsupported_methods:
        rhzm__rza = 'Series.dt.' + ayql__fsoe
        overload_method(SeriesDatetimePropertiesType, ayql__fsoe,
            no_unliteral=True)(create_unsupported_overload(rhzm__rza))


_install_series_dt_unsupported()
