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
            hehsd__jdh = idx
            rfbjk__dioyj = df.data
            fwdoj__rfq = df.columns
            oiqnc__jbyv = self.replace_range_with_numeric_idx_if_needed(df,
                hehsd__jdh)
            hclny__tldr = DataFrameType(rfbjk__dioyj, oiqnc__jbyv, fwdoj__rfq)
            return hclny__tldr(*args)
        if isinstance(idx, types.BaseTuple) and len(idx) == 2:
            muj__lngh = idx.types[0]
            ilylj__uzjnh = idx.types[1]
            if isinstance(muj__lngh, types.Integer):
                if not isinstance(df.index, bodo.hiframes.pd_index_ext.
                    RangeIndexType):
                    raise_bodo_error(
                        'Dataframe.loc[int, col_ind] getitem only supported for dataframes with RangeIndexes'
                        )
                if is_overload_constant_str(ilylj__uzjnh):
                    kbkua__dry = get_overload_const_str(ilylj__uzjnh)
                    if kbkua__dry not in df.columns:
                        raise_bodo_error(
                            'dataframe {} does not include column {}'.
                            format(df, kbkua__dry))
                    tryn__sxlmd = df.columns.index(kbkua__dry)
                    return df.data[tryn__sxlmd].dtype(*args)
                if isinstance(ilylj__uzjnh, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                        )
                else:
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
                        )
            if is_list_like_index_type(muj__lngh
                ) and muj__lngh.dtype == types.bool_ or isinstance(muj__lngh,
                types.SliceType):
                oiqnc__jbyv = self.replace_range_with_numeric_idx_if_needed(df,
                    muj__lngh)
                if is_overload_constant_str(ilylj__uzjnh):
                    octuq__ddng = get_overload_const_str(ilylj__uzjnh)
                    if octuq__ddng not in df.columns:
                        raise_bodo_error(
                            f'dataframe {df} does not include column {octuq__ddng}'
                            )
                    tryn__sxlmd = df.columns.index(octuq__ddng)
                    uib__vmb = df.data[tryn__sxlmd]
                    gyqbe__xspi = uib__vmb.dtype
                    dhoar__lhrzv = types.literal(df.columns[tryn__sxlmd])
                    hclny__tldr = bodo.SeriesType(gyqbe__xspi, uib__vmb,
                        oiqnc__jbyv, dhoar__lhrzv)
                    return hclny__tldr(*args)
                if isinstance(ilylj__uzjnh, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                        )
                elif is_overload_constant_list(ilylj__uzjnh):
                    flpr__lbt = get_overload_const_list(ilylj__uzjnh)
                    fnri__xez = types.unliteral(ilylj__uzjnh)
                    if fnri__xez.dtype == types.bool_:
                        if len(df.columns) != len(flpr__lbt):
                            raise_bodo_error(
                                f'dataframe {df} has {len(df.columns)} columns, but boolean array used with DataFrame.loc[] {flpr__lbt} has {len(flpr__lbt)} values'
                                )
                        ubvpp__qoaly = []
                        thni__ewh = []
                        for rnev__qraxg in range(len(flpr__lbt)):
                            if flpr__lbt[rnev__qraxg]:
                                ubvpp__qoaly.append(df.columns[rnev__qraxg])
                                thni__ewh.append(df.data[rnev__qraxg])
                        rxvsl__iscg = tuple()
                        hclny__tldr = DataFrameType(tuple(thni__ewh),
                            oiqnc__jbyv, tuple(ubvpp__qoaly))
                        return hclny__tldr(*args)
                    elif fnri__xez.dtype == bodo.string_type:
                        rxvsl__iscg, thni__ewh = self.get_kept_cols_and_data(df
                            , flpr__lbt)
                        hclny__tldr = DataFrameType(thni__ewh, oiqnc__jbyv,
                            rxvsl__iscg)
                        return hclny__tldr(*args)
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
                ubvpp__qoaly = []
                thni__ewh = []
                for rnev__qraxg, xdqgy__eurmd in enumerate(df.columns):
                    if xdqgy__eurmd[0] != ind_val:
                        continue
                    ubvpp__qoaly.append(xdqgy__eurmd[1] if len(xdqgy__eurmd
                        ) == 2 else xdqgy__eurmd[1:])
                    thni__ewh.append(df.data[rnev__qraxg])
                uib__vmb = tuple(thni__ewh)
                udz__uxgn = df.index
                lgow__ngvt = tuple(ubvpp__qoaly)
                hclny__tldr = DataFrameType(uib__vmb, udz__uxgn, lgow__ngvt)
                return hclny__tldr(*args)
            else:
                if ind_val not in df.columns:
                    raise_bodo_error('dataframe {} does not include column {}'
                        .format(df, ind_val))
                tryn__sxlmd = df.columns.index(ind_val)
                uib__vmb = df.data[tryn__sxlmd]
                gyqbe__xspi = uib__vmb.dtype
                udz__uxgn = df.index
                dhoar__lhrzv = types.literal(df.columns[tryn__sxlmd])
                hclny__tldr = bodo.SeriesType(gyqbe__xspi, uib__vmb,
                    udz__uxgn, dhoar__lhrzv)
                return hclny__tldr(*args)
        if isinstance(ind, types.Integer) or isinstance(ind, types.UnicodeType
            ):
            raise_bodo_error(
                'df[] getitem selecting a subset of columns requires providing constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        if is_list_like_index_type(ind
            ) and ind.dtype == types.bool_ or isinstance(ind, types.SliceType):
            uib__vmb = df.data
            udz__uxgn = self.replace_range_with_numeric_idx_if_needed(df, ind)
            lgow__ngvt = df.columns
            hclny__tldr = DataFrameType(uib__vmb, udz__uxgn, lgow__ngvt,
                is_table_format=df.is_table_format)
            return hclny__tldr(*args)
        elif is_overload_constant_list(ind):
            duota__rkm = get_overload_const_list(ind)
            lgow__ngvt, uib__vmb = self.get_kept_cols_and_data(df, duota__rkm)
            udz__uxgn = df.index
            hclny__tldr = DataFrameType(uib__vmb, udz__uxgn, lgow__ngvt)
            return hclny__tldr(*args)
        raise_bodo_error(
            f'df[] getitem using {ind} not supported. If you are trying to select a subset of the columns, you must provide the column names you are selecting as a constant. See https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
            )

    def get_kept_cols_and_data(self, df, cols_to_keep_list):
        for wyd__wicl in cols_to_keep_list:
            if wyd__wicl not in df.columns:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(wyd__wicl, df.columns))
        lgow__ngvt = tuple(cols_to_keep_list)
        uib__vmb = tuple(df.data[df.column_index[htqea__qsdys]] for
            htqea__qsdys in lgow__ngvt)
        return lgow__ngvt, uib__vmb

    def replace_range_with_numeric_idx_if_needed(self, df, ind):
        oiqnc__jbyv = bodo.hiframes.pd_index_ext.NumericIndexType(types.
            int64, df.index.name_typ) if not isinstance(ind, types.SliceType
            ) and isinstance(df.index, bodo.hiframes.pd_index_ext.
            RangeIndexType) else df.index
        return oiqnc__jbyv


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
            ubvpp__qoaly = []
            thni__ewh = []
            for rnev__qraxg, xdqgy__eurmd in enumerate(df.columns):
                if xdqgy__eurmd[0] != ind_val:
                    continue
                ubvpp__qoaly.append(xdqgy__eurmd[1] if len(xdqgy__eurmd) ==
                    2 else xdqgy__eurmd[1:])
                thni__ewh.append(
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'
                    .format(rnev__qraxg))
            kayr__rckrn = 'def impl(df, ind):\n'
            ukbff__kjv = (
                'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
            return bodo.hiframes.dataframe_impl._gen_init_df(kayr__rckrn,
                ubvpp__qoaly, ', '.join(thni__ewh), ukbff__kjv)
        if ind_val not in df.columns:
            raise_bodo_error('dataframe {} does not include column {}'.
                format(df, ind_val))
        col_no = df.columns.index(ind_val)
        return lambda df, ind: bodo.hiframes.pd_series_ext.init_series(bodo
            .hiframes.pd_dataframe_ext.get_dataframe_data(df, col_no), bodo
            .hiframes.pd_dataframe_ext.get_dataframe_index(df), ind_val)
    if is_overload_constant_list(ind):
        duota__rkm = get_overload_const_list(ind)
        for wyd__wicl in duota__rkm:
            if wyd__wicl not in df.column_index:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(wyd__wicl, df.columns))
        thni__ewh = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[wyd__wicl]}).copy()'
             for wyd__wicl in duota__rkm)
        kayr__rckrn = 'def impl(df, ind):\n'
        ukbff__kjv = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
        return bodo.hiframes.dataframe_impl._gen_init_df(kayr__rckrn,
            duota__rkm, thni__ewh, ukbff__kjv)
    if is_list_like_index_type(ind) and ind.dtype == types.bool_ or isinstance(
        ind, types.SliceType):
        kayr__rckrn = 'def impl(df, ind):\n'
        if not isinstance(ind, types.SliceType):
            kayr__rckrn += (
                '  ind = bodo.utils.conversion.coerce_to_ndarray(ind)\n')
        ukbff__kjv = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[ind]')
        if df.is_table_format:
            thni__ewh = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[ind]')
        else:
            thni__ewh = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[wyd__wicl]})[ind]'
                 for wyd__wicl in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(kayr__rckrn, df.
            columns, thni__ewh, ukbff__kjv, out_df_type=df)
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
        htqea__qsdys = 'DataFrameILocType({})'.format(df_type)
        super(DataFrameILocType, self).__init__(htqea__qsdys)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameILocType)
class DataFrameILocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        cnnv__dmwe = [('obj', fe_type.df_type)]
        super(DataFrameILocModel, self).__init__(dmm, fe_type, cnnv__dmwe)


make_attribute_wrapper(DataFrameILocType, 'obj', '_obj')


@intrinsic
def init_dataframe_iloc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        qyj__pww, = args
        hryik__jbtyf = signature.return_type
        kxheo__fpgvi = cgutils.create_struct_proxy(hryik__jbtyf)(context,
            builder)
        kxheo__fpgvi.obj = qyj__pww
        context.nrt.incref(builder, signature.args[0], qyj__pww)
        return kxheo__fpgvi._getvalue()
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
        aya__kiwji = len(df.data)
        if is_overload_constant_int(idx.types[1]):
            is_out_series = True
            lji__zovqs = get_overload_const_int(idx.types[1])
            if lji__zovqs < 0 or lji__zovqs >= aya__kiwji:
                raise BodoError(
                    'df.iloc: column integer must refer to a valid column number'
                    )
            tsil__dhfgq = [lji__zovqs]
        else:
            is_out_series = False
            tsil__dhfgq = get_overload_const_list(idx.types[1])
            if any(not isinstance(ind, int) or ind < 0 or ind >= aya__kiwji for
                ind in tsil__dhfgq):
                raise BodoError(
                    'df.iloc: column list must be integers referring to a valid column number'
                    )
        col_names = tuple(pd.Series(df.columns, dtype=object)[tsil__dhfgq])
        if isinstance(idx.types[0], types.Integer):
            if isinstance(idx.types[1], types.Integer):
                lji__zovqs = tsil__dhfgq[0]

                def impl(I, idx):
                    df = I._obj
                    return bodo.utils.conversion.box_if_dt64(bodo.hiframes.
                        pd_dataframe_ext.get_dataframe_data(df, lji__zovqs)
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
    kayr__rckrn = 'def impl(I, idx):\n'
    kayr__rckrn += '  df = I._obj\n'
    if isinstance(idx_typ, types.SliceType):
        kayr__rckrn += f'  idx_t = {idx}\n'
    else:
        kayr__rckrn += (
            f'  idx_t = bodo.utils.conversion.coerce_to_ndarray({idx})\n')
    ukbff__kjv = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]')
    thni__ewh = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[wyd__wicl]})[idx_t]'
         for wyd__wicl in col_names)
    if is_out_series:
        zbb__hbinb = f"'{col_names[0]}'" if isinstance(col_names[0], str
            ) else f'{col_names[0]}'
        kayr__rckrn += f"""  return bodo.hiframes.pd_series_ext.init_series({thni__ewh}, {ukbff__kjv}, {zbb__hbinb})
"""
        une__fbs = {}
        exec(kayr__rckrn, {'bodo': bodo}, une__fbs)
        return une__fbs['impl']
    return bodo.hiframes.dataframe_impl._gen_init_df(kayr__rckrn, col_names,
        thni__ewh, ukbff__kjv)


def _gen_iloc_getitem_row_impl(df, col_names, idx):
    kayr__rckrn = 'def impl(I, idx):\n'
    kayr__rckrn += '  df = I._obj\n'
    hjfv__gwce = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[wyd__wicl]})[{idx}]'
         for wyd__wicl in col_names)
    kayr__rckrn += f"""  row_idx = bodo.hiframes.pd_index_ext.init_heter_index({gen_const_tup(col_names)}, None)
"""
    kayr__rckrn += f"""  return bodo.hiframes.pd_series_ext.init_series(({hjfv__gwce},), row_idx, None)
"""
    une__fbs = {}
    exec(kayr__rckrn, {'bodo': bodo}, une__fbs)
    impl = une__fbs['impl']
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
        htqea__qsdys = 'DataFrameLocType({})'.format(df_type)
        super(DataFrameLocType, self).__init__(htqea__qsdys)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameLocType)
class DataFrameLocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        cnnv__dmwe = [('obj', fe_type.df_type)]
        super(DataFrameLocModel, self).__init__(dmm, fe_type, cnnv__dmwe)


make_attribute_wrapper(DataFrameLocType, 'obj', '_obj')


@intrinsic
def init_dataframe_loc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        qyj__pww, = args
        pvvnd__nyvu = signature.return_type
        tnt__lvjk = cgutils.create_struct_proxy(pvvnd__nyvu)(context, builder)
        tnt__lvjk.obj = qyj__pww
        context.nrt.incref(builder, signature.args[0], qyj__pww)
        return tnt__lvjk._getvalue()
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
        kayr__rckrn = 'def impl(I, idx):\n'
        kayr__rckrn += '  df = I._obj\n'
        kayr__rckrn += (
            '  idx_t = bodo.utils.conversion.coerce_to_ndarray(idx)\n')
        ukbff__kjv = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]')
        thni__ewh = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[wyd__wicl]})[idx_t]'
             for wyd__wicl in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(kayr__rckrn, df.
            columns, thni__ewh, ukbff__kjv)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        wzoz__whard = idx.types[1]
        if is_overload_constant_str(wzoz__whard):
            hlog__lqlm = get_overload_const_str(wzoz__whard)
            lji__zovqs = df.columns.index(hlog__lqlm)

            def impl_col_name(I, idx):
                df = I._obj
                ukbff__kjv = (bodo.hiframes.pd_dataframe_ext.
                    get_dataframe_index(df))
                phvd__wsni = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
                    df, lji__zovqs)
                return bodo.hiframes.pd_series_ext.init_series(phvd__wsni,
                    ukbff__kjv, hlog__lqlm).loc[idx[0]]
            return impl_col_name
        if is_overload_constant_list(wzoz__whard):
            col_idx_list = get_overload_const_list(wzoz__whard)
            if len(col_idx_list) > 0 and not isinstance(col_idx_list[0], (
                bool, np.bool_)) and not all(wyd__wicl in df.columns for
                wyd__wicl in col_idx_list):
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
    thni__ewh = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[wyd__wicl]})[idx[0]]'
         for wyd__wicl in col_idx_list)
    ukbff__kjv = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx[0]]')
    kayr__rckrn = 'def impl(I, idx):\n'
    kayr__rckrn += '  df = I._obj\n'
    return bodo.hiframes.dataframe_impl._gen_init_df(kayr__rckrn,
        col_idx_list, thni__ewh, ukbff__kjv)


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
        htqea__qsdys = 'DataFrameIatType({})'.format(df_type)
        super(DataFrameIatType, self).__init__(htqea__qsdys)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameIatType)
class DataFrameIatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        cnnv__dmwe = [('obj', fe_type.df_type)]
        super(DataFrameIatModel, self).__init__(dmm, fe_type, cnnv__dmwe)


make_attribute_wrapper(DataFrameIatType, 'obj', '_obj')


@intrinsic
def init_dataframe_iat(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        qyj__pww, = args
        wivm__urw = signature.return_type
        gyt__bsa = cgutils.create_struct_proxy(wivm__urw)(context, builder)
        gyt__bsa.obj = qyj__pww
        context.nrt.incref(builder, signature.args[0], qyj__pww)
        return gyt__bsa._getvalue()
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
        lji__zovqs = get_overload_const_int(idx.types[1])

        def impl_col_ind(I, idx):
            df = I._obj
            phvd__wsni = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                lji__zovqs)
            return phvd__wsni[idx[0]]
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
        lji__zovqs = get_overload_const_int(idx.types[1])
        if is_immutable_array(I.df_type.data[lji__zovqs]):
            raise BodoError(
                f'DataFrame setitem not supported for column with immutable array type {I.df_type.data}'
                )

        def impl_col_ind(I, idx, val):
            df = I._obj
            phvd__wsni = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                lji__zovqs)
            phvd__wsni[idx[0]] = bodo.utils.conversion.unbox_if_timestamp(val)
        return impl_col_ind
    raise BodoError('df.iat[] setitem using {} not supported'.format(idx))


@lower_cast(DataFrameIatType, DataFrameIatType)
@lower_cast(DataFrameILocType, DataFrameILocType)
@lower_cast(DataFrameLocType, DataFrameLocType)
def cast_series_iat(context, builder, fromty, toty, val):
    gyt__bsa = cgutils.create_struct_proxy(fromty)(context, builder, val)
    kdavl__vdxi = context.cast(builder, gyt__bsa.obj, fromty.df_type, toty.
        df_type)
    vwhce__vbko = cgutils.create_struct_proxy(toty)(context, builder)
    vwhce__vbko.obj = kdavl__vdxi
    return vwhce__vbko._getvalue()
