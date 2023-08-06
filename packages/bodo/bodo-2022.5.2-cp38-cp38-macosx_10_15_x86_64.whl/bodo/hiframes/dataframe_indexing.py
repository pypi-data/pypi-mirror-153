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
            zkx__wero = idx
            zape__ftsl = df.data
            cqobu__nmptm = df.columns
            mbelh__glwgj = self.replace_range_with_numeric_idx_if_needed(df,
                zkx__wero)
            kxad__gyf = DataFrameType(zape__ftsl, mbelh__glwgj, cqobu__nmptm)
            return kxad__gyf(*args)
        if isinstance(idx, types.BaseTuple) and len(idx) == 2:
            cybk__exozn = idx.types[0]
            dfe__whmz = idx.types[1]
            if isinstance(cybk__exozn, types.Integer):
                if not isinstance(df.index, bodo.hiframes.pd_index_ext.
                    RangeIndexType):
                    raise_bodo_error(
                        'Dataframe.loc[int, col_ind] getitem only supported for dataframes with RangeIndexes'
                        )
                if is_overload_constant_str(dfe__whmz):
                    eou__knd = get_overload_const_str(dfe__whmz)
                    if eou__knd not in df.columns:
                        raise_bodo_error(
                            'dataframe {} does not include column {}'.
                            format(df, eou__knd))
                    aucb__qyvi = df.columns.index(eou__knd)
                    return df.data[aucb__qyvi].dtype(*args)
                if isinstance(dfe__whmz, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                        )
                else:
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
                        )
            if is_list_like_index_type(cybk__exozn
                ) and cybk__exozn.dtype == types.bool_ or isinstance(
                cybk__exozn, types.SliceType):
                mbelh__glwgj = self.replace_range_with_numeric_idx_if_needed(df
                    , cybk__exozn)
                if is_overload_constant_str(dfe__whmz):
                    tvvto__rmh = get_overload_const_str(dfe__whmz)
                    if tvvto__rmh not in df.columns:
                        raise_bodo_error(
                            f'dataframe {df} does not include column {tvvto__rmh}'
                            )
                    aucb__qyvi = df.columns.index(tvvto__rmh)
                    muwvv__tpqyc = df.data[aucb__qyvi]
                    gzfah__srtl = muwvv__tpqyc.dtype
                    mrn__dsitr = types.literal(df.columns[aucb__qyvi])
                    kxad__gyf = bodo.SeriesType(gzfah__srtl, muwvv__tpqyc,
                        mbelh__glwgj, mrn__dsitr)
                    return kxad__gyf(*args)
                if isinstance(dfe__whmz, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                        )
                elif is_overload_constant_list(dfe__whmz):
                    oxrcn__rlv = get_overload_const_list(dfe__whmz)
                    tloq__jnc = types.unliteral(dfe__whmz)
                    if tloq__jnc.dtype == types.bool_:
                        if len(df.columns) != len(oxrcn__rlv):
                            raise_bodo_error(
                                f'dataframe {df} has {len(df.columns)} columns, but boolean array used with DataFrame.loc[] {oxrcn__rlv} has {len(oxrcn__rlv)} values'
                                )
                        nguc__zdax = []
                        qntdo__vmu = []
                        for vxhj__zsvpi in range(len(oxrcn__rlv)):
                            if oxrcn__rlv[vxhj__zsvpi]:
                                nguc__zdax.append(df.columns[vxhj__zsvpi])
                                qntdo__vmu.append(df.data[vxhj__zsvpi])
                        egazm__qtyqx = tuple()
                        kxad__gyf = DataFrameType(tuple(qntdo__vmu),
                            mbelh__glwgj, tuple(nguc__zdax))
                        return kxad__gyf(*args)
                    elif tloq__jnc.dtype == bodo.string_type:
                        egazm__qtyqx, qntdo__vmu = self.get_kept_cols_and_data(
                            df, oxrcn__rlv)
                        kxad__gyf = DataFrameType(qntdo__vmu, mbelh__glwgj,
                            egazm__qtyqx)
                        return kxad__gyf(*args)
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
                nguc__zdax = []
                qntdo__vmu = []
                for vxhj__zsvpi, noe__snps in enumerate(df.columns):
                    if noe__snps[0] != ind_val:
                        continue
                    nguc__zdax.append(noe__snps[1] if len(noe__snps) == 2 else
                        noe__snps[1:])
                    qntdo__vmu.append(df.data[vxhj__zsvpi])
                muwvv__tpqyc = tuple(qntdo__vmu)
                wcjas__yqb = df.index
                prjtx__jqlw = tuple(nguc__zdax)
                kxad__gyf = DataFrameType(muwvv__tpqyc, wcjas__yqb, prjtx__jqlw
                    )
                return kxad__gyf(*args)
            else:
                if ind_val not in df.columns:
                    raise_bodo_error('dataframe {} does not include column {}'
                        .format(df, ind_val))
                aucb__qyvi = df.columns.index(ind_val)
                muwvv__tpqyc = df.data[aucb__qyvi]
                gzfah__srtl = muwvv__tpqyc.dtype
                wcjas__yqb = df.index
                mrn__dsitr = types.literal(df.columns[aucb__qyvi])
                kxad__gyf = bodo.SeriesType(gzfah__srtl, muwvv__tpqyc,
                    wcjas__yqb, mrn__dsitr)
                return kxad__gyf(*args)
        if isinstance(ind, types.Integer) or isinstance(ind, types.UnicodeType
            ):
            raise_bodo_error(
                'df[] getitem selecting a subset of columns requires providing constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        if is_list_like_index_type(ind
            ) and ind.dtype == types.bool_ or isinstance(ind, types.SliceType):
            muwvv__tpqyc = df.data
            wcjas__yqb = self.replace_range_with_numeric_idx_if_needed(df, ind)
            prjtx__jqlw = df.columns
            kxad__gyf = DataFrameType(muwvv__tpqyc, wcjas__yqb, prjtx__jqlw,
                is_table_format=df.is_table_format)
            return kxad__gyf(*args)
        elif is_overload_constant_list(ind):
            cjp__flj = get_overload_const_list(ind)
            prjtx__jqlw, muwvv__tpqyc = self.get_kept_cols_and_data(df,
                cjp__flj)
            wcjas__yqb = df.index
            kxad__gyf = DataFrameType(muwvv__tpqyc, wcjas__yqb, prjtx__jqlw)
            return kxad__gyf(*args)
        raise_bodo_error(
            f'df[] getitem using {ind} not supported. If you are trying to select a subset of the columns, you must provide the column names you are selecting as a constant. See https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
            )

    def get_kept_cols_and_data(self, df, cols_to_keep_list):
        for kdits__tusy in cols_to_keep_list:
            if kdits__tusy not in df.columns:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(kdits__tusy, df.columns))
        prjtx__jqlw = tuple(cols_to_keep_list)
        muwvv__tpqyc = tuple(df.data[df.column_index[vqtwn__ixq]] for
            vqtwn__ixq in prjtx__jqlw)
        return prjtx__jqlw, muwvv__tpqyc

    def replace_range_with_numeric_idx_if_needed(self, df, ind):
        mbelh__glwgj = bodo.hiframes.pd_index_ext.NumericIndexType(types.
            int64, df.index.name_typ) if not isinstance(ind, types.SliceType
            ) and isinstance(df.index, bodo.hiframes.pd_index_ext.
            RangeIndexType) else df.index
        return mbelh__glwgj


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
            nguc__zdax = []
            qntdo__vmu = []
            for vxhj__zsvpi, noe__snps in enumerate(df.columns):
                if noe__snps[0] != ind_val:
                    continue
                nguc__zdax.append(noe__snps[1] if len(noe__snps) == 2 else
                    noe__snps[1:])
                qntdo__vmu.append(
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'
                    .format(vxhj__zsvpi))
            loow__yqqc = 'def impl(df, ind):\n'
            hux__aopr = (
                'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
            return bodo.hiframes.dataframe_impl._gen_init_df(loow__yqqc,
                nguc__zdax, ', '.join(qntdo__vmu), hux__aopr)
        if ind_val not in df.columns:
            raise_bodo_error('dataframe {} does not include column {}'.
                format(df, ind_val))
        col_no = df.columns.index(ind_val)
        return lambda df, ind: bodo.hiframes.pd_series_ext.init_series(bodo
            .hiframes.pd_dataframe_ext.get_dataframe_data(df, col_no), bodo
            .hiframes.pd_dataframe_ext.get_dataframe_index(df), ind_val)
    if is_overload_constant_list(ind):
        cjp__flj = get_overload_const_list(ind)
        for kdits__tusy in cjp__flj:
            if kdits__tusy not in df.column_index:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(kdits__tusy, df.columns))
        qntdo__vmu = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[kdits__tusy]}).copy()'
             for kdits__tusy in cjp__flj)
        loow__yqqc = 'def impl(df, ind):\n'
        hux__aopr = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
        return bodo.hiframes.dataframe_impl._gen_init_df(loow__yqqc,
            cjp__flj, qntdo__vmu, hux__aopr)
    if is_list_like_index_type(ind) and ind.dtype == types.bool_ or isinstance(
        ind, types.SliceType):
        loow__yqqc = 'def impl(df, ind):\n'
        if not isinstance(ind, types.SliceType):
            loow__yqqc += (
                '  ind = bodo.utils.conversion.coerce_to_ndarray(ind)\n')
        hux__aopr = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[ind]')
        if df.is_table_format:
            qntdo__vmu = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[ind]')
        else:
            qntdo__vmu = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[kdits__tusy]})[ind]'
                 for kdits__tusy in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(loow__yqqc, df.
            columns, qntdo__vmu, hux__aopr, out_df_type=df)
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
        vqtwn__ixq = 'DataFrameILocType({})'.format(df_type)
        super(DataFrameILocType, self).__init__(vqtwn__ixq)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameILocType)
class DataFrameILocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        xia__qxhjx = [('obj', fe_type.df_type)]
        super(DataFrameILocModel, self).__init__(dmm, fe_type, xia__qxhjx)


make_attribute_wrapper(DataFrameILocType, 'obj', '_obj')


@intrinsic
def init_dataframe_iloc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        vjj__fyb, = args
        dbryb__ajt = signature.return_type
        hsqde__uzyf = cgutils.create_struct_proxy(dbryb__ajt)(context, builder)
        hsqde__uzyf.obj = vjj__fyb
        context.nrt.incref(builder, signature.args[0], vjj__fyb)
        return hsqde__uzyf._getvalue()
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
        elbd__igbwt = len(df.data)
        if is_overload_constant_int(idx.types[1]):
            is_out_series = True
            bvp__eckcw = get_overload_const_int(idx.types[1])
            if bvp__eckcw < 0 or bvp__eckcw >= elbd__igbwt:
                raise BodoError(
                    'df.iloc: column integer must refer to a valid column number'
                    )
            pgdl__khco = [bvp__eckcw]
        else:
            is_out_series = False
            pgdl__khco = get_overload_const_list(idx.types[1])
            if any(not isinstance(ind, int) or ind < 0 or ind >=
                elbd__igbwt for ind in pgdl__khco):
                raise BodoError(
                    'df.iloc: column list must be integers referring to a valid column number'
                    )
        col_names = tuple(pd.Series(df.columns, dtype=object)[pgdl__khco])
        if isinstance(idx.types[0], types.Integer):
            if isinstance(idx.types[1], types.Integer):
                bvp__eckcw = pgdl__khco[0]

                def impl(I, idx):
                    df = I._obj
                    return bodo.utils.conversion.box_if_dt64(bodo.hiframes.
                        pd_dataframe_ext.get_dataframe_data(df, bvp__eckcw)
                        [idx[0]])
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
    loow__yqqc = 'def impl(I, idx):\n'
    loow__yqqc += '  df = I._obj\n'
    if isinstance(idx_typ, types.SliceType):
        loow__yqqc += f'  idx_t = {idx}\n'
    else:
        loow__yqqc += (
            f'  idx_t = bodo.utils.conversion.coerce_to_ndarray({idx})\n')
    hux__aopr = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]'
    qntdo__vmu = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[kdits__tusy]})[idx_t]'
         for kdits__tusy in col_names)
    if is_out_series:
        gmvdt__dhei = f"'{col_names[0]}'" if isinstance(col_names[0], str
            ) else f'{col_names[0]}'
        loow__yqqc += f"""  return bodo.hiframes.pd_series_ext.init_series({qntdo__vmu}, {hux__aopr}, {gmvdt__dhei})
"""
        rkqhs__iynp = {}
        exec(loow__yqqc, {'bodo': bodo}, rkqhs__iynp)
        return rkqhs__iynp['impl']
    return bodo.hiframes.dataframe_impl._gen_init_df(loow__yqqc, col_names,
        qntdo__vmu, hux__aopr)


def _gen_iloc_getitem_row_impl(df, col_names, idx):
    loow__yqqc = 'def impl(I, idx):\n'
    loow__yqqc += '  df = I._obj\n'
    ebmnp__fsidj = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[kdits__tusy]})[{idx}]'
         for kdits__tusy in col_names)
    loow__yqqc += f"""  row_idx = bodo.hiframes.pd_index_ext.init_heter_index({gen_const_tup(col_names)}, None)
"""
    loow__yqqc += f"""  return bodo.hiframes.pd_series_ext.init_series(({ebmnp__fsidj},), row_idx, None)
"""
    rkqhs__iynp = {}
    exec(loow__yqqc, {'bodo': bodo}, rkqhs__iynp)
    impl = rkqhs__iynp['impl']
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
        vqtwn__ixq = 'DataFrameLocType({})'.format(df_type)
        super(DataFrameLocType, self).__init__(vqtwn__ixq)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameLocType)
class DataFrameLocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        xia__qxhjx = [('obj', fe_type.df_type)]
        super(DataFrameLocModel, self).__init__(dmm, fe_type, xia__qxhjx)


make_attribute_wrapper(DataFrameLocType, 'obj', '_obj')


@intrinsic
def init_dataframe_loc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        vjj__fyb, = args
        alqy__lzkx = signature.return_type
        quiyk__zucj = cgutils.create_struct_proxy(alqy__lzkx)(context, builder)
        quiyk__zucj.obj = vjj__fyb
        context.nrt.incref(builder, signature.args[0], vjj__fyb)
        return quiyk__zucj._getvalue()
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
        loow__yqqc = 'def impl(I, idx):\n'
        loow__yqqc += '  df = I._obj\n'
        loow__yqqc += (
            '  idx_t = bodo.utils.conversion.coerce_to_ndarray(idx)\n')
        hux__aopr = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]')
        qntdo__vmu = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[kdits__tusy]})[idx_t]'
             for kdits__tusy in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(loow__yqqc, df.
            columns, qntdo__vmu, hux__aopr)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        txka__gamn = idx.types[1]
        if is_overload_constant_str(txka__gamn):
            fcxk__saehg = get_overload_const_str(txka__gamn)
            bvp__eckcw = df.columns.index(fcxk__saehg)

            def impl_col_name(I, idx):
                df = I._obj
                hux__aopr = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
                    df)
                vicr__ehntv = (bodo.hiframes.pd_dataframe_ext.
                    get_dataframe_data(df, bvp__eckcw))
                return bodo.hiframes.pd_series_ext.init_series(vicr__ehntv,
                    hux__aopr, fcxk__saehg).loc[idx[0]]
            return impl_col_name
        if is_overload_constant_list(txka__gamn):
            col_idx_list = get_overload_const_list(txka__gamn)
            if len(col_idx_list) > 0 and not isinstance(col_idx_list[0], (
                bool, np.bool_)) and not all(kdits__tusy in df.columns for
                kdits__tusy in col_idx_list):
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
    qntdo__vmu = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[kdits__tusy]})[idx[0]]'
         for kdits__tusy in col_idx_list)
    hux__aopr = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx[0]]')
    loow__yqqc = 'def impl(I, idx):\n'
    loow__yqqc += '  df = I._obj\n'
    return bodo.hiframes.dataframe_impl._gen_init_df(loow__yqqc,
        col_idx_list, qntdo__vmu, hux__aopr)


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
        vqtwn__ixq = 'DataFrameIatType({})'.format(df_type)
        super(DataFrameIatType, self).__init__(vqtwn__ixq)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameIatType)
class DataFrameIatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        xia__qxhjx = [('obj', fe_type.df_type)]
        super(DataFrameIatModel, self).__init__(dmm, fe_type, xia__qxhjx)


make_attribute_wrapper(DataFrameIatType, 'obj', '_obj')


@intrinsic
def init_dataframe_iat(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        vjj__fyb, = args
        ccgi__woheb = signature.return_type
        rofw__qmnm = cgutils.create_struct_proxy(ccgi__woheb)(context, builder)
        rofw__qmnm.obj = vjj__fyb
        context.nrt.incref(builder, signature.args[0], vjj__fyb)
        return rofw__qmnm._getvalue()
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
        bvp__eckcw = get_overload_const_int(idx.types[1])

        def impl_col_ind(I, idx):
            df = I._obj
            vicr__ehntv = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                bvp__eckcw)
            return vicr__ehntv[idx[0]]
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
        bvp__eckcw = get_overload_const_int(idx.types[1])
        if is_immutable_array(I.df_type.data[bvp__eckcw]):
            raise BodoError(
                f'DataFrame setitem not supported for column with immutable array type {I.df_type.data}'
                )

        def impl_col_ind(I, idx, val):
            df = I._obj
            vicr__ehntv = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                bvp__eckcw)
            vicr__ehntv[idx[0]] = bodo.utils.conversion.unbox_if_timestamp(val)
        return impl_col_ind
    raise BodoError('df.iat[] setitem using {} not supported'.format(idx))


@lower_cast(DataFrameIatType, DataFrameIatType)
@lower_cast(DataFrameILocType, DataFrameILocType)
@lower_cast(DataFrameLocType, DataFrameLocType)
def cast_series_iat(context, builder, fromty, toty, val):
    rofw__qmnm = cgutils.create_struct_proxy(fromty)(context, builder, val)
    fxi__izp = context.cast(builder, rofw__qmnm.obj, fromty.df_type, toty.
        df_type)
    ubire__gzxev = cgutils.create_struct_proxy(toty)(context, builder)
    ubire__gzxev.obj = fxi__izp
    return ubire__gzxev._getvalue()
