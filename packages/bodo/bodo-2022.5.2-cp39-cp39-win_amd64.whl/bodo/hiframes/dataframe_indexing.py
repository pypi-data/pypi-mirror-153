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
            xxyr__nwcav = idx
            urim__aha = df.data
            lxvuc__ckle = df.columns
            nvwt__fte = self.replace_range_with_numeric_idx_if_needed(df,
                xxyr__nwcav)
            bsdk__fmw = DataFrameType(urim__aha, nvwt__fte, lxvuc__ckle)
            return bsdk__fmw(*args)
        if isinstance(idx, types.BaseTuple) and len(idx) == 2:
            syta__cvppi = idx.types[0]
            gmb__vtk = idx.types[1]
            if isinstance(syta__cvppi, types.Integer):
                if not isinstance(df.index, bodo.hiframes.pd_index_ext.
                    RangeIndexType):
                    raise_bodo_error(
                        'Dataframe.loc[int, col_ind] getitem only supported for dataframes with RangeIndexes'
                        )
                if is_overload_constant_str(gmb__vtk):
                    gdijj__lil = get_overload_const_str(gmb__vtk)
                    if gdijj__lil not in df.columns:
                        raise_bodo_error(
                            'dataframe {} does not include column {}'.
                            format(df, gdijj__lil))
                    wrja__qnift = df.columns.index(gdijj__lil)
                    return df.data[wrja__qnift].dtype(*args)
                if isinstance(gmb__vtk, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                        )
                else:
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
                        )
            if is_list_like_index_type(syta__cvppi
                ) and syta__cvppi.dtype == types.bool_ or isinstance(
                syta__cvppi, types.SliceType):
                nvwt__fte = self.replace_range_with_numeric_idx_if_needed(df,
                    syta__cvppi)
                if is_overload_constant_str(gmb__vtk):
                    xwhrk__pqhfi = get_overload_const_str(gmb__vtk)
                    if xwhrk__pqhfi not in df.columns:
                        raise_bodo_error(
                            f'dataframe {df} does not include column {xwhrk__pqhfi}'
                            )
                    wrja__qnift = df.columns.index(xwhrk__pqhfi)
                    vct__tdebu = df.data[wrja__qnift]
                    qmm__thb = vct__tdebu.dtype
                    vvd__xixg = types.literal(df.columns[wrja__qnift])
                    bsdk__fmw = bodo.SeriesType(qmm__thb, vct__tdebu,
                        nvwt__fte, vvd__xixg)
                    return bsdk__fmw(*args)
                if isinstance(gmb__vtk, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                        )
                elif is_overload_constant_list(gmb__vtk):
                    eqak__xexe = get_overload_const_list(gmb__vtk)
                    htak__ehmp = types.unliteral(gmb__vtk)
                    if htak__ehmp.dtype == types.bool_:
                        if len(df.columns) != len(eqak__xexe):
                            raise_bodo_error(
                                f'dataframe {df} has {len(df.columns)} columns, but boolean array used with DataFrame.loc[] {eqak__xexe} has {len(eqak__xexe)} values'
                                )
                        nyzh__zged = []
                        bed__qgms = []
                        for mfel__jfw in range(len(eqak__xexe)):
                            if eqak__xexe[mfel__jfw]:
                                nyzh__zged.append(df.columns[mfel__jfw])
                                bed__qgms.append(df.data[mfel__jfw])
                        yqqi__zwyzj = tuple()
                        bsdk__fmw = DataFrameType(tuple(bed__qgms),
                            nvwt__fte, tuple(nyzh__zged))
                        return bsdk__fmw(*args)
                    elif htak__ehmp.dtype == bodo.string_type:
                        yqqi__zwyzj, bed__qgms = self.get_kept_cols_and_data(df
                            , eqak__xexe)
                        bsdk__fmw = DataFrameType(bed__qgms, nvwt__fte,
                            yqqi__zwyzj)
                        return bsdk__fmw(*args)
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
                nyzh__zged = []
                bed__qgms = []
                for mfel__jfw, uari__dcvlj in enumerate(df.columns):
                    if uari__dcvlj[0] != ind_val:
                        continue
                    nyzh__zged.append(uari__dcvlj[1] if len(uari__dcvlj) ==
                        2 else uari__dcvlj[1:])
                    bed__qgms.append(df.data[mfel__jfw])
                vct__tdebu = tuple(bed__qgms)
                iyfxo__cpsd = df.index
                opgwf__lzvv = tuple(nyzh__zged)
                bsdk__fmw = DataFrameType(vct__tdebu, iyfxo__cpsd, opgwf__lzvv)
                return bsdk__fmw(*args)
            else:
                if ind_val not in df.columns:
                    raise_bodo_error('dataframe {} does not include column {}'
                        .format(df, ind_val))
                wrja__qnift = df.columns.index(ind_val)
                vct__tdebu = df.data[wrja__qnift]
                qmm__thb = vct__tdebu.dtype
                iyfxo__cpsd = df.index
                vvd__xixg = types.literal(df.columns[wrja__qnift])
                bsdk__fmw = bodo.SeriesType(qmm__thb, vct__tdebu,
                    iyfxo__cpsd, vvd__xixg)
                return bsdk__fmw(*args)
        if isinstance(ind, types.Integer) or isinstance(ind, types.UnicodeType
            ):
            raise_bodo_error(
                'df[] getitem selecting a subset of columns requires providing constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        if is_list_like_index_type(ind
            ) and ind.dtype == types.bool_ or isinstance(ind, types.SliceType):
            vct__tdebu = df.data
            iyfxo__cpsd = self.replace_range_with_numeric_idx_if_needed(df, ind
                )
            opgwf__lzvv = df.columns
            bsdk__fmw = DataFrameType(vct__tdebu, iyfxo__cpsd, opgwf__lzvv,
                is_table_format=df.is_table_format)
            return bsdk__fmw(*args)
        elif is_overload_constant_list(ind):
            sxlxx__ilj = get_overload_const_list(ind)
            opgwf__lzvv, vct__tdebu = self.get_kept_cols_and_data(df,
                sxlxx__ilj)
            iyfxo__cpsd = df.index
            bsdk__fmw = DataFrameType(vct__tdebu, iyfxo__cpsd, opgwf__lzvv)
            return bsdk__fmw(*args)
        raise_bodo_error(
            f'df[] getitem using {ind} not supported. If you are trying to select a subset of the columns, you must provide the column names you are selecting as a constant. See https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
            )

    def get_kept_cols_and_data(self, df, cols_to_keep_list):
        for jqgn__ifqk in cols_to_keep_list:
            if jqgn__ifqk not in df.columns:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(jqgn__ifqk, df.columns))
        opgwf__lzvv = tuple(cols_to_keep_list)
        vct__tdebu = tuple(df.data[df.column_index[aea__vzfvp]] for
            aea__vzfvp in opgwf__lzvv)
        return opgwf__lzvv, vct__tdebu

    def replace_range_with_numeric_idx_if_needed(self, df, ind):
        nvwt__fte = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64,
            df.index.name_typ) if not isinstance(ind, types.SliceType
            ) and isinstance(df.index, bodo.hiframes.pd_index_ext.
            RangeIndexType) else df.index
        return nvwt__fte


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
            nyzh__zged = []
            bed__qgms = []
            for mfel__jfw, uari__dcvlj in enumerate(df.columns):
                if uari__dcvlj[0] != ind_val:
                    continue
                nyzh__zged.append(uari__dcvlj[1] if len(uari__dcvlj) == 2 else
                    uari__dcvlj[1:])
                bed__qgms.append(
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'
                    .format(mfel__jfw))
            qcgr__jzvqv = 'def impl(df, ind):\n'
            cjj__mib = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
            return bodo.hiframes.dataframe_impl._gen_init_df(qcgr__jzvqv,
                nyzh__zged, ', '.join(bed__qgms), cjj__mib)
        if ind_val not in df.columns:
            raise_bodo_error('dataframe {} does not include column {}'.
                format(df, ind_val))
        col_no = df.columns.index(ind_val)
        return lambda df, ind: bodo.hiframes.pd_series_ext.init_series(bodo
            .hiframes.pd_dataframe_ext.get_dataframe_data(df, col_no), bodo
            .hiframes.pd_dataframe_ext.get_dataframe_index(df), ind_val)
    if is_overload_constant_list(ind):
        sxlxx__ilj = get_overload_const_list(ind)
        for jqgn__ifqk in sxlxx__ilj:
            if jqgn__ifqk not in df.column_index:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(jqgn__ifqk, df.columns))
        bed__qgms = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[jqgn__ifqk]}).copy()'
             for jqgn__ifqk in sxlxx__ilj)
        qcgr__jzvqv = 'def impl(df, ind):\n'
        cjj__mib = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
        return bodo.hiframes.dataframe_impl._gen_init_df(qcgr__jzvqv,
            sxlxx__ilj, bed__qgms, cjj__mib)
    if is_list_like_index_type(ind) and ind.dtype == types.bool_ or isinstance(
        ind, types.SliceType):
        qcgr__jzvqv = 'def impl(df, ind):\n'
        if not isinstance(ind, types.SliceType):
            qcgr__jzvqv += (
                '  ind = bodo.utils.conversion.coerce_to_ndarray(ind)\n')
        cjj__mib = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[ind]')
        if df.is_table_format:
            bed__qgms = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[ind]')
        else:
            bed__qgms = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[jqgn__ifqk]})[ind]'
                 for jqgn__ifqk in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(qcgr__jzvqv, df.
            columns, bed__qgms, cjj__mib, out_df_type=df)
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
        aea__vzfvp = 'DataFrameILocType({})'.format(df_type)
        super(DataFrameILocType, self).__init__(aea__vzfvp)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameILocType)
class DataFrameILocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        piw__velnj = [('obj', fe_type.df_type)]
        super(DataFrameILocModel, self).__init__(dmm, fe_type, piw__velnj)


make_attribute_wrapper(DataFrameILocType, 'obj', '_obj')


@intrinsic
def init_dataframe_iloc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        fnnk__sei, = args
        teql__odv = signature.return_type
        lnlfu__zxc = cgutils.create_struct_proxy(teql__odv)(context, builder)
        lnlfu__zxc.obj = fnnk__sei
        context.nrt.incref(builder, signature.args[0], fnnk__sei)
        return lnlfu__zxc._getvalue()
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
        isif__qkq = len(df.data)
        if is_overload_constant_int(idx.types[1]):
            is_out_series = True
            wcapr__bku = get_overload_const_int(idx.types[1])
            if wcapr__bku < 0 or wcapr__bku >= isif__qkq:
                raise BodoError(
                    'df.iloc: column integer must refer to a valid column number'
                    )
            oye__pwyjt = [wcapr__bku]
        else:
            is_out_series = False
            oye__pwyjt = get_overload_const_list(idx.types[1])
            if any(not isinstance(ind, int) or ind < 0 or ind >= isif__qkq for
                ind in oye__pwyjt):
                raise BodoError(
                    'df.iloc: column list must be integers referring to a valid column number'
                    )
        col_names = tuple(pd.Series(df.columns, dtype=object)[oye__pwyjt])
        if isinstance(idx.types[0], types.Integer):
            if isinstance(idx.types[1], types.Integer):
                wcapr__bku = oye__pwyjt[0]

                def impl(I, idx):
                    df = I._obj
                    return bodo.utils.conversion.box_if_dt64(bodo.hiframes.
                        pd_dataframe_ext.get_dataframe_data(df, wcapr__bku)
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
    qcgr__jzvqv = 'def impl(I, idx):\n'
    qcgr__jzvqv += '  df = I._obj\n'
    if isinstance(idx_typ, types.SliceType):
        qcgr__jzvqv += f'  idx_t = {idx}\n'
    else:
        qcgr__jzvqv += (
            f'  idx_t = bodo.utils.conversion.coerce_to_ndarray({idx})\n')
    cjj__mib = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]'
    bed__qgms = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[jqgn__ifqk]})[idx_t]'
         for jqgn__ifqk in col_names)
    if is_out_series:
        ket__pgads = f"'{col_names[0]}'" if isinstance(col_names[0], str
            ) else f'{col_names[0]}'
        qcgr__jzvqv += f"""  return bodo.hiframes.pd_series_ext.init_series({bed__qgms}, {cjj__mib}, {ket__pgads})
"""
        zubz__cztb = {}
        exec(qcgr__jzvqv, {'bodo': bodo}, zubz__cztb)
        return zubz__cztb['impl']
    return bodo.hiframes.dataframe_impl._gen_init_df(qcgr__jzvqv, col_names,
        bed__qgms, cjj__mib)


def _gen_iloc_getitem_row_impl(df, col_names, idx):
    qcgr__jzvqv = 'def impl(I, idx):\n'
    qcgr__jzvqv += '  df = I._obj\n'
    ddx__bjbi = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[jqgn__ifqk]})[{idx}]'
         for jqgn__ifqk in col_names)
    qcgr__jzvqv += f"""  row_idx = bodo.hiframes.pd_index_ext.init_heter_index({gen_const_tup(col_names)}, None)
"""
    qcgr__jzvqv += f"""  return bodo.hiframes.pd_series_ext.init_series(({ddx__bjbi},), row_idx, None)
"""
    zubz__cztb = {}
    exec(qcgr__jzvqv, {'bodo': bodo}, zubz__cztb)
    impl = zubz__cztb['impl']
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
        aea__vzfvp = 'DataFrameLocType({})'.format(df_type)
        super(DataFrameLocType, self).__init__(aea__vzfvp)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameLocType)
class DataFrameLocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        piw__velnj = [('obj', fe_type.df_type)]
        super(DataFrameLocModel, self).__init__(dmm, fe_type, piw__velnj)


make_attribute_wrapper(DataFrameLocType, 'obj', '_obj')


@intrinsic
def init_dataframe_loc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        fnnk__sei, = args
        miw__lcp = signature.return_type
        vynf__mfomq = cgutils.create_struct_proxy(miw__lcp)(context, builder)
        vynf__mfomq.obj = fnnk__sei
        context.nrt.incref(builder, signature.args[0], fnnk__sei)
        return vynf__mfomq._getvalue()
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
        qcgr__jzvqv = 'def impl(I, idx):\n'
        qcgr__jzvqv += '  df = I._obj\n'
        qcgr__jzvqv += (
            '  idx_t = bodo.utils.conversion.coerce_to_ndarray(idx)\n')
        cjj__mib = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]')
        bed__qgms = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[jqgn__ifqk]})[idx_t]'
             for jqgn__ifqk in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(qcgr__jzvqv, df.
            columns, bed__qgms, cjj__mib)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        ifqy__uikc = idx.types[1]
        if is_overload_constant_str(ifqy__uikc):
            fdg__epf = get_overload_const_str(ifqy__uikc)
            wcapr__bku = df.columns.index(fdg__epf)

            def impl_col_name(I, idx):
                df = I._obj
                cjj__mib = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
                    df)
                zjysl__ukj = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
                    df, wcapr__bku)
                return bodo.hiframes.pd_series_ext.init_series(zjysl__ukj,
                    cjj__mib, fdg__epf).loc[idx[0]]
            return impl_col_name
        if is_overload_constant_list(ifqy__uikc):
            col_idx_list = get_overload_const_list(ifqy__uikc)
            if len(col_idx_list) > 0 and not isinstance(col_idx_list[0], (
                bool, np.bool_)) and not all(jqgn__ifqk in df.columns for
                jqgn__ifqk in col_idx_list):
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
    bed__qgms = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[jqgn__ifqk]})[idx[0]]'
         for jqgn__ifqk in col_idx_list)
    cjj__mib = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx[0]]'
    qcgr__jzvqv = 'def impl(I, idx):\n'
    qcgr__jzvqv += '  df = I._obj\n'
    return bodo.hiframes.dataframe_impl._gen_init_df(qcgr__jzvqv,
        col_idx_list, bed__qgms, cjj__mib)


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
        aea__vzfvp = 'DataFrameIatType({})'.format(df_type)
        super(DataFrameIatType, self).__init__(aea__vzfvp)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameIatType)
class DataFrameIatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        piw__velnj = [('obj', fe_type.df_type)]
        super(DataFrameIatModel, self).__init__(dmm, fe_type, piw__velnj)


make_attribute_wrapper(DataFrameIatType, 'obj', '_obj')


@intrinsic
def init_dataframe_iat(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        fnnk__sei, = args
        jav__nfhpn = signature.return_type
        nnqvh__emmz = cgutils.create_struct_proxy(jav__nfhpn)(context, builder)
        nnqvh__emmz.obj = fnnk__sei
        context.nrt.incref(builder, signature.args[0], fnnk__sei)
        return nnqvh__emmz._getvalue()
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
        wcapr__bku = get_overload_const_int(idx.types[1])

        def impl_col_ind(I, idx):
            df = I._obj
            zjysl__ukj = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                wcapr__bku)
            return zjysl__ukj[idx[0]]
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
        wcapr__bku = get_overload_const_int(idx.types[1])
        if is_immutable_array(I.df_type.data[wcapr__bku]):
            raise BodoError(
                f'DataFrame setitem not supported for column with immutable array type {I.df_type.data}'
                )

        def impl_col_ind(I, idx, val):
            df = I._obj
            zjysl__ukj = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                wcapr__bku)
            zjysl__ukj[idx[0]] = bodo.utils.conversion.unbox_if_timestamp(val)
        return impl_col_ind
    raise BodoError('df.iat[] setitem using {} not supported'.format(idx))


@lower_cast(DataFrameIatType, DataFrameIatType)
@lower_cast(DataFrameILocType, DataFrameILocType)
@lower_cast(DataFrameLocType, DataFrameLocType)
def cast_series_iat(context, builder, fromty, toty, val):
    nnqvh__emmz = cgutils.create_struct_proxy(fromty)(context, builder, val)
    nmtee__myr = context.cast(builder, nnqvh__emmz.obj, fromty.df_type,
        toty.df_type)
    wcd__tnvr = cgutils.create_struct_proxy(toty)(context, builder)
    wcd__tnvr.obj = nmtee__myr
    return wcd__tnvr._getvalue()
