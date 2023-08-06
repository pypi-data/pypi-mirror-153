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
            wse__sfl = 'Series'
        else:
            wse__sfl = 'DataFrame'
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(obj_type,
            f'{wse__sfl}.rolling()')
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
        ejru__lkrv = [('obj', fe_type.obj_type), ('window', fe_type.
            window_type), ('min_periods', types.int64), ('center', types.bool_)
            ]
        super(RollingModel, self).__init__(dmm, fe_type, ejru__lkrv)


make_attribute_wrapper(RollingType, 'obj', 'obj')
make_attribute_wrapper(RollingType, 'window', 'window')
make_attribute_wrapper(RollingType, 'center', 'center')
make_attribute_wrapper(RollingType, 'min_periods', 'min_periods')


@overload_method(DataFrameType, 'rolling', inline='always', no_unliteral=True)
def df_rolling_overload(df, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    check_runtime_cols_unsupported(df, 'DataFrame.rolling()')
    qtkj__krnyt = dict(win_type=win_type, axis=axis, closed=closed)
    wkaxp__pnls = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('DataFrame.rolling', qtkj__krnyt, wkaxp__pnls,
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
    qtkj__krnyt = dict(win_type=win_type, axis=axis, closed=closed)
    wkaxp__pnls = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('Series.rolling', qtkj__krnyt, wkaxp__pnls,
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
        svo__zvl, atcvk__mtnlw, nrnjr__mmq, aqppp__qjiho, pcg__fhbyy = args
        asazn__ijx = signature.return_type
        tkxi__klwy = cgutils.create_struct_proxy(asazn__ijx)(context, builder)
        tkxi__klwy.obj = svo__zvl
        tkxi__klwy.window = atcvk__mtnlw
        tkxi__klwy.min_periods = nrnjr__mmq
        tkxi__klwy.center = aqppp__qjiho
        context.nrt.incref(builder, signature.args[0], svo__zvl)
        context.nrt.incref(builder, signature.args[1], atcvk__mtnlw)
        context.nrt.incref(builder, signature.args[2], nrnjr__mmq)
        context.nrt.incref(builder, signature.args[3], aqppp__qjiho)
        return tkxi__klwy._getvalue()
    on = get_literal_value(on_type)
    if isinstance(obj_type, SeriesType):
        selection = None
    elif isinstance(obj_type, DataFrameType):
        selection = obj_type.columns
    else:
        assert isinstance(obj_type, DataFrameGroupByType
            ), f'invalid obj type for rolling: {obj_type}'
        selection = obj_type.selection
    asazn__ijx = RollingType(obj_type, window_type, on, selection, False)
    return asazn__ijx(obj_type, window_type, min_periods_type, center_type,
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
    gkr__dhpm = not isinstance(rolling.window_type, types.Integer)
    hbhlc__xsfra = 'variable' if gkr__dhpm else 'fixed'
    hne__epeel = 'None'
    if gkr__dhpm:
        hne__epeel = ('bodo.utils.conversion.index_to_array(index)' if 
            rolling.on is None else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {rolling.obj_type.columns.index(rolling.on)})'
            )
    hgw__pgrk = []
    qoifq__jcc = 'on_arr, ' if gkr__dhpm else ''
    if isinstance(rolling.obj_type, SeriesType):
        return (
            f'bodo.hiframes.rolling.rolling_{hbhlc__xsfra}(bodo.hiframes.pd_series_ext.get_series_data(df), {qoifq__jcc}index_arr, window, minp, center, func, raw)'
            , hne__epeel, rolling.selection)
    assert isinstance(rolling.obj_type, DataFrameType
        ), 'expected df in rolling obj'
    ymo__rhr = rolling.obj_type.data
    out_cols = []
    for eza__rsf in rolling.selection:
        bbpkg__hlba = rolling.obj_type.columns.index(eza__rsf)
        if eza__rsf == rolling.on:
            if len(rolling.selection) == 2 and rolling.series_select:
                continue
            rwi__hjb = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {bbpkg__hlba})'
                )
            out_cols.append(eza__rsf)
        else:
            if not isinstance(ymo__rhr[bbpkg__hlba].dtype, (types.Boolean,
                types.Number)):
                continue
            rwi__hjb = (
                f'bodo.hiframes.rolling.rolling_{hbhlc__xsfra}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {bbpkg__hlba}), {qoifq__jcc}index_arr, window, minp, center, func, raw)'
                )
            out_cols.append(eza__rsf)
        hgw__pgrk.append(rwi__hjb)
    return ', '.join(hgw__pgrk), hne__epeel, tuple(out_cols)


@overload_method(RollingType, 'apply', inline='always', no_unliteral=True)
def overload_rolling_apply(rolling, func, raw=False, engine=None,
    engine_kwargs=None, args=None, kwargs=None):
    qtkj__krnyt = dict(engine=engine, engine_kwargs=engine_kwargs, args=
        args, kwargs=kwargs)
    wkaxp__pnls = dict(engine=None, engine_kwargs=None, args=None, kwargs=None)
    check_unsupported_args('Rolling.apply', qtkj__krnyt, wkaxp__pnls,
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
    qtkj__krnyt = dict(win_type=win_type, axis=axis, closed=closed, method=
        method)
    wkaxp__pnls = dict(win_type=None, axis=0, closed=None, method='single')
    check_unsupported_args('GroupBy.rolling', qtkj__krnyt, wkaxp__pnls,
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
        ult__dng = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
        wkv__jcce = f"'{rolling.on}'" if isinstance(rolling.on, str
            ) else f'{rolling.on}'
        selection = ''
        if rolling.explicit_select:
            selection = '[{}]'.format(', '.join(f"'{mrtxd__vjbfc}'" if
                isinstance(mrtxd__vjbfc, str) else f'{mrtxd__vjbfc}' for
                mrtxd__vjbfc in rolling.selection if mrtxd__vjbfc !=
                rolling.on))
        ojsba__tmru = etqay__uivnf = ''
        if fname == 'apply':
            ojsba__tmru = 'func, raw, args, kwargs'
            etqay__uivnf = 'func, raw, None, None, args, kwargs'
        if fname == 'corr':
            ojsba__tmru = etqay__uivnf = 'other, pairwise'
        if fname == 'cov':
            ojsba__tmru = etqay__uivnf = 'other, pairwise, ddof'
        dkdq__nwwf = (
            f'lambda df, window, minp, center, {ojsba__tmru}: bodo.hiframes.pd_rolling_ext.init_rolling(df, window, minp, center, {wkv__jcce}){selection}.{fname}({etqay__uivnf})'
            )
        ult__dng += f"""  return rolling.obj.apply({dkdq__nwwf}, rolling.window, rolling.min_periods, rolling.center, {ojsba__tmru})
"""
        kdkw__xsnj = {}
        exec(ult__dng, {'bodo': bodo}, kdkw__xsnj)
        impl = kdkw__xsnj['impl']
        return impl
    gby__vumnx = isinstance(rolling.obj_type, SeriesType)
    if fname in ('corr', 'cov'):
        out_cols = None if gby__vumnx else _get_corr_cov_out_cols(rolling,
            other, fname)
        df_cols = None if gby__vumnx else rolling.obj_type.columns
        other_cols = None if gby__vumnx else other.columns
        hgw__pgrk, hne__epeel = _gen_corr_cov_out_data(out_cols, df_cols,
            other_cols, rolling.window_type, fname)
    else:
        hgw__pgrk, hne__epeel, out_cols = _gen_df_rolling_out_data(rolling)
    olte__oxvn = gby__vumnx or len(rolling.selection) == (1 if rolling.on is
        None else 2) and rolling.series_select
    yzd__ejkkc = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
    yzd__ejkkc += '  df = rolling.obj\n'
    yzd__ejkkc += '  index = {}\n'.format(
        'bodo.hiframes.pd_series_ext.get_series_index(df)' if gby__vumnx else
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
    wse__sfl = 'None'
    if gby__vumnx:
        wse__sfl = 'bodo.hiframes.pd_series_ext.get_series_name(df)'
    elif olte__oxvn:
        eza__rsf = (set(out_cols) - set([rolling.on])).pop()
        wse__sfl = f"'{eza__rsf}'" if isinstance(eza__rsf, str) else str(
            eza__rsf)
    yzd__ejkkc += f'  name = {wse__sfl}\n'
    yzd__ejkkc += '  window = rolling.window\n'
    yzd__ejkkc += '  center = rolling.center\n'
    yzd__ejkkc += '  minp = rolling.min_periods\n'
    yzd__ejkkc += f'  on_arr = {hne__epeel}\n'
    if fname == 'apply':
        yzd__ejkkc += (
            f'  index_arr = bodo.utils.conversion.index_to_array(index)\n')
    else:
        yzd__ejkkc += f"  func = '{fname}'\n"
        yzd__ejkkc += f'  index_arr = None\n'
        yzd__ejkkc += f'  raw = False\n'
    if olte__oxvn:
        yzd__ejkkc += (
            f'  return bodo.hiframes.pd_series_ext.init_series({hgw__pgrk}, index, name)'
            )
        kdkw__xsnj = {}
        ijpwh__jrwym = {'bodo': bodo}
        exec(yzd__ejkkc, ijpwh__jrwym, kdkw__xsnj)
        impl = kdkw__xsnj['impl']
        return impl
    return bodo.hiframes.dataframe_impl._gen_init_df(yzd__ejkkc, out_cols,
        hgw__pgrk)


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
        itxh__fxt = create_rolling_overload(fname)
        overload_method(RollingType, fname, inline='always', no_unliteral=True
            )(itxh__fxt)


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
    gcetk__xdy = rolling.selection
    if rolling.on is not None:
        raise BodoError(
            f'variable window rolling {func_name} not supported yet.')
    out_cols = tuple(sorted(set(gcetk__xdy) | set(other.columns), key=lambda
        k: str(k)))
    return out_cols


def _gen_corr_cov_out_data(out_cols, df_cols, other_cols, window_type,
    func_name):
    gkr__dhpm = not isinstance(window_type, types.Integer)
    hne__epeel = 'None'
    if gkr__dhpm:
        hne__epeel = 'bodo.utils.conversion.index_to_array(index)'
    qoifq__jcc = 'on_arr, ' if gkr__dhpm else ''
    hgw__pgrk = []
    if out_cols is None:
        return (
            f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_series_ext.get_series_data(df), bodo.hiframes.pd_series_ext.get_series_data(other), {qoifq__jcc}window, minp, center)'
            , hne__epeel)
    for eza__rsf in out_cols:
        if eza__rsf in df_cols and eza__rsf in other_cols:
            oibsx__rhty = df_cols.index(eza__rsf)
            qvw__nlpg = other_cols.index(eza__rsf)
            rwi__hjb = (
                f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {oibsx__rhty}), bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {qvw__nlpg}), {qoifq__jcc}window, minp, center)'
                )
        else:
            rwi__hjb = 'np.full(len(df), np.nan)'
        hgw__pgrk.append(rwi__hjb)
    return ', '.join(hgw__pgrk), hne__epeel


@overload_method(RollingType, 'corr', inline='always', no_unliteral=True)
def overload_rolling_corr(rolling, other=None, pairwise=None, ddof=1):
    ots__kpjgw = {'pairwise': pairwise, 'ddof': ddof}
    xrngk__kxnrj = {'pairwise': None, 'ddof': 1}
    check_unsupported_args('pandas.core.window.rolling.Rolling.corr',
        ots__kpjgw, xrngk__kxnrj, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'corr', other)


@overload_method(RollingType, 'cov', inline='always', no_unliteral=True)
def overload_rolling_cov(rolling, other=None, pairwise=None, ddof=1):
    ots__kpjgw = {'ddof': ddof, 'pairwise': pairwise}
    xrngk__kxnrj = {'ddof': 1, 'pairwise': None}
    check_unsupported_args('pandas.core.window.rolling.Rolling.cov',
        ots__kpjgw, xrngk__kxnrj, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'cov', other)


@infer
class GetItemDataFrameRolling2(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        rolling, fhkx__mzoor = args
        if isinstance(rolling, RollingType):
            gcetk__xdy = rolling.obj_type.selection if isinstance(rolling.
                obj_type, DataFrameGroupByType) else rolling.obj_type.columns
            series_select = False
            if isinstance(fhkx__mzoor, (tuple, list)):
                if len(set(fhkx__mzoor).difference(set(gcetk__xdy))) > 0:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(set(fhkx__mzoor).difference(set(gcetk__xdy))))
                selection = list(fhkx__mzoor)
            else:
                if fhkx__mzoor not in gcetk__xdy:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(fhkx__mzoor))
                selection = [fhkx__mzoor]
                series_select = True
            if rolling.on is not None:
                selection.append(rolling.on)
            hhc__yyd = RollingType(rolling.obj_type, rolling.window_type,
                rolling.on, tuple(selection), True, series_select)
            return signature(hhc__yyd, *args)


@lower_builtin('static_getitem', RollingType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@infer_getattr
class RollingAttribute(AttributeTemplate):
    key = RollingType

    def generic_resolve(self, rolling, attr):
        gcetk__xdy = ()
        if isinstance(rolling.obj_type, DataFrameGroupByType):
            gcetk__xdy = rolling.obj_type.selection
        if isinstance(rolling.obj_type, DataFrameType):
            gcetk__xdy = rolling.obj_type.columns
        if attr in gcetk__xdy:
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
    zze__qllj = obj.columns if isinstance(obj, DataFrameType
        ) else obj.df_type.columns if isinstance(obj, DataFrameGroupByType
        ) else []
    ymo__rhr = [obj.data] if isinstance(obj, SeriesType
        ) else obj.data if isinstance(obj, DataFrameType) else obj.df_type.data
    if not is_overload_none(on) and (not is_literal_type(on) or 
        get_literal_value(on) not in zze__qllj):
        raise BodoError(
            f"{func_name}.rolling(): 'on' should be a constant column name.")
    if not is_overload_none(on):
        vcwx__mgk = ymo__rhr[zze__qllj.index(get_literal_value(on))]
        if not isinstance(vcwx__mgk, types.Array
            ) or vcwx__mgk.dtype != bodo.datetime64ns:
            raise BodoError(
                f"{func_name}.rolling(): 'on' column should have datetime64 data."
                )
    if not any(isinstance(lsh__ktjhl.dtype, (types.Boolean, types.Number)) for
        lsh__ktjhl in ymo__rhr):
        raise BodoError(f'{func_name}.rolling(): No numeric types to aggregate'
            )
