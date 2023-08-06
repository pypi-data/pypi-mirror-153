"""typing for rolling window functions
"""
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.core.typing.templates import AbstractTemplate, AttributeTemplate, signature
from numba.extending import infer, infer_getattr, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_method, register_model
import bodo
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_type, pd_timedelta_type
from bodo.hiframes.pd_dataframe_ext import DataFrameType, check_runtime_cols_unsupported
from bodo.hiframes.pd_groupby_ext import DataFrameGroupByType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.hiframes.rolling import supported_rolling_funcs, unsupported_rolling_methods
from bodo.utils.typing import BodoError, check_unsupported_args, create_unsupported_overload, get_literal_value, is_const_func_type, is_literal_type, is_overload_bool, is_overload_constant_str, is_overload_int, is_overload_none, raise_bodo_error


class RollingType(types.Type):

    def __init__(self, obj_type, window_type, on, selection,
        explicit_select=False, series_select=False):
        if isinstance(obj_type, bodo.SeriesType):
            aken__dyaog = 'Series'
        else:
            aken__dyaog = 'DataFrame'
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(obj_type,
            f'{aken__dyaog}.rolling()')
        self.obj_type = obj_type
        self.window_type = window_type
        self.on = on
        self.selection = selection
        self.explicit_select = explicit_select
        self.series_select = series_select
        super(RollingType, self).__init__(name=
            f'RollingType({obj_type}, {window_type}, {on}, {selection}, {explicit_select}, {series_select})'
            )

    def copy(self):
        return RollingType(self.obj_type, self.window_type, self.on, self.
            selection, self.explicit_select, self.series_select)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(RollingType)
class RollingModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        jmj__ble = [('obj', fe_type.obj_type), ('window', fe_type.
            window_type), ('min_periods', types.int64), ('center', types.bool_)
            ]
        super(RollingModel, self).__init__(dmm, fe_type, jmj__ble)


make_attribute_wrapper(RollingType, 'obj', 'obj')
make_attribute_wrapper(RollingType, 'window', 'window')
make_attribute_wrapper(RollingType, 'center', 'center')
make_attribute_wrapper(RollingType, 'min_periods', 'min_periods')


@overload_method(DataFrameType, 'rolling', inline='always', no_unliteral=True)
def df_rolling_overload(df, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    check_runtime_cols_unsupported(df, 'DataFrame.rolling()')
    fsdwg__sxnd = dict(win_type=win_type, axis=axis, closed=closed)
    lfnet__gdhz = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('DataFrame.rolling', fsdwg__sxnd, lfnet__gdhz,
        package_name='pandas', module_name='Window')
    _validate_rolling_args(df, window, min_periods, center, on)

    def impl(df, window, min_periods=None, center=False, win_type=None, on=
        None, axis=0, closed=None):
        min_periods = _handle_default_min_periods(min_periods, window)
        return bodo.hiframes.pd_rolling_ext.init_rolling(df, window,
            min_periods, center, on)
    return impl


@overload_method(SeriesType, 'rolling', inline='always', no_unliteral=True)
def overload_series_rolling(S, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    fsdwg__sxnd = dict(win_type=win_type, axis=axis, closed=closed)
    lfnet__gdhz = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('Series.rolling', fsdwg__sxnd, lfnet__gdhz,
        package_name='pandas', module_name='Window')
    _validate_rolling_args(S, window, min_periods, center, on)

    def impl(S, window, min_periods=None, center=False, win_type=None, on=
        None, axis=0, closed=None):
        min_periods = _handle_default_min_periods(min_periods, window)
        return bodo.hiframes.pd_rolling_ext.init_rolling(S, window,
            min_periods, center, on)
    return impl


@intrinsic
def init_rolling(typingctx, obj_type, window_type, min_periods_type,
    center_type, on_type=None):

    def codegen(context, builder, signature, args):
        qblly__jyxf, evu__erk, saoz__qhmv, vkmij__pvc, syrzu__wby = args
        qwajb__bpu = signature.return_type
        tnf__hvza = cgutils.create_struct_proxy(qwajb__bpu)(context, builder)
        tnf__hvza.obj = qblly__jyxf
        tnf__hvza.window = evu__erk
        tnf__hvza.min_periods = saoz__qhmv
        tnf__hvza.center = vkmij__pvc
        context.nrt.incref(builder, signature.args[0], qblly__jyxf)
        context.nrt.incref(builder, signature.args[1], evu__erk)
        context.nrt.incref(builder, signature.args[2], saoz__qhmv)
        context.nrt.incref(builder, signature.args[3], vkmij__pvc)
        return tnf__hvza._getvalue()
    on = get_literal_value(on_type)
    if isinstance(obj_type, SeriesType):
        selection = None
    elif isinstance(obj_type, DataFrameType):
        selection = obj_type.columns
    else:
        assert isinstance(obj_type, DataFrameGroupByType
            ), f'invalid obj type for rolling: {obj_type}'
        selection = obj_type.selection
    qwajb__bpu = RollingType(obj_type, window_type, on, selection, False)
    return qwajb__bpu(obj_type, window_type, min_periods_type, center_type,
        on_type), codegen


def _handle_default_min_periods(min_periods, window):
    return min_periods


@overload(_handle_default_min_periods)
def overload_handle_default_min_periods(min_periods, window):
    if is_overload_none(min_periods):
        if isinstance(window, types.Integer):
            return lambda min_periods, window: window
        else:
            return lambda min_periods, window: 1
    else:
        return lambda min_periods, window: min_periods


def _gen_df_rolling_out_data(rolling):
    axp__elpm = not isinstance(rolling.window_type, types.Integer)
    mznh__jfq = 'variable' if axp__elpm else 'fixed'
    okz__xlo = 'None'
    if axp__elpm:
        okz__xlo = ('bodo.utils.conversion.index_to_array(index)' if 
            rolling.on is None else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {rolling.obj_type.columns.index(rolling.on)})'
            )
    hep__evq = []
    hrxh__eyl = 'on_arr, ' if axp__elpm else ''
    if isinstance(rolling.obj_type, SeriesType):
        return (
            f'bodo.hiframes.rolling.rolling_{mznh__jfq}(bodo.hiframes.pd_series_ext.get_series_data(df), {hrxh__eyl}index_arr, window, minp, center, func, raw)'
            , okz__xlo, rolling.selection)
    assert isinstance(rolling.obj_type, DataFrameType
        ), 'expected df in rolling obj'
    nro__vttu = rolling.obj_type.data
    out_cols = []
    for zkf__vfrgb in rolling.selection:
        jsam__dmxg = rolling.obj_type.columns.index(zkf__vfrgb)
        if zkf__vfrgb == rolling.on:
            if len(rolling.selection) == 2 and rolling.series_select:
                continue
            bswbz__rakbr = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {jsam__dmxg})'
                )
            out_cols.append(zkf__vfrgb)
        else:
            if not isinstance(nro__vttu[jsam__dmxg].dtype, (types.Boolean,
                types.Number)):
                continue
            bswbz__rakbr = (
                f'bodo.hiframes.rolling.rolling_{mznh__jfq}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {jsam__dmxg}), {hrxh__eyl}index_arr, window, minp, center, func, raw)'
                )
            out_cols.append(zkf__vfrgb)
        hep__evq.append(bswbz__rakbr)
    return ', '.join(hep__evq), okz__xlo, tuple(out_cols)


@overload_method(RollingType, 'apply', inline='always', no_unliteral=True)
def overload_rolling_apply(rolling, func, raw=False, engine=None,
    engine_kwargs=None, args=None, kwargs=None):
    fsdwg__sxnd = dict(engine=engine, engine_kwargs=engine_kwargs, args=
        args, kwargs=kwargs)
    lfnet__gdhz = dict(engine=None, engine_kwargs=None, args=None, kwargs=None)
    check_unsupported_args('Rolling.apply', fsdwg__sxnd, lfnet__gdhz,
        package_name='pandas', module_name='Window')
    if not is_const_func_type(func):
        raise BodoError(
            f"Rolling.apply(): 'func' parameter must be a function, not {func} (builtin functions not supported yet)."
            )
    if not is_overload_bool(raw):
        raise BodoError(
            f"Rolling.apply(): 'raw' parameter must be bool, not {raw}.")
    return _gen_rolling_impl(rolling, 'apply')


@overload_method(DataFrameGroupByType, 'rolling', inline='always',
    no_unliteral=True)
def groupby_rolling_overload(grp, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None, method='single'):
    fsdwg__sxnd = dict(win_type=win_type, axis=axis, closed=closed, method=
        method)
    lfnet__gdhz = dict(win_type=None, axis=0, closed=None, method='single')
    check_unsupported_args('GroupBy.rolling', fsdwg__sxnd, lfnet__gdhz,
        package_name='pandas', module_name='Window')
    _validate_rolling_args(grp, window, min_periods, center, on)

    def _impl(grp, window, min_periods=None, center=False, win_type=None,
        on=None, axis=0, closed=None, method='single'):
        min_periods = _handle_default_min_periods(min_periods, window)
        return bodo.hiframes.pd_rolling_ext.init_rolling(grp, window,
            min_periods, center, on)
    return _impl


def _gen_rolling_impl(rolling, fname, other=None):
    if isinstance(rolling.obj_type, DataFrameGroupByType):
        svc__mgscp = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
        djxf__pla = f"'{rolling.on}'" if isinstance(rolling.on, str
            ) else f'{rolling.on}'
        selection = ''
        if rolling.explicit_select:
            selection = '[{}]'.format(', '.join(f"'{stcca__wcv}'" if
                isinstance(stcca__wcv, str) else f'{stcca__wcv}' for
                stcca__wcv in rolling.selection if stcca__wcv != rolling.on))
        rozv__mcr = jggo__bbp = ''
        if fname == 'apply':
            rozv__mcr = 'func, raw, args, kwargs'
            jggo__bbp = 'func, raw, None, None, args, kwargs'
        if fname == 'corr':
            rozv__mcr = jggo__bbp = 'other, pairwise'
        if fname == 'cov':
            rozv__mcr = jggo__bbp = 'other, pairwise, ddof'
        jel__pntfk = (
            f'lambda df, window, minp, center, {rozv__mcr}: bodo.hiframes.pd_rolling_ext.init_rolling(df, window, minp, center, {djxf__pla}){selection}.{fname}({jggo__bbp})'
            )
        svc__mgscp += f"""  return rolling.obj.apply({jel__pntfk}, rolling.window, rolling.min_periods, rolling.center, {rozv__mcr})
"""
        ysaam__wmc = {}
        exec(svc__mgscp, {'bodo': bodo}, ysaam__wmc)
        impl = ysaam__wmc['impl']
        return impl
    ccyeq__hlen = isinstance(rolling.obj_type, SeriesType)
    if fname in ('corr', 'cov'):
        out_cols = None if ccyeq__hlen else _get_corr_cov_out_cols(rolling,
            other, fname)
        df_cols = None if ccyeq__hlen else rolling.obj_type.columns
        other_cols = None if ccyeq__hlen else other.columns
        hep__evq, okz__xlo = _gen_corr_cov_out_data(out_cols, df_cols,
            other_cols, rolling.window_type, fname)
    else:
        hep__evq, okz__xlo, out_cols = _gen_df_rolling_out_data(rolling)
    mhady__mkn = ccyeq__hlen or len(rolling.selection) == (1 if rolling.on is
        None else 2) and rolling.series_select
    ncccb__rckr = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
    ncccb__rckr += '  df = rolling.obj\n'
    ncccb__rckr += '  index = {}\n'.format(
        'bodo.hiframes.pd_series_ext.get_series_index(df)' if ccyeq__hlen else
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
    aken__dyaog = 'None'
    if ccyeq__hlen:
        aken__dyaog = 'bodo.hiframes.pd_series_ext.get_series_name(df)'
    elif mhady__mkn:
        zkf__vfrgb = (set(out_cols) - set([rolling.on])).pop()
        aken__dyaog = f"'{zkf__vfrgb}'" if isinstance(zkf__vfrgb, str
            ) else str(zkf__vfrgb)
    ncccb__rckr += f'  name = {aken__dyaog}\n'
    ncccb__rckr += '  window = rolling.window\n'
    ncccb__rckr += '  center = rolling.center\n'
    ncccb__rckr += '  minp = rolling.min_periods\n'
    ncccb__rckr += f'  on_arr = {okz__xlo}\n'
    if fname == 'apply':
        ncccb__rckr += (
            f'  index_arr = bodo.utils.conversion.index_to_array(index)\n')
    else:
        ncccb__rckr += f"  func = '{fname}'\n"
        ncccb__rckr += f'  index_arr = None\n'
        ncccb__rckr += f'  raw = False\n'
    if mhady__mkn:
        ncccb__rckr += (
            f'  return bodo.hiframes.pd_series_ext.init_series({hep__evq}, index, name)'
            )
        ysaam__wmc = {}
        mvoe__nclfk = {'bodo': bodo}
        exec(ncccb__rckr, mvoe__nclfk, ysaam__wmc)
        impl = ysaam__wmc['impl']
        return impl
    return bodo.hiframes.dataframe_impl._gen_init_df(ncccb__rckr, out_cols,
        hep__evq)


def _get_rolling_func_args(fname):
    if fname == 'apply':
        return (
            'func, raw=False, engine=None, engine_kwargs=None, args=None, kwargs=None\n'
            )
    elif fname == 'corr':
        return 'other=None, pairwise=None, ddof=1\n'
    elif fname == 'cov':
        return 'other=None, pairwise=None, ddof=1\n'
    return ''


def create_rolling_overload(fname):

    def overload_rolling_func(rolling):
        return _gen_rolling_impl(rolling, fname)
    return overload_rolling_func


def _install_rolling_methods():
    for fname in supported_rolling_funcs:
        if fname in ('apply', 'corr', 'cov'):
            continue
        zmdgo__pob = create_rolling_overload(fname)
        overload_method(RollingType, fname, inline='always', no_unliteral=True
            )(zmdgo__pob)


def _install_rolling_unsupported_methods():
    for fname in unsupported_rolling_methods:
        overload_method(RollingType, fname, no_unliteral=True)(
            create_unsupported_overload(
            f'pandas.core.window.rolling.Rolling.{fname}()'))


_install_rolling_methods()
_install_rolling_unsupported_methods()


def _get_corr_cov_out_cols(rolling, other, func_name):
    if not isinstance(other, DataFrameType):
        raise_bodo_error(
            f"DataFrame.rolling.{func_name}(): requires providing a DataFrame for 'other'"
            )
    gtmqc__negd = rolling.selection
    if rolling.on is not None:
        raise BodoError(
            f'variable window rolling {func_name} not supported yet.')
    out_cols = tuple(sorted(set(gtmqc__negd) | set(other.columns), key=lambda
        k: str(k)))
    return out_cols


def _gen_corr_cov_out_data(out_cols, df_cols, other_cols, window_type,
    func_name):
    axp__elpm = not isinstance(window_type, types.Integer)
    okz__xlo = 'None'
    if axp__elpm:
        okz__xlo = 'bodo.utils.conversion.index_to_array(index)'
    hrxh__eyl = 'on_arr, ' if axp__elpm else ''
    hep__evq = []
    if out_cols is None:
        return (
            f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_series_ext.get_series_data(df), bodo.hiframes.pd_series_ext.get_series_data(other), {hrxh__eyl}window, minp, center)'
            , okz__xlo)
    for zkf__vfrgb in out_cols:
        if zkf__vfrgb in df_cols and zkf__vfrgb in other_cols:
            hptgp__uvu = df_cols.index(zkf__vfrgb)
            azerb__hfk = other_cols.index(zkf__vfrgb)
            bswbz__rakbr = (
                f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {hptgp__uvu}), bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {azerb__hfk}), {hrxh__eyl}window, minp, center)'
                )
        else:
            bswbz__rakbr = 'np.full(len(df), np.nan)'
        hep__evq.append(bswbz__rakbr)
    return ', '.join(hep__evq), okz__xlo


@overload_method(RollingType, 'corr', inline='always', no_unliteral=True)
def overload_rolling_corr(rolling, other=None, pairwise=None, ddof=1):
    rabum__ked = {'pairwise': pairwise, 'ddof': ddof}
    vcjr__ufeuh = {'pairwise': None, 'ddof': 1}
    check_unsupported_args('pandas.core.window.rolling.Rolling.corr',
        rabum__ked, vcjr__ufeuh, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'corr', other)


@overload_method(RollingType, 'cov', inline='always', no_unliteral=True)
def overload_rolling_cov(rolling, other=None, pairwise=None, ddof=1):
    rabum__ked = {'ddof': ddof, 'pairwise': pairwise}
    vcjr__ufeuh = {'ddof': 1, 'pairwise': None}
    check_unsupported_args('pandas.core.window.rolling.Rolling.cov',
        rabum__ked, vcjr__ufeuh, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'cov', other)


@infer
class GetItemDataFrameRolling2(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        rolling, pvqqk__yjawp = args
        if isinstance(rolling, RollingType):
            gtmqc__negd = rolling.obj_type.selection if isinstance(rolling.
                obj_type, DataFrameGroupByType) else rolling.obj_type.columns
            series_select = False
            if isinstance(pvqqk__yjawp, (tuple, list)):
                if len(set(pvqqk__yjawp).difference(set(gtmqc__negd))) > 0:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(set(pvqqk__yjawp).difference(set(gtmqc__negd)))
                        )
                selection = list(pvqqk__yjawp)
            else:
                if pvqqk__yjawp not in gtmqc__negd:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(pvqqk__yjawp))
                selection = [pvqqk__yjawp]
                series_select = True
            if rolling.on is not None:
                selection.append(rolling.on)
            mgco__ywvwg = RollingType(rolling.obj_type, rolling.window_type,
                rolling.on, tuple(selection), True, series_select)
            return signature(mgco__ywvwg, *args)


@lower_builtin('static_getitem', RollingType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@infer_getattr
class RollingAttribute(AttributeTemplate):
    key = RollingType

    def generic_resolve(self, rolling, attr):
        gtmqc__negd = ()
        if isinstance(rolling.obj_type, DataFrameGroupByType):
            gtmqc__negd = rolling.obj_type.selection
        if isinstance(rolling.obj_type, DataFrameType):
            gtmqc__negd = rolling.obj_type.columns
        if attr in gtmqc__negd:
            return RollingType(rolling.obj_type, rolling.window_type,
                rolling.on, (attr,) if rolling.on is None else (attr,
                rolling.on), True, True)


def _validate_rolling_args(obj, window, min_periods, center, on):
    assert isinstance(obj, (SeriesType, DataFrameType, DataFrameGroupByType)
        ), 'invalid rolling obj'
    func_name = 'Series' if isinstance(obj, SeriesType
        ) else 'DataFrame' if isinstance(obj, DataFrameType
        ) else 'DataFrameGroupBy'
    if not (is_overload_int(window) or is_overload_constant_str(window) or 
        window == bodo.string_type or window in (pd_timedelta_type,
        datetime_timedelta_type)):
        raise BodoError(
            f"{func_name}.rolling(): 'window' should be int or time offset (str, pd.Timedelta, datetime.timedelta), not {window}"
            )
    if not is_overload_bool(center):
        raise BodoError(
            f'{func_name}.rolling(): center must be a boolean, not {center}')
    if not (is_overload_none(min_periods) or isinstance(min_periods, types.
        Integer)):
        raise BodoError(
            f'{func_name}.rolling(): min_periods must be an integer, not {min_periods}'
            )
    if isinstance(obj, SeriesType) and not is_overload_none(on):
        raise BodoError(
            f"{func_name}.rolling(): 'on' not supported for Series yet (can use a DataFrame instead)."
            )
    dxg__eoa = obj.columns if isinstance(obj, DataFrameType
        ) else obj.df_type.columns if isinstance(obj, DataFrameGroupByType
        ) else []
    nro__vttu = [obj.data] if isinstance(obj, SeriesType
        ) else obj.data if isinstance(obj, DataFrameType) else obj.df_type.data
    if not is_overload_none(on) and (not is_literal_type(on) or 
        get_literal_value(on) not in dxg__eoa):
        raise BodoError(
            f"{func_name}.rolling(): 'on' should be a constant column name.")
    if not is_overload_none(on):
        ogt__puxvy = nro__vttu[dxg__eoa.index(get_literal_value(on))]
        if not isinstance(ogt__puxvy, types.Array
            ) or ogt__puxvy.dtype != bodo.datetime64ns:
            raise BodoError(
                f"{func_name}.rolling(): 'on' column should have datetime64 data."
                )
    if not any(isinstance(nsc__qwc.dtype, (types.Boolean, types.Number)) for
        nsc__qwc in nro__vttu):
        raise BodoError(f'{func_name}.rolling(): No numeric types to aggregate'
            )
