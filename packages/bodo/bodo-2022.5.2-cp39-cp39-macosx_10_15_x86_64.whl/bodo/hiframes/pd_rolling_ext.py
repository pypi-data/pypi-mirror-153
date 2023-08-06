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
            nyt__mpo = 'Series'
        else:
            nyt__mpo = 'DataFrame'
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(obj_type,
            f'{nyt__mpo}.rolling()')
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
        lkw__blmj = [('obj', fe_type.obj_type), ('window', fe_type.
            window_type), ('min_periods', types.int64), ('center', types.bool_)
            ]
        super(RollingModel, self).__init__(dmm, fe_type, lkw__blmj)


make_attribute_wrapper(RollingType, 'obj', 'obj')
make_attribute_wrapper(RollingType, 'window', 'window')
make_attribute_wrapper(RollingType, 'center', 'center')
make_attribute_wrapper(RollingType, 'min_periods', 'min_periods')


@overload_method(DataFrameType, 'rolling', inline='always', no_unliteral=True)
def df_rolling_overload(df, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    check_runtime_cols_unsupported(df, 'DataFrame.rolling()')
    xleay__wtqn = dict(win_type=win_type, axis=axis, closed=closed)
    vkjh__tebm = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('DataFrame.rolling', xleay__wtqn, vkjh__tebm,
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
    xleay__wtqn = dict(win_type=win_type, axis=axis, closed=closed)
    vkjh__tebm = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('Series.rolling', xleay__wtqn, vkjh__tebm,
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
        zuxem__eieb, jkzve__lly, fgjpp__wfglh, swwx__azi, qtxrj__sxs = args
        lbwx__ccxg = signature.return_type
        zejj__bem = cgutils.create_struct_proxy(lbwx__ccxg)(context, builder)
        zejj__bem.obj = zuxem__eieb
        zejj__bem.window = jkzve__lly
        zejj__bem.min_periods = fgjpp__wfglh
        zejj__bem.center = swwx__azi
        context.nrt.incref(builder, signature.args[0], zuxem__eieb)
        context.nrt.incref(builder, signature.args[1], jkzve__lly)
        context.nrt.incref(builder, signature.args[2], fgjpp__wfglh)
        context.nrt.incref(builder, signature.args[3], swwx__azi)
        return zejj__bem._getvalue()
    on = get_literal_value(on_type)
    if isinstance(obj_type, SeriesType):
        selection = None
    elif isinstance(obj_type, DataFrameType):
        selection = obj_type.columns
    else:
        assert isinstance(obj_type, DataFrameGroupByType
            ), f'invalid obj type for rolling: {obj_type}'
        selection = obj_type.selection
    lbwx__ccxg = RollingType(obj_type, window_type, on, selection, False)
    return lbwx__ccxg(obj_type, window_type, min_periods_type, center_type,
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
    crerr__nal = not isinstance(rolling.window_type, types.Integer)
    tdwlh__rlza = 'variable' if crerr__nal else 'fixed'
    rjgo__yjs = 'None'
    if crerr__nal:
        rjgo__yjs = ('bodo.utils.conversion.index_to_array(index)' if 
            rolling.on is None else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {rolling.obj_type.columns.index(rolling.on)})'
            )
    qhxg__efm = []
    ybfj__vgs = 'on_arr, ' if crerr__nal else ''
    if isinstance(rolling.obj_type, SeriesType):
        return (
            f'bodo.hiframes.rolling.rolling_{tdwlh__rlza}(bodo.hiframes.pd_series_ext.get_series_data(df), {ybfj__vgs}index_arr, window, minp, center, func, raw)'
            , rjgo__yjs, rolling.selection)
    assert isinstance(rolling.obj_type, DataFrameType
        ), 'expected df in rolling obj'
    fwpm__kfsw = rolling.obj_type.data
    out_cols = []
    for jcko__evhc in rolling.selection:
        rjfl__pso = rolling.obj_type.columns.index(jcko__evhc)
        if jcko__evhc == rolling.on:
            if len(rolling.selection) == 2 and rolling.series_select:
                continue
            rqsz__zuqvz = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {rjfl__pso})'
                )
            out_cols.append(jcko__evhc)
        else:
            if not isinstance(fwpm__kfsw[rjfl__pso].dtype, (types.Boolean,
                types.Number)):
                continue
            rqsz__zuqvz = (
                f'bodo.hiframes.rolling.rolling_{tdwlh__rlza}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {rjfl__pso}), {ybfj__vgs}index_arr, window, minp, center, func, raw)'
                )
            out_cols.append(jcko__evhc)
        qhxg__efm.append(rqsz__zuqvz)
    return ', '.join(qhxg__efm), rjgo__yjs, tuple(out_cols)


@overload_method(RollingType, 'apply', inline='always', no_unliteral=True)
def overload_rolling_apply(rolling, func, raw=False, engine=None,
    engine_kwargs=None, args=None, kwargs=None):
    xleay__wtqn = dict(engine=engine, engine_kwargs=engine_kwargs, args=
        args, kwargs=kwargs)
    vkjh__tebm = dict(engine=None, engine_kwargs=None, args=None, kwargs=None)
    check_unsupported_args('Rolling.apply', xleay__wtqn, vkjh__tebm,
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
    xleay__wtqn = dict(win_type=win_type, axis=axis, closed=closed, method=
        method)
    vkjh__tebm = dict(win_type=None, axis=0, closed=None, method='single')
    check_unsupported_args('GroupBy.rolling', xleay__wtqn, vkjh__tebm,
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
        fziq__nropp = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
        eixo__dxpt = f"'{rolling.on}'" if isinstance(rolling.on, str
            ) else f'{rolling.on}'
        selection = ''
        if rolling.explicit_select:
            selection = '[{}]'.format(', '.join(f"'{evau__wqn}'" if
                isinstance(evau__wqn, str) else f'{evau__wqn}' for
                evau__wqn in rolling.selection if evau__wqn != rolling.on))
        rgv__lmikx = quja__iyvmc = ''
        if fname == 'apply':
            rgv__lmikx = 'func, raw, args, kwargs'
            quja__iyvmc = 'func, raw, None, None, args, kwargs'
        if fname == 'corr':
            rgv__lmikx = quja__iyvmc = 'other, pairwise'
        if fname == 'cov':
            rgv__lmikx = quja__iyvmc = 'other, pairwise, ddof'
        viryo__xiq = (
            f'lambda df, window, minp, center, {rgv__lmikx}: bodo.hiframes.pd_rolling_ext.init_rolling(df, window, minp, center, {eixo__dxpt}){selection}.{fname}({quja__iyvmc})'
            )
        fziq__nropp += f"""  return rolling.obj.apply({viryo__xiq}, rolling.window, rolling.min_periods, rolling.center, {rgv__lmikx})
"""
        ifd__zbvba = {}
        exec(fziq__nropp, {'bodo': bodo}, ifd__zbvba)
        impl = ifd__zbvba['impl']
        return impl
    xlfpf__brpx = isinstance(rolling.obj_type, SeriesType)
    if fname in ('corr', 'cov'):
        out_cols = None if xlfpf__brpx else _get_corr_cov_out_cols(rolling,
            other, fname)
        df_cols = None if xlfpf__brpx else rolling.obj_type.columns
        other_cols = None if xlfpf__brpx else other.columns
        qhxg__efm, rjgo__yjs = _gen_corr_cov_out_data(out_cols, df_cols,
            other_cols, rolling.window_type, fname)
    else:
        qhxg__efm, rjgo__yjs, out_cols = _gen_df_rolling_out_data(rolling)
    oiy__pwtwe = xlfpf__brpx or len(rolling.selection) == (1 if rolling.on is
        None else 2) and rolling.series_select
    eatj__bvc = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
    eatj__bvc += '  df = rolling.obj\n'
    eatj__bvc += '  index = {}\n'.format(
        'bodo.hiframes.pd_series_ext.get_series_index(df)' if xlfpf__brpx else
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
    nyt__mpo = 'None'
    if xlfpf__brpx:
        nyt__mpo = 'bodo.hiframes.pd_series_ext.get_series_name(df)'
    elif oiy__pwtwe:
        jcko__evhc = (set(out_cols) - set([rolling.on])).pop()
        nyt__mpo = f"'{jcko__evhc}'" if isinstance(jcko__evhc, str) else str(
            jcko__evhc)
    eatj__bvc += f'  name = {nyt__mpo}\n'
    eatj__bvc += '  window = rolling.window\n'
    eatj__bvc += '  center = rolling.center\n'
    eatj__bvc += '  minp = rolling.min_periods\n'
    eatj__bvc += f'  on_arr = {rjgo__yjs}\n'
    if fname == 'apply':
        eatj__bvc += (
            f'  index_arr = bodo.utils.conversion.index_to_array(index)\n')
    else:
        eatj__bvc += f"  func = '{fname}'\n"
        eatj__bvc += f'  index_arr = None\n'
        eatj__bvc += f'  raw = False\n'
    if oiy__pwtwe:
        eatj__bvc += (
            f'  return bodo.hiframes.pd_series_ext.init_series({qhxg__efm}, index, name)'
            )
        ifd__zbvba = {}
        fwjb__dlogu = {'bodo': bodo}
        exec(eatj__bvc, fwjb__dlogu, ifd__zbvba)
        impl = ifd__zbvba['impl']
        return impl
    return bodo.hiframes.dataframe_impl._gen_init_df(eatj__bvc, out_cols,
        qhxg__efm)


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
        yytsq__jky = create_rolling_overload(fname)
        overload_method(RollingType, fname, inline='always', no_unliteral=True
            )(yytsq__jky)


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
    yttu__nneo = rolling.selection
    if rolling.on is not None:
        raise BodoError(
            f'variable window rolling {func_name} not supported yet.')
    out_cols = tuple(sorted(set(yttu__nneo) | set(other.columns), key=lambda
        k: str(k)))
    return out_cols


def _gen_corr_cov_out_data(out_cols, df_cols, other_cols, window_type,
    func_name):
    crerr__nal = not isinstance(window_type, types.Integer)
    rjgo__yjs = 'None'
    if crerr__nal:
        rjgo__yjs = 'bodo.utils.conversion.index_to_array(index)'
    ybfj__vgs = 'on_arr, ' if crerr__nal else ''
    qhxg__efm = []
    if out_cols is None:
        return (
            f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_series_ext.get_series_data(df), bodo.hiframes.pd_series_ext.get_series_data(other), {ybfj__vgs}window, minp, center)'
            , rjgo__yjs)
    for jcko__evhc in out_cols:
        if jcko__evhc in df_cols and jcko__evhc in other_cols:
            thjyd__hwv = df_cols.index(jcko__evhc)
            rsv__afo = other_cols.index(jcko__evhc)
            rqsz__zuqvz = (
                f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {thjyd__hwv}), bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {rsv__afo}), {ybfj__vgs}window, minp, center)'
                )
        else:
            rqsz__zuqvz = 'np.full(len(df), np.nan)'
        qhxg__efm.append(rqsz__zuqvz)
    return ', '.join(qhxg__efm), rjgo__yjs


@overload_method(RollingType, 'corr', inline='always', no_unliteral=True)
def overload_rolling_corr(rolling, other=None, pairwise=None, ddof=1):
    gfg__dtcjb = {'pairwise': pairwise, 'ddof': ddof}
    lwaif__xnk = {'pairwise': None, 'ddof': 1}
    check_unsupported_args('pandas.core.window.rolling.Rolling.corr',
        gfg__dtcjb, lwaif__xnk, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'corr', other)


@overload_method(RollingType, 'cov', inline='always', no_unliteral=True)
def overload_rolling_cov(rolling, other=None, pairwise=None, ddof=1):
    gfg__dtcjb = {'ddof': ddof, 'pairwise': pairwise}
    lwaif__xnk = {'ddof': 1, 'pairwise': None}
    check_unsupported_args('pandas.core.window.rolling.Rolling.cov',
        gfg__dtcjb, lwaif__xnk, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'cov', other)


@infer
class GetItemDataFrameRolling2(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        rolling, cqt__ubzkd = args
        if isinstance(rolling, RollingType):
            yttu__nneo = rolling.obj_type.selection if isinstance(rolling.
                obj_type, DataFrameGroupByType) else rolling.obj_type.columns
            series_select = False
            if isinstance(cqt__ubzkd, (tuple, list)):
                if len(set(cqt__ubzkd).difference(set(yttu__nneo))) > 0:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(set(cqt__ubzkd).difference(set(yttu__nneo))))
                selection = list(cqt__ubzkd)
            else:
                if cqt__ubzkd not in yttu__nneo:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(cqt__ubzkd))
                selection = [cqt__ubzkd]
                series_select = True
            if rolling.on is not None:
                selection.append(rolling.on)
            ftctp__nxiof = RollingType(rolling.obj_type, rolling.
                window_type, rolling.on, tuple(selection), True, series_select)
            return signature(ftctp__nxiof, *args)


@lower_builtin('static_getitem', RollingType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@infer_getattr
class RollingAttribute(AttributeTemplate):
    key = RollingType

    def generic_resolve(self, rolling, attr):
        yttu__nneo = ()
        if isinstance(rolling.obj_type, DataFrameGroupByType):
            yttu__nneo = rolling.obj_type.selection
        if isinstance(rolling.obj_type, DataFrameType):
            yttu__nneo = rolling.obj_type.columns
        if attr in yttu__nneo:
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
    svm__hiuk = obj.columns if isinstance(obj, DataFrameType
        ) else obj.df_type.columns if isinstance(obj, DataFrameGroupByType
        ) else []
    fwpm__kfsw = [obj.data] if isinstance(obj, SeriesType
        ) else obj.data if isinstance(obj, DataFrameType) else obj.df_type.data
    if not is_overload_none(on) and (not is_literal_type(on) or 
        get_literal_value(on) not in svm__hiuk):
        raise BodoError(
            f"{func_name}.rolling(): 'on' should be a constant column name.")
    if not is_overload_none(on):
        spnhf__xzwxi = fwpm__kfsw[svm__hiuk.index(get_literal_value(on))]
        if not isinstance(spnhf__xzwxi, types.Array
            ) or spnhf__xzwxi.dtype != bodo.datetime64ns:
            raise BodoError(
                f"{func_name}.rolling(): 'on' column should have datetime64 data."
                )
    if not any(isinstance(eznco__fjwe.dtype, (types.Boolean, types.Number)) for
        eznco__fjwe in fwpm__kfsw):
        raise BodoError(f'{func_name}.rolling(): No numeric types to aggregate'
            )
