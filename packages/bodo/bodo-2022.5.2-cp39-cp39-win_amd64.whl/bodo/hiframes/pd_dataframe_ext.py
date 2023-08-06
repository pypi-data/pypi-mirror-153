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
            wdxmv__hrlzx = (
                f'{len(self.data)} columns of types {set(self.data)}')
            goe__adgcx = (
                f"('{self.columns[0]}', '{self.columns[1]}', ..., '{self.columns[-1]}')"
                )
            return (
                f'dataframe({wdxmv__hrlzx}, {self.index}, {goe__adgcx}, {self.dist}, {self.is_table_format})'
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
        return {yzb__tus: i for i, yzb__tus in enumerate(self.columns)}

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
            pbaz__pwgzt = (self.index if self.index == other.index else
                self.index.unify(typingctx, other.index))
            data = tuple(gdw__kwy.unify(typingctx, uzjv__raq) if gdw__kwy !=
                uzjv__raq else gdw__kwy for gdw__kwy, uzjv__raq in zip(self
                .data, other.data))
            dist = Distribution(min(self.dist.value, other.dist.value))
            if pbaz__pwgzt is not None and None not in data:
                return DataFrameType(data, pbaz__pwgzt, self.columns, dist,
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
        return all(gdw__kwy.is_precise() for gdw__kwy in self.data
            ) and self.index.is_precise()

    def replace_col_type(self, col_name, new_type):
        if col_name not in self.columns:
            raise ValueError(
                f"DataFrameType.replace_col_type replaced column must be found in the DataFrameType. '{col_name}' not found in DataFrameType with columns {self.columns}"
                )
        hzp__tzlud = self.columns.index(col_name)
        mnfgi__nys = tuple(list(self.data[:hzp__tzlud]) + [new_type] + list
            (self.data[hzp__tzlud + 1:]))
        return DataFrameType(mnfgi__nys, self.index, self.columns, self.
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
        xxxxd__ovmh = [('data', data_typ), ('index', fe_type.df_type.index),
            ('parent', types.pyobject)]
        if fe_type.df_type.has_runtime_cols:
            xxxxd__ovmh.append(('columns', fe_type.df_type.runtime_colname_typ)
                )
        super(DataFramePayloadModel, self).__init__(dmm, fe_type, xxxxd__ovmh)


@register_model(DataFrameType)
class DataFrameModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = DataFramePayloadType(fe_type)
        xxxxd__ovmh = [('meminfo', types.MemInfoPointer(payload_type)), (
            'parent', types.pyobject)]
        super(DataFrameModel, self).__init__(dmm, fe_type, xxxxd__ovmh)


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
        lol__wgf = 'n',
        qcula__uxvl = {'n': 5}
        vcpxm__ymc, pxac__ddwhs = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, lol__wgf, qcula__uxvl)
        scmm__yuo = pxac__ddwhs[0]
        if not is_overload_int(scmm__yuo):
            raise BodoError(f"{func_name}(): 'n' must be an Integer")
        xaegu__ogqsr = df.copy(is_table_format=False)
        return xaegu__ogqsr(*pxac__ddwhs).replace(pysig=vcpxm__ymc)

    @bound_function('df.corr')
    def resolve_corr(self, df, args, kws):
        func_name = 'DataFrame.corr'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        paw__zey = (df,) + args
        lol__wgf = 'df', 'method', 'min_periods'
        qcula__uxvl = {'method': 'pearson', 'min_periods': 1}
        gzbp__ibrt = 'method',
        vcpxm__ymc, pxac__ddwhs = bodo.utils.typing.fold_typing_args(func_name,
            paw__zey, kws, lol__wgf, qcula__uxvl, gzbp__ibrt)
        tnqu__pvykp = pxac__ddwhs[2]
        if not is_overload_int(tnqu__pvykp):
            raise BodoError(f"{func_name}(): 'min_periods' must be an Integer")
        grniv__sfva = []
        ssqiq__ydn = []
        for yzb__tus, fut__nohr in zip(df.columns, df.data):
            if bodo.utils.typing._is_pandas_numeric_dtype(fut__nohr.dtype):
                grniv__sfva.append(yzb__tus)
                ssqiq__ydn.append(types.Array(types.float64, 1, 'A'))
        if len(grniv__sfva) == 0:
            raise_bodo_error('DataFrame.corr(): requires non-empty dataframe')
        ssqiq__ydn = tuple(ssqiq__ydn)
        grniv__sfva = tuple(grniv__sfva)
        index_typ = bodo.utils.typing.type_col_to_index(grniv__sfva)
        xaegu__ogqsr = DataFrameType(ssqiq__ydn, index_typ, grniv__sfva)
        return xaegu__ogqsr(*pxac__ddwhs).replace(pysig=vcpxm__ymc)

    @bound_function('df.pipe', no_unliteral=True)
    def resolve_pipe(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.pipe()')
        return bodo.hiframes.pd_groupby_ext.resolve_obj_pipe(self, df, args,
            kws, 'DataFrame')

    @bound_function('df.apply', no_unliteral=True)
    def resolve_apply(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.apply()')
        kws = dict(kws)
        qrrj__jski = args[0] if len(args) > 0 else kws.pop('func', None)
        axis = args[1] if len(args) > 1 else kws.pop('axis', types.literal(0))
        urxor__ojt = args[2] if len(args) > 2 else kws.pop('raw', types.
            literal(False))
        zixc__nmzy = args[3] if len(args) > 3 else kws.pop('result_type',
            types.none)
        ujq__kstqx = args[4] if len(args) > 4 else kws.pop('args', types.
            Tuple([]))
        adj__cpae = dict(raw=urxor__ojt, result_type=zixc__nmzy)
        zgl__rtzf = dict(raw=False, result_type=None)
        check_unsupported_args('Dataframe.apply', adj__cpae, zgl__rtzf,
            package_name='pandas', module_name='DataFrame')
        udgvw__kfooe = True
        if types.unliteral(qrrj__jski) == types.unicode_type:
            if not is_overload_constant_str(qrrj__jski):
                raise BodoError(
                    f'DataFrame.apply(): string argument (for builtins) must be a compile time constant'
                    )
            udgvw__kfooe = False
        if not is_overload_constant_int(axis):
            raise BodoError(
                'Dataframe.apply(): axis argument must be a compile time constant.'
                )
        lbun__wmbm = get_overload_const_int(axis)
        if udgvw__kfooe and lbun__wmbm != 1:
            raise BodoError(
                'Dataframe.apply(): only axis=1 supported for user-defined functions'
                )
        elif lbun__wmbm not in (0, 1):
            raise BodoError('Dataframe.apply(): axis must be either 0 or 1')
        dpzoq__mvy = []
        for arr_typ in df.data:
            nra__cvzmu = SeriesType(arr_typ.dtype, arr_typ, df.index,
                string_type)
            jsfcl__ojx = self.context.resolve_function_type(operator.
                getitem, (SeriesIlocType(nra__cvzmu), types.int64), {}
                ).return_type
            dpzoq__mvy.append(jsfcl__ojx)
        pnea__vsypk = types.none
        mal__xnmh = HeterogeneousIndexType(types.BaseTuple.from_types(tuple
            (types.literal(yzb__tus) for yzb__tus in df.columns)), None)
        mnqb__ixk = types.BaseTuple.from_types(dpzoq__mvy)
        qsfr__chx = types.Tuple([types.bool_] * len(mnqb__ixk))
        qyx__fka = bodo.NullableTupleType(mnqb__ixk, qsfr__chx)
        viaeo__gjmq = df.index.dtype
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df.index,
            'DataFrame.apply()')
        if viaeo__gjmq == types.NPDatetime('ns'):
            viaeo__gjmq = bodo.pd_timestamp_type
        if viaeo__gjmq == types.NPTimedelta('ns'):
            viaeo__gjmq = bodo.pd_timedelta_type
        if is_heterogeneous_tuple_type(mnqb__ixk):
            cob__bma = HeterogeneousSeriesType(qyx__fka, mal__xnmh, viaeo__gjmq
                )
        else:
            cob__bma = SeriesType(mnqb__ixk.dtype, qyx__fka, mal__xnmh,
                viaeo__gjmq)
        ipq__kqiab = cob__bma,
        if ujq__kstqx is not None:
            ipq__kqiab += tuple(ujq__kstqx.types)
        try:
            if not udgvw__kfooe:
                eds__cuha = bodo.utils.transform.get_udf_str_return_type(df,
                    get_overload_const_str(qrrj__jski), self.context,
                    'DataFrame.apply', axis if lbun__wmbm == 1 else None)
            else:
                eds__cuha = get_const_func_output_type(qrrj__jski,
                    ipq__kqiab, kws, self.context, numba.core.registry.
                    cpu_target.target_context)
        except Exception as axy__wou:
            raise_bodo_error(get_udf_error_msg('DataFrame.apply()', axy__wou))
        if udgvw__kfooe:
            if not (is_overload_constant_int(axis) and 
                get_overload_const_int(axis) == 1):
                raise BodoError(
                    'Dataframe.apply(): only user-defined functions with axis=1 supported'
                    )
            if isinstance(eds__cuha, (SeriesType, HeterogeneousSeriesType)
                ) and eds__cuha.const_info is None:
                raise BodoError(
                    'Invalid Series output in UDF (Series with constant length and constant Index value expected)'
                    )
            if isinstance(eds__cuha, HeterogeneousSeriesType):
                lar__cid, zpdt__lgb = eds__cuha.const_info
                if isinstance(eds__cuha.data, bodo.libs.nullable_tuple_ext.
                    NullableTupleType):
                    ljwo__tadak = eds__cuha.data.tuple_typ.types
                elif isinstance(eds__cuha.data, types.Tuple):
                    ljwo__tadak = eds__cuha.data.types
                else:
                    raise_bodo_error(
                        'df.apply(): Unexpected Series return type for Heterogeneous data'
                        )
                etoc__zze = tuple(to_nullable_type(dtype_to_array_type(
                    yas__drfp)) for yas__drfp in ljwo__tadak)
                uzqw__kizo = DataFrameType(etoc__zze, df.index, zpdt__lgb)
            elif isinstance(eds__cuha, SeriesType):
                wfk__dcmc, zpdt__lgb = eds__cuha.const_info
                etoc__zze = tuple(to_nullable_type(dtype_to_array_type(
                    eds__cuha.dtype)) for lar__cid in range(wfk__dcmc))
                uzqw__kizo = DataFrameType(etoc__zze, df.index, zpdt__lgb)
            else:
                ysi__orzxc = get_udf_out_arr_type(eds__cuha)
                uzqw__kizo = SeriesType(ysi__orzxc.dtype, ysi__orzxc, df.
                    index, None)
        else:
            uzqw__kizo = eds__cuha
        teo__qacs = ', '.join("{} = ''".format(gdw__kwy) for gdw__kwy in
            kws.keys())
        hpxwn__ilmnz = f"""def apply_stub(func, axis=0, raw=False, result_type=None, args=(), {teo__qacs}):
"""
        hpxwn__ilmnz += '    pass\n'
        fsvb__dmbn = {}
        exec(hpxwn__ilmnz, {}, fsvb__dmbn)
        vgy__vnd = fsvb__dmbn['apply_stub']
        vcpxm__ymc = numba.core.utils.pysignature(vgy__vnd)
        jvwrr__xsrt = (qrrj__jski, axis, urxor__ojt, zixc__nmzy, ujq__kstqx
            ) + tuple(kws.values())
        return signature(uzqw__kizo, *jvwrr__xsrt).replace(pysig=vcpxm__ymc)

    @bound_function('df.plot', no_unliteral=True)
    def resolve_plot(self, df, args, kws):
        func_name = 'DataFrame.plot'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        lol__wgf = ('x', 'y', 'kind', 'figsize', 'ax', 'subplots', 'sharex',
            'sharey', 'layout', 'use_index', 'title', 'grid', 'legend',
            'style', 'logx', 'logy', 'loglog', 'xticks', 'yticks', 'xlim',
            'ylim', 'rot', 'fontsize', 'colormap', 'table', 'yerr', 'xerr',
            'secondary_y', 'sort_columns', 'xlabel', 'ylabel', 'position',
            'stacked', 'mark_right', 'include_bool', 'backend')
        qcula__uxvl = {'x': None, 'y': None, 'kind': 'line', 'figsize':
            None, 'ax': None, 'subplots': False, 'sharex': None, 'sharey': 
            False, 'layout': None, 'use_index': True, 'title': None, 'grid':
            None, 'legend': True, 'style': None, 'logx': False, 'logy': 
            False, 'loglog': False, 'xticks': None, 'yticks': None, 'xlim':
            None, 'ylim': None, 'rot': None, 'fontsize': None, 'colormap':
            None, 'table': False, 'yerr': None, 'xerr': None, 'secondary_y':
            False, 'sort_columns': False, 'xlabel': None, 'ylabel': None,
            'position': 0.5, 'stacked': False, 'mark_right': True,
            'include_bool': False, 'backend': None}
        gzbp__ibrt = ('subplots', 'sharex', 'sharey', 'layout', 'use_index',
            'grid', 'style', 'logx', 'logy', 'loglog', 'xlim', 'ylim',
            'rot', 'colormap', 'table', 'yerr', 'xerr', 'sort_columns',
            'secondary_y', 'colorbar', 'position', 'stacked', 'mark_right',
            'include_bool', 'backend')
        vcpxm__ymc, pxac__ddwhs = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, lol__wgf, qcula__uxvl, gzbp__ibrt)
        rayhf__ness = pxac__ddwhs[2]
        if not is_overload_constant_str(rayhf__ness):
            raise BodoError(
                f"{func_name}: kind must be a constant string and one of ('line', 'scatter')."
                )
        ixzb__ckg = pxac__ddwhs[0]
        if not is_overload_none(ixzb__ckg) and not (is_overload_int(
            ixzb__ckg) or is_overload_constant_str(ixzb__ckg)):
            raise BodoError(
                f'{func_name}: x must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(ixzb__ckg):
            gdyj__hdven = get_overload_const_str(ixzb__ckg)
            if gdyj__hdven not in df.columns:
                raise BodoError(f'{func_name}: {gdyj__hdven} column not found.'
                    )
        elif is_overload_int(ixzb__ckg):
            clf__fayu = get_overload_const_int(ixzb__ckg)
            if clf__fayu > len(df.columns):
                raise BodoError(
                    f'{func_name}: x: {clf__fayu} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            ixzb__ckg = df.columns[ixzb__ckg]
        vxf__mhqfm = pxac__ddwhs[1]
        if not is_overload_none(vxf__mhqfm) and not (is_overload_int(
            vxf__mhqfm) or is_overload_constant_str(vxf__mhqfm)):
            raise BodoError(
                'df.plot(): y must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(vxf__mhqfm):
            uth__gqphj = get_overload_const_str(vxf__mhqfm)
            if uth__gqphj not in df.columns:
                raise BodoError(f'{func_name}: {uth__gqphj} column not found.')
        elif is_overload_int(vxf__mhqfm):
            zstj__sbz = get_overload_const_int(vxf__mhqfm)
            if zstj__sbz > len(df.columns):
                raise BodoError(
                    f'{func_name}: y: {zstj__sbz} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            vxf__mhqfm = df.columns[vxf__mhqfm]
        hclt__gdl = pxac__ddwhs[3]
        if not is_overload_none(hclt__gdl) and not is_tuple_like_type(hclt__gdl
            ):
            raise BodoError(
                f'{func_name}: figsize must be a constant numeric tuple (width, height) or None.'
                )
        vual__clv = pxac__ddwhs[10]
        if not is_overload_none(vual__clv) and not is_overload_constant_str(
            vual__clv):
            raise BodoError(
                f'{func_name}: title must be a constant string or None.')
        xhn__udv = pxac__ddwhs[12]
        if not is_overload_bool(xhn__udv):
            raise BodoError(f'{func_name}: legend must be a boolean type.')
        qjf__cfbif = pxac__ddwhs[17]
        if not is_overload_none(qjf__cfbif) and not is_tuple_like_type(
            qjf__cfbif):
            raise BodoError(
                f'{func_name}: xticks must be a constant tuple or None.')
        nqp__cih = pxac__ddwhs[18]
        if not is_overload_none(nqp__cih) and not is_tuple_like_type(nqp__cih):
            raise BodoError(
                f'{func_name}: yticks must be a constant tuple or None.')
        saei__ksxyq = pxac__ddwhs[22]
        if not is_overload_none(saei__ksxyq) and not is_overload_int(
            saei__ksxyq):
            raise BodoError(
                f'{func_name}: fontsize must be an integer or None.')
        uyoa__pds = pxac__ddwhs[29]
        if not is_overload_none(uyoa__pds) and not is_overload_constant_str(
            uyoa__pds):
            raise BodoError(
                f'{func_name}: xlabel must be a constant string or None.')
        sug__dkve = pxac__ddwhs[30]
        if not is_overload_none(sug__dkve) and not is_overload_constant_str(
            sug__dkve):
            raise BodoError(
                f'{func_name}: ylabel must be a constant string or None.')
        brqud__rymx = types.List(types.mpl_line_2d_type)
        rayhf__ness = get_overload_const_str(rayhf__ness)
        if rayhf__ness == 'scatter':
            if is_overload_none(ixzb__ckg) and is_overload_none(vxf__mhqfm):
                raise BodoError(
                    f'{func_name}: {rayhf__ness} requires an x and y column.')
            elif is_overload_none(ixzb__ckg):
                raise BodoError(
                    f'{func_name}: {rayhf__ness} x column is missing.')
            elif is_overload_none(vxf__mhqfm):
                raise BodoError(
                    f'{func_name}: {rayhf__ness} y column is missing.')
            brqud__rymx = types.mpl_path_collection_type
        elif rayhf__ness != 'line':
            raise BodoError(
                f'{func_name}: {rayhf__ness} plot is not supported.')
        return signature(brqud__rymx, *pxac__ddwhs).replace(pysig=vcpxm__ymc)

    def generic_resolve(self, df, attr):
        if self._is_existing_attr(attr):
            return
        check_runtime_cols_unsupported(df,
            'Acessing DataFrame columns by attribute')
        if attr in df.columns:
            fbwne__dxbj = df.columns.index(attr)
            arr_typ = df.data[fbwne__dxbj]
            return SeriesType(arr_typ.dtype, arr_typ, df.index, types.
                StringLiteral(attr))
        if len(df.columns) > 0 and isinstance(df.columns[0], tuple):
            qojd__epwga = []
            mnfgi__nys = []
            pfcn__cjju = False
            for i, thb__zcpso in enumerate(df.columns):
                if thb__zcpso[0] != attr:
                    continue
                pfcn__cjju = True
                qojd__epwga.append(thb__zcpso[1] if len(thb__zcpso) == 2 else
                    thb__zcpso[1:])
                mnfgi__nys.append(df.data[i])
            if pfcn__cjju:
                return DataFrameType(tuple(mnfgi__nys), df.index, tuple(
                    qojd__epwga))


DataFrameAttribute._no_unliteral = True


@overload(operator.getitem, no_unliteral=True)
def namedtuple_getitem_overload(tup, idx):
    if isinstance(tup, types.BaseNamedTuple) and is_overload_constant_str(idx):
        hek__vgjv = get_overload_const_str(idx)
        val_ind = tup.instance_class._fields.index(hek__vgjv)
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
        jewd__xfd = builder.extract_value(payload.data, i)
        context.nrt.decref(builder, df_type.data[i], jewd__xfd)
    context.nrt.decref(builder, df_type.index, payload.index)


def define_df_dtor(context, builder, df_type, payload_type):
    sskm__vdx = builder.module
    weau__pde = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    qbn__kitrp = cgutils.get_or_insert_function(sskm__vdx, weau__pde, name=
        '.dtor.df.{}'.format(df_type))
    if not qbn__kitrp.is_declaration:
        return qbn__kitrp
    qbn__kitrp.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(qbn__kitrp.append_basic_block())
    lvjv__uaxgr = qbn__kitrp.args[0]
    mbyyy__xoxno = context.get_value_type(payload_type).as_pointer()
    yyoh__xib = builder.bitcast(lvjv__uaxgr, mbyyy__xoxno)
    payload = context.make_helper(builder, payload_type, ref=yyoh__xib)
    decref_df_data(context, builder, payload, df_type)
    has_parent = cgutils.is_not_null(builder, payload.parent)
    with builder.if_then(has_parent):
        idx__yhq = context.get_python_api(builder)
        poecv__wqjlq = idx__yhq.gil_ensure()
        idx__yhq.decref(payload.parent)
        idx__yhq.gil_release(poecv__wqjlq)
    builder.ret_void()
    return qbn__kitrp


def construct_dataframe(context, builder, df_type, data_tup, index_val,
    parent=None, colnames=None):
    payload_type = DataFramePayloadType(df_type)
    tcw__jxzf = cgutils.create_struct_proxy(payload_type)(context, builder)
    tcw__jxzf.data = data_tup
    tcw__jxzf.index = index_val
    if colnames is not None:
        assert df_type.has_runtime_cols, 'construct_dataframe can only provide colnames if columns are determined at runtime'
        tcw__jxzf.columns = colnames
    lsbo__cdptv = context.get_value_type(payload_type)
    gycc__wlh = context.get_abi_sizeof(lsbo__cdptv)
    mjqoo__fpt = define_df_dtor(context, builder, df_type, payload_type)
    mwtwt__rdl = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, gycc__wlh), mjqoo__fpt)
    wab__fxtfh = context.nrt.meminfo_data(builder, mwtwt__rdl)
    cgk__uba = builder.bitcast(wab__fxtfh, lsbo__cdptv.as_pointer())
    xrzti__bzetz = cgutils.create_struct_proxy(df_type)(context, builder)
    xrzti__bzetz.meminfo = mwtwt__rdl
    if parent is None:
        xrzti__bzetz.parent = cgutils.get_null_value(xrzti__bzetz.parent.type)
    else:
        xrzti__bzetz.parent = parent
        tcw__jxzf.parent = parent
        has_parent = cgutils.is_not_null(builder, parent)
        with builder.if_then(has_parent):
            idx__yhq = context.get_python_api(builder)
            poecv__wqjlq = idx__yhq.gil_ensure()
            idx__yhq.incref(parent)
            idx__yhq.gil_release(poecv__wqjlq)
    builder.store(tcw__jxzf._getvalue(), cgk__uba)
    return xrzti__bzetz._getvalue()


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
        kxvr__hoegj = [data_typ.dtype.arr_types.dtype] * len(data_typ.dtype
            .arr_types)
    else:
        kxvr__hoegj = [yas__drfp for yas__drfp in data_typ.dtype.arr_types]
    qvae__acms = DataFrameType(tuple(kxvr__hoegj + [colnames_index_typ]),
        index_typ, None, is_table_format=True)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup, index, col_names = args
        parent = None
        mwn__ycrn = construct_dataframe(context, builder, df_type, data_tup,
            index, parent, col_names)
        context.nrt.incref(builder, data_typ, data_tup)
        context.nrt.incref(builder, index_typ, index)
        context.nrt.incref(builder, colnames_index_typ, col_names)
        return mwn__ycrn
    sig = signature(qvae__acms, data_typ, index_typ, colnames_index_typ)
    return sig, codegen


@intrinsic
def init_dataframe(typingctx, data_tup_typ, index_typ, col_names_typ=None):
    assert is_pd_index_type(index_typ) or isinstance(index_typ, MultiIndexType
        ), 'init_dataframe(): invalid index type'
    wfk__dcmc = len(data_tup_typ.types)
    if wfk__dcmc == 0:
        column_names = ()
    elif isinstance(col_names_typ, types.TypeRef):
        column_names = col_names_typ.instance_type.columns
    else:
        column_names = get_const_tup_vals(col_names_typ)
    if wfk__dcmc == 1 and isinstance(data_tup_typ.types[0], TableType):
        wfk__dcmc = len(data_tup_typ.types[0].arr_types)
    assert len(column_names
        ) == wfk__dcmc, 'init_dataframe(): number of column names does not match number of columns'
    is_table_format = False
    vzy__foc = data_tup_typ.types
    if wfk__dcmc != 0 and isinstance(data_tup_typ.types[0], TableType):
        vzy__foc = data_tup_typ.types[0].arr_types
        is_table_format = True
    qvae__acms = DataFrameType(vzy__foc, index_typ, column_names,
        is_table_format=is_table_format)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup = args[0]
        index_val = args[1]
        parent = None
        if is_table_format:
            ytm__lbv = cgutils.create_struct_proxy(qvae__acms.table_type)(
                context, builder, builder.extract_value(data_tup, 0))
            parent = ytm__lbv.parent
        mwn__ycrn = construct_dataframe(context, builder, df_type, data_tup,
            index_val, parent, None)
        context.nrt.incref(builder, data_tup_typ, data_tup)
        context.nrt.incref(builder, index_typ, index_val)
        return mwn__ycrn
    sig = signature(qvae__acms, data_tup_typ, index_typ, col_names_typ)
    return sig, codegen


@intrinsic
def has_parent(typingctx, df=None):
    check_runtime_cols_unsupported(df, 'has_parent')

    def codegen(context, builder, sig, args):
        xrzti__bzetz = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        return cgutils.is_not_null(builder, xrzti__bzetz.parent)
    return signature(types.bool_, df), codegen


@intrinsic
def _column_needs_unboxing(typingctx, df_typ, i_typ=None):
    check_runtime_cols_unsupported(df_typ, '_column_needs_unboxing')
    assert isinstance(df_typ, DataFrameType) and is_overload_constant_int(i_typ
        )

    def codegen(context, builder, sig, args):
        tcw__jxzf = get_dataframe_payload(context, builder, df_typ, args[0])
        ekflo__uoxy = get_overload_const_int(i_typ)
        arr_typ = df_typ.data[ekflo__uoxy]
        if df_typ.is_table_format:
            ytm__lbv = cgutils.create_struct_proxy(df_typ.table_type)(context,
                builder, builder.extract_value(tcw__jxzf.data, 0))
            eorl__yabcg = df_typ.table_type.type_to_blk[arr_typ]
            bvgvu__iiqzq = getattr(ytm__lbv, f'block_{eorl__yabcg}')
            exy__jzzip = ListInstance(context, builder, types.List(arr_typ),
                bvgvu__iiqzq)
            rreep__rzlx = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[ekflo__uoxy])
            jewd__xfd = exy__jzzip.getitem(rreep__rzlx)
        else:
            jewd__xfd = builder.extract_value(tcw__jxzf.data, ekflo__uoxy)
        kcsin__zpgdl = cgutils.alloca_once_value(builder, jewd__xfd)
        uqp__fjx = cgutils.alloca_once_value(builder, context.
            get_constant_null(arr_typ))
        return is_ll_eq(builder, kcsin__zpgdl, uqp__fjx)
    return signature(types.bool_, df_typ, i_typ), codegen


def get_dataframe_payload(context, builder, df_type, value):
    mwtwt__rdl = cgutils.create_struct_proxy(df_type)(context, builder, value
        ).meminfo
    payload_type = DataFramePayloadType(df_type)
    payload = context.nrt.meminfo_data(builder, mwtwt__rdl)
    mbyyy__xoxno = context.get_value_type(payload_type).as_pointer()
    payload = builder.bitcast(payload, mbyyy__xoxno)
    return context.make_helper(builder, payload_type, ref=payload)


@intrinsic
def _get_dataframe_data(typingctx, df_typ=None):
    check_runtime_cols_unsupported(df_typ, '_get_dataframe_data')
    qvae__acms = types.Tuple(df_typ.data)
    if df_typ.is_table_format:
        qvae__acms = types.Tuple([TableType(df_typ.data)])
    sig = signature(qvae__acms, df_typ)

    def codegen(context, builder, signature, args):
        tcw__jxzf = get_dataframe_payload(context, builder, signature.args[
            0], args[0])
        return impl_ret_borrowed(context, builder, signature.return_type,
            tcw__jxzf.data)
    return sig, codegen


@intrinsic
def get_dataframe_index(typingctx, df_typ=None):

    def codegen(context, builder, signature, args):
        tcw__jxzf = get_dataframe_payload(context, builder, signature.args[
            0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.index, tcw__jxzf.
            index)
    qvae__acms = df_typ.index
    sig = signature(qvae__acms, df_typ)
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
        xaegu__ogqsr = df.data[i]
        return xaegu__ogqsr(*args)


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
        tcw__jxzf = get_dataframe_payload(context, builder, signature.args[
            0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.table_type,
            builder.extract_value(tcw__jxzf.data, 0))
    return df_typ.table_type(df_typ), codegen


@intrinsic
def get_dataframe_column_names(typingctx, df_typ=None):
    assert df_typ.has_runtime_cols, 'get_dataframe_column_names() expects columns to be determined at runtime'

    def codegen(context, builder, signature, args):
        tcw__jxzf = get_dataframe_payload(context, builder, signature.args[
            0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.
            runtime_colname_typ, tcw__jxzf.columns)
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
    mnqb__ixk = self.typemap[data_tup.name]
    if any(is_tuple_like_type(yas__drfp) for yas__drfp in mnqb__ixk.types):
        return None
    if equiv_set.has_shape(data_tup):
        ovl__bxf = equiv_set.get_shape(data_tup)
        if len(ovl__bxf) > 1:
            equiv_set.insert_equiv(*ovl__bxf)
        if len(ovl__bxf) > 0:
            mal__xnmh = self.typemap[index.name]
            if not isinstance(mal__xnmh, HeterogeneousIndexType
                ) and equiv_set.has_shape(index):
                equiv_set.insert_equiv(ovl__bxf[0], index)
            return ArrayAnalysis.AnalyzeResult(shape=(ovl__bxf[0], len(
                ovl__bxf)), pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_dataframe_ext_init_dataframe
    ) = init_dataframe_equiv


def get_dataframe_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    ywp__tlrxw = args[0]
    data_types = self.typemap[ywp__tlrxw.name].data
    if any(is_tuple_like_type(yas__drfp) for yas__drfp in data_types):
        return None
    if equiv_set.has_shape(ywp__tlrxw):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            ywp__tlrxw)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_data
    ) = get_dataframe_data_equiv


def get_dataframe_index_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 1 and not kws
    ywp__tlrxw = args[0]
    mal__xnmh = self.typemap[ywp__tlrxw.name].index
    if isinstance(mal__xnmh, HeterogeneousIndexType):
        return None
    if equiv_set.has_shape(ywp__tlrxw):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            ywp__tlrxw)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_index
    ) = get_dataframe_index_equiv


def get_dataframe_table_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    ywp__tlrxw = args[0]
    if equiv_set.has_shape(ywp__tlrxw):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            ywp__tlrxw), pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_table
    ) = get_dataframe_table_equiv


def get_dataframe_column_names_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    ywp__tlrxw = args[0]
    if equiv_set.has_shape(ywp__tlrxw):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            ywp__tlrxw)[1], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_column_names
    ) = get_dataframe_column_names_equiv


@intrinsic
def set_dataframe_data(typingctx, df_typ, c_ind_typ, arr_typ=None):
    check_runtime_cols_unsupported(df_typ, 'set_dataframe_data')
    assert is_overload_constant_int(c_ind_typ)
    ekflo__uoxy = get_overload_const_int(c_ind_typ)
    if df_typ.data[ekflo__uoxy] != arr_typ:
        raise BodoError(
            'Changing dataframe column data type inplace is not supported in conditionals/loops or for dataframe arguments'
            )

    def codegen(context, builder, signature, args):
        gfqr__fdsj, lar__cid, qdfy__ktom = args
        tcw__jxzf = get_dataframe_payload(context, builder, df_typ, gfqr__fdsj)
        if df_typ.is_table_format:
            ytm__lbv = cgutils.create_struct_proxy(df_typ.table_type)(context,
                builder, builder.extract_value(tcw__jxzf.data, 0))
            eorl__yabcg = df_typ.table_type.type_to_blk[arr_typ]
            bvgvu__iiqzq = getattr(ytm__lbv, f'block_{eorl__yabcg}')
            exy__jzzip = ListInstance(context, builder, types.List(arr_typ),
                bvgvu__iiqzq)
            rreep__rzlx = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[ekflo__uoxy])
            exy__jzzip.setitem(rreep__rzlx, qdfy__ktom, True)
        else:
            jewd__xfd = builder.extract_value(tcw__jxzf.data, ekflo__uoxy)
            context.nrt.decref(builder, df_typ.data[ekflo__uoxy], jewd__xfd)
            tcw__jxzf.data = builder.insert_value(tcw__jxzf.data,
                qdfy__ktom, ekflo__uoxy)
            context.nrt.incref(builder, arr_typ, qdfy__ktom)
        xrzti__bzetz = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=gfqr__fdsj)
        payload_type = DataFramePayloadType(df_typ)
        yyoh__xib = context.nrt.meminfo_data(builder, xrzti__bzetz.meminfo)
        mbyyy__xoxno = context.get_value_type(payload_type).as_pointer()
        yyoh__xib = builder.bitcast(yyoh__xib, mbyyy__xoxno)
        builder.store(tcw__jxzf._getvalue(), yyoh__xib)
        return impl_ret_borrowed(context, builder, df_typ, gfqr__fdsj)
    sig = signature(df_typ, df_typ, c_ind_typ, arr_typ)
    return sig, codegen


@intrinsic
def set_df_index(typingctx, df_t, index_t=None):
    check_runtime_cols_unsupported(df_t, 'set_df_index')

    def codegen(context, builder, signature, args):
        knce__gup = args[0]
        index_val = args[1]
        df_typ = signature.args[0]
        iwg__aqn = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=knce__gup)
        hlj__gusqk = get_dataframe_payload(context, builder, df_typ, knce__gup)
        xrzti__bzetz = construct_dataframe(context, builder, signature.
            return_type, hlj__gusqk.data, index_val, iwg__aqn.parent, None)
        context.nrt.incref(builder, index_t, index_val)
        context.nrt.incref(builder, types.Tuple(df_t.data), hlj__gusqk.data)
        return xrzti__bzetz
    qvae__acms = DataFrameType(df_t.data, index_t, df_t.columns, df_t.dist,
        df_t.is_table_format)
    sig = signature(qvae__acms, df_t, index_t)
    return sig, codegen


@intrinsic
def set_df_column_with_reflect(typingctx, df_type, cname_type, arr_type=None):
    check_runtime_cols_unsupported(df_type, 'set_df_column_with_reflect')
    assert is_literal_type(cname_type), 'constant column name expected'
    col_name = get_literal_value(cname_type)
    wfk__dcmc = len(df_type.columns)
    qncdj__sdxs = wfk__dcmc
    iflwx__lldst = df_type.data
    column_names = df_type.columns
    index_typ = df_type.index
    hxjdf__fthi = col_name not in df_type.columns
    ekflo__uoxy = wfk__dcmc
    if hxjdf__fthi:
        iflwx__lldst += arr_type,
        column_names += col_name,
        qncdj__sdxs += 1
    else:
        ekflo__uoxy = df_type.columns.index(col_name)
        iflwx__lldst = tuple(arr_type if i == ekflo__uoxy else iflwx__lldst
            [i] for i in range(wfk__dcmc))

    def codegen(context, builder, signature, args):
        gfqr__fdsj, lar__cid, qdfy__ktom = args
        in_dataframe_payload = get_dataframe_payload(context, builder,
            df_type, gfqr__fdsj)
        dnxu__vzax = cgutils.create_struct_proxy(df_type)(context, builder,
            value=gfqr__fdsj)
        if df_type.is_table_format:
            bmovc__usjy = df_type.table_type
            ypty__cwm = builder.extract_value(in_dataframe_payload.data, 0)
            iee__ksqvv = TableType(iflwx__lldst)
            gxbt__ikohw = set_table_data_codegen(context, builder,
                bmovc__usjy, ypty__cwm, iee__ksqvv, arr_type, qdfy__ktom,
                ekflo__uoxy, hxjdf__fthi)
            data_tup = context.make_tuple(builder, types.Tuple([iee__ksqvv]
                ), [gxbt__ikohw])
        else:
            vzy__foc = [(builder.extract_value(in_dataframe_payload.data, i
                ) if i != ekflo__uoxy else qdfy__ktom) for i in range(
                wfk__dcmc)]
            if hxjdf__fthi:
                vzy__foc.append(qdfy__ktom)
            for ywp__tlrxw, nijhf__qbcsr in zip(vzy__foc, iflwx__lldst):
                context.nrt.incref(builder, nijhf__qbcsr, ywp__tlrxw)
            data_tup = context.make_tuple(builder, types.Tuple(iflwx__lldst
                ), vzy__foc)
        index_val = in_dataframe_payload.index
        context.nrt.incref(builder, index_typ, index_val)
        pbxq__zbr = construct_dataframe(context, builder, signature.
            return_type, data_tup, index_val, dnxu__vzax.parent, None)
        if not hxjdf__fthi and arr_type == df_type.data[ekflo__uoxy]:
            decref_df_data(context, builder, in_dataframe_payload, df_type)
            payload_type = DataFramePayloadType(df_type)
            yyoh__xib = context.nrt.meminfo_data(builder, dnxu__vzax.meminfo)
            mbyyy__xoxno = context.get_value_type(payload_type).as_pointer()
            yyoh__xib = builder.bitcast(yyoh__xib, mbyyy__xoxno)
            wyulp__zppor = get_dataframe_payload(context, builder, df_type,
                pbxq__zbr)
            builder.store(wyulp__zppor._getvalue(), yyoh__xib)
            context.nrt.incref(builder, index_typ, index_val)
            if df_type.is_table_format:
                context.nrt.incref(builder, iee__ksqvv, builder.
                    extract_value(data_tup, 0))
            else:
                for ywp__tlrxw, nijhf__qbcsr in zip(vzy__foc, iflwx__lldst):
                    context.nrt.incref(builder, nijhf__qbcsr, ywp__tlrxw)
        has_parent = cgutils.is_not_null(builder, dnxu__vzax.parent)
        with builder.if_then(has_parent):
            idx__yhq = context.get_python_api(builder)
            poecv__wqjlq = idx__yhq.gil_ensure()
            rbcm__wzpk = context.get_env_manager(builder)
            context.nrt.incref(builder, arr_type, qdfy__ktom)
            yzb__tus = numba.core.pythonapi._BoxContext(context, builder,
                idx__yhq, rbcm__wzpk)
            bctl__sxfly = yzb__tus.pyapi.from_native_value(arr_type,
                qdfy__ktom, yzb__tus.env_manager)
            if isinstance(col_name, str):
                swd__ijiu = context.insert_const_string(builder.module,
                    col_name)
                idxtk__erlc = idx__yhq.string_from_string(swd__ijiu)
            else:
                assert isinstance(col_name, int)
                idxtk__erlc = idx__yhq.long_from_longlong(context.
                    get_constant(types.intp, col_name))
            idx__yhq.object_setitem(dnxu__vzax.parent, idxtk__erlc, bctl__sxfly
                )
            idx__yhq.decref(bctl__sxfly)
            idx__yhq.decref(idxtk__erlc)
            idx__yhq.gil_release(poecv__wqjlq)
        return pbxq__zbr
    qvae__acms = DataFrameType(iflwx__lldst, index_typ, column_names,
        df_type.dist, df_type.is_table_format)
    sig = signature(qvae__acms, df_type, cname_type, arr_type)
    return sig, codegen


@lower_constant(DataFrameType)
def lower_constant_dataframe(context, builder, df_type, pyval):
    check_runtime_cols_unsupported(df_type, 'lowering a constant DataFrame')
    wfk__dcmc = len(pyval.columns)
    vzy__foc = []
    for i in range(wfk__dcmc):
        tit__lqfvt = pyval.iloc[:, i]
        if isinstance(df_type.data[i], bodo.DatetimeArrayType):
            bctl__sxfly = tit__lqfvt.array
        else:
            bctl__sxfly = tit__lqfvt.values
        vzy__foc.append(bctl__sxfly)
    vzy__foc = tuple(vzy__foc)
    if df_type.is_table_format:
        ytm__lbv = context.get_constant_generic(builder, df_type.table_type,
            Table(vzy__foc))
        data_tup = lir.Constant.literal_struct([ytm__lbv])
    else:
        data_tup = lir.Constant.literal_struct([context.
            get_constant_generic(builder, df_type.data[i], thb__zcpso) for 
            i, thb__zcpso in enumerate(vzy__foc)])
    index_val = context.get_constant_generic(builder, df_type.index, pyval.
        index)
    berfa__jpu = context.get_constant_null(types.pyobject)
    payload = lir.Constant.literal_struct([data_tup, index_val, berfa__jpu])
    payload = cgutils.global_constant(builder, '.const.payload', payload
        ).bitcast(cgutils.voidptr_t)
    dbmm__ldama = context.get_constant(types.int64, -1)
    hfgvl__hnlg = context.get_constant_null(types.voidptr)
    mwtwt__rdl = lir.Constant.literal_struct([dbmm__ldama, hfgvl__hnlg,
        hfgvl__hnlg, payload, dbmm__ldama])
    mwtwt__rdl = cgutils.global_constant(builder, '.const.meminfo', mwtwt__rdl
        ).bitcast(cgutils.voidptr_t)
    return lir.Constant.literal_struct([mwtwt__rdl, berfa__jpu])


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
        pbaz__pwgzt = context.cast(builder, in_dataframe_payload.index,
            fromty.index, toty.index)
    else:
        pbaz__pwgzt = in_dataframe_payload.index
        context.nrt.incref(builder, fromty.index, pbaz__pwgzt)
    if (fromty.is_table_format == toty.is_table_format and fromty.data ==
        toty.data):
        mnfgi__nys = in_dataframe_payload.data
        if fromty.is_table_format:
            context.nrt.incref(builder, types.Tuple([fromty.table_type]),
                mnfgi__nys)
        else:
            context.nrt.incref(builder, types.BaseTuple.from_types(fromty.
                data), mnfgi__nys)
    elif not fromty.is_table_format and toty.is_table_format:
        mnfgi__nys = _cast_df_data_to_table_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    elif fromty.is_table_format and not toty.is_table_format:
        mnfgi__nys = _cast_df_data_to_tuple_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    elif fromty.is_table_format and toty.is_table_format:
        mnfgi__nys = _cast_df_data_keep_table_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    else:
        mnfgi__nys = _cast_df_data_keep_tuple_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    return construct_dataframe(context, builder, toty, mnfgi__nys,
        pbaz__pwgzt, in_dataframe_payload.parent, None)


def _cast_empty_df(context, builder, toty):
    vtk__yykom = {}
    if isinstance(toty.index, RangeIndexType):
        index = 'bodo.hiframes.pd_index_ext.init_range_index(0, 0, 1, None)'
    else:
        zagh__fdpod = get_index_data_arr_types(toty.index)[0]
        boo__gta = bodo.utils.transform.get_type_alloc_counts(zagh__fdpod) - 1
        cta__hxd = ', '.join('0' for lar__cid in range(boo__gta))
        index = (
            'bodo.utils.conversion.index_from_array(bodo.utils.utils.alloc_type(0, index_arr_type, ({}{})))'
            .format(cta__hxd, ', ' if boo__gta == 1 else ''))
        vtk__yykom['index_arr_type'] = zagh__fdpod
    bpa__orvj = []
    for i, arr_typ in enumerate(toty.data):
        boo__gta = bodo.utils.transform.get_type_alloc_counts(arr_typ) - 1
        cta__hxd = ', '.join('0' for lar__cid in range(boo__gta))
        lhby__saypx = ('bodo.utils.utils.alloc_type(0, arr_type{}, ({}{}))'
            .format(i, cta__hxd, ', ' if boo__gta == 1 else ''))
        bpa__orvj.append(lhby__saypx)
        vtk__yykom[f'arr_type{i}'] = arr_typ
    bpa__orvj = ', '.join(bpa__orvj)
    hpxwn__ilmnz = 'def impl():\n'
    ponuq__oegji = bodo.hiframes.dataframe_impl._gen_init_df(hpxwn__ilmnz,
        toty.columns, bpa__orvj, index, vtk__yykom)
    df = context.compile_internal(builder, ponuq__oegji, toty(), [])
    return df


def _cast_df_data_to_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame to table format')
    boqxr__ryl = toty.table_type
    ytm__lbv = cgutils.create_struct_proxy(boqxr__ryl)(context, builder)
    ytm__lbv.parent = in_dataframe_payload.parent
    for yas__drfp, eorl__yabcg in boqxr__ryl.type_to_blk.items():
        lui__jmd = context.get_constant(types.int64, len(boqxr__ryl.
            block_to_arr_ind[eorl__yabcg]))
        lar__cid, jstfz__smj = ListInstance.allocate_ex(context, builder,
            types.List(yas__drfp), lui__jmd)
        jstfz__smj.size = lui__jmd
        setattr(ytm__lbv, f'block_{eorl__yabcg}', jstfz__smj.value)
    for i, yas__drfp in enumerate(fromty.data):
        mkd__lhit = toty.data[i]
        if yas__drfp != mkd__lhit:
            aeeb__innvb = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*aeeb__innvb)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        jewd__xfd = builder.extract_value(in_dataframe_payload.data, i)
        if yas__drfp != mkd__lhit:
            ugblm__sgio = context.cast(builder, jewd__xfd, yas__drfp, mkd__lhit
                )
            cftea__drz = False
        else:
            ugblm__sgio = jewd__xfd
            cftea__drz = True
        eorl__yabcg = boqxr__ryl.type_to_blk[yas__drfp]
        bvgvu__iiqzq = getattr(ytm__lbv, f'block_{eorl__yabcg}')
        exy__jzzip = ListInstance(context, builder, types.List(yas__drfp),
            bvgvu__iiqzq)
        rreep__rzlx = context.get_constant(types.int64, boqxr__ryl.
            block_offsets[i])
        exy__jzzip.setitem(rreep__rzlx, ugblm__sgio, cftea__drz)
    data_tup = context.make_tuple(builder, types.Tuple([boqxr__ryl]), [
        ytm__lbv._getvalue()])
    return data_tup


def _cast_df_data_keep_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame columns')
    vzy__foc = []
    for i in range(len(fromty.data)):
        if fromty.data[i] != toty.data[i]:
            aeeb__innvb = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*aeeb__innvb)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
            jewd__xfd = builder.extract_value(in_dataframe_payload.data, i)
            ugblm__sgio = context.cast(builder, jewd__xfd, fromty.data[i],
                toty.data[i])
            cftea__drz = False
        else:
            ugblm__sgio = builder.extract_value(in_dataframe_payload.data, i)
            cftea__drz = True
        if cftea__drz:
            context.nrt.incref(builder, toty.data[i], ugblm__sgio)
        vzy__foc.append(ugblm__sgio)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), vzy__foc)
    return data_tup


def _cast_df_data_keep_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting table format DataFrame columns')
    bmovc__usjy = fromty.table_type
    ypty__cwm = cgutils.create_struct_proxy(bmovc__usjy)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    iee__ksqvv = toty.table_type
    gxbt__ikohw = cgutils.create_struct_proxy(iee__ksqvv)(context, builder)
    gxbt__ikohw.parent = in_dataframe_payload.parent
    for yas__drfp, eorl__yabcg in iee__ksqvv.type_to_blk.items():
        lui__jmd = context.get_constant(types.int64, len(iee__ksqvv.
            block_to_arr_ind[eorl__yabcg]))
        lar__cid, jstfz__smj = ListInstance.allocate_ex(context, builder,
            types.List(yas__drfp), lui__jmd)
        jstfz__smj.size = lui__jmd
        setattr(gxbt__ikohw, f'block_{eorl__yabcg}', jstfz__smj.value)
    for i in range(len(fromty.data)):
        mlst__kdvx = fromty.data[i]
        mkd__lhit = toty.data[i]
        if mlst__kdvx != mkd__lhit:
            aeeb__innvb = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*aeeb__innvb)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        ulxqa__biba = bmovc__usjy.type_to_blk[mlst__kdvx]
        qdan__qxocx = getattr(ypty__cwm, f'block_{ulxqa__biba}')
        bxbv__yxtfh = ListInstance(context, builder, types.List(mlst__kdvx),
            qdan__qxocx)
        qggm__dpkc = context.get_constant(types.int64, bmovc__usjy.
            block_offsets[i])
        jewd__xfd = bxbv__yxtfh.getitem(qggm__dpkc)
        if mlst__kdvx != mkd__lhit:
            ugblm__sgio = context.cast(builder, jewd__xfd, mlst__kdvx,
                mkd__lhit)
            cftea__drz = False
        else:
            ugblm__sgio = jewd__xfd
            cftea__drz = True
        yazn__xbsd = iee__ksqvv.type_to_blk[yas__drfp]
        jstfz__smj = getattr(gxbt__ikohw, f'block_{yazn__xbsd}')
        ies__vvt = ListInstance(context, builder, types.List(mkd__lhit),
            jstfz__smj)
        rahiu__wumap = context.get_constant(types.int64, iee__ksqvv.
            block_offsets[i])
        ies__vvt.setitem(rahiu__wumap, ugblm__sgio, cftea__drz)
    data_tup = context.make_tuple(builder, types.Tuple([iee__ksqvv]), [
        gxbt__ikohw._getvalue()])
    return data_tup


def _cast_df_data_to_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(fromty,
        'casting table format to traditional DataFrame')
    boqxr__ryl = fromty.table_type
    ytm__lbv = cgutils.create_struct_proxy(boqxr__ryl)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    vzy__foc = []
    for i, yas__drfp in enumerate(toty.data):
        mlst__kdvx = fromty.data[i]
        if yas__drfp != mlst__kdvx:
            aeeb__innvb = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*aeeb__innvb)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        eorl__yabcg = boqxr__ryl.type_to_blk[yas__drfp]
        bvgvu__iiqzq = getattr(ytm__lbv, f'block_{eorl__yabcg}')
        exy__jzzip = ListInstance(context, builder, types.List(yas__drfp),
            bvgvu__iiqzq)
        rreep__rzlx = context.get_constant(types.int64, boqxr__ryl.
            block_offsets[i])
        jewd__xfd = exy__jzzip.getitem(rreep__rzlx)
        if yas__drfp != mlst__kdvx:
            ugblm__sgio = context.cast(builder, jewd__xfd, mlst__kdvx,
                yas__drfp)
            cftea__drz = False
        else:
            ugblm__sgio = jewd__xfd
            cftea__drz = True
        if cftea__drz:
            context.nrt.incref(builder, yas__drfp, ugblm__sgio)
        vzy__foc.append(ugblm__sgio)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), vzy__foc)
    return data_tup


@overload(pd.DataFrame, inline='always', no_unliteral=True)
def pd_dataframe_overload(data=None, index=None, columns=None, dtype=None,
    copy=False):
    if not is_overload_constant_bool(copy):
        raise BodoError(
            "pd.DataFrame(): 'copy' argument should be a constant boolean")
    copy = get_overload_const(copy)
    atv__kgwbe, bpa__orvj, index_arg = _get_df_args(data, index, columns,
        dtype, copy)
    xkcc__bvsd = gen_const_tup(atv__kgwbe)
    hpxwn__ilmnz = (
        'def _init_df(data=None, index=None, columns=None, dtype=None, copy=False):\n'
        )
    hpxwn__ilmnz += (
        '  return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, {}, {})\n'
        .format(bpa__orvj, index_arg, xkcc__bvsd))
    fsvb__dmbn = {}
    exec(hpxwn__ilmnz, {'bodo': bodo, 'np': np}, fsvb__dmbn)
    mxbwv__pzja = fsvb__dmbn['_init_df']
    return mxbwv__pzja


@intrinsic
def _tuple_to_table_format_decoded(typingctx, df_typ):
    assert not df_typ.is_table_format, '_tuple_to_table_format requires a tuple format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    qvae__acms = DataFrameType(to_str_arr_if_dict_array(df_typ.data),
        df_typ.index, df_typ.columns, dist=df_typ.dist, is_table_format=True)
    sig = signature(qvae__acms, df_typ)
    return sig, codegen


@intrinsic
def _table_to_tuple_format_decoded(typingctx, df_typ):
    assert df_typ.is_table_format, '_tuple_to_table_format requires a table format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    qvae__acms = DataFrameType(to_str_arr_if_dict_array(df_typ.data),
        df_typ.index, df_typ.columns, dist=df_typ.dist, is_table_format=False)
    sig = signature(qvae__acms, df_typ)
    return sig, codegen


def _get_df_args(data, index, columns, dtype, copy):
    git__xovjm = ''
    if not is_overload_none(dtype):
        git__xovjm = '.astype(dtype)'
    index_is_none = is_overload_none(index)
    index_arg = 'bodo.utils.conversion.convert_to_index(index)'
    if isinstance(data, types.BaseTuple):
        if not data.types[0] == types.StringLiteral('__bodo_tup'):
            raise BodoError('pd.DataFrame tuple input data not supported yet')
        assert len(data.types) % 2 == 1, 'invalid const dict tuple structure'
        wfk__dcmc = (len(data.types) - 1) // 2
        bseps__bozt = [yas__drfp.literal_value for yas__drfp in data.types[
            1:wfk__dcmc + 1]]
        data_val_types = dict(zip(bseps__bozt, data.types[wfk__dcmc + 1:]))
        vzy__foc = ['data[{}]'.format(i) for i in range(wfk__dcmc + 1, 2 *
            wfk__dcmc + 1)]
        data_dict = dict(zip(bseps__bozt, vzy__foc))
        if is_overload_none(index):
            for i, yas__drfp in enumerate(data.types[wfk__dcmc + 1:]):
                if isinstance(yas__drfp, SeriesType):
                    index_arg = (
                        'bodo.hiframes.pd_series_ext.get_series_index(data[{}])'
                        .format(wfk__dcmc + 1 + i))
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
        tld__khb = '.copy()' if copy else ''
        ityl__ism = get_overload_const_list(columns)
        wfk__dcmc = len(ityl__ism)
        data_val_types = {yzb__tus: data.copy(ndim=1) for yzb__tus in ityl__ism
            }
        vzy__foc = ['data[:,{}]{}'.format(i, tld__khb) for i in range(
            wfk__dcmc)]
        data_dict = dict(zip(ityl__ism, vzy__foc))
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
    bpa__orvj = '({},)'.format(', '.join(
        'bodo.utils.conversion.coerce_to_array({}, True, scalar_to_arr_len={}){}'
        .format(data_dict[yzb__tus], df_len, git__xovjm) for yzb__tus in
        col_names))
    if len(col_names) == 0:
        bpa__orvj = '()'
    return col_names, bpa__orvj, index_arg


def _get_df_len_from_info(data_dict, data_val_types, col_names,
    index_is_none, index_arg):
    df_len = '0'
    for yzb__tus in col_names:
        if yzb__tus in data_dict and is_iterable_type(data_val_types[yzb__tus]
            ):
            df_len = 'len({})'.format(data_dict[yzb__tus])
            break
    if df_len == '0' and not index_is_none:
        df_len = f'len({index_arg})'
    return df_len


def _fill_null_arrays(data_dict, col_names, df_len, dtype):
    if all(yzb__tus in data_dict for yzb__tus in col_names):
        return
    if is_overload_none(dtype):
        dtype = 'bodo.string_array_type'
    else:
        dtype = 'bodo.utils.conversion.array_type_from_dtype(dtype)'
    rmdt__ckyw = 'bodo.libs.array_kernels.gen_na_array({}, {})'.format(df_len,
        dtype)
    for yzb__tus in col_names:
        if yzb__tus not in data_dict:
            data_dict[yzb__tus] = rmdt__ckyw


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
            yas__drfp = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            return len(yas__drfp)
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
        qsgto__ovicw = idx.literal_value
        if isinstance(qsgto__ovicw, int):
            xaegu__ogqsr = tup.types[qsgto__ovicw]
        elif isinstance(qsgto__ovicw, slice):
            xaegu__ogqsr = types.BaseTuple.from_types(tup.types[qsgto__ovicw])
        return signature(xaegu__ogqsr, *args)


GetItemTuple.prefer_literal = True


@lower_builtin(operator.getitem, types.BaseTuple, types.IntegerLiteral)
@lower_builtin(operator.getitem, types.BaseTuple, types.SliceLiteral)
def getitem_tuple_lower(context, builder, sig, args):
    fkjsm__dxlx, idx = sig.args
    idx = idx.literal_value
    tup, lar__cid = args
    if isinstance(idx, int):
        if idx < 0:
            idx += len(fkjsm__dxlx)
        if not 0 <= idx < len(fkjsm__dxlx):
            raise IndexError('cannot index at %d in %s' % (idx, fkjsm__dxlx))
        uokfk__enksx = builder.extract_value(tup, idx)
    elif isinstance(idx, slice):
        hqa__mprcl = cgutils.unpack_tuple(builder, tup)[idx]
        uokfk__enksx = context.make_tuple(builder, sig.return_type, hqa__mprcl)
    else:
        raise NotImplementedError('unexpected index %r for %s' % (idx, sig.
            args[0]))
    return impl_ret_borrowed(context, builder, sig.return_type, uokfk__enksx)


def join_dummy(left_df, right_df, left_on, right_on, how, suffix_x,
    suffix_y, is_join, indicator, _bodo_na_equal, gen_cond):
    return left_df


@infer_global(join_dummy)
class JoinTyper(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        from bodo.utils.typing import is_overload_str
        assert not kws
        (left_df, right_df, left_on, right_on, zixkb__rxwr, suffix_x,
            suffix_y, is_join, indicator, lar__cid, lar__cid) = args
        left_on = get_overload_const_list(left_on)
        right_on = get_overload_const_list(right_on)
        fzk__bald = {yzb__tus: i for i, yzb__tus in enumerate(left_on)}
        bqib__luhz = {yzb__tus: i for i, yzb__tus in enumerate(right_on)}
        jxe__idjr = set(left_on) & set(right_on)
        kct__ipni = set(left_df.columns) & set(right_df.columns)
        ovmod__ivtq = kct__ipni - jxe__idjr
        vwkx__eei = '$_bodo_index_' in left_on
        zmnz__cfp = '$_bodo_index_' in right_on
        how = get_overload_const_str(zixkb__rxwr)
        fcvn__zjpz = how in {'left', 'outer'}
        vrc__jixh = how in {'right', 'outer'}
        columns = []
        data = []
        if vwkx__eei:
            lfgw__adcr = bodo.utils.typing.get_index_data_arr_types(left_df
                .index)[0]
        else:
            lfgw__adcr = left_df.data[left_df.column_index[left_on[0]]]
        if zmnz__cfp:
            klkk__umtj = bodo.utils.typing.get_index_data_arr_types(right_df
                .index)[0]
        else:
            klkk__umtj = right_df.data[right_df.column_index[right_on[0]]]
        if vwkx__eei and not zmnz__cfp and not is_join.literal_value:
            ylg__qjzu = right_on[0]
            if ylg__qjzu in left_df.column_index:
                columns.append(ylg__qjzu)
                if (klkk__umtj == bodo.dict_str_arr_type and lfgw__adcr ==
                    bodo.string_array_type):
                    glym__eztt = bodo.string_array_type
                else:
                    glym__eztt = klkk__umtj
                data.append(glym__eztt)
        if zmnz__cfp and not vwkx__eei and not is_join.literal_value:
            qtqc__gsadc = left_on[0]
            if qtqc__gsadc in right_df.column_index:
                columns.append(qtqc__gsadc)
                if (lfgw__adcr == bodo.dict_str_arr_type and klkk__umtj ==
                    bodo.string_array_type):
                    glym__eztt = bodo.string_array_type
                else:
                    glym__eztt = lfgw__adcr
                data.append(glym__eztt)
        for mlst__kdvx, tit__lqfvt in zip(left_df.data, left_df.columns):
            columns.append(str(tit__lqfvt) + suffix_x.literal_value if 
                tit__lqfvt in ovmod__ivtq else tit__lqfvt)
            if tit__lqfvt in jxe__idjr:
                if mlst__kdvx == bodo.dict_str_arr_type:
                    mlst__kdvx = right_df.data[right_df.column_index[
                        tit__lqfvt]]
                data.append(mlst__kdvx)
            else:
                if (mlst__kdvx == bodo.dict_str_arr_type and tit__lqfvt in
                    fzk__bald):
                    if zmnz__cfp:
                        mlst__kdvx = klkk__umtj
                    else:
                        lqr__goeu = fzk__bald[tit__lqfvt]
                        itp__rghi = right_on[lqr__goeu]
                        mlst__kdvx = right_df.data[right_df.column_index[
                            itp__rghi]]
                if vrc__jixh:
                    mlst__kdvx = to_nullable_type(mlst__kdvx)
                data.append(mlst__kdvx)
        for mlst__kdvx, tit__lqfvt in zip(right_df.data, right_df.columns):
            if tit__lqfvt not in jxe__idjr:
                columns.append(str(tit__lqfvt) + suffix_y.literal_value if 
                    tit__lqfvt in ovmod__ivtq else tit__lqfvt)
                if (mlst__kdvx == bodo.dict_str_arr_type and tit__lqfvt in
                    bqib__luhz):
                    if vwkx__eei:
                        mlst__kdvx = lfgw__adcr
                    else:
                        lqr__goeu = bqib__luhz[tit__lqfvt]
                        duk__ntey = left_on[lqr__goeu]
                        mlst__kdvx = left_df.data[left_df.column_index[
                            duk__ntey]]
                if fcvn__zjpz:
                    mlst__kdvx = to_nullable_type(mlst__kdvx)
                data.append(mlst__kdvx)
        yklzb__rpj = get_overload_const_bool(indicator)
        if yklzb__rpj:
            columns.append('_merge')
            data.append(bodo.CategoricalArrayType(bodo.PDCategoricalDtype((
                'left_only', 'right_only', 'both'), bodo.string_type, False)))
        index_typ = RangeIndexType(types.none)
        ahe__xys = False
        if vwkx__eei and zmnz__cfp and not is_overload_str(how, 'asof'):
            index_typ = left_df.index
            ahe__xys = True
        elif vwkx__eei and not zmnz__cfp:
            index_typ = right_df.index
            ahe__xys = True
        elif zmnz__cfp and not vwkx__eei:
            index_typ = left_df.index
            ahe__xys = True
        if ahe__xys and isinstance(index_typ, bodo.hiframes.pd_index_ext.
            RangeIndexType):
            index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64
                )
        hrrid__ont = DataFrameType(tuple(data), index_typ, tuple(columns))
        return signature(hrrid__ont, *args)


JoinTyper._no_unliteral = True


@lower_builtin(join_dummy, types.VarArg(types.Any))
def lower_join_dummy(context, builder, sig, args):
    xrzti__bzetz = cgutils.create_struct_proxy(sig.return_type)(context,
        builder)
    return xrzti__bzetz._getvalue()


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
    adj__cpae = dict(join=join, join_axes=join_axes, keys=keys, levels=
        levels, names=names, verify_integrity=verify_integrity, sort=sort,
        copy=copy)
    qcula__uxvl = dict(join='outer', join_axes=None, keys=None, levels=None,
        names=None, verify_integrity=False, sort=None, copy=True)
    check_unsupported_args('pandas.concat', adj__cpae, qcula__uxvl,
        package_name='pandas', module_name='General')
    hpxwn__ilmnz = """def impl(objs, axis=0, join='outer', join_axes=None, ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False, sort=None, copy=True):
"""
    if axis == 1:
        if not isinstance(objs, types.BaseTuple):
            raise_bodo_error(
                'Only tuple argument for pd.concat(axis=1) expected')
        index = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len(objs[0]), 1, None)'
            )
        afi__vwtba = 0
        bpa__orvj = []
        names = []
        for i, aualf__skbyj in enumerate(objs.types):
            assert isinstance(aualf__skbyj, (SeriesType, DataFrameType))
            check_runtime_cols_unsupported(aualf__skbyj, 'pandas.concat()')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                aualf__skbyj, 'pandas.concat()')
            if isinstance(aualf__skbyj, SeriesType):
                names.append(str(afi__vwtba))
                afi__vwtba += 1
                bpa__orvj.append(
                    'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'
                    .format(i))
            else:
                names.extend(aualf__skbyj.columns)
                for jjxpq__mnn in range(len(aualf__skbyj.data)):
                    bpa__orvj.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, jjxpq__mnn))
        return bodo.hiframes.dataframe_impl._gen_init_df(hpxwn__ilmnz,
            names, ', '.join(bpa__orvj), index)
    if axis != 0:
        raise_bodo_error('pd.concat(): axis must be 0 or 1')
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        DataFrameType):
        assert all(isinstance(yas__drfp, DataFrameType) for yas__drfp in
            objs.types)
        fels__pfsr = []
        for df in objs.types:
            check_runtime_cols_unsupported(df, 'pandas.concat()')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
                'pandas.concat()')
            fels__pfsr.extend(df.columns)
        fels__pfsr = list(dict.fromkeys(fels__pfsr).keys())
        kxvr__hoegj = {}
        for afi__vwtba, yzb__tus in enumerate(fels__pfsr):
            for i, df in enumerate(objs.types):
                if yzb__tus in df.column_index:
                    kxvr__hoegj[f'arr_typ{afi__vwtba}'] = df.data[df.
                        column_index[yzb__tus]]
                    break
        assert len(kxvr__hoegj) == len(fels__pfsr)
        ffdw__iazz = []
        for afi__vwtba, yzb__tus in enumerate(fels__pfsr):
            args = []
            for i, df in enumerate(objs.types):
                if yzb__tus in df.column_index:
                    ekflo__uoxy = df.column_index[yzb__tus]
                    args.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, ekflo__uoxy))
                else:
                    args.append(
                        'bodo.libs.array_kernels.gen_na_array(len(objs[{}]), arr_typ{})'
                        .format(i, afi__vwtba))
            hpxwn__ilmnz += ('  A{} = bodo.libs.array_kernels.concat(({},))\n'
                .format(afi__vwtba, ', '.join(args)))
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
        return bodo.hiframes.dataframe_impl._gen_init_df(hpxwn__ilmnz,
            fels__pfsr, ', '.join('A{}'.format(i) for i in range(len(
            fels__pfsr))), index, kxvr__hoegj)
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        SeriesType):
        assert all(isinstance(yas__drfp, SeriesType) for yas__drfp in objs.
            types)
        hpxwn__ilmnz += ('  out_arr = bodo.libs.array_kernels.concat(({},))\n'
            .format(', '.join(
            'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'.format(
            i) for i in range(len(objs.types)))))
        if ignore_index:
            hpxwn__ilmnz += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            hpxwn__ilmnz += (
                """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)))))
        hpxwn__ilmnz += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        fsvb__dmbn = {}
        exec(hpxwn__ilmnz, {'bodo': bodo, 'np': np, 'numba': numba}, fsvb__dmbn
            )
        return fsvb__dmbn['impl']
    if isinstance(objs, types.List) and isinstance(objs.dtype, DataFrameType):
        check_runtime_cols_unsupported(objs.dtype, 'pandas.concat()')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(objs.
            dtype, 'pandas.concat()')
        df_type = objs.dtype
        for afi__vwtba, yzb__tus in enumerate(df_type.columns):
            hpxwn__ilmnz += '  arrs{} = []\n'.format(afi__vwtba)
            hpxwn__ilmnz += '  for i in range(len(objs)):\n'
            hpxwn__ilmnz += '    df = objs[i]\n'
            hpxwn__ilmnz += (
                """    arrs{0}.append(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0}))
"""
                .format(afi__vwtba))
            hpxwn__ilmnz += (
                '  out_arr{0} = bodo.libs.array_kernels.concat(arrs{0})\n'.
                format(afi__vwtba))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr0), 1, None)'
                )
        else:
            hpxwn__ilmnz += '  arrs_index = []\n'
            hpxwn__ilmnz += '  for i in range(len(objs)):\n'
            hpxwn__ilmnz += '    df = objs[i]\n'
            hpxwn__ilmnz += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
            if objs.dtype.index.name_typ == types.none:
                name = None
            else:
                name = objs.dtype.index.name_typ.literal_value
            index = f"""bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index), {name!r})
"""
        return bodo.hiframes.dataframe_impl._gen_init_df(hpxwn__ilmnz,
            df_type.columns, ', '.join('out_arr{}'.format(i) for i in range
            (len(df_type.columns))), index)
    if isinstance(objs, types.List) and isinstance(objs.dtype, SeriesType):
        hpxwn__ilmnz += '  arrs = []\n'
        hpxwn__ilmnz += '  for i in range(len(objs)):\n'
        hpxwn__ilmnz += (
            '    arrs.append(bodo.hiframes.pd_series_ext.get_series_data(objs[i]))\n'
            )
        hpxwn__ilmnz += '  out_arr = bodo.libs.array_kernels.concat(arrs)\n'
        if ignore_index:
            hpxwn__ilmnz += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            hpxwn__ilmnz += '  arrs_index = []\n'
            hpxwn__ilmnz += '  for i in range(len(objs)):\n'
            hpxwn__ilmnz += '    S = objs[i]\n'
            hpxwn__ilmnz += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(S)))
"""
            hpxwn__ilmnz += """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index))
"""
        hpxwn__ilmnz += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        fsvb__dmbn = {}
        exec(hpxwn__ilmnz, {'bodo': bodo, 'np': np, 'numba': numba}, fsvb__dmbn
            )
        return fsvb__dmbn['impl']
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
        qvae__acms = df.copy(index=index, is_table_format=False)
        return signature(qvae__acms, *args)


SortDummyTyper._no_unliteral = True


@lower_builtin(sort_values_dummy, types.VarArg(types.Any))
def lower_sort_values_dummy(context, builder, sig, args):
    if sig.return_type == types.none:
        return
    yakoa__xfoxn = cgutils.create_struct_proxy(sig.return_type)(context,
        builder)
    return yakoa__xfoxn._getvalue()


@overload_method(DataFrameType, 'itertuples', inline='always', no_unliteral
    =True)
def itertuples_overload(df, index=True, name='Pandas'):
    check_runtime_cols_unsupported(df, 'DataFrame.itertuples()')
    adj__cpae = dict(index=index, name=name)
    qcula__uxvl = dict(index=True, name='Pandas')
    check_unsupported_args('DataFrame.itertuples', adj__cpae, qcula__uxvl,
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
        kxvr__hoegj = (types.Array(types.int64, 1, 'C'),) + df.data
        hhir__znyi = bodo.hiframes.dataframe_impl.DataFrameTupleIterator(
            columns, kxvr__hoegj)
        return signature(hhir__znyi, *args)


@lower_builtin(itertuples_dummy, types.VarArg(types.Any))
def lower_itertuples_dummy(context, builder, sig, args):
    yakoa__xfoxn = cgutils.create_struct_proxy(sig.return_type)(context,
        builder)
    return yakoa__xfoxn._getvalue()


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
    yakoa__xfoxn = cgutils.create_struct_proxy(sig.return_type)(context,
        builder)
    return yakoa__xfoxn._getvalue()


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
    yakoa__xfoxn = cgutils.create_struct_proxy(sig.return_type)(context,
        builder)
    return yakoa__xfoxn._getvalue()


@numba.generated_jit(nopython=True)
def pivot_impl(index_tup, columns_tup, values_tup, pivot_values,
    index_names, columns_name, value_names, check_duplicates=True, parallel
    =False):
    if not is_overload_constant_bool(check_duplicates):
        raise BodoError(
            'pivot_impl(): check_duplicates must be a constant boolean')
    mgk__uefx = get_overload_const_bool(check_duplicates)
    jcz__mya = not is_overload_none(value_names)
    mop__nzo = isinstance(values_tup, types.UniTuple)
    if mop__nzo:
        wwzh__hmgi = [to_nullable_type(values_tup.dtype)]
    else:
        wwzh__hmgi = [to_nullable_type(nijhf__qbcsr) for nijhf__qbcsr in
            values_tup]
    hpxwn__ilmnz = 'def impl(\n'
    hpxwn__ilmnz += """    index_tup, columns_tup, values_tup, pivot_values, index_names, columns_name, value_names, check_duplicates=True, parallel=False
"""
    hpxwn__ilmnz += '):\n'
    hpxwn__ilmnz += '    if parallel:\n'
    jokj__afk = ', '.join([f'array_to_info(index_tup[{i}])' for i in range(
        len(index_tup))] + [f'array_to_info(columns_tup[{i}])' for i in
        range(len(columns_tup))] + [f'array_to_info(values_tup[{i}])' for i in
        range(len(values_tup))])
    hpxwn__ilmnz += f'        info_list = [{jokj__afk}]\n'
    hpxwn__ilmnz += '        cpp_table = arr_info_list_to_table(info_list)\n'
    hpxwn__ilmnz += f"""        out_cpp_table = shuffle_table(cpp_table, {len(index_tup)}, parallel, 0)
"""
    lycmd__dcwac = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i}), index_tup[{i}])'
         for i in range(len(index_tup))])
    vbjgt__okfji = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup)}), columns_tup[{i}])'
         for i in range(len(columns_tup))])
    mojqa__hmz = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup) + len(columns_tup)}), values_tup[{i}])'
         for i in range(len(values_tup))])
    hpxwn__ilmnz += f'        index_tup = ({lycmd__dcwac},)\n'
    hpxwn__ilmnz += f'        columns_tup = ({vbjgt__okfji},)\n'
    hpxwn__ilmnz += f'        values_tup = ({mojqa__hmz},)\n'
    hpxwn__ilmnz += '        delete_table(cpp_table)\n'
    hpxwn__ilmnz += '        delete_table(out_cpp_table)\n'
    hpxwn__ilmnz += '    columns_arr = columns_tup[0]\n'
    if mop__nzo:
        hpxwn__ilmnz += '    values_arrs = [arr for arr in values_tup]\n'
    hpxwn__ilmnz += """    unique_index_arr_tup, row_vector = bodo.libs.array_ops.array_unique_vector_map(
"""
    hpxwn__ilmnz += '        index_tup\n'
    hpxwn__ilmnz += '    )\n'
    hpxwn__ilmnz += '    n_rows = len(unique_index_arr_tup[0])\n'
    hpxwn__ilmnz += '    num_values_arrays = len(values_tup)\n'
    hpxwn__ilmnz += '    n_unique_pivots = len(pivot_values)\n'
    if mop__nzo:
        hpxwn__ilmnz += '    n_cols = num_values_arrays * n_unique_pivots\n'
    else:
        hpxwn__ilmnz += '    n_cols = n_unique_pivots\n'
    hpxwn__ilmnz += '    col_map = {}\n'
    hpxwn__ilmnz += '    for i in range(n_unique_pivots):\n'
    hpxwn__ilmnz += (
        '        if bodo.libs.array_kernels.isna(pivot_values, i):\n')
    hpxwn__ilmnz += '            raise ValueError(\n'
    hpxwn__ilmnz += """                "DataFrame.pivot(): NA values in 'columns' array not supported\"
"""
    hpxwn__ilmnz += '            )\n'
    hpxwn__ilmnz += '        col_map[pivot_values[i]] = i\n'
    zti__jiha = False
    for i, mzam__gzso in enumerate(wwzh__hmgi):
        if is_str_arr_type(mzam__gzso):
            zti__jiha = True
            hpxwn__ilmnz += f"""    len_arrs_{i} = [np.zeros(n_rows, np.int64) for _ in range(n_cols)]
"""
            hpxwn__ilmnz += (
                f'    total_lens_{i} = np.zeros(n_cols, np.int64)\n')
    if zti__jiha:
        if mgk__uefx:
            hpxwn__ilmnz += '    nbytes = (n_rows + 7) >> 3\n'
            hpxwn__ilmnz += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
        hpxwn__ilmnz += '    for i in range(len(columns_arr)):\n'
        hpxwn__ilmnz += '        col_name = columns_arr[i]\n'
        hpxwn__ilmnz += '        pivot_idx = col_map[col_name]\n'
        hpxwn__ilmnz += '        row_idx = row_vector[i]\n'
        if mgk__uefx:
            hpxwn__ilmnz += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
            hpxwn__ilmnz += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
            hpxwn__ilmnz += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
            hpxwn__ilmnz += '        else:\n'
            hpxwn__ilmnz += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
        if mop__nzo:
            hpxwn__ilmnz += '        for j in range(num_values_arrays):\n'
            hpxwn__ilmnz += (
                '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
            hpxwn__ilmnz += '            len_arr = len_arrs_0[col_idx]\n'
            hpxwn__ilmnz += '            values_arr = values_arrs[j]\n'
            hpxwn__ilmnz += (
                '            if not bodo.libs.array_kernels.isna(values_arr, i):\n'
                )
            hpxwn__ilmnz += """                str_val_len = bodo.libs.str_arr_ext.get_str_arr_item_length(values_arr, i)
"""
            hpxwn__ilmnz += '                len_arr[row_idx] = str_val_len\n'
            hpxwn__ilmnz += (
                '                total_lens_0[col_idx] += str_val_len\n')
        else:
            for i, mzam__gzso in enumerate(wwzh__hmgi):
                if is_str_arr_type(mzam__gzso):
                    hpxwn__ilmnz += f"""        if not bodo.libs.array_kernels.isna(values_tup[{i}], i):
"""
                    hpxwn__ilmnz += f"""            str_val_len_{i} = bodo.libs.str_arr_ext.get_str_arr_item_length(values_tup[{i}], i)
"""
                    hpxwn__ilmnz += f"""            len_arrs_{i}[pivot_idx][row_idx] = str_val_len_{i}
"""
                    hpxwn__ilmnz += (
                        f'            total_lens_{i}[pivot_idx] += str_val_len_{i}\n'
                        )
    for i, mzam__gzso in enumerate(wwzh__hmgi):
        if is_str_arr_type(mzam__gzso):
            hpxwn__ilmnz += f'    data_arrs_{i} = [\n'
            hpxwn__ilmnz += (
                '        bodo.libs.str_arr_ext.gen_na_str_array_lens(\n')
            hpxwn__ilmnz += (
                f'            n_rows, total_lens_{i}[i], len_arrs_{i}[i]\n')
            hpxwn__ilmnz += '        )\n'
            hpxwn__ilmnz += '        for i in range(n_cols)\n'
            hpxwn__ilmnz += '    ]\n'
        else:
            hpxwn__ilmnz += f'    data_arrs_{i} = [\n'
            hpxwn__ilmnz += f"""        bodo.libs.array_kernels.gen_na_array(n_rows, data_arr_typ_{i})
"""
            hpxwn__ilmnz += '        for _ in range(n_cols)\n'
            hpxwn__ilmnz += '    ]\n'
    if not zti__jiha and mgk__uefx:
        hpxwn__ilmnz += '    nbytes = (n_rows + 7) >> 3\n'
        hpxwn__ilmnz += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
    hpxwn__ilmnz += '    for i in range(len(columns_arr)):\n'
    hpxwn__ilmnz += '        col_name = columns_arr[i]\n'
    hpxwn__ilmnz += '        pivot_idx = col_map[col_name]\n'
    hpxwn__ilmnz += '        row_idx = row_vector[i]\n'
    if not zti__jiha and mgk__uefx:
        hpxwn__ilmnz += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
        hpxwn__ilmnz += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
        hpxwn__ilmnz += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
        hpxwn__ilmnz += '        else:\n'
        hpxwn__ilmnz += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
    if mop__nzo:
        hpxwn__ilmnz += '        for j in range(num_values_arrays):\n'
        hpxwn__ilmnz += (
            '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
        hpxwn__ilmnz += '            col_arr = data_arrs_0[col_idx]\n'
        hpxwn__ilmnz += '            values_arr = values_arrs[j]\n'
        hpxwn__ilmnz += (
            '            if bodo.libs.array_kernels.isna(values_arr, i):\n')
        hpxwn__ilmnz += (
            '                bodo.libs.array_kernels.setna(col_arr, row_idx)\n'
            )
        hpxwn__ilmnz += '            else:\n'
        hpxwn__ilmnz += '                col_arr[row_idx] = values_arr[i]\n'
    else:
        for i, mzam__gzso in enumerate(wwzh__hmgi):
            hpxwn__ilmnz += f'        col_arr_{i} = data_arrs_{i}[pivot_idx]\n'
            hpxwn__ilmnz += (
                f'        if bodo.libs.array_kernels.isna(values_tup[{i}], i):\n'
                )
            hpxwn__ilmnz += (
                f'            bodo.libs.array_kernels.setna(col_arr_{i}, row_idx)\n'
                )
            hpxwn__ilmnz += f'        else:\n'
            hpxwn__ilmnz += (
                f'            col_arr_{i}[row_idx] = values_tup[{i}][i]\n')
    if len(index_tup) == 1:
        hpxwn__ilmnz += """    index = bodo.utils.conversion.index_from_array(unique_index_arr_tup[0], index_names[0])
"""
    else:
        hpxwn__ilmnz += """    index = bodo.hiframes.pd_multi_index_ext.init_multi_index(unique_index_arr_tup, index_names, None)
"""
    if jcz__mya:
        hpxwn__ilmnz += '    num_rows = len(value_names) * len(pivot_values)\n'
        if is_str_arr_type(value_names):
            hpxwn__ilmnz += '    total_chars = 0\n'
            hpxwn__ilmnz += '    for i in range(len(value_names)):\n'
            hpxwn__ilmnz += """        value_name_str_len = bodo.libs.str_arr_ext.get_str_arr_item_length(value_names, i)
"""
            hpxwn__ilmnz += '        total_chars += value_name_str_len\n'
            hpxwn__ilmnz += """    new_value_names = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(pivot_values))
"""
        else:
            hpxwn__ilmnz += """    new_value_names = bodo.utils.utils.alloc_type(num_rows, value_names, (-1,))
"""
        if is_str_arr_type(pivot_values):
            hpxwn__ilmnz += '    total_chars = 0\n'
            hpxwn__ilmnz += '    for i in range(len(pivot_values)):\n'
            hpxwn__ilmnz += """        pivot_val_str_len = bodo.libs.str_arr_ext.get_str_arr_item_length(pivot_values, i)
"""
            hpxwn__ilmnz += '        total_chars += pivot_val_str_len\n'
            hpxwn__ilmnz += """    new_pivot_values = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(value_names))
"""
        else:
            hpxwn__ilmnz += """    new_pivot_values = bodo.utils.utils.alloc_type(num_rows, pivot_values, (-1,))
"""
        hpxwn__ilmnz += '    for i in range(len(value_names)):\n'
        hpxwn__ilmnz += '        for j in range(len(pivot_values)):\n'
        hpxwn__ilmnz += """            new_value_names[(i * len(pivot_values)) + j] = value_names[i]
"""
        hpxwn__ilmnz += """            new_pivot_values[(i * len(pivot_values)) + j] = pivot_values[j]
"""
        hpxwn__ilmnz += """    column_index = bodo.hiframes.pd_multi_index_ext.init_multi_index((new_value_names, new_pivot_values), (None, columns_name), None)
"""
    else:
        hpxwn__ilmnz += """    column_index =  bodo.utils.conversion.index_from_array(pivot_values, columns_name)
"""
    hdwhq__oro = ', '.join(f'data_arrs_{i}' for i in range(len(wwzh__hmgi)))
    hpxwn__ilmnz += f"""    table = bodo.hiframes.table.init_runtime_table_from_lists(({hdwhq__oro},), n_rows)
"""
    hpxwn__ilmnz += (
        '    return bodo.hiframes.pd_dataframe_ext.init_runtime_cols_dataframe(\n'
        )
    hpxwn__ilmnz += '        (table,), index, column_index\n'
    hpxwn__ilmnz += '    )\n'
    fsvb__dmbn = {}
    jzg__zonw = {f'data_arr_typ_{i}': mzam__gzso for i, mzam__gzso in
        enumerate(wwzh__hmgi)}
    ijyxh__iaq = {'bodo': bodo, 'np': np, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'info_from_table': info_from_table, **jzg__zonw}
    exec(hpxwn__ilmnz, ijyxh__iaq, fsvb__dmbn)
    impl = fsvb__dmbn['impl']
    return impl


def gen_pandas_parquet_metadata(column_names, data_types, index,
    write_non_range_index_to_metadata, write_rangeindex_to_metadata,
    partition_cols=None, is_runtime_columns=False):
    espc__wrwj = {}
    espc__wrwj['columns'] = []
    if partition_cols is None:
        partition_cols = []
    for col_name, hbpt__haruv in zip(column_names, data_types):
        if col_name in partition_cols:
            continue
        rgvx__gtfy = None
        if isinstance(hbpt__haruv, bodo.DatetimeArrayType):
            mvzz__jdu = 'datetimetz'
            beuiq__msnqn = 'datetime64[ns]'
            if isinstance(hbpt__haruv.tz, int):
                emq__gowd = (bodo.libs.pd_datetime_arr_ext.
                    nanoseconds_to_offset(hbpt__haruv.tz))
            else:
                emq__gowd = pd.DatetimeTZDtype(tz=hbpt__haruv.tz).tz
            rgvx__gtfy = {'timezone': pa.lib.tzinfo_to_string(emq__gowd)}
        elif isinstance(hbpt__haruv, types.Array
            ) or hbpt__haruv == boolean_array:
            mvzz__jdu = beuiq__msnqn = hbpt__haruv.dtype.name
            if beuiq__msnqn.startswith('datetime'):
                mvzz__jdu = 'datetime'
        elif is_str_arr_type(hbpt__haruv):
            mvzz__jdu = 'unicode'
            beuiq__msnqn = 'object'
        elif hbpt__haruv == binary_array_type:
            mvzz__jdu = 'bytes'
            beuiq__msnqn = 'object'
        elif isinstance(hbpt__haruv, DecimalArrayType):
            mvzz__jdu = beuiq__msnqn = 'object'
        elif isinstance(hbpt__haruv, IntegerArrayType):
            yodr__tjgcw = hbpt__haruv.dtype.name
            if yodr__tjgcw.startswith('int'):
                mvzz__jdu = 'Int' + yodr__tjgcw[3:]
            elif yodr__tjgcw.startswith('uint'):
                mvzz__jdu = 'UInt' + yodr__tjgcw[4:]
            else:
                if is_runtime_columns:
                    col_name = 'Runtime determined column of type'
                raise BodoError(
                    'to_parquet(): unknown dtype in nullable Integer column {} {}'
                    .format(col_name, hbpt__haruv))
            beuiq__msnqn = hbpt__haruv.dtype.name
        elif hbpt__haruv == datetime_date_array_type:
            mvzz__jdu = 'datetime'
            beuiq__msnqn = 'object'
        elif isinstance(hbpt__haruv, (StructArrayType, ArrayItemArrayType)):
            mvzz__jdu = 'object'
            beuiq__msnqn = 'object'
        else:
            if is_runtime_columns:
                col_name = 'Runtime determined column of type'
            raise BodoError(
                'to_parquet(): unsupported column type for metadata generation : {} {}'
                .format(col_name, hbpt__haruv))
        skv__ztn = {'name': col_name, 'field_name': col_name, 'pandas_type':
            mvzz__jdu, 'numpy_type': beuiq__msnqn, 'metadata': rgvx__gtfy}
        espc__wrwj['columns'].append(skv__ztn)
    if write_non_range_index_to_metadata:
        if isinstance(index, MultiIndexType):
            raise BodoError('to_parquet: MultiIndex not supported yet')
        if 'none' in index.name:
            oewuj__svjcq = '__index_level_0__'
            pjip__pziy = None
        else:
            oewuj__svjcq = '%s'
            pjip__pziy = '%s'
        espc__wrwj['index_columns'] = [oewuj__svjcq]
        espc__wrwj['columns'].append({'name': pjip__pziy, 'field_name':
            oewuj__svjcq, 'pandas_type': index.pandas_type_name,
            'numpy_type': index.numpy_type_name, 'metadata': None})
    elif write_rangeindex_to_metadata:
        espc__wrwj['index_columns'] = [{'kind': 'range', 'name': '%s',
            'start': '%d', 'stop': '%d', 'step': '%d'}]
    else:
        espc__wrwj['index_columns'] = []
    espc__wrwj['pandas_version'] = pd.__version__
    return espc__wrwj


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
        pzjm__bmz = []
        for bfr__rllz in partition_cols:
            try:
                idx = df.columns.index(bfr__rllz)
            except ValueError as tpl__jhhj:
                raise BodoError(
                    f'Partition column {bfr__rllz} is not in dataframe')
            pzjm__bmz.append(idx)
    else:
        partition_cols = None
    if not is_overload_none(index) and not is_overload_constant_bool(index):
        raise BodoError('to_parquet(): index must be a constant bool or None')
    if not is_overload_int(row_group_size):
        raise BodoError('to_parquet(): row_group_size must be integer')
    from bodo.io.parquet_pio import parquet_write_table_cpp, parquet_write_table_partitioned_cpp
    ncm__zvxki = isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType
        )
    efcm__hzbj = df.index is not None and (is_overload_true(_is_parallel) or
        not is_overload_true(_is_parallel) and not ncm__zvxki)
    write_non_range_index_to_metadata = is_overload_true(index
        ) or is_overload_none(index) and (not ncm__zvxki or
        is_overload_true(_is_parallel))
    write_rangeindex_to_metadata = is_overload_none(index
        ) and ncm__zvxki and not is_overload_true(_is_parallel)
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
        hei__qfz = df.runtime_data_types
        ienw__fzkic = len(hei__qfz)
        rgvx__gtfy = gen_pandas_parquet_metadata([''] * ienw__fzkic,
            hei__qfz, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=True)
        tdh__fovkv = rgvx__gtfy['columns'][:ienw__fzkic]
        rgvx__gtfy['columns'] = rgvx__gtfy['columns'][ienw__fzkic:]
        tdh__fovkv = [json.dumps(ixzb__ckg).replace('""', '{0}') for
            ixzb__ckg in tdh__fovkv]
        dpuj__kkczx = json.dumps(rgvx__gtfy)
        aqpzt__wako = '"columns": ['
        sgkab__lldew = dpuj__kkczx.find(aqpzt__wako)
        if sgkab__lldew == -1:
            raise BodoError(
                'DataFrame.to_parquet(): Unexpected metadata string for runtime columns.  Please return the DataFrame to regular Python to update typing information.'
                )
        cutnv__kee = sgkab__lldew + len(aqpzt__wako)
        jlo__kcddz = dpuj__kkczx[:cutnv__kee]
        dpuj__kkczx = dpuj__kkczx[cutnv__kee:]
        jqb__prae = len(rgvx__gtfy['columns'])
    else:
        dpuj__kkczx = json.dumps(gen_pandas_parquet_metadata(df.columns, df
            .data, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=False))
    if not is_overload_true(_is_parallel) and ncm__zvxki:
        dpuj__kkczx = dpuj__kkczx.replace('"%d"', '%d')
        if df.index.name == 'RangeIndexType(none)':
            dpuj__kkczx = dpuj__kkczx.replace('"%s"', '%s')
    if not df.is_table_format:
        bpa__orvj = ', '.join(
            'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
            .format(i) for i in range(len(df.columns)))
    hpxwn__ilmnz = """def df_to_parquet(df, path, engine='auto', compression='snappy', index=None, partition_cols=None, storage_options=None, row_group_size=-1, _is_parallel=False):
"""
    if df.is_table_format:
        hpxwn__ilmnz += '    py_table = get_dataframe_table(df)\n'
        hpxwn__ilmnz += (
            '    table = py_table_to_cpp_table(py_table, py_table_typ)\n')
    else:
        hpxwn__ilmnz += '    info_list = [{}]\n'.format(bpa__orvj)
        hpxwn__ilmnz += '    table = arr_info_list_to_table(info_list)\n'
    if df.has_runtime_cols:
        hpxwn__ilmnz += '    columns_index = get_dataframe_column_names(df)\n'
        hpxwn__ilmnz += '    names_arr = index_to_array(columns_index)\n'
        hpxwn__ilmnz += '    col_names = array_to_info(names_arr)\n'
    else:
        hpxwn__ilmnz += '    col_names = array_to_info(col_names_arr)\n'
    if is_overload_true(index) or is_overload_none(index) and efcm__hzbj:
        hpxwn__ilmnz += """    index_col = array_to_info(index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
        xwsjc__bdabw = True
    else:
        hpxwn__ilmnz += '    index_col = array_to_info(np.empty(0))\n'
        xwsjc__bdabw = False
    if df.has_runtime_cols:
        hpxwn__ilmnz += '    columns_lst = []\n'
        hpxwn__ilmnz += '    num_cols = 0\n'
        for i in range(len(df.runtime_data_types)):
            hpxwn__ilmnz += f'    for _ in range(len(py_table.block_{i})):\n'
            hpxwn__ilmnz += f"""        columns_lst.append({tdh__fovkv[i]!r}.replace('{{0}}', '"' + names_arr[num_cols] + '"'))
"""
            hpxwn__ilmnz += '        num_cols += 1\n'
        if jqb__prae:
            hpxwn__ilmnz += "    columns_lst.append('')\n"
        hpxwn__ilmnz += '    columns_str = ", ".join(columns_lst)\n'
        hpxwn__ilmnz += ('    metadata = """' + jlo__kcddz +
            '""" + columns_str + """' + dpuj__kkczx + '"""\n')
    else:
        hpxwn__ilmnz += '    metadata = """' + dpuj__kkczx + '"""\n'
    hpxwn__ilmnz += '    if compression is None:\n'
    hpxwn__ilmnz += "        compression = 'none'\n"
    hpxwn__ilmnz += '    if df.index.name is not None:\n'
    hpxwn__ilmnz += '        name_ptr = df.index.name\n'
    hpxwn__ilmnz += '    else:\n'
    hpxwn__ilmnz += "        name_ptr = 'null'\n"
    hpxwn__ilmnz += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(path, parallel=_is_parallel)
"""
    dpx__lzacw = None
    if partition_cols:
        dpx__lzacw = pd.array([col_name for col_name in df.columns if 
            col_name not in partition_cols])
        htdce__cjbj = ', '.join(
            f'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype.categories.values)'
             for i in range(len(df.columns)) if isinstance(df.data[i],
            CategoricalArrayType) and i in pzjm__bmz)
        if htdce__cjbj:
            hpxwn__ilmnz += '    cat_info_list = [{}]\n'.format(htdce__cjbj)
            hpxwn__ilmnz += (
                '    cat_table = arr_info_list_to_table(cat_info_list)\n')
        else:
            hpxwn__ilmnz += '    cat_table = table\n'
        hpxwn__ilmnz += (
            '    col_names_no_partitions = array_to_info(col_names_no_parts_arr)\n'
            )
        hpxwn__ilmnz += (
            f'    part_cols_idxs = np.array({pzjm__bmz}, dtype=np.int32)\n')
        hpxwn__ilmnz += (
            '    parquet_write_table_partitioned_cpp(unicode_to_utf8(path),\n')
        hpxwn__ilmnz += """                            table, col_names, col_names_no_partitions, cat_table,
"""
        hpxwn__ilmnz += (
            '                            part_cols_idxs.ctypes, len(part_cols_idxs),\n'
            )
        hpxwn__ilmnz += (
            '                            unicode_to_utf8(compression),\n')
        hpxwn__ilmnz += '                            _is_parallel,\n'
        hpxwn__ilmnz += (
            '                            unicode_to_utf8(bucket_region),\n')
        hpxwn__ilmnz += '                            row_group_size)\n'
        hpxwn__ilmnz += '    delete_table_decref_arrays(table)\n'
        hpxwn__ilmnz += '    delete_info_decref_array(index_col)\n'
        hpxwn__ilmnz += (
            '    delete_info_decref_array(col_names_no_partitions)\n')
        hpxwn__ilmnz += '    delete_info_decref_array(col_names)\n'
        if htdce__cjbj:
            hpxwn__ilmnz += '    delete_table_decref_arrays(cat_table)\n'
    elif write_rangeindex_to_metadata:
        hpxwn__ilmnz += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        hpxwn__ilmnz += (
            '                            table, col_names, index_col,\n')
        hpxwn__ilmnz += '                            ' + str(xwsjc__bdabw
            ) + ',\n'
        hpxwn__ilmnz += (
            '                            unicode_to_utf8(metadata),\n')
        hpxwn__ilmnz += (
            '                            unicode_to_utf8(compression),\n')
        hpxwn__ilmnz += (
            '                            _is_parallel, 1, df.index.start,\n')
        hpxwn__ilmnz += (
            '                            df.index.stop, df.index.step,\n')
        hpxwn__ilmnz += (
            '                            unicode_to_utf8(name_ptr),\n')
        hpxwn__ilmnz += (
            '                            unicode_to_utf8(bucket_region),\n')
        hpxwn__ilmnz += '                            row_group_size)\n'
        hpxwn__ilmnz += '    delete_table_decref_arrays(table)\n'
        hpxwn__ilmnz += '    delete_info_decref_array(index_col)\n'
        hpxwn__ilmnz += '    delete_info_decref_array(col_names)\n'
    else:
        hpxwn__ilmnz += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        hpxwn__ilmnz += (
            '                            table, col_names, index_col,\n')
        hpxwn__ilmnz += '                            ' + str(xwsjc__bdabw
            ) + ',\n'
        hpxwn__ilmnz += (
            '                            unicode_to_utf8(metadata),\n')
        hpxwn__ilmnz += (
            '                            unicode_to_utf8(compression),\n')
        hpxwn__ilmnz += (
            '                            _is_parallel, 0, 0, 0, 0,\n')
        hpxwn__ilmnz += (
            '                            unicode_to_utf8(name_ptr),\n')
        hpxwn__ilmnz += (
            '                            unicode_to_utf8(bucket_region),\n')
        hpxwn__ilmnz += '                            row_group_size)\n'
        hpxwn__ilmnz += '    delete_table_decref_arrays(table)\n'
        hpxwn__ilmnz += '    delete_info_decref_array(index_col)\n'
        hpxwn__ilmnz += '    delete_info_decref_array(col_names)\n'
    fsvb__dmbn = {}
    if df.has_runtime_cols:
        mao__mcc = None
    else:
        for tit__lqfvt in df.columns:
            if not isinstance(tit__lqfvt, str):
                raise BodoError(
                    'DataFrame.to_parquet(): parquet must have string column names'
                    )
        mao__mcc = pd.array(df.columns)
    exec(hpxwn__ilmnz, {'np': np, 'bodo': bodo, 'unicode_to_utf8':
        unicode_to_utf8, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'str_arr_from_sequence': str_arr_from_sequence,
        'parquet_write_table_cpp': parquet_write_table_cpp,
        'parquet_write_table_partitioned_cpp':
        parquet_write_table_partitioned_cpp, 'index_to_array':
        index_to_array, 'delete_info_decref_array':
        delete_info_decref_array, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'col_names_arr': mao__mcc,
        'py_table_to_cpp_table': py_table_to_cpp_table, 'py_table_typ': df.
        table_type, 'get_dataframe_table': get_dataframe_table,
        'col_names_no_parts_arr': dpx__lzacw, 'get_dataframe_column_names':
        get_dataframe_column_names, 'fix_arr_dtype': fix_arr_dtype,
        'decode_if_dict_array': decode_if_dict_array,
        'decode_if_dict_table': decode_if_dict_table}, fsvb__dmbn)
    nbgg__cpr = fsvb__dmbn['df_to_parquet']
    return nbgg__cpr


def to_sql_exception_guard(df, name, con, schema=None, if_exists='fail',
    index=True, index_label=None, chunksize=None, dtype=None, method=None,
    _is_table_create=False, _is_parallel=False):
    yxt__jtslu = 'all_ok'
    nktq__nea, rhi__jqeua = bodo.ir.sql_ext.parse_dbtype(con)
    if _is_parallel and bodo.get_rank() == 0:
        rlmav__wli = 100
        if chunksize is None:
            wjp__vfia = rlmav__wli
        else:
            wjp__vfia = min(chunksize, rlmav__wli)
        if _is_table_create:
            df = df.iloc[:wjp__vfia, :]
        else:
            df = df.iloc[wjp__vfia:, :]
            if len(df) == 0:
                return yxt__jtslu
    hjcif__qngeb = df.columns
    try:
        if nktq__nea == 'snowflake':
            if rhi__jqeua and con.count(rhi__jqeua) == 1:
                con = con.replace(rhi__jqeua, quote(rhi__jqeua))
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
                df.columns = [(yzb__tus.upper() if yzb__tus.islower() else
                    yzb__tus) for yzb__tus in df.columns]
            except ImportError as tpl__jhhj:
                yxt__jtslu = (
                    "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires both snowflake-sqlalchemy and snowflake-connector-python. These can be installed by calling 'conda install -c conda-forge snowflake-sqlalchemy snowflake-connector-python' or 'pip install snowflake-sqlalchemy snowflake-connector-python'."
                    )
                return yxt__jtslu
        if nktq__nea == 'oracle':
            import sqlalchemy as sa
            jlo__rvy = bodo.typeof(df)
            nhv__pzdlr = {}
            for yzb__tus, zaez__jkql in zip(jlo__rvy.columns, jlo__rvy.data):
                if df[yzb__tus].dtype == 'object':
                    if zaez__jkql == datetime_date_array_type:
                        nhv__pzdlr[yzb__tus] = sa.types.Date
                    elif zaez__jkql == bodo.string_array_type:
                        nhv__pzdlr[yzb__tus] = sa.types.VARCHAR(df[yzb__tus
                            ].str.len().max())
            dtype = nhv__pzdlr
        try:
            df.to_sql(name, con, schema, if_exists, index, index_label,
                chunksize, dtype, method)
        except Exception as axy__wou:
            yxt__jtslu = axy__wou.args[0]
        return yxt__jtslu
    finally:
        df.columns = hjcif__qngeb


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
        otb__yatuj = bodo.libs.distributed_api.get_rank()
        yxt__jtslu = 'unset'
        if otb__yatuj != 0:
            yxt__jtslu = bcast_scalar(yxt__jtslu)
        elif otb__yatuj == 0:
            yxt__jtslu = to_sql_exception_guard_encaps(df, name, con,
                schema, if_exists, index, index_label, chunksize, dtype,
                method, True, _is_parallel)
            yxt__jtslu = bcast_scalar(yxt__jtslu)
        if_exists = 'append'
        if _is_parallel and yxt__jtslu == 'all_ok':
            yxt__jtslu = to_sql_exception_guard_encaps(df, name, con,
                schema, if_exists, index, index_label, chunksize, dtype,
                method, False, _is_parallel)
        if yxt__jtslu != 'all_ok':
            print('err_msg=', yxt__jtslu)
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
        eifxp__iqnot = get_overload_const_str(path_or_buf)
        if eifxp__iqnot.endswith(('.gz', '.bz2', '.zip', '.xz')):
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
        pwdd__mmaro = bodo.io.fs_io.get_s3_bucket_region_njit(path_or_buf,
            parallel=False)
        if lines and orient == 'records':
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, True,
                unicode_to_utf8(pwdd__mmaro))
            bodo.utils.utils.check_and_propagate_cpp_exception()
        else:
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, False,
                unicode_to_utf8(pwdd__mmaro))
            bodo.utils.utils.check_and_propagate_cpp_exception()
    return _impl


@overload(pd.get_dummies, inline='always', no_unliteral=True)
def get_dummies(data, prefix=None, prefix_sep='_', dummy_na=False, columns=
    None, sparse=False, drop_first=False, dtype=None):
    ttxum__ggvf = {'prefix': prefix, 'prefix_sep': prefix_sep, 'dummy_na':
        dummy_na, 'columns': columns, 'sparse': sparse, 'drop_first':
        drop_first, 'dtype': dtype}
    poqt__ccm = {'prefix': None, 'prefix_sep': '_', 'dummy_na': False,
        'columns': None, 'sparse': False, 'drop_first': False, 'dtype': None}
    check_unsupported_args('pandas.get_dummies', ttxum__ggvf, poqt__ccm,
        package_name='pandas', module_name='General')
    if not categorical_can_construct_dataframe(data):
        raise BodoError(
            'pandas.get_dummies() only support categorical data types with explicitly known categories'
            )
    hpxwn__ilmnz = """def impl(data, prefix=None, prefix_sep='_', dummy_na=False, columns=None, sparse=False, drop_first=False, dtype=None,):
"""
    if isinstance(data, SeriesType):
        kzh__chat = data.data.dtype.categories
        hpxwn__ilmnz += (
            '  data_values = bodo.hiframes.pd_series_ext.get_series_data(data)\n'
            )
    else:
        kzh__chat = data.dtype.categories
        hpxwn__ilmnz += '  data_values = data\n'
    wfk__dcmc = len(kzh__chat)
    hpxwn__ilmnz += """  codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(data_values)
"""
    hpxwn__ilmnz += '  numba.parfors.parfor.init_prange()\n'
    hpxwn__ilmnz += '  n = len(data_values)\n'
    for i in range(wfk__dcmc):
        hpxwn__ilmnz += '  data_arr_{} = np.empty(n, np.uint8)\n'.format(i)
    hpxwn__ilmnz += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    hpxwn__ilmnz += '      if bodo.libs.array_kernels.isna(data_values, i):\n'
    for jjxpq__mnn in range(wfk__dcmc):
        hpxwn__ilmnz += '          data_arr_{}[i] = 0\n'.format(jjxpq__mnn)
    hpxwn__ilmnz += '      else:\n'
    for cngzd__kgtk in range(wfk__dcmc):
        hpxwn__ilmnz += '          data_arr_{0}[i] = codes[i] == {0}\n'.format(
            cngzd__kgtk)
    bpa__orvj = ', '.join(f'data_arr_{i}' for i in range(wfk__dcmc))
    index = 'bodo.hiframes.pd_index_ext.init_range_index(0, n, 1, None)'
    if isinstance(kzh__chat[0], np.datetime64):
        kzh__chat = tuple(pd.Timestamp(yzb__tus) for yzb__tus in kzh__chat)
    elif isinstance(kzh__chat[0], np.timedelta64):
        kzh__chat = tuple(pd.Timedelta(yzb__tus) for yzb__tus in kzh__chat)
    return bodo.hiframes.dataframe_impl._gen_init_df(hpxwn__ilmnz,
        kzh__chat, bpa__orvj, index)


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
    for asr__qvhrl in pd_unsupported:
        zqi__imn = mod_name + '.' + asr__qvhrl.__name__
        overload(asr__qvhrl, no_unliteral=True)(create_unsupported_overload
            (zqi__imn))


def _install_dataframe_unsupported():
    for jxlhh__yvw in dataframe_unsupported_attrs:
        nhr__hyzml = 'DataFrame.' + jxlhh__yvw
        overload_attribute(DataFrameType, jxlhh__yvw)(
            create_unsupported_overload(nhr__hyzml))
    for zqi__imn in dataframe_unsupported:
        nhr__hyzml = 'DataFrame.' + zqi__imn + '()'
        overload_method(DataFrameType, zqi__imn)(create_unsupported_overload
            (nhr__hyzml))


_install_pd_unsupported('pandas', pd_unsupported)
_install_pd_unsupported('pandas.util', pd_util_unsupported)
_install_dataframe_unsupported()
