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
        vxxyi__qfpw = 'SeriesDatetimePropertiesType({})'.format(stype)
        super(SeriesDatetimePropertiesType, self).__init__(vxxyi__qfpw)


@register_model(SeriesDatetimePropertiesType)
class SeriesDtModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        fmsbs__ozmok = [('obj', fe_type.stype)]
        super(SeriesDtModel, self).__init__(dmm, fe_type, fmsbs__ozmok)


make_attribute_wrapper(SeriesDatetimePropertiesType, 'obj', '_obj')


@intrinsic
def init_series_dt_properties(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        khe__uiafb, = args
        amew__awb = signature.return_type
        dwfc__yucgo = cgutils.create_struct_proxy(amew__awb)(context, builder)
        dwfc__yucgo.obj = khe__uiafb
        context.nrt.incref(builder, signature.args[0], khe__uiafb)
        return dwfc__yucgo._getvalue()
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
        kty__kavk = 'def impl(S_dt):\n'
        kty__kavk += '    S = S_dt._obj\n'
        kty__kavk += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        kty__kavk += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        kty__kavk += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        kty__kavk += '    numba.parfors.parfor.init_prange()\n'
        kty__kavk += '    n = len(arr)\n'
        if field in ('is_leap_year', 'is_month_start', 'is_month_end',
            'is_quarter_start', 'is_quarter_end', 'is_year_start',
            'is_year_end'):
            kty__kavk += '    out_arr = np.empty(n, np.bool_)\n'
        else:
            kty__kavk += (
                '    out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n'
                )
        kty__kavk += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        kty__kavk += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        kty__kavk += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
        kty__kavk += '            continue\n'
        kty__kavk += (
            '        dt64 = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arr[i])\n'
            )
        if field in ('year', 'month', 'day'):
            kty__kavk += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            if field in ('month', 'day'):
                kty__kavk += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            kty__kavk += '        out_arr[i] = {}\n'.format(field)
        elif field in ('dayofyear', 'day_of_year', 'dayofweek',
            'day_of_week', 'weekday'):
            atlb__duzp = {'dayofyear': 'get_day_of_year', 'day_of_year':
                'get_day_of_year', 'dayofweek': 'get_day_of_week',
                'day_of_week': 'get_day_of_week', 'weekday': 'get_day_of_week'}
            kty__kavk += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            kty__kavk += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            kty__kavk += (
                """        out_arr[i] = bodo.hiframes.pd_timestamp_ext.{}(year, month, day)
"""
                .format(atlb__duzp[field]))
        elif field == 'is_leap_year':
            kty__kavk += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            kty__kavk += (
                '        out_arr[i] = bodo.hiframes.pd_timestamp_ext.is_leap_year(year)\n'
                )
        elif field in ('daysinmonth', 'days_in_month'):
            atlb__duzp = {'days_in_month': 'get_days_in_month',
                'daysinmonth': 'get_days_in_month'}
            kty__kavk += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            kty__kavk += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            kty__kavk += (
                '        out_arr[i] = bodo.hiframes.pd_timestamp_ext.{}(year, month)\n'
                .format(atlb__duzp[field]))
        else:
            kty__kavk += """        ts = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(dt64)
"""
            kty__kavk += '        out_arr[i] = ts.' + field + '\n'
        kty__kavk += (
            '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        bezdx__pdgo = {}
        exec(kty__kavk, {'bodo': bodo, 'numba': numba, 'np': np}, bezdx__pdgo)
        impl = bezdx__pdgo['impl']
        return impl
    return overload_field


def _install_date_fields():
    for field in bodo.hiframes.pd_timestamp_ext.date_fields:
        swei__erxr = create_date_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(swei__erxr)


_install_date_fields()


def create_date_method_overload(method):
    kzem__rvymw = method in ['day_name', 'month_name']
    if kzem__rvymw:
        kty__kavk = 'def overload_method(S_dt, locale=None):\n'
        kty__kavk += '    unsupported_args = dict(locale=locale)\n'
        kty__kavk += '    arg_defaults = dict(locale=None)\n'
        kty__kavk += '    bodo.utils.typing.check_unsupported_args(\n'
        kty__kavk += f"        'Series.dt.{method}',\n"
        kty__kavk += '        unsupported_args,\n'
        kty__kavk += '        arg_defaults,\n'
        kty__kavk += "        package_name='pandas',\n"
        kty__kavk += "        module_name='Series',\n"
        kty__kavk += '    )\n'
    else:
        kty__kavk = 'def overload_method(S_dt):\n'
        kty__kavk += f"""    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt, 'Series.dt.{method}()')
"""
    kty__kavk += """    if not (S_dt.stype.dtype == bodo.datetime64ns or isinstance(S_dt.stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
"""
    kty__kavk += '        return\n'
    if kzem__rvymw:
        kty__kavk += '    def impl(S_dt, locale=None):\n'
    else:
        kty__kavk += '    def impl(S_dt):\n'
    kty__kavk += '        S = S_dt._obj\n'
    kty__kavk += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    kty__kavk += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    kty__kavk += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    kty__kavk += '        numba.parfors.parfor.init_prange()\n'
    kty__kavk += '        n = len(arr)\n'
    if kzem__rvymw:
        kty__kavk += """        out_arr = bodo.utils.utils.alloc_type(n, bodo.string_array_type, (-1,))
"""
    else:
        kty__kavk += (
            "        out_arr = np.empty(n, np.dtype('datetime64[ns]'))\n")
    kty__kavk += '        for i in numba.parfors.parfor.internal_prange(n):\n'
    kty__kavk += '            if bodo.libs.array_kernels.isna(arr, i):\n'
    kty__kavk += '                bodo.libs.array_kernels.setna(out_arr, i)\n'
    kty__kavk += '                continue\n'
    kty__kavk += '            ts = bodo.utils.conversion.box_if_dt64(arr[i])\n'
    kty__kavk += f'            method_val = ts.{method}()\n'
    if kzem__rvymw:
        kty__kavk += '            out_arr[i] = method_val\n'
    else:
        kty__kavk += """            out_arr[i] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(method_val.value)
"""
    kty__kavk += (
        '        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    kty__kavk += '    return impl\n'
    bezdx__pdgo = {}
    exec(kty__kavk, {'bodo': bodo, 'numba': numba, 'np': np}, bezdx__pdgo)
    overload_method = bezdx__pdgo['overload_method']
    return overload_method


def _install_date_methods():
    for method in bodo.hiframes.pd_timestamp_ext.date_methods:
        swei__erxr = create_date_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            swei__erxr)


_install_date_methods()


@overload_attribute(SeriesDatetimePropertiesType, 'date')
def series_dt_date_overload(S_dt):
    if not (S_dt.stype.dtype == types.NPDatetime('ns') or isinstance(S_dt.
        stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
        return

    def impl(S_dt):
        ktm__bzfz = S_dt._obj
        qbvb__rol = bodo.hiframes.pd_series_ext.get_series_data(ktm__bzfz)
        wce__wvp = bodo.hiframes.pd_series_ext.get_series_index(ktm__bzfz)
        vxxyi__qfpw = bodo.hiframes.pd_series_ext.get_series_name(ktm__bzfz)
        numba.parfors.parfor.init_prange()
        yqrbm__hslp = len(qbvb__rol)
        njf__zlk = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
            yqrbm__hslp)
        for cllb__yvkk in numba.parfors.parfor.internal_prange(yqrbm__hslp):
            gqjvx__elvc = qbvb__rol[cllb__yvkk]
            osg__gthpu = bodo.utils.conversion.box_if_dt64(gqjvx__elvc)
            njf__zlk[cllb__yvkk] = datetime.date(osg__gthpu.year,
                osg__gthpu.month, osg__gthpu.day)
        return bodo.hiframes.pd_series_ext.init_series(njf__zlk, wce__wvp,
            vxxyi__qfpw)
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
            gujhn__ylxaq = ['days', 'hours', 'minutes', 'seconds',
                'milliseconds', 'microseconds', 'nanoseconds']
            zyz__rrel = 'convert_numpy_timedelta64_to_pd_timedelta'
            zlbo__gozv = 'np.empty(n, np.int64)'
            gskr__bvr = attr
        elif attr == 'isocalendar':
            gujhn__ylxaq = ['year', 'week', 'day']
            zyz__rrel = 'convert_datetime64_to_timestamp'
            zlbo__gozv = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.uint32)'
            gskr__bvr = attr + '()'
        kty__kavk = 'def impl(S_dt):\n'
        kty__kavk += '    S = S_dt._obj\n'
        kty__kavk += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        kty__kavk += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        kty__kavk += '    numba.parfors.parfor.init_prange()\n'
        kty__kavk += '    n = len(arr)\n'
        for field in gujhn__ylxaq:
            kty__kavk += '    {} = {}\n'.format(field, zlbo__gozv)
        kty__kavk += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        kty__kavk += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        for field in gujhn__ylxaq:
            kty__kavk += ('            bodo.libs.array_kernels.setna({}, i)\n'
                .format(field))
        kty__kavk += '            continue\n'
        jfyv__kuxyl = '(' + '[i], '.join(gujhn__ylxaq) + '[i])'
        kty__kavk += (
            '        {} = bodo.hiframes.pd_timestamp_ext.{}(arr[i]).{}\n'.
            format(jfyv__kuxyl, zyz__rrel, gskr__bvr))
        pnh__wfuar = '(' + ', '.join(gujhn__ylxaq) + ')'
        xecxz__uyw = "('" + "', '".join(gujhn__ylxaq) + "')"
        kty__kavk += (
            '    return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, index, {})\n'
            .format(pnh__wfuar, xecxz__uyw))
        bezdx__pdgo = {}
        exec(kty__kavk, {'bodo': bodo, 'numba': numba, 'np': np}, bezdx__pdgo)
        impl = bezdx__pdgo['impl']
        return impl
    return series_dt_df_output_overload


def _install_df_output_overload():
    mlpfs__mvr = [('components', overload_attribute), ('isocalendar',
        overload_method)]
    for attr, tlt__xpa in mlpfs__mvr:
        swei__erxr = create_series_dt_df_output_overload(attr)
        tlt__xpa(SeriesDatetimePropertiesType, attr, inline='always')(
            swei__erxr)


_install_df_output_overload()


def create_timedelta_field_overload(field):

    def overload_field(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        kty__kavk = 'def impl(S_dt):\n'
        kty__kavk += '    S = S_dt._obj\n'
        kty__kavk += '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
        kty__kavk += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        kty__kavk += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        kty__kavk += '    numba.parfors.parfor.init_prange()\n'
        kty__kavk += '    n = len(A)\n'
        kty__kavk += (
            '    B = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
        kty__kavk += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        kty__kavk += '        if bodo.libs.array_kernels.isna(A, i):\n'
        kty__kavk += '            bodo.libs.array_kernels.setna(B, i)\n'
        kty__kavk += '            continue\n'
        kty__kavk += (
            '        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])\n'
            )
        if field == 'nanoseconds':
            kty__kavk += '        B[i] = td64 % 1000\n'
        elif field == 'microseconds':
            kty__kavk += '        B[i] = td64 // 1000 % 1000000\n'
        elif field == 'seconds':
            kty__kavk += (
                '        B[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
        elif field == 'days':
            kty__kavk += (
                '        B[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n')
        else:
            assert False, 'invalid timedelta field'
        kty__kavk += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        bezdx__pdgo = {}
        exec(kty__kavk, {'numba': numba, 'np': np, 'bodo': bodo}, bezdx__pdgo)
        impl = bezdx__pdgo['impl']
        return impl
    return overload_field


def create_timedelta_method_overload(method):

    def overload_method(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        kty__kavk = 'def impl(S_dt):\n'
        kty__kavk += '    S = S_dt._obj\n'
        kty__kavk += '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
        kty__kavk += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        kty__kavk += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        kty__kavk += '    numba.parfors.parfor.init_prange()\n'
        kty__kavk += '    n = len(A)\n'
        if method == 'total_seconds':
            kty__kavk += '    B = np.empty(n, np.float64)\n'
        else:
            kty__kavk += """    B = bodo.hiframes.datetime_timedelta_ext.alloc_datetime_timedelta_array(n)
"""
        kty__kavk += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        kty__kavk += '        if bodo.libs.array_kernels.isna(A, i):\n'
        kty__kavk += '            bodo.libs.array_kernels.setna(B, i)\n'
        kty__kavk += '            continue\n'
        kty__kavk += (
            '        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])\n'
            )
        if method == 'total_seconds':
            kty__kavk += '        B[i] = td64 / (1000.0 * 1000000.0)\n'
        elif method == 'to_pytimedelta':
            kty__kavk += (
                '        B[i] = datetime.timedelta(microseconds=td64 // 1000)\n'
                )
        else:
            assert False, 'invalid timedelta method'
        if method == 'total_seconds':
            kty__kavk += (
                '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
                )
        else:
            kty__kavk += '    return B\n'
        bezdx__pdgo = {}
        exec(kty__kavk, {'numba': numba, 'np': np, 'bodo': bodo, 'datetime':
            datetime}, bezdx__pdgo)
        impl = bezdx__pdgo['impl']
        return impl
    return overload_method


def _install_S_dt_timedelta_fields():
    for field in bodo.hiframes.pd_timestamp_ext.timedelta_fields:
        swei__erxr = create_timedelta_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(swei__erxr)


_install_S_dt_timedelta_fields()


def _install_S_dt_timedelta_methods():
    for method in bodo.hiframes.pd_timestamp_ext.timedelta_methods:
        swei__erxr = create_timedelta_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            swei__erxr)


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
        ktm__bzfz = S_dt._obj
        bdy__vpwb = bodo.hiframes.pd_series_ext.get_series_data(ktm__bzfz)
        wce__wvp = bodo.hiframes.pd_series_ext.get_series_index(ktm__bzfz)
        vxxyi__qfpw = bodo.hiframes.pd_series_ext.get_series_name(ktm__bzfz)
        numba.parfors.parfor.init_prange()
        yqrbm__hslp = len(bdy__vpwb)
        ezfuz__xku = bodo.libs.str_arr_ext.pre_alloc_string_array(yqrbm__hslp,
            -1)
        for xlydu__dkms in numba.parfors.parfor.internal_prange(yqrbm__hslp):
            if bodo.libs.array_kernels.isna(bdy__vpwb, xlydu__dkms):
                bodo.libs.array_kernels.setna(ezfuz__xku, xlydu__dkms)
                continue
            ezfuz__xku[xlydu__dkms] = bodo.utils.conversion.box_if_dt64(
                bdy__vpwb[xlydu__dkms]).strftime(date_format)
        return bodo.hiframes.pd_series_ext.init_series(ezfuz__xku, wce__wvp,
            vxxyi__qfpw)
    return impl


@overload_method(SeriesDatetimePropertiesType, 'tz_convert', inline=
    'always', no_unliteral=True)
def overload_dt_tz_convert(S_dt, tz):

    def impl(S_dt, tz):
        ktm__bzfz = S_dt._obj
        eemer__yhnjs = get_series_data(ktm__bzfz).tz_convert(tz)
        wce__wvp = get_series_index(ktm__bzfz)
        vxxyi__qfpw = get_series_name(ktm__bzfz)
        return init_series(eemer__yhnjs, wce__wvp, vxxyi__qfpw)
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
        hoi__xprr = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        lnet__fmw = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args(f'Series.dt.{method}', hoi__xprr, lnet__fmw,
            package_name='pandas', module_name='Series')
        kty__kavk = (
            "def impl(S_dt, freq, ambiguous='raise', nonexistent='raise'):\n")
        kty__kavk += '    S = S_dt._obj\n'
        kty__kavk += '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
        kty__kavk += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        kty__kavk += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        kty__kavk += '    numba.parfors.parfor.init_prange()\n'
        kty__kavk += '    n = len(A)\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            kty__kavk += "    B = np.empty(n, np.dtype('timedelta64[ns]'))\n"
        else:
            kty__kavk += "    B = np.empty(n, np.dtype('datetime64[ns]'))\n"
        kty__kavk += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        kty__kavk += '        if bodo.libs.array_kernels.isna(A, i):\n'
        kty__kavk += '            bodo.libs.array_kernels.setna(B, i)\n'
        kty__kavk += '            continue\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            rikum__qwps = (
                'bodo.hiframes.pd_timestamp_ext.convert_numpy_timedelta64_to_pd_timedelta'
                )
            zehyf__vmh = (
                'bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64')
        else:
            rikum__qwps = (
                'bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp'
                )
            zehyf__vmh = 'bodo.hiframes.pd_timestamp_ext.integer_to_dt64'
        kty__kavk += '        B[i] = {}({}(A[i]).{}(freq).value)\n'.format(
            zehyf__vmh, rikum__qwps, method)
        kty__kavk += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        bezdx__pdgo = {}
        exec(kty__kavk, {'numba': numba, 'np': np, 'bodo': bodo}, bezdx__pdgo)
        impl = bezdx__pdgo['impl']
        return impl
    return freq_overload


def _install_S_dt_timedelta_freq_methods():
    knjv__ashrc = ['ceil', 'floor', 'round']
    for method in knjv__ashrc:
        swei__erxr = create_timedelta_freq_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            swei__erxr)


_install_S_dt_timedelta_freq_methods()


def create_bin_op_overload(op):

    def overload_series_dt_binop(lhs, rhs):
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs):
            uqm__ljldv = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                optzu__btrjo = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                hhyf__oay = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    optzu__btrjo)
                wce__wvp = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                vxxyi__qfpw = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                fltyf__zjz = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                rwkf__kyc = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    fltyf__zjz)
                yqrbm__hslp = len(hhyf__oay)
                ktm__bzfz = np.empty(yqrbm__hslp, timedelta64_dtype)
                zjao__kluyw = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    uqm__ljldv)
                for cllb__yvkk in numba.parfors.parfor.internal_prange(
                    yqrbm__hslp):
                    tbnrp__sou = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(hhyf__oay[cllb__yvkk]))
                    yygjw__ern = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(rwkf__kyc[cllb__yvkk]))
                    if tbnrp__sou == zjao__kluyw or yygjw__ern == zjao__kluyw:
                        azdz__rxcr = zjao__kluyw
                    else:
                        azdz__rxcr = op(tbnrp__sou, yygjw__ern)
                    ktm__bzfz[cllb__yvkk
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        azdz__rxcr)
                return bodo.hiframes.pd_series_ext.init_series(ktm__bzfz,
                    wce__wvp, vxxyi__qfpw)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs):
            uqm__ljldv = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                rkw__yafei = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                qbvb__rol = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    rkw__yafei)
                wce__wvp = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                vxxyi__qfpw = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                rwkf__kyc = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                yqrbm__hslp = len(qbvb__rol)
                ktm__bzfz = np.empty(yqrbm__hslp, dt64_dtype)
                zjao__kluyw = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    uqm__ljldv)
                for cllb__yvkk in numba.parfors.parfor.internal_prange(
                    yqrbm__hslp):
                    lte__totpi = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(qbvb__rol[cllb__yvkk]))
                    ubkx__hcic = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(rwkf__kyc[cllb__yvkk]))
                    if lte__totpi == zjao__kluyw or ubkx__hcic == zjao__kluyw:
                        azdz__rxcr = zjao__kluyw
                    else:
                        azdz__rxcr = op(lte__totpi, ubkx__hcic)
                    ktm__bzfz[cllb__yvkk
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        azdz__rxcr)
                return bodo.hiframes.pd_series_ext.init_series(ktm__bzfz,
                    wce__wvp, vxxyi__qfpw)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs):
            uqm__ljldv = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                rkw__yafei = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                qbvb__rol = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    rkw__yafei)
                wce__wvp = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                vxxyi__qfpw = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                rwkf__kyc = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                yqrbm__hslp = len(qbvb__rol)
                ktm__bzfz = np.empty(yqrbm__hslp, dt64_dtype)
                zjao__kluyw = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    uqm__ljldv)
                for cllb__yvkk in numba.parfors.parfor.internal_prange(
                    yqrbm__hslp):
                    lte__totpi = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(qbvb__rol[cllb__yvkk]))
                    ubkx__hcic = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(rwkf__kyc[cllb__yvkk]))
                    if lte__totpi == zjao__kluyw or ubkx__hcic == zjao__kluyw:
                        azdz__rxcr = zjao__kluyw
                    else:
                        azdz__rxcr = op(lte__totpi, ubkx__hcic)
                    ktm__bzfz[cllb__yvkk
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        azdz__rxcr)
                return bodo.hiframes.pd_series_ext.init_series(ktm__bzfz,
                    wce__wvp, vxxyi__qfpw)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            uqm__ljldv = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                rkw__yafei = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                qbvb__rol = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    rkw__yafei)
                wce__wvp = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                vxxyi__qfpw = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                yqrbm__hslp = len(qbvb__rol)
                ktm__bzfz = np.empty(yqrbm__hslp, timedelta64_dtype)
                zjao__kluyw = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    uqm__ljldv)
                ggspv__nmbzh = rhs.value
                for cllb__yvkk in numba.parfors.parfor.internal_prange(
                    yqrbm__hslp):
                    lte__totpi = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(qbvb__rol[cllb__yvkk]))
                    if (lte__totpi == zjao__kluyw or ggspv__nmbzh ==
                        zjao__kluyw):
                        azdz__rxcr = zjao__kluyw
                    else:
                        azdz__rxcr = op(lte__totpi, ggspv__nmbzh)
                    ktm__bzfz[cllb__yvkk
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        azdz__rxcr)
                return bodo.hiframes.pd_series_ext.init_series(ktm__bzfz,
                    wce__wvp, vxxyi__qfpw)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            uqm__ljldv = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                rkw__yafei = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                qbvb__rol = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    rkw__yafei)
                wce__wvp = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                vxxyi__qfpw = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                yqrbm__hslp = len(qbvb__rol)
                ktm__bzfz = np.empty(yqrbm__hslp, timedelta64_dtype)
                zjao__kluyw = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    uqm__ljldv)
                ggspv__nmbzh = lhs.value
                for cllb__yvkk in numba.parfors.parfor.internal_prange(
                    yqrbm__hslp):
                    lte__totpi = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(qbvb__rol[cllb__yvkk]))
                    if (ggspv__nmbzh == zjao__kluyw or lte__totpi ==
                        zjao__kluyw):
                        azdz__rxcr = zjao__kluyw
                    else:
                        azdz__rxcr = op(ggspv__nmbzh, lte__totpi)
                    ktm__bzfz[cllb__yvkk
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        azdz__rxcr)
                return bodo.hiframes.pd_series_ext.init_series(ktm__bzfz,
                    wce__wvp, vxxyi__qfpw)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            uqm__ljldv = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                rkw__yafei = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                qbvb__rol = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    rkw__yafei)
                wce__wvp = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                vxxyi__qfpw = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                yqrbm__hslp = len(qbvb__rol)
                ktm__bzfz = np.empty(yqrbm__hslp, dt64_dtype)
                zjao__kluyw = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    uqm__ljldv)
                pyk__oti = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                ubkx__hcic = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(pyk__oti))
                for cllb__yvkk in numba.parfors.parfor.internal_prange(
                    yqrbm__hslp):
                    lte__totpi = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(qbvb__rol[cllb__yvkk]))
                    if lte__totpi == zjao__kluyw or ubkx__hcic == zjao__kluyw:
                        azdz__rxcr = zjao__kluyw
                    else:
                        azdz__rxcr = op(lte__totpi, ubkx__hcic)
                    ktm__bzfz[cllb__yvkk
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        azdz__rxcr)
                return bodo.hiframes.pd_series_ext.init_series(ktm__bzfz,
                    wce__wvp, vxxyi__qfpw)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            uqm__ljldv = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                rkw__yafei = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                qbvb__rol = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    rkw__yafei)
                wce__wvp = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                vxxyi__qfpw = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                yqrbm__hslp = len(qbvb__rol)
                ktm__bzfz = np.empty(yqrbm__hslp, dt64_dtype)
                zjao__kluyw = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    uqm__ljldv)
                pyk__oti = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                ubkx__hcic = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(pyk__oti))
                for cllb__yvkk in numba.parfors.parfor.internal_prange(
                    yqrbm__hslp):
                    lte__totpi = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(qbvb__rol[cllb__yvkk]))
                    if lte__totpi == zjao__kluyw or ubkx__hcic == zjao__kluyw:
                        azdz__rxcr = zjao__kluyw
                    else:
                        azdz__rxcr = op(lte__totpi, ubkx__hcic)
                    ktm__bzfz[cllb__yvkk
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        azdz__rxcr)
                return bodo.hiframes.pd_series_ext.init_series(ktm__bzfz,
                    wce__wvp, vxxyi__qfpw)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            uqm__ljldv = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                rkw__yafei = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                qbvb__rol = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    rkw__yafei)
                wce__wvp = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                vxxyi__qfpw = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                yqrbm__hslp = len(qbvb__rol)
                ktm__bzfz = np.empty(yqrbm__hslp, timedelta64_dtype)
                zjao__kluyw = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    uqm__ljldv)
                ubdb__bconm = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(rhs))
                lte__totpi = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ubdb__bconm)
                for cllb__yvkk in numba.parfors.parfor.internal_prange(
                    yqrbm__hslp):
                    gioaq__hwz = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(qbvb__rol[cllb__yvkk]))
                    if gioaq__hwz == zjao__kluyw or lte__totpi == zjao__kluyw:
                        azdz__rxcr = zjao__kluyw
                    else:
                        azdz__rxcr = op(gioaq__hwz, lte__totpi)
                    ktm__bzfz[cllb__yvkk
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        azdz__rxcr)
                return bodo.hiframes.pd_series_ext.init_series(ktm__bzfz,
                    wce__wvp, vxxyi__qfpw)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            uqm__ljldv = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                rkw__yafei = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                qbvb__rol = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    rkw__yafei)
                wce__wvp = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                vxxyi__qfpw = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                yqrbm__hslp = len(qbvb__rol)
                ktm__bzfz = np.empty(yqrbm__hslp, timedelta64_dtype)
                zjao__kluyw = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    uqm__ljldv)
                ubdb__bconm = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(lhs))
                lte__totpi = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ubdb__bconm)
                for cllb__yvkk in numba.parfors.parfor.internal_prange(
                    yqrbm__hslp):
                    gioaq__hwz = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(qbvb__rol[cllb__yvkk]))
                    if lte__totpi == zjao__kluyw or gioaq__hwz == zjao__kluyw:
                        azdz__rxcr = zjao__kluyw
                    else:
                        azdz__rxcr = op(lte__totpi, gioaq__hwz)
                    ktm__bzfz[cllb__yvkk
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        azdz__rxcr)
                return bodo.hiframes.pd_series_ext.init_series(ktm__bzfz,
                    wce__wvp, vxxyi__qfpw)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            uqm__ljldv = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                qbvb__rol = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                wce__wvp = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                vxxyi__qfpw = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                yqrbm__hslp = len(qbvb__rol)
                ktm__bzfz = np.empty(yqrbm__hslp, timedelta64_dtype)
                zjao__kluyw = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(uqm__ljldv))
                pyk__oti = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                ubkx__hcic = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(pyk__oti))
                for cllb__yvkk in numba.parfors.parfor.internal_prange(
                    yqrbm__hslp):
                    kvxhu__vvizf = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(qbvb__rol[cllb__yvkk]))
                    if (ubkx__hcic == zjao__kluyw or kvxhu__vvizf ==
                        zjao__kluyw):
                        azdz__rxcr = zjao__kluyw
                    else:
                        azdz__rxcr = op(kvxhu__vvizf, ubkx__hcic)
                    ktm__bzfz[cllb__yvkk
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        azdz__rxcr)
                return bodo.hiframes.pd_series_ext.init_series(ktm__bzfz,
                    wce__wvp, vxxyi__qfpw)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            uqm__ljldv = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                qbvb__rol = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                wce__wvp = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                vxxyi__qfpw = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                yqrbm__hslp = len(qbvb__rol)
                ktm__bzfz = np.empty(yqrbm__hslp, timedelta64_dtype)
                zjao__kluyw = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(uqm__ljldv))
                pyk__oti = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                ubkx__hcic = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(pyk__oti))
                for cllb__yvkk in numba.parfors.parfor.internal_prange(
                    yqrbm__hslp):
                    kvxhu__vvizf = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(qbvb__rol[cllb__yvkk]))
                    if (ubkx__hcic == zjao__kluyw or kvxhu__vvizf ==
                        zjao__kluyw):
                        azdz__rxcr = zjao__kluyw
                    else:
                        azdz__rxcr = op(ubkx__hcic, kvxhu__vvizf)
                    ktm__bzfz[cllb__yvkk
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        azdz__rxcr)
                return bodo.hiframes.pd_series_ext.init_series(ktm__bzfz,
                    wce__wvp, vxxyi__qfpw)
            return impl
        raise BodoError(f'{op} not supported for data types {lhs} and {rhs}.')
    return overload_series_dt_binop


def create_cmp_op_overload(op):

    def overload_series_dt64_cmp(lhs, rhs):
        if op == operator.ne:
            mxn__vgzhh = True
        else:
            mxn__vgzhh = False
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            uqm__ljldv = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                qbvb__rol = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                wce__wvp = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                vxxyi__qfpw = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                yqrbm__hslp = len(qbvb__rol)
                njf__zlk = bodo.libs.bool_arr_ext.alloc_bool_array(yqrbm__hslp)
                zjao__kluyw = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(uqm__ljldv))
                hsksv__ubvu = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                xomg__jhtkt = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(hsksv__ubvu))
                for cllb__yvkk in numba.parfors.parfor.internal_prange(
                    yqrbm__hslp):
                    vuwdi__kbx = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(qbvb__rol[cllb__yvkk]))
                    if vuwdi__kbx == zjao__kluyw or xomg__jhtkt == zjao__kluyw:
                        azdz__rxcr = mxn__vgzhh
                    else:
                        azdz__rxcr = op(vuwdi__kbx, xomg__jhtkt)
                    njf__zlk[cllb__yvkk] = azdz__rxcr
                return bodo.hiframes.pd_series_ext.init_series(njf__zlk,
                    wce__wvp, vxxyi__qfpw)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            uqm__ljldv = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                qbvb__rol = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                wce__wvp = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                vxxyi__qfpw = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                yqrbm__hslp = len(qbvb__rol)
                njf__zlk = bodo.libs.bool_arr_ext.alloc_bool_array(yqrbm__hslp)
                zjao__kluyw = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(uqm__ljldv))
                oduj__tbzz = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                vuwdi__kbx = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(oduj__tbzz))
                for cllb__yvkk in numba.parfors.parfor.internal_prange(
                    yqrbm__hslp):
                    xomg__jhtkt = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(qbvb__rol[cllb__yvkk]))
                    if vuwdi__kbx == zjao__kluyw or xomg__jhtkt == zjao__kluyw:
                        azdz__rxcr = mxn__vgzhh
                    else:
                        azdz__rxcr = op(vuwdi__kbx, xomg__jhtkt)
                    njf__zlk[cllb__yvkk] = azdz__rxcr
                return bodo.hiframes.pd_series_ext.init_series(njf__zlk,
                    wce__wvp, vxxyi__qfpw)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            uqm__ljldv = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                rkw__yafei = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                qbvb__rol = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    rkw__yafei)
                wce__wvp = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                vxxyi__qfpw = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                yqrbm__hslp = len(qbvb__rol)
                njf__zlk = bodo.libs.bool_arr_ext.alloc_bool_array(yqrbm__hslp)
                zjao__kluyw = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    uqm__ljldv)
                for cllb__yvkk in numba.parfors.parfor.internal_prange(
                    yqrbm__hslp):
                    vuwdi__kbx = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(qbvb__rol[cllb__yvkk]))
                    if vuwdi__kbx == zjao__kluyw or rhs.value == zjao__kluyw:
                        azdz__rxcr = mxn__vgzhh
                    else:
                        azdz__rxcr = op(vuwdi__kbx, rhs.value)
                    njf__zlk[cllb__yvkk] = azdz__rxcr
                return bodo.hiframes.pd_series_ext.init_series(njf__zlk,
                    wce__wvp, vxxyi__qfpw)
            return impl
        if (lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type and
            bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs)):
            uqm__ljldv = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                rkw__yafei = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                qbvb__rol = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    rkw__yafei)
                wce__wvp = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                vxxyi__qfpw = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                yqrbm__hslp = len(qbvb__rol)
                njf__zlk = bodo.libs.bool_arr_ext.alloc_bool_array(yqrbm__hslp)
                zjao__kluyw = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    uqm__ljldv)
                for cllb__yvkk in numba.parfors.parfor.internal_prange(
                    yqrbm__hslp):
                    xomg__jhtkt = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(qbvb__rol[cllb__yvkk]))
                    if xomg__jhtkt == zjao__kluyw or lhs.value == zjao__kluyw:
                        azdz__rxcr = mxn__vgzhh
                    else:
                        azdz__rxcr = op(lhs.value, xomg__jhtkt)
                    njf__zlk[cllb__yvkk] = azdz__rxcr
                return bodo.hiframes.pd_series_ext.init_series(njf__zlk,
                    wce__wvp, vxxyi__qfpw)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (rhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(rhs)):
            uqm__ljldv = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                rkw__yafei = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                qbvb__rol = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    rkw__yafei)
                wce__wvp = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                vxxyi__qfpw = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                yqrbm__hslp = len(qbvb__rol)
                njf__zlk = bodo.libs.bool_arr_ext.alloc_bool_array(yqrbm__hslp)
                zjao__kluyw = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    uqm__ljldv)
                baf__kul = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    rhs)
                eqnwh__uqx = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    baf__kul)
                for cllb__yvkk in numba.parfors.parfor.internal_prange(
                    yqrbm__hslp):
                    vuwdi__kbx = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(qbvb__rol[cllb__yvkk]))
                    if vuwdi__kbx == zjao__kluyw or eqnwh__uqx == zjao__kluyw:
                        azdz__rxcr = mxn__vgzhh
                    else:
                        azdz__rxcr = op(vuwdi__kbx, eqnwh__uqx)
                    njf__zlk[cllb__yvkk] = azdz__rxcr
                return bodo.hiframes.pd_series_ext.init_series(njf__zlk,
                    wce__wvp, vxxyi__qfpw)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (lhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(lhs)):
            uqm__ljldv = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                rkw__yafei = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                qbvb__rol = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    rkw__yafei)
                wce__wvp = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                vxxyi__qfpw = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                numba.parfors.parfor.init_prange()
                yqrbm__hslp = len(qbvb__rol)
                njf__zlk = bodo.libs.bool_arr_ext.alloc_bool_array(yqrbm__hslp)
                zjao__kluyw = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    uqm__ljldv)
                baf__kul = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    lhs)
                eqnwh__uqx = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    baf__kul)
                for cllb__yvkk in numba.parfors.parfor.internal_prange(
                    yqrbm__hslp):
                    ubdb__bconm = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(qbvb__rol[cllb__yvkk]))
                    if ubdb__bconm == zjao__kluyw or eqnwh__uqx == zjao__kluyw:
                        azdz__rxcr = mxn__vgzhh
                    else:
                        azdz__rxcr = op(eqnwh__uqx, ubdb__bconm)
                    njf__zlk[cllb__yvkk] = azdz__rxcr
                return bodo.hiframes.pd_series_ext.init_series(njf__zlk,
                    wce__wvp, vxxyi__qfpw)
            return impl
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_series_dt64_cmp


series_dt_unsupported_methods = {'to_period', 'to_pydatetime',
    'tz_localize', 'asfreq', 'to_timestamp'}
series_dt_unsupported_attrs = {'time', 'timetz', 'tz', 'freq', 'qyear',
    'start_time', 'end_time'}


def _install_series_dt_unsupported():
    for iis__gofwe in series_dt_unsupported_attrs:
        mgb__kxnm = 'Series.dt.' + iis__gofwe
        overload_attribute(SeriesDatetimePropertiesType, iis__gofwe)(
            create_unsupported_overload(mgb__kxnm))
    for mqto__rbbdx in series_dt_unsupported_methods:
        mgb__kxnm = 'Series.dt.' + mqto__rbbdx
        overload_method(SeriesDatetimePropertiesType, mqto__rbbdx,
            no_unliteral=True)(create_unsupported_overload(mgb__kxnm))


_install_series_dt_unsupported()
