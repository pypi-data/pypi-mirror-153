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
            dqv__czica = 'Series'
        else:
            dqv__czica = 'DataFrame'
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(obj_type,
            f'{dqv__czica}.rolling()')
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
        byfv__yukk = [('obj', fe_type.obj_type), ('window', fe_type.
            window_type), ('min_periods', types.int64), ('center', types.bool_)
            ]
        super(RollingModel, self).__init__(dmm, fe_type, byfv__yukk)


make_attribute_wrapper(RollingType, 'obj', 'obj')
make_attribute_wrapper(RollingType, 'window', 'window')
make_attribute_wrapper(RollingType, 'center', 'center')
make_attribute_wrapper(RollingType, 'min_periods', 'min_periods')


@overload_method(DataFrameType, 'rolling', inline='always', no_unliteral=True)
def df_rolling_overload(df, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    check_runtime_cols_unsupported(df, 'DataFrame.rolling()')
    zfdaw__wtvre = dict(win_type=win_type, axis=axis, closed=closed)
    cqj__rwvse = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('DataFrame.rolling', zfdaw__wtvre, cqj__rwvse,
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
    zfdaw__wtvre = dict(win_type=win_type, axis=axis, closed=closed)
    cqj__rwvse = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('Series.rolling', zfdaw__wtvre, cqj__rwvse,
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
        frd__xyp, utqei__oxq, klqgr__and, urgis__mfvcj, wgvuu__ibovn = args
        lxdj__tgrim = signature.return_type
        yreg__yjk = cgutils.create_struct_proxy(lxdj__tgrim)(context, builder)
        yreg__yjk.obj = frd__xyp
        yreg__yjk.window = utqei__oxq
        yreg__yjk.min_periods = klqgr__and
        yreg__yjk.center = urgis__mfvcj
        context.nrt.incref(builder, signature.args[0], frd__xyp)
        context.nrt.incref(builder, signature.args[1], utqei__oxq)
        context.nrt.incref(builder, signature.args[2], klqgr__and)
        context.nrt.incref(builder, signature.args[3], urgis__mfvcj)
        return yreg__yjk._getvalue()
    on = get_literal_value(on_type)
    if isinstance(obj_type, SeriesType):
        selection = None
    elif isinstance(obj_type, DataFrameType):
        selection = obj_type.columns
    else:
        assert isinstance(obj_type, DataFrameGroupByType
            ), f'invalid obj type for rolling: {obj_type}'
        selection = obj_type.selection
    lxdj__tgrim = RollingType(obj_type, window_type, on, selection, False)
    return lxdj__tgrim(obj_type, window_type, min_periods_type, center_type,
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
    afaw__qcl = not isinstance(rolling.window_type, types.Integer)
    byajj__fyjtz = 'variable' if afaw__qcl else 'fixed'
    wir__fya = 'None'
    if afaw__qcl:
        wir__fya = ('bodo.utils.conversion.index_to_array(index)' if 
            rolling.on is None else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {rolling.obj_type.columns.index(rolling.on)})'
            )
    qbc__aetd = []
    khogu__odjz = 'on_arr, ' if afaw__qcl else ''
    if isinstance(rolling.obj_type, SeriesType):
        return (
            f'bodo.hiframes.rolling.rolling_{byajj__fyjtz}(bodo.hiframes.pd_series_ext.get_series_data(df), {khogu__odjz}index_arr, window, minp, center, func, raw)'
            , wir__fya, rolling.selection)
    assert isinstance(rolling.obj_type, DataFrameType
        ), 'expected df in rolling obj'
    vjls__kvmw = rolling.obj_type.data
    out_cols = []
    for qjokt__vos in rolling.selection:
        gsj__xters = rolling.obj_type.columns.index(qjokt__vos)
        if qjokt__vos == rolling.on:
            if len(rolling.selection) == 2 and rolling.series_select:
                continue
            sbhqt__jkvo = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {gsj__xters})'
                )
            out_cols.append(qjokt__vos)
        else:
            if not isinstance(vjls__kvmw[gsj__xters].dtype, (types.Boolean,
                types.Number)):
                continue
            sbhqt__jkvo = (
                f'bodo.hiframes.rolling.rolling_{byajj__fyjtz}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {gsj__xters}), {khogu__odjz}index_arr, window, minp, center, func, raw)'
                )
            out_cols.append(qjokt__vos)
        qbc__aetd.append(sbhqt__jkvo)
    return ', '.join(qbc__aetd), wir__fya, tuple(out_cols)


@overload_method(RollingType, 'apply', inline='always', no_unliteral=True)
def overload_rolling_apply(rolling, func, raw=False, engine=None,
    engine_kwargs=None, args=None, kwargs=None):
    zfdaw__wtvre = dict(engine=engine, engine_kwargs=engine_kwargs, args=
        args, kwargs=kwargs)
    cqj__rwvse = dict(engine=None, engine_kwargs=None, args=None, kwargs=None)
    check_unsupported_args('Rolling.apply', zfdaw__wtvre, cqj__rwvse,
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
    zfdaw__wtvre = dict(win_type=win_type, axis=axis, closed=closed, method
        =method)
    cqj__rwvse = dict(win_type=None, axis=0, closed=None, method='single')
    check_unsupported_args('GroupBy.rolling', zfdaw__wtvre, cqj__rwvse,
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
        iqmv__mbm = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
        mfp__bdeuw = f"'{rolling.on}'" if isinstance(rolling.on, str
            ) else f'{rolling.on}'
        selection = ''
        if rolling.explicit_select:
            selection = '[{}]'.format(', '.join(f"'{sxkp__jvjsu}'" if
                isinstance(sxkp__jvjsu, str) else f'{sxkp__jvjsu}' for
                sxkp__jvjsu in rolling.selection if sxkp__jvjsu != rolling.on))
        xtvee__hjv = dwan__asjl = ''
        if fname == 'apply':
            xtvee__hjv = 'func, raw, args, kwargs'
            dwan__asjl = 'func, raw, None, None, args, kwargs'
        if fname == 'corr':
            xtvee__hjv = dwan__asjl = 'other, pairwise'
        if fname == 'cov':
            xtvee__hjv = dwan__asjl = 'other, pairwise, ddof'
        hyc__ejsk = (
            f'lambda df, window, minp, center, {xtvee__hjv}: bodo.hiframes.pd_rolling_ext.init_rolling(df, window, minp, center, {mfp__bdeuw}){selection}.{fname}({dwan__asjl})'
            )
        iqmv__mbm += f"""  return rolling.obj.apply({hyc__ejsk}, rolling.window, rolling.min_periods, rolling.center, {xtvee__hjv})
"""
        jhd__vxwhi = {}
        exec(iqmv__mbm, {'bodo': bodo}, jhd__vxwhi)
        impl = jhd__vxwhi['impl']
        return impl
    sjnv__bbhao = isinstance(rolling.obj_type, SeriesType)
    if fname in ('corr', 'cov'):
        out_cols = None if sjnv__bbhao else _get_corr_cov_out_cols(rolling,
            other, fname)
        df_cols = None if sjnv__bbhao else rolling.obj_type.columns
        other_cols = None if sjnv__bbhao else other.columns
        qbc__aetd, wir__fya = _gen_corr_cov_out_data(out_cols, df_cols,
            other_cols, rolling.window_type, fname)
    else:
        qbc__aetd, wir__fya, out_cols = _gen_df_rolling_out_data(rolling)
    hytrd__ckmlo = sjnv__bbhao or len(rolling.selection) == (1 if rolling.
        on is None else 2) and rolling.series_select
    pgsuh__hucp = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
    pgsuh__hucp += '  df = rolling.obj\n'
    pgsuh__hucp += '  index = {}\n'.format(
        'bodo.hiframes.pd_series_ext.get_series_index(df)' if sjnv__bbhao else
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
    dqv__czica = 'None'
    if sjnv__bbhao:
        dqv__czica = 'bodo.hiframes.pd_series_ext.get_series_name(df)'
    elif hytrd__ckmlo:
        qjokt__vos = (set(out_cols) - set([rolling.on])).pop()
        dqv__czica = f"'{qjokt__vos}'" if isinstance(qjokt__vos, str) else str(
            qjokt__vos)
    pgsuh__hucp += f'  name = {dqv__czica}\n'
    pgsuh__hucp += '  window = rolling.window\n'
    pgsuh__hucp += '  center = rolling.center\n'
    pgsuh__hucp += '  minp = rolling.min_periods\n'
    pgsuh__hucp += f'  on_arr = {wir__fya}\n'
    if fname == 'apply':
        pgsuh__hucp += (
            f'  index_arr = bodo.utils.conversion.index_to_array(index)\n')
    else:
        pgsuh__hucp += f"  func = '{fname}'\n"
        pgsuh__hucp += f'  index_arr = None\n'
        pgsuh__hucp += f'  raw = False\n'
    if hytrd__ckmlo:
        pgsuh__hucp += (
            f'  return bodo.hiframes.pd_series_ext.init_series({qbc__aetd}, index, name)'
            )
        jhd__vxwhi = {}
        rqjoa__tliu = {'bodo': bodo}
        exec(pgsuh__hucp, rqjoa__tliu, jhd__vxwhi)
        impl = jhd__vxwhi['impl']
        return impl
    return bodo.hiframes.dataframe_impl._gen_init_df(pgsuh__hucp, out_cols,
        qbc__aetd)


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
        pmli__ciqhg = create_rolling_overload(fname)
        overload_method(RollingType, fname, inline='always', no_unliteral=True
            )(pmli__ciqhg)


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
    yru__jzp = rolling.selection
    if rolling.on is not None:
        raise BodoError(
            f'variable window rolling {func_name} not supported yet.')
    out_cols = tuple(sorted(set(yru__jzp) | set(other.columns), key=lambda
        k: str(k)))
    return out_cols


def _gen_corr_cov_out_data(out_cols, df_cols, other_cols, window_type,
    func_name):
    afaw__qcl = not isinstance(window_type, types.Integer)
    wir__fya = 'None'
    if afaw__qcl:
        wir__fya = 'bodo.utils.conversion.index_to_array(index)'
    khogu__odjz = 'on_arr, ' if afaw__qcl else ''
    qbc__aetd = []
    if out_cols is None:
        return (
            f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_series_ext.get_series_data(df), bodo.hiframes.pd_series_ext.get_series_data(other), {khogu__odjz}window, minp, center)'
            , wir__fya)
    for qjokt__vos in out_cols:
        if qjokt__vos in df_cols and qjokt__vos in other_cols:
            brd__enzd = df_cols.index(qjokt__vos)
            fbzcr__mwz = other_cols.index(qjokt__vos)
            sbhqt__jkvo = (
                f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {brd__enzd}), bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {fbzcr__mwz}), {khogu__odjz}window, minp, center)'
                )
        else:
            sbhqt__jkvo = 'np.full(len(df), np.nan)'
        qbc__aetd.append(sbhqt__jkvo)
    return ', '.join(qbc__aetd), wir__fya


@overload_method(RollingType, 'corr', inline='always', no_unliteral=True)
def overload_rolling_corr(rolling, other=None, pairwise=None, ddof=1):
    biy__tfobj = {'pairwise': pairwise, 'ddof': ddof}
    hcth__gxe = {'pairwise': None, 'ddof': 1}
    check_unsupported_args('pandas.core.window.rolling.Rolling.corr',
        biy__tfobj, hcth__gxe, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'corr', other)


@overload_method(RollingType, 'cov', inline='always', no_unliteral=True)
def overload_rolling_cov(rolling, other=None, pairwise=None, ddof=1):
    biy__tfobj = {'ddof': ddof, 'pairwise': pairwise}
    hcth__gxe = {'ddof': 1, 'pairwise': None}
    check_unsupported_args('pandas.core.window.rolling.Rolling.cov',
        biy__tfobj, hcth__gxe, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'cov', other)


@infer
class GetItemDataFrameRolling2(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        rolling, pvm__duqi = args
        if isinstance(rolling, RollingType):
            yru__jzp = rolling.obj_type.selection if isinstance(rolling.
                obj_type, DataFrameGroupByType) else rolling.obj_type.columns
            series_select = False
            if isinstance(pvm__duqi, (tuple, list)):
                if len(set(pvm__duqi).difference(set(yru__jzp))) > 0:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(set(pvm__duqi).difference(set(yru__jzp))))
                selection = list(pvm__duqi)
            else:
                if pvm__duqi not in yru__jzp:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(pvm__duqi))
                selection = [pvm__duqi]
                series_select = True
            if rolling.on is not None:
                selection.append(rolling.on)
            bbrrm__xmcb = RollingType(rolling.obj_type, rolling.window_type,
                rolling.on, tuple(selection), True, series_select)
            return signature(bbrrm__xmcb, *args)


@lower_builtin('static_getitem', RollingType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@infer_getattr
class RollingAttribute(AttributeTemplate):
    key = RollingType

    def generic_resolve(self, rolling, attr):
        yru__jzp = ()
        if isinstance(rolling.obj_type, DataFrameGroupByType):
            yru__jzp = rolling.obj_type.selection
        if isinstance(rolling.obj_type, DataFrameType):
            yru__jzp = rolling.obj_type.columns
        if attr in yru__jzp:
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
    glua__lnec = obj.columns if isinstance(obj, DataFrameType
        ) else obj.df_type.columns if isinstance(obj, DataFrameGroupByType
        ) else []
    vjls__kvmw = [obj.data] if isinstance(obj, SeriesType
        ) else obj.data if isinstance(obj, DataFrameType) else obj.df_type.data
    if not is_overload_none(on) and (not is_literal_type(on) or 
        get_literal_value(on) not in glua__lnec):
        raise BodoError(
            f"{func_name}.rolling(): 'on' should be a constant column name.")
    if not is_overload_none(on):
        mlt__kavt = vjls__kvmw[glua__lnec.index(get_literal_value(on))]
        if not isinstance(mlt__kavt, types.Array
            ) or mlt__kavt.dtype != bodo.datetime64ns:
            raise BodoError(
                f"{func_name}.rolling(): 'on' column should have datetime64 data."
                )
    if not any(isinstance(tpqy__jqqwi.dtype, (types.Boolean, types.Number)) for
        tpqy__jqqwi in vjls__kvmw):
        raise BodoError(f'{func_name}.rolling(): No numeric types to aggregate'
            )
