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
            ictlt__rjs = idx
            xwj__hao = df.data
            novw__vqb = df.columns
            lpu__kyh = self.replace_range_with_numeric_idx_if_needed(df,
                ictlt__rjs)
            rlnc__bmehl = DataFrameType(xwj__hao, lpu__kyh, novw__vqb)
            return rlnc__bmehl(*args)
        if isinstance(idx, types.BaseTuple) and len(idx) == 2:
            wdvlc__mpb = idx.types[0]
            lyvd__lfrlh = idx.types[1]
            if isinstance(wdvlc__mpb, types.Integer):
                if not isinstance(df.index, bodo.hiframes.pd_index_ext.
                    RangeIndexType):
                    raise_bodo_error(
                        'Dataframe.loc[int, col_ind] getitem only supported for dataframes with RangeIndexes'
                        )
                if is_overload_constant_str(lyvd__lfrlh):
                    rod__boe = get_overload_const_str(lyvd__lfrlh)
                    if rod__boe not in df.columns:
                        raise_bodo_error(
                            'dataframe {} does not include column {}'.
                            format(df, rod__boe))
                    ovz__jfe = df.columns.index(rod__boe)
                    return df.data[ovz__jfe].dtype(*args)
                if isinstance(lyvd__lfrlh, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                        )
                else:
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
                        )
            if is_list_like_index_type(wdvlc__mpb
                ) and wdvlc__mpb.dtype == types.bool_ or isinstance(wdvlc__mpb,
                types.SliceType):
                lpu__kyh = self.replace_range_with_numeric_idx_if_needed(df,
                    wdvlc__mpb)
                if is_overload_constant_str(lyvd__lfrlh):
                    rdqsf__kgry = get_overload_const_str(lyvd__lfrlh)
                    if rdqsf__kgry not in df.columns:
                        raise_bodo_error(
                            f'dataframe {df} does not include column {rdqsf__kgry}'
                            )
                    ovz__jfe = df.columns.index(rdqsf__kgry)
                    sach__zfe = df.data[ovz__jfe]
                    jwb__rnfy = sach__zfe.dtype
                    jmh__guju = types.literal(df.columns[ovz__jfe])
                    rlnc__bmehl = bodo.SeriesType(jwb__rnfy, sach__zfe,
                        lpu__kyh, jmh__guju)
                    return rlnc__bmehl(*args)
                if isinstance(lyvd__lfrlh, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                        )
                elif is_overload_constant_list(lyvd__lfrlh):
                    ruzvk__srvgu = get_overload_const_list(lyvd__lfrlh)
                    ivl__loe = types.unliteral(lyvd__lfrlh)
                    if ivl__loe.dtype == types.bool_:
                        if len(df.columns) != len(ruzvk__srvgu):
                            raise_bodo_error(
                                f'dataframe {df} has {len(df.columns)} columns, but boolean array used with DataFrame.loc[] {ruzvk__srvgu} has {len(ruzvk__srvgu)} values'
                                )
                        rqa__nej = []
                        mpwyq__oxoyy = []
                        for owho__zccr in range(len(ruzvk__srvgu)):
                            if ruzvk__srvgu[owho__zccr]:
                                rqa__nej.append(df.columns[owho__zccr])
                                mpwyq__oxoyy.append(df.data[owho__zccr])
                        koyo__svp = tuple()
                        rlnc__bmehl = DataFrameType(tuple(mpwyq__oxoyy),
                            lpu__kyh, tuple(rqa__nej))
                        return rlnc__bmehl(*args)
                    elif ivl__loe.dtype == bodo.string_type:
                        koyo__svp, mpwyq__oxoyy = self.get_kept_cols_and_data(
                            df, ruzvk__srvgu)
                        rlnc__bmehl = DataFrameType(mpwyq__oxoyy, lpu__kyh,
                            koyo__svp)
                        return rlnc__bmehl(*args)
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
                rqa__nej = []
                mpwyq__oxoyy = []
                for owho__zccr, upusk__wedf in enumerate(df.columns):
                    if upusk__wedf[0] != ind_val:
                        continue
                    rqa__nej.append(upusk__wedf[1] if len(upusk__wedf) == 2
                         else upusk__wedf[1:])
                    mpwyq__oxoyy.append(df.data[owho__zccr])
                sach__zfe = tuple(mpwyq__oxoyy)
                iuq__pghz = df.index
                rdb__oqnzr = tuple(rqa__nej)
                rlnc__bmehl = DataFrameType(sach__zfe, iuq__pghz, rdb__oqnzr)
                return rlnc__bmehl(*args)
            else:
                if ind_val not in df.columns:
                    raise_bodo_error('dataframe {} does not include column {}'
                        .format(df, ind_val))
                ovz__jfe = df.columns.index(ind_val)
                sach__zfe = df.data[ovz__jfe]
                jwb__rnfy = sach__zfe.dtype
                iuq__pghz = df.index
                jmh__guju = types.literal(df.columns[ovz__jfe])
                rlnc__bmehl = bodo.SeriesType(jwb__rnfy, sach__zfe,
                    iuq__pghz, jmh__guju)
                return rlnc__bmehl(*args)
        if isinstance(ind, types.Integer) or isinstance(ind, types.UnicodeType
            ):
            raise_bodo_error(
                'df[] getitem selecting a subset of columns requires providing constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        if is_list_like_index_type(ind
            ) and ind.dtype == types.bool_ or isinstance(ind, types.SliceType):
            sach__zfe = df.data
            iuq__pghz = self.replace_range_with_numeric_idx_if_needed(df, ind)
            rdb__oqnzr = df.columns
            rlnc__bmehl = DataFrameType(sach__zfe, iuq__pghz, rdb__oqnzr,
                is_table_format=df.is_table_format)
            return rlnc__bmehl(*args)
        elif is_overload_constant_list(ind):
            biot__tdk = get_overload_const_list(ind)
            rdb__oqnzr, sach__zfe = self.get_kept_cols_and_data(df, biot__tdk)
            iuq__pghz = df.index
            rlnc__bmehl = DataFrameType(sach__zfe, iuq__pghz, rdb__oqnzr)
            return rlnc__bmehl(*args)
        raise_bodo_error(
            f'df[] getitem using {ind} not supported. If you are trying to select a subset of the columns, you must provide the column names you are selecting as a constant. See https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
            )

    def get_kept_cols_and_data(self, df, cols_to_keep_list):
        for kgva__mhmml in cols_to_keep_list:
            if kgva__mhmml not in df.columns:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(kgva__mhmml, df.columns))
        rdb__oqnzr = tuple(cols_to_keep_list)
        sach__zfe = tuple(df.data[df.column_index[vfrg__qnoq]] for
            vfrg__qnoq in rdb__oqnzr)
        return rdb__oqnzr, sach__zfe

    def replace_range_with_numeric_idx_if_needed(self, df, ind):
        lpu__kyh = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64,
            df.index.name_typ) if not isinstance(ind, types.SliceType
            ) and isinstance(df.index, bodo.hiframes.pd_index_ext.
            RangeIndexType) else df.index
        return lpu__kyh


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
            rqa__nej = []
            mpwyq__oxoyy = []
            for owho__zccr, upusk__wedf in enumerate(df.columns):
                if upusk__wedf[0] != ind_val:
                    continue
                rqa__nej.append(upusk__wedf[1] if len(upusk__wedf) == 2 else
                    upusk__wedf[1:])
                mpwyq__oxoyy.append(
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'
                    .format(owho__zccr))
            zxuod__ytc = 'def impl(df, ind):\n'
            xnk__ggo = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
            return bodo.hiframes.dataframe_impl._gen_init_df(zxuod__ytc,
                rqa__nej, ', '.join(mpwyq__oxoyy), xnk__ggo)
        if ind_val not in df.columns:
            raise_bodo_error('dataframe {} does not include column {}'.
                format(df, ind_val))
        col_no = df.columns.index(ind_val)
        return lambda df, ind: bodo.hiframes.pd_series_ext.init_series(bodo
            .hiframes.pd_dataframe_ext.get_dataframe_data(df, col_no), bodo
            .hiframes.pd_dataframe_ext.get_dataframe_index(df), ind_val)
    if is_overload_constant_list(ind):
        biot__tdk = get_overload_const_list(ind)
        for kgva__mhmml in biot__tdk:
            if kgva__mhmml not in df.column_index:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(kgva__mhmml, df.columns))
        mpwyq__oxoyy = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[kgva__mhmml]}).copy()'
             for kgva__mhmml in biot__tdk)
        zxuod__ytc = 'def impl(df, ind):\n'
        xnk__ggo = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
        return bodo.hiframes.dataframe_impl._gen_init_df(zxuod__ytc,
            biot__tdk, mpwyq__oxoyy, xnk__ggo)
    if is_list_like_index_type(ind) and ind.dtype == types.bool_ or isinstance(
        ind, types.SliceType):
        zxuod__ytc = 'def impl(df, ind):\n'
        if not isinstance(ind, types.SliceType):
            zxuod__ytc += (
                '  ind = bodo.utils.conversion.coerce_to_ndarray(ind)\n')
        xnk__ggo = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[ind]')
        if df.is_table_format:
            mpwyq__oxoyy = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[ind]')
        else:
            mpwyq__oxoyy = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[kgva__mhmml]})[ind]'
                 for kgva__mhmml in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(zxuod__ytc, df.
            columns, mpwyq__oxoyy, xnk__ggo, out_df_type=df)
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
        vfrg__qnoq = 'DataFrameILocType({})'.format(df_type)
        super(DataFrameILocType, self).__init__(vfrg__qnoq)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameILocType)
class DataFrameILocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        yak__wndjq = [('obj', fe_type.df_type)]
        super(DataFrameILocModel, self).__init__(dmm, fe_type, yak__wndjq)


make_attribute_wrapper(DataFrameILocType, 'obj', '_obj')


@intrinsic
def init_dataframe_iloc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        tyk__avu, = args
        vimkp__znsdp = signature.return_type
        vwb__uqfg = cgutils.create_struct_proxy(vimkp__znsdp)(context, builder)
        vwb__uqfg.obj = tyk__avu
        context.nrt.incref(builder, signature.args[0], tyk__avu)
        return vwb__uqfg._getvalue()
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
        ifuzu__mzjr = len(df.data)
        if is_overload_constant_int(idx.types[1]):
            is_out_series = True
            dan__jzp = get_overload_const_int(idx.types[1])
            if dan__jzp < 0 or dan__jzp >= ifuzu__mzjr:
                raise BodoError(
                    'df.iloc: column integer must refer to a valid column number'
                    )
            pnv__osdiv = [dan__jzp]
        else:
            is_out_series = False
            pnv__osdiv = get_overload_const_list(idx.types[1])
            if any(not isinstance(ind, int) or ind < 0 or ind >=
                ifuzu__mzjr for ind in pnv__osdiv):
                raise BodoError(
                    'df.iloc: column list must be integers referring to a valid column number'
                    )
        col_names = tuple(pd.Series(df.columns, dtype=object)[pnv__osdiv])
        if isinstance(idx.types[0], types.Integer):
            if isinstance(idx.types[1], types.Integer):
                dan__jzp = pnv__osdiv[0]

                def impl(I, idx):
                    df = I._obj
                    return bodo.utils.conversion.box_if_dt64(bodo.hiframes.
                        pd_dataframe_ext.get_dataframe_data(df, dan__jzp)[
                        idx[0]])
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
    zxuod__ytc = 'def impl(I, idx):\n'
    zxuod__ytc += '  df = I._obj\n'
    if isinstance(idx_typ, types.SliceType):
        zxuod__ytc += f'  idx_t = {idx}\n'
    else:
        zxuod__ytc += (
            f'  idx_t = bodo.utils.conversion.coerce_to_ndarray({idx})\n')
    xnk__ggo = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]'
    mpwyq__oxoyy = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[kgva__mhmml]})[idx_t]'
         for kgva__mhmml in col_names)
    if is_out_series:
        krgd__bbccn = f"'{col_names[0]}'" if isinstance(col_names[0], str
            ) else f'{col_names[0]}'
        zxuod__ytc += f"""  return bodo.hiframes.pd_series_ext.init_series({mpwyq__oxoyy}, {xnk__ggo}, {krgd__bbccn})
"""
        ljdra__yqps = {}
        exec(zxuod__ytc, {'bodo': bodo}, ljdra__yqps)
        return ljdra__yqps['impl']
    return bodo.hiframes.dataframe_impl._gen_init_df(zxuod__ytc, col_names,
        mpwyq__oxoyy, xnk__ggo)


def _gen_iloc_getitem_row_impl(df, col_names, idx):
    zxuod__ytc = 'def impl(I, idx):\n'
    zxuod__ytc += '  df = I._obj\n'
    arti__lkqg = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[kgva__mhmml]})[{idx}]'
         for kgva__mhmml in col_names)
    zxuod__ytc += f"""  row_idx = bodo.hiframes.pd_index_ext.init_heter_index({gen_const_tup(col_names)}, None)
"""
    zxuod__ytc += f"""  return bodo.hiframes.pd_series_ext.init_series(({arti__lkqg},), row_idx, None)
"""
    ljdra__yqps = {}
    exec(zxuod__ytc, {'bodo': bodo}, ljdra__yqps)
    impl = ljdra__yqps['impl']
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
        vfrg__qnoq = 'DataFrameLocType({})'.format(df_type)
        super(DataFrameLocType, self).__init__(vfrg__qnoq)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameLocType)
class DataFrameLocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        yak__wndjq = [('obj', fe_type.df_type)]
        super(DataFrameLocModel, self).__init__(dmm, fe_type, yak__wndjq)


make_attribute_wrapper(DataFrameLocType, 'obj', '_obj')


@intrinsic
def init_dataframe_loc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        tyk__avu, = args
        xtmua__cqwgw = signature.return_type
        wlvub__vcai = cgutils.create_struct_proxy(xtmua__cqwgw)(context,
            builder)
        wlvub__vcai.obj = tyk__avu
        context.nrt.incref(builder, signature.args[0], tyk__avu)
        return wlvub__vcai._getvalue()
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
        zxuod__ytc = 'def impl(I, idx):\n'
        zxuod__ytc += '  df = I._obj\n'
        zxuod__ytc += (
            '  idx_t = bodo.utils.conversion.coerce_to_ndarray(idx)\n')
        xnk__ggo = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]')
        mpwyq__oxoyy = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[kgva__mhmml]})[idx_t]'
             for kgva__mhmml in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(zxuod__ytc, df.
            columns, mpwyq__oxoyy, xnk__ggo)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        ixee__wxbor = idx.types[1]
        if is_overload_constant_str(ixee__wxbor):
            jsna__nfkqq = get_overload_const_str(ixee__wxbor)
            dan__jzp = df.columns.index(jsna__nfkqq)

            def impl_col_name(I, idx):
                df = I._obj
                xnk__ggo = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
                    df)
                llwj__ibat = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
                    df, dan__jzp)
                return bodo.hiframes.pd_series_ext.init_series(llwj__ibat,
                    xnk__ggo, jsna__nfkqq).loc[idx[0]]
            return impl_col_name
        if is_overload_constant_list(ixee__wxbor):
            col_idx_list = get_overload_const_list(ixee__wxbor)
            if len(col_idx_list) > 0 and not isinstance(col_idx_list[0], (
                bool, np.bool_)) and not all(kgva__mhmml in df.columns for
                kgva__mhmml in col_idx_list):
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
    mpwyq__oxoyy = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[kgva__mhmml]})[idx[0]]'
         for kgva__mhmml in col_idx_list)
    xnk__ggo = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx[0]]'
    zxuod__ytc = 'def impl(I, idx):\n'
    zxuod__ytc += '  df = I._obj\n'
    return bodo.hiframes.dataframe_impl._gen_init_df(zxuod__ytc,
        col_idx_list, mpwyq__oxoyy, xnk__ggo)


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
        vfrg__qnoq = 'DataFrameIatType({})'.format(df_type)
        super(DataFrameIatType, self).__init__(vfrg__qnoq)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameIatType)
class DataFrameIatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        yak__wndjq = [('obj', fe_type.df_type)]
        super(DataFrameIatModel, self).__init__(dmm, fe_type, yak__wndjq)


make_attribute_wrapper(DataFrameIatType, 'obj', '_obj')


@intrinsic
def init_dataframe_iat(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        tyk__avu, = args
        xtgcb__mdub = signature.return_type
        ddhvk__zyq = cgutils.create_struct_proxy(xtgcb__mdub)(context, builder)
        ddhvk__zyq.obj = tyk__avu
        context.nrt.incref(builder, signature.args[0], tyk__avu)
        return ddhvk__zyq._getvalue()
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
        dan__jzp = get_overload_const_int(idx.types[1])

        def impl_col_ind(I, idx):
            df = I._obj
            llwj__ibat = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                dan__jzp)
            return llwj__ibat[idx[0]]
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
        dan__jzp = get_overload_const_int(idx.types[1])
        if is_immutable_array(I.df_type.data[dan__jzp]):
            raise BodoError(
                f'DataFrame setitem not supported for column with immutable array type {I.df_type.data}'
                )

        def impl_col_ind(I, idx, val):
            df = I._obj
            llwj__ibat = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                dan__jzp)
            llwj__ibat[idx[0]] = bodo.utils.conversion.unbox_if_timestamp(val)
        return impl_col_ind
    raise BodoError('df.iat[] setitem using {} not supported'.format(idx))


@lower_cast(DataFrameIatType, DataFrameIatType)
@lower_cast(DataFrameILocType, DataFrameILocType)
@lower_cast(DataFrameLocType, DataFrameLocType)
def cast_series_iat(context, builder, fromty, toty, val):
    ddhvk__zyq = cgutils.create_struct_proxy(fromty)(context, builder, val)
    qhso__wvid = context.cast(builder, ddhvk__zyq.obj, fromty.df_type, toty
        .df_type)
    qjqc__vyyf = cgutils.create_struct_proxy(toty)(context, builder)
    qjqc__vyyf.obj = qhso__wvid
    return qjqc__vyyf._getvalue()
