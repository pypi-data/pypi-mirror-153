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
            pywxf__rof = f'{len(self.data)} columns of types {set(self.data)}'
            lch__quygi = (
                f"('{self.columns[0]}', '{self.columns[1]}', ..., '{self.columns[-1]}')"
                )
            return (
                f'dataframe({pywxf__rof}, {self.index}, {lch__quygi}, {self.dist}, {self.is_table_format})'
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
        return {qmal__nutcm: i for i, qmal__nutcm in enumerate(self.columns)}

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
            mucga__oozhs = (self.index if self.index == other.index else
                self.index.unify(typingctx, other.index))
            data = tuple(svcn__mkz.unify(typingctx, lcmq__rks) if svcn__mkz !=
                lcmq__rks else svcn__mkz for svcn__mkz, lcmq__rks in zip(
                self.data, other.data))
            dist = Distribution(min(self.dist.value, other.dist.value))
            if mucga__oozhs is not None and None not in data:
                return DataFrameType(data, mucga__oozhs, self.columns, dist,
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
        return all(svcn__mkz.is_precise() for svcn__mkz in self.data
            ) and self.index.is_precise()

    def replace_col_type(self, col_name, new_type):
        if col_name not in self.columns:
            raise ValueError(
                f"DataFrameType.replace_col_type replaced column must be found in the DataFrameType. '{col_name}' not found in DataFrameType with columns {self.columns}"
                )
        smvuv__jmh = self.columns.index(col_name)
        ahej__dmugg = tuple(list(self.data[:smvuv__jmh]) + [new_type] +
            list(self.data[smvuv__jmh + 1:]))
        return DataFrameType(ahej__dmugg, self.index, self.columns, self.
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
        yizgh__kjwom = [('data', data_typ), ('index', fe_type.df_type.index
            ), ('parent', types.pyobject)]
        if fe_type.df_type.has_runtime_cols:
            yizgh__kjwom.append(('columns', fe_type.df_type.
                runtime_colname_typ))
        super(DataFramePayloadModel, self).__init__(dmm, fe_type, yizgh__kjwom)


@register_model(DataFrameType)
class DataFrameModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = DataFramePayloadType(fe_type)
        yizgh__kjwom = [('meminfo', types.MemInfoPointer(payload_type)), (
            'parent', types.pyobject)]
        super(DataFrameModel, self).__init__(dmm, fe_type, yizgh__kjwom)


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
        wgck__behsz = 'n',
        gpid__sbvrc = {'n': 5}
        bbujq__ejzy, nqk__udr = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, wgck__behsz, gpid__sbvrc)
        wzw__jop = nqk__udr[0]
        if not is_overload_int(wzw__jop):
            raise BodoError(f"{func_name}(): 'n' must be an Integer")
        ijrvs__qvf = df.copy(is_table_format=False)
        return ijrvs__qvf(*nqk__udr).replace(pysig=bbujq__ejzy)

    @bound_function('df.corr')
    def resolve_corr(self, df, args, kws):
        func_name = 'DataFrame.corr'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        gem__ktfmb = (df,) + args
        wgck__behsz = 'df', 'method', 'min_periods'
        gpid__sbvrc = {'method': 'pearson', 'min_periods': 1}
        crrj__daui = 'method',
        bbujq__ejzy, nqk__udr = bodo.utils.typing.fold_typing_args(func_name,
            gem__ktfmb, kws, wgck__behsz, gpid__sbvrc, crrj__daui)
        euee__bmv = nqk__udr[2]
        if not is_overload_int(euee__bmv):
            raise BodoError(f"{func_name}(): 'min_periods' must be an Integer")
        uehj__alv = []
        rfxes__ktp = []
        for qmal__nutcm, aqwks__ayjz in zip(df.columns, df.data):
            if bodo.utils.typing._is_pandas_numeric_dtype(aqwks__ayjz.dtype):
                uehj__alv.append(qmal__nutcm)
                rfxes__ktp.append(types.Array(types.float64, 1, 'A'))
        if len(uehj__alv) == 0:
            raise_bodo_error('DataFrame.corr(): requires non-empty dataframe')
        rfxes__ktp = tuple(rfxes__ktp)
        uehj__alv = tuple(uehj__alv)
        index_typ = bodo.utils.typing.type_col_to_index(uehj__alv)
        ijrvs__qvf = DataFrameType(rfxes__ktp, index_typ, uehj__alv)
        return ijrvs__qvf(*nqk__udr).replace(pysig=bbujq__ejzy)

    @bound_function('df.pipe', no_unliteral=True)
    def resolve_pipe(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.pipe()')
        return bodo.hiframes.pd_groupby_ext.resolve_obj_pipe(self, df, args,
            kws, 'DataFrame')

    @bound_function('df.apply', no_unliteral=True)
    def resolve_apply(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.apply()')
        kws = dict(kws)
        son__rayku = args[0] if len(args) > 0 else kws.pop('func', None)
        axis = args[1] if len(args) > 1 else kws.pop('axis', types.literal(0))
        psfme__ywjyq = args[2] if len(args) > 2 else kws.pop('raw', types.
            literal(False))
        irbtq__auym = args[3] if len(args) > 3 else kws.pop('result_type',
            types.none)
        mic__hawf = args[4] if len(args) > 4 else kws.pop('args', types.
            Tuple([]))
        lscll__dkgie = dict(raw=psfme__ywjyq, result_type=irbtq__auym)
        vnw__ybq = dict(raw=False, result_type=None)
        check_unsupported_args('Dataframe.apply', lscll__dkgie, vnw__ybq,
            package_name='pandas', module_name='DataFrame')
        ozfsf__uomyd = True
        if types.unliteral(son__rayku) == types.unicode_type:
            if not is_overload_constant_str(son__rayku):
                raise BodoError(
                    f'DataFrame.apply(): string argument (for builtins) must be a compile time constant'
                    )
            ozfsf__uomyd = False
        if not is_overload_constant_int(axis):
            raise BodoError(
                'Dataframe.apply(): axis argument must be a compile time constant.'
                )
        cmbg__czej = get_overload_const_int(axis)
        if ozfsf__uomyd and cmbg__czej != 1:
            raise BodoError(
                'Dataframe.apply(): only axis=1 supported for user-defined functions'
                )
        elif cmbg__czej not in (0, 1):
            raise BodoError('Dataframe.apply(): axis must be either 0 or 1')
        kwvlz__vla = []
        for arr_typ in df.data:
            mbqb__llwp = SeriesType(arr_typ.dtype, arr_typ, df.index,
                string_type)
            xuz__zavxw = self.context.resolve_function_type(operator.
                getitem, (SeriesIlocType(mbqb__llwp), types.int64), {}
                ).return_type
            kwvlz__vla.append(xuz__zavxw)
        edh__ngc = types.none
        gzgh__jza = HeterogeneousIndexType(types.BaseTuple.from_types(tuple
            (types.literal(qmal__nutcm) for qmal__nutcm in df.columns)), None)
        embo__kxs = types.BaseTuple.from_types(kwvlz__vla)
        lewq__qqdfu = types.Tuple([types.bool_] * len(embo__kxs))
        bauv__ebrrf = bodo.NullableTupleType(embo__kxs, lewq__qqdfu)
        pfu__uswxl = df.index.dtype
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df.index,
            'DataFrame.apply()')
        if pfu__uswxl == types.NPDatetime('ns'):
            pfu__uswxl = bodo.pd_timestamp_type
        if pfu__uswxl == types.NPTimedelta('ns'):
            pfu__uswxl = bodo.pd_timedelta_type
        if is_heterogeneous_tuple_type(embo__kxs):
            eypru__zng = HeterogeneousSeriesType(bauv__ebrrf, gzgh__jza,
                pfu__uswxl)
        else:
            eypru__zng = SeriesType(embo__kxs.dtype, bauv__ebrrf, gzgh__jza,
                pfu__uswxl)
        rfu__jhdlw = eypru__zng,
        if mic__hawf is not None:
            rfu__jhdlw += tuple(mic__hawf.types)
        try:
            if not ozfsf__uomyd:
                sxu__jhymj = bodo.utils.transform.get_udf_str_return_type(df,
                    get_overload_const_str(son__rayku), self.context,
                    'DataFrame.apply', axis if cmbg__czej == 1 else None)
            else:
                sxu__jhymj = get_const_func_output_type(son__rayku,
                    rfu__jhdlw, kws, self.context, numba.core.registry.
                    cpu_target.target_context)
        except Exception as mbzpy__iubis:
            raise_bodo_error(get_udf_error_msg('DataFrame.apply()',
                mbzpy__iubis))
        if ozfsf__uomyd:
            if not (is_overload_constant_int(axis) and 
                get_overload_const_int(axis) == 1):
                raise BodoError(
                    'Dataframe.apply(): only user-defined functions with axis=1 supported'
                    )
            if isinstance(sxu__jhymj, (SeriesType, HeterogeneousSeriesType)
                ) and sxu__jhymj.const_info is None:
                raise BodoError(
                    'Invalid Series output in UDF (Series with constant length and constant Index value expected)'
                    )
            if isinstance(sxu__jhymj, HeterogeneousSeriesType):
                ycsdl__wgot, ptyz__bamk = sxu__jhymj.const_info
                if isinstance(sxu__jhymj.data, bodo.libs.nullable_tuple_ext
                    .NullableTupleType):
                    ctnj__lwq = sxu__jhymj.data.tuple_typ.types
                elif isinstance(sxu__jhymj.data, types.Tuple):
                    ctnj__lwq = sxu__jhymj.data.types
                else:
                    raise_bodo_error(
                        'df.apply(): Unexpected Series return type for Heterogeneous data'
                        )
                mft__tlas = tuple(to_nullable_type(dtype_to_array_type(
                    tjo__lpnf)) for tjo__lpnf in ctnj__lwq)
                sdpqm__mwi = DataFrameType(mft__tlas, df.index, ptyz__bamk)
            elif isinstance(sxu__jhymj, SeriesType):
                uvw__eyln, ptyz__bamk = sxu__jhymj.const_info
                mft__tlas = tuple(to_nullable_type(dtype_to_array_type(
                    sxu__jhymj.dtype)) for ycsdl__wgot in range(uvw__eyln))
                sdpqm__mwi = DataFrameType(mft__tlas, df.index, ptyz__bamk)
            else:
                wze__mvocu = get_udf_out_arr_type(sxu__jhymj)
                sdpqm__mwi = SeriesType(wze__mvocu.dtype, wze__mvocu, df.
                    index, None)
        else:
            sdpqm__mwi = sxu__jhymj
        kae__qaz = ', '.join("{} = ''".format(svcn__mkz) for svcn__mkz in
            kws.keys())
        squbx__opjt = f"""def apply_stub(func, axis=0, raw=False, result_type=None, args=(), {kae__qaz}):
"""
        squbx__opjt += '    pass\n'
        qmlq__zptb = {}
        exec(squbx__opjt, {}, qmlq__zptb)
        dxjy__qmjqs = qmlq__zptb['apply_stub']
        bbujq__ejzy = numba.core.utils.pysignature(dxjy__qmjqs)
        qtt__poe = (son__rayku, axis, psfme__ywjyq, irbtq__auym, mic__hawf
            ) + tuple(kws.values())
        return signature(sdpqm__mwi, *qtt__poe).replace(pysig=bbujq__ejzy)

    @bound_function('df.plot', no_unliteral=True)
    def resolve_plot(self, df, args, kws):
        func_name = 'DataFrame.plot'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        wgck__behsz = ('x', 'y', 'kind', 'figsize', 'ax', 'subplots',
            'sharex', 'sharey', 'layout', 'use_index', 'title', 'grid',
            'legend', 'style', 'logx', 'logy', 'loglog', 'xticks', 'yticks',
            'xlim', 'ylim', 'rot', 'fontsize', 'colormap', 'table', 'yerr',
            'xerr', 'secondary_y', 'sort_columns', 'xlabel', 'ylabel',
            'position', 'stacked', 'mark_right', 'include_bool', 'backend')
        gpid__sbvrc = {'x': None, 'y': None, 'kind': 'line', 'figsize':
            None, 'ax': None, 'subplots': False, 'sharex': None, 'sharey': 
            False, 'layout': None, 'use_index': True, 'title': None, 'grid':
            None, 'legend': True, 'style': None, 'logx': False, 'logy': 
            False, 'loglog': False, 'xticks': None, 'yticks': None, 'xlim':
            None, 'ylim': None, 'rot': None, 'fontsize': None, 'colormap':
            None, 'table': False, 'yerr': None, 'xerr': None, 'secondary_y':
            False, 'sort_columns': False, 'xlabel': None, 'ylabel': None,
            'position': 0.5, 'stacked': False, 'mark_right': True,
            'include_bool': False, 'backend': None}
        crrj__daui = ('subplots', 'sharex', 'sharey', 'layout', 'use_index',
            'grid', 'style', 'logx', 'logy', 'loglog', 'xlim', 'ylim',
            'rot', 'colormap', 'table', 'yerr', 'xerr', 'sort_columns',
            'secondary_y', 'colorbar', 'position', 'stacked', 'mark_right',
            'include_bool', 'backend')
        bbujq__ejzy, nqk__udr = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, wgck__behsz, gpid__sbvrc, crrj__daui)
        dxps__uqgp = nqk__udr[2]
        if not is_overload_constant_str(dxps__uqgp):
            raise BodoError(
                f"{func_name}: kind must be a constant string and one of ('line', 'scatter')."
                )
        xxdix__let = nqk__udr[0]
        if not is_overload_none(xxdix__let) and not (is_overload_int(
            xxdix__let) or is_overload_constant_str(xxdix__let)):
            raise BodoError(
                f'{func_name}: x must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(xxdix__let):
            hgxx__yolxp = get_overload_const_str(xxdix__let)
            if hgxx__yolxp not in df.columns:
                raise BodoError(f'{func_name}: {hgxx__yolxp} column not found.'
                    )
        elif is_overload_int(xxdix__let):
            xjej__cyqp = get_overload_const_int(xxdix__let)
            if xjej__cyqp > len(df.columns):
                raise BodoError(
                    f'{func_name}: x: {xjej__cyqp} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            xxdix__let = df.columns[xxdix__let]
        qqgti__uqg = nqk__udr[1]
        if not is_overload_none(qqgti__uqg) and not (is_overload_int(
            qqgti__uqg) or is_overload_constant_str(qqgti__uqg)):
            raise BodoError(
                'df.plot(): y must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(qqgti__uqg):
            xbge__hws = get_overload_const_str(qqgti__uqg)
            if xbge__hws not in df.columns:
                raise BodoError(f'{func_name}: {xbge__hws} column not found.')
        elif is_overload_int(qqgti__uqg):
            ogx__obzjg = get_overload_const_int(qqgti__uqg)
            if ogx__obzjg > len(df.columns):
                raise BodoError(
                    f'{func_name}: y: {ogx__obzjg} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            qqgti__uqg = df.columns[qqgti__uqg]
        wcg__yae = nqk__udr[3]
        if not is_overload_none(wcg__yae) and not is_tuple_like_type(wcg__yae):
            raise BodoError(
                f'{func_name}: figsize must be a constant numeric tuple (width, height) or None.'
                )
        iojn__dwho = nqk__udr[10]
        if not is_overload_none(iojn__dwho) and not is_overload_constant_str(
            iojn__dwho):
            raise BodoError(
                f'{func_name}: title must be a constant string or None.')
        exzo__liahd = nqk__udr[12]
        if not is_overload_bool(exzo__liahd):
            raise BodoError(f'{func_name}: legend must be a boolean type.')
        xnx__nfvq = nqk__udr[17]
        if not is_overload_none(xnx__nfvq) and not is_tuple_like_type(xnx__nfvq
            ):
            raise BodoError(
                f'{func_name}: xticks must be a constant tuple or None.')
        wajg__srl = nqk__udr[18]
        if not is_overload_none(wajg__srl) and not is_tuple_like_type(wajg__srl
            ):
            raise BodoError(
                f'{func_name}: yticks must be a constant tuple or None.')
        aytup__fzh = nqk__udr[22]
        if not is_overload_none(aytup__fzh) and not is_overload_int(aytup__fzh
            ):
            raise BodoError(
                f'{func_name}: fontsize must be an integer or None.')
        rgb__iqq = nqk__udr[29]
        if not is_overload_none(rgb__iqq) and not is_overload_constant_str(
            rgb__iqq):
            raise BodoError(
                f'{func_name}: xlabel must be a constant string or None.')
        imwxc__rcbkx = nqk__udr[30]
        if not is_overload_none(imwxc__rcbkx) and not is_overload_constant_str(
            imwxc__rcbkx):
            raise BodoError(
                f'{func_name}: ylabel must be a constant string or None.')
        pdbi__hohlr = types.List(types.mpl_line_2d_type)
        dxps__uqgp = get_overload_const_str(dxps__uqgp)
        if dxps__uqgp == 'scatter':
            if is_overload_none(xxdix__let) and is_overload_none(qqgti__uqg):
                raise BodoError(
                    f'{func_name}: {dxps__uqgp} requires an x and y column.')
            elif is_overload_none(xxdix__let):
                raise BodoError(
                    f'{func_name}: {dxps__uqgp} x column is missing.')
            elif is_overload_none(qqgti__uqg):
                raise BodoError(
                    f'{func_name}: {dxps__uqgp} y column is missing.')
            pdbi__hohlr = types.mpl_path_collection_type
        elif dxps__uqgp != 'line':
            raise BodoError(f'{func_name}: {dxps__uqgp} plot is not supported.'
                )
        return signature(pdbi__hohlr, *nqk__udr).replace(pysig=bbujq__ejzy)

    def generic_resolve(self, df, attr):
        if self._is_existing_attr(attr):
            return
        check_runtime_cols_unsupported(df,
            'Acessing DataFrame columns by attribute')
        if attr in df.columns:
            nzphv__nxocx = df.columns.index(attr)
            arr_typ = df.data[nzphv__nxocx]
            return SeriesType(arr_typ.dtype, arr_typ, df.index, types.
                StringLiteral(attr))
        if len(df.columns) > 0 and isinstance(df.columns[0], tuple):
            fid__kgxxf = []
            ahej__dmugg = []
            berjb__hdanj = False
            for i, cfql__grzx in enumerate(df.columns):
                if cfql__grzx[0] != attr:
                    continue
                berjb__hdanj = True
                fid__kgxxf.append(cfql__grzx[1] if len(cfql__grzx) == 2 else
                    cfql__grzx[1:])
                ahej__dmugg.append(df.data[i])
            if berjb__hdanj:
                return DataFrameType(tuple(ahej__dmugg), df.index, tuple(
                    fid__kgxxf))


DataFrameAttribute._no_unliteral = True


@overload(operator.getitem, no_unliteral=True)
def namedtuple_getitem_overload(tup, idx):
    if isinstance(tup, types.BaseNamedTuple) and is_overload_constant_str(idx):
        uvly__azg = get_overload_const_str(idx)
        val_ind = tup.instance_class._fields.index(uvly__azg)
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
        ysdcc__rlt = builder.extract_value(payload.data, i)
        context.nrt.decref(builder, df_type.data[i], ysdcc__rlt)
    context.nrt.decref(builder, df_type.index, payload.index)


def define_df_dtor(context, builder, df_type, payload_type):
    zruxx__tmf = builder.module
    aogvx__uiarl = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    aicu__oih = cgutils.get_or_insert_function(zruxx__tmf, aogvx__uiarl,
        name='.dtor.df.{}'.format(df_type))
    if not aicu__oih.is_declaration:
        return aicu__oih
    aicu__oih.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(aicu__oih.append_basic_block())
    rjy__bfuzr = aicu__oih.args[0]
    byc__dacjc = context.get_value_type(payload_type).as_pointer()
    wtrr__rqwt = builder.bitcast(rjy__bfuzr, byc__dacjc)
    payload = context.make_helper(builder, payload_type, ref=wtrr__rqwt)
    decref_df_data(context, builder, payload, df_type)
    has_parent = cgutils.is_not_null(builder, payload.parent)
    with builder.if_then(has_parent):
        kky__vpcrg = context.get_python_api(builder)
        fke__bzbdg = kky__vpcrg.gil_ensure()
        kky__vpcrg.decref(payload.parent)
        kky__vpcrg.gil_release(fke__bzbdg)
    builder.ret_void()
    return aicu__oih


def construct_dataframe(context, builder, df_type, data_tup, index_val,
    parent=None, colnames=None):
    payload_type = DataFramePayloadType(df_type)
    eika__stehu = cgutils.create_struct_proxy(payload_type)(context, builder)
    eika__stehu.data = data_tup
    eika__stehu.index = index_val
    if colnames is not None:
        assert df_type.has_runtime_cols, 'construct_dataframe can only provide colnames if columns are determined at runtime'
        eika__stehu.columns = colnames
    zjx__sgrbg = context.get_value_type(payload_type)
    uizra__sgo = context.get_abi_sizeof(zjx__sgrbg)
    szca__hefug = define_df_dtor(context, builder, df_type, payload_type)
    uygb__wgqw = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, uizra__sgo), szca__hefug)
    msz__tby = context.nrt.meminfo_data(builder, uygb__wgqw)
    yjar__zktm = builder.bitcast(msz__tby, zjx__sgrbg.as_pointer())
    qfmva__jow = cgutils.create_struct_proxy(df_type)(context, builder)
    qfmva__jow.meminfo = uygb__wgqw
    if parent is None:
        qfmva__jow.parent = cgutils.get_null_value(qfmva__jow.parent.type)
    else:
        qfmva__jow.parent = parent
        eika__stehu.parent = parent
        has_parent = cgutils.is_not_null(builder, parent)
        with builder.if_then(has_parent):
            kky__vpcrg = context.get_python_api(builder)
            fke__bzbdg = kky__vpcrg.gil_ensure()
            kky__vpcrg.incref(parent)
            kky__vpcrg.gil_release(fke__bzbdg)
    builder.store(eika__stehu._getvalue(), yjar__zktm)
    return qfmva__jow._getvalue()


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
        mrzbs__gisst = [data_typ.dtype.arr_types.dtype] * len(data_typ.
            dtype.arr_types)
    else:
        mrzbs__gisst = [tjo__lpnf for tjo__lpnf in data_typ.dtype.arr_types]
    cvxyu__znshw = DataFrameType(tuple(mrzbs__gisst + [colnames_index_typ]),
        index_typ, None, is_table_format=True)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup, index, col_names = args
        parent = None
        yybm__aoipc = construct_dataframe(context, builder, df_type,
            data_tup, index, parent, col_names)
        context.nrt.incref(builder, data_typ, data_tup)
        context.nrt.incref(builder, index_typ, index)
        context.nrt.incref(builder, colnames_index_typ, col_names)
        return yybm__aoipc
    sig = signature(cvxyu__znshw, data_typ, index_typ, colnames_index_typ)
    return sig, codegen


@intrinsic
def init_dataframe(typingctx, data_tup_typ, index_typ, col_names_typ=None):
    assert is_pd_index_type(index_typ) or isinstance(index_typ, MultiIndexType
        ), 'init_dataframe(): invalid index type'
    uvw__eyln = len(data_tup_typ.types)
    if uvw__eyln == 0:
        column_names = ()
    elif isinstance(col_names_typ, types.TypeRef):
        column_names = col_names_typ.instance_type.columns
    else:
        column_names = get_const_tup_vals(col_names_typ)
    if uvw__eyln == 1 and isinstance(data_tup_typ.types[0], TableType):
        uvw__eyln = len(data_tup_typ.types[0].arr_types)
    assert len(column_names
        ) == uvw__eyln, 'init_dataframe(): number of column names does not match number of columns'
    is_table_format = False
    mim__fygsv = data_tup_typ.types
    if uvw__eyln != 0 and isinstance(data_tup_typ.types[0], TableType):
        mim__fygsv = data_tup_typ.types[0].arr_types
        is_table_format = True
    cvxyu__znshw = DataFrameType(mim__fygsv, index_typ, column_names,
        is_table_format=is_table_format)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup = args[0]
        index_val = args[1]
        parent = None
        if is_table_format:
            ljxb__atrr = cgutils.create_struct_proxy(cvxyu__znshw.table_type)(
                context, builder, builder.extract_value(data_tup, 0))
            parent = ljxb__atrr.parent
        yybm__aoipc = construct_dataframe(context, builder, df_type,
            data_tup, index_val, parent, None)
        context.nrt.incref(builder, data_tup_typ, data_tup)
        context.nrt.incref(builder, index_typ, index_val)
        return yybm__aoipc
    sig = signature(cvxyu__znshw, data_tup_typ, index_typ, col_names_typ)
    return sig, codegen


@intrinsic
def has_parent(typingctx, df=None):
    check_runtime_cols_unsupported(df, 'has_parent')

    def codegen(context, builder, sig, args):
        qfmva__jow = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        return cgutils.is_not_null(builder, qfmva__jow.parent)
    return signature(types.bool_, df), codegen


@intrinsic
def _column_needs_unboxing(typingctx, df_typ, i_typ=None):
    check_runtime_cols_unsupported(df_typ, '_column_needs_unboxing')
    assert isinstance(df_typ, DataFrameType) and is_overload_constant_int(i_typ
        )

    def codegen(context, builder, sig, args):
        eika__stehu = get_dataframe_payload(context, builder, df_typ, args[0])
        kif__qggx = get_overload_const_int(i_typ)
        arr_typ = df_typ.data[kif__qggx]
        if df_typ.is_table_format:
            ljxb__atrr = cgutils.create_struct_proxy(df_typ.table_type)(context
                , builder, builder.extract_value(eika__stehu.data, 0))
            jgg__rglvu = df_typ.table_type.type_to_blk[arr_typ]
            cfdaj__ywac = getattr(ljxb__atrr, f'block_{jgg__rglvu}')
            lzq__duky = ListInstance(context, builder, types.List(arr_typ),
                cfdaj__ywac)
            mozt__cbyn = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[kif__qggx])
            ysdcc__rlt = lzq__duky.getitem(mozt__cbyn)
        else:
            ysdcc__rlt = builder.extract_value(eika__stehu.data, kif__qggx)
        iwss__crf = cgutils.alloca_once_value(builder, ysdcc__rlt)
        bor__tbtoj = cgutils.alloca_once_value(builder, context.
            get_constant_null(arr_typ))
        return is_ll_eq(builder, iwss__crf, bor__tbtoj)
    return signature(types.bool_, df_typ, i_typ), codegen


def get_dataframe_payload(context, builder, df_type, value):
    uygb__wgqw = cgutils.create_struct_proxy(df_type)(context, builder, value
        ).meminfo
    payload_type = DataFramePayloadType(df_type)
    payload = context.nrt.meminfo_data(builder, uygb__wgqw)
    byc__dacjc = context.get_value_type(payload_type).as_pointer()
    payload = builder.bitcast(payload, byc__dacjc)
    return context.make_helper(builder, payload_type, ref=payload)


@intrinsic
def _get_dataframe_data(typingctx, df_typ=None):
    check_runtime_cols_unsupported(df_typ, '_get_dataframe_data')
    cvxyu__znshw = types.Tuple(df_typ.data)
    if df_typ.is_table_format:
        cvxyu__znshw = types.Tuple([TableType(df_typ.data)])
    sig = signature(cvxyu__znshw, df_typ)

    def codegen(context, builder, signature, args):
        eika__stehu = get_dataframe_payload(context, builder, signature.
            args[0], args[0])
        return impl_ret_borrowed(context, builder, signature.return_type,
            eika__stehu.data)
    return sig, codegen


@intrinsic
def get_dataframe_index(typingctx, df_typ=None):

    def codegen(context, builder, signature, args):
        eika__stehu = get_dataframe_payload(context, builder, signature.
            args[0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.index,
            eika__stehu.index)
    cvxyu__znshw = df_typ.index
    sig = signature(cvxyu__znshw, df_typ)
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
        ijrvs__qvf = df.data[i]
        return ijrvs__qvf(*args)


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
        eika__stehu = get_dataframe_payload(context, builder, signature.
            args[0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.table_type,
            builder.extract_value(eika__stehu.data, 0))
    return df_typ.table_type(df_typ), codegen


@intrinsic
def get_dataframe_column_names(typingctx, df_typ=None):
    assert df_typ.has_runtime_cols, 'get_dataframe_column_names() expects columns to be determined at runtime'

    def codegen(context, builder, signature, args):
        eika__stehu = get_dataframe_payload(context, builder, signature.
            args[0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.
            runtime_colname_typ, eika__stehu.columns)
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
    embo__kxs = self.typemap[data_tup.name]
    if any(is_tuple_like_type(tjo__lpnf) for tjo__lpnf in embo__kxs.types):
        return None
    if equiv_set.has_shape(data_tup):
        nru__rirr = equiv_set.get_shape(data_tup)
        if len(nru__rirr) > 1:
            equiv_set.insert_equiv(*nru__rirr)
        if len(nru__rirr) > 0:
            gzgh__jza = self.typemap[index.name]
            if not isinstance(gzgh__jza, HeterogeneousIndexType
                ) and equiv_set.has_shape(index):
                equiv_set.insert_equiv(nru__rirr[0], index)
            return ArrayAnalysis.AnalyzeResult(shape=(nru__rirr[0], len(
                nru__rirr)), pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_dataframe_ext_init_dataframe
    ) = init_dataframe_equiv


def get_dataframe_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    rat__cfmfb = args[0]
    data_types = self.typemap[rat__cfmfb.name].data
    if any(is_tuple_like_type(tjo__lpnf) for tjo__lpnf in data_types):
        return None
    if equiv_set.has_shape(rat__cfmfb):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            rat__cfmfb)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_data
    ) = get_dataframe_data_equiv


def get_dataframe_index_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 1 and not kws
    rat__cfmfb = args[0]
    gzgh__jza = self.typemap[rat__cfmfb.name].index
    if isinstance(gzgh__jza, HeterogeneousIndexType):
        return None
    if equiv_set.has_shape(rat__cfmfb):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            rat__cfmfb)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_index
    ) = get_dataframe_index_equiv


def get_dataframe_table_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    rat__cfmfb = args[0]
    if equiv_set.has_shape(rat__cfmfb):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            rat__cfmfb), pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_table
    ) = get_dataframe_table_equiv


def get_dataframe_column_names_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    rat__cfmfb = args[0]
    if equiv_set.has_shape(rat__cfmfb):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            rat__cfmfb)[1], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_column_names
    ) = get_dataframe_column_names_equiv


@intrinsic
def set_dataframe_data(typingctx, df_typ, c_ind_typ, arr_typ=None):
    check_runtime_cols_unsupported(df_typ, 'set_dataframe_data')
    assert is_overload_constant_int(c_ind_typ)
    kif__qggx = get_overload_const_int(c_ind_typ)
    if df_typ.data[kif__qggx] != arr_typ:
        raise BodoError(
            'Changing dataframe column data type inplace is not supported in conditionals/loops or for dataframe arguments'
            )

    def codegen(context, builder, signature, args):
        oyt__ote, ycsdl__wgot, xspd__ozcqk = args
        eika__stehu = get_dataframe_payload(context, builder, df_typ, oyt__ote)
        if df_typ.is_table_format:
            ljxb__atrr = cgutils.create_struct_proxy(df_typ.table_type)(context
                , builder, builder.extract_value(eika__stehu.data, 0))
            jgg__rglvu = df_typ.table_type.type_to_blk[arr_typ]
            cfdaj__ywac = getattr(ljxb__atrr, f'block_{jgg__rglvu}')
            lzq__duky = ListInstance(context, builder, types.List(arr_typ),
                cfdaj__ywac)
            mozt__cbyn = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[kif__qggx])
            lzq__duky.setitem(mozt__cbyn, xspd__ozcqk, True)
        else:
            ysdcc__rlt = builder.extract_value(eika__stehu.data, kif__qggx)
            context.nrt.decref(builder, df_typ.data[kif__qggx], ysdcc__rlt)
            eika__stehu.data = builder.insert_value(eika__stehu.data,
                xspd__ozcqk, kif__qggx)
            context.nrt.incref(builder, arr_typ, xspd__ozcqk)
        qfmva__jow = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=oyt__ote)
        payload_type = DataFramePayloadType(df_typ)
        wtrr__rqwt = context.nrt.meminfo_data(builder, qfmva__jow.meminfo)
        byc__dacjc = context.get_value_type(payload_type).as_pointer()
        wtrr__rqwt = builder.bitcast(wtrr__rqwt, byc__dacjc)
        builder.store(eika__stehu._getvalue(), wtrr__rqwt)
        return impl_ret_borrowed(context, builder, df_typ, oyt__ote)
    sig = signature(df_typ, df_typ, c_ind_typ, arr_typ)
    return sig, codegen


@intrinsic
def set_df_index(typingctx, df_t, index_t=None):
    check_runtime_cols_unsupported(df_t, 'set_df_index')

    def codegen(context, builder, signature, args):
        ghdn__rgod = args[0]
        index_val = args[1]
        df_typ = signature.args[0]
        jsfc__vsy = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=ghdn__rgod)
        pjm__kpmic = get_dataframe_payload(context, builder, df_typ, ghdn__rgod
            )
        qfmva__jow = construct_dataframe(context, builder, signature.
            return_type, pjm__kpmic.data, index_val, jsfc__vsy.parent, None)
        context.nrt.incref(builder, index_t, index_val)
        context.nrt.incref(builder, types.Tuple(df_t.data), pjm__kpmic.data)
        return qfmva__jow
    cvxyu__znshw = DataFrameType(df_t.data, index_t, df_t.columns, df_t.
        dist, df_t.is_table_format)
    sig = signature(cvxyu__znshw, df_t, index_t)
    return sig, codegen


@intrinsic
def set_df_column_with_reflect(typingctx, df_type, cname_type, arr_type=None):
    check_runtime_cols_unsupported(df_type, 'set_df_column_with_reflect')
    assert is_literal_type(cname_type), 'constant column name expected'
    col_name = get_literal_value(cname_type)
    uvw__eyln = len(df_type.columns)
    rpjs__bnq = uvw__eyln
    ybn__bujm = df_type.data
    column_names = df_type.columns
    index_typ = df_type.index
    ixmne__zortq = col_name not in df_type.columns
    kif__qggx = uvw__eyln
    if ixmne__zortq:
        ybn__bujm += arr_type,
        column_names += col_name,
        rpjs__bnq += 1
    else:
        kif__qggx = df_type.columns.index(col_name)
        ybn__bujm = tuple(arr_type if i == kif__qggx else ybn__bujm[i] for
            i in range(uvw__eyln))

    def codegen(context, builder, signature, args):
        oyt__ote, ycsdl__wgot, xspd__ozcqk = args
        in_dataframe_payload = get_dataframe_payload(context, builder,
            df_type, oyt__ote)
        dvpfd__kfc = cgutils.create_struct_proxy(df_type)(context, builder,
            value=oyt__ote)
        if df_type.is_table_format:
            eoer__zlt = df_type.table_type
            pci__aaot = builder.extract_value(in_dataframe_payload.data, 0)
            qhy__giad = TableType(ybn__bujm)
            lnhl__pok = set_table_data_codegen(context, builder, eoer__zlt,
                pci__aaot, qhy__giad, arr_type, xspd__ozcqk, kif__qggx,
                ixmne__zortq)
            data_tup = context.make_tuple(builder, types.Tuple([qhy__giad]),
                [lnhl__pok])
        else:
            mim__fygsv = [(builder.extract_value(in_dataframe_payload.data,
                i) if i != kif__qggx else xspd__ozcqk) for i in range(
                uvw__eyln)]
            if ixmne__zortq:
                mim__fygsv.append(xspd__ozcqk)
            for rat__cfmfb, hbusu__kky in zip(mim__fygsv, ybn__bujm):
                context.nrt.incref(builder, hbusu__kky, rat__cfmfb)
            data_tup = context.make_tuple(builder, types.Tuple(ybn__bujm),
                mim__fygsv)
        index_val = in_dataframe_payload.index
        context.nrt.incref(builder, index_typ, index_val)
        bpcri__xceew = construct_dataframe(context, builder, signature.
            return_type, data_tup, index_val, dvpfd__kfc.parent, None)
        if not ixmne__zortq and arr_type == df_type.data[kif__qggx]:
            decref_df_data(context, builder, in_dataframe_payload, df_type)
            payload_type = DataFramePayloadType(df_type)
            wtrr__rqwt = context.nrt.meminfo_data(builder, dvpfd__kfc.meminfo)
            byc__dacjc = context.get_value_type(payload_type).as_pointer()
            wtrr__rqwt = builder.bitcast(wtrr__rqwt, byc__dacjc)
            evbc__hdfq = get_dataframe_payload(context, builder, df_type,
                bpcri__xceew)
            builder.store(evbc__hdfq._getvalue(), wtrr__rqwt)
            context.nrt.incref(builder, index_typ, index_val)
            if df_type.is_table_format:
                context.nrt.incref(builder, qhy__giad, builder.
                    extract_value(data_tup, 0))
            else:
                for rat__cfmfb, hbusu__kky in zip(mim__fygsv, ybn__bujm):
                    context.nrt.incref(builder, hbusu__kky, rat__cfmfb)
        has_parent = cgutils.is_not_null(builder, dvpfd__kfc.parent)
        with builder.if_then(has_parent):
            kky__vpcrg = context.get_python_api(builder)
            fke__bzbdg = kky__vpcrg.gil_ensure()
            aluyq__bom = context.get_env_manager(builder)
            context.nrt.incref(builder, arr_type, xspd__ozcqk)
            qmal__nutcm = numba.core.pythonapi._BoxContext(context, builder,
                kky__vpcrg, aluyq__bom)
            epg__liyz = qmal__nutcm.pyapi.from_native_value(arr_type,
                xspd__ozcqk, qmal__nutcm.env_manager)
            if isinstance(col_name, str):
                agzm__qti = context.insert_const_string(builder.module,
                    col_name)
                qto__pzmqc = kky__vpcrg.string_from_string(agzm__qti)
            else:
                assert isinstance(col_name, int)
                qto__pzmqc = kky__vpcrg.long_from_longlong(context.
                    get_constant(types.intp, col_name))
            kky__vpcrg.object_setitem(dvpfd__kfc.parent, qto__pzmqc, epg__liyz)
            kky__vpcrg.decref(epg__liyz)
            kky__vpcrg.decref(qto__pzmqc)
            kky__vpcrg.gil_release(fke__bzbdg)
        return bpcri__xceew
    cvxyu__znshw = DataFrameType(ybn__bujm, index_typ, column_names,
        df_type.dist, df_type.is_table_format)
    sig = signature(cvxyu__znshw, df_type, cname_type, arr_type)
    return sig, codegen


@lower_constant(DataFrameType)
def lower_constant_dataframe(context, builder, df_type, pyval):
    check_runtime_cols_unsupported(df_type, 'lowering a constant DataFrame')
    uvw__eyln = len(pyval.columns)
    mim__fygsv = []
    for i in range(uvw__eyln):
        rmvzu__dppuk = pyval.iloc[:, i]
        if isinstance(df_type.data[i], bodo.DatetimeArrayType):
            epg__liyz = rmvzu__dppuk.array
        else:
            epg__liyz = rmvzu__dppuk.values
        mim__fygsv.append(epg__liyz)
    mim__fygsv = tuple(mim__fygsv)
    if df_type.is_table_format:
        ljxb__atrr = context.get_constant_generic(builder, df_type.
            table_type, Table(mim__fygsv))
        data_tup = lir.Constant.literal_struct([ljxb__atrr])
    else:
        data_tup = lir.Constant.literal_struct([context.
            get_constant_generic(builder, df_type.data[i], cfql__grzx) for 
            i, cfql__grzx in enumerate(mim__fygsv)])
    index_val = context.get_constant_generic(builder, df_type.index, pyval.
        index)
    qsq__eud = context.get_constant_null(types.pyobject)
    payload = lir.Constant.literal_struct([data_tup, index_val, qsq__eud])
    payload = cgutils.global_constant(builder, '.const.payload', payload
        ).bitcast(cgutils.voidptr_t)
    imhf__kpzkx = context.get_constant(types.int64, -1)
    nlp__znojv = context.get_constant_null(types.voidptr)
    uygb__wgqw = lir.Constant.literal_struct([imhf__kpzkx, nlp__znojv,
        nlp__znojv, payload, imhf__kpzkx])
    uygb__wgqw = cgutils.global_constant(builder, '.const.meminfo', uygb__wgqw
        ).bitcast(cgutils.voidptr_t)
    return lir.Constant.literal_struct([uygb__wgqw, qsq__eud])


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
        mucga__oozhs = context.cast(builder, in_dataframe_payload.index,
            fromty.index, toty.index)
    else:
        mucga__oozhs = in_dataframe_payload.index
        context.nrt.incref(builder, fromty.index, mucga__oozhs)
    if (fromty.is_table_format == toty.is_table_format and fromty.data ==
        toty.data):
        ahej__dmugg = in_dataframe_payload.data
        if fromty.is_table_format:
            context.nrt.incref(builder, types.Tuple([fromty.table_type]),
                ahej__dmugg)
        else:
            context.nrt.incref(builder, types.BaseTuple.from_types(fromty.
                data), ahej__dmugg)
    elif not fromty.is_table_format and toty.is_table_format:
        ahej__dmugg = _cast_df_data_to_table_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    elif fromty.is_table_format and not toty.is_table_format:
        ahej__dmugg = _cast_df_data_to_tuple_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    elif fromty.is_table_format and toty.is_table_format:
        ahej__dmugg = _cast_df_data_keep_table_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    else:
        ahej__dmugg = _cast_df_data_keep_tuple_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    return construct_dataframe(context, builder, toty, ahej__dmugg,
        mucga__oozhs, in_dataframe_payload.parent, None)


def _cast_empty_df(context, builder, toty):
    krzbl__tgtt = {}
    if isinstance(toty.index, RangeIndexType):
        index = 'bodo.hiframes.pd_index_ext.init_range_index(0, 0, 1, None)'
    else:
        mcz__ldoo = get_index_data_arr_types(toty.index)[0]
        xib__iuio = bodo.utils.transform.get_type_alloc_counts(mcz__ldoo) - 1
        upxt__rnam = ', '.join('0' for ycsdl__wgot in range(xib__iuio))
        index = (
            'bodo.utils.conversion.index_from_array(bodo.utils.utils.alloc_type(0, index_arr_type, ({}{})))'
            .format(upxt__rnam, ', ' if xib__iuio == 1 else ''))
        krzbl__tgtt['index_arr_type'] = mcz__ldoo
    gek__uas = []
    for i, arr_typ in enumerate(toty.data):
        xib__iuio = bodo.utils.transform.get_type_alloc_counts(arr_typ) - 1
        upxt__rnam = ', '.join('0' for ycsdl__wgot in range(xib__iuio))
        yrw__tdy = 'bodo.utils.utils.alloc_type(0, arr_type{}, ({}{}))'.format(
            i, upxt__rnam, ', ' if xib__iuio == 1 else '')
        gek__uas.append(yrw__tdy)
        krzbl__tgtt[f'arr_type{i}'] = arr_typ
    gek__uas = ', '.join(gek__uas)
    squbx__opjt = 'def impl():\n'
    xyf__zjg = bodo.hiframes.dataframe_impl._gen_init_df(squbx__opjt, toty.
        columns, gek__uas, index, krzbl__tgtt)
    df = context.compile_internal(builder, xyf__zjg, toty(), [])
    return df


def _cast_df_data_to_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame to table format')
    zgi__mclnr = toty.table_type
    ljxb__atrr = cgutils.create_struct_proxy(zgi__mclnr)(context, builder)
    ljxb__atrr.parent = in_dataframe_payload.parent
    for tjo__lpnf, jgg__rglvu in zgi__mclnr.type_to_blk.items():
        fafwn__mvu = context.get_constant(types.int64, len(zgi__mclnr.
            block_to_arr_ind[jgg__rglvu]))
        ycsdl__wgot, uiy__ltxpj = ListInstance.allocate_ex(context, builder,
            types.List(tjo__lpnf), fafwn__mvu)
        uiy__ltxpj.size = fafwn__mvu
        setattr(ljxb__atrr, f'block_{jgg__rglvu}', uiy__ltxpj.value)
    for i, tjo__lpnf in enumerate(fromty.data):
        yanqa__xtk = toty.data[i]
        if tjo__lpnf != yanqa__xtk:
            penkz__izv = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*penkz__izv)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        ysdcc__rlt = builder.extract_value(in_dataframe_payload.data, i)
        if tjo__lpnf != yanqa__xtk:
            uavnl__njzvq = context.cast(builder, ysdcc__rlt, tjo__lpnf,
                yanqa__xtk)
            hxwju__qnd = False
        else:
            uavnl__njzvq = ysdcc__rlt
            hxwju__qnd = True
        jgg__rglvu = zgi__mclnr.type_to_blk[tjo__lpnf]
        cfdaj__ywac = getattr(ljxb__atrr, f'block_{jgg__rglvu}')
        lzq__duky = ListInstance(context, builder, types.List(tjo__lpnf),
            cfdaj__ywac)
        mozt__cbyn = context.get_constant(types.int64, zgi__mclnr.
            block_offsets[i])
        lzq__duky.setitem(mozt__cbyn, uavnl__njzvq, hxwju__qnd)
    data_tup = context.make_tuple(builder, types.Tuple([zgi__mclnr]), [
        ljxb__atrr._getvalue()])
    return data_tup


def _cast_df_data_keep_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame columns')
    mim__fygsv = []
    for i in range(len(fromty.data)):
        if fromty.data[i] != toty.data[i]:
            penkz__izv = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*penkz__izv)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
            ysdcc__rlt = builder.extract_value(in_dataframe_payload.data, i)
            uavnl__njzvq = context.cast(builder, ysdcc__rlt, fromty.data[i],
                toty.data[i])
            hxwju__qnd = False
        else:
            uavnl__njzvq = builder.extract_value(in_dataframe_payload.data, i)
            hxwju__qnd = True
        if hxwju__qnd:
            context.nrt.incref(builder, toty.data[i], uavnl__njzvq)
        mim__fygsv.append(uavnl__njzvq)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), mim__fygsv)
    return data_tup


def _cast_df_data_keep_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting table format DataFrame columns')
    eoer__zlt = fromty.table_type
    pci__aaot = cgutils.create_struct_proxy(eoer__zlt)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    qhy__giad = toty.table_type
    lnhl__pok = cgutils.create_struct_proxy(qhy__giad)(context, builder)
    lnhl__pok.parent = in_dataframe_payload.parent
    for tjo__lpnf, jgg__rglvu in qhy__giad.type_to_blk.items():
        fafwn__mvu = context.get_constant(types.int64, len(qhy__giad.
            block_to_arr_ind[jgg__rglvu]))
        ycsdl__wgot, uiy__ltxpj = ListInstance.allocate_ex(context, builder,
            types.List(tjo__lpnf), fafwn__mvu)
        uiy__ltxpj.size = fafwn__mvu
        setattr(lnhl__pok, f'block_{jgg__rglvu}', uiy__ltxpj.value)
    for i in range(len(fromty.data)):
        kfkr__rpbqk = fromty.data[i]
        yanqa__xtk = toty.data[i]
        if kfkr__rpbqk != yanqa__xtk:
            penkz__izv = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*penkz__izv)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        pnev__maps = eoer__zlt.type_to_blk[kfkr__rpbqk]
        wms__fqxwe = getattr(pci__aaot, f'block_{pnev__maps}')
        wzut__hvyb = ListInstance(context, builder, types.List(kfkr__rpbqk),
            wms__fqxwe)
        dct__qmieo = context.get_constant(types.int64, eoer__zlt.
            block_offsets[i])
        ysdcc__rlt = wzut__hvyb.getitem(dct__qmieo)
        if kfkr__rpbqk != yanqa__xtk:
            uavnl__njzvq = context.cast(builder, ysdcc__rlt, kfkr__rpbqk,
                yanqa__xtk)
            hxwju__qnd = False
        else:
            uavnl__njzvq = ysdcc__rlt
            hxwju__qnd = True
        fdu__nda = qhy__giad.type_to_blk[tjo__lpnf]
        uiy__ltxpj = getattr(lnhl__pok, f'block_{fdu__nda}')
        jbilg__pkkb = ListInstance(context, builder, types.List(yanqa__xtk),
            uiy__ltxpj)
        fkl__yyb = context.get_constant(types.int64, qhy__giad.block_offsets[i]
            )
        jbilg__pkkb.setitem(fkl__yyb, uavnl__njzvq, hxwju__qnd)
    data_tup = context.make_tuple(builder, types.Tuple([qhy__giad]), [
        lnhl__pok._getvalue()])
    return data_tup


def _cast_df_data_to_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(fromty,
        'casting table format to traditional DataFrame')
    zgi__mclnr = fromty.table_type
    ljxb__atrr = cgutils.create_struct_proxy(zgi__mclnr)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    mim__fygsv = []
    for i, tjo__lpnf in enumerate(toty.data):
        kfkr__rpbqk = fromty.data[i]
        if tjo__lpnf != kfkr__rpbqk:
            penkz__izv = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*penkz__izv)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        jgg__rglvu = zgi__mclnr.type_to_blk[tjo__lpnf]
        cfdaj__ywac = getattr(ljxb__atrr, f'block_{jgg__rglvu}')
        lzq__duky = ListInstance(context, builder, types.List(tjo__lpnf),
            cfdaj__ywac)
        mozt__cbyn = context.get_constant(types.int64, zgi__mclnr.
            block_offsets[i])
        ysdcc__rlt = lzq__duky.getitem(mozt__cbyn)
        if tjo__lpnf != kfkr__rpbqk:
            uavnl__njzvq = context.cast(builder, ysdcc__rlt, kfkr__rpbqk,
                tjo__lpnf)
            hxwju__qnd = False
        else:
            uavnl__njzvq = ysdcc__rlt
            hxwju__qnd = True
        if hxwju__qnd:
            context.nrt.incref(builder, tjo__lpnf, uavnl__njzvq)
        mim__fygsv.append(uavnl__njzvq)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), mim__fygsv)
    return data_tup


@overload(pd.DataFrame, inline='always', no_unliteral=True)
def pd_dataframe_overload(data=None, index=None, columns=None, dtype=None,
    copy=False):
    if not is_overload_constant_bool(copy):
        raise BodoError(
            "pd.DataFrame(): 'copy' argument should be a constant boolean")
    copy = get_overload_const(copy)
    zonal__hpboc, gek__uas, index_arg = _get_df_args(data, index, columns,
        dtype, copy)
    jac__awxb = gen_const_tup(zonal__hpboc)
    squbx__opjt = (
        'def _init_df(data=None, index=None, columns=None, dtype=None, copy=False):\n'
        )
    squbx__opjt += (
        '  return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, {}, {})\n'
        .format(gek__uas, index_arg, jac__awxb))
    qmlq__zptb = {}
    exec(squbx__opjt, {'bodo': bodo, 'np': np}, qmlq__zptb)
    jscjr__znbmv = qmlq__zptb['_init_df']
    return jscjr__znbmv


@intrinsic
def _tuple_to_table_format_decoded(typingctx, df_typ):
    assert not df_typ.is_table_format, '_tuple_to_table_format requires a tuple format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    cvxyu__znshw = DataFrameType(to_str_arr_if_dict_array(df_typ.data),
        df_typ.index, df_typ.columns, dist=df_typ.dist, is_table_format=True)
    sig = signature(cvxyu__znshw, df_typ)
    return sig, codegen


@intrinsic
def _table_to_tuple_format_decoded(typingctx, df_typ):
    assert df_typ.is_table_format, '_tuple_to_table_format requires a table format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    cvxyu__znshw = DataFrameType(to_str_arr_if_dict_array(df_typ.data),
        df_typ.index, df_typ.columns, dist=df_typ.dist, is_table_format=False)
    sig = signature(cvxyu__znshw, df_typ)
    return sig, codegen


def _get_df_args(data, index, columns, dtype, copy):
    mkocx__hcws = ''
    if not is_overload_none(dtype):
        mkocx__hcws = '.astype(dtype)'
    index_is_none = is_overload_none(index)
    index_arg = 'bodo.utils.conversion.convert_to_index(index)'
    if isinstance(data, types.BaseTuple):
        if not data.types[0] == types.StringLiteral('__bodo_tup'):
            raise BodoError('pd.DataFrame tuple input data not supported yet')
        assert len(data.types) % 2 == 1, 'invalid const dict tuple structure'
        uvw__eyln = (len(data.types) - 1) // 2
        acec__tim = [tjo__lpnf.literal_value for tjo__lpnf in data.types[1:
            uvw__eyln + 1]]
        data_val_types = dict(zip(acec__tim, data.types[uvw__eyln + 1:]))
        mim__fygsv = ['data[{}]'.format(i) for i in range(uvw__eyln + 1, 2 *
            uvw__eyln + 1)]
        data_dict = dict(zip(acec__tim, mim__fygsv))
        if is_overload_none(index):
            for i, tjo__lpnf in enumerate(data.types[uvw__eyln + 1:]):
                if isinstance(tjo__lpnf, SeriesType):
                    index_arg = (
                        'bodo.hiframes.pd_series_ext.get_series_index(data[{}])'
                        .format(uvw__eyln + 1 + i))
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
        kuy__wmnnq = '.copy()' if copy else ''
        qdllv__tkqmw = get_overload_const_list(columns)
        uvw__eyln = len(qdllv__tkqmw)
        data_val_types = {qmal__nutcm: data.copy(ndim=1) for qmal__nutcm in
            qdllv__tkqmw}
        mim__fygsv = ['data[:,{}]{}'.format(i, kuy__wmnnq) for i in range(
            uvw__eyln)]
        data_dict = dict(zip(qdllv__tkqmw, mim__fygsv))
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
    gek__uas = '({},)'.format(', '.join(
        'bodo.utils.conversion.coerce_to_array({}, True, scalar_to_arr_len={}){}'
        .format(data_dict[qmal__nutcm], df_len, mkocx__hcws) for
        qmal__nutcm in col_names))
    if len(col_names) == 0:
        gek__uas = '()'
    return col_names, gek__uas, index_arg


def _get_df_len_from_info(data_dict, data_val_types, col_names,
    index_is_none, index_arg):
    df_len = '0'
    for qmal__nutcm in col_names:
        if qmal__nutcm in data_dict and is_iterable_type(data_val_types[
            qmal__nutcm]):
            df_len = 'len({})'.format(data_dict[qmal__nutcm])
            break
    if df_len == '0' and not index_is_none:
        df_len = f'len({index_arg})'
    return df_len


def _fill_null_arrays(data_dict, col_names, df_len, dtype):
    if all(qmal__nutcm in data_dict for qmal__nutcm in col_names):
        return
    if is_overload_none(dtype):
        dtype = 'bodo.string_array_type'
    else:
        dtype = 'bodo.utils.conversion.array_type_from_dtype(dtype)'
    hhqo__scef = 'bodo.libs.array_kernels.gen_na_array({}, {})'.format(df_len,
        dtype)
    for qmal__nutcm in col_names:
        if qmal__nutcm not in data_dict:
            data_dict[qmal__nutcm] = hhqo__scef


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
            tjo__lpnf = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            return len(tjo__lpnf)
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
        tbal__zxhmz = idx.literal_value
        if isinstance(tbal__zxhmz, int):
            ijrvs__qvf = tup.types[tbal__zxhmz]
        elif isinstance(tbal__zxhmz, slice):
            ijrvs__qvf = types.BaseTuple.from_types(tup.types[tbal__zxhmz])
        return signature(ijrvs__qvf, *args)


GetItemTuple.prefer_literal = True


@lower_builtin(operator.getitem, types.BaseTuple, types.IntegerLiteral)
@lower_builtin(operator.getitem, types.BaseTuple, types.SliceLiteral)
def getitem_tuple_lower(context, builder, sig, args):
    gcwv__tzm, idx = sig.args
    idx = idx.literal_value
    tup, ycsdl__wgot = args
    if isinstance(idx, int):
        if idx < 0:
            idx += len(gcwv__tzm)
        if not 0 <= idx < len(gcwv__tzm):
            raise IndexError('cannot index at %d in %s' % (idx, gcwv__tzm))
        bbsyb__dok = builder.extract_value(tup, idx)
    elif isinstance(idx, slice):
        otvw__djaw = cgutils.unpack_tuple(builder, tup)[idx]
        bbsyb__dok = context.make_tuple(builder, sig.return_type, otvw__djaw)
    else:
        raise NotImplementedError('unexpected index %r for %s' % (idx, sig.
            args[0]))
    return impl_ret_borrowed(context, builder, sig.return_type, bbsyb__dok)


def join_dummy(left_df, right_df, left_on, right_on, how, suffix_x,
    suffix_y, is_join, indicator, _bodo_na_equal, gen_cond):
    return left_df


@infer_global(join_dummy)
class JoinTyper(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        from bodo.utils.typing import is_overload_str
        assert not kws
        (left_df, right_df, left_on, right_on, tvfg__sfg, suffix_x,
            suffix_y, is_join, indicator, ycsdl__wgot, ycsdl__wgot) = args
        left_on = get_overload_const_list(left_on)
        right_on = get_overload_const_list(right_on)
        xaea__eyg = {qmal__nutcm: i for i, qmal__nutcm in enumerate(left_on)}
        ljytk__adogo = {qmal__nutcm: i for i, qmal__nutcm in enumerate(
            right_on)}
        bxdf__coj = set(left_on) & set(right_on)
        kwt__xxp = set(left_df.columns) & set(right_df.columns)
        dbc__sovzn = kwt__xxp - bxdf__coj
        khyud__mij = '$_bodo_index_' in left_on
        erl__wady = '$_bodo_index_' in right_on
        how = get_overload_const_str(tvfg__sfg)
        mscg__ttqkz = how in {'left', 'outer'}
        cnfky__ousv = how in {'right', 'outer'}
        columns = []
        data = []
        if khyud__mij:
            kjqjg__zri = bodo.utils.typing.get_index_data_arr_types(left_df
                .index)[0]
        else:
            kjqjg__zri = left_df.data[left_df.column_index[left_on[0]]]
        if erl__wady:
            rdzf__cnrps = bodo.utils.typing.get_index_data_arr_types(right_df
                .index)[0]
        else:
            rdzf__cnrps = right_df.data[right_df.column_index[right_on[0]]]
        if khyud__mij and not erl__wady and not is_join.literal_value:
            rbqgi__aubd = right_on[0]
            if rbqgi__aubd in left_df.column_index:
                columns.append(rbqgi__aubd)
                if (rdzf__cnrps == bodo.dict_str_arr_type and kjqjg__zri ==
                    bodo.string_array_type):
                    nkvkx__ojv = bodo.string_array_type
                else:
                    nkvkx__ojv = rdzf__cnrps
                data.append(nkvkx__ojv)
        if erl__wady and not khyud__mij and not is_join.literal_value:
            ret__syipl = left_on[0]
            if ret__syipl in right_df.column_index:
                columns.append(ret__syipl)
                if (kjqjg__zri == bodo.dict_str_arr_type and rdzf__cnrps ==
                    bodo.string_array_type):
                    nkvkx__ojv = bodo.string_array_type
                else:
                    nkvkx__ojv = kjqjg__zri
                data.append(nkvkx__ojv)
        for kfkr__rpbqk, rmvzu__dppuk in zip(left_df.data, left_df.columns):
            columns.append(str(rmvzu__dppuk) + suffix_x.literal_value if 
                rmvzu__dppuk in dbc__sovzn else rmvzu__dppuk)
            if rmvzu__dppuk in bxdf__coj:
                if kfkr__rpbqk == bodo.dict_str_arr_type:
                    kfkr__rpbqk = right_df.data[right_df.column_index[
                        rmvzu__dppuk]]
                data.append(kfkr__rpbqk)
            else:
                if (kfkr__rpbqk == bodo.dict_str_arr_type and rmvzu__dppuk in
                    xaea__eyg):
                    if erl__wady:
                        kfkr__rpbqk = rdzf__cnrps
                    else:
                        fim__xue = xaea__eyg[rmvzu__dppuk]
                        mkpca__xsoha = right_on[fim__xue]
                        kfkr__rpbqk = right_df.data[right_df.column_index[
                            mkpca__xsoha]]
                if cnfky__ousv:
                    kfkr__rpbqk = to_nullable_type(kfkr__rpbqk)
                data.append(kfkr__rpbqk)
        for kfkr__rpbqk, rmvzu__dppuk in zip(right_df.data, right_df.columns):
            if rmvzu__dppuk not in bxdf__coj:
                columns.append(str(rmvzu__dppuk) + suffix_y.literal_value if
                    rmvzu__dppuk in dbc__sovzn else rmvzu__dppuk)
                if (kfkr__rpbqk == bodo.dict_str_arr_type and rmvzu__dppuk in
                    ljytk__adogo):
                    if khyud__mij:
                        kfkr__rpbqk = kjqjg__zri
                    else:
                        fim__xue = ljytk__adogo[rmvzu__dppuk]
                        dsb__btsgp = left_on[fim__xue]
                        kfkr__rpbqk = left_df.data[left_df.column_index[
                            dsb__btsgp]]
                if mscg__ttqkz:
                    kfkr__rpbqk = to_nullable_type(kfkr__rpbqk)
                data.append(kfkr__rpbqk)
        ustdd__ppfr = get_overload_const_bool(indicator)
        if ustdd__ppfr:
            columns.append('_merge')
            data.append(bodo.CategoricalArrayType(bodo.PDCategoricalDtype((
                'left_only', 'right_only', 'both'), bodo.string_type, False)))
        index_typ = RangeIndexType(types.none)
        zulu__rtl = False
        if khyud__mij and erl__wady and not is_overload_str(how, 'asof'):
            index_typ = left_df.index
            zulu__rtl = True
        elif khyud__mij and not erl__wady:
            index_typ = right_df.index
            zulu__rtl = True
        elif erl__wady and not khyud__mij:
            index_typ = left_df.index
            zulu__rtl = True
        if zulu__rtl and isinstance(index_typ, bodo.hiframes.pd_index_ext.
            RangeIndexType):
            index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64
                )
        ezpb__febh = DataFrameType(tuple(data), index_typ, tuple(columns))
        return signature(ezpb__febh, *args)


JoinTyper._no_unliteral = True


@lower_builtin(join_dummy, types.VarArg(types.Any))
def lower_join_dummy(context, builder, sig, args):
    qfmva__jow = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return qfmva__jow._getvalue()


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
    lscll__dkgie = dict(join=join, join_axes=join_axes, keys=keys, levels=
        levels, names=names, verify_integrity=verify_integrity, sort=sort,
        copy=copy)
    gpid__sbvrc = dict(join='outer', join_axes=None, keys=None, levels=None,
        names=None, verify_integrity=False, sort=None, copy=True)
    check_unsupported_args('pandas.concat', lscll__dkgie, gpid__sbvrc,
        package_name='pandas', module_name='General')
    squbx__opjt = """def impl(objs, axis=0, join='outer', join_axes=None, ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False, sort=None, copy=True):
"""
    if axis == 1:
        if not isinstance(objs, types.BaseTuple):
            raise_bodo_error(
                'Only tuple argument for pd.concat(axis=1) expected')
        index = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len(objs[0]), 1, None)'
            )
        iibed__vfwcy = 0
        gek__uas = []
        names = []
        for i, urbt__dxvn in enumerate(objs.types):
            assert isinstance(urbt__dxvn, (SeriesType, DataFrameType))
            check_runtime_cols_unsupported(urbt__dxvn, 'pandas.concat()')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                urbt__dxvn, 'pandas.concat()')
            if isinstance(urbt__dxvn, SeriesType):
                names.append(str(iibed__vfwcy))
                iibed__vfwcy += 1
                gek__uas.append(
                    'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'
                    .format(i))
            else:
                names.extend(urbt__dxvn.columns)
                for yghrt__bek in range(len(urbt__dxvn.data)):
                    gek__uas.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, yghrt__bek))
        return bodo.hiframes.dataframe_impl._gen_init_df(squbx__opjt, names,
            ', '.join(gek__uas), index)
    if axis != 0:
        raise_bodo_error('pd.concat(): axis must be 0 or 1')
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        DataFrameType):
        assert all(isinstance(tjo__lpnf, DataFrameType) for tjo__lpnf in
            objs.types)
        ijdsh__vem = []
        for df in objs.types:
            check_runtime_cols_unsupported(df, 'pandas.concat()')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
                'pandas.concat()')
            ijdsh__vem.extend(df.columns)
        ijdsh__vem = list(dict.fromkeys(ijdsh__vem).keys())
        mrzbs__gisst = {}
        for iibed__vfwcy, qmal__nutcm in enumerate(ijdsh__vem):
            for i, df in enumerate(objs.types):
                if qmal__nutcm in df.column_index:
                    mrzbs__gisst[f'arr_typ{iibed__vfwcy}'] = df.data[df.
                        column_index[qmal__nutcm]]
                    break
        assert len(mrzbs__gisst) == len(ijdsh__vem)
        jixh__pwb = []
        for iibed__vfwcy, qmal__nutcm in enumerate(ijdsh__vem):
            args = []
            for i, df in enumerate(objs.types):
                if qmal__nutcm in df.column_index:
                    kif__qggx = df.column_index[qmal__nutcm]
                    args.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, kif__qggx))
                else:
                    args.append(
                        'bodo.libs.array_kernels.gen_na_array(len(objs[{}]), arr_typ{})'
                        .format(i, iibed__vfwcy))
            squbx__opjt += ('  A{} = bodo.libs.array_kernels.concat(({},))\n'
                .format(iibed__vfwcy, ', '.join(args)))
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
        return bodo.hiframes.dataframe_impl._gen_init_df(squbx__opjt,
            ijdsh__vem, ', '.join('A{}'.format(i) for i in range(len(
            ijdsh__vem))), index, mrzbs__gisst)
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        SeriesType):
        assert all(isinstance(tjo__lpnf, SeriesType) for tjo__lpnf in objs.
            types)
        squbx__opjt += ('  out_arr = bodo.libs.array_kernels.concat(({},))\n'
            .format(', '.join(
            'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'.format(
            i) for i in range(len(objs.types)))))
        if ignore_index:
            squbx__opjt += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            squbx__opjt += (
                """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)))))
        squbx__opjt += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        qmlq__zptb = {}
        exec(squbx__opjt, {'bodo': bodo, 'np': np, 'numba': numba}, qmlq__zptb)
        return qmlq__zptb['impl']
    if isinstance(objs, types.List) and isinstance(objs.dtype, DataFrameType):
        check_runtime_cols_unsupported(objs.dtype, 'pandas.concat()')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(objs.
            dtype, 'pandas.concat()')
        df_type = objs.dtype
        for iibed__vfwcy, qmal__nutcm in enumerate(df_type.columns):
            squbx__opjt += '  arrs{} = []\n'.format(iibed__vfwcy)
            squbx__opjt += '  for i in range(len(objs)):\n'
            squbx__opjt += '    df = objs[i]\n'
            squbx__opjt += (
                """    arrs{0}.append(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0}))
"""
                .format(iibed__vfwcy))
            squbx__opjt += (
                '  out_arr{0} = bodo.libs.array_kernels.concat(arrs{0})\n'.
                format(iibed__vfwcy))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr0), 1, None)'
                )
        else:
            squbx__opjt += '  arrs_index = []\n'
            squbx__opjt += '  for i in range(len(objs)):\n'
            squbx__opjt += '    df = objs[i]\n'
            squbx__opjt += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
            if objs.dtype.index.name_typ == types.none:
                name = None
            else:
                name = objs.dtype.index.name_typ.literal_value
            index = f"""bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index), {name!r})
"""
        return bodo.hiframes.dataframe_impl._gen_init_df(squbx__opjt,
            df_type.columns, ', '.join('out_arr{}'.format(i) for i in range
            (len(df_type.columns))), index)
    if isinstance(objs, types.List) and isinstance(objs.dtype, SeriesType):
        squbx__opjt += '  arrs = []\n'
        squbx__opjt += '  for i in range(len(objs)):\n'
        squbx__opjt += (
            '    arrs.append(bodo.hiframes.pd_series_ext.get_series_data(objs[i]))\n'
            )
        squbx__opjt += '  out_arr = bodo.libs.array_kernels.concat(arrs)\n'
        if ignore_index:
            squbx__opjt += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            squbx__opjt += '  arrs_index = []\n'
            squbx__opjt += '  for i in range(len(objs)):\n'
            squbx__opjt += '    S = objs[i]\n'
            squbx__opjt += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(S)))
"""
            squbx__opjt += """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index))
"""
        squbx__opjt += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        qmlq__zptb = {}
        exec(squbx__opjt, {'bodo': bodo, 'np': np, 'numba': numba}, qmlq__zptb)
        return qmlq__zptb['impl']
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
        cvxyu__znshw = df.copy(index=index, is_table_format=False)
        return signature(cvxyu__znshw, *args)


SortDummyTyper._no_unliteral = True


@lower_builtin(sort_values_dummy, types.VarArg(types.Any))
def lower_sort_values_dummy(context, builder, sig, args):
    if sig.return_type == types.none:
        return
    rqbi__hej = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return rqbi__hej._getvalue()


@overload_method(DataFrameType, 'itertuples', inline='always', no_unliteral
    =True)
def itertuples_overload(df, index=True, name='Pandas'):
    check_runtime_cols_unsupported(df, 'DataFrame.itertuples()')
    lscll__dkgie = dict(index=index, name=name)
    gpid__sbvrc = dict(index=True, name='Pandas')
    check_unsupported_args('DataFrame.itertuples', lscll__dkgie,
        gpid__sbvrc, package_name='pandas', module_name='DataFrame')

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
        mrzbs__gisst = (types.Array(types.int64, 1, 'C'),) + df.data
        zlt__pmorp = bodo.hiframes.dataframe_impl.DataFrameTupleIterator(
            columns, mrzbs__gisst)
        return signature(zlt__pmorp, *args)


@lower_builtin(itertuples_dummy, types.VarArg(types.Any))
def lower_itertuples_dummy(context, builder, sig, args):
    rqbi__hej = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return rqbi__hej._getvalue()


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
    rqbi__hej = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return rqbi__hej._getvalue()


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
    rqbi__hej = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return rqbi__hej._getvalue()


@numba.generated_jit(nopython=True)
def pivot_impl(index_tup, columns_tup, values_tup, pivot_values,
    index_names, columns_name, value_names, check_duplicates=True, parallel
    =False):
    if not is_overload_constant_bool(check_duplicates):
        raise BodoError(
            'pivot_impl(): check_duplicates must be a constant boolean')
    rmutz__waybp = get_overload_const_bool(check_duplicates)
    mqly__qnsnk = not is_overload_none(value_names)
    mvbl__zlne = isinstance(values_tup, types.UniTuple)
    if mvbl__zlne:
        ldr__qvszw = [to_nullable_type(values_tup.dtype)]
    else:
        ldr__qvszw = [to_nullable_type(hbusu__kky) for hbusu__kky in values_tup
            ]
    squbx__opjt = 'def impl(\n'
    squbx__opjt += """    index_tup, columns_tup, values_tup, pivot_values, index_names, columns_name, value_names, check_duplicates=True, parallel=False
"""
    squbx__opjt += '):\n'
    squbx__opjt += '    if parallel:\n'
    phymj__zkgir = ', '.join([f'array_to_info(index_tup[{i}])' for i in
        range(len(index_tup))] + [f'array_to_info(columns_tup[{i}])' for i in
        range(len(columns_tup))] + [f'array_to_info(values_tup[{i}])' for i in
        range(len(values_tup))])
    squbx__opjt += f'        info_list = [{phymj__zkgir}]\n'
    squbx__opjt += '        cpp_table = arr_info_list_to_table(info_list)\n'
    squbx__opjt += f"""        out_cpp_table = shuffle_table(cpp_table, {len(index_tup)}, parallel, 0)
"""
    xtzhm__gryk = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i}), index_tup[{i}])'
         for i in range(len(index_tup))])
    lsrnf__bee = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup)}), columns_tup[{i}])'
         for i in range(len(columns_tup))])
    oyhg__aypw = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup) + len(columns_tup)}), values_tup[{i}])'
         for i in range(len(values_tup))])
    squbx__opjt += f'        index_tup = ({xtzhm__gryk},)\n'
    squbx__opjt += f'        columns_tup = ({lsrnf__bee},)\n'
    squbx__opjt += f'        values_tup = ({oyhg__aypw},)\n'
    squbx__opjt += '        delete_table(cpp_table)\n'
    squbx__opjt += '        delete_table(out_cpp_table)\n'
    squbx__opjt += '    columns_arr = columns_tup[0]\n'
    if mvbl__zlne:
        squbx__opjt += '    values_arrs = [arr for arr in values_tup]\n'
    squbx__opjt += """    unique_index_arr_tup, row_vector = bodo.libs.array_ops.array_unique_vector_map(
"""
    squbx__opjt += '        index_tup\n'
    squbx__opjt += '    )\n'
    squbx__opjt += '    n_rows = len(unique_index_arr_tup[0])\n'
    squbx__opjt += '    num_values_arrays = len(values_tup)\n'
    squbx__opjt += '    n_unique_pivots = len(pivot_values)\n'
    if mvbl__zlne:
        squbx__opjt += '    n_cols = num_values_arrays * n_unique_pivots\n'
    else:
        squbx__opjt += '    n_cols = n_unique_pivots\n'
    squbx__opjt += '    col_map = {}\n'
    squbx__opjt += '    for i in range(n_unique_pivots):\n'
    squbx__opjt += (
        '        if bodo.libs.array_kernels.isna(pivot_values, i):\n')
    squbx__opjt += '            raise ValueError(\n'
    squbx__opjt += """                "DataFrame.pivot(): NA values in 'columns' array not supported\"
"""
    squbx__opjt += '            )\n'
    squbx__opjt += '        col_map[pivot_values[i]] = i\n'
    tny__rtzlf = False
    for i, gdqe__bkch in enumerate(ldr__qvszw):
        if is_str_arr_type(gdqe__bkch):
            tny__rtzlf = True
            squbx__opjt += f"""    len_arrs_{i} = [np.zeros(n_rows, np.int64) for _ in range(n_cols)]
"""
            squbx__opjt += f'    total_lens_{i} = np.zeros(n_cols, np.int64)\n'
    if tny__rtzlf:
        if rmutz__waybp:
            squbx__opjt += '    nbytes = (n_rows + 7) >> 3\n'
            squbx__opjt += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
        squbx__opjt += '    for i in range(len(columns_arr)):\n'
        squbx__opjt += '        col_name = columns_arr[i]\n'
        squbx__opjt += '        pivot_idx = col_map[col_name]\n'
        squbx__opjt += '        row_idx = row_vector[i]\n'
        if rmutz__waybp:
            squbx__opjt += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
            squbx__opjt += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
            squbx__opjt += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
            squbx__opjt += '        else:\n'
            squbx__opjt += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
        if mvbl__zlne:
            squbx__opjt += '        for j in range(num_values_arrays):\n'
            squbx__opjt += (
                '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
            squbx__opjt += '            len_arr = len_arrs_0[col_idx]\n'
            squbx__opjt += '            values_arr = values_arrs[j]\n'
            squbx__opjt += (
                '            if not bodo.libs.array_kernels.isna(values_arr, i):\n'
                )
            squbx__opjt += """                str_val_len = bodo.libs.str_arr_ext.get_str_arr_item_length(values_arr, i)
"""
            squbx__opjt += '                len_arr[row_idx] = str_val_len\n'
            squbx__opjt += (
                '                total_lens_0[col_idx] += str_val_len\n')
        else:
            for i, gdqe__bkch in enumerate(ldr__qvszw):
                if is_str_arr_type(gdqe__bkch):
                    squbx__opjt += f"""        if not bodo.libs.array_kernels.isna(values_tup[{i}], i):
"""
                    squbx__opjt += f"""            str_val_len_{i} = bodo.libs.str_arr_ext.get_str_arr_item_length(values_tup[{i}], i)
"""
                    squbx__opjt += f"""            len_arrs_{i}[pivot_idx][row_idx] = str_val_len_{i}
"""
                    squbx__opjt += (
                        f'            total_lens_{i}[pivot_idx] += str_val_len_{i}\n'
                        )
    for i, gdqe__bkch in enumerate(ldr__qvszw):
        if is_str_arr_type(gdqe__bkch):
            squbx__opjt += f'    data_arrs_{i} = [\n'
            squbx__opjt += (
                '        bodo.libs.str_arr_ext.gen_na_str_array_lens(\n')
            squbx__opjt += (
                f'            n_rows, total_lens_{i}[i], len_arrs_{i}[i]\n')
            squbx__opjt += '        )\n'
            squbx__opjt += '        for i in range(n_cols)\n'
            squbx__opjt += '    ]\n'
        else:
            squbx__opjt += f'    data_arrs_{i} = [\n'
            squbx__opjt += f"""        bodo.libs.array_kernels.gen_na_array(n_rows, data_arr_typ_{i})
"""
            squbx__opjt += '        for _ in range(n_cols)\n'
            squbx__opjt += '    ]\n'
    if not tny__rtzlf and rmutz__waybp:
        squbx__opjt += '    nbytes = (n_rows + 7) >> 3\n'
        squbx__opjt += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
    squbx__opjt += '    for i in range(len(columns_arr)):\n'
    squbx__opjt += '        col_name = columns_arr[i]\n'
    squbx__opjt += '        pivot_idx = col_map[col_name]\n'
    squbx__opjt += '        row_idx = row_vector[i]\n'
    if not tny__rtzlf and rmutz__waybp:
        squbx__opjt += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
        squbx__opjt += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
        squbx__opjt += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
        squbx__opjt += '        else:\n'
        squbx__opjt += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
    if mvbl__zlne:
        squbx__opjt += '        for j in range(num_values_arrays):\n'
        squbx__opjt += (
            '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
        squbx__opjt += '            col_arr = data_arrs_0[col_idx]\n'
        squbx__opjt += '            values_arr = values_arrs[j]\n'
        squbx__opjt += (
            '            if bodo.libs.array_kernels.isna(values_arr, i):\n')
        squbx__opjt += (
            '                bodo.libs.array_kernels.setna(col_arr, row_idx)\n'
            )
        squbx__opjt += '            else:\n'
        squbx__opjt += '                col_arr[row_idx] = values_arr[i]\n'
    else:
        for i, gdqe__bkch in enumerate(ldr__qvszw):
            squbx__opjt += f'        col_arr_{i} = data_arrs_{i}[pivot_idx]\n'
            squbx__opjt += (
                f'        if bodo.libs.array_kernels.isna(values_tup[{i}], i):\n'
                )
            squbx__opjt += (
                f'            bodo.libs.array_kernels.setna(col_arr_{i}, row_idx)\n'
                )
            squbx__opjt += f'        else:\n'
            squbx__opjt += (
                f'            col_arr_{i}[row_idx] = values_tup[{i}][i]\n')
    if len(index_tup) == 1:
        squbx__opjt += """    index = bodo.utils.conversion.index_from_array(unique_index_arr_tup[0], index_names[0])
"""
    else:
        squbx__opjt += """    index = bodo.hiframes.pd_multi_index_ext.init_multi_index(unique_index_arr_tup, index_names, None)
"""
    if mqly__qnsnk:
        squbx__opjt += '    num_rows = len(value_names) * len(pivot_values)\n'
        if is_str_arr_type(value_names):
            squbx__opjt += '    total_chars = 0\n'
            squbx__opjt += '    for i in range(len(value_names)):\n'
            squbx__opjt += """        value_name_str_len = bodo.libs.str_arr_ext.get_str_arr_item_length(value_names, i)
"""
            squbx__opjt += '        total_chars += value_name_str_len\n'
            squbx__opjt += """    new_value_names = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(pivot_values))
"""
        else:
            squbx__opjt += """    new_value_names = bodo.utils.utils.alloc_type(num_rows, value_names, (-1,))
"""
        if is_str_arr_type(pivot_values):
            squbx__opjt += '    total_chars = 0\n'
            squbx__opjt += '    for i in range(len(pivot_values)):\n'
            squbx__opjt += """        pivot_val_str_len = bodo.libs.str_arr_ext.get_str_arr_item_length(pivot_values, i)
"""
            squbx__opjt += '        total_chars += pivot_val_str_len\n'
            squbx__opjt += """    new_pivot_values = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(value_names))
"""
        else:
            squbx__opjt += """    new_pivot_values = bodo.utils.utils.alloc_type(num_rows, pivot_values, (-1,))
"""
        squbx__opjt += '    for i in range(len(value_names)):\n'
        squbx__opjt += '        for j in range(len(pivot_values)):\n'
        squbx__opjt += """            new_value_names[(i * len(pivot_values)) + j] = value_names[i]
"""
        squbx__opjt += """            new_pivot_values[(i * len(pivot_values)) + j] = pivot_values[j]
"""
        squbx__opjt += """    column_index = bodo.hiframes.pd_multi_index_ext.init_multi_index((new_value_names, new_pivot_values), (None, columns_name), None)
"""
    else:
        squbx__opjt += """    column_index =  bodo.utils.conversion.index_from_array(pivot_values, columns_name)
"""
    kefd__robb = ', '.join(f'data_arrs_{i}' for i in range(len(ldr__qvszw)))
    squbx__opjt += f"""    table = bodo.hiframes.table.init_runtime_table_from_lists(({kefd__robb},), n_rows)
"""
    squbx__opjt += (
        '    return bodo.hiframes.pd_dataframe_ext.init_runtime_cols_dataframe(\n'
        )
    squbx__opjt += '        (table,), index, column_index\n'
    squbx__opjt += '    )\n'
    qmlq__zptb = {}
    ezt__dvkex = {f'data_arr_typ_{i}': gdqe__bkch for i, gdqe__bkch in
        enumerate(ldr__qvszw)}
    riwgo__dcc = {'bodo': bodo, 'np': np, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'info_from_table': info_from_table, **ezt__dvkex}
    exec(squbx__opjt, riwgo__dcc, qmlq__zptb)
    impl = qmlq__zptb['impl']
    return impl


def gen_pandas_parquet_metadata(column_names, data_types, index,
    write_non_range_index_to_metadata, write_rangeindex_to_metadata,
    partition_cols=None, is_runtime_columns=False):
    dtlpt__jxcck = {}
    dtlpt__jxcck['columns'] = []
    if partition_cols is None:
        partition_cols = []
    for col_name, wejsi__erfml in zip(column_names, data_types):
        if col_name in partition_cols:
            continue
        hnixf__wnbz = None
        if isinstance(wejsi__erfml, bodo.DatetimeArrayType):
            cwm__ckxnw = 'datetimetz'
            vqwa__wfrn = 'datetime64[ns]'
            if isinstance(wejsi__erfml.tz, int):
                ewlup__nrcjs = (bodo.libs.pd_datetime_arr_ext.
                    nanoseconds_to_offset(wejsi__erfml.tz))
            else:
                ewlup__nrcjs = pd.DatetimeTZDtype(tz=wejsi__erfml.tz).tz
            hnixf__wnbz = {'timezone': pa.lib.tzinfo_to_string(ewlup__nrcjs)}
        elif isinstance(wejsi__erfml, types.Array
            ) or wejsi__erfml == boolean_array:
            cwm__ckxnw = vqwa__wfrn = wejsi__erfml.dtype.name
            if vqwa__wfrn.startswith('datetime'):
                cwm__ckxnw = 'datetime'
        elif is_str_arr_type(wejsi__erfml):
            cwm__ckxnw = 'unicode'
            vqwa__wfrn = 'object'
        elif wejsi__erfml == binary_array_type:
            cwm__ckxnw = 'bytes'
            vqwa__wfrn = 'object'
        elif isinstance(wejsi__erfml, DecimalArrayType):
            cwm__ckxnw = vqwa__wfrn = 'object'
        elif isinstance(wejsi__erfml, IntegerArrayType):
            kke__zkbi = wejsi__erfml.dtype.name
            if kke__zkbi.startswith('int'):
                cwm__ckxnw = 'Int' + kke__zkbi[3:]
            elif kke__zkbi.startswith('uint'):
                cwm__ckxnw = 'UInt' + kke__zkbi[4:]
            else:
                if is_runtime_columns:
                    col_name = 'Runtime determined column of type'
                raise BodoError(
                    'to_parquet(): unknown dtype in nullable Integer column {} {}'
                    .format(col_name, wejsi__erfml))
            vqwa__wfrn = wejsi__erfml.dtype.name
        elif wejsi__erfml == datetime_date_array_type:
            cwm__ckxnw = 'datetime'
            vqwa__wfrn = 'object'
        elif isinstance(wejsi__erfml, (StructArrayType, ArrayItemArrayType)):
            cwm__ckxnw = 'object'
            vqwa__wfrn = 'object'
        else:
            if is_runtime_columns:
                col_name = 'Runtime determined column of type'
            raise BodoError(
                'to_parquet(): unsupported column type for metadata generation : {} {}'
                .format(col_name, wejsi__erfml))
        lkp__uqbdx = {'name': col_name, 'field_name': col_name,
            'pandas_type': cwm__ckxnw, 'numpy_type': vqwa__wfrn, 'metadata':
            hnixf__wnbz}
        dtlpt__jxcck['columns'].append(lkp__uqbdx)
    if write_non_range_index_to_metadata:
        if isinstance(index, MultiIndexType):
            raise BodoError('to_parquet: MultiIndex not supported yet')
        if 'none' in index.name:
            zxpah__ijy = '__index_level_0__'
            mpepj__qly = None
        else:
            zxpah__ijy = '%s'
            mpepj__qly = '%s'
        dtlpt__jxcck['index_columns'] = [zxpah__ijy]
        dtlpt__jxcck['columns'].append({'name': mpepj__qly, 'field_name':
            zxpah__ijy, 'pandas_type': index.pandas_type_name, 'numpy_type':
            index.numpy_type_name, 'metadata': None})
    elif write_rangeindex_to_metadata:
        dtlpt__jxcck['index_columns'] = [{'kind': 'range', 'name': '%s',
            'start': '%d', 'stop': '%d', 'step': '%d'}]
    else:
        dtlpt__jxcck['index_columns'] = []
    dtlpt__jxcck['pandas_version'] = pd.__version__
    return dtlpt__jxcck


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
        qlalv__uynx = []
        for joqgp__xew in partition_cols:
            try:
                idx = df.columns.index(joqgp__xew)
            except ValueError as umt__puk:
                raise BodoError(
                    f'Partition column {joqgp__xew} is not in dataframe')
            qlalv__uynx.append(idx)
    else:
        partition_cols = None
    if not is_overload_none(index) and not is_overload_constant_bool(index):
        raise BodoError('to_parquet(): index must be a constant bool or None')
    if not is_overload_int(row_group_size):
        raise BodoError('to_parquet(): row_group_size must be integer')
    from bodo.io.parquet_pio import parquet_write_table_cpp, parquet_write_table_partitioned_cpp
    qbnp__owyvs = isinstance(df.index, bodo.hiframes.pd_index_ext.
        RangeIndexType)
    kciy__wzhlk = df.index is not None and (is_overload_true(_is_parallel) or
        not is_overload_true(_is_parallel) and not qbnp__owyvs)
    write_non_range_index_to_metadata = is_overload_true(index
        ) or is_overload_none(index) and (not qbnp__owyvs or
        is_overload_true(_is_parallel))
    write_rangeindex_to_metadata = is_overload_none(index
        ) and qbnp__owyvs and not is_overload_true(_is_parallel)
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
        tgov__ckyn = df.runtime_data_types
        zamm__xzim = len(tgov__ckyn)
        hnixf__wnbz = gen_pandas_parquet_metadata([''] * zamm__xzim,
            tgov__ckyn, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=True)
        mrkf__cyid = hnixf__wnbz['columns'][:zamm__xzim]
        hnixf__wnbz['columns'] = hnixf__wnbz['columns'][zamm__xzim:]
        mrkf__cyid = [json.dumps(xxdix__let).replace('""', '{0}') for
            xxdix__let in mrkf__cyid]
        yslyf__lgik = json.dumps(hnixf__wnbz)
        qokbh__aglj = '"columns": ['
        jrut__ziztw = yslyf__lgik.find(qokbh__aglj)
        if jrut__ziztw == -1:
            raise BodoError(
                'DataFrame.to_parquet(): Unexpected metadata string for runtime columns.  Please return the DataFrame to regular Python to update typing information.'
                )
        eiuzf__ahwm = jrut__ziztw + len(qokbh__aglj)
        bkuy__eha = yslyf__lgik[:eiuzf__ahwm]
        yslyf__lgik = yslyf__lgik[eiuzf__ahwm:]
        hti__ugz = len(hnixf__wnbz['columns'])
    else:
        yslyf__lgik = json.dumps(gen_pandas_parquet_metadata(df.columns, df
            .data, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=False))
    if not is_overload_true(_is_parallel) and qbnp__owyvs:
        yslyf__lgik = yslyf__lgik.replace('"%d"', '%d')
        if df.index.name == 'RangeIndexType(none)':
            yslyf__lgik = yslyf__lgik.replace('"%s"', '%s')
    if not df.is_table_format:
        gek__uas = ', '.join(
            'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
            .format(i) for i in range(len(df.columns)))
    squbx__opjt = """def df_to_parquet(df, path, engine='auto', compression='snappy', index=None, partition_cols=None, storage_options=None, row_group_size=-1, _is_parallel=False):
"""
    if df.is_table_format:
        squbx__opjt += '    py_table = get_dataframe_table(df)\n'
        squbx__opjt += (
            '    table = py_table_to_cpp_table(py_table, py_table_typ)\n')
    else:
        squbx__opjt += '    info_list = [{}]\n'.format(gek__uas)
        squbx__opjt += '    table = arr_info_list_to_table(info_list)\n'
    if df.has_runtime_cols:
        squbx__opjt += '    columns_index = get_dataframe_column_names(df)\n'
        squbx__opjt += '    names_arr = index_to_array(columns_index)\n'
        squbx__opjt += '    col_names = array_to_info(names_arr)\n'
    else:
        squbx__opjt += '    col_names = array_to_info(col_names_arr)\n'
    if is_overload_true(index) or is_overload_none(index) and kciy__wzhlk:
        squbx__opjt += """    index_col = array_to_info(index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
        uvst__ymi = True
    else:
        squbx__opjt += '    index_col = array_to_info(np.empty(0))\n'
        uvst__ymi = False
    if df.has_runtime_cols:
        squbx__opjt += '    columns_lst = []\n'
        squbx__opjt += '    num_cols = 0\n'
        for i in range(len(df.runtime_data_types)):
            squbx__opjt += f'    for _ in range(len(py_table.block_{i})):\n'
            squbx__opjt += f"""        columns_lst.append({mrkf__cyid[i]!r}.replace('{{0}}', '"' + names_arr[num_cols] + '"'))
"""
            squbx__opjt += '        num_cols += 1\n'
        if hti__ugz:
            squbx__opjt += "    columns_lst.append('')\n"
        squbx__opjt += '    columns_str = ", ".join(columns_lst)\n'
        squbx__opjt += ('    metadata = """' + bkuy__eha +
            '""" + columns_str + """' + yslyf__lgik + '"""\n')
    else:
        squbx__opjt += '    metadata = """' + yslyf__lgik + '"""\n'
    squbx__opjt += '    if compression is None:\n'
    squbx__opjt += "        compression = 'none'\n"
    squbx__opjt += '    if df.index.name is not None:\n'
    squbx__opjt += '        name_ptr = df.index.name\n'
    squbx__opjt += '    else:\n'
    squbx__opjt += "        name_ptr = 'null'\n"
    squbx__opjt += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(path, parallel=_is_parallel)
"""
    enycw__wdvq = None
    if partition_cols:
        enycw__wdvq = pd.array([col_name for col_name in df.columns if 
            col_name not in partition_cols])
        ofue__mtu = ', '.join(
            f'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype.categories.values)'
             for i in range(len(df.columns)) if isinstance(df.data[i],
            CategoricalArrayType) and i in qlalv__uynx)
        if ofue__mtu:
            squbx__opjt += '    cat_info_list = [{}]\n'.format(ofue__mtu)
            squbx__opjt += (
                '    cat_table = arr_info_list_to_table(cat_info_list)\n')
        else:
            squbx__opjt += '    cat_table = table\n'
        squbx__opjt += (
            '    col_names_no_partitions = array_to_info(col_names_no_parts_arr)\n'
            )
        squbx__opjt += (
            f'    part_cols_idxs = np.array({qlalv__uynx}, dtype=np.int32)\n')
        squbx__opjt += (
            '    parquet_write_table_partitioned_cpp(unicode_to_utf8(path),\n')
        squbx__opjt += """                            table, col_names, col_names_no_partitions, cat_table,
"""
        squbx__opjt += (
            '                            part_cols_idxs.ctypes, len(part_cols_idxs),\n'
            )
        squbx__opjt += (
            '                            unicode_to_utf8(compression),\n')
        squbx__opjt += '                            _is_parallel,\n'
        squbx__opjt += (
            '                            unicode_to_utf8(bucket_region),\n')
        squbx__opjt += '                            row_group_size)\n'
        squbx__opjt += '    delete_table_decref_arrays(table)\n'
        squbx__opjt += '    delete_info_decref_array(index_col)\n'
        squbx__opjt += (
            '    delete_info_decref_array(col_names_no_partitions)\n')
        squbx__opjt += '    delete_info_decref_array(col_names)\n'
        if ofue__mtu:
            squbx__opjt += '    delete_table_decref_arrays(cat_table)\n'
    elif write_rangeindex_to_metadata:
        squbx__opjt += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        squbx__opjt += (
            '                            table, col_names, index_col,\n')
        squbx__opjt += '                            ' + str(uvst__ymi) + ',\n'
        squbx__opjt += (
            '                            unicode_to_utf8(metadata),\n')
        squbx__opjt += (
            '                            unicode_to_utf8(compression),\n')
        squbx__opjt += (
            '                            _is_parallel, 1, df.index.start,\n')
        squbx__opjt += (
            '                            df.index.stop, df.index.step,\n')
        squbx__opjt += (
            '                            unicode_to_utf8(name_ptr),\n')
        squbx__opjt += (
            '                            unicode_to_utf8(bucket_region),\n')
        squbx__opjt += '                            row_group_size)\n'
        squbx__opjt += '    delete_table_decref_arrays(table)\n'
        squbx__opjt += '    delete_info_decref_array(index_col)\n'
        squbx__opjt += '    delete_info_decref_array(col_names)\n'
    else:
        squbx__opjt += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        squbx__opjt += (
            '                            table, col_names, index_col,\n')
        squbx__opjt += '                            ' + str(uvst__ymi) + ',\n'
        squbx__opjt += (
            '                            unicode_to_utf8(metadata),\n')
        squbx__opjt += (
            '                            unicode_to_utf8(compression),\n')
        squbx__opjt += (
            '                            _is_parallel, 0, 0, 0, 0,\n')
        squbx__opjt += (
            '                            unicode_to_utf8(name_ptr),\n')
        squbx__opjt += (
            '                            unicode_to_utf8(bucket_region),\n')
        squbx__opjt += '                            row_group_size)\n'
        squbx__opjt += '    delete_table_decref_arrays(table)\n'
        squbx__opjt += '    delete_info_decref_array(index_col)\n'
        squbx__opjt += '    delete_info_decref_array(col_names)\n'
    qmlq__zptb = {}
    if df.has_runtime_cols:
        fhbay__ciype = None
    else:
        for rmvzu__dppuk in df.columns:
            if not isinstance(rmvzu__dppuk, str):
                raise BodoError(
                    'DataFrame.to_parquet(): parquet must have string column names'
                    )
        fhbay__ciype = pd.array(df.columns)
    exec(squbx__opjt, {'np': np, 'bodo': bodo, 'unicode_to_utf8':
        unicode_to_utf8, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'str_arr_from_sequence': str_arr_from_sequence,
        'parquet_write_table_cpp': parquet_write_table_cpp,
        'parquet_write_table_partitioned_cpp':
        parquet_write_table_partitioned_cpp, 'index_to_array':
        index_to_array, 'delete_info_decref_array':
        delete_info_decref_array, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'col_names_arr': fhbay__ciype,
        'py_table_to_cpp_table': py_table_to_cpp_table, 'py_table_typ': df.
        table_type, 'get_dataframe_table': get_dataframe_table,
        'col_names_no_parts_arr': enycw__wdvq, 'get_dataframe_column_names':
        get_dataframe_column_names, 'fix_arr_dtype': fix_arr_dtype,
        'decode_if_dict_array': decode_if_dict_array,
        'decode_if_dict_table': decode_if_dict_table}, qmlq__zptb)
    agfob__qfca = qmlq__zptb['df_to_parquet']
    return agfob__qfca


def to_sql_exception_guard(df, name, con, schema=None, if_exists='fail',
    index=True, index_label=None, chunksize=None, dtype=None, method=None,
    _is_table_create=False, _is_parallel=False):
    kqm__lbgur = 'all_ok'
    ibud__aukhm, fttl__htvx = bodo.ir.sql_ext.parse_dbtype(con)
    if _is_parallel and bodo.get_rank() == 0:
        ogtjo__cmz = 100
        if chunksize is None:
            stcz__zjlzq = ogtjo__cmz
        else:
            stcz__zjlzq = min(chunksize, ogtjo__cmz)
        if _is_table_create:
            df = df.iloc[:stcz__zjlzq, :]
        else:
            df = df.iloc[stcz__zjlzq:, :]
            if len(df) == 0:
                return kqm__lbgur
    xoaoh__pqxma = df.columns
    try:
        if ibud__aukhm == 'snowflake':
            if fttl__htvx and con.count(fttl__htvx) == 1:
                con = con.replace(fttl__htvx, quote(fttl__htvx))
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
                df.columns = [(qmal__nutcm.upper() if qmal__nutcm.islower()
                     else qmal__nutcm) for qmal__nutcm in df.columns]
            except ImportError as umt__puk:
                kqm__lbgur = (
                    "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires both snowflake-sqlalchemy and snowflake-connector-python. These can be installed by calling 'conda install -c conda-forge snowflake-sqlalchemy snowflake-connector-python' or 'pip install snowflake-sqlalchemy snowflake-connector-python'."
                    )
                return kqm__lbgur
        if ibud__aukhm == 'oracle':
            import sqlalchemy as sa
            fhfo__featp = bodo.typeof(df)
            kgt__ruzqq = {}
            for qmal__nutcm, ghi__neys in zip(fhfo__featp.columns,
                fhfo__featp.data):
                if df[qmal__nutcm].dtype == 'object':
                    if ghi__neys == datetime_date_array_type:
                        kgt__ruzqq[qmal__nutcm] = sa.types.Date
                    elif ghi__neys == bodo.string_array_type:
                        kgt__ruzqq[qmal__nutcm] = sa.types.VARCHAR(df[
                            qmal__nutcm].str.len().max())
            dtype = kgt__ruzqq
        try:
            df.to_sql(name, con, schema, if_exists, index, index_label,
                chunksize, dtype, method)
        except Exception as mbzpy__iubis:
            kqm__lbgur = mbzpy__iubis.args[0]
        return kqm__lbgur
    finally:
        df.columns = xoaoh__pqxma


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
        hsors__ywc = bodo.libs.distributed_api.get_rank()
        kqm__lbgur = 'unset'
        if hsors__ywc != 0:
            kqm__lbgur = bcast_scalar(kqm__lbgur)
        elif hsors__ywc == 0:
            kqm__lbgur = to_sql_exception_guard_encaps(df, name, con,
                schema, if_exists, index, index_label, chunksize, dtype,
                method, True, _is_parallel)
            kqm__lbgur = bcast_scalar(kqm__lbgur)
        if_exists = 'append'
        if _is_parallel and kqm__lbgur == 'all_ok':
            kqm__lbgur = to_sql_exception_guard_encaps(df, name, con,
                schema, if_exists, index, index_label, chunksize, dtype,
                method, False, _is_parallel)
        if kqm__lbgur != 'all_ok':
            print('err_msg=', kqm__lbgur)
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
        nnvlk__ldz = get_overload_const_str(path_or_buf)
        if nnvlk__ldz.endswith(('.gz', '.bz2', '.zip', '.xz')):
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
        efmdz__ghdj = bodo.io.fs_io.get_s3_bucket_region_njit(path_or_buf,
            parallel=False)
        if lines and orient == 'records':
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, True,
                unicode_to_utf8(efmdz__ghdj))
            bodo.utils.utils.check_and_propagate_cpp_exception()
        else:
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, False,
                unicode_to_utf8(efmdz__ghdj))
            bodo.utils.utils.check_and_propagate_cpp_exception()
    return _impl


@overload(pd.get_dummies, inline='always', no_unliteral=True)
def get_dummies(data, prefix=None, prefix_sep='_', dummy_na=False, columns=
    None, sparse=False, drop_first=False, dtype=None):
    jsmk__geabw = {'prefix': prefix, 'prefix_sep': prefix_sep, 'dummy_na':
        dummy_na, 'columns': columns, 'sparse': sparse, 'drop_first':
        drop_first, 'dtype': dtype}
    jbm__adoab = {'prefix': None, 'prefix_sep': '_', 'dummy_na': False,
        'columns': None, 'sparse': False, 'drop_first': False, 'dtype': None}
    check_unsupported_args('pandas.get_dummies', jsmk__geabw, jbm__adoab,
        package_name='pandas', module_name='General')
    if not categorical_can_construct_dataframe(data):
        raise BodoError(
            'pandas.get_dummies() only support categorical data types with explicitly known categories'
            )
    squbx__opjt = """def impl(data, prefix=None, prefix_sep='_', dummy_na=False, columns=None, sparse=False, drop_first=False, dtype=None,):
"""
    if isinstance(data, SeriesType):
        tbqwc__rhxh = data.data.dtype.categories
        squbx__opjt += (
            '  data_values = bodo.hiframes.pd_series_ext.get_series_data(data)\n'
            )
    else:
        tbqwc__rhxh = data.dtype.categories
        squbx__opjt += '  data_values = data\n'
    uvw__eyln = len(tbqwc__rhxh)
    squbx__opjt += """  codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(data_values)
"""
    squbx__opjt += '  numba.parfors.parfor.init_prange()\n'
    squbx__opjt += '  n = len(data_values)\n'
    for i in range(uvw__eyln):
        squbx__opjt += '  data_arr_{} = np.empty(n, np.uint8)\n'.format(i)
    squbx__opjt += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    squbx__opjt += '      if bodo.libs.array_kernels.isna(data_values, i):\n'
    for yghrt__bek in range(uvw__eyln):
        squbx__opjt += '          data_arr_{}[i] = 0\n'.format(yghrt__bek)
    squbx__opjt += '      else:\n'
    for paz__goku in range(uvw__eyln):
        squbx__opjt += '          data_arr_{0}[i] = codes[i] == {0}\n'.format(
            paz__goku)
    gek__uas = ', '.join(f'data_arr_{i}' for i in range(uvw__eyln))
    index = 'bodo.hiframes.pd_index_ext.init_range_index(0, n, 1, None)'
    if isinstance(tbqwc__rhxh[0], np.datetime64):
        tbqwc__rhxh = tuple(pd.Timestamp(qmal__nutcm) for qmal__nutcm in
            tbqwc__rhxh)
    elif isinstance(tbqwc__rhxh[0], np.timedelta64):
        tbqwc__rhxh = tuple(pd.Timedelta(qmal__nutcm) for qmal__nutcm in
            tbqwc__rhxh)
    return bodo.hiframes.dataframe_impl._gen_init_df(squbx__opjt,
        tbqwc__rhxh, gek__uas, index)


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
    for yswnr__ihdcb in pd_unsupported:
        nzl__fwuvr = mod_name + '.' + yswnr__ihdcb.__name__
        overload(yswnr__ihdcb, no_unliteral=True)(create_unsupported_overload
            (nzl__fwuvr))


def _install_dataframe_unsupported():
    for qozu__khdck in dataframe_unsupported_attrs:
        wes__dux = 'DataFrame.' + qozu__khdck
        overload_attribute(DataFrameType, qozu__khdck)(
            create_unsupported_overload(wes__dux))
    for nzl__fwuvr in dataframe_unsupported:
        wes__dux = 'DataFrame.' + nzl__fwuvr + '()'
        overload_method(DataFrameType, nzl__fwuvr)(create_unsupported_overload
            (wes__dux))


_install_pd_unsupported('pandas', pd_unsupported)
_install_pd_unsupported('pandas.util', pd_util_unsupported)
_install_dataframe_unsupported()
