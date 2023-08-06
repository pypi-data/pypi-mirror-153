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
            azzda__mpvv = 'Series'
        else:
            azzda__mpvv = 'DataFrame'
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(obj_type,
            f'{azzda__mpvv}.rolling()')
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
        enyd__ybv = [('obj', fe_type.obj_type), ('window', fe_type.
            window_type), ('min_periods', types.int64), ('center', types.bool_)
            ]
        super(RollingModel, self).__init__(dmm, fe_type, enyd__ybv)


make_attribute_wrapper(RollingType, 'obj', 'obj')
make_attribute_wrapper(RollingType, 'window', 'window')
make_attribute_wrapper(RollingType, 'center', 'center')
make_attribute_wrapper(RollingType, 'min_periods', 'min_periods')


@overload_method(DataFrameType, 'rolling', inline='always', no_unliteral=True)
def df_rolling_overload(df, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    check_runtime_cols_unsupported(df, 'DataFrame.rolling()')
    qokfz__uhy = dict(win_type=win_type, axis=axis, closed=closed)
    crtuu__iytzq = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('DataFrame.rolling', qokfz__uhy, crtuu__iytzq,
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
    qokfz__uhy = dict(win_type=win_type, axis=axis, closed=closed)
    crtuu__iytzq = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('Series.rolling', qokfz__uhy, crtuu__iytzq,
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
        hwt__apwd, vspgn__kga, fjzo__fiqop, ztvvn__kwcrw, upq__owwk = args
        dbmup__ybrp = signature.return_type
        fdpwn__poqq = cgutils.create_struct_proxy(dbmup__ybrp)(context, builder
            )
        fdpwn__poqq.obj = hwt__apwd
        fdpwn__poqq.window = vspgn__kga
        fdpwn__poqq.min_periods = fjzo__fiqop
        fdpwn__poqq.center = ztvvn__kwcrw
        context.nrt.incref(builder, signature.args[0], hwt__apwd)
        context.nrt.incref(builder, signature.args[1], vspgn__kga)
        context.nrt.incref(builder, signature.args[2], fjzo__fiqop)
        context.nrt.incref(builder, signature.args[3], ztvvn__kwcrw)
        return fdpwn__poqq._getvalue()
    on = get_literal_value(on_type)
    if isinstance(obj_type, SeriesType):
        selection = None
    elif isinstance(obj_type, DataFrameType):
        selection = obj_type.columns
    else:
        assert isinstance(obj_type, DataFrameGroupByType
            ), f'invalid obj type for rolling: {obj_type}'
        selection = obj_type.selection
    dbmup__ybrp = RollingType(obj_type, window_type, on, selection, False)
    return dbmup__ybrp(obj_type, window_type, min_periods_type, center_type,
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
    iupi__yyvd = not isinstance(rolling.window_type, types.Integer)
    qoc__vuds = 'variable' if iupi__yyvd else 'fixed'
    gkfkh__hsfn = 'None'
    if iupi__yyvd:
        gkfkh__hsfn = ('bodo.utils.conversion.index_to_array(index)' if 
            rolling.on is None else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {rolling.obj_type.columns.index(rolling.on)})'
            )
    ykrq__klz = []
    bgvrs__xjk = 'on_arr, ' if iupi__yyvd else ''
    if isinstance(rolling.obj_type, SeriesType):
        return (
            f'bodo.hiframes.rolling.rolling_{qoc__vuds}(bodo.hiframes.pd_series_ext.get_series_data(df), {bgvrs__xjk}index_arr, window, minp, center, func, raw)'
            , gkfkh__hsfn, rolling.selection)
    assert isinstance(rolling.obj_type, DataFrameType
        ), 'expected df in rolling obj'
    gve__nwkv = rolling.obj_type.data
    out_cols = []
    for vdu__jsmm in rolling.selection:
        wkuw__knc = rolling.obj_type.columns.index(vdu__jsmm)
        if vdu__jsmm == rolling.on:
            if len(rolling.selection) == 2 and rolling.series_select:
                continue
            pftkf__nmy = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {wkuw__knc})'
                )
            out_cols.append(vdu__jsmm)
        else:
            if not isinstance(gve__nwkv[wkuw__knc].dtype, (types.Boolean,
                types.Number)):
                continue
            pftkf__nmy = (
                f'bodo.hiframes.rolling.rolling_{qoc__vuds}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {wkuw__knc}), {bgvrs__xjk}index_arr, window, minp, center, func, raw)'
                )
            out_cols.append(vdu__jsmm)
        ykrq__klz.append(pftkf__nmy)
    return ', '.join(ykrq__klz), gkfkh__hsfn, tuple(out_cols)


@overload_method(RollingType, 'apply', inline='always', no_unliteral=True)
def overload_rolling_apply(rolling, func, raw=False, engine=None,
    engine_kwargs=None, args=None, kwargs=None):
    qokfz__uhy = dict(engine=engine, engine_kwargs=engine_kwargs, args=args,
        kwargs=kwargs)
    crtuu__iytzq = dict(engine=None, engine_kwargs=None, args=None, kwargs=None
        )
    check_unsupported_args('Rolling.apply', qokfz__uhy, crtuu__iytzq,
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
    qokfz__uhy = dict(win_type=win_type, axis=axis, closed=closed, method=
        method)
    crtuu__iytzq = dict(win_type=None, axis=0, closed=None, method='single')
    check_unsupported_args('GroupBy.rolling', qokfz__uhy, crtuu__iytzq,
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
        qdl__flbyb = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
        cmqoq__xyz = f"'{rolling.on}'" if isinstance(rolling.on, str
            ) else f'{rolling.on}'
        selection = ''
        if rolling.explicit_select:
            selection = '[{}]'.format(', '.join(f"'{xcb__ktzoc}'" if
                isinstance(xcb__ktzoc, str) else f'{xcb__ktzoc}' for
                xcb__ktzoc in rolling.selection if xcb__ktzoc != rolling.on))
        yjqkf__nycxv = yxo__kqifm = ''
        if fname == 'apply':
            yjqkf__nycxv = 'func, raw, args, kwargs'
            yxo__kqifm = 'func, raw, None, None, args, kwargs'
        if fname == 'corr':
            yjqkf__nycxv = yxo__kqifm = 'other, pairwise'
        if fname == 'cov':
            yjqkf__nycxv = yxo__kqifm = 'other, pairwise, ddof'
        mlc__lcpcc = (
            f'lambda df, window, minp, center, {yjqkf__nycxv}: bodo.hiframes.pd_rolling_ext.init_rolling(df, window, minp, center, {cmqoq__xyz}){selection}.{fname}({yxo__kqifm})'
            )
        qdl__flbyb += f"""  return rolling.obj.apply({mlc__lcpcc}, rolling.window, rolling.min_periods, rolling.center, {yjqkf__nycxv})
"""
        ade__pwj = {}
        exec(qdl__flbyb, {'bodo': bodo}, ade__pwj)
        impl = ade__pwj['impl']
        return impl
    mtif__qvzt = isinstance(rolling.obj_type, SeriesType)
    if fname in ('corr', 'cov'):
        out_cols = None if mtif__qvzt else _get_corr_cov_out_cols(rolling,
            other, fname)
        df_cols = None if mtif__qvzt else rolling.obj_type.columns
        other_cols = None if mtif__qvzt else other.columns
        ykrq__klz, gkfkh__hsfn = _gen_corr_cov_out_data(out_cols, df_cols,
            other_cols, rolling.window_type, fname)
    else:
        ykrq__klz, gkfkh__hsfn, out_cols = _gen_df_rolling_out_data(rolling)
    schi__qqm = mtif__qvzt or len(rolling.selection) == (1 if rolling.on is
        None else 2) and rolling.series_select
    adc__thdjk = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
    adc__thdjk += '  df = rolling.obj\n'
    adc__thdjk += '  index = {}\n'.format(
        'bodo.hiframes.pd_series_ext.get_series_index(df)' if mtif__qvzt else
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
    azzda__mpvv = 'None'
    if mtif__qvzt:
        azzda__mpvv = 'bodo.hiframes.pd_series_ext.get_series_name(df)'
    elif schi__qqm:
        vdu__jsmm = (set(out_cols) - set([rolling.on])).pop()
        azzda__mpvv = f"'{vdu__jsmm}'" if isinstance(vdu__jsmm, str) else str(
            vdu__jsmm)
    adc__thdjk += f'  name = {azzda__mpvv}\n'
    adc__thdjk += '  window = rolling.window\n'
    adc__thdjk += '  center = rolling.center\n'
    adc__thdjk += '  minp = rolling.min_periods\n'
    adc__thdjk += f'  on_arr = {gkfkh__hsfn}\n'
    if fname == 'apply':
        adc__thdjk += (
            f'  index_arr = bodo.utils.conversion.index_to_array(index)\n')
    else:
        adc__thdjk += f"  func = '{fname}'\n"
        adc__thdjk += f'  index_arr = None\n'
        adc__thdjk += f'  raw = False\n'
    if schi__qqm:
        adc__thdjk += (
            f'  return bodo.hiframes.pd_series_ext.init_series({ykrq__klz}, index, name)'
            )
        ade__pwj = {}
        jpt__uxjd = {'bodo': bodo}
        exec(adc__thdjk, jpt__uxjd, ade__pwj)
        impl = ade__pwj['impl']
        return impl
    return bodo.hiframes.dataframe_impl._gen_init_df(adc__thdjk, out_cols,
        ykrq__klz)


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
        vzx__cksv = create_rolling_overload(fname)
        overload_method(RollingType, fname, inline='always', no_unliteral=True
            )(vzx__cksv)


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
    rqqfr__lyle = rolling.selection
    if rolling.on is not None:
        raise BodoError(
            f'variable window rolling {func_name} not supported yet.')
    out_cols = tuple(sorted(set(rqqfr__lyle) | set(other.columns), key=lambda
        k: str(k)))
    return out_cols


def _gen_corr_cov_out_data(out_cols, df_cols, other_cols, window_type,
    func_name):
    iupi__yyvd = not isinstance(window_type, types.Integer)
    gkfkh__hsfn = 'None'
    if iupi__yyvd:
        gkfkh__hsfn = 'bodo.utils.conversion.index_to_array(index)'
    bgvrs__xjk = 'on_arr, ' if iupi__yyvd else ''
    ykrq__klz = []
    if out_cols is None:
        return (
            f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_series_ext.get_series_data(df), bodo.hiframes.pd_series_ext.get_series_data(other), {bgvrs__xjk}window, minp, center)'
            , gkfkh__hsfn)
    for vdu__jsmm in out_cols:
        if vdu__jsmm in df_cols and vdu__jsmm in other_cols:
            muqx__sopn = df_cols.index(vdu__jsmm)
            agm__jsz = other_cols.index(vdu__jsmm)
            pftkf__nmy = (
                f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {muqx__sopn}), bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {agm__jsz}), {bgvrs__xjk}window, minp, center)'
                )
        else:
            pftkf__nmy = 'np.full(len(df), np.nan)'
        ykrq__klz.append(pftkf__nmy)
    return ', '.join(ykrq__klz), gkfkh__hsfn


@overload_method(RollingType, 'corr', inline='always', no_unliteral=True)
def overload_rolling_corr(rolling, other=None, pairwise=None, ddof=1):
    vsi__lvazq = {'pairwise': pairwise, 'ddof': ddof}
    yczo__gumwn = {'pairwise': None, 'ddof': 1}
    check_unsupported_args('pandas.core.window.rolling.Rolling.corr',
        vsi__lvazq, yczo__gumwn, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'corr', other)


@overload_method(RollingType, 'cov', inline='always', no_unliteral=True)
def overload_rolling_cov(rolling, other=None, pairwise=None, ddof=1):
    vsi__lvazq = {'ddof': ddof, 'pairwise': pairwise}
    yczo__gumwn = {'ddof': 1, 'pairwise': None}
    check_unsupported_args('pandas.core.window.rolling.Rolling.cov',
        vsi__lvazq, yczo__gumwn, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'cov', other)


@infer
class GetItemDataFrameRolling2(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        rolling, eqpz__xdkh = args
        if isinstance(rolling, RollingType):
            rqqfr__lyle = rolling.obj_type.selection if isinstance(rolling.
                obj_type, DataFrameGroupByType) else rolling.obj_type.columns
            series_select = False
            if isinstance(eqpz__xdkh, (tuple, list)):
                if len(set(eqpz__xdkh).difference(set(rqqfr__lyle))) > 0:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(set(eqpz__xdkh).difference(set(rqqfr__lyle))))
                selection = list(eqpz__xdkh)
            else:
                if eqpz__xdkh not in rqqfr__lyle:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(eqpz__xdkh))
                selection = [eqpz__xdkh]
                series_select = True
            if rolling.on is not None:
                selection.append(rolling.on)
            gax__cbcck = RollingType(rolling.obj_type, rolling.window_type,
                rolling.on, tuple(selection), True, series_select)
            return signature(gax__cbcck, *args)


@lower_builtin('static_getitem', RollingType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@infer_getattr
class RollingAttribute(AttributeTemplate):
    key = RollingType

    def generic_resolve(self, rolling, attr):
        rqqfr__lyle = ()
        if isinstance(rolling.obj_type, DataFrameGroupByType):
            rqqfr__lyle = rolling.obj_type.selection
        if isinstance(rolling.obj_type, DataFrameType):
            rqqfr__lyle = rolling.obj_type.columns
        if attr in rqqfr__lyle:
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
    imqfg__kfwhh = obj.columns if isinstance(obj, DataFrameType
        ) else obj.df_type.columns if isinstance(obj, DataFrameGroupByType
        ) else []
    gve__nwkv = [obj.data] if isinstance(obj, SeriesType
        ) else obj.data if isinstance(obj, DataFrameType) else obj.df_type.data
    if not is_overload_none(on) and (not is_literal_type(on) or 
        get_literal_value(on) not in imqfg__kfwhh):
        raise BodoError(
            f"{func_name}.rolling(): 'on' should be a constant column name.")
    if not is_overload_none(on):
        mka__gdhwg = gve__nwkv[imqfg__kfwhh.index(get_literal_value(on))]
        if not isinstance(mka__gdhwg, types.Array
            ) or mka__gdhwg.dtype != bodo.datetime64ns:
            raise BodoError(
                f"{func_name}.rolling(): 'on' column should have datetime64 data."
                )
    if not any(isinstance(qolr__kol.dtype, (types.Boolean, types.Number)) for
        qolr__kol in gve__nwkv):
        raise BodoError(f'{func_name}.rolling(): No numeric types to aggregate'
            )
