"""
Implement pd.DataFrame typing and data model handling.
"""
import json
import operator
from functools import cached_property
from urllib.parse import quote
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
import pyarrow as pa
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.typing.templates import AbstractTemplate, bound_function, infer_global, signature
from numba.cpython.listobj import ListInstance
from numba.extending import infer_getattr, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.hiframes.pd_index_ext import HeterogeneousIndexType, NumericIndexType, RangeIndexType, is_pd_index_type
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
from bodo.hiframes.series_indexing import SeriesIlocType
from bodo.hiframes.table import Table, TableType, decode_if_dict_table, get_table_data, set_table_data_codegen
from bodo.io import json_cpp
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_info_decref_array, delete_table, delete_table_decref_arrays, info_from_table, info_to_array, py_table_to_cpp_table, shuffle_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.distributed_api import bcast_scalar
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import str_arr_from_sequence
from bodo.libs.str_ext import string_type, unicode_to_utf8
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.conversion import fix_arr_dtype, index_to_array
from bodo.utils.templates import OverloadedKeyAttributeTemplate
from bodo.utils.transform import gen_const_tup, get_const_func_output_type, get_const_tup_vals
from bodo.utils.typing import BodoError, BodoWarning, check_unsupported_args, create_unsupported_overload, decode_if_dict_array, dtype_to_array_type, get_index_data_arr_types, get_literal_value, get_overload_const, get_overload_const_bool, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_udf_error_msg, get_udf_out_arr_type, is_heterogeneous_tuple_type, is_iterable_type, is_literal_type, is_overload_bool, is_overload_constant_bool, is_overload_constant_int, is_overload_constant_str, is_overload_false, is_overload_int, is_overload_none, is_overload_true, is_str_arr_type, is_tuple_like_type, raise_bodo_error, to_nullable_type, to_str_arr_if_dict_array
from bodo.utils.utils import is_null_pointer
_json_write = types.ExternalFunction('json_write', types.void(types.voidptr,
    types.voidptr, types.int64, types.int64, types.bool_, types.bool_,
    types.voidptr))
ll.add_symbol('json_write', json_cpp.json_write)


class DataFrameType(types.ArrayCompatible):
    ndim = 2

    def __init__(self, data=None, index=None, columns=None, dist=None,
        is_table_format=False):
        from bodo.transforms.distributed_analysis import Distribution
        self.data = data
        if index is None:
            index = RangeIndexType(types.none)
        self.index = index
        self.columns = columns
        dist = Distribution.OneD_Var if dist is None else dist
        self.dist = dist
        self.is_table_format = is_table_format
        if columns is None:
            assert is_table_format, 'Determining columns at runtime is only supported for DataFrame with table format'
            self.table_type = TableType(tuple(data[:-1]), True)
        else:
            self.table_type = TableType(data) if is_table_format else None
        super(DataFrameType, self).__init__(name=
            f'dataframe({data}, {index}, {columns}, {dist}, {is_table_format})'
            )

    def __str__(self):
        if not self.has_runtime_cols and len(self.columns) > 20:
            yavkj__mkyht = (
                f'{len(self.data)} columns of types {set(self.data)}')
            hvcy__qvhuj = (
                f"('{self.columns[0]}', '{self.columns[1]}', ..., '{self.columns[-1]}')"
                )
            return (
                f'dataframe({yavkj__mkyht}, {self.index}, {hvcy__qvhuj}, {self.dist}, {self.is_table_format})'
                )
        return super().__str__()

    def copy(self, data=None, index=None, columns=None, dist=None,
        is_table_format=None):
        if data is None:
            data = self.data
        if columns is None:
            columns = self.columns
        if index is None:
            index = self.index
        if dist is None:
            dist = self.dist
        if is_table_format is None:
            is_table_format = self.is_table_format
        return DataFrameType(data, index, columns, dist, is_table_format)

    @property
    def has_runtime_cols(self):
        return self.columns is None

    @cached_property
    def column_index(self):
        return {xeul__cris: i for i, xeul__cris in enumerate(self.columns)}

    @property
    def runtime_colname_typ(self):
        return self.data[-1] if self.has_runtime_cols else None

    @property
    def runtime_data_types(self):
        return self.data[:-1] if self.has_runtime_cols else self.data

    @property
    def as_array(self):
        return types.Array(types.undefined, 2, 'C')

    @property
    def key(self):
        return (self.data, self.index, self.columns, self.dist, self.
            is_table_format)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    def unify(self, typingctx, other):
        from bodo.transforms.distributed_analysis import Distribution
        if (isinstance(other, DataFrameType) and len(other.data) == len(
            self.data) and other.columns == self.columns and other.
            has_runtime_cols == self.has_runtime_cols):
            durnm__kbjgh = (self.index if self.index == other.index else
                self.index.unify(typingctx, other.index))
            data = tuple(pao__ocp.unify(typingctx, psugk__qzc) if pao__ocp !=
                psugk__qzc else pao__ocp for pao__ocp, psugk__qzc in zip(
                self.data, other.data))
            dist = Distribution(min(self.dist.value, other.dist.value))
            if durnm__kbjgh is not None and None not in data:
                return DataFrameType(data, durnm__kbjgh, self.columns, dist,
                    self.is_table_format)
        if isinstance(other, DataFrameType) and len(self.data
            ) == 0 and not self.has_runtime_cols:
            return other

    def can_convert_to(self, typingctx, other):
        from numba.core.typeconv import Conversion
        if (isinstance(other, DataFrameType) and self.data == other.data and
            self.index == other.index and self.columns == other.columns and
            self.dist != other.dist and self.has_runtime_cols == other.
            has_runtime_cols):
            return Conversion.safe

    def is_precise(self):
        return all(pao__ocp.is_precise() for pao__ocp in self.data
            ) and self.index.is_precise()

    def replace_col_type(self, col_name, new_type):
        if col_name not in self.columns:
            raise ValueError(
                f"DataFrameType.replace_col_type replaced column must be found in the DataFrameType. '{col_name}' not found in DataFrameType with columns {self.columns}"
                )
        cmin__jmajn = self.columns.index(col_name)
        nyyss__lzdds = tuple(list(self.data[:cmin__jmajn]) + [new_type] +
            list(self.data[cmin__jmajn + 1:]))
        return DataFrameType(nyyss__lzdds, self.index, self.columns, self.
            dist, self.is_table_format)


def check_runtime_cols_unsupported(df, func_name):
    if isinstance(df, DataFrameType) and df.has_runtime_cols:
        raise BodoError(
            f'{func_name} on DataFrames with columns determined at runtime is not yet supported. Please return the DataFrame to regular Python to update typing information.'
            )


class DataFramePayloadType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        super(DataFramePayloadType, self).__init__(name=
            f'DataFramePayloadType({df_type})')

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(DataFramePayloadType)
class DataFramePayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        data_typ = types.Tuple(fe_type.df_type.data)
        if fe_type.df_type.is_table_format:
            data_typ = types.Tuple([fe_type.df_type.table_type])
        wta__wubn = [('data', data_typ), ('index', fe_type.df_type.index),
            ('parent', types.pyobject)]
        if fe_type.df_type.has_runtime_cols:
            wta__wubn.append(('columns', fe_type.df_type.runtime_colname_typ))
        super(DataFramePayloadModel, self).__init__(dmm, fe_type, wta__wubn)


@register_model(DataFrameType)
class DataFrameModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = DataFramePayloadType(fe_type)
        wta__wubn = [('meminfo', types.MemInfoPointer(payload_type)), (
            'parent', types.pyobject)]
        super(DataFrameModel, self).__init__(dmm, fe_type, wta__wubn)


make_attribute_wrapper(DataFrameType, 'meminfo', '_meminfo')


@infer_getattr
class DataFrameAttribute(OverloadedKeyAttributeTemplate):
    key = DataFrameType

    def resolve_shape(self, df):
        return types.Tuple([types.int64, types.int64])

    @bound_function('df.head')
    def resolve_head(self, df, args, kws):
        func_name = 'DataFrame.head'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        rlo__rcmo = 'n',
        guqnc__tsbd = {'n': 5}
        slml__lsaf, akw__xzcg = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, rlo__rcmo, guqnc__tsbd)
        tjggd__biz = akw__xzcg[0]
        if not is_overload_int(tjggd__biz):
            raise BodoError(f"{func_name}(): 'n' must be an Integer")
        zniy__svwf = df.copy(is_table_format=False)
        return zniy__svwf(*akw__xzcg).replace(pysig=slml__lsaf)

    @bound_function('df.corr')
    def resolve_corr(self, df, args, kws):
        func_name = 'DataFrame.corr'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        lxms__gfc = (df,) + args
        rlo__rcmo = 'df', 'method', 'min_periods'
        guqnc__tsbd = {'method': 'pearson', 'min_periods': 1}
        bzhbt__rhmjz = 'method',
        slml__lsaf, akw__xzcg = bodo.utils.typing.fold_typing_args(func_name,
            lxms__gfc, kws, rlo__rcmo, guqnc__tsbd, bzhbt__rhmjz)
        dmlkg__grd = akw__xzcg[2]
        if not is_overload_int(dmlkg__grd):
            raise BodoError(f"{func_name}(): 'min_periods' must be an Integer")
        dnugw__xsn = []
        seg__ukkr = []
        for xeul__cris, adu__ggr in zip(df.columns, df.data):
            if bodo.utils.typing._is_pandas_numeric_dtype(adu__ggr.dtype):
                dnugw__xsn.append(xeul__cris)
                seg__ukkr.append(types.Array(types.float64, 1, 'A'))
        if len(dnugw__xsn) == 0:
            raise_bodo_error('DataFrame.corr(): requires non-empty dataframe')
        seg__ukkr = tuple(seg__ukkr)
        dnugw__xsn = tuple(dnugw__xsn)
        index_typ = bodo.utils.typing.type_col_to_index(dnugw__xsn)
        zniy__svwf = DataFrameType(seg__ukkr, index_typ, dnugw__xsn)
        return zniy__svwf(*akw__xzcg).replace(pysig=slml__lsaf)

    @bound_function('df.pipe', no_unliteral=True)
    def resolve_pipe(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.pipe()')
        return bodo.hiframes.pd_groupby_ext.resolve_obj_pipe(self, df, args,
            kws, 'DataFrame')

    @bound_function('df.apply', no_unliteral=True)
    def resolve_apply(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.apply()')
        kws = dict(kws)
        dgjh__gwmk = args[0] if len(args) > 0 else kws.pop('func', None)
        axis = args[1] if len(args) > 1 else kws.pop('axis', types.literal(0))
        rmd__bbvtw = args[2] if len(args) > 2 else kws.pop('raw', types.
            literal(False))
        rhr__djcv = args[3] if len(args) > 3 else kws.pop('result_type',
            types.none)
        iimdh__ggm = args[4] if len(args) > 4 else kws.pop('args', types.
            Tuple([]))
        nbuk__punz = dict(raw=rmd__bbvtw, result_type=rhr__djcv)
        mnwao__tgqsh = dict(raw=False, result_type=None)
        check_unsupported_args('Dataframe.apply', nbuk__punz, mnwao__tgqsh,
            package_name='pandas', module_name='DataFrame')
        tks__tiv = True
        if types.unliteral(dgjh__gwmk) == types.unicode_type:
            if not is_overload_constant_str(dgjh__gwmk):
                raise BodoError(
                    f'DataFrame.apply(): string argument (for builtins) must be a compile time constant'
                    )
            tks__tiv = False
        if not is_overload_constant_int(axis):
            raise BodoError(
                'Dataframe.apply(): axis argument must be a compile time constant.'
                )
        mvcox__xdq = get_overload_const_int(axis)
        if tks__tiv and mvcox__xdq != 1:
            raise BodoError(
                'Dataframe.apply(): only axis=1 supported for user-defined functions'
                )
        elif mvcox__xdq not in (0, 1):
            raise BodoError('Dataframe.apply(): axis must be either 0 or 1')
        erkgz__hphfu = []
        for arr_typ in df.data:
            gtez__dtzr = SeriesType(arr_typ.dtype, arr_typ, df.index,
                string_type)
            lte__xzj = self.context.resolve_function_type(operator.getitem,
                (SeriesIlocType(gtez__dtzr), types.int64), {}).return_type
            erkgz__hphfu.append(lte__xzj)
        fgq__qhak = types.none
        ofu__osty = HeterogeneousIndexType(types.BaseTuple.from_types(tuple
            (types.literal(xeul__cris) for xeul__cris in df.columns)), None)
        vgtq__svdng = types.BaseTuple.from_types(erkgz__hphfu)
        cwwbh__ejpfg = types.Tuple([types.bool_] * len(vgtq__svdng))
        hgcf__toop = bodo.NullableTupleType(vgtq__svdng, cwwbh__ejpfg)
        fxu__ishs = df.index.dtype
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df.index,
            'DataFrame.apply()')
        if fxu__ishs == types.NPDatetime('ns'):
            fxu__ishs = bodo.pd_timestamp_type
        if fxu__ishs == types.NPTimedelta('ns'):
            fxu__ishs = bodo.pd_timedelta_type
        if is_heterogeneous_tuple_type(vgtq__svdng):
            roxgv__wtwea = HeterogeneousSeriesType(hgcf__toop, ofu__osty,
                fxu__ishs)
        else:
            roxgv__wtwea = SeriesType(vgtq__svdng.dtype, hgcf__toop,
                ofu__osty, fxu__ishs)
        vze__gzj = roxgv__wtwea,
        if iimdh__ggm is not None:
            vze__gzj += tuple(iimdh__ggm.types)
        try:
            if not tks__tiv:
                bwg__tml = bodo.utils.transform.get_udf_str_return_type(df,
                    get_overload_const_str(dgjh__gwmk), self.context,
                    'DataFrame.apply', axis if mvcox__xdq == 1 else None)
            else:
                bwg__tml = get_const_func_output_type(dgjh__gwmk, vze__gzj,
                    kws, self.context, numba.core.registry.cpu_target.
                    target_context)
        except Exception as yjuv__hzzbp:
            raise_bodo_error(get_udf_error_msg('DataFrame.apply()',
                yjuv__hzzbp))
        if tks__tiv:
            if not (is_overload_constant_int(axis) and 
                get_overload_const_int(axis) == 1):
                raise BodoError(
                    'Dataframe.apply(): only user-defined functions with axis=1 supported'
                    )
            if isinstance(bwg__tml, (SeriesType, HeterogeneousSeriesType)
                ) and bwg__tml.const_info is None:
                raise BodoError(
                    'Invalid Series output in UDF (Series with constant length and constant Index value expected)'
                    )
            if isinstance(bwg__tml, HeterogeneousSeriesType):
                gbry__iziu, karz__avrnx = bwg__tml.const_info
                if isinstance(bwg__tml.data, bodo.libs.nullable_tuple_ext.
                    NullableTupleType):
                    xtmcz__gftm = bwg__tml.data.tuple_typ.types
                elif isinstance(bwg__tml.data, types.Tuple):
                    xtmcz__gftm = bwg__tml.data.types
                else:
                    raise_bodo_error(
                        'df.apply(): Unexpected Series return type for Heterogeneous data'
                        )
                vhr__novz = tuple(to_nullable_type(dtype_to_array_type(
                    wqca__bqmko)) for wqca__bqmko in xtmcz__gftm)
                sszby__arezd = DataFrameType(vhr__novz, df.index, karz__avrnx)
            elif isinstance(bwg__tml, SeriesType):
                kuvr__ame, karz__avrnx = bwg__tml.const_info
                vhr__novz = tuple(to_nullable_type(dtype_to_array_type(
                    bwg__tml.dtype)) for gbry__iziu in range(kuvr__ame))
                sszby__arezd = DataFrameType(vhr__novz, df.index, karz__avrnx)
            else:
                tteyf__hkhdw = get_udf_out_arr_type(bwg__tml)
                sszby__arezd = SeriesType(tteyf__hkhdw.dtype, tteyf__hkhdw,
                    df.index, None)
        else:
            sszby__arezd = bwg__tml
        trt__cwlv = ', '.join("{} = ''".format(pao__ocp) for pao__ocp in
            kws.keys())
        hljtn__idzh = f"""def apply_stub(func, axis=0, raw=False, result_type=None, args=(), {trt__cwlv}):
"""
        hljtn__idzh += '    pass\n'
        qpcx__wxpnc = {}
        exec(hljtn__idzh, {}, qpcx__wxpnc)
        ajcmn__yvs = qpcx__wxpnc['apply_stub']
        slml__lsaf = numba.core.utils.pysignature(ajcmn__yvs)
        qxri__mzze = (dgjh__gwmk, axis, rmd__bbvtw, rhr__djcv, iimdh__ggm
            ) + tuple(kws.values())
        return signature(sszby__arezd, *qxri__mzze).replace(pysig=slml__lsaf)

    @bound_function('df.plot', no_unliteral=True)
    def resolve_plot(self, df, args, kws):
        func_name = 'DataFrame.plot'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        rlo__rcmo = ('x', 'y', 'kind', 'figsize', 'ax', 'subplots',
            'sharex', 'sharey', 'layout', 'use_index', 'title', 'grid',
            'legend', 'style', 'logx', 'logy', 'loglog', 'xticks', 'yticks',
            'xlim', 'ylim', 'rot', 'fontsize', 'colormap', 'table', 'yerr',
            'xerr', 'secondary_y', 'sort_columns', 'xlabel', 'ylabel',
            'position', 'stacked', 'mark_right', 'include_bool', 'backend')
        guqnc__tsbd = {'x': None, 'y': None, 'kind': 'line', 'figsize':
            None, 'ax': None, 'subplots': False, 'sharex': None, 'sharey': 
            False, 'layout': None, 'use_index': True, 'title': None, 'grid':
            None, 'legend': True, 'style': None, 'logx': False, 'logy': 
            False, 'loglog': False, 'xticks': None, 'yticks': None, 'xlim':
            None, 'ylim': None, 'rot': None, 'fontsize': None, 'colormap':
            None, 'table': False, 'yerr': None, 'xerr': None, 'secondary_y':
            False, 'sort_columns': False, 'xlabel': None, 'ylabel': None,
            'position': 0.5, 'stacked': False, 'mark_right': True,
            'include_bool': False, 'backend': None}
        bzhbt__rhmjz = ('subplots', 'sharex', 'sharey', 'layout',
            'use_index', 'grid', 'style', 'logx', 'logy', 'loglog', 'xlim',
            'ylim', 'rot', 'colormap', 'table', 'yerr', 'xerr',
            'sort_columns', 'secondary_y', 'colorbar', 'position',
            'stacked', 'mark_right', 'include_bool', 'backend')
        slml__lsaf, akw__xzcg = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, rlo__rcmo, guqnc__tsbd, bzhbt__rhmjz)
        nlqa__ilnsn = akw__xzcg[2]
        if not is_overload_constant_str(nlqa__ilnsn):
            raise BodoError(
                f"{func_name}: kind must be a constant string and one of ('line', 'scatter')."
                )
        abhge__kjkob = akw__xzcg[0]
        if not is_overload_none(abhge__kjkob) and not (is_overload_int(
            abhge__kjkob) or is_overload_constant_str(abhge__kjkob)):
            raise BodoError(
                f'{func_name}: x must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(abhge__kjkob):
            yhfib__dzpr = get_overload_const_str(abhge__kjkob)
            if yhfib__dzpr not in df.columns:
                raise BodoError(f'{func_name}: {yhfib__dzpr} column not found.'
                    )
        elif is_overload_int(abhge__kjkob):
            hwuv__lijpu = get_overload_const_int(abhge__kjkob)
            if hwuv__lijpu > len(df.columns):
                raise BodoError(
                    f'{func_name}: x: {hwuv__lijpu} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            abhge__kjkob = df.columns[abhge__kjkob]
        ggrpo__mmgyj = akw__xzcg[1]
        if not is_overload_none(ggrpo__mmgyj) and not (is_overload_int(
            ggrpo__mmgyj) or is_overload_constant_str(ggrpo__mmgyj)):
            raise BodoError(
                'df.plot(): y must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(ggrpo__mmgyj):
            fcaho__epu = get_overload_const_str(ggrpo__mmgyj)
            if fcaho__epu not in df.columns:
                raise BodoError(f'{func_name}: {fcaho__epu} column not found.')
        elif is_overload_int(ggrpo__mmgyj):
            odm__mjts = get_overload_const_int(ggrpo__mmgyj)
            if odm__mjts > len(df.columns):
                raise BodoError(
                    f'{func_name}: y: {odm__mjts} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            ggrpo__mmgyj = df.columns[ggrpo__mmgyj]
        dovz__itiel = akw__xzcg[3]
        if not is_overload_none(dovz__itiel) and not is_tuple_like_type(
            dovz__itiel):
            raise BodoError(
                f'{func_name}: figsize must be a constant numeric tuple (width, height) or None.'
                )
        hnrif__zeni = akw__xzcg[10]
        if not is_overload_none(hnrif__zeni) and not is_overload_constant_str(
            hnrif__zeni):
            raise BodoError(
                f'{func_name}: title must be a constant string or None.')
        asah__zahr = akw__xzcg[12]
        if not is_overload_bool(asah__zahr):
            raise BodoError(f'{func_name}: legend must be a boolean type.')
        rug__eujh = akw__xzcg[17]
        if not is_overload_none(rug__eujh) and not is_tuple_like_type(rug__eujh
            ):
            raise BodoError(
                f'{func_name}: xticks must be a constant tuple or None.')
        bsfx__jny = akw__xzcg[18]
        if not is_overload_none(bsfx__jny) and not is_tuple_like_type(bsfx__jny
            ):
            raise BodoError(
                f'{func_name}: yticks must be a constant tuple or None.')
        gumcj__shl = akw__xzcg[22]
        if not is_overload_none(gumcj__shl) and not is_overload_int(gumcj__shl
            ):
            raise BodoError(
                f'{func_name}: fontsize must be an integer or None.')
        tuhf__zdsm = akw__xzcg[29]
        if not is_overload_none(tuhf__zdsm) and not is_overload_constant_str(
            tuhf__zdsm):
            raise BodoError(
                f'{func_name}: xlabel must be a constant string or None.')
        xnghe__awb = akw__xzcg[30]
        if not is_overload_none(xnghe__awb) and not is_overload_constant_str(
            xnghe__awb):
            raise BodoError(
                f'{func_name}: ylabel must be a constant string or None.')
        kbwa__sbqlm = types.List(types.mpl_line_2d_type)
        nlqa__ilnsn = get_overload_const_str(nlqa__ilnsn)
        if nlqa__ilnsn == 'scatter':
            if is_overload_none(abhge__kjkob) and is_overload_none(ggrpo__mmgyj
                ):
                raise BodoError(
                    f'{func_name}: {nlqa__ilnsn} requires an x and y column.')
            elif is_overload_none(abhge__kjkob):
                raise BodoError(
                    f'{func_name}: {nlqa__ilnsn} x column is missing.')
            elif is_overload_none(ggrpo__mmgyj):
                raise BodoError(
                    f'{func_name}: {nlqa__ilnsn} y column is missing.')
            kbwa__sbqlm = types.mpl_path_collection_type
        elif nlqa__ilnsn != 'line':
            raise BodoError(
                f'{func_name}: {nlqa__ilnsn} plot is not supported.')
        return signature(kbwa__sbqlm, *akw__xzcg).replace(pysig=slml__lsaf)

    def generic_resolve(self, df, attr):
        if self._is_existing_attr(attr):
            return
        check_runtime_cols_unsupported(df,
            'Acessing DataFrame columns by attribute')
        if attr in df.columns:
            qqr__ejxad = df.columns.index(attr)
            arr_typ = df.data[qqr__ejxad]
            return SeriesType(arr_typ.dtype, arr_typ, df.index, types.
                StringLiteral(attr))
        if len(df.columns) > 0 and isinstance(df.columns[0], tuple):
            rbyqg__knr = []
            nyyss__lzdds = []
            chz__flbqp = False
            for i, lkhk__mhaau in enumerate(df.columns):
                if lkhk__mhaau[0] != attr:
                    continue
                chz__flbqp = True
                rbyqg__knr.append(lkhk__mhaau[1] if len(lkhk__mhaau) == 2 else
                    lkhk__mhaau[1:])
                nyyss__lzdds.append(df.data[i])
            if chz__flbqp:
                return DataFrameType(tuple(nyyss__lzdds), df.index, tuple(
                    rbyqg__knr))


DataFrameAttribute._no_unliteral = True


@overload(operator.getitem, no_unliteral=True)
def namedtuple_getitem_overload(tup, idx):
    if isinstance(tup, types.BaseNamedTuple) and is_overload_constant_str(idx):
        luft__ecsky = get_overload_const_str(idx)
        val_ind = tup.instance_class._fields.index(luft__ecsky)
        return lambda tup, idx: tup[val_ind]


def decref_df_data(context, builder, payload, df_type):
    if df_type.is_table_format:
        context.nrt.decref(builder, df_type.table_type, builder.
            extract_value(payload.data, 0))
        context.nrt.decref(builder, df_type.index, payload.index)
        if df_type.has_runtime_cols:
            context.nrt.decref(builder, df_type.data[-1], payload.columns)
        return
    for i in range(len(df_type.data)):
        bhnva__oul = builder.extract_value(payload.data, i)
        context.nrt.decref(builder, df_type.data[i], bhnva__oul)
    context.nrt.decref(builder, df_type.index, payload.index)


def define_df_dtor(context, builder, df_type, payload_type):
    fyy__oizly = builder.module
    zngc__bgrdb = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    xfkx__xyc = cgutils.get_or_insert_function(fyy__oizly, zngc__bgrdb,
        name='.dtor.df.{}'.format(df_type))
    if not xfkx__xyc.is_declaration:
        return xfkx__xyc
    xfkx__xyc.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(xfkx__xyc.append_basic_block())
    rsas__rca = xfkx__xyc.args[0]
    mxh__ibsk = context.get_value_type(payload_type).as_pointer()
    nzs__kqu = builder.bitcast(rsas__rca, mxh__ibsk)
    payload = context.make_helper(builder, payload_type, ref=nzs__kqu)
    decref_df_data(context, builder, payload, df_type)
    has_parent = cgutils.is_not_null(builder, payload.parent)
    with builder.if_then(has_parent):
        urjp__srhe = context.get_python_api(builder)
        whi__bevpa = urjp__srhe.gil_ensure()
        urjp__srhe.decref(payload.parent)
        urjp__srhe.gil_release(whi__bevpa)
    builder.ret_void()
    return xfkx__xyc


def construct_dataframe(context, builder, df_type, data_tup, index_val,
    parent=None, colnames=None):
    payload_type = DataFramePayloadType(df_type)
    xpql__fda = cgutils.create_struct_proxy(payload_type)(context, builder)
    xpql__fda.data = data_tup
    xpql__fda.index = index_val
    if colnames is not None:
        assert df_type.has_runtime_cols, 'construct_dataframe can only provide colnames if columns are determined at runtime'
        xpql__fda.columns = colnames
    kbc__vxmn = context.get_value_type(payload_type)
    rit__uekoy = context.get_abi_sizeof(kbc__vxmn)
    jxih__hlo = define_df_dtor(context, builder, df_type, payload_type)
    zfxx__rwmu = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, rit__uekoy), jxih__hlo)
    rtdi__twfbk = context.nrt.meminfo_data(builder, zfxx__rwmu)
    jgj__beach = builder.bitcast(rtdi__twfbk, kbc__vxmn.as_pointer())
    uyxy__lgm = cgutils.create_struct_proxy(df_type)(context, builder)
    uyxy__lgm.meminfo = zfxx__rwmu
    if parent is None:
        uyxy__lgm.parent = cgutils.get_null_value(uyxy__lgm.parent.type)
    else:
        uyxy__lgm.parent = parent
        xpql__fda.parent = parent
        has_parent = cgutils.is_not_null(builder, parent)
        with builder.if_then(has_parent):
            urjp__srhe = context.get_python_api(builder)
            whi__bevpa = urjp__srhe.gil_ensure()
            urjp__srhe.incref(parent)
            urjp__srhe.gil_release(whi__bevpa)
    builder.store(xpql__fda._getvalue(), jgj__beach)
    return uyxy__lgm._getvalue()


@intrinsic
def init_runtime_cols_dataframe(typingctx, data_typ, index_typ,
    colnames_index_typ=None):
    assert isinstance(data_typ, types.BaseTuple) and isinstance(data_typ.
        dtype, TableType
        ) and data_typ.dtype.has_runtime_cols, 'init_runtime_cols_dataframe must be called with a table that determines columns at runtime.'
    assert bodo.hiframes.pd_index_ext.is_pd_index_type(colnames_index_typ
        ) or isinstance(colnames_index_typ, bodo.hiframes.
        pd_multi_index_ext.MultiIndexType), 'Column names must be an index'
    if isinstance(data_typ.dtype.arr_types, types.UniTuple):
        xcrpb__lwxx = [data_typ.dtype.arr_types.dtype] * len(data_typ.dtype
            .arr_types)
    else:
        xcrpb__lwxx = [wqca__bqmko for wqca__bqmko in data_typ.dtype.arr_types]
    zlvi__znh = DataFrameType(tuple(xcrpb__lwxx + [colnames_index_typ]),
        index_typ, None, is_table_format=True)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup, index, col_names = args
        parent = None
        zbfx__dgi = construct_dataframe(context, builder, df_type, data_tup,
            index, parent, col_names)
        context.nrt.incref(builder, data_typ, data_tup)
        context.nrt.incref(builder, index_typ, index)
        context.nrt.incref(builder, colnames_index_typ, col_names)
        return zbfx__dgi
    sig = signature(zlvi__znh, data_typ, index_typ, colnames_index_typ)
    return sig, codegen


@intrinsic
def init_dataframe(typingctx, data_tup_typ, index_typ, col_names_typ=None):
    assert is_pd_index_type(index_typ) or isinstance(index_typ, MultiIndexType
        ), 'init_dataframe(): invalid index type'
    kuvr__ame = len(data_tup_typ.types)
    if kuvr__ame == 0:
        column_names = ()
    elif isinstance(col_names_typ, types.TypeRef):
        column_names = col_names_typ.instance_type.columns
    else:
        column_names = get_const_tup_vals(col_names_typ)
    if kuvr__ame == 1 and isinstance(data_tup_typ.types[0], TableType):
        kuvr__ame = len(data_tup_typ.types[0].arr_types)
    assert len(column_names
        ) == kuvr__ame, 'init_dataframe(): number of column names does not match number of columns'
    is_table_format = False
    tzq__ofh = data_tup_typ.types
    if kuvr__ame != 0 and isinstance(data_tup_typ.types[0], TableType):
        tzq__ofh = data_tup_typ.types[0].arr_types
        is_table_format = True
    zlvi__znh = DataFrameType(tzq__ofh, index_typ, column_names,
        is_table_format=is_table_format)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup = args[0]
        index_val = args[1]
        parent = None
        if is_table_format:
            cpzd__hqbkz = cgutils.create_struct_proxy(zlvi__znh.table_type)(
                context, builder, builder.extract_value(data_tup, 0))
            parent = cpzd__hqbkz.parent
        zbfx__dgi = construct_dataframe(context, builder, df_type, data_tup,
            index_val, parent, None)
        context.nrt.incref(builder, data_tup_typ, data_tup)
        context.nrt.incref(builder, index_typ, index_val)
        return zbfx__dgi
    sig = signature(zlvi__znh, data_tup_typ, index_typ, col_names_typ)
    return sig, codegen


@intrinsic
def has_parent(typingctx, df=None):
    check_runtime_cols_unsupported(df, 'has_parent')

    def codegen(context, builder, sig, args):
        uyxy__lgm = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        return cgutils.is_not_null(builder, uyxy__lgm.parent)
    return signature(types.bool_, df), codegen


@intrinsic
def _column_needs_unboxing(typingctx, df_typ, i_typ=None):
    check_runtime_cols_unsupported(df_typ, '_column_needs_unboxing')
    assert isinstance(df_typ, DataFrameType) and is_overload_constant_int(i_typ
        )

    def codegen(context, builder, sig, args):
        xpql__fda = get_dataframe_payload(context, builder, df_typ, args[0])
        lisq__stkt = get_overload_const_int(i_typ)
        arr_typ = df_typ.data[lisq__stkt]
        if df_typ.is_table_format:
            cpzd__hqbkz = cgutils.create_struct_proxy(df_typ.table_type)(
                context, builder, builder.extract_value(xpql__fda.data, 0))
            dvon__xyjb = df_typ.table_type.type_to_blk[arr_typ]
            qapf__uhaf = getattr(cpzd__hqbkz, f'block_{dvon__xyjb}')
            icsrj__kvrb = ListInstance(context, builder, types.List(arr_typ
                ), qapf__uhaf)
            pzici__pig = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[lisq__stkt])
            bhnva__oul = icsrj__kvrb.getitem(pzici__pig)
        else:
            bhnva__oul = builder.extract_value(xpql__fda.data, lisq__stkt)
        ngook__loqx = cgutils.alloca_once_value(builder, bhnva__oul)
        dqmz__jaw = cgutils.alloca_once_value(builder, context.
            get_constant_null(arr_typ))
        return is_ll_eq(builder, ngook__loqx, dqmz__jaw)
    return signature(types.bool_, df_typ, i_typ), codegen


def get_dataframe_payload(context, builder, df_type, value):
    zfxx__rwmu = cgutils.create_struct_proxy(df_type)(context, builder, value
        ).meminfo
    payload_type = DataFramePayloadType(df_type)
    payload = context.nrt.meminfo_data(builder, zfxx__rwmu)
    mxh__ibsk = context.get_value_type(payload_type).as_pointer()
    payload = builder.bitcast(payload, mxh__ibsk)
    return context.make_helper(builder, payload_type, ref=payload)


@intrinsic
def _get_dataframe_data(typingctx, df_typ=None):
    check_runtime_cols_unsupported(df_typ, '_get_dataframe_data')
    zlvi__znh = types.Tuple(df_typ.data)
    if df_typ.is_table_format:
        zlvi__znh = types.Tuple([TableType(df_typ.data)])
    sig = signature(zlvi__znh, df_typ)

    def codegen(context, builder, signature, args):
        xpql__fda = get_dataframe_payload(context, builder, signature.args[
            0], args[0])
        return impl_ret_borrowed(context, builder, signature.return_type,
            xpql__fda.data)
    return sig, codegen


@intrinsic
def get_dataframe_index(typingctx, df_typ=None):

    def codegen(context, builder, signature, args):
        xpql__fda = get_dataframe_payload(context, builder, signature.args[
            0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.index, xpql__fda.
            index)
    zlvi__znh = df_typ.index
    sig = signature(zlvi__znh, df_typ)
    return sig, codegen


def get_dataframe_data(df, i):
    return df[i]


@infer_global(get_dataframe_data)
class GetDataFrameDataInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        if not is_overload_constant_int(args[1]):
            raise_bodo_error(
                'Selecting a DataFrame column requires a constant column label'
                )
        df = args[0]
        check_runtime_cols_unsupported(df, 'get_dataframe_data')
        i = get_overload_const_int(args[1])
        zniy__svwf = df.data[i]
        return zniy__svwf(*args)


GetDataFrameDataInfer.prefer_literal = True


def get_dataframe_data_impl(df, i):
    if df.is_table_format:

        def _impl(df, i):
            if has_parent(df) and _column_needs_unboxing(df, i):
                bodo.hiframes.boxing.unbox_dataframe_column(df, i)
            return get_table_data(_get_dataframe_data(df)[0], i)
        return _impl

    def _impl(df, i):
        if has_parent(df) and _column_needs_unboxing(df, i):
            bodo.hiframes.boxing.unbox_dataframe_column(df, i)
        return _get_dataframe_data(df)[i]
    return _impl


@intrinsic
def get_dataframe_table(typingctx, df_typ=None):
    assert df_typ.is_table_format, 'get_dataframe_table() expects table format'

    def codegen(context, builder, signature, args):
        xpql__fda = get_dataframe_payload(context, builder, signature.args[
            0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.table_type,
            builder.extract_value(xpql__fda.data, 0))
    return df_typ.table_type(df_typ), codegen


@intrinsic
def get_dataframe_column_names(typingctx, df_typ=None):
    assert df_typ.has_runtime_cols, 'get_dataframe_column_names() expects columns to be determined at runtime'

    def codegen(context, builder, signature, args):
        xpql__fda = get_dataframe_payload(context, builder, signature.args[
            0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.
            runtime_colname_typ, xpql__fda.columns)
    return df_typ.runtime_colname_typ(df_typ), codegen


@lower_builtin(get_dataframe_data, DataFrameType, types.IntegerLiteral)
def lower_get_dataframe_data(context, builder, sig, args):
    impl = get_dataframe_data_impl(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_dataframe_data',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_dataframe_index',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_dataframe_table',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func


def alias_ext_init_dataframe(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 3
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_dataframe',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_init_dataframe


def init_dataframe_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 3 and not kws
    data_tup = args[0]
    index = args[1]
    vgtq__svdng = self.typemap[data_tup.name]
    if any(is_tuple_like_type(wqca__bqmko) for wqca__bqmko in vgtq__svdng.types
        ):
        return None
    if equiv_set.has_shape(data_tup):
        aamcy__dzpwq = equiv_set.get_shape(data_tup)
        if len(aamcy__dzpwq) > 1:
            equiv_set.insert_equiv(*aamcy__dzpwq)
        if len(aamcy__dzpwq) > 0:
            ofu__osty = self.typemap[index.name]
            if not isinstance(ofu__osty, HeterogeneousIndexType
                ) and equiv_set.has_shape(index):
                equiv_set.insert_equiv(aamcy__dzpwq[0], index)
            return ArrayAnalysis.AnalyzeResult(shape=(aamcy__dzpwq[0], len(
                aamcy__dzpwq)), pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_dataframe_ext_init_dataframe
    ) = init_dataframe_equiv


def get_dataframe_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    hax__bmkg = args[0]
    data_types = self.typemap[hax__bmkg.name].data
    if any(is_tuple_like_type(wqca__bqmko) for wqca__bqmko in data_types):
        return None
    if equiv_set.has_shape(hax__bmkg):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            hax__bmkg)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_data
    ) = get_dataframe_data_equiv


def get_dataframe_index_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 1 and not kws
    hax__bmkg = args[0]
    ofu__osty = self.typemap[hax__bmkg.name].index
    if isinstance(ofu__osty, HeterogeneousIndexType):
        return None
    if equiv_set.has_shape(hax__bmkg):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            hax__bmkg)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_index
    ) = get_dataframe_index_equiv


def get_dataframe_table_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    hax__bmkg = args[0]
    if equiv_set.has_shape(hax__bmkg):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            hax__bmkg), pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_table
    ) = get_dataframe_table_equiv


def get_dataframe_column_names_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    hax__bmkg = args[0]
    if equiv_set.has_shape(hax__bmkg):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            hax__bmkg)[1], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_column_names
    ) = get_dataframe_column_names_equiv


@intrinsic
def set_dataframe_data(typingctx, df_typ, c_ind_typ, arr_typ=None):
    check_runtime_cols_unsupported(df_typ, 'set_dataframe_data')
    assert is_overload_constant_int(c_ind_typ)
    lisq__stkt = get_overload_const_int(c_ind_typ)
    if df_typ.data[lisq__stkt] != arr_typ:
        raise BodoError(
            'Changing dataframe column data type inplace is not supported in conditionals/loops or for dataframe arguments'
            )

    def codegen(context, builder, signature, args):
        mhok__sdxta, gbry__iziu, mnbch__znasz = args
        xpql__fda = get_dataframe_payload(context, builder, df_typ, mhok__sdxta
            )
        if df_typ.is_table_format:
            cpzd__hqbkz = cgutils.create_struct_proxy(df_typ.table_type)(
                context, builder, builder.extract_value(xpql__fda.data, 0))
            dvon__xyjb = df_typ.table_type.type_to_blk[arr_typ]
            qapf__uhaf = getattr(cpzd__hqbkz, f'block_{dvon__xyjb}')
            icsrj__kvrb = ListInstance(context, builder, types.List(arr_typ
                ), qapf__uhaf)
            pzici__pig = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[lisq__stkt])
            icsrj__kvrb.setitem(pzici__pig, mnbch__znasz, True)
        else:
            bhnva__oul = builder.extract_value(xpql__fda.data, lisq__stkt)
            context.nrt.decref(builder, df_typ.data[lisq__stkt], bhnva__oul)
            xpql__fda.data = builder.insert_value(xpql__fda.data,
                mnbch__znasz, lisq__stkt)
            context.nrt.incref(builder, arr_typ, mnbch__znasz)
        uyxy__lgm = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=mhok__sdxta)
        payload_type = DataFramePayloadType(df_typ)
        nzs__kqu = context.nrt.meminfo_data(builder, uyxy__lgm.meminfo)
        mxh__ibsk = context.get_value_type(payload_type).as_pointer()
        nzs__kqu = builder.bitcast(nzs__kqu, mxh__ibsk)
        builder.store(xpql__fda._getvalue(), nzs__kqu)
        return impl_ret_borrowed(context, builder, df_typ, mhok__sdxta)
    sig = signature(df_typ, df_typ, c_ind_typ, arr_typ)
    return sig, codegen


@intrinsic
def set_df_index(typingctx, df_t, index_t=None):
    check_runtime_cols_unsupported(df_t, 'set_df_index')

    def codegen(context, builder, signature, args):
        vedz__sjjo = args[0]
        index_val = args[1]
        df_typ = signature.args[0]
        vujcd__fabl = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=vedz__sjjo)
        srrv__gxre = get_dataframe_payload(context, builder, df_typ, vedz__sjjo
            )
        uyxy__lgm = construct_dataframe(context, builder, signature.
            return_type, srrv__gxre.data, index_val, vujcd__fabl.parent, None)
        context.nrt.incref(builder, index_t, index_val)
        context.nrt.incref(builder, types.Tuple(df_t.data), srrv__gxre.data)
        return uyxy__lgm
    zlvi__znh = DataFrameType(df_t.data, index_t, df_t.columns, df_t.dist,
        df_t.is_table_format)
    sig = signature(zlvi__znh, df_t, index_t)
    return sig, codegen


@intrinsic
def set_df_column_with_reflect(typingctx, df_type, cname_type, arr_type=None):
    check_runtime_cols_unsupported(df_type, 'set_df_column_with_reflect')
    assert is_literal_type(cname_type), 'constant column name expected'
    col_name = get_literal_value(cname_type)
    kuvr__ame = len(df_type.columns)
    iyfc__jxsw = kuvr__ame
    ote__ksi = df_type.data
    column_names = df_type.columns
    index_typ = df_type.index
    kcrob__cpp = col_name not in df_type.columns
    lisq__stkt = kuvr__ame
    if kcrob__cpp:
        ote__ksi += arr_type,
        column_names += col_name,
        iyfc__jxsw += 1
    else:
        lisq__stkt = df_type.columns.index(col_name)
        ote__ksi = tuple(arr_type if i == lisq__stkt else ote__ksi[i] for i in
            range(kuvr__ame))

    def codegen(context, builder, signature, args):
        mhok__sdxta, gbry__iziu, mnbch__znasz = args
        in_dataframe_payload = get_dataframe_payload(context, builder,
            df_type, mhok__sdxta)
        ppud__jnmx = cgutils.create_struct_proxy(df_type)(context, builder,
            value=mhok__sdxta)
        if df_type.is_table_format:
            fwsl__mviz = df_type.table_type
            pjy__mnqfs = builder.extract_value(in_dataframe_payload.data, 0)
            exo__kqwa = TableType(ote__ksi)
            azmex__squ = set_table_data_codegen(context, builder,
                fwsl__mviz, pjy__mnqfs, exo__kqwa, arr_type, mnbch__znasz,
                lisq__stkt, kcrob__cpp)
            data_tup = context.make_tuple(builder, types.Tuple([exo__kqwa]),
                [azmex__squ])
        else:
            tzq__ofh = [(builder.extract_value(in_dataframe_payload.data, i
                ) if i != lisq__stkt else mnbch__znasz) for i in range(
                kuvr__ame)]
            if kcrob__cpp:
                tzq__ofh.append(mnbch__znasz)
            for hax__bmkg, ofy__mpq in zip(tzq__ofh, ote__ksi):
                context.nrt.incref(builder, ofy__mpq, hax__bmkg)
            data_tup = context.make_tuple(builder, types.Tuple(ote__ksi),
                tzq__ofh)
        index_val = in_dataframe_payload.index
        context.nrt.incref(builder, index_typ, index_val)
        jxvb__wyf = construct_dataframe(context, builder, signature.
            return_type, data_tup, index_val, ppud__jnmx.parent, None)
        if not kcrob__cpp and arr_type == df_type.data[lisq__stkt]:
            decref_df_data(context, builder, in_dataframe_payload, df_type)
            payload_type = DataFramePayloadType(df_type)
            nzs__kqu = context.nrt.meminfo_data(builder, ppud__jnmx.meminfo)
            mxh__ibsk = context.get_value_type(payload_type).as_pointer()
            nzs__kqu = builder.bitcast(nzs__kqu, mxh__ibsk)
            bkh__kcz = get_dataframe_payload(context, builder, df_type,
                jxvb__wyf)
            builder.store(bkh__kcz._getvalue(), nzs__kqu)
            context.nrt.incref(builder, index_typ, index_val)
            if df_type.is_table_format:
                context.nrt.incref(builder, exo__kqwa, builder.
                    extract_value(data_tup, 0))
            else:
                for hax__bmkg, ofy__mpq in zip(tzq__ofh, ote__ksi):
                    context.nrt.incref(builder, ofy__mpq, hax__bmkg)
        has_parent = cgutils.is_not_null(builder, ppud__jnmx.parent)
        with builder.if_then(has_parent):
            urjp__srhe = context.get_python_api(builder)
            whi__bevpa = urjp__srhe.gil_ensure()
            xjwzq__jzfwa = context.get_env_manager(builder)
            context.nrt.incref(builder, arr_type, mnbch__znasz)
            xeul__cris = numba.core.pythonapi._BoxContext(context, builder,
                urjp__srhe, xjwzq__jzfwa)
            ukf__mxif = xeul__cris.pyapi.from_native_value(arr_type,
                mnbch__znasz, xeul__cris.env_manager)
            if isinstance(col_name, str):
                yztbo__wia = context.insert_const_string(builder.module,
                    col_name)
                sjthg__sbifh = urjp__srhe.string_from_string(yztbo__wia)
            else:
                assert isinstance(col_name, int)
                sjthg__sbifh = urjp__srhe.long_from_longlong(context.
                    get_constant(types.intp, col_name))
            urjp__srhe.object_setitem(ppud__jnmx.parent, sjthg__sbifh,
                ukf__mxif)
            urjp__srhe.decref(ukf__mxif)
            urjp__srhe.decref(sjthg__sbifh)
            urjp__srhe.gil_release(whi__bevpa)
        return jxvb__wyf
    zlvi__znh = DataFrameType(ote__ksi, index_typ, column_names, df_type.
        dist, df_type.is_table_format)
    sig = signature(zlvi__znh, df_type, cname_type, arr_type)
    return sig, codegen


@lower_constant(DataFrameType)
def lower_constant_dataframe(context, builder, df_type, pyval):
    check_runtime_cols_unsupported(df_type, 'lowering a constant DataFrame')
    kuvr__ame = len(pyval.columns)
    tzq__ofh = []
    for i in range(kuvr__ame):
        zequ__mioy = pyval.iloc[:, i]
        if isinstance(df_type.data[i], bodo.DatetimeArrayType):
            ukf__mxif = zequ__mioy.array
        else:
            ukf__mxif = zequ__mioy.values
        tzq__ofh.append(ukf__mxif)
    tzq__ofh = tuple(tzq__ofh)
    if df_type.is_table_format:
        cpzd__hqbkz = context.get_constant_generic(builder, df_type.
            table_type, Table(tzq__ofh))
        data_tup = lir.Constant.literal_struct([cpzd__hqbkz])
    else:
        data_tup = lir.Constant.literal_struct([context.
            get_constant_generic(builder, df_type.data[i], lkhk__mhaau) for
            i, lkhk__mhaau in enumerate(tzq__ofh)])
    index_val = context.get_constant_generic(builder, df_type.index, pyval.
        index)
    mgxk__ycdf = context.get_constant_null(types.pyobject)
    payload = lir.Constant.literal_struct([data_tup, index_val, mgxk__ycdf])
    payload = cgutils.global_constant(builder, '.const.payload', payload
        ).bitcast(cgutils.voidptr_t)
    yha__vuy = context.get_constant(types.int64, -1)
    kwpos__cyp = context.get_constant_null(types.voidptr)
    zfxx__rwmu = lir.Constant.literal_struct([yha__vuy, kwpos__cyp,
        kwpos__cyp, payload, yha__vuy])
    zfxx__rwmu = cgutils.global_constant(builder, '.const.meminfo', zfxx__rwmu
        ).bitcast(cgutils.voidptr_t)
    return lir.Constant.literal_struct([zfxx__rwmu, mgxk__ycdf])


@lower_cast(DataFrameType, DataFrameType)
def cast_df_to_df(context, builder, fromty, toty, val):
    if (fromty.data == toty.data and fromty.index == toty.index and fromty.
        columns == toty.columns and fromty.is_table_format == toty.
        is_table_format and fromty.dist != toty.dist and fromty.
        has_runtime_cols == toty.has_runtime_cols):
        return val
    if not fromty.has_runtime_cols and not toty.has_runtime_cols and len(fromty
        .data) == 0 and len(toty.columns):
        return _cast_empty_df(context, builder, toty)
    if len(fromty.data) != len(toty.data) or fromty.data != toty.data and any(
        context.typing_context.unify_pairs(fromty.data[i], toty.data[i]) is
        None for i in range(len(fromty.data))
        ) or fromty.has_runtime_cols != toty.has_runtime_cols:
        raise BodoError(f'Invalid dataframe cast from {fromty} to {toty}')
    in_dataframe_payload = get_dataframe_payload(context, builder, fromty, val)
    if isinstance(fromty.index, RangeIndexType) and isinstance(toty.index,
        NumericIndexType):
        durnm__kbjgh = context.cast(builder, in_dataframe_payload.index,
            fromty.index, toty.index)
    else:
        durnm__kbjgh = in_dataframe_payload.index
        context.nrt.incref(builder, fromty.index, durnm__kbjgh)
    if (fromty.is_table_format == toty.is_table_format and fromty.data ==
        toty.data):
        nyyss__lzdds = in_dataframe_payload.data
        if fromty.is_table_format:
            context.nrt.incref(builder, types.Tuple([fromty.table_type]),
                nyyss__lzdds)
        else:
            context.nrt.incref(builder, types.BaseTuple.from_types(fromty.
                data), nyyss__lzdds)
    elif not fromty.is_table_format and toty.is_table_format:
        nyyss__lzdds = _cast_df_data_to_table_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    elif fromty.is_table_format and not toty.is_table_format:
        nyyss__lzdds = _cast_df_data_to_tuple_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    elif fromty.is_table_format and toty.is_table_format:
        nyyss__lzdds = _cast_df_data_keep_table_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    else:
        nyyss__lzdds = _cast_df_data_keep_tuple_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    return construct_dataframe(context, builder, toty, nyyss__lzdds,
        durnm__kbjgh, in_dataframe_payload.parent, None)


def _cast_empty_df(context, builder, toty):
    pbqvp__bnf = {}
    if isinstance(toty.index, RangeIndexType):
        index = 'bodo.hiframes.pd_index_ext.init_range_index(0, 0, 1, None)'
    else:
        iisi__uhmk = get_index_data_arr_types(toty.index)[0]
        lcz__eoqh = bodo.utils.transform.get_type_alloc_counts(iisi__uhmk) - 1
        tto__edee = ', '.join('0' for gbry__iziu in range(lcz__eoqh))
        index = (
            'bodo.utils.conversion.index_from_array(bodo.utils.utils.alloc_type(0, index_arr_type, ({}{})))'
            .format(tto__edee, ', ' if lcz__eoqh == 1 else ''))
        pbqvp__bnf['index_arr_type'] = iisi__uhmk
    ytwz__vqhd = []
    for i, arr_typ in enumerate(toty.data):
        lcz__eoqh = bodo.utils.transform.get_type_alloc_counts(arr_typ) - 1
        tto__edee = ', '.join('0' for gbry__iziu in range(lcz__eoqh))
        lqdpv__nzlz = ('bodo.utils.utils.alloc_type(0, arr_type{}, ({}{}))'
            .format(i, tto__edee, ', ' if lcz__eoqh == 1 else ''))
        ytwz__vqhd.append(lqdpv__nzlz)
        pbqvp__bnf[f'arr_type{i}'] = arr_typ
    ytwz__vqhd = ', '.join(ytwz__vqhd)
    hljtn__idzh = 'def impl():\n'
    onquq__nasf = bodo.hiframes.dataframe_impl._gen_init_df(hljtn__idzh,
        toty.columns, ytwz__vqhd, index, pbqvp__bnf)
    df = context.compile_internal(builder, onquq__nasf, toty(), [])
    return df


def _cast_df_data_to_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame to table format')
    nurcu__ofw = toty.table_type
    cpzd__hqbkz = cgutils.create_struct_proxy(nurcu__ofw)(context, builder)
    cpzd__hqbkz.parent = in_dataframe_payload.parent
    for wqca__bqmko, dvon__xyjb in nurcu__ofw.type_to_blk.items():
        radr__sfuo = context.get_constant(types.int64, len(nurcu__ofw.
            block_to_arr_ind[dvon__xyjb]))
        gbry__iziu, eohx__ppmrm = ListInstance.allocate_ex(context, builder,
            types.List(wqca__bqmko), radr__sfuo)
        eohx__ppmrm.size = radr__sfuo
        setattr(cpzd__hqbkz, f'block_{dvon__xyjb}', eohx__ppmrm.value)
    for i, wqca__bqmko in enumerate(fromty.data):
        thig__fduk = toty.data[i]
        if wqca__bqmko != thig__fduk:
            wdkl__roj = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*wdkl__roj)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        bhnva__oul = builder.extract_value(in_dataframe_payload.data, i)
        if wqca__bqmko != thig__fduk:
            lomw__bhgu = context.cast(builder, bhnva__oul, wqca__bqmko,
                thig__fduk)
            mfnxc__iff = False
        else:
            lomw__bhgu = bhnva__oul
            mfnxc__iff = True
        dvon__xyjb = nurcu__ofw.type_to_blk[wqca__bqmko]
        qapf__uhaf = getattr(cpzd__hqbkz, f'block_{dvon__xyjb}')
        icsrj__kvrb = ListInstance(context, builder, types.List(wqca__bqmko
            ), qapf__uhaf)
        pzici__pig = context.get_constant(types.int64, nurcu__ofw.
            block_offsets[i])
        icsrj__kvrb.setitem(pzici__pig, lomw__bhgu, mfnxc__iff)
    data_tup = context.make_tuple(builder, types.Tuple([nurcu__ofw]), [
        cpzd__hqbkz._getvalue()])
    return data_tup


def _cast_df_data_keep_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame columns')
    tzq__ofh = []
    for i in range(len(fromty.data)):
        if fromty.data[i] != toty.data[i]:
            wdkl__roj = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*wdkl__roj)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
            bhnva__oul = builder.extract_value(in_dataframe_payload.data, i)
            lomw__bhgu = context.cast(builder, bhnva__oul, fromty.data[i],
                toty.data[i])
            mfnxc__iff = False
        else:
            lomw__bhgu = builder.extract_value(in_dataframe_payload.data, i)
            mfnxc__iff = True
        if mfnxc__iff:
            context.nrt.incref(builder, toty.data[i], lomw__bhgu)
        tzq__ofh.append(lomw__bhgu)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), tzq__ofh)
    return data_tup


def _cast_df_data_keep_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting table format DataFrame columns')
    fwsl__mviz = fromty.table_type
    pjy__mnqfs = cgutils.create_struct_proxy(fwsl__mviz)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    exo__kqwa = toty.table_type
    azmex__squ = cgutils.create_struct_proxy(exo__kqwa)(context, builder)
    azmex__squ.parent = in_dataframe_payload.parent
    for wqca__bqmko, dvon__xyjb in exo__kqwa.type_to_blk.items():
        radr__sfuo = context.get_constant(types.int64, len(exo__kqwa.
            block_to_arr_ind[dvon__xyjb]))
        gbry__iziu, eohx__ppmrm = ListInstance.allocate_ex(context, builder,
            types.List(wqca__bqmko), radr__sfuo)
        eohx__ppmrm.size = radr__sfuo
        setattr(azmex__squ, f'block_{dvon__xyjb}', eohx__ppmrm.value)
    for i in range(len(fromty.data)):
        ssoak__fglj = fromty.data[i]
        thig__fduk = toty.data[i]
        if ssoak__fglj != thig__fduk:
            wdkl__roj = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*wdkl__roj)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        wknsu__krjhf = fwsl__mviz.type_to_blk[ssoak__fglj]
        oixdf__ppuh = getattr(pjy__mnqfs, f'block_{wknsu__krjhf}')
        gykjo__nzv = ListInstance(context, builder, types.List(ssoak__fglj),
            oixdf__ppuh)
        lpzu__ppj = context.get_constant(types.int64, fwsl__mviz.
            block_offsets[i])
        bhnva__oul = gykjo__nzv.getitem(lpzu__ppj)
        if ssoak__fglj != thig__fduk:
            lomw__bhgu = context.cast(builder, bhnva__oul, ssoak__fglj,
                thig__fduk)
            mfnxc__iff = False
        else:
            lomw__bhgu = bhnva__oul
            mfnxc__iff = True
        ycnd__bit = exo__kqwa.type_to_blk[wqca__bqmko]
        eohx__ppmrm = getattr(azmex__squ, f'block_{ycnd__bit}')
        efpw__todp = ListInstance(context, builder, types.List(thig__fduk),
            eohx__ppmrm)
        gcyx__okmmy = context.get_constant(types.int64, exo__kqwa.
            block_offsets[i])
        efpw__todp.setitem(gcyx__okmmy, lomw__bhgu, mfnxc__iff)
    data_tup = context.make_tuple(builder, types.Tuple([exo__kqwa]), [
        azmex__squ._getvalue()])
    return data_tup


def _cast_df_data_to_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(fromty,
        'casting table format to traditional DataFrame')
    nurcu__ofw = fromty.table_type
    cpzd__hqbkz = cgutils.create_struct_proxy(nurcu__ofw)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    tzq__ofh = []
    for i, wqca__bqmko in enumerate(toty.data):
        ssoak__fglj = fromty.data[i]
        if wqca__bqmko != ssoak__fglj:
            wdkl__roj = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*wdkl__roj)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        dvon__xyjb = nurcu__ofw.type_to_blk[wqca__bqmko]
        qapf__uhaf = getattr(cpzd__hqbkz, f'block_{dvon__xyjb}')
        icsrj__kvrb = ListInstance(context, builder, types.List(wqca__bqmko
            ), qapf__uhaf)
        pzici__pig = context.get_constant(types.int64, nurcu__ofw.
            block_offsets[i])
        bhnva__oul = icsrj__kvrb.getitem(pzici__pig)
        if wqca__bqmko != ssoak__fglj:
            lomw__bhgu = context.cast(builder, bhnva__oul, ssoak__fglj,
                wqca__bqmko)
            mfnxc__iff = False
        else:
            lomw__bhgu = bhnva__oul
            mfnxc__iff = True
        if mfnxc__iff:
            context.nrt.incref(builder, wqca__bqmko, lomw__bhgu)
        tzq__ofh.append(lomw__bhgu)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), tzq__ofh)
    return data_tup


@overload(pd.DataFrame, inline='always', no_unliteral=True)
def pd_dataframe_overload(data=None, index=None, columns=None, dtype=None,
    copy=False):
    if not is_overload_constant_bool(copy):
        raise BodoError(
            "pd.DataFrame(): 'copy' argument should be a constant boolean")
    copy = get_overload_const(copy)
    uwr__vvclj, ytwz__vqhd, index_arg = _get_df_args(data, index, columns,
        dtype, copy)
    bydi__ptcn = gen_const_tup(uwr__vvclj)
    hljtn__idzh = (
        'def _init_df(data=None, index=None, columns=None, dtype=None, copy=False):\n'
        )
    hljtn__idzh += (
        '  return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, {}, {})\n'
        .format(ytwz__vqhd, index_arg, bydi__ptcn))
    qpcx__wxpnc = {}
    exec(hljtn__idzh, {'bodo': bodo, 'np': np}, qpcx__wxpnc)
    fxjd__rxfy = qpcx__wxpnc['_init_df']
    return fxjd__rxfy


@intrinsic
def _tuple_to_table_format_decoded(typingctx, df_typ):
    assert not df_typ.is_table_format, '_tuple_to_table_format requires a tuple format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    zlvi__znh = DataFrameType(to_str_arr_if_dict_array(df_typ.data), df_typ
        .index, df_typ.columns, dist=df_typ.dist, is_table_format=True)
    sig = signature(zlvi__znh, df_typ)
    return sig, codegen


@intrinsic
def _table_to_tuple_format_decoded(typingctx, df_typ):
    assert df_typ.is_table_format, '_tuple_to_table_format requires a table format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    zlvi__znh = DataFrameType(to_str_arr_if_dict_array(df_typ.data), df_typ
        .index, df_typ.columns, dist=df_typ.dist, is_table_format=False)
    sig = signature(zlvi__znh, df_typ)
    return sig, codegen


def _get_df_args(data, index, columns, dtype, copy):
    uky__ewls = ''
    if not is_overload_none(dtype):
        uky__ewls = '.astype(dtype)'
    index_is_none = is_overload_none(index)
    index_arg = 'bodo.utils.conversion.convert_to_index(index)'
    if isinstance(data, types.BaseTuple):
        if not data.types[0] == types.StringLiteral('__bodo_tup'):
            raise BodoError('pd.DataFrame tuple input data not supported yet')
        assert len(data.types) % 2 == 1, 'invalid const dict tuple structure'
        kuvr__ame = (len(data.types) - 1) // 2
        hjs__herxk = [wqca__bqmko.literal_value for wqca__bqmko in data.
            types[1:kuvr__ame + 1]]
        data_val_types = dict(zip(hjs__herxk, data.types[kuvr__ame + 1:]))
        tzq__ofh = ['data[{}]'.format(i) for i in range(kuvr__ame + 1, 2 *
            kuvr__ame + 1)]
        data_dict = dict(zip(hjs__herxk, tzq__ofh))
        if is_overload_none(index):
            for i, wqca__bqmko in enumerate(data.types[kuvr__ame + 1:]):
                if isinstance(wqca__bqmko, SeriesType):
                    index_arg = (
                        'bodo.hiframes.pd_series_ext.get_series_index(data[{}])'
                        .format(kuvr__ame + 1 + i))
                    index_is_none = False
                    break
    elif is_overload_none(data):
        data_dict = {}
        data_val_types = {}
    else:
        if not (isinstance(data, types.Array) and data.ndim == 2):
            raise BodoError(
                'pd.DataFrame() only supports constant dictionary and array input'
                )
        if is_overload_none(columns):
            raise BodoError(
                "pd.DataFrame() 'columns' argument is required when an array is passed as data"
                )
        wkrbt__vegq = '.copy()' if copy else ''
        zloch__tjwz = get_overload_const_list(columns)
        kuvr__ame = len(zloch__tjwz)
        data_val_types = {xeul__cris: data.copy(ndim=1) for xeul__cris in
            zloch__tjwz}
        tzq__ofh = ['data[:,{}]{}'.format(i, wkrbt__vegq) for i in range(
            kuvr__ame)]
        data_dict = dict(zip(zloch__tjwz, tzq__ofh))
    if is_overload_none(columns):
        col_names = data_dict.keys()
    else:
        col_names = get_overload_const_list(columns)
    df_len = _get_df_len_from_info(data_dict, data_val_types, col_names,
        index_is_none, index_arg)
    _fill_null_arrays(data_dict, col_names, df_len, dtype)
    if index_is_none:
        if is_overload_none(data):
            index_arg = (
                'bodo.hiframes.pd_index_ext.init_binary_str_index(bodo.libs.str_arr_ext.pre_alloc_string_array(0, 0))'
                )
        else:
            index_arg = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, {}, 1, None)'
                .format(df_len))
    ytwz__vqhd = '({},)'.format(', '.join(
        'bodo.utils.conversion.coerce_to_array({}, True, scalar_to_arr_len={}){}'
        .format(data_dict[xeul__cris], df_len, uky__ewls) for xeul__cris in
        col_names))
    if len(col_names) == 0:
        ytwz__vqhd = '()'
    return col_names, ytwz__vqhd, index_arg


def _get_df_len_from_info(data_dict, data_val_types, col_names,
    index_is_none, index_arg):
    df_len = '0'
    for xeul__cris in col_names:
        if xeul__cris in data_dict and is_iterable_type(data_val_types[
            xeul__cris]):
            df_len = 'len({})'.format(data_dict[xeul__cris])
            break
    if df_len == '0' and not index_is_none:
        df_len = f'len({index_arg})'
    return df_len


def _fill_null_arrays(data_dict, col_names, df_len, dtype):
    if all(xeul__cris in data_dict for xeul__cris in col_names):
        return
    if is_overload_none(dtype):
        dtype = 'bodo.string_array_type'
    else:
        dtype = 'bodo.utils.conversion.array_type_from_dtype(dtype)'
    nqawh__oxqg = 'bodo.libs.array_kernels.gen_na_array({}, {})'.format(df_len,
        dtype)
    for xeul__cris in col_names:
        if xeul__cris not in data_dict:
            data_dict[xeul__cris] = nqawh__oxqg


@infer_global(len)
class LenTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        if isinstance(args[0], (DataFrameType, bodo.TableType)):
            return types.int64(*args)


@lower_builtin(len, DataFrameType)
def table_len_lower(context, builder, sig, args):
    impl = df_len_overload(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def df_len_overload(df):
    if not isinstance(df, DataFrameType):
        return
    if df.has_runtime_cols:

        def impl(df):
            if is_null_pointer(df._meminfo):
                return 0
            wqca__bqmko = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df
                )
            return len(wqca__bqmko)
        return impl
    if len(df.columns) == 0:

        def impl(df):
            if is_null_pointer(df._meminfo):
                return 0
            return len(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
        return impl

    def impl(df):
        if is_null_pointer(df._meminfo):
            return 0
        return len(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, 0))
    return impl


@infer_global(operator.getitem)
class GetItemTuple(AbstractTemplate):
    key = operator.getitem

    def generic(self, args, kws):
        tup, idx = args
        if not isinstance(tup, types.BaseTuple) or not isinstance(idx,
            types.IntegerLiteral):
            return
        ahn__jdny = idx.literal_value
        if isinstance(ahn__jdny, int):
            zniy__svwf = tup.types[ahn__jdny]
        elif isinstance(ahn__jdny, slice):
            zniy__svwf = types.BaseTuple.from_types(tup.types[ahn__jdny])
        return signature(zniy__svwf, *args)


GetItemTuple.prefer_literal = True


@lower_builtin(operator.getitem, types.BaseTuple, types.IntegerLiteral)
@lower_builtin(operator.getitem, types.BaseTuple, types.SliceLiteral)
def getitem_tuple_lower(context, builder, sig, args):
    lpagz__qhgfq, idx = sig.args
    idx = idx.literal_value
    tup, gbry__iziu = args
    if isinstance(idx, int):
        if idx < 0:
            idx += len(lpagz__qhgfq)
        if not 0 <= idx < len(lpagz__qhgfq):
            raise IndexError('cannot index at %d in %s' % (idx, lpagz__qhgfq))
        noac__eyb = builder.extract_value(tup, idx)
    elif isinstance(idx, slice):
        ohzxj__sthl = cgutils.unpack_tuple(builder, tup)[idx]
        noac__eyb = context.make_tuple(builder, sig.return_type, ohzxj__sthl)
    else:
        raise NotImplementedError('unexpected index %r for %s' % (idx, sig.
            args[0]))
    return impl_ret_borrowed(context, builder, sig.return_type, noac__eyb)


def join_dummy(left_df, right_df, left_on, right_on, how, suffix_x,
    suffix_y, is_join, indicator, _bodo_na_equal, gen_cond):
    return left_df


@infer_global(join_dummy)
class JoinTyper(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        from bodo.utils.typing import is_overload_str
        assert not kws
        (left_df, right_df, left_on, right_on, lzffw__twe, suffix_x,
            suffix_y, is_join, indicator, _bodo_na_equal, ogh__ebh) = args
        left_on = get_overload_const_list(left_on)
        right_on = get_overload_const_list(right_on)
        qmwg__rdh = set(left_on) & set(right_on)
        qba__ypmth = set(left_df.columns) & set(right_df.columns)
        elbi__trgux = qba__ypmth - qmwg__rdh
        mijt__fpgrc = '$_bodo_index_' in left_on
        wfb__fbylw = '$_bodo_index_' in right_on
        how = get_overload_const_str(lzffw__twe)
        ixr__zjvh = how in {'left', 'outer'}
        cov__inlp = how in {'right', 'outer'}
        columns = []
        data = []
        if mijt__fpgrc:
            gcun__dwnz = bodo.utils.typing.get_index_data_arr_types(left_df
                .index)[0]
        else:
            gcun__dwnz = left_df.data[left_df.columns.index(left_on[0])]
        if wfb__fbylw:
            yjqzh__ehllo = bodo.utils.typing.get_index_data_arr_types(right_df
                .index)[0]
        else:
            yjqzh__ehllo = right_df.data[right_df.columns.index(right_on[0])]
        if mijt__fpgrc and not wfb__fbylw and not is_join.literal_value:
            gpoxr__trkbc = right_on[0]
            if gpoxr__trkbc in left_df.columns:
                columns.append(gpoxr__trkbc)
                if (yjqzh__ehllo == bodo.dict_str_arr_type and gcun__dwnz ==
                    bodo.string_array_type):
                    iebdk__zselt = bodo.string_array_type
                else:
                    iebdk__zselt = yjqzh__ehllo
                data.append(iebdk__zselt)
        if wfb__fbylw and not mijt__fpgrc and not is_join.literal_value:
            mmcj__clum = left_on[0]
            if mmcj__clum in right_df.columns:
                columns.append(mmcj__clum)
                if (gcun__dwnz == bodo.dict_str_arr_type and yjqzh__ehllo ==
                    bodo.string_array_type):
                    iebdk__zselt = bodo.string_array_type
                else:
                    iebdk__zselt = gcun__dwnz
                data.append(iebdk__zselt)
        for ssoak__fglj, zequ__mioy in zip(left_df.data, left_df.columns):
            columns.append(str(zequ__mioy) + suffix_x.literal_value if 
                zequ__mioy in elbi__trgux else zequ__mioy)
            if zequ__mioy in qmwg__rdh:
                if ssoak__fglj == bodo.dict_str_arr_type:
                    ssoak__fglj = right_df.data[right_df.columns.index(
                        zequ__mioy)]
                data.append(ssoak__fglj)
            else:
                if (ssoak__fglj == bodo.dict_str_arr_type and zequ__mioy in
                    left_on):
                    if wfb__fbylw:
                        ssoak__fglj = yjqzh__ehllo
                    else:
                        mvv__hkgee = left_on.index(zequ__mioy)
                        hja__fhjbt = right_on[mvv__hkgee]
                        ssoak__fglj = right_df.data[right_df.columns.index(
                            hja__fhjbt)]
                if cov__inlp:
                    ssoak__fglj = to_nullable_type(ssoak__fglj)
                data.append(ssoak__fglj)
        for ssoak__fglj, zequ__mioy in zip(right_df.data, right_df.columns):
            if zequ__mioy not in qmwg__rdh:
                columns.append(str(zequ__mioy) + suffix_y.literal_value if 
                    zequ__mioy in elbi__trgux else zequ__mioy)
                if (ssoak__fglj == bodo.dict_str_arr_type and zequ__mioy in
                    right_on):
                    if mijt__fpgrc:
                        ssoak__fglj = gcun__dwnz
                    else:
                        mvv__hkgee = right_on.index(zequ__mioy)
                        eehxp__wjrq = left_on[mvv__hkgee]
                        ssoak__fglj = left_df.data[left_df.columns.index(
                            eehxp__wjrq)]
                if ixr__zjvh:
                    ssoak__fglj = to_nullable_type(ssoak__fglj)
                data.append(ssoak__fglj)
        diz__fri = get_overload_const_bool(indicator)
        if diz__fri:
            columns.append('_merge')
            data.append(bodo.CategoricalArrayType(bodo.PDCategoricalDtype((
                'left_only', 'right_only', 'both'), bodo.string_type, False)))
        index_typ = RangeIndexType(types.none)
        if mijt__fpgrc and wfb__fbylw and not is_overload_str(how, 'asof'):
            index_typ = left_df.index
            if isinstance(index_typ, bodo.hiframes.pd_index_ext.RangeIndexType
                ):
                index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types
                    .int64)
        elif mijt__fpgrc and not wfb__fbylw:
            index_typ = right_df.index
            if isinstance(index_typ, bodo.hiframes.pd_index_ext.RangeIndexType
                ):
                index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types
                    .int64)
        elif wfb__fbylw and not mijt__fpgrc:
            index_typ = left_df.index
            if isinstance(index_typ, bodo.hiframes.pd_index_ext.RangeIndexType
                ):
                index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types
                    .int64)
        wno__mdbof = DataFrameType(tuple(data), index_typ, tuple(columns))
        return signature(wno__mdbof, *args)


JoinTyper._no_unliteral = True


@lower_builtin(join_dummy, types.VarArg(types.Any))
def lower_join_dummy(context, builder, sig, args):
    uyxy__lgm = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return uyxy__lgm._getvalue()


@overload(pd.concat, inline='always', no_unliteral=True)
def concat_overload(objs, axis=0, join='outer', join_axes=None,
    ignore_index=False, keys=None, levels=None, names=None,
    verify_integrity=False, sort=None, copy=True):
    if not is_overload_constant_int(axis):
        raise BodoError("pd.concat(): 'axis' should be a constant integer")
    if not is_overload_constant_bool(ignore_index):
        raise BodoError(
            "pd.concat(): 'ignore_index' should be a constant boolean")
    axis = get_overload_const_int(axis)
    ignore_index = is_overload_true(ignore_index)
    nbuk__punz = dict(join=join, join_axes=join_axes, keys=keys, levels=
        levels, names=names, verify_integrity=verify_integrity, sort=sort,
        copy=copy)
    guqnc__tsbd = dict(join='outer', join_axes=None, keys=None, levels=None,
        names=None, verify_integrity=False, sort=None, copy=True)
    check_unsupported_args('pandas.concat', nbuk__punz, guqnc__tsbd,
        package_name='pandas', module_name='General')
    hljtn__idzh = """def impl(objs, axis=0, join='outer', join_axes=None, ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False, sort=None, copy=True):
"""
    if axis == 1:
        if not isinstance(objs, types.BaseTuple):
            raise_bodo_error(
                'Only tuple argument for pd.concat(axis=1) expected')
        index = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len(objs[0]), 1, None)'
            )
        bgjyf__akr = 0
        ytwz__vqhd = []
        names = []
        for i, icyj__tvji in enumerate(objs.types):
            assert isinstance(icyj__tvji, (SeriesType, DataFrameType))
            check_runtime_cols_unsupported(icyj__tvji, 'pandas.concat()')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                icyj__tvji, 'pandas.concat()')
            if isinstance(icyj__tvji, SeriesType):
                names.append(str(bgjyf__akr))
                bgjyf__akr += 1
                ytwz__vqhd.append(
                    'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'
                    .format(i))
            else:
                names.extend(icyj__tvji.columns)
                for npak__finid in range(len(icyj__tvji.data)):
                    ytwz__vqhd.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, npak__finid))
        return bodo.hiframes.dataframe_impl._gen_init_df(hljtn__idzh, names,
            ', '.join(ytwz__vqhd), index)
    if axis != 0:
        raise_bodo_error('pd.concat(): axis must be 0 or 1')
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        DataFrameType):
        assert all(isinstance(wqca__bqmko, DataFrameType) for wqca__bqmko in
            objs.types)
        mdmd__piesw = []
        for df in objs.types:
            check_runtime_cols_unsupported(df, 'pandas.concat()')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
                'pandas.concat()')
            mdmd__piesw.extend(df.columns)
        mdmd__piesw = list(dict.fromkeys(mdmd__piesw).keys())
        xcrpb__lwxx = {}
        for bgjyf__akr, xeul__cris in enumerate(mdmd__piesw):
            for i, df in enumerate(objs.types):
                if xeul__cris in df.column_index:
                    xcrpb__lwxx[f'arr_typ{bgjyf__akr}'] = df.data[df.
                        column_index[xeul__cris]]
                    break
        assert len(xcrpb__lwxx) == len(mdmd__piesw)
        qmgms__lad = []
        for bgjyf__akr, xeul__cris in enumerate(mdmd__piesw):
            args = []
            for i, df in enumerate(objs.types):
                if xeul__cris in df.column_index:
                    lisq__stkt = df.column_index[xeul__cris]
                    args.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, lisq__stkt))
                else:
                    args.append(
                        'bodo.libs.array_kernels.gen_na_array(len(objs[{}]), arr_typ{})'
                        .format(i, bgjyf__akr))
            hljtn__idzh += ('  A{} = bodo.libs.array_kernels.concat(({},))\n'
                .format(bgjyf__akr, ', '.join(args)))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(A0), 1, None)'
                )
        else:
            index = (
                """bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)) if len(objs[i].
                columns) > 0)))
        return bodo.hiframes.dataframe_impl._gen_init_df(hljtn__idzh,
            mdmd__piesw, ', '.join('A{}'.format(i) for i in range(len(
            mdmd__piesw))), index, xcrpb__lwxx)
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        SeriesType):
        assert all(isinstance(wqca__bqmko, SeriesType) for wqca__bqmko in
            objs.types)
        hljtn__idzh += ('  out_arr = bodo.libs.array_kernels.concat(({},))\n'
            .format(', '.join(
            'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'.format(
            i) for i in range(len(objs.types)))))
        if ignore_index:
            hljtn__idzh += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            hljtn__idzh += (
                """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)))))
        hljtn__idzh += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        qpcx__wxpnc = {}
        exec(hljtn__idzh, {'bodo': bodo, 'np': np, 'numba': numba}, qpcx__wxpnc
            )
        return qpcx__wxpnc['impl']
    if isinstance(objs, types.List) and isinstance(objs.dtype, DataFrameType):
        check_runtime_cols_unsupported(objs.dtype, 'pandas.concat()')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(objs.
            dtype, 'pandas.concat()')
        df_type = objs.dtype
        for bgjyf__akr, xeul__cris in enumerate(df_type.columns):
            hljtn__idzh += '  arrs{} = []\n'.format(bgjyf__akr)
            hljtn__idzh += '  for i in range(len(objs)):\n'
            hljtn__idzh += '    df = objs[i]\n'
            hljtn__idzh += (
                """    arrs{0}.append(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0}))
"""
                .format(bgjyf__akr))
            hljtn__idzh += (
                '  out_arr{0} = bodo.libs.array_kernels.concat(arrs{0})\n'.
                format(bgjyf__akr))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr0), 1, None)'
                )
        else:
            hljtn__idzh += '  arrs_index = []\n'
            hljtn__idzh += '  for i in range(len(objs)):\n'
            hljtn__idzh += '    df = objs[i]\n'
            hljtn__idzh += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
            if objs.dtype.index.name_typ == types.none:
                name = None
            else:
                name = objs.dtype.index.name_typ.literal_value
            index = f"""bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index), {name!r})
"""
        return bodo.hiframes.dataframe_impl._gen_init_df(hljtn__idzh,
            df_type.columns, ', '.join('out_arr{}'.format(i) for i in range
            (len(df_type.columns))), index)
    if isinstance(objs, types.List) and isinstance(objs.dtype, SeriesType):
        hljtn__idzh += '  arrs = []\n'
        hljtn__idzh += '  for i in range(len(objs)):\n'
        hljtn__idzh += (
            '    arrs.append(bodo.hiframes.pd_series_ext.get_series_data(objs[i]))\n'
            )
        hljtn__idzh += '  out_arr = bodo.libs.array_kernels.concat(arrs)\n'
        if ignore_index:
            hljtn__idzh += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            hljtn__idzh += '  arrs_index = []\n'
            hljtn__idzh += '  for i in range(len(objs)):\n'
            hljtn__idzh += '    S = objs[i]\n'
            hljtn__idzh += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(S)))
"""
            hljtn__idzh += """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index))
"""
        hljtn__idzh += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        qpcx__wxpnc = {}
        exec(hljtn__idzh, {'bodo': bodo, 'np': np, 'numba': numba}, qpcx__wxpnc
            )
        return qpcx__wxpnc['impl']
    raise BodoError('pd.concat(): input type {} not supported yet'.format(objs)
        )


def sort_values_dummy(df, by, ascending, inplace, na_position):
    return df.sort_values(by, ascending=ascending, inplace=inplace,
        na_position=na_position)


@infer_global(sort_values_dummy)
class SortDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        df, by, ascending, inplace, na_position = args
        index = df.index
        if isinstance(index, bodo.hiframes.pd_index_ext.RangeIndexType):
            index = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64)
        zlvi__znh = df.copy(index=index, is_table_format=False)
        return signature(zlvi__znh, *args)


SortDummyTyper._no_unliteral = True


@lower_builtin(sort_values_dummy, types.VarArg(types.Any))
def lower_sort_values_dummy(context, builder, sig, args):
    if sig.return_type == types.none:
        return
    disl__wjghh = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return disl__wjghh._getvalue()


@overload_method(DataFrameType, 'itertuples', inline='always', no_unliteral
    =True)
def itertuples_overload(df, index=True, name='Pandas'):
    check_runtime_cols_unsupported(df, 'DataFrame.itertuples()')
    nbuk__punz = dict(index=index, name=name)
    guqnc__tsbd = dict(index=True, name='Pandas')
    check_unsupported_args('DataFrame.itertuples', nbuk__punz, guqnc__tsbd,
        package_name='pandas', module_name='DataFrame')

    def _impl(df, index=True, name='Pandas'):
        return bodo.hiframes.pd_dataframe_ext.itertuples_dummy(df)
    return _impl


def itertuples_dummy(df):
    return df


@infer_global(itertuples_dummy)
class ItertuplesDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        df, = args
        assert 'Index' not in df.columns
        columns = ('Index',) + df.columns
        xcrpb__lwxx = (types.Array(types.int64, 1, 'C'),) + df.data
        ypqn__opv = bodo.hiframes.dataframe_impl.DataFrameTupleIterator(columns
            , xcrpb__lwxx)
        return signature(ypqn__opv, *args)


@lower_builtin(itertuples_dummy, types.VarArg(types.Any))
def lower_itertuples_dummy(context, builder, sig, args):
    disl__wjghh = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return disl__wjghh._getvalue()


def query_dummy(df, expr):
    return df.eval(expr)


@infer_global(query_dummy)
class QueryDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(SeriesType(types.bool_, index=RangeIndexType(types
            .none)), *args)


@lower_builtin(query_dummy, types.VarArg(types.Any))
def lower_query_dummy(context, builder, sig, args):
    disl__wjghh = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return disl__wjghh._getvalue()


def val_isin_dummy(S, vals):
    return S in vals


def val_notin_dummy(S, vals):
    return S not in vals


@infer_global(val_isin_dummy)
@infer_global(val_notin_dummy)
class ValIsinTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(SeriesType(types.bool_, index=args[0].index), *args)


@lower_builtin(val_isin_dummy, types.VarArg(types.Any))
@lower_builtin(val_notin_dummy, types.VarArg(types.Any))
def lower_val_isin_dummy(context, builder, sig, args):
    disl__wjghh = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return disl__wjghh._getvalue()


@numba.generated_jit(nopython=True)
def pivot_impl(index_tup, columns_tup, values_tup, pivot_values,
    index_names, columns_name, value_names, check_duplicates=True, parallel
    =False):
    if not is_overload_constant_bool(check_duplicates):
        raise BodoError(
            'pivot_impl(): check_duplicates must be a constant boolean')
    lowcr__kwfa = get_overload_const_bool(check_duplicates)
    myyjd__cayu = not is_overload_none(value_names)
    mhr__xfvnv = isinstance(values_tup, types.UniTuple)
    if mhr__xfvnv:
        fgp__jfx = [to_nullable_type(values_tup.dtype)]
    else:
        fgp__jfx = [to_nullable_type(ofy__mpq) for ofy__mpq in values_tup]
    hljtn__idzh = 'def impl(\n'
    hljtn__idzh += """    index_tup, columns_tup, values_tup, pivot_values, index_names, columns_name, value_names, check_duplicates=True, parallel=False
"""
    hljtn__idzh += '):\n'
    hljtn__idzh += '    if parallel:\n'
    rtwef__rrx = ', '.join([f'array_to_info(index_tup[{i}])' for i in range
        (len(index_tup))] + [f'array_to_info(columns_tup[{i}])' for i in
        range(len(columns_tup))] + [f'array_to_info(values_tup[{i}])' for i in
        range(len(values_tup))])
    hljtn__idzh += f'        info_list = [{rtwef__rrx}]\n'
    hljtn__idzh += '        cpp_table = arr_info_list_to_table(info_list)\n'
    hljtn__idzh += f"""        out_cpp_table = shuffle_table(cpp_table, {len(index_tup)}, parallel, 0)
"""
    jtd__qfdbd = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i}), index_tup[{i}])'
         for i in range(len(index_tup))])
    qfa__hnwfk = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup)}), columns_tup[{i}])'
         for i in range(len(columns_tup))])
    ctpa__jqcq = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup) + len(columns_tup)}), values_tup[{i}])'
         for i in range(len(values_tup))])
    hljtn__idzh += f'        index_tup = ({jtd__qfdbd},)\n'
    hljtn__idzh += f'        columns_tup = ({qfa__hnwfk},)\n'
    hljtn__idzh += f'        values_tup = ({ctpa__jqcq},)\n'
    hljtn__idzh += '        delete_table(cpp_table)\n'
    hljtn__idzh += '        delete_table(out_cpp_table)\n'
    hljtn__idzh += '    columns_arr = columns_tup[0]\n'
    if mhr__xfvnv:
        hljtn__idzh += '    values_arrs = [arr for arr in values_tup]\n'
    hljtn__idzh += """    unique_index_arr_tup, row_vector = bodo.libs.array_ops.array_unique_vector_map(
"""
    hljtn__idzh += '        index_tup\n'
    hljtn__idzh += '    )\n'
    hljtn__idzh += '    n_rows = len(unique_index_arr_tup[0])\n'
    hljtn__idzh += '    num_values_arrays = len(values_tup)\n'
    hljtn__idzh += '    n_unique_pivots = len(pivot_values)\n'
    if mhr__xfvnv:
        hljtn__idzh += '    n_cols = num_values_arrays * n_unique_pivots\n'
    else:
        hljtn__idzh += '    n_cols = n_unique_pivots\n'
    hljtn__idzh += '    col_map = {}\n'
    hljtn__idzh += '    for i in range(n_unique_pivots):\n'
    hljtn__idzh += (
        '        if bodo.libs.array_kernels.isna(pivot_values, i):\n')
    hljtn__idzh += '            raise ValueError(\n'
    hljtn__idzh += """                "DataFrame.pivot(): NA values in 'columns' array not supported\"
"""
    hljtn__idzh += '            )\n'
    hljtn__idzh += '        col_map[pivot_values[i]] = i\n'
    vqyd__wlxgw = False
    for i, wcfs__sit in enumerate(fgp__jfx):
        if is_str_arr_type(wcfs__sit):
            vqyd__wlxgw = True
            hljtn__idzh += f"""    len_arrs_{i} = [np.zeros(n_rows, np.int64) for _ in range(n_cols)]
"""
            hljtn__idzh += f'    total_lens_{i} = np.zeros(n_cols, np.int64)\n'
    if vqyd__wlxgw:
        if lowcr__kwfa:
            hljtn__idzh += '    nbytes = (n_rows + 7) >> 3\n'
            hljtn__idzh += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
        hljtn__idzh += '    for i in range(len(columns_arr)):\n'
        hljtn__idzh += '        col_name = columns_arr[i]\n'
        hljtn__idzh += '        pivot_idx = col_map[col_name]\n'
        hljtn__idzh += '        row_idx = row_vector[i]\n'
        if lowcr__kwfa:
            hljtn__idzh += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
            hljtn__idzh += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
            hljtn__idzh += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
            hljtn__idzh += '        else:\n'
            hljtn__idzh += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
        if mhr__xfvnv:
            hljtn__idzh += '        for j in range(num_values_arrays):\n'
            hljtn__idzh += (
                '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
            hljtn__idzh += '            len_arr = len_arrs_0[col_idx]\n'
            hljtn__idzh += '            values_arr = values_arrs[j]\n'
            hljtn__idzh += (
                '            if not bodo.libs.array_kernels.isna(values_arr, i):\n'
                )
            hljtn__idzh += (
                '                len_arr[row_idx] = len(values_arr[i])\n')
            hljtn__idzh += (
                '                total_lens_0[col_idx] += len(values_arr[i])\n'
                )
        else:
            for i, wcfs__sit in enumerate(fgp__jfx):
                if is_str_arr_type(wcfs__sit):
                    hljtn__idzh += f"""        if not bodo.libs.array_kernels.isna(values_tup[{i}], i):
"""
                    hljtn__idzh += f"""            len_arrs_{i}[pivot_idx][row_idx] = len(values_tup[{i}][i])
"""
                    hljtn__idzh += f"""            total_lens_{i}[pivot_idx] += len(values_tup[{i}][i])
"""
    for i, wcfs__sit in enumerate(fgp__jfx):
        if is_str_arr_type(wcfs__sit):
            hljtn__idzh += f'    data_arrs_{i} = [\n'
            hljtn__idzh += (
                '        bodo.libs.str_arr_ext.gen_na_str_array_lens(\n')
            hljtn__idzh += (
                f'            n_rows, total_lens_{i}[i], len_arrs_{i}[i]\n')
            hljtn__idzh += '        )\n'
            hljtn__idzh += '        for i in range(n_cols)\n'
            hljtn__idzh += '    ]\n'
        else:
            hljtn__idzh += f'    data_arrs_{i} = [\n'
            hljtn__idzh += f"""        bodo.libs.array_kernels.gen_na_array(n_rows, data_arr_typ_{i})
"""
            hljtn__idzh += '        for _ in range(n_cols)\n'
            hljtn__idzh += '    ]\n'
    if not vqyd__wlxgw and lowcr__kwfa:
        hljtn__idzh += '    nbytes = (n_rows + 7) >> 3\n'
        hljtn__idzh += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
    hljtn__idzh += '    for i in range(len(columns_arr)):\n'
    hljtn__idzh += '        col_name = columns_arr[i]\n'
    hljtn__idzh += '        pivot_idx = col_map[col_name]\n'
    hljtn__idzh += '        row_idx = row_vector[i]\n'
    if not vqyd__wlxgw and lowcr__kwfa:
        hljtn__idzh += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
        hljtn__idzh += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
        hljtn__idzh += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
        hljtn__idzh += '        else:\n'
        hljtn__idzh += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
    if mhr__xfvnv:
        hljtn__idzh += '        for j in range(num_values_arrays):\n'
        hljtn__idzh += (
            '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
        hljtn__idzh += '            col_arr = data_arrs_0[col_idx]\n'
        hljtn__idzh += '            values_arr = values_arrs[j]\n'
        hljtn__idzh += (
            '            if bodo.libs.array_kernels.isna(values_arr, i):\n')
        hljtn__idzh += (
            '                bodo.libs.array_kernels.setna(col_arr, row_idx)\n'
            )
        hljtn__idzh += '            else:\n'
        hljtn__idzh += '                col_arr[row_idx] = values_arr[i]\n'
    else:
        for i, wcfs__sit in enumerate(fgp__jfx):
            hljtn__idzh += f'        col_arr_{i} = data_arrs_{i}[pivot_idx]\n'
            hljtn__idzh += (
                f'        if bodo.libs.array_kernels.isna(values_tup[{i}], i):\n'
                )
            hljtn__idzh += (
                f'            bodo.libs.array_kernels.setna(col_arr_{i}, row_idx)\n'
                )
            hljtn__idzh += f'        else:\n'
            hljtn__idzh += (
                f'            col_arr_{i}[row_idx] = values_tup[{i}][i]\n')
    if len(index_tup) == 1:
        hljtn__idzh += """    index = bodo.utils.conversion.index_from_array(unique_index_arr_tup[0], index_names[0])
"""
    else:
        hljtn__idzh += """    index = bodo.hiframes.pd_multi_index_ext.init_multi_index(unique_index_arr_tup, index_names, None)
"""
    if myyjd__cayu:
        hljtn__idzh += '    num_rows = len(value_names) * len(pivot_values)\n'
        if is_str_arr_type(value_names):
            hljtn__idzh += '    total_chars = 0\n'
            hljtn__idzh += '    for i in range(len(value_names)):\n'
            hljtn__idzh += '        total_chars += len(value_names[i])\n'
            hljtn__idzh += """    new_value_names = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(pivot_values))
"""
        else:
            hljtn__idzh += """    new_value_names = bodo.utils.utils.alloc_type(num_rows, value_names, (-1,))
"""
        if is_str_arr_type(pivot_values):
            hljtn__idzh += '    total_chars = 0\n'
            hljtn__idzh += '    for i in range(len(pivot_values)):\n'
            hljtn__idzh += '        total_chars += len(pivot_values[i])\n'
            hljtn__idzh += """    new_pivot_values = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(value_names))
"""
        else:
            hljtn__idzh += """    new_pivot_values = bodo.utils.utils.alloc_type(num_rows, pivot_values, (-1,))
"""
        hljtn__idzh += '    for i in range(len(value_names)):\n'
        hljtn__idzh += '        for j in range(len(pivot_values)):\n'
        hljtn__idzh += """            new_value_names[(i * len(pivot_values)) + j] = value_names[i]
"""
        hljtn__idzh += """            new_pivot_values[(i * len(pivot_values)) + j] = pivot_values[j]
"""
        hljtn__idzh += """    column_index = bodo.hiframes.pd_multi_index_ext.init_multi_index((new_value_names, new_pivot_values), (None, columns_name), None)
"""
    else:
        hljtn__idzh += """    column_index =  bodo.utils.conversion.index_from_array(pivot_values, columns_name)
"""
    rcin__rxlbq = ', '.join(f'data_arrs_{i}' for i in range(len(fgp__jfx)))
    hljtn__idzh += f"""    table = bodo.hiframes.table.init_runtime_table_from_lists(({rcin__rxlbq},), n_rows)
"""
    hljtn__idzh += (
        '    return bodo.hiframes.pd_dataframe_ext.init_runtime_cols_dataframe(\n'
        )
    hljtn__idzh += '        (table,), index, column_index\n'
    hljtn__idzh += '    )\n'
    qpcx__wxpnc = {}
    udwl__ngpf = {f'data_arr_typ_{i}': wcfs__sit for i, wcfs__sit in
        enumerate(fgp__jfx)}
    vkjh__fdyw = {'bodo': bodo, 'np': np, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'info_from_table': info_from_table, **udwl__ngpf}
    exec(hljtn__idzh, vkjh__fdyw, qpcx__wxpnc)
    impl = qpcx__wxpnc['impl']
    return impl


def gen_pandas_parquet_metadata(column_names, data_types, index,
    write_non_range_index_to_metadata, write_rangeindex_to_metadata,
    partition_cols=None, is_runtime_columns=False):
    ahav__qdwno = {}
    ahav__qdwno['columns'] = []
    if partition_cols is None:
        partition_cols = []
    for col_name, uti__xgske in zip(column_names, data_types):
        if col_name in partition_cols:
            continue
        uyr__qeg = None
        if isinstance(uti__xgske, bodo.DatetimeArrayType):
            itfvi__nyvo = 'datetimetz'
            gex__kguqx = 'datetime64[ns]'
            if isinstance(uti__xgske.tz, int):
                jbsx__mekzi = (bodo.libs.pd_datetime_arr_ext.
                    nanoseconds_to_offset(uti__xgske.tz))
            else:
                jbsx__mekzi = pd.DatetimeTZDtype(tz=uti__xgske.tz).tz
            uyr__qeg = {'timezone': pa.lib.tzinfo_to_string(jbsx__mekzi)}
        elif isinstance(uti__xgske, types.Array
            ) or uti__xgske == boolean_array:
            itfvi__nyvo = gex__kguqx = uti__xgske.dtype.name
            if gex__kguqx.startswith('datetime'):
                itfvi__nyvo = 'datetime'
        elif is_str_arr_type(uti__xgske):
            itfvi__nyvo = 'unicode'
            gex__kguqx = 'object'
        elif uti__xgske == binary_array_type:
            itfvi__nyvo = 'bytes'
            gex__kguqx = 'object'
        elif isinstance(uti__xgske, DecimalArrayType):
            itfvi__nyvo = gex__kguqx = 'object'
        elif isinstance(uti__xgske, IntegerArrayType):
            bbdax__bjp = uti__xgske.dtype.name
            if bbdax__bjp.startswith('int'):
                itfvi__nyvo = 'Int' + bbdax__bjp[3:]
            elif bbdax__bjp.startswith('uint'):
                itfvi__nyvo = 'UInt' + bbdax__bjp[4:]
            else:
                if is_runtime_columns:
                    col_name = 'Runtime determined column of type'
                raise BodoError(
                    'to_parquet(): unknown dtype in nullable Integer column {} {}'
                    .format(col_name, uti__xgske))
            gex__kguqx = uti__xgske.dtype.name
        elif uti__xgske == datetime_date_array_type:
            itfvi__nyvo = 'datetime'
            gex__kguqx = 'object'
        elif isinstance(uti__xgske, (StructArrayType, ArrayItemArrayType)):
            itfvi__nyvo = 'object'
            gex__kguqx = 'object'
        else:
            if is_runtime_columns:
                col_name = 'Runtime determined column of type'
            raise BodoError(
                'to_parquet(): unsupported column type for metadata generation : {} {}'
                .format(col_name, uti__xgske))
        ddlw__knf = {'name': col_name, 'field_name': col_name,
            'pandas_type': itfvi__nyvo, 'numpy_type': gex__kguqx,
            'metadata': uyr__qeg}
        ahav__qdwno['columns'].append(ddlw__knf)
    if write_non_range_index_to_metadata:
        if isinstance(index, MultiIndexType):
            raise BodoError('to_parquet: MultiIndex not supported yet')
        if 'none' in index.name:
            hexyn__oxnf = '__index_level_0__'
            nxe__xgfek = None
        else:
            hexyn__oxnf = '%s'
            nxe__xgfek = '%s'
        ahav__qdwno['index_columns'] = [hexyn__oxnf]
        ahav__qdwno['columns'].append({'name': nxe__xgfek, 'field_name':
            hexyn__oxnf, 'pandas_type': index.pandas_type_name,
            'numpy_type': index.numpy_type_name, 'metadata': None})
    elif write_rangeindex_to_metadata:
        ahav__qdwno['index_columns'] = [{'kind': 'range', 'name': '%s',
            'start': '%d', 'stop': '%d', 'step': '%d'}]
    else:
        ahav__qdwno['index_columns'] = []
    ahav__qdwno['pandas_version'] = pd.__version__
    return ahav__qdwno


@overload_method(DataFrameType, 'to_parquet', no_unliteral=True)
def to_parquet_overload(df, path, engine='auto', compression='snappy',
    index=None, partition_cols=None, storage_options=None, row_group_size=-
    1, _is_parallel=False):
    check_unsupported_args('DataFrame.to_parquet', {'storage_options':
        storage_options}, {'storage_options': None}, package_name='pandas',
        module_name='IO')
    if df.has_runtime_cols and not is_overload_none(partition_cols):
        raise BodoError(
            f"DataFrame.to_parquet(): Providing 'partition_cols' on DataFrames with columns determined at runtime is not yet supported. Please return the DataFrame to regular Python to update typing information."
            )
    if not is_overload_none(engine) and get_overload_const_str(engine) not in (
        'auto', 'pyarrow'):
        raise BodoError('DataFrame.to_parquet(): only pyarrow engine supported'
            )
    if not is_overload_none(compression) and get_overload_const_str(compression
        ) not in {'snappy', 'gzip', 'brotli'}:
        raise BodoError('to_parquet(): Unsupported compression: ' + str(
            get_overload_const_str(compression)))
    if not is_overload_none(partition_cols):
        partition_cols = get_overload_const_list(partition_cols)
        qgci__lob = []
        for pax__css in partition_cols:
            try:
                idx = df.columns.index(pax__css)
            except ValueError as xrpqk__cuhvj:
                raise BodoError(
                    f'Partition column {pax__css} is not in dataframe')
            qgci__lob.append(idx)
    else:
        partition_cols = None
    if not is_overload_none(index) and not is_overload_constant_bool(index):
        raise BodoError('to_parquet(): index must be a constant bool or None')
    if not is_overload_int(row_group_size):
        raise BodoError('to_parquet(): row_group_size must be integer')
    from bodo.io.parquet_pio import parquet_write_table_cpp, parquet_write_table_partitioned_cpp
    kyy__nrq = isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType)
    gvbr__xnw = df.index is not None and (is_overload_true(_is_parallel) or
        not is_overload_true(_is_parallel) and not kyy__nrq)
    write_non_range_index_to_metadata = is_overload_true(index
        ) or is_overload_none(index) and (not kyy__nrq or is_overload_true(
        _is_parallel))
    write_rangeindex_to_metadata = is_overload_none(index
        ) and kyy__nrq and not is_overload_true(_is_parallel)
    if df.has_runtime_cols:
        if isinstance(df.runtime_colname_typ, MultiIndexType):
            raise BodoError(
                'DataFrame.to_parquet(): Not supported with MultiIndex runtime column names. Please return the DataFrame to regular Python to update typing information.'
                )
        if not isinstance(df.runtime_colname_typ, bodo.hiframes.
            pd_index_ext.StringIndexType):
            raise BodoError(
                'DataFrame.to_parquet(): parquet must have string column names. Please return the DataFrame with runtime column names to regular Python to modify column names.'
                )
        lwavn__tebkk = df.runtime_data_types
        uqcs__xapm = len(lwavn__tebkk)
        uyr__qeg = gen_pandas_parquet_metadata([''] * uqcs__xapm,
            lwavn__tebkk, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=True)
        kbbrf__qgjg = uyr__qeg['columns'][:uqcs__xapm]
        uyr__qeg['columns'] = uyr__qeg['columns'][uqcs__xapm:]
        kbbrf__qgjg = [json.dumps(abhge__kjkob).replace('""', '{0}') for
            abhge__kjkob in kbbrf__qgjg]
        xxs__odc = json.dumps(uyr__qeg)
        wmfqr__mphry = '"columns": ['
        jtf__sdd = xxs__odc.find(wmfqr__mphry)
        if jtf__sdd == -1:
            raise BodoError(
                'DataFrame.to_parquet(): Unexpected metadata string for runtime columns.  Please return the DataFrame to regular Python to update typing information.'
                )
        rkc__rji = jtf__sdd + len(wmfqr__mphry)
        jjj__izx = xxs__odc[:rkc__rji]
        xxs__odc = xxs__odc[rkc__rji:]
        clhsc__qmb = len(uyr__qeg['columns'])
    else:
        xxs__odc = json.dumps(gen_pandas_parquet_metadata(df.columns, df.
            data, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=False))
    if not is_overload_true(_is_parallel) and kyy__nrq:
        xxs__odc = xxs__odc.replace('"%d"', '%d')
        if df.index.name == 'RangeIndexType(none)':
            xxs__odc = xxs__odc.replace('"%s"', '%s')
    if not df.is_table_format:
        ytwz__vqhd = ', '.join(
            'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
            .format(i) for i in range(len(df.columns)))
    hljtn__idzh = """def df_to_parquet(df, path, engine='auto', compression='snappy', index=None, partition_cols=None, storage_options=None, row_group_size=-1, _is_parallel=False):
"""
    if df.is_table_format:
        hljtn__idzh += '    py_table = get_dataframe_table(df)\n'
        hljtn__idzh += (
            '    table = py_table_to_cpp_table(py_table, py_table_typ)\n')
    else:
        hljtn__idzh += '    info_list = [{}]\n'.format(ytwz__vqhd)
        hljtn__idzh += '    table = arr_info_list_to_table(info_list)\n'
    if df.has_runtime_cols:
        hljtn__idzh += '    columns_index = get_dataframe_column_names(df)\n'
        hljtn__idzh += '    names_arr = index_to_array(columns_index)\n'
        hljtn__idzh += '    col_names = array_to_info(names_arr)\n'
    else:
        hljtn__idzh += '    col_names = array_to_info(col_names_arr)\n'
    if is_overload_true(index) or is_overload_none(index) and gvbr__xnw:
        hljtn__idzh += """    index_col = array_to_info(index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
        kdcs__engm = True
    else:
        hljtn__idzh += '    index_col = array_to_info(np.empty(0))\n'
        kdcs__engm = False
    if df.has_runtime_cols:
        hljtn__idzh += '    columns_lst = []\n'
        hljtn__idzh += '    num_cols = 0\n'
        for i in range(len(df.runtime_data_types)):
            hljtn__idzh += f'    for _ in range(len(py_table.block_{i})):\n'
            hljtn__idzh += f"""        columns_lst.append({kbbrf__qgjg[i]!r}.replace('{{0}}', '"' + names_arr[num_cols] + '"'))
"""
            hljtn__idzh += '        num_cols += 1\n'
        if clhsc__qmb:
            hljtn__idzh += "    columns_lst.append('')\n"
        hljtn__idzh += '    columns_str = ", ".join(columns_lst)\n'
        hljtn__idzh += ('    metadata = """' + jjj__izx +
            '""" + columns_str + """' + xxs__odc + '"""\n')
    else:
        hljtn__idzh += '    metadata = """' + xxs__odc + '"""\n'
    hljtn__idzh += '    if compression is None:\n'
    hljtn__idzh += "        compression = 'none'\n"
    hljtn__idzh += '    if df.index.name is not None:\n'
    hljtn__idzh += '        name_ptr = df.index.name\n'
    hljtn__idzh += '    else:\n'
    hljtn__idzh += "        name_ptr = 'null'\n"
    hljtn__idzh += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(path, parallel=_is_parallel)
"""
    sjavp__ften = None
    if partition_cols:
        sjavp__ften = pd.array([col_name for col_name in df.columns if 
            col_name not in partition_cols])
        xatp__rvgv = ', '.join(
            f'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype.categories.values)'
             for i in range(len(df.columns)) if isinstance(df.data[i],
            CategoricalArrayType) and i in qgci__lob)
        if xatp__rvgv:
            hljtn__idzh += '    cat_info_list = [{}]\n'.format(xatp__rvgv)
            hljtn__idzh += (
                '    cat_table = arr_info_list_to_table(cat_info_list)\n')
        else:
            hljtn__idzh += '    cat_table = table\n'
        hljtn__idzh += (
            '    col_names_no_partitions = array_to_info(col_names_no_parts_arr)\n'
            )
        hljtn__idzh += (
            f'    part_cols_idxs = np.array({qgci__lob}, dtype=np.int32)\n')
        hljtn__idzh += (
            '    parquet_write_table_partitioned_cpp(unicode_to_utf8(path),\n')
        hljtn__idzh += """                            table, col_names, col_names_no_partitions, cat_table,
"""
        hljtn__idzh += (
            '                            part_cols_idxs.ctypes, len(part_cols_idxs),\n'
            )
        hljtn__idzh += (
            '                            unicode_to_utf8(compression),\n')
        hljtn__idzh += '                            _is_parallel,\n'
        hljtn__idzh += (
            '                            unicode_to_utf8(bucket_region),\n')
        hljtn__idzh += '                            row_group_size)\n'
        hljtn__idzh += '    delete_table_decref_arrays(table)\n'
        hljtn__idzh += '    delete_info_decref_array(index_col)\n'
        hljtn__idzh += (
            '    delete_info_decref_array(col_names_no_partitions)\n')
        hljtn__idzh += '    delete_info_decref_array(col_names)\n'
        if xatp__rvgv:
            hljtn__idzh += '    delete_table_decref_arrays(cat_table)\n'
    elif write_rangeindex_to_metadata:
        hljtn__idzh += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        hljtn__idzh += (
            '                            table, col_names, index_col,\n')
        hljtn__idzh += '                            ' + str(kdcs__engm) + ',\n'
        hljtn__idzh += (
            '                            unicode_to_utf8(metadata),\n')
        hljtn__idzh += (
            '                            unicode_to_utf8(compression),\n')
        hljtn__idzh += (
            '                            _is_parallel, 1, df.index.start,\n')
        hljtn__idzh += (
            '                            df.index.stop, df.index.step,\n')
        hljtn__idzh += (
            '                            unicode_to_utf8(name_ptr),\n')
        hljtn__idzh += (
            '                            unicode_to_utf8(bucket_region),\n')
        hljtn__idzh += '                            row_group_size)\n'
        hljtn__idzh += '    delete_table_decref_arrays(table)\n'
        hljtn__idzh += '    delete_info_decref_array(index_col)\n'
        hljtn__idzh += '    delete_info_decref_array(col_names)\n'
    else:
        hljtn__idzh += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        hljtn__idzh += (
            '                            table, col_names, index_col,\n')
        hljtn__idzh += '                            ' + str(kdcs__engm) + ',\n'
        hljtn__idzh += (
            '                            unicode_to_utf8(metadata),\n')
        hljtn__idzh += (
            '                            unicode_to_utf8(compression),\n')
        hljtn__idzh += (
            '                            _is_parallel, 0, 0, 0, 0,\n')
        hljtn__idzh += (
            '                            unicode_to_utf8(name_ptr),\n')
        hljtn__idzh += (
            '                            unicode_to_utf8(bucket_region),\n')
        hljtn__idzh += '                            row_group_size)\n'
        hljtn__idzh += '    delete_table_decref_arrays(table)\n'
        hljtn__idzh += '    delete_info_decref_array(index_col)\n'
        hljtn__idzh += '    delete_info_decref_array(col_names)\n'
    qpcx__wxpnc = {}
    if df.has_runtime_cols:
        mmtx__bxv = None
    else:
        for zequ__mioy in df.columns:
            if not isinstance(zequ__mioy, str):
                raise BodoError(
                    'DataFrame.to_parquet(): parquet must have string column names'
                    )
        mmtx__bxv = pd.array(df.columns)
    exec(hljtn__idzh, {'np': np, 'bodo': bodo, 'unicode_to_utf8':
        unicode_to_utf8, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'str_arr_from_sequence': str_arr_from_sequence,
        'parquet_write_table_cpp': parquet_write_table_cpp,
        'parquet_write_table_partitioned_cpp':
        parquet_write_table_partitioned_cpp, 'index_to_array':
        index_to_array, 'delete_info_decref_array':
        delete_info_decref_array, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'col_names_arr': mmtx__bxv,
        'py_table_to_cpp_table': py_table_to_cpp_table, 'py_table_typ': df.
        table_type, 'get_dataframe_table': get_dataframe_table,
        'col_names_no_parts_arr': sjavp__ften, 'get_dataframe_column_names':
        get_dataframe_column_names, 'fix_arr_dtype': fix_arr_dtype,
        'decode_if_dict_array': decode_if_dict_array,
        'decode_if_dict_table': decode_if_dict_table}, qpcx__wxpnc)
    jzo__ogv = qpcx__wxpnc['df_to_parquet']
    return jzo__ogv


def to_sql_exception_guard(df, name, con, schema=None, if_exists='fail',
    index=True, index_label=None, chunksize=None, dtype=None, method=None,
    _is_table_create=False, _is_parallel=False):
    ysswu__mvy = 'all_ok'
    zrnyq__ysrh, ieq__izzfq = bodo.ir.sql_ext.parse_dbtype(con)
    if _is_parallel and bodo.get_rank() == 0:
        bgr__uemq = 100
        if chunksize is None:
            opz__qoyu = bgr__uemq
        else:
            opz__qoyu = min(chunksize, bgr__uemq)
        if _is_table_create:
            df = df.iloc[:opz__qoyu, :]
        else:
            df = df.iloc[opz__qoyu:, :]
            if len(df) == 0:
                return ysswu__mvy
    uesxn__xxw = df.columns
    try:
        if zrnyq__ysrh == 'snowflake':
            if ieq__izzfq and con.count(ieq__izzfq) == 1:
                con = con.replace(ieq__izzfq, quote(ieq__izzfq))
            try:
                from snowflake.connector.pandas_tools import pd_writer
                from bodo import snowflake_sqlalchemy_compat
                if method is not None and _is_table_create and bodo.get_rank(
                    ) == 0:
                    import warnings
                    from bodo.utils.typing import BodoWarning
                    warnings.warn(BodoWarning(
                        'DataFrame.to_sql(): method argument is not supported with Snowflake. Bodo always uses snowflake.connector.pandas_tools.pd_writer to write data.'
                        ))
                method = pd_writer
                df.columns = [(xeul__cris.upper() if xeul__cris.islower() else
                    xeul__cris) for xeul__cris in df.columns]
            except ImportError as xrpqk__cuhvj:
                ysswu__mvy = (
                    "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires both snowflake-sqlalchemy and snowflake-connector-python. These can be installed by calling 'conda install -c conda-forge snowflake-sqlalchemy snowflake-connector-python' or 'pip install snowflake-sqlalchemy snowflake-connector-python'."
                    )
                return ysswu__mvy
        if zrnyq__ysrh == 'oracle':
            import sqlalchemy as sa
            tgg__tas = bodo.typeof(df)
            dcmx__adg = {}
            for xeul__cris, yam__wualp in zip(tgg__tas.columns, tgg__tas.data):
                if df[xeul__cris].dtype == 'object':
                    if yam__wualp == datetime_date_array_type:
                        dcmx__adg[xeul__cris] = sa.types.Date
                    elif yam__wualp == bodo.string_array_type:
                        dcmx__adg[xeul__cris] = sa.types.VARCHAR(df[
                            xeul__cris].str.len().max())
            dtype = dcmx__adg
        try:
            df.to_sql(name, con, schema, if_exists, index, index_label,
                chunksize, dtype, method)
        except Exception as yjuv__hzzbp:
            ysswu__mvy = yjuv__hzzbp.args[0]
        return ysswu__mvy
    finally:
        df.columns = uesxn__xxw


@numba.njit
def to_sql_exception_guard_encaps(df, name, con, schema=None, if_exists=
    'fail', index=True, index_label=None, chunksize=None, dtype=None,
    method=None, _is_table_create=False, _is_parallel=False):
    with numba.objmode(out='unicode_type'):
        out = to_sql_exception_guard(df, name, con, schema, if_exists,
            index, index_label, chunksize, dtype, method, _is_table_create,
            _is_parallel)
    return out


@overload_method(DataFrameType, 'to_sql')
def to_sql_overload(df, name, con, schema=None, if_exists='fail', index=
    True, index_label=None, chunksize=None, dtype=None, method=None,
    _is_parallel=False):
    check_runtime_cols_unsupported(df, 'DataFrame.to_sql()')
    if is_overload_none(schema):
        if bodo.get_rank() == 0:
            import warnings
            warnings.warn(BodoWarning(
                f'DataFrame.to_sql(): schema argument is recommended to avoid permission issues when writing the table.'
                ))
    if not (is_overload_none(chunksize) or isinstance(chunksize, types.Integer)
        ):
        raise BodoError(
            "DataFrame.to_sql(): 'chunksize' argument must be an integer if provided."
            )

    def _impl(df, name, con, schema=None, if_exists='fail', index=True,
        index_label=None, chunksize=None, dtype=None, method=None,
        _is_parallel=False):
        sjps__qhxl = bodo.libs.distributed_api.get_rank()
        ysswu__mvy = 'unset'
        if sjps__qhxl != 0:
            ysswu__mvy = bcast_scalar(ysswu__mvy)
        elif sjps__qhxl == 0:
            ysswu__mvy = to_sql_exception_guard_encaps(df, name, con,
                schema, if_exists, index, index_label, chunksize, dtype,
                method, True, _is_parallel)
            ysswu__mvy = bcast_scalar(ysswu__mvy)
        if_exists = 'append'
        if _is_parallel and ysswu__mvy == 'all_ok':
            ysswu__mvy = to_sql_exception_guard_encaps(df, name, con,
                schema, if_exists, index, index_label, chunksize, dtype,
                method, False, _is_parallel)
        if ysswu__mvy != 'all_ok':
            print('err_msg=', ysswu__mvy)
            raise ValueError('error in to_sql() operation')
    return _impl


@overload_method(DataFrameType, 'to_csv', no_unliteral=True)
def to_csv_overload(df, path_or_buf=None, sep=',', na_rep='', float_format=
    None, columns=None, header=True, index=True, index_label=None, mode='w',
    encoding=None, compression=None, quoting=None, quotechar='"',
    line_terminator=None, chunksize=None, date_format=None, doublequote=
    True, escapechar=None, decimal='.', errors='strict', storage_options=None):
    check_runtime_cols_unsupported(df, 'DataFrame.to_csv()')
    check_unsupported_args('DataFrame.to_csv', {'encoding': encoding,
        'mode': mode, 'errors': errors, 'storage_options': storage_options},
        {'encoding': None, 'mode': 'w', 'errors': 'strict',
        'storage_options': None}, package_name='pandas', module_name='IO')
    if not (is_overload_none(path_or_buf) or is_overload_constant_str(
        path_or_buf) or path_or_buf == string_type):
        raise BodoError(
            "DataFrame.to_csv(): 'path_or_buf' argument should be None or string"
            )
    if not is_overload_none(compression):
        raise BodoError(
            "DataFrame.to_csv(): 'compression' argument supports only None, which is the default in JIT code."
            )
    if is_overload_constant_str(path_or_buf):
        dlvd__nfqgr = get_overload_const_str(path_or_buf)
        if dlvd__nfqgr.endswith(('.gz', '.bz2', '.zip', '.xz')):
            import warnings
            from bodo.utils.typing import BodoWarning
            warnings.warn(BodoWarning(
                "DataFrame.to_csv(): 'compression' argument defaults to None in JIT code, which is the only supported value."
                ))
    if not (is_overload_none(columns) or isinstance(columns, (types.List,
        types.Tuple))):
        raise BodoError(
            "DataFrame.to_csv(): 'columns' argument must be list a or tuple type."
            )
    if is_overload_none(path_or_buf):

        def _impl(df, path_or_buf=None, sep=',', na_rep='', float_format=
            None, columns=None, header=True, index=True, index_label=None,
            mode='w', encoding=None, compression=None, quoting=None,
            quotechar='"', line_terminator=None, chunksize=None,
            date_format=None, doublequote=True, escapechar=None, decimal=
            '.', errors='strict', storage_options=None):
            with numba.objmode(D='unicode_type'):
                D = df.to_csv(path_or_buf, sep, na_rep, float_format,
                    columns, header, index, index_label, mode, encoding,
                    compression, quoting, quotechar, line_terminator,
                    chunksize, date_format, doublequote, escapechar,
                    decimal, errors, storage_options)
            return D
        return _impl

    def _impl(df, path_or_buf=None, sep=',', na_rep='', float_format=None,
        columns=None, header=True, index=True, index_label=None, mode='w',
        encoding=None, compression=None, quoting=None, quotechar='"',
        line_terminator=None, chunksize=None, date_format=None, doublequote
        =True, escapechar=None, decimal='.', errors='strict',
        storage_options=None):
        with numba.objmode(D='unicode_type'):
            D = df.to_csv(None, sep, na_rep, float_format, columns, header,
                index, index_label, mode, encoding, compression, quoting,
                quotechar, line_terminator, chunksize, date_format,
                doublequote, escapechar, decimal, errors, storage_options)
        bodo.io.fs_io.csv_write(path_or_buf, D)
    return _impl


@overload_method(DataFrameType, 'to_json', no_unliteral=True)
def to_json_overload(df, path_or_buf=None, orient='records', date_format=
    None, double_precision=10, force_ascii=True, date_unit='ms',
    default_handler=None, lines=True, compression='infer', index=True,
    indent=None, storage_options=None):
    check_runtime_cols_unsupported(df, 'DataFrame.to_json()')
    check_unsupported_args('DataFrame.to_json', {'storage_options':
        storage_options}, {'storage_options': None}, package_name='pandas',
        module_name='IO')
    if path_or_buf is None or path_or_buf == types.none:

        def _impl(df, path_or_buf=None, orient='records', date_format=None,
            double_precision=10, force_ascii=True, date_unit='ms',
            default_handler=None, lines=True, compression='infer', index=
            True, indent=None, storage_options=None):
            with numba.objmode(D='unicode_type'):
                D = df.to_json(path_or_buf, orient, date_format,
                    double_precision, force_ascii, date_unit,
                    default_handler, lines, compression, index, indent,
                    storage_options)
            return D
        return _impl

    def _impl(df, path_or_buf=None, orient='records', date_format=None,
        double_precision=10, force_ascii=True, date_unit='ms',
        default_handler=None, lines=True, compression='infer', index=True,
        indent=None, storage_options=None):
        with numba.objmode(D='unicode_type'):
            D = df.to_json(None, orient, date_format, double_precision,
                force_ascii, date_unit, default_handler, lines, compression,
                index, indent, storage_options)
        tyibv__hahdd = bodo.io.fs_io.get_s3_bucket_region_njit(path_or_buf,
            parallel=False)
        if lines and orient == 'records':
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, True,
                unicode_to_utf8(tyibv__hahdd))
            bodo.utils.utils.check_and_propagate_cpp_exception()
        else:
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, False,
                unicode_to_utf8(tyibv__hahdd))
            bodo.utils.utils.check_and_propagate_cpp_exception()
    return _impl


@overload(pd.get_dummies, inline='always', no_unliteral=True)
def get_dummies(data, prefix=None, prefix_sep='_', dummy_na=False, columns=
    None, sparse=False, drop_first=False, dtype=None):
    idhvr__wucl = {'prefix': prefix, 'prefix_sep': prefix_sep, 'dummy_na':
        dummy_na, 'columns': columns, 'sparse': sparse, 'drop_first':
        drop_first, 'dtype': dtype}
    urbs__uks = {'prefix': None, 'prefix_sep': '_', 'dummy_na': False,
        'columns': None, 'sparse': False, 'drop_first': False, 'dtype': None}
    check_unsupported_args('pandas.get_dummies', idhvr__wucl, urbs__uks,
        package_name='pandas', module_name='General')
    if not categorical_can_construct_dataframe(data):
        raise BodoError(
            'pandas.get_dummies() only support categorical data types with explicitly known categories'
            )
    hljtn__idzh = """def impl(data, prefix=None, prefix_sep='_', dummy_na=False, columns=None, sparse=False, drop_first=False, dtype=None,):
"""
    if isinstance(data, SeriesType):
        prrj__wuu = data.data.dtype.categories
        hljtn__idzh += (
            '  data_values = bodo.hiframes.pd_series_ext.get_series_data(data)\n'
            )
    else:
        prrj__wuu = data.dtype.categories
        hljtn__idzh += '  data_values = data\n'
    kuvr__ame = len(prrj__wuu)
    hljtn__idzh += """  codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(data_values)
"""
    hljtn__idzh += '  numba.parfors.parfor.init_prange()\n'
    hljtn__idzh += '  n = len(data_values)\n'
    for i in range(kuvr__ame):
        hljtn__idzh += '  data_arr_{} = np.empty(n, np.uint8)\n'.format(i)
    hljtn__idzh += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    hljtn__idzh += '      if bodo.libs.array_kernels.isna(data_values, i):\n'
    for npak__finid in range(kuvr__ame):
        hljtn__idzh += '          data_arr_{}[i] = 0\n'.format(npak__finid)
    hljtn__idzh += '      else:\n'
    for musay__noyqc in range(kuvr__ame):
        hljtn__idzh += '          data_arr_{0}[i] = codes[i] == {0}\n'.format(
            musay__noyqc)
    ytwz__vqhd = ', '.join(f'data_arr_{i}' for i in range(kuvr__ame))
    index = 'bodo.hiframes.pd_index_ext.init_range_index(0, n, 1, None)'
    if isinstance(prrj__wuu[0], np.datetime64):
        prrj__wuu = tuple(pd.Timestamp(xeul__cris) for xeul__cris in prrj__wuu)
    elif isinstance(prrj__wuu[0], np.timedelta64):
        prrj__wuu = tuple(pd.Timedelta(xeul__cris) for xeul__cris in prrj__wuu)
    return bodo.hiframes.dataframe_impl._gen_init_df(hljtn__idzh, prrj__wuu,
        ytwz__vqhd, index)


def categorical_can_construct_dataframe(val):
    if isinstance(val, CategoricalArrayType):
        return val.dtype.categories is not None
    elif isinstance(val, SeriesType) and isinstance(val.data,
        CategoricalArrayType):
        return val.data.dtype.categories is not None
    return False


def handle_inplace_df_type_change(inplace, _bodo_transformed, func_name):
    if is_overload_false(_bodo_transformed
        ) and bodo.transforms.typing_pass.in_partial_typing and (
        is_overload_true(inplace) or not is_overload_constant_bool(inplace)):
        bodo.transforms.typing_pass.typing_transform_required = True
        raise Exception('DataFrame.{}(): transform necessary for inplace'.
            format(func_name))


pd_unsupported = (pd.read_pickle, pd.read_table, pd.read_fwf, pd.
    read_clipboard, pd.ExcelFile, pd.read_html, pd.read_xml, pd.read_hdf,
    pd.read_feather, pd.read_orc, pd.read_sas, pd.read_spss, pd.
    read_sql_query, pd.read_gbq, pd.read_stata, pd.ExcelWriter, pd.
    json_normalize, pd.merge_ordered, pd.factorize, pd.wide_to_long, pd.
    bdate_range, pd.period_range, pd.infer_freq, pd.interval_range, pd.eval,
    pd.test, pd.Grouper)
pd_util_unsupported = pd.util.hash_array, pd.util.hash_pandas_object
dataframe_unsupported = ['set_flags', 'convert_dtypes', 'bool', '__iter__',
    'items', 'iteritems', 'keys', 'iterrows', 'lookup', 'pop', 'xs', 'get',
    'add', 'sub', 'mul', 'div', 'truediv', 'floordiv', 'mod', 'pow', 'dot',
    'radd', 'rsub', 'rmul', 'rdiv', 'rtruediv', 'rfloordiv', 'rmod', 'rpow',
    'lt', 'gt', 'le', 'ge', 'ne', 'eq', 'combine', 'combine_first',
    'subtract', 'divide', 'multiply', 'applymap', 'agg', 'aggregate',
    'transform', 'expanding', 'ewm', 'all', 'any', 'clip', 'corrwith',
    'cummax', 'cummin', 'eval', 'kurt', 'kurtosis', 'mad', 'mode', 'rank',
    'round', 'sem', 'skew', 'value_counts', 'add_prefix', 'add_suffix',
    'align', 'at_time', 'between_time', 'equals', 'reindex', 'reindex_like',
    'rename_axis', 'set_axis', 'truncate', 'backfill', 'bfill', 'ffill',
    'interpolate', 'pad', 'droplevel', 'reorder_levels', 'nlargest',
    'nsmallest', 'swaplevel', 'stack', 'unstack', 'swapaxes', 'squeeze',
    'to_xarray', 'T', 'transpose', 'compare', 'update', 'asfreq', 'asof',
    'slice_shift', 'tshift', 'first_valid_index', 'last_valid_index',
    'resample', 'to_period', 'to_timestamp', 'tz_convert', 'tz_localize',
    'boxplot', 'hist', 'from_dict', 'from_records', 'to_pickle', 'to_hdf',
    'to_dict', 'to_excel', 'to_html', 'to_feather', 'to_latex', 'to_stata',
    'to_gbq', 'to_records', 'to_clipboard', 'to_markdown', 'to_xml']
dataframe_unsupported_attrs = ['at', 'attrs', 'axes', 'flags', 'style',
    'sparse']


def _install_pd_unsupported(mod_name, pd_unsupported):
    for qdygy__tcb in pd_unsupported:
        lnqum__atlt = mod_name + '.' + qdygy__tcb.__name__
        overload(qdygy__tcb, no_unliteral=True)(create_unsupported_overload
            (lnqum__atlt))


def _install_dataframe_unsupported():
    for qmw__srp in dataframe_unsupported_attrs:
        dzgdp__xwhc = 'DataFrame.' + qmw__srp
        overload_attribute(DataFrameType, qmw__srp)(create_unsupported_overload
            (dzgdp__xwhc))
    for lnqum__atlt in dataframe_unsupported:
        dzgdp__xwhc = 'DataFrame.' + lnqum__atlt + '()'
        overload_method(DataFrameType, lnqum__atlt)(create_unsupported_overload
            (dzgdp__xwhc))


_install_pd_unsupported('pandas', pd_unsupported)
_install_pd_unsupported('pandas.util', pd_util_unsupported)
_install_dataframe_unsupported()
