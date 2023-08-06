"""
Indexing support for pd.DataFrame type.
"""
import operator
import numpy as np
import pandas as pd
from numba.core import cgutils, types
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, register_model
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType, check_runtime_cols_unsupported
from bodo.utils.transform import gen_const_tup
from bodo.utils.typing import BodoError, get_overload_const_int, get_overload_const_list, get_overload_const_str, is_immutable_array, is_list_like_index_type, is_overload_constant_int, is_overload_constant_list, is_overload_constant_str, raise_bodo_error


@infer_global(operator.getitem)
class DataFrameGetItemTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        check_runtime_cols_unsupported(args[0], 'DataFrame getitem (df[])')
        if isinstance(args[0], DataFrameType):
            return self.typecheck_df_getitem(args)
        elif isinstance(args[0], DataFrameLocType):
            return self.typecheck_loc_getitem(args)
        else:
            return

    def typecheck_loc_getitem(self, args):
        I = args[0]
        idx = args[1]
        df = I.df_type
        if isinstance(df.columns[0], tuple):
            raise_bodo_error(
                'DataFrame.loc[] getitem (location-based indexing) with multi-indexed columns not supported yet'
                )
        if is_list_like_index_type(idx) and idx.dtype == types.bool_:
            ihcqt__htmjm = idx
            gse__yiqi = df.data
            rxelm__zqvxe = df.columns
            aow__fobsy = self.replace_range_with_numeric_idx_if_needed(df,
                ihcqt__htmjm)
            nfjeh__shsip = DataFrameType(gse__yiqi, aow__fobsy, rxelm__zqvxe)
            return nfjeh__shsip(*args)
        if isinstance(idx, types.BaseTuple) and len(idx) == 2:
            uafr__fplkg = idx.types[0]
            bskiy__lro = idx.types[1]
            if isinstance(uafr__fplkg, types.Integer):
                if not isinstance(df.index, bodo.hiframes.pd_index_ext.
                    RangeIndexType):
                    raise_bodo_error(
                        'Dataframe.loc[int, col_ind] getitem only supported for dataframes with RangeIndexes'
                        )
                if is_overload_constant_str(bskiy__lro):
                    nwy__dyra = get_overload_const_str(bskiy__lro)
                    if nwy__dyra not in df.columns:
                        raise_bodo_error(
                            'dataframe {} does not include column {}'.
                            format(df, nwy__dyra))
                    psoq__lkmj = df.columns.index(nwy__dyra)
                    return df.data[psoq__lkmj].dtype(*args)
                if isinstance(bskiy__lro, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                        )
                else:
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
                        )
            if is_list_like_index_type(uafr__fplkg
                ) and uafr__fplkg.dtype == types.bool_ or isinstance(
                uafr__fplkg, types.SliceType):
                aow__fobsy = self.replace_range_with_numeric_idx_if_needed(df,
                    uafr__fplkg)
                if is_overload_constant_str(bskiy__lro):
                    htzht__xaz = get_overload_const_str(bskiy__lro)
                    if htzht__xaz not in df.columns:
                        raise_bodo_error(
                            f'dataframe {df} does not include column {htzht__xaz}'
                            )
                    psoq__lkmj = df.columns.index(htzht__xaz)
                    uju__mjr = df.data[psoq__lkmj]
                    bmn__mzep = uju__mjr.dtype
                    uhw__hzvi = types.literal(df.columns[psoq__lkmj])
                    nfjeh__shsip = bodo.SeriesType(bmn__mzep, uju__mjr,
                        aow__fobsy, uhw__hzvi)
                    return nfjeh__shsip(*args)
                if isinstance(bskiy__lro, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                        )
                elif is_overload_constant_list(bskiy__lro):
                    dsi__ogzqt = get_overload_const_list(bskiy__lro)
                    itts__xlm = types.unliteral(bskiy__lro)
                    if itts__xlm.dtype == types.bool_:
                        if len(df.columns) != len(dsi__ogzqt):
                            raise_bodo_error(
                                f'dataframe {df} has {len(df.columns)} columns, but boolean array used with DataFrame.loc[] {dsi__ogzqt} has {len(dsi__ogzqt)} values'
                                )
                        hud__mkoj = []
                        hri__fzw = []
                        for nalsi__kwsal in range(len(dsi__ogzqt)):
                            if dsi__ogzqt[nalsi__kwsal]:
                                hud__mkoj.append(df.columns[nalsi__kwsal])
                                hri__fzw.append(df.data[nalsi__kwsal])
                        ctzs__ycxf = tuple()
                        nfjeh__shsip = DataFrameType(tuple(hri__fzw),
                            aow__fobsy, tuple(hud__mkoj))
                        return nfjeh__shsip(*args)
                    elif itts__xlm.dtype == bodo.string_type:
                        ctzs__ycxf, hri__fzw = self.get_kept_cols_and_data(df,
                            dsi__ogzqt)
                        nfjeh__shsip = DataFrameType(hri__fzw, aow__fobsy,
                            ctzs__ycxf)
                        return nfjeh__shsip(*args)
        raise_bodo_error(
            f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet. If you are trying to select a subset of the columns by passing a list of column names, that list must be a compile time constant. See https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
            )

    def typecheck_df_getitem(self, args):
        df = args[0]
        ind = args[1]
        if is_overload_constant_str(ind) or is_overload_constant_int(ind):
            ind_val = get_overload_const_str(ind) if is_overload_constant_str(
                ind) else get_overload_const_int(ind)
            if isinstance(df.columns[0], tuple):
                hud__mkoj = []
                hri__fzw = []
                for nalsi__kwsal, hlqdx__qtnh in enumerate(df.columns):
                    if hlqdx__qtnh[0] != ind_val:
                        continue
                    hud__mkoj.append(hlqdx__qtnh[1] if len(hlqdx__qtnh) == 
                        2 else hlqdx__qtnh[1:])
                    hri__fzw.append(df.data[nalsi__kwsal])
                uju__mjr = tuple(hri__fzw)
                sre__flai = df.index
                krs__oeuc = tuple(hud__mkoj)
                nfjeh__shsip = DataFrameType(uju__mjr, sre__flai, krs__oeuc)
                return nfjeh__shsip(*args)
            else:
                if ind_val not in df.columns:
                    raise_bodo_error('dataframe {} does not include column {}'
                        .format(df, ind_val))
                psoq__lkmj = df.columns.index(ind_val)
                uju__mjr = df.data[psoq__lkmj]
                bmn__mzep = uju__mjr.dtype
                sre__flai = df.index
                uhw__hzvi = types.literal(df.columns[psoq__lkmj])
                nfjeh__shsip = bodo.SeriesType(bmn__mzep, uju__mjr,
                    sre__flai, uhw__hzvi)
                return nfjeh__shsip(*args)
        if isinstance(ind, types.Integer) or isinstance(ind, types.UnicodeType
            ):
            raise_bodo_error(
                'df[] getitem selecting a subset of columns requires providing constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        if is_list_like_index_type(ind
            ) and ind.dtype == types.bool_ or isinstance(ind, types.SliceType):
            uju__mjr = df.data
            sre__flai = self.replace_range_with_numeric_idx_if_needed(df, ind)
            krs__oeuc = df.columns
            nfjeh__shsip = DataFrameType(uju__mjr, sre__flai, krs__oeuc,
                is_table_format=df.is_table_format)
            return nfjeh__shsip(*args)
        elif is_overload_constant_list(ind):
            wtb__zvc = get_overload_const_list(ind)
            krs__oeuc, uju__mjr = self.get_kept_cols_and_data(df, wtb__zvc)
            sre__flai = df.index
            nfjeh__shsip = DataFrameType(uju__mjr, sre__flai, krs__oeuc)
            return nfjeh__shsip(*args)
        raise_bodo_error(
            f'df[] getitem using {ind} not supported. If you are trying to select a subset of the columns, you must provide the column names you are selecting as a constant. See https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
            )

    def get_kept_cols_and_data(self, df, cols_to_keep_list):
        for pmu__xrs in cols_to_keep_list:
            if pmu__xrs not in df.columns:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(pmu__xrs, df.columns))
        krs__oeuc = tuple(cols_to_keep_list)
        uju__mjr = tuple(df.data[df.column_index[jnljf__fny]] for
            jnljf__fny in krs__oeuc)
        return krs__oeuc, uju__mjr

    def replace_range_with_numeric_idx_if_needed(self, df, ind):
        aow__fobsy = bodo.hiframes.pd_index_ext.NumericIndexType(types.
            int64, df.index.name_typ) if not isinstance(ind, types.SliceType
            ) and isinstance(df.index, bodo.hiframes.pd_index_ext.
            RangeIndexType) else df.index
        return aow__fobsy


DataFrameGetItemTemplate._no_unliteral = True


@lower_builtin(operator.getitem, DataFrameType, types.Any)
def getitem_df_lower(context, builder, sig, args):
    impl = df_getitem_overload(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def df_getitem_overload(df, ind):
    if not isinstance(df, DataFrameType):
        return
    if is_overload_constant_str(ind) or is_overload_constant_int(ind):
        ind_val = get_overload_const_str(ind) if is_overload_constant_str(ind
            ) else get_overload_const_int(ind)
        if isinstance(df.columns[0], tuple):
            hud__mkoj = []
            hri__fzw = []
            for nalsi__kwsal, hlqdx__qtnh in enumerate(df.columns):
                if hlqdx__qtnh[0] != ind_val:
                    continue
                hud__mkoj.append(hlqdx__qtnh[1] if len(hlqdx__qtnh) == 2 else
                    hlqdx__qtnh[1:])
                hri__fzw.append(
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'
                    .format(nalsi__kwsal))
            amsc__guk = 'def impl(df, ind):\n'
            zjybm__shx = (
                'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
            return bodo.hiframes.dataframe_impl._gen_init_df(amsc__guk,
                hud__mkoj, ', '.join(hri__fzw), zjybm__shx)
        if ind_val not in df.columns:
            raise_bodo_error('dataframe {} does not include column {}'.
                format(df, ind_val))
        col_no = df.columns.index(ind_val)
        return lambda df, ind: bodo.hiframes.pd_series_ext.init_series(bodo
            .hiframes.pd_dataframe_ext.get_dataframe_data(df, col_no), bodo
            .hiframes.pd_dataframe_ext.get_dataframe_index(df), ind_val)
    if is_overload_constant_list(ind):
        wtb__zvc = get_overload_const_list(ind)
        for pmu__xrs in wtb__zvc:
            if pmu__xrs not in df.column_index:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(pmu__xrs, df.columns))
        hri__fzw = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[pmu__xrs]}).copy()'
             for pmu__xrs in wtb__zvc)
        amsc__guk = 'def impl(df, ind):\n'
        zjybm__shx = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
        return bodo.hiframes.dataframe_impl._gen_init_df(amsc__guk,
            wtb__zvc, hri__fzw, zjybm__shx)
    if is_list_like_index_type(ind) and ind.dtype == types.bool_ or isinstance(
        ind, types.SliceType):
        amsc__guk = 'def impl(df, ind):\n'
        if not isinstance(ind, types.SliceType):
            amsc__guk += (
                '  ind = bodo.utils.conversion.coerce_to_ndarray(ind)\n')
        zjybm__shx = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[ind]')
        if df.is_table_format:
            hri__fzw = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[ind]')
        else:
            hri__fzw = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[pmu__xrs]})[ind]'
                 for pmu__xrs in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(amsc__guk, df.
            columns, hri__fzw, zjybm__shx, out_df_type=df)
    raise_bodo_error('df[] getitem using {} not supported'.format(ind))


@overload(operator.setitem, no_unliteral=True)
def df_setitem_overload(df, idx, val):
    check_runtime_cols_unsupported(df, 'DataFrame setitem (df[])')
    if not isinstance(df, DataFrameType):
        return
    raise_bodo_error('DataFrame setitem: transform necessary')


class DataFrameILocType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        jnljf__fny = 'DataFrameILocType({})'.format(df_type)
        super(DataFrameILocType, self).__init__(jnljf__fny)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameILocType)
class DataFrameILocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        zbis__muvc = [('obj', fe_type.df_type)]
        super(DataFrameILocModel, self).__init__(dmm, fe_type, zbis__muvc)


make_attribute_wrapper(DataFrameILocType, 'obj', '_obj')


@intrinsic
def init_dataframe_iloc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        neqno__qli, = args
        oco__fdict = signature.return_type
        ptwri__lnp = cgutils.create_struct_proxy(oco__fdict)(context, builder)
        ptwri__lnp.obj = neqno__qli
        context.nrt.incref(builder, signature.args[0], neqno__qli)
        return ptwri__lnp._getvalue()
    return DataFrameILocType(obj)(obj), codegen


@overload_attribute(DataFrameType, 'iloc')
def overload_dataframe_iloc(df):
    check_runtime_cols_unsupported(df, 'DataFrame.iloc')
    return lambda df: bodo.hiframes.dataframe_indexing.init_dataframe_iloc(df)


@overload(operator.getitem, no_unliteral=True)
def overload_iloc_getitem(I, idx):
    if not isinstance(I, DataFrameILocType):
        return
    df = I.df_type
    if isinstance(idx, types.Integer):
        return _gen_iloc_getitem_row_impl(df, df.columns, 'idx')
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and not isinstance(
        idx[1], types.SliceType):
        if not (is_overload_constant_list(idx.types[1]) or
            is_overload_constant_int(idx.types[1])):
            raise_bodo_error(
                'idx2 in df.iloc[idx1, idx2] should be a constant integer or constant list of integers. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        tdvhp__ads = len(df.data)
        if is_overload_constant_int(idx.types[1]):
            is_out_series = True
            ljadd__zwpdc = get_overload_const_int(idx.types[1])
            if ljadd__zwpdc < 0 or ljadd__zwpdc >= tdvhp__ads:
                raise BodoError(
                    'df.iloc: column integer must refer to a valid column number'
                    )
            vmgu__sbq = [ljadd__zwpdc]
        else:
            is_out_series = False
            vmgu__sbq = get_overload_const_list(idx.types[1])
            if any(not isinstance(ind, int) or ind < 0 or ind >= tdvhp__ads for
                ind in vmgu__sbq):
                raise BodoError(
                    'df.iloc: column list must be integers referring to a valid column number'
                    )
        col_names = tuple(pd.Series(df.columns, dtype=object)[vmgu__sbq])
        if isinstance(idx.types[0], types.Integer):
            if isinstance(idx.types[1], types.Integer):
                ljadd__zwpdc = vmgu__sbq[0]

                def impl(I, idx):
                    df = I._obj
                    return bodo.utils.conversion.box_if_dt64(bodo.hiframes.
                        pd_dataframe_ext.get_dataframe_data(df,
                        ljadd__zwpdc)[idx[0]])
                return impl
            return _gen_iloc_getitem_row_impl(df, col_names, 'idx[0]')
        if is_list_like_index_type(idx.types[0]) and isinstance(idx.types[0
            ].dtype, (types.Integer, types.Boolean)) or isinstance(idx.
            types[0], types.SliceType):
            return _gen_iloc_getitem_bool_slice_impl(df, col_names, idx.
                types[0], 'idx[0]', is_out_series)
    if is_list_like_index_type(idx) and isinstance(idx.dtype, (types.
        Integer, types.Boolean)) or isinstance(idx, types.SliceType):
        return _gen_iloc_getitem_bool_slice_impl(df, df.columns, idx, 'idx',
            False)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):
        raise_bodo_error(
            'slice2 in df.iloc[slice1,slice2] should be constant. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
            )
    raise_bodo_error(f'df.iloc[] getitem using {idx} not supported')


def _gen_iloc_getitem_bool_slice_impl(df, col_names, idx_typ, idx,
    is_out_series):
    amsc__guk = 'def impl(I, idx):\n'
    amsc__guk += '  df = I._obj\n'
    if isinstance(idx_typ, types.SliceType):
        amsc__guk += f'  idx_t = {idx}\n'
    else:
        amsc__guk += (
            f'  idx_t = bodo.utils.conversion.coerce_to_ndarray({idx})\n')
    zjybm__shx = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]')
    hri__fzw = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[pmu__xrs]})[idx_t]'
         for pmu__xrs in col_names)
    if is_out_series:
        gckk__eky = f"'{col_names[0]}'" if isinstance(col_names[0], str
            ) else f'{col_names[0]}'
        amsc__guk += f"""  return bodo.hiframes.pd_series_ext.init_series({hri__fzw}, {zjybm__shx}, {gckk__eky})
"""
        bipi__qfvp = {}
        exec(amsc__guk, {'bodo': bodo}, bipi__qfvp)
        return bipi__qfvp['impl']
    return bodo.hiframes.dataframe_impl._gen_init_df(amsc__guk, col_names,
        hri__fzw, zjybm__shx)


def _gen_iloc_getitem_row_impl(df, col_names, idx):
    amsc__guk = 'def impl(I, idx):\n'
    amsc__guk += '  df = I._obj\n'
    nqm__opf = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[pmu__xrs]})[{idx}]'
         for pmu__xrs in col_names)
    amsc__guk += f"""  row_idx = bodo.hiframes.pd_index_ext.init_heter_index({gen_const_tup(col_names)}, None)
"""
    amsc__guk += (
        f'  return bodo.hiframes.pd_series_ext.init_series(({nqm__opf},), row_idx, None)\n'
        )
    bipi__qfvp = {}
    exec(amsc__guk, {'bodo': bodo}, bipi__qfvp)
    impl = bipi__qfvp['impl']
    return impl


@overload(operator.setitem, no_unliteral=True)
def df_iloc_setitem_overload(df, idx, val):
    if not isinstance(df, DataFrameILocType):
        return
    raise_bodo_error(
        f'DataFrame.iloc setitem unsupported for dataframe {df.df_type}, index {idx}, value {val}'
        )


class DataFrameLocType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        jnljf__fny = 'DataFrameLocType({})'.format(df_type)
        super(DataFrameLocType, self).__init__(jnljf__fny)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameLocType)
class DataFrameLocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        zbis__muvc = [('obj', fe_type.df_type)]
        super(DataFrameLocModel, self).__init__(dmm, fe_type, zbis__muvc)


make_attribute_wrapper(DataFrameLocType, 'obj', '_obj')


@intrinsic
def init_dataframe_loc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        neqno__qli, = args
        emh__xqmk = signature.return_type
        kzti__drx = cgutils.create_struct_proxy(emh__xqmk)(context, builder)
        kzti__drx.obj = neqno__qli
        context.nrt.incref(builder, signature.args[0], neqno__qli)
        return kzti__drx._getvalue()
    return DataFrameLocType(obj)(obj), codegen


@overload_attribute(DataFrameType, 'loc')
def overload_dataframe_loc(df):
    check_runtime_cols_unsupported(df, 'DataFrame.loc')
    return lambda df: bodo.hiframes.dataframe_indexing.init_dataframe_loc(df)


@lower_builtin(operator.getitem, DataFrameLocType, types.Any)
def loc_getitem_lower(context, builder, sig, args):
    impl = overload_loc_getitem(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def overload_loc_getitem(I, idx):
    if not isinstance(I, DataFrameLocType):
        return
    df = I.df_type
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        amsc__guk = 'def impl(I, idx):\n'
        amsc__guk += '  df = I._obj\n'
        amsc__guk += '  idx_t = bodo.utils.conversion.coerce_to_ndarray(idx)\n'
        zjybm__shx = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]')
        hri__fzw = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[pmu__xrs]})[idx_t]'
             for pmu__xrs in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(amsc__guk, df.
            columns, hri__fzw, zjybm__shx)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        chmqp__mgox = idx.types[1]
        if is_overload_constant_str(chmqp__mgox):
            jcepa__bvy = get_overload_const_str(chmqp__mgox)
            ljadd__zwpdc = df.columns.index(jcepa__bvy)

            def impl_col_name(I, idx):
                df = I._obj
                zjybm__shx = (bodo.hiframes.pd_dataframe_ext.
                    get_dataframe_index(df))
                fqns__gfw = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
                    df, ljadd__zwpdc)
                return bodo.hiframes.pd_series_ext.init_series(fqns__gfw,
                    zjybm__shx, jcepa__bvy).loc[idx[0]]
            return impl_col_name
        if is_overload_constant_list(chmqp__mgox):
            col_idx_list = get_overload_const_list(chmqp__mgox)
            if len(col_idx_list) > 0 and not isinstance(col_idx_list[0], (
                bool, np.bool_)) and not all(pmu__xrs in df.columns for
                pmu__xrs in col_idx_list):
                raise_bodo_error(
                    f'DataFrame.loc[]: invalid column list {col_idx_list}; not all in dataframe columns {df.columns}'
                    )
            return gen_df_loc_col_select_impl(df, col_idx_list)
    raise_bodo_error(
        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
        )


def gen_df_loc_col_select_impl(df, col_idx_list):
    if len(col_idx_list) > 0 and isinstance(col_idx_list[0], (bool, np.bool_)):
        col_idx_list = list(pd.Series(df.columns, dtype=object)[col_idx_list])
    hri__fzw = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[pmu__xrs]})[idx[0]]'
         for pmu__xrs in col_idx_list)
    zjybm__shx = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx[0]]')
    amsc__guk = 'def impl(I, idx):\n'
    amsc__guk += '  df = I._obj\n'
    return bodo.hiframes.dataframe_impl._gen_init_df(amsc__guk,
        col_idx_list, hri__fzw, zjybm__shx)


@overload(operator.setitem, no_unliteral=True)
def df_loc_setitem_overload(df, idx, val):
    if not isinstance(df, DataFrameLocType):
        return
    raise_bodo_error(
        f'DataFrame.loc setitem unsupported for dataframe {df.df_type}, index {idx}, value {val}'
        )


class DataFrameIatType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        jnljf__fny = 'DataFrameIatType({})'.format(df_type)
        super(DataFrameIatType, self).__init__(jnljf__fny)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameIatType)
class DataFrameIatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        zbis__muvc = [('obj', fe_type.df_type)]
        super(DataFrameIatModel, self).__init__(dmm, fe_type, zbis__muvc)


make_attribute_wrapper(DataFrameIatType, 'obj', '_obj')


@intrinsic
def init_dataframe_iat(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        neqno__qli, = args
        vofby__jluxi = signature.return_type
        ipqp__tlf = cgutils.create_struct_proxy(vofby__jluxi)(context, builder)
        ipqp__tlf.obj = neqno__qli
        context.nrt.incref(builder, signature.args[0], neqno__qli)
        return ipqp__tlf._getvalue()
    return DataFrameIatType(obj)(obj), codegen


@overload_attribute(DataFrameType, 'iat')
def overload_dataframe_iat(df):
    check_runtime_cols_unsupported(df, 'DataFrame.iat')
    return lambda df: bodo.hiframes.dataframe_indexing.init_dataframe_iat(df)


@overload(operator.getitem, no_unliteral=True)
def overload_iat_getitem(I, idx):
    if not isinstance(I, DataFrameIatType):
        return
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        if not isinstance(idx.types[0], types.Integer):
            raise BodoError(
                'DataFrame.iat: iAt based indexing can only have integer indexers'
                )
        if not is_overload_constant_int(idx.types[1]):
            raise_bodo_error(
                'DataFrame.iat getitem: column index must be a constant integer. For more informaton, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        ljadd__zwpdc = get_overload_const_int(idx.types[1])

        def impl_col_ind(I, idx):
            df = I._obj
            fqns__gfw = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                ljadd__zwpdc)
            return fqns__gfw[idx[0]]
        return impl_col_ind
    raise BodoError('df.iat[] getitem using {} not supported'.format(idx))


@overload(operator.setitem, no_unliteral=True)
def overload_iat_setitem(I, idx, val):
    if not isinstance(I, DataFrameIatType):
        return
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        if not isinstance(idx.types[0], types.Integer):
            raise BodoError(
                'DataFrame.iat: iAt based indexing can only have integer indexers'
                )
        if not is_overload_constant_int(idx.types[1]):
            raise_bodo_error(
                'DataFrame.iat setitem: column index must be a constant integer. For more informaton, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        ljadd__zwpdc = get_overload_const_int(idx.types[1])
        if is_immutable_array(I.df_type.data[ljadd__zwpdc]):
            raise BodoError(
                f'DataFrame setitem not supported for column with immutable array type {I.df_type.data}'
                )

        def impl_col_ind(I, idx, val):
            df = I._obj
            fqns__gfw = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                ljadd__zwpdc)
            fqns__gfw[idx[0]] = bodo.utils.conversion.unbox_if_timestamp(val)
        return impl_col_ind
    raise BodoError('df.iat[] setitem using {} not supported'.format(idx))


@lower_cast(DataFrameIatType, DataFrameIatType)
@lower_cast(DataFrameILocType, DataFrameILocType)
@lower_cast(DataFrameLocType, DataFrameLocType)
def cast_series_iat(context, builder, fromty, toty, val):
    ipqp__tlf = cgutils.create_struct_proxy(fromty)(context, builder, val)
    ncwc__zngi = context.cast(builder, ipqp__tlf.obj, fromty.df_type, toty.
        df_type)
    mriat__gpr = cgutils.create_struct_proxy(toty)(context, builder)
    mriat__gpr.obj = ncwc__zngi
    return mriat__gpr._getvalue()
