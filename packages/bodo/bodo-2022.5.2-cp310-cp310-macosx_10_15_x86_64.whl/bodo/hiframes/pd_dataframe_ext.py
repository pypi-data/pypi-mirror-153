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
            ney__blll = f'{len(self.data)} columns of types {set(self.data)}'
            fxrbj__jsfe = (
                f"('{self.columns[0]}', '{self.columns[1]}', ..., '{self.columns[-1]}')"
                )
            return (
                f'dataframe({ney__blll}, {self.index}, {fxrbj__jsfe}, {self.dist}, {self.is_table_format})'
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
        return {wdufm__wfsal: i for i, wdufm__wfsal in enumerate(self.columns)}

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
            fpauf__bbst = (self.index if self.index == other.index else
                self.index.unify(typingctx, other.index))
            data = tuple(etdg__capp.unify(typingctx, khxw__xipc) if 
                etdg__capp != khxw__xipc else etdg__capp for etdg__capp,
                khxw__xipc in zip(self.data, other.data))
            dist = Distribution(min(self.dist.value, other.dist.value))
            if fpauf__bbst is not None and None not in data:
                return DataFrameType(data, fpauf__bbst, self.columns, dist,
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
        return all(etdg__capp.is_precise() for etdg__capp in self.data
            ) and self.index.is_precise()

    def replace_col_type(self, col_name, new_type):
        if col_name not in self.columns:
            raise ValueError(
                f"DataFrameType.replace_col_type replaced column must be found in the DataFrameType. '{col_name}' not found in DataFrameType with columns {self.columns}"
                )
        fev__hvzp = self.columns.index(col_name)
        abb__hyl = tuple(list(self.data[:fev__hvzp]) + [new_type] + list(
            self.data[fev__hvzp + 1:]))
        return DataFrameType(abb__hyl, self.index, self.columns, self.dist,
            self.is_table_format)


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
        tzzj__nxji = [('data', data_typ), ('index', fe_type.df_type.index),
            ('parent', types.pyobject)]
        if fe_type.df_type.has_runtime_cols:
            tzzj__nxji.append(('columns', fe_type.df_type.runtime_colname_typ))
        super(DataFramePayloadModel, self).__init__(dmm, fe_type, tzzj__nxji)


@register_model(DataFrameType)
class DataFrameModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = DataFramePayloadType(fe_type)
        tzzj__nxji = [('meminfo', types.MemInfoPointer(payload_type)), (
            'parent', types.pyobject)]
        super(DataFrameModel, self).__init__(dmm, fe_type, tzzj__nxji)


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
        matg__dnf = 'n',
        iqwjv__rbu = {'n': 5}
        cqbq__dpb, rwht__nvbf = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, matg__dnf, iqwjv__rbu)
        sdv__jgyhp = rwht__nvbf[0]
        if not is_overload_int(sdv__jgyhp):
            raise BodoError(f"{func_name}(): 'n' must be an Integer")
        qflv__qhjys = df.copy(is_table_format=False)
        return qflv__qhjys(*rwht__nvbf).replace(pysig=cqbq__dpb)

    @bound_function('df.corr')
    def resolve_corr(self, df, args, kws):
        func_name = 'DataFrame.corr'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        dygy__abjx = (df,) + args
        matg__dnf = 'df', 'method', 'min_periods'
        iqwjv__rbu = {'method': 'pearson', 'min_periods': 1}
        tink__emmx = 'method',
        cqbq__dpb, rwht__nvbf = bodo.utils.typing.fold_typing_args(func_name,
            dygy__abjx, kws, matg__dnf, iqwjv__rbu, tink__emmx)
        nzbre__gxwfv = rwht__nvbf[2]
        if not is_overload_int(nzbre__gxwfv):
            raise BodoError(f"{func_name}(): 'min_periods' must be an Integer")
        tka__xtkv = []
        ucj__yqyyr = []
        for wdufm__wfsal, lca__uol in zip(df.columns, df.data):
            if bodo.utils.typing._is_pandas_numeric_dtype(lca__uol.dtype):
                tka__xtkv.append(wdufm__wfsal)
                ucj__yqyyr.append(types.Array(types.float64, 1, 'A'))
        if len(tka__xtkv) == 0:
            raise_bodo_error('DataFrame.corr(): requires non-empty dataframe')
        ucj__yqyyr = tuple(ucj__yqyyr)
        tka__xtkv = tuple(tka__xtkv)
        index_typ = bodo.utils.typing.type_col_to_index(tka__xtkv)
        qflv__qhjys = DataFrameType(ucj__yqyyr, index_typ, tka__xtkv)
        return qflv__qhjys(*rwht__nvbf).replace(pysig=cqbq__dpb)

    @bound_function('df.pipe', no_unliteral=True)
    def resolve_pipe(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.pipe()')
        return bodo.hiframes.pd_groupby_ext.resolve_obj_pipe(self, df, args,
            kws, 'DataFrame')

    @bound_function('df.apply', no_unliteral=True)
    def resolve_apply(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.apply()')
        kws = dict(kws)
        pfpz__fixhc = args[0] if len(args) > 0 else kws.pop('func', None)
        axis = args[1] if len(args) > 1 else kws.pop('axis', types.literal(0))
        khk__bsao = args[2] if len(args) > 2 else kws.pop('raw', types.
            literal(False))
        wbfup__kaea = args[3] if len(args) > 3 else kws.pop('result_type',
            types.none)
        omfqk__viyoa = args[4] if len(args) > 4 else kws.pop('args', types.
            Tuple([]))
        cwf__zmn = dict(raw=khk__bsao, result_type=wbfup__kaea)
        trvqw__cum = dict(raw=False, result_type=None)
        check_unsupported_args('Dataframe.apply', cwf__zmn, trvqw__cum,
            package_name='pandas', module_name='DataFrame')
        jevvd__epjm = True
        if types.unliteral(pfpz__fixhc) == types.unicode_type:
            if not is_overload_constant_str(pfpz__fixhc):
                raise BodoError(
                    f'DataFrame.apply(): string argument (for builtins) must be a compile time constant'
                    )
            jevvd__epjm = False
        if not is_overload_constant_int(axis):
            raise BodoError(
                'Dataframe.apply(): axis argument must be a compile time constant.'
                )
        pxb__affjp = get_overload_const_int(axis)
        if jevvd__epjm and pxb__affjp != 1:
            raise BodoError(
                'Dataframe.apply(): only axis=1 supported for user-defined functions'
                )
        elif pxb__affjp not in (0, 1):
            raise BodoError('Dataframe.apply(): axis must be either 0 or 1')
        jrxdc__htke = []
        for arr_typ in df.data:
            mkr__tkrfy = SeriesType(arr_typ.dtype, arr_typ, df.index,
                string_type)
            xhhd__gzbor = self.context.resolve_function_type(operator.
                getitem, (SeriesIlocType(mkr__tkrfy), types.int64), {}
                ).return_type
            jrxdc__htke.append(xhhd__gzbor)
        nho__rplet = types.none
        ljvr__hgz = HeterogeneousIndexType(types.BaseTuple.from_types(tuple
            (types.literal(wdufm__wfsal) for wdufm__wfsal in df.columns)), None
            )
        coqjo__mbb = types.BaseTuple.from_types(jrxdc__htke)
        kvoso__fhax = types.Tuple([types.bool_] * len(coqjo__mbb))
        qrnlb__huxuy = bodo.NullableTupleType(coqjo__mbb, kvoso__fhax)
        zuw__jcjig = df.index.dtype
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df.index,
            'DataFrame.apply()')
        if zuw__jcjig == types.NPDatetime('ns'):
            zuw__jcjig = bodo.pd_timestamp_type
        if zuw__jcjig == types.NPTimedelta('ns'):
            zuw__jcjig = bodo.pd_timedelta_type
        if is_heterogeneous_tuple_type(coqjo__mbb):
            ysptu__hgcfc = HeterogeneousSeriesType(qrnlb__huxuy, ljvr__hgz,
                zuw__jcjig)
        else:
            ysptu__hgcfc = SeriesType(coqjo__mbb.dtype, qrnlb__huxuy,
                ljvr__hgz, zuw__jcjig)
        pdux__ckux = ysptu__hgcfc,
        if omfqk__viyoa is not None:
            pdux__ckux += tuple(omfqk__viyoa.types)
        try:
            if not jevvd__epjm:
                mmt__blgjz = bodo.utils.transform.get_udf_str_return_type(df,
                    get_overload_const_str(pfpz__fixhc), self.context,
                    'DataFrame.apply', axis if pxb__affjp == 1 else None)
            else:
                mmt__blgjz = get_const_func_output_type(pfpz__fixhc,
                    pdux__ckux, kws, self.context, numba.core.registry.
                    cpu_target.target_context)
        except Exception as rrd__xnp:
            raise_bodo_error(get_udf_error_msg('DataFrame.apply()', rrd__xnp))
        if jevvd__epjm:
            if not (is_overload_constant_int(axis) and 
                get_overload_const_int(axis) == 1):
                raise BodoError(
                    'Dataframe.apply(): only user-defined functions with axis=1 supported'
                    )
            if isinstance(mmt__blgjz, (SeriesType, HeterogeneousSeriesType)
                ) and mmt__blgjz.const_info is None:
                raise BodoError(
                    'Invalid Series output in UDF (Series with constant length and constant Index value expected)'
                    )
            if isinstance(mmt__blgjz, HeterogeneousSeriesType):
                tymyj__xgvlj, opv__hkj = mmt__blgjz.const_info
                if isinstance(mmt__blgjz.data, bodo.libs.nullable_tuple_ext
                    .NullableTupleType):
                    iow__djp = mmt__blgjz.data.tuple_typ.types
                elif isinstance(mmt__blgjz.data, types.Tuple):
                    iow__djp = mmt__blgjz.data.types
                else:
                    raise_bodo_error(
                        'df.apply(): Unexpected Series return type for Heterogeneous data'
                        )
                wyyi__kyb = tuple(to_nullable_type(dtype_to_array_type(
                    tavg__bsdta)) for tavg__bsdta in iow__djp)
                mzuyf__qsgyo = DataFrameType(wyyi__kyb, df.index, opv__hkj)
            elif isinstance(mmt__blgjz, SeriesType):
                ccnv__ngm, opv__hkj = mmt__blgjz.const_info
                wyyi__kyb = tuple(to_nullable_type(dtype_to_array_type(
                    mmt__blgjz.dtype)) for tymyj__xgvlj in range(ccnv__ngm))
                mzuyf__qsgyo = DataFrameType(wyyi__kyb, df.index, opv__hkj)
            else:
                ruoeb__kspck = get_udf_out_arr_type(mmt__blgjz)
                mzuyf__qsgyo = SeriesType(ruoeb__kspck.dtype, ruoeb__kspck,
                    df.index, None)
        else:
            mzuyf__qsgyo = mmt__blgjz
        fzto__wajz = ', '.join("{} = ''".format(etdg__capp) for etdg__capp in
            kws.keys())
        pvtk__uytsz = f"""def apply_stub(func, axis=0, raw=False, result_type=None, args=(), {fzto__wajz}):
"""
        pvtk__uytsz += '    pass\n'
        oepi__zgc = {}
        exec(pvtk__uytsz, {}, oepi__zgc)
        gsa__chqnw = oepi__zgc['apply_stub']
        cqbq__dpb = numba.core.utils.pysignature(gsa__chqnw)
        udnyr__zgtgq = (pfpz__fixhc, axis, khk__bsao, wbfup__kaea, omfqk__viyoa
            ) + tuple(kws.values())
        return signature(mzuyf__qsgyo, *udnyr__zgtgq).replace(pysig=cqbq__dpb)

    @bound_function('df.plot', no_unliteral=True)
    def resolve_plot(self, df, args, kws):
        func_name = 'DataFrame.plot'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        matg__dnf = ('x', 'y', 'kind', 'figsize', 'ax', 'subplots',
            'sharex', 'sharey', 'layout', 'use_index', 'title', 'grid',
            'legend', 'style', 'logx', 'logy', 'loglog', 'xticks', 'yticks',
            'xlim', 'ylim', 'rot', 'fontsize', 'colormap', 'table', 'yerr',
            'xerr', 'secondary_y', 'sort_columns', 'xlabel', 'ylabel',
            'position', 'stacked', 'mark_right', 'include_bool', 'backend')
        iqwjv__rbu = {'x': None, 'y': None, 'kind': 'line', 'figsize': None,
            'ax': None, 'subplots': False, 'sharex': None, 'sharey': False,
            'layout': None, 'use_index': True, 'title': None, 'grid': None,
            'legend': True, 'style': None, 'logx': False, 'logy': False,
            'loglog': False, 'xticks': None, 'yticks': None, 'xlim': None,
            'ylim': None, 'rot': None, 'fontsize': None, 'colormap': None,
            'table': False, 'yerr': None, 'xerr': None, 'secondary_y': 
            False, 'sort_columns': False, 'xlabel': None, 'ylabel': None,
            'position': 0.5, 'stacked': False, 'mark_right': True,
            'include_bool': False, 'backend': None}
        tink__emmx = ('subplots', 'sharex', 'sharey', 'layout', 'use_index',
            'grid', 'style', 'logx', 'logy', 'loglog', 'xlim', 'ylim',
            'rot', 'colormap', 'table', 'yerr', 'xerr', 'sort_columns',
            'secondary_y', 'colorbar', 'position', 'stacked', 'mark_right',
            'include_bool', 'backend')
        cqbq__dpb, rwht__nvbf = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, matg__dnf, iqwjv__rbu, tink__emmx)
        xdp__deb = rwht__nvbf[2]
        if not is_overload_constant_str(xdp__deb):
            raise BodoError(
                f"{func_name}: kind must be a constant string and one of ('line', 'scatter')."
                )
        omgtf__vzpy = rwht__nvbf[0]
        if not is_overload_none(omgtf__vzpy) and not (is_overload_int(
            omgtf__vzpy) or is_overload_constant_str(omgtf__vzpy)):
            raise BodoError(
                f'{func_name}: x must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(omgtf__vzpy):
            ugmyh__ngjt = get_overload_const_str(omgtf__vzpy)
            if ugmyh__ngjt not in df.columns:
                raise BodoError(f'{func_name}: {ugmyh__ngjt} column not found.'
                    )
        elif is_overload_int(omgtf__vzpy):
            kqir__lxs = get_overload_const_int(omgtf__vzpy)
            if kqir__lxs > len(df.columns):
                raise BodoError(
                    f'{func_name}: x: {kqir__lxs} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            omgtf__vzpy = df.columns[omgtf__vzpy]
        tbnlq__lxrh = rwht__nvbf[1]
        if not is_overload_none(tbnlq__lxrh) and not (is_overload_int(
            tbnlq__lxrh) or is_overload_constant_str(tbnlq__lxrh)):
            raise BodoError(
                'df.plot(): y must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(tbnlq__lxrh):
            gjqtf__ice = get_overload_const_str(tbnlq__lxrh)
            if gjqtf__ice not in df.columns:
                raise BodoError(f'{func_name}: {gjqtf__ice} column not found.')
        elif is_overload_int(tbnlq__lxrh):
            qdxop__fvdkl = get_overload_const_int(tbnlq__lxrh)
            if qdxop__fvdkl > len(df.columns):
                raise BodoError(
                    f'{func_name}: y: {qdxop__fvdkl} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            tbnlq__lxrh = df.columns[tbnlq__lxrh]
        aol__tszo = rwht__nvbf[3]
        if not is_overload_none(aol__tszo) and not is_tuple_like_type(aol__tszo
            ):
            raise BodoError(
                f'{func_name}: figsize must be a constant numeric tuple (width, height) or None.'
                )
        juee__cqpca = rwht__nvbf[10]
        if not is_overload_none(juee__cqpca) and not is_overload_constant_str(
            juee__cqpca):
            raise BodoError(
                f'{func_name}: title must be a constant string or None.')
        bhrwg__tqs = rwht__nvbf[12]
        if not is_overload_bool(bhrwg__tqs):
            raise BodoError(f'{func_name}: legend must be a boolean type.')
        gdq__ltxo = rwht__nvbf[17]
        if not is_overload_none(gdq__ltxo) and not is_tuple_like_type(gdq__ltxo
            ):
            raise BodoError(
                f'{func_name}: xticks must be a constant tuple or None.')
        yin__pkbgu = rwht__nvbf[18]
        if not is_overload_none(yin__pkbgu) and not is_tuple_like_type(
            yin__pkbgu):
            raise BodoError(
                f'{func_name}: yticks must be a constant tuple or None.')
        lof__uvc = rwht__nvbf[22]
        if not is_overload_none(lof__uvc) and not is_overload_int(lof__uvc):
            raise BodoError(
                f'{func_name}: fontsize must be an integer or None.')
        wumr__xmyl = rwht__nvbf[29]
        if not is_overload_none(wumr__xmyl) and not is_overload_constant_str(
            wumr__xmyl):
            raise BodoError(
                f'{func_name}: xlabel must be a constant string or None.')
        cok__fci = rwht__nvbf[30]
        if not is_overload_none(cok__fci) and not is_overload_constant_str(
            cok__fci):
            raise BodoError(
                f'{func_name}: ylabel must be a constant string or None.')
        gnjdp__ickj = types.List(types.mpl_line_2d_type)
        xdp__deb = get_overload_const_str(xdp__deb)
        if xdp__deb == 'scatter':
            if is_overload_none(omgtf__vzpy) and is_overload_none(tbnlq__lxrh):
                raise BodoError(
                    f'{func_name}: {xdp__deb} requires an x and y column.')
            elif is_overload_none(omgtf__vzpy):
                raise BodoError(f'{func_name}: {xdp__deb} x column is missing.'
                    )
            elif is_overload_none(tbnlq__lxrh):
                raise BodoError(f'{func_name}: {xdp__deb} y column is missing.'
                    )
            gnjdp__ickj = types.mpl_path_collection_type
        elif xdp__deb != 'line':
            raise BodoError(f'{func_name}: {xdp__deb} plot is not supported.')
        return signature(gnjdp__ickj, *rwht__nvbf).replace(pysig=cqbq__dpb)

    def generic_resolve(self, df, attr):
        if self._is_existing_attr(attr):
            return
        check_runtime_cols_unsupported(df,
            'Acessing DataFrame columns by attribute')
        if attr in df.columns:
            tosc__axtqa = df.columns.index(attr)
            arr_typ = df.data[tosc__axtqa]
            return SeriesType(arr_typ.dtype, arr_typ, df.index, types.
                StringLiteral(attr))
        if len(df.columns) > 0 and isinstance(df.columns[0], tuple):
            djm__objc = []
            abb__hyl = []
            ofkn__weyd = False
            for i, xzh__nurkd in enumerate(df.columns):
                if xzh__nurkd[0] != attr:
                    continue
                ofkn__weyd = True
                djm__objc.append(xzh__nurkd[1] if len(xzh__nurkd) == 2 else
                    xzh__nurkd[1:])
                abb__hyl.append(df.data[i])
            if ofkn__weyd:
                return DataFrameType(tuple(abb__hyl), df.index, tuple(
                    djm__objc))


DataFrameAttribute._no_unliteral = True


@overload(operator.getitem, no_unliteral=True)
def namedtuple_getitem_overload(tup, idx):
    if isinstance(tup, types.BaseNamedTuple) and is_overload_constant_str(idx):
        wclbb__lyj = get_overload_const_str(idx)
        val_ind = tup.instance_class._fields.index(wclbb__lyj)
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
        uddd__zov = builder.extract_value(payload.data, i)
        context.nrt.decref(builder, df_type.data[i], uddd__zov)
    context.nrt.decref(builder, df_type.index, payload.index)


def define_df_dtor(context, builder, df_type, payload_type):
    hle__pmb = builder.module
    pog__tkpdd = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    pcopb__xiwvu = cgutils.get_or_insert_function(hle__pmb, pog__tkpdd,
        name='.dtor.df.{}'.format(df_type))
    if not pcopb__xiwvu.is_declaration:
        return pcopb__xiwvu
    pcopb__xiwvu.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(pcopb__xiwvu.append_basic_block())
    pwk__qqd = pcopb__xiwvu.args[0]
    xdaey__whqg = context.get_value_type(payload_type).as_pointer()
    hcmxc__gmty = builder.bitcast(pwk__qqd, xdaey__whqg)
    payload = context.make_helper(builder, payload_type, ref=hcmxc__gmty)
    decref_df_data(context, builder, payload, df_type)
    has_parent = cgutils.is_not_null(builder, payload.parent)
    with builder.if_then(has_parent):
        qkwlh__pian = context.get_python_api(builder)
        qsgg__rxm = qkwlh__pian.gil_ensure()
        qkwlh__pian.decref(payload.parent)
        qkwlh__pian.gil_release(qsgg__rxm)
    builder.ret_void()
    return pcopb__xiwvu


def construct_dataframe(context, builder, df_type, data_tup, index_val,
    parent=None, colnames=None):
    payload_type = DataFramePayloadType(df_type)
    cng__ras = cgutils.create_struct_proxy(payload_type)(context, builder)
    cng__ras.data = data_tup
    cng__ras.index = index_val
    if colnames is not None:
        assert df_type.has_runtime_cols, 'construct_dataframe can only provide colnames if columns are determined at runtime'
        cng__ras.columns = colnames
    jrn__hwz = context.get_value_type(payload_type)
    ffe__amzu = context.get_abi_sizeof(jrn__hwz)
    lojd__cnnu = define_df_dtor(context, builder, df_type, payload_type)
    vclc__ceih = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, ffe__amzu), lojd__cnnu)
    kol__ehtmk = context.nrt.meminfo_data(builder, vclc__ceih)
    hayqz__mva = builder.bitcast(kol__ehtmk, jrn__hwz.as_pointer())
    kqy__mdyr = cgutils.create_struct_proxy(df_type)(context, builder)
    kqy__mdyr.meminfo = vclc__ceih
    if parent is None:
        kqy__mdyr.parent = cgutils.get_null_value(kqy__mdyr.parent.type)
    else:
        kqy__mdyr.parent = parent
        cng__ras.parent = parent
        has_parent = cgutils.is_not_null(builder, parent)
        with builder.if_then(has_parent):
            qkwlh__pian = context.get_python_api(builder)
            qsgg__rxm = qkwlh__pian.gil_ensure()
            qkwlh__pian.incref(parent)
            qkwlh__pian.gil_release(qsgg__rxm)
    builder.store(cng__ras._getvalue(), hayqz__mva)
    return kqy__mdyr._getvalue()


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
        lgvjl__vmom = [data_typ.dtype.arr_types.dtype] * len(data_typ.dtype
            .arr_types)
    else:
        lgvjl__vmom = [tavg__bsdta for tavg__bsdta in data_typ.dtype.arr_types]
    rpq__yqx = DataFrameType(tuple(lgvjl__vmom + [colnames_index_typ]),
        index_typ, None, is_table_format=True)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup, index, col_names = args
        parent = None
        tnblz__vzlle = construct_dataframe(context, builder, df_type,
            data_tup, index, parent, col_names)
        context.nrt.incref(builder, data_typ, data_tup)
        context.nrt.incref(builder, index_typ, index)
        context.nrt.incref(builder, colnames_index_typ, col_names)
        return tnblz__vzlle
    sig = signature(rpq__yqx, data_typ, index_typ, colnames_index_typ)
    return sig, codegen


@intrinsic
def init_dataframe(typingctx, data_tup_typ, index_typ, col_names_typ=None):
    assert is_pd_index_type(index_typ) or isinstance(index_typ, MultiIndexType
        ), 'init_dataframe(): invalid index type'
    ccnv__ngm = len(data_tup_typ.types)
    if ccnv__ngm == 0:
        column_names = ()
    elif isinstance(col_names_typ, types.TypeRef):
        column_names = col_names_typ.instance_type.columns
    else:
        column_names = get_const_tup_vals(col_names_typ)
    if ccnv__ngm == 1 and isinstance(data_tup_typ.types[0], TableType):
        ccnv__ngm = len(data_tup_typ.types[0].arr_types)
    assert len(column_names
        ) == ccnv__ngm, 'init_dataframe(): number of column names does not match number of columns'
    is_table_format = False
    lkmsz__npzb = data_tup_typ.types
    if ccnv__ngm != 0 and isinstance(data_tup_typ.types[0], TableType):
        lkmsz__npzb = data_tup_typ.types[0].arr_types
        is_table_format = True
    rpq__yqx = DataFrameType(lkmsz__npzb, index_typ, column_names,
        is_table_format=is_table_format)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup = args[0]
        index_val = args[1]
        parent = None
        if is_table_format:
            enssi__hcic = cgutils.create_struct_proxy(rpq__yqx.table_type)(
                context, builder, builder.extract_value(data_tup, 0))
            parent = enssi__hcic.parent
        tnblz__vzlle = construct_dataframe(context, builder, df_type,
            data_tup, index_val, parent, None)
        context.nrt.incref(builder, data_tup_typ, data_tup)
        context.nrt.incref(builder, index_typ, index_val)
        return tnblz__vzlle
    sig = signature(rpq__yqx, data_tup_typ, index_typ, col_names_typ)
    return sig, codegen


@intrinsic
def has_parent(typingctx, df=None):
    check_runtime_cols_unsupported(df, 'has_parent')

    def codegen(context, builder, sig, args):
        kqy__mdyr = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        return cgutils.is_not_null(builder, kqy__mdyr.parent)
    return signature(types.bool_, df), codegen


@intrinsic
def _column_needs_unboxing(typingctx, df_typ, i_typ=None):
    check_runtime_cols_unsupported(df_typ, '_column_needs_unboxing')
    assert isinstance(df_typ, DataFrameType) and is_overload_constant_int(i_typ
        )

    def codegen(context, builder, sig, args):
        cng__ras = get_dataframe_payload(context, builder, df_typ, args[0])
        qsqel__rqc = get_overload_const_int(i_typ)
        arr_typ = df_typ.data[qsqel__rqc]
        if df_typ.is_table_format:
            enssi__hcic = cgutils.create_struct_proxy(df_typ.table_type)(
                context, builder, builder.extract_value(cng__ras.data, 0))
            heysu__icyxa = df_typ.table_type.type_to_blk[arr_typ]
            tfmov__fvy = getattr(enssi__hcic, f'block_{heysu__icyxa}')
            shpks__oqs = ListInstance(context, builder, types.List(arr_typ),
                tfmov__fvy)
            ftjvr__ilmb = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[qsqel__rqc])
            uddd__zov = shpks__oqs.getitem(ftjvr__ilmb)
        else:
            uddd__zov = builder.extract_value(cng__ras.data, qsqel__rqc)
        vun__cqo = cgutils.alloca_once_value(builder, uddd__zov)
        bqnh__uni = cgutils.alloca_once_value(builder, context.
            get_constant_null(arr_typ))
        return is_ll_eq(builder, vun__cqo, bqnh__uni)
    return signature(types.bool_, df_typ, i_typ), codegen


def get_dataframe_payload(context, builder, df_type, value):
    vclc__ceih = cgutils.create_struct_proxy(df_type)(context, builder, value
        ).meminfo
    payload_type = DataFramePayloadType(df_type)
    payload = context.nrt.meminfo_data(builder, vclc__ceih)
    xdaey__whqg = context.get_value_type(payload_type).as_pointer()
    payload = builder.bitcast(payload, xdaey__whqg)
    return context.make_helper(builder, payload_type, ref=payload)


@intrinsic
def _get_dataframe_data(typingctx, df_typ=None):
    check_runtime_cols_unsupported(df_typ, '_get_dataframe_data')
    rpq__yqx = types.Tuple(df_typ.data)
    if df_typ.is_table_format:
        rpq__yqx = types.Tuple([TableType(df_typ.data)])
    sig = signature(rpq__yqx, df_typ)

    def codegen(context, builder, signature, args):
        cng__ras = get_dataframe_payload(context, builder, signature.args[0
            ], args[0])
        return impl_ret_borrowed(context, builder, signature.return_type,
            cng__ras.data)
    return sig, codegen


@intrinsic
def get_dataframe_index(typingctx, df_typ=None):

    def codegen(context, builder, signature, args):
        cng__ras = get_dataframe_payload(context, builder, signature.args[0
            ], args[0])
        return impl_ret_borrowed(context, builder, df_typ.index, cng__ras.index
            )
    rpq__yqx = df_typ.index
    sig = signature(rpq__yqx, df_typ)
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
        qflv__qhjys = df.data[i]
        return qflv__qhjys(*args)


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
        cng__ras = get_dataframe_payload(context, builder, signature.args[0
            ], args[0])
        return impl_ret_borrowed(context, builder, df_typ.table_type,
            builder.extract_value(cng__ras.data, 0))
    return df_typ.table_type(df_typ), codegen


@intrinsic
def get_dataframe_column_names(typingctx, df_typ=None):
    assert df_typ.has_runtime_cols, 'get_dataframe_column_names() expects columns to be determined at runtime'

    def codegen(context, builder, signature, args):
        cng__ras = get_dataframe_payload(context, builder, signature.args[0
            ], args[0])
        return impl_ret_borrowed(context, builder, df_typ.
            runtime_colname_typ, cng__ras.columns)
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
    coqjo__mbb = self.typemap[data_tup.name]
    if any(is_tuple_like_type(tavg__bsdta) for tavg__bsdta in coqjo__mbb.types
        ):
        return None
    if equiv_set.has_shape(data_tup):
        xni__fbhzr = equiv_set.get_shape(data_tup)
        if len(xni__fbhzr) > 1:
            equiv_set.insert_equiv(*xni__fbhzr)
        if len(xni__fbhzr) > 0:
            ljvr__hgz = self.typemap[index.name]
            if not isinstance(ljvr__hgz, HeterogeneousIndexType
                ) and equiv_set.has_shape(index):
                equiv_set.insert_equiv(xni__fbhzr[0], index)
            return ArrayAnalysis.AnalyzeResult(shape=(xni__fbhzr[0], len(
                xni__fbhzr)), pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_dataframe_ext_init_dataframe
    ) = init_dataframe_equiv


def get_dataframe_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    hij__gpgit = args[0]
    data_types = self.typemap[hij__gpgit.name].data
    if any(is_tuple_like_type(tavg__bsdta) for tavg__bsdta in data_types):
        return None
    if equiv_set.has_shape(hij__gpgit):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            hij__gpgit)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_data
    ) = get_dataframe_data_equiv


def get_dataframe_index_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 1 and not kws
    hij__gpgit = args[0]
    ljvr__hgz = self.typemap[hij__gpgit.name].index
    if isinstance(ljvr__hgz, HeterogeneousIndexType):
        return None
    if equiv_set.has_shape(hij__gpgit):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            hij__gpgit)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_index
    ) = get_dataframe_index_equiv


def get_dataframe_table_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    hij__gpgit = args[0]
    if equiv_set.has_shape(hij__gpgit):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            hij__gpgit), pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_table
    ) = get_dataframe_table_equiv


def get_dataframe_column_names_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    hij__gpgit = args[0]
    if equiv_set.has_shape(hij__gpgit):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            hij__gpgit)[1], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_column_names
    ) = get_dataframe_column_names_equiv


@intrinsic
def set_dataframe_data(typingctx, df_typ, c_ind_typ, arr_typ=None):
    check_runtime_cols_unsupported(df_typ, 'set_dataframe_data')
    assert is_overload_constant_int(c_ind_typ)
    qsqel__rqc = get_overload_const_int(c_ind_typ)
    if df_typ.data[qsqel__rqc] != arr_typ:
        raise BodoError(
            'Changing dataframe column data type inplace is not supported in conditionals/loops or for dataframe arguments'
            )

    def codegen(context, builder, signature, args):
        cbz__npwcs, tymyj__xgvlj, ogvug__yjjqh = args
        cng__ras = get_dataframe_payload(context, builder, df_typ, cbz__npwcs)
        if df_typ.is_table_format:
            enssi__hcic = cgutils.create_struct_proxy(df_typ.table_type)(
                context, builder, builder.extract_value(cng__ras.data, 0))
            heysu__icyxa = df_typ.table_type.type_to_blk[arr_typ]
            tfmov__fvy = getattr(enssi__hcic, f'block_{heysu__icyxa}')
            shpks__oqs = ListInstance(context, builder, types.List(arr_typ),
                tfmov__fvy)
            ftjvr__ilmb = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[qsqel__rqc])
            shpks__oqs.setitem(ftjvr__ilmb, ogvug__yjjqh, True)
        else:
            uddd__zov = builder.extract_value(cng__ras.data, qsqel__rqc)
            context.nrt.decref(builder, df_typ.data[qsqel__rqc], uddd__zov)
            cng__ras.data = builder.insert_value(cng__ras.data,
                ogvug__yjjqh, qsqel__rqc)
            context.nrt.incref(builder, arr_typ, ogvug__yjjqh)
        kqy__mdyr = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=cbz__npwcs)
        payload_type = DataFramePayloadType(df_typ)
        hcmxc__gmty = context.nrt.meminfo_data(builder, kqy__mdyr.meminfo)
        xdaey__whqg = context.get_value_type(payload_type).as_pointer()
        hcmxc__gmty = builder.bitcast(hcmxc__gmty, xdaey__whqg)
        builder.store(cng__ras._getvalue(), hcmxc__gmty)
        return impl_ret_borrowed(context, builder, df_typ, cbz__npwcs)
    sig = signature(df_typ, df_typ, c_ind_typ, arr_typ)
    return sig, codegen


@intrinsic
def set_df_index(typingctx, df_t, index_t=None):
    check_runtime_cols_unsupported(df_t, 'set_df_index')

    def codegen(context, builder, signature, args):
        nfsuw__drhzy = args[0]
        index_val = args[1]
        df_typ = signature.args[0]
        cyxr__neri = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=nfsuw__drhzy)
        zqemc__ami = get_dataframe_payload(context, builder, df_typ,
            nfsuw__drhzy)
        kqy__mdyr = construct_dataframe(context, builder, signature.
            return_type, zqemc__ami.data, index_val, cyxr__neri.parent, None)
        context.nrt.incref(builder, index_t, index_val)
        context.nrt.incref(builder, types.Tuple(df_t.data), zqemc__ami.data)
        return kqy__mdyr
    rpq__yqx = DataFrameType(df_t.data, index_t, df_t.columns, df_t.dist,
        df_t.is_table_format)
    sig = signature(rpq__yqx, df_t, index_t)
    return sig, codegen


@intrinsic
def set_df_column_with_reflect(typingctx, df_type, cname_type, arr_type=None):
    check_runtime_cols_unsupported(df_type, 'set_df_column_with_reflect')
    assert is_literal_type(cname_type), 'constant column name expected'
    col_name = get_literal_value(cname_type)
    ccnv__ngm = len(df_type.columns)
    xgo__fkr = ccnv__ngm
    xdhq__pnfu = df_type.data
    column_names = df_type.columns
    index_typ = df_type.index
    tze__ckr = col_name not in df_type.columns
    qsqel__rqc = ccnv__ngm
    if tze__ckr:
        xdhq__pnfu += arr_type,
        column_names += col_name,
        xgo__fkr += 1
    else:
        qsqel__rqc = df_type.columns.index(col_name)
        xdhq__pnfu = tuple(arr_type if i == qsqel__rqc else xdhq__pnfu[i] for
            i in range(ccnv__ngm))

    def codegen(context, builder, signature, args):
        cbz__npwcs, tymyj__xgvlj, ogvug__yjjqh = args
        in_dataframe_payload = get_dataframe_payload(context, builder,
            df_type, cbz__npwcs)
        tcetk__ehrvf = cgutils.create_struct_proxy(df_type)(context,
            builder, value=cbz__npwcs)
        if df_type.is_table_format:
            owf__piw = df_type.table_type
            oujve__kvef = builder.extract_value(in_dataframe_payload.data, 0)
            sbnyn__ufofu = TableType(xdhq__pnfu)
            ltrm__bike = set_table_data_codegen(context, builder, owf__piw,
                oujve__kvef, sbnyn__ufofu, arr_type, ogvug__yjjqh,
                qsqel__rqc, tze__ckr)
            data_tup = context.make_tuple(builder, types.Tuple([
                sbnyn__ufofu]), [ltrm__bike])
        else:
            lkmsz__npzb = [(builder.extract_value(in_dataframe_payload.data,
                i) if i != qsqel__rqc else ogvug__yjjqh) for i in range(
                ccnv__ngm)]
            if tze__ckr:
                lkmsz__npzb.append(ogvug__yjjqh)
            for hij__gpgit, xqw__mdxx in zip(lkmsz__npzb, xdhq__pnfu):
                context.nrt.incref(builder, xqw__mdxx, hij__gpgit)
            data_tup = context.make_tuple(builder, types.Tuple(xdhq__pnfu),
                lkmsz__npzb)
        index_val = in_dataframe_payload.index
        context.nrt.incref(builder, index_typ, index_val)
        sqc__upe = construct_dataframe(context, builder, signature.
            return_type, data_tup, index_val, tcetk__ehrvf.parent, None)
        if not tze__ckr and arr_type == df_type.data[qsqel__rqc]:
            decref_df_data(context, builder, in_dataframe_payload, df_type)
            payload_type = DataFramePayloadType(df_type)
            hcmxc__gmty = context.nrt.meminfo_data(builder, tcetk__ehrvf.
                meminfo)
            xdaey__whqg = context.get_value_type(payload_type).as_pointer()
            hcmxc__gmty = builder.bitcast(hcmxc__gmty, xdaey__whqg)
            hgjd__bacou = get_dataframe_payload(context, builder, df_type,
                sqc__upe)
            builder.store(hgjd__bacou._getvalue(), hcmxc__gmty)
            context.nrt.incref(builder, index_typ, index_val)
            if df_type.is_table_format:
                context.nrt.incref(builder, sbnyn__ufofu, builder.
                    extract_value(data_tup, 0))
            else:
                for hij__gpgit, xqw__mdxx in zip(lkmsz__npzb, xdhq__pnfu):
                    context.nrt.incref(builder, xqw__mdxx, hij__gpgit)
        has_parent = cgutils.is_not_null(builder, tcetk__ehrvf.parent)
        with builder.if_then(has_parent):
            qkwlh__pian = context.get_python_api(builder)
            qsgg__rxm = qkwlh__pian.gil_ensure()
            chl__zmbse = context.get_env_manager(builder)
            context.nrt.incref(builder, arr_type, ogvug__yjjqh)
            wdufm__wfsal = numba.core.pythonapi._BoxContext(context,
                builder, qkwlh__pian, chl__zmbse)
            ddbo__laer = wdufm__wfsal.pyapi.from_native_value(arr_type,
                ogvug__yjjqh, wdufm__wfsal.env_manager)
            if isinstance(col_name, str):
                dzwqa__dvz = context.insert_const_string(builder.module,
                    col_name)
                ccfae__yfiiz = qkwlh__pian.string_from_string(dzwqa__dvz)
            else:
                assert isinstance(col_name, int)
                ccfae__yfiiz = qkwlh__pian.long_from_longlong(context.
                    get_constant(types.intp, col_name))
            qkwlh__pian.object_setitem(tcetk__ehrvf.parent, ccfae__yfiiz,
                ddbo__laer)
            qkwlh__pian.decref(ddbo__laer)
            qkwlh__pian.decref(ccfae__yfiiz)
            qkwlh__pian.gil_release(qsgg__rxm)
        return sqc__upe
    rpq__yqx = DataFrameType(xdhq__pnfu, index_typ, column_names, df_type.
        dist, df_type.is_table_format)
    sig = signature(rpq__yqx, df_type, cname_type, arr_type)
    return sig, codegen


@lower_constant(DataFrameType)
def lower_constant_dataframe(context, builder, df_type, pyval):
    check_runtime_cols_unsupported(df_type, 'lowering a constant DataFrame')
    ccnv__ngm = len(pyval.columns)
    lkmsz__npzb = []
    for i in range(ccnv__ngm):
        abo__ywlkk = pyval.iloc[:, i]
        if isinstance(df_type.data[i], bodo.DatetimeArrayType):
            ddbo__laer = abo__ywlkk.array
        else:
            ddbo__laer = abo__ywlkk.values
        lkmsz__npzb.append(ddbo__laer)
    lkmsz__npzb = tuple(lkmsz__npzb)
    if df_type.is_table_format:
        enssi__hcic = context.get_constant_generic(builder, df_type.
            table_type, Table(lkmsz__npzb))
        data_tup = lir.Constant.literal_struct([enssi__hcic])
    else:
        data_tup = lir.Constant.literal_struct([context.
            get_constant_generic(builder, df_type.data[i], xzh__nurkd) for 
            i, xzh__nurkd in enumerate(lkmsz__npzb)])
    index_val = context.get_constant_generic(builder, df_type.index, pyval.
        index)
    krr__qszj = context.get_constant_null(types.pyobject)
    payload = lir.Constant.literal_struct([data_tup, index_val, krr__qszj])
    payload = cgutils.global_constant(builder, '.const.payload', payload
        ).bitcast(cgutils.voidptr_t)
    gfa__dxjr = context.get_constant(types.int64, -1)
    cbh__cnkdm = context.get_constant_null(types.voidptr)
    vclc__ceih = lir.Constant.literal_struct([gfa__dxjr, cbh__cnkdm,
        cbh__cnkdm, payload, gfa__dxjr])
    vclc__ceih = cgutils.global_constant(builder, '.const.meminfo', vclc__ceih
        ).bitcast(cgutils.voidptr_t)
    return lir.Constant.literal_struct([vclc__ceih, krr__qszj])


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
        fpauf__bbst = context.cast(builder, in_dataframe_payload.index,
            fromty.index, toty.index)
    else:
        fpauf__bbst = in_dataframe_payload.index
        context.nrt.incref(builder, fromty.index, fpauf__bbst)
    if (fromty.is_table_format == toty.is_table_format and fromty.data ==
        toty.data):
        abb__hyl = in_dataframe_payload.data
        if fromty.is_table_format:
            context.nrt.incref(builder, types.Tuple([fromty.table_type]),
                abb__hyl)
        else:
            context.nrt.incref(builder, types.BaseTuple.from_types(fromty.
                data), abb__hyl)
    elif not fromty.is_table_format and toty.is_table_format:
        abb__hyl = _cast_df_data_to_table_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    elif fromty.is_table_format and not toty.is_table_format:
        abb__hyl = _cast_df_data_to_tuple_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    elif fromty.is_table_format and toty.is_table_format:
        abb__hyl = _cast_df_data_keep_table_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    else:
        abb__hyl = _cast_df_data_keep_tuple_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    return construct_dataframe(context, builder, toty, abb__hyl,
        fpauf__bbst, in_dataframe_payload.parent, None)


def _cast_empty_df(context, builder, toty):
    ack__iquyp = {}
    if isinstance(toty.index, RangeIndexType):
        index = 'bodo.hiframes.pd_index_ext.init_range_index(0, 0, 1, None)'
    else:
        ucc__xsxpu = get_index_data_arr_types(toty.index)[0]
        rfoai__uujch = bodo.utils.transform.get_type_alloc_counts(ucc__xsxpu
            ) - 1
        igbkr__suliq = ', '.join('0' for tymyj__xgvlj in range(rfoai__uujch))
        index = (
            'bodo.utils.conversion.index_from_array(bodo.utils.utils.alloc_type(0, index_arr_type, ({}{})))'
            .format(igbkr__suliq, ', ' if rfoai__uujch == 1 else ''))
        ack__iquyp['index_arr_type'] = ucc__xsxpu
    nrnt__gouib = []
    for i, arr_typ in enumerate(toty.data):
        rfoai__uujch = bodo.utils.transform.get_type_alloc_counts(arr_typ) - 1
        igbkr__suliq = ', '.join('0' for tymyj__xgvlj in range(rfoai__uujch))
        jmzj__qqojm = ('bodo.utils.utils.alloc_type(0, arr_type{}, ({}{}))'
            .format(i, igbkr__suliq, ', ' if rfoai__uujch == 1 else ''))
        nrnt__gouib.append(jmzj__qqojm)
        ack__iquyp[f'arr_type{i}'] = arr_typ
    nrnt__gouib = ', '.join(nrnt__gouib)
    pvtk__uytsz = 'def impl():\n'
    cdxbf__fzfp = bodo.hiframes.dataframe_impl._gen_init_df(pvtk__uytsz,
        toty.columns, nrnt__gouib, index, ack__iquyp)
    df = context.compile_internal(builder, cdxbf__fzfp, toty(), [])
    return df


def _cast_df_data_to_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame to table format')
    mpo__hrk = toty.table_type
    enssi__hcic = cgutils.create_struct_proxy(mpo__hrk)(context, builder)
    enssi__hcic.parent = in_dataframe_payload.parent
    for tavg__bsdta, heysu__icyxa in mpo__hrk.type_to_blk.items():
        rzujf__mmzgb = context.get_constant(types.int64, len(mpo__hrk.
            block_to_arr_ind[heysu__icyxa]))
        tymyj__xgvlj, gmbw__eeqb = ListInstance.allocate_ex(context,
            builder, types.List(tavg__bsdta), rzujf__mmzgb)
        gmbw__eeqb.size = rzujf__mmzgb
        setattr(enssi__hcic, f'block_{heysu__icyxa}', gmbw__eeqb.value)
    for i, tavg__bsdta in enumerate(fromty.data):
        hacwm__vpk = toty.data[i]
        if tavg__bsdta != hacwm__vpk:
            ods__soiid = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*ods__soiid)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        uddd__zov = builder.extract_value(in_dataframe_payload.data, i)
        if tavg__bsdta != hacwm__vpk:
            oplpl__zal = context.cast(builder, uddd__zov, tavg__bsdta,
                hacwm__vpk)
            nplp__sulk = False
        else:
            oplpl__zal = uddd__zov
            nplp__sulk = True
        heysu__icyxa = mpo__hrk.type_to_blk[tavg__bsdta]
        tfmov__fvy = getattr(enssi__hcic, f'block_{heysu__icyxa}')
        shpks__oqs = ListInstance(context, builder, types.List(tavg__bsdta),
            tfmov__fvy)
        ftjvr__ilmb = context.get_constant(types.int64, mpo__hrk.
            block_offsets[i])
        shpks__oqs.setitem(ftjvr__ilmb, oplpl__zal, nplp__sulk)
    data_tup = context.make_tuple(builder, types.Tuple([mpo__hrk]), [
        enssi__hcic._getvalue()])
    return data_tup


def _cast_df_data_keep_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame columns')
    lkmsz__npzb = []
    for i in range(len(fromty.data)):
        if fromty.data[i] != toty.data[i]:
            ods__soiid = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*ods__soiid)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
            uddd__zov = builder.extract_value(in_dataframe_payload.data, i)
            oplpl__zal = context.cast(builder, uddd__zov, fromty.data[i],
                toty.data[i])
            nplp__sulk = False
        else:
            oplpl__zal = builder.extract_value(in_dataframe_payload.data, i)
            nplp__sulk = True
        if nplp__sulk:
            context.nrt.incref(builder, toty.data[i], oplpl__zal)
        lkmsz__npzb.append(oplpl__zal)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), lkmsz__npzb)
    return data_tup


def _cast_df_data_keep_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting table format DataFrame columns')
    owf__piw = fromty.table_type
    oujve__kvef = cgutils.create_struct_proxy(owf__piw)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    sbnyn__ufofu = toty.table_type
    ltrm__bike = cgutils.create_struct_proxy(sbnyn__ufofu)(context, builder)
    ltrm__bike.parent = in_dataframe_payload.parent
    for tavg__bsdta, heysu__icyxa in sbnyn__ufofu.type_to_blk.items():
        rzujf__mmzgb = context.get_constant(types.int64, len(sbnyn__ufofu.
            block_to_arr_ind[heysu__icyxa]))
        tymyj__xgvlj, gmbw__eeqb = ListInstance.allocate_ex(context,
            builder, types.List(tavg__bsdta), rzujf__mmzgb)
        gmbw__eeqb.size = rzujf__mmzgb
        setattr(ltrm__bike, f'block_{heysu__icyxa}', gmbw__eeqb.value)
    for i in range(len(fromty.data)):
        xjul__ckqby = fromty.data[i]
        hacwm__vpk = toty.data[i]
        if xjul__ckqby != hacwm__vpk:
            ods__soiid = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*ods__soiid)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        eqeq__gxv = owf__piw.type_to_blk[xjul__ckqby]
        phol__yvoxk = getattr(oujve__kvef, f'block_{eqeq__gxv}')
        eim__nobdr = ListInstance(context, builder, types.List(xjul__ckqby),
            phol__yvoxk)
        tcee__ydst = context.get_constant(types.int64, owf__piw.
            block_offsets[i])
        uddd__zov = eim__nobdr.getitem(tcee__ydst)
        if xjul__ckqby != hacwm__vpk:
            oplpl__zal = context.cast(builder, uddd__zov, xjul__ckqby,
                hacwm__vpk)
            nplp__sulk = False
        else:
            oplpl__zal = uddd__zov
            nplp__sulk = True
        umju__rntdv = sbnyn__ufofu.type_to_blk[tavg__bsdta]
        gmbw__eeqb = getattr(ltrm__bike, f'block_{umju__rntdv}')
        rzsm__elcc = ListInstance(context, builder, types.List(hacwm__vpk),
            gmbw__eeqb)
        hfxlg__kynv = context.get_constant(types.int64, sbnyn__ufofu.
            block_offsets[i])
        rzsm__elcc.setitem(hfxlg__kynv, oplpl__zal, nplp__sulk)
    data_tup = context.make_tuple(builder, types.Tuple([sbnyn__ufofu]), [
        ltrm__bike._getvalue()])
    return data_tup


def _cast_df_data_to_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(fromty,
        'casting table format to traditional DataFrame')
    mpo__hrk = fromty.table_type
    enssi__hcic = cgutils.create_struct_proxy(mpo__hrk)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    lkmsz__npzb = []
    for i, tavg__bsdta in enumerate(toty.data):
        xjul__ckqby = fromty.data[i]
        if tavg__bsdta != xjul__ckqby:
            ods__soiid = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*ods__soiid)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        heysu__icyxa = mpo__hrk.type_to_blk[tavg__bsdta]
        tfmov__fvy = getattr(enssi__hcic, f'block_{heysu__icyxa}')
        shpks__oqs = ListInstance(context, builder, types.List(tavg__bsdta),
            tfmov__fvy)
        ftjvr__ilmb = context.get_constant(types.int64, mpo__hrk.
            block_offsets[i])
        uddd__zov = shpks__oqs.getitem(ftjvr__ilmb)
        if tavg__bsdta != xjul__ckqby:
            oplpl__zal = context.cast(builder, uddd__zov, xjul__ckqby,
                tavg__bsdta)
            nplp__sulk = False
        else:
            oplpl__zal = uddd__zov
            nplp__sulk = True
        if nplp__sulk:
            context.nrt.incref(builder, tavg__bsdta, oplpl__zal)
        lkmsz__npzb.append(oplpl__zal)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), lkmsz__npzb)
    return data_tup


@overload(pd.DataFrame, inline='always', no_unliteral=True)
def pd_dataframe_overload(data=None, index=None, columns=None, dtype=None,
    copy=False):
    if not is_overload_constant_bool(copy):
        raise BodoError(
            "pd.DataFrame(): 'copy' argument should be a constant boolean")
    copy = get_overload_const(copy)
    fawa__yay, nrnt__gouib, index_arg = _get_df_args(data, index, columns,
        dtype, copy)
    cyohg__wzisa = gen_const_tup(fawa__yay)
    pvtk__uytsz = (
        'def _init_df(data=None, index=None, columns=None, dtype=None, copy=False):\n'
        )
    pvtk__uytsz += (
        '  return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, {}, {})\n'
        .format(nrnt__gouib, index_arg, cyohg__wzisa))
    oepi__zgc = {}
    exec(pvtk__uytsz, {'bodo': bodo, 'np': np}, oepi__zgc)
    uivt__icch = oepi__zgc['_init_df']
    return uivt__icch


@intrinsic
def _tuple_to_table_format_decoded(typingctx, df_typ):
    assert not df_typ.is_table_format, '_tuple_to_table_format requires a tuple format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    rpq__yqx = DataFrameType(to_str_arr_if_dict_array(df_typ.data), df_typ.
        index, df_typ.columns, dist=df_typ.dist, is_table_format=True)
    sig = signature(rpq__yqx, df_typ)
    return sig, codegen


@intrinsic
def _table_to_tuple_format_decoded(typingctx, df_typ):
    assert df_typ.is_table_format, '_tuple_to_table_format requires a table format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    rpq__yqx = DataFrameType(to_str_arr_if_dict_array(df_typ.data), df_typ.
        index, df_typ.columns, dist=df_typ.dist, is_table_format=False)
    sig = signature(rpq__yqx, df_typ)
    return sig, codegen


def _get_df_args(data, index, columns, dtype, copy):
    gcv__ign = ''
    if not is_overload_none(dtype):
        gcv__ign = '.astype(dtype)'
    index_is_none = is_overload_none(index)
    index_arg = 'bodo.utils.conversion.convert_to_index(index)'
    if isinstance(data, types.BaseTuple):
        if not data.types[0] == types.StringLiteral('__bodo_tup'):
            raise BodoError('pd.DataFrame tuple input data not supported yet')
        assert len(data.types) % 2 == 1, 'invalid const dict tuple structure'
        ccnv__ngm = (len(data.types) - 1) // 2
        szy__akqlq = [tavg__bsdta.literal_value for tavg__bsdta in data.
            types[1:ccnv__ngm + 1]]
        data_val_types = dict(zip(szy__akqlq, data.types[ccnv__ngm + 1:]))
        lkmsz__npzb = ['data[{}]'.format(i) for i in range(ccnv__ngm + 1, 2 *
            ccnv__ngm + 1)]
        data_dict = dict(zip(szy__akqlq, lkmsz__npzb))
        if is_overload_none(index):
            for i, tavg__bsdta in enumerate(data.types[ccnv__ngm + 1:]):
                if isinstance(tavg__bsdta, SeriesType):
                    index_arg = (
                        'bodo.hiframes.pd_series_ext.get_series_index(data[{}])'
                        .format(ccnv__ngm + 1 + i))
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
        ajzok__xfjqk = '.copy()' if copy else ''
        lmy__xzy = get_overload_const_list(columns)
        ccnv__ngm = len(lmy__xzy)
        data_val_types = {wdufm__wfsal: data.copy(ndim=1) for wdufm__wfsal in
            lmy__xzy}
        lkmsz__npzb = ['data[:,{}]{}'.format(i, ajzok__xfjqk) for i in
            range(ccnv__ngm)]
        data_dict = dict(zip(lmy__xzy, lkmsz__npzb))
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
    nrnt__gouib = '({},)'.format(', '.join(
        'bodo.utils.conversion.coerce_to_array({}, True, scalar_to_arr_len={}){}'
        .format(data_dict[wdufm__wfsal], df_len, gcv__ign) for wdufm__wfsal in
        col_names))
    if len(col_names) == 0:
        nrnt__gouib = '()'
    return col_names, nrnt__gouib, index_arg


def _get_df_len_from_info(data_dict, data_val_types, col_names,
    index_is_none, index_arg):
    df_len = '0'
    for wdufm__wfsal in col_names:
        if wdufm__wfsal in data_dict and is_iterable_type(data_val_types[
            wdufm__wfsal]):
            df_len = 'len({})'.format(data_dict[wdufm__wfsal])
            break
    if df_len == '0' and not index_is_none:
        df_len = f'len({index_arg})'
    return df_len


def _fill_null_arrays(data_dict, col_names, df_len, dtype):
    if all(wdufm__wfsal in data_dict for wdufm__wfsal in col_names):
        return
    if is_overload_none(dtype):
        dtype = 'bodo.string_array_type'
    else:
        dtype = 'bodo.utils.conversion.array_type_from_dtype(dtype)'
    tcg__nxz = 'bodo.libs.array_kernels.gen_na_array({}, {})'.format(df_len,
        dtype)
    for wdufm__wfsal in col_names:
        if wdufm__wfsal not in data_dict:
            data_dict[wdufm__wfsal] = tcg__nxz


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
            tavg__bsdta = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df
                )
            return len(tavg__bsdta)
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
        eyg__pcu = idx.literal_value
        if isinstance(eyg__pcu, int):
            qflv__qhjys = tup.types[eyg__pcu]
        elif isinstance(eyg__pcu, slice):
            qflv__qhjys = types.BaseTuple.from_types(tup.types[eyg__pcu])
        return signature(qflv__qhjys, *args)


GetItemTuple.prefer_literal = True


@lower_builtin(operator.getitem, types.BaseTuple, types.IntegerLiteral)
@lower_builtin(operator.getitem, types.BaseTuple, types.SliceLiteral)
def getitem_tuple_lower(context, builder, sig, args):
    umqu__zop, idx = sig.args
    idx = idx.literal_value
    tup, tymyj__xgvlj = args
    if isinstance(idx, int):
        if idx < 0:
            idx += len(umqu__zop)
        if not 0 <= idx < len(umqu__zop):
            raise IndexError('cannot index at %d in %s' % (idx, umqu__zop))
        csm__ayvsw = builder.extract_value(tup, idx)
    elif isinstance(idx, slice):
        guyk__qicl = cgutils.unpack_tuple(builder, tup)[idx]
        csm__ayvsw = context.make_tuple(builder, sig.return_type, guyk__qicl)
    else:
        raise NotImplementedError('unexpected index %r for %s' % (idx, sig.
            args[0]))
    return impl_ret_borrowed(context, builder, sig.return_type, csm__ayvsw)


def join_dummy(left_df, right_df, left_on, right_on, how, suffix_x,
    suffix_y, is_join, indicator, _bodo_na_equal, gen_cond):
    return left_df


@infer_global(join_dummy)
class JoinTyper(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        from bodo.utils.typing import is_overload_str
        assert not kws
        (left_df, right_df, left_on, right_on, vcw__ysd, suffix_x, suffix_y,
            is_join, indicator, tymyj__xgvlj, tymyj__xgvlj) = args
        left_on = get_overload_const_list(left_on)
        right_on = get_overload_const_list(right_on)
        tcbj__qxv = {wdufm__wfsal: i for i, wdufm__wfsal in enumerate(left_on)}
        wdvfl__oeygk = {wdufm__wfsal: i for i, wdufm__wfsal in enumerate(
            right_on)}
        bho__cmjtc = set(left_on) & set(right_on)
        mfx__nzgx = set(left_df.columns) & set(right_df.columns)
        bpndn__ciye = mfx__nzgx - bho__cmjtc
        kqwa__tmc = '$_bodo_index_' in left_on
        efcv__uouv = '$_bodo_index_' in right_on
        how = get_overload_const_str(vcw__ysd)
        pcbso__ihbn = how in {'left', 'outer'}
        pcfsd__qzc = how in {'right', 'outer'}
        columns = []
        data = []
        if kqwa__tmc:
            yyzsl__jop = bodo.utils.typing.get_index_data_arr_types(left_df
                .index)[0]
        else:
            yyzsl__jop = left_df.data[left_df.column_index[left_on[0]]]
        if efcv__uouv:
            gbm__irjq = bodo.utils.typing.get_index_data_arr_types(right_df
                .index)[0]
        else:
            gbm__irjq = right_df.data[right_df.column_index[right_on[0]]]
        if kqwa__tmc and not efcv__uouv and not is_join.literal_value:
            dbg__aybvx = right_on[0]
            if dbg__aybvx in left_df.column_index:
                columns.append(dbg__aybvx)
                if (gbm__irjq == bodo.dict_str_arr_type and yyzsl__jop ==
                    bodo.string_array_type):
                    fans__xryb = bodo.string_array_type
                else:
                    fans__xryb = gbm__irjq
                data.append(fans__xryb)
        if efcv__uouv and not kqwa__tmc and not is_join.literal_value:
            hiwc__jxswe = left_on[0]
            if hiwc__jxswe in right_df.column_index:
                columns.append(hiwc__jxswe)
                if (yyzsl__jop == bodo.dict_str_arr_type and gbm__irjq ==
                    bodo.string_array_type):
                    fans__xryb = bodo.string_array_type
                else:
                    fans__xryb = yyzsl__jop
                data.append(fans__xryb)
        for xjul__ckqby, abo__ywlkk in zip(left_df.data, left_df.columns):
            columns.append(str(abo__ywlkk) + suffix_x.literal_value if 
                abo__ywlkk in bpndn__ciye else abo__ywlkk)
            if abo__ywlkk in bho__cmjtc:
                if xjul__ckqby == bodo.dict_str_arr_type:
                    xjul__ckqby = right_df.data[right_df.column_index[
                        abo__ywlkk]]
                data.append(xjul__ckqby)
            else:
                if (xjul__ckqby == bodo.dict_str_arr_type and abo__ywlkk in
                    tcbj__qxv):
                    if efcv__uouv:
                        xjul__ckqby = gbm__irjq
                    else:
                        utxy__oqzlg = tcbj__qxv[abo__ywlkk]
                        mxchk__vqpt = right_on[utxy__oqzlg]
                        xjul__ckqby = right_df.data[right_df.column_index[
                            mxchk__vqpt]]
                if pcfsd__qzc:
                    xjul__ckqby = to_nullable_type(xjul__ckqby)
                data.append(xjul__ckqby)
        for xjul__ckqby, abo__ywlkk in zip(right_df.data, right_df.columns):
            if abo__ywlkk not in bho__cmjtc:
                columns.append(str(abo__ywlkk) + suffix_y.literal_value if 
                    abo__ywlkk in bpndn__ciye else abo__ywlkk)
                if (xjul__ckqby == bodo.dict_str_arr_type and abo__ywlkk in
                    wdvfl__oeygk):
                    if kqwa__tmc:
                        xjul__ckqby = yyzsl__jop
                    else:
                        utxy__oqzlg = wdvfl__oeygk[abo__ywlkk]
                        ehk__aef = left_on[utxy__oqzlg]
                        xjul__ckqby = left_df.data[left_df.column_index[
                            ehk__aef]]
                if pcbso__ihbn:
                    xjul__ckqby = to_nullable_type(xjul__ckqby)
                data.append(xjul__ckqby)
        gzer__yggq = get_overload_const_bool(indicator)
        if gzer__yggq:
            columns.append('_merge')
            data.append(bodo.CategoricalArrayType(bodo.PDCategoricalDtype((
                'left_only', 'right_only', 'both'), bodo.string_type, False)))
        index_typ = RangeIndexType(types.none)
        vxcjp__fxa = False
        if kqwa__tmc and efcv__uouv and not is_overload_str(how, 'asof'):
            index_typ = left_df.index
            vxcjp__fxa = True
        elif kqwa__tmc and not efcv__uouv:
            index_typ = right_df.index
            vxcjp__fxa = True
        elif efcv__uouv and not kqwa__tmc:
            index_typ = left_df.index
            vxcjp__fxa = True
        if vxcjp__fxa and isinstance(index_typ, bodo.hiframes.pd_index_ext.
            RangeIndexType):
            index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64
                )
        lhd__rqow = DataFrameType(tuple(data), index_typ, tuple(columns))
        return signature(lhd__rqow, *args)


JoinTyper._no_unliteral = True


@lower_builtin(join_dummy, types.VarArg(types.Any))
def lower_join_dummy(context, builder, sig, args):
    kqy__mdyr = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return kqy__mdyr._getvalue()


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
    cwf__zmn = dict(join=join, join_axes=join_axes, keys=keys, levels=
        levels, names=names, verify_integrity=verify_integrity, sort=sort,
        copy=copy)
    iqwjv__rbu = dict(join='outer', join_axes=None, keys=None, levels=None,
        names=None, verify_integrity=False, sort=None, copy=True)
    check_unsupported_args('pandas.concat', cwf__zmn, iqwjv__rbu,
        package_name='pandas', module_name='General')
    pvtk__uytsz = """def impl(objs, axis=0, join='outer', join_axes=None, ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False, sort=None, copy=True):
"""
    if axis == 1:
        if not isinstance(objs, types.BaseTuple):
            raise_bodo_error(
                'Only tuple argument for pd.concat(axis=1) expected')
        index = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len(objs[0]), 1, None)'
            )
        zwjf__now = 0
        nrnt__gouib = []
        names = []
        for i, qyau__smedy in enumerate(objs.types):
            assert isinstance(qyau__smedy, (SeriesType, DataFrameType))
            check_runtime_cols_unsupported(qyau__smedy, 'pandas.concat()')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                qyau__smedy, 'pandas.concat()')
            if isinstance(qyau__smedy, SeriesType):
                names.append(str(zwjf__now))
                zwjf__now += 1
                nrnt__gouib.append(
                    'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'
                    .format(i))
            else:
                names.extend(qyau__smedy.columns)
                for fequp__szguo in range(len(qyau__smedy.data)):
                    nrnt__gouib.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, fequp__szguo))
        return bodo.hiframes.dataframe_impl._gen_init_df(pvtk__uytsz, names,
            ', '.join(nrnt__gouib), index)
    if axis != 0:
        raise_bodo_error('pd.concat(): axis must be 0 or 1')
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        DataFrameType):
        assert all(isinstance(tavg__bsdta, DataFrameType) for tavg__bsdta in
            objs.types)
        redvb__jwkdy = []
        for df in objs.types:
            check_runtime_cols_unsupported(df, 'pandas.concat()')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
                'pandas.concat()')
            redvb__jwkdy.extend(df.columns)
        redvb__jwkdy = list(dict.fromkeys(redvb__jwkdy).keys())
        lgvjl__vmom = {}
        for zwjf__now, wdufm__wfsal in enumerate(redvb__jwkdy):
            for i, df in enumerate(objs.types):
                if wdufm__wfsal in df.column_index:
                    lgvjl__vmom[f'arr_typ{zwjf__now}'] = df.data[df.
                        column_index[wdufm__wfsal]]
                    break
        assert len(lgvjl__vmom) == len(redvb__jwkdy)
        jsju__gldoz = []
        for zwjf__now, wdufm__wfsal in enumerate(redvb__jwkdy):
            args = []
            for i, df in enumerate(objs.types):
                if wdufm__wfsal in df.column_index:
                    qsqel__rqc = df.column_index[wdufm__wfsal]
                    args.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, qsqel__rqc))
                else:
                    args.append(
                        'bodo.libs.array_kernels.gen_na_array(len(objs[{}]), arr_typ{})'
                        .format(i, zwjf__now))
            pvtk__uytsz += ('  A{} = bodo.libs.array_kernels.concat(({},))\n'
                .format(zwjf__now, ', '.join(args)))
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
        return bodo.hiframes.dataframe_impl._gen_init_df(pvtk__uytsz,
            redvb__jwkdy, ', '.join('A{}'.format(i) for i in range(len(
            redvb__jwkdy))), index, lgvjl__vmom)
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        SeriesType):
        assert all(isinstance(tavg__bsdta, SeriesType) for tavg__bsdta in
            objs.types)
        pvtk__uytsz += ('  out_arr = bodo.libs.array_kernels.concat(({},))\n'
            .format(', '.join(
            'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'.format(
            i) for i in range(len(objs.types)))))
        if ignore_index:
            pvtk__uytsz += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            pvtk__uytsz += (
                """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)))))
        pvtk__uytsz += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        oepi__zgc = {}
        exec(pvtk__uytsz, {'bodo': bodo, 'np': np, 'numba': numba}, oepi__zgc)
        return oepi__zgc['impl']
    if isinstance(objs, types.List) and isinstance(objs.dtype, DataFrameType):
        check_runtime_cols_unsupported(objs.dtype, 'pandas.concat()')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(objs.
            dtype, 'pandas.concat()')
        df_type = objs.dtype
        for zwjf__now, wdufm__wfsal in enumerate(df_type.columns):
            pvtk__uytsz += '  arrs{} = []\n'.format(zwjf__now)
            pvtk__uytsz += '  for i in range(len(objs)):\n'
            pvtk__uytsz += '    df = objs[i]\n'
            pvtk__uytsz += (
                """    arrs{0}.append(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0}))
"""
                .format(zwjf__now))
            pvtk__uytsz += (
                '  out_arr{0} = bodo.libs.array_kernels.concat(arrs{0})\n'.
                format(zwjf__now))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr0), 1, None)'
                )
        else:
            pvtk__uytsz += '  arrs_index = []\n'
            pvtk__uytsz += '  for i in range(len(objs)):\n'
            pvtk__uytsz += '    df = objs[i]\n'
            pvtk__uytsz += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
            if objs.dtype.index.name_typ == types.none:
                name = None
            else:
                name = objs.dtype.index.name_typ.literal_value
            index = f"""bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index), {name!r})
"""
        return bodo.hiframes.dataframe_impl._gen_init_df(pvtk__uytsz,
            df_type.columns, ', '.join('out_arr{}'.format(i) for i in range
            (len(df_type.columns))), index)
    if isinstance(objs, types.List) and isinstance(objs.dtype, SeriesType):
        pvtk__uytsz += '  arrs = []\n'
        pvtk__uytsz += '  for i in range(len(objs)):\n'
        pvtk__uytsz += (
            '    arrs.append(bodo.hiframes.pd_series_ext.get_series_data(objs[i]))\n'
            )
        pvtk__uytsz += '  out_arr = bodo.libs.array_kernels.concat(arrs)\n'
        if ignore_index:
            pvtk__uytsz += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            pvtk__uytsz += '  arrs_index = []\n'
            pvtk__uytsz += '  for i in range(len(objs)):\n'
            pvtk__uytsz += '    S = objs[i]\n'
            pvtk__uytsz += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(S)))
"""
            pvtk__uytsz += """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index))
"""
        pvtk__uytsz += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        oepi__zgc = {}
        exec(pvtk__uytsz, {'bodo': bodo, 'np': np, 'numba': numba}, oepi__zgc)
        return oepi__zgc['impl']
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
        rpq__yqx = df.copy(index=index, is_table_format=False)
        return signature(rpq__yqx, *args)


SortDummyTyper._no_unliteral = True


@lower_builtin(sort_values_dummy, types.VarArg(types.Any))
def lower_sort_values_dummy(context, builder, sig, args):
    if sig.return_type == types.none:
        return
    gcym__diocn = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return gcym__diocn._getvalue()


@overload_method(DataFrameType, 'itertuples', inline='always', no_unliteral
    =True)
def itertuples_overload(df, index=True, name='Pandas'):
    check_runtime_cols_unsupported(df, 'DataFrame.itertuples()')
    cwf__zmn = dict(index=index, name=name)
    iqwjv__rbu = dict(index=True, name='Pandas')
    check_unsupported_args('DataFrame.itertuples', cwf__zmn, iqwjv__rbu,
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
        lgvjl__vmom = (types.Array(types.int64, 1, 'C'),) + df.data
        odfps__gpjs = bodo.hiframes.dataframe_impl.DataFrameTupleIterator(
            columns, lgvjl__vmom)
        return signature(odfps__gpjs, *args)


@lower_builtin(itertuples_dummy, types.VarArg(types.Any))
def lower_itertuples_dummy(context, builder, sig, args):
    gcym__diocn = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return gcym__diocn._getvalue()


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
    gcym__diocn = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return gcym__diocn._getvalue()


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
    gcym__diocn = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return gcym__diocn._getvalue()


@numba.generated_jit(nopython=True)
def pivot_impl(index_tup, columns_tup, values_tup, pivot_values,
    index_names, columns_name, value_names, check_duplicates=True, parallel
    =False):
    if not is_overload_constant_bool(check_duplicates):
        raise BodoError(
            'pivot_impl(): check_duplicates must be a constant boolean')
    ayb__zec = get_overload_const_bool(check_duplicates)
    yicj__ohc = not is_overload_none(value_names)
    vpsf__tpeeb = isinstance(values_tup, types.UniTuple)
    if vpsf__tpeeb:
        xfjv__wkvr = [to_nullable_type(values_tup.dtype)]
    else:
        xfjv__wkvr = [to_nullable_type(xqw__mdxx) for xqw__mdxx in values_tup]
    pvtk__uytsz = 'def impl(\n'
    pvtk__uytsz += """    index_tup, columns_tup, values_tup, pivot_values, index_names, columns_name, value_names, check_duplicates=True, parallel=False
"""
    pvtk__uytsz += '):\n'
    pvtk__uytsz += '    if parallel:\n'
    cweee__exxp = ', '.join([f'array_to_info(index_tup[{i}])' for i in
        range(len(index_tup))] + [f'array_to_info(columns_tup[{i}])' for i in
        range(len(columns_tup))] + [f'array_to_info(values_tup[{i}])' for i in
        range(len(values_tup))])
    pvtk__uytsz += f'        info_list = [{cweee__exxp}]\n'
    pvtk__uytsz += '        cpp_table = arr_info_list_to_table(info_list)\n'
    pvtk__uytsz += f"""        out_cpp_table = shuffle_table(cpp_table, {len(index_tup)}, parallel, 0)
"""
    qwuj__acug = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i}), index_tup[{i}])'
         for i in range(len(index_tup))])
    xutyj__butp = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup)}), columns_tup[{i}])'
         for i in range(len(columns_tup))])
    hxqou__ujswx = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup) + len(columns_tup)}), values_tup[{i}])'
         for i in range(len(values_tup))])
    pvtk__uytsz += f'        index_tup = ({qwuj__acug},)\n'
    pvtk__uytsz += f'        columns_tup = ({xutyj__butp},)\n'
    pvtk__uytsz += f'        values_tup = ({hxqou__ujswx},)\n'
    pvtk__uytsz += '        delete_table(cpp_table)\n'
    pvtk__uytsz += '        delete_table(out_cpp_table)\n'
    pvtk__uytsz += '    columns_arr = columns_tup[0]\n'
    if vpsf__tpeeb:
        pvtk__uytsz += '    values_arrs = [arr for arr in values_tup]\n'
    pvtk__uytsz += """    unique_index_arr_tup, row_vector = bodo.libs.array_ops.array_unique_vector_map(
"""
    pvtk__uytsz += '        index_tup\n'
    pvtk__uytsz += '    )\n'
    pvtk__uytsz += '    n_rows = len(unique_index_arr_tup[0])\n'
    pvtk__uytsz += '    num_values_arrays = len(values_tup)\n'
    pvtk__uytsz += '    n_unique_pivots = len(pivot_values)\n'
    if vpsf__tpeeb:
        pvtk__uytsz += '    n_cols = num_values_arrays * n_unique_pivots\n'
    else:
        pvtk__uytsz += '    n_cols = n_unique_pivots\n'
    pvtk__uytsz += '    col_map = {}\n'
    pvtk__uytsz += '    for i in range(n_unique_pivots):\n'
    pvtk__uytsz += (
        '        if bodo.libs.array_kernels.isna(pivot_values, i):\n')
    pvtk__uytsz += '            raise ValueError(\n'
    pvtk__uytsz += """                "DataFrame.pivot(): NA values in 'columns' array not supported\"
"""
    pvtk__uytsz += '            )\n'
    pvtk__uytsz += '        col_map[pivot_values[i]] = i\n'
    ydxt__fvon = False
    for i, jnuc__vyn in enumerate(xfjv__wkvr):
        if is_str_arr_type(jnuc__vyn):
            ydxt__fvon = True
            pvtk__uytsz += f"""    len_arrs_{i} = [np.zeros(n_rows, np.int64) for _ in range(n_cols)]
"""
            pvtk__uytsz += f'    total_lens_{i} = np.zeros(n_cols, np.int64)\n'
    if ydxt__fvon:
        if ayb__zec:
            pvtk__uytsz += '    nbytes = (n_rows + 7) >> 3\n'
            pvtk__uytsz += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
        pvtk__uytsz += '    for i in range(len(columns_arr)):\n'
        pvtk__uytsz += '        col_name = columns_arr[i]\n'
        pvtk__uytsz += '        pivot_idx = col_map[col_name]\n'
        pvtk__uytsz += '        row_idx = row_vector[i]\n'
        if ayb__zec:
            pvtk__uytsz += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
            pvtk__uytsz += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
            pvtk__uytsz += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
            pvtk__uytsz += '        else:\n'
            pvtk__uytsz += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
        if vpsf__tpeeb:
            pvtk__uytsz += '        for j in range(num_values_arrays):\n'
            pvtk__uytsz += (
                '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
            pvtk__uytsz += '            len_arr = len_arrs_0[col_idx]\n'
            pvtk__uytsz += '            values_arr = values_arrs[j]\n'
            pvtk__uytsz += (
                '            if not bodo.libs.array_kernels.isna(values_arr, i):\n'
                )
            pvtk__uytsz += """                str_val_len = bodo.libs.str_arr_ext.get_str_arr_item_length(values_arr, i)
"""
            pvtk__uytsz += '                len_arr[row_idx] = str_val_len\n'
            pvtk__uytsz += (
                '                total_lens_0[col_idx] += str_val_len\n')
        else:
            for i, jnuc__vyn in enumerate(xfjv__wkvr):
                if is_str_arr_type(jnuc__vyn):
                    pvtk__uytsz += f"""        if not bodo.libs.array_kernels.isna(values_tup[{i}], i):
"""
                    pvtk__uytsz += f"""            str_val_len_{i} = bodo.libs.str_arr_ext.get_str_arr_item_length(values_tup[{i}], i)
"""
                    pvtk__uytsz += f"""            len_arrs_{i}[pivot_idx][row_idx] = str_val_len_{i}
"""
                    pvtk__uytsz += (
                        f'            total_lens_{i}[pivot_idx] += str_val_len_{i}\n'
                        )
    for i, jnuc__vyn in enumerate(xfjv__wkvr):
        if is_str_arr_type(jnuc__vyn):
            pvtk__uytsz += f'    data_arrs_{i} = [\n'
            pvtk__uytsz += (
                '        bodo.libs.str_arr_ext.gen_na_str_array_lens(\n')
            pvtk__uytsz += (
                f'            n_rows, total_lens_{i}[i], len_arrs_{i}[i]\n')
            pvtk__uytsz += '        )\n'
            pvtk__uytsz += '        for i in range(n_cols)\n'
            pvtk__uytsz += '    ]\n'
        else:
            pvtk__uytsz += f'    data_arrs_{i} = [\n'
            pvtk__uytsz += f"""        bodo.libs.array_kernels.gen_na_array(n_rows, data_arr_typ_{i})
"""
            pvtk__uytsz += '        for _ in range(n_cols)\n'
            pvtk__uytsz += '    ]\n'
    if not ydxt__fvon and ayb__zec:
        pvtk__uytsz += '    nbytes = (n_rows + 7) >> 3\n'
        pvtk__uytsz += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
    pvtk__uytsz += '    for i in range(len(columns_arr)):\n'
    pvtk__uytsz += '        col_name = columns_arr[i]\n'
    pvtk__uytsz += '        pivot_idx = col_map[col_name]\n'
    pvtk__uytsz += '        row_idx = row_vector[i]\n'
    if not ydxt__fvon and ayb__zec:
        pvtk__uytsz += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
        pvtk__uytsz += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
        pvtk__uytsz += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
        pvtk__uytsz += '        else:\n'
        pvtk__uytsz += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
    if vpsf__tpeeb:
        pvtk__uytsz += '        for j in range(num_values_arrays):\n'
        pvtk__uytsz += (
            '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
        pvtk__uytsz += '            col_arr = data_arrs_0[col_idx]\n'
        pvtk__uytsz += '            values_arr = values_arrs[j]\n'
        pvtk__uytsz += (
            '            if bodo.libs.array_kernels.isna(values_arr, i):\n')
        pvtk__uytsz += (
            '                bodo.libs.array_kernels.setna(col_arr, row_idx)\n'
            )
        pvtk__uytsz += '            else:\n'
        pvtk__uytsz += '                col_arr[row_idx] = values_arr[i]\n'
    else:
        for i, jnuc__vyn in enumerate(xfjv__wkvr):
            pvtk__uytsz += f'        col_arr_{i} = data_arrs_{i}[pivot_idx]\n'
            pvtk__uytsz += (
                f'        if bodo.libs.array_kernels.isna(values_tup[{i}], i):\n'
                )
            pvtk__uytsz += (
                f'            bodo.libs.array_kernels.setna(col_arr_{i}, row_idx)\n'
                )
            pvtk__uytsz += f'        else:\n'
            pvtk__uytsz += (
                f'            col_arr_{i}[row_idx] = values_tup[{i}][i]\n')
    if len(index_tup) == 1:
        pvtk__uytsz += """    index = bodo.utils.conversion.index_from_array(unique_index_arr_tup[0], index_names[0])
"""
    else:
        pvtk__uytsz += """    index = bodo.hiframes.pd_multi_index_ext.init_multi_index(unique_index_arr_tup, index_names, None)
"""
    if yicj__ohc:
        pvtk__uytsz += '    num_rows = len(value_names) * len(pivot_values)\n'
        if is_str_arr_type(value_names):
            pvtk__uytsz += '    total_chars = 0\n'
            pvtk__uytsz += '    for i in range(len(value_names)):\n'
            pvtk__uytsz += """        value_name_str_len = bodo.libs.str_arr_ext.get_str_arr_item_length(value_names, i)
"""
            pvtk__uytsz += '        total_chars += value_name_str_len\n'
            pvtk__uytsz += """    new_value_names = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(pivot_values))
"""
        else:
            pvtk__uytsz += """    new_value_names = bodo.utils.utils.alloc_type(num_rows, value_names, (-1,))
"""
        if is_str_arr_type(pivot_values):
            pvtk__uytsz += '    total_chars = 0\n'
            pvtk__uytsz += '    for i in range(len(pivot_values)):\n'
            pvtk__uytsz += """        pivot_val_str_len = bodo.libs.str_arr_ext.get_str_arr_item_length(pivot_values, i)
"""
            pvtk__uytsz += '        total_chars += pivot_val_str_len\n'
            pvtk__uytsz += """    new_pivot_values = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(value_names))
"""
        else:
            pvtk__uytsz += """    new_pivot_values = bodo.utils.utils.alloc_type(num_rows, pivot_values, (-1,))
"""
        pvtk__uytsz += '    for i in range(len(value_names)):\n'
        pvtk__uytsz += '        for j in range(len(pivot_values)):\n'
        pvtk__uytsz += """            new_value_names[(i * len(pivot_values)) + j] = value_names[i]
"""
        pvtk__uytsz += """            new_pivot_values[(i * len(pivot_values)) + j] = pivot_values[j]
"""
        pvtk__uytsz += """    column_index = bodo.hiframes.pd_multi_index_ext.init_multi_index((new_value_names, new_pivot_values), (None, columns_name), None)
"""
    else:
        pvtk__uytsz += """    column_index =  bodo.utils.conversion.index_from_array(pivot_values, columns_name)
"""
    xmmyo__zat = ', '.join(f'data_arrs_{i}' for i in range(len(xfjv__wkvr)))
    pvtk__uytsz += f"""    table = bodo.hiframes.table.init_runtime_table_from_lists(({xmmyo__zat},), n_rows)
"""
    pvtk__uytsz += (
        '    return bodo.hiframes.pd_dataframe_ext.init_runtime_cols_dataframe(\n'
        )
    pvtk__uytsz += '        (table,), index, column_index\n'
    pvtk__uytsz += '    )\n'
    oepi__zgc = {}
    lgsr__akc = {f'data_arr_typ_{i}': jnuc__vyn for i, jnuc__vyn in
        enumerate(xfjv__wkvr)}
    aah__syoz = {'bodo': bodo, 'np': np, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'info_from_table': info_from_table, **lgsr__akc}
    exec(pvtk__uytsz, aah__syoz, oepi__zgc)
    impl = oepi__zgc['impl']
    return impl


def gen_pandas_parquet_metadata(column_names, data_types, index,
    write_non_range_index_to_metadata, write_rangeindex_to_metadata,
    partition_cols=None, is_runtime_columns=False):
    bfwrt__fjnnr = {}
    bfwrt__fjnnr['columns'] = []
    if partition_cols is None:
        partition_cols = []
    for col_name, beco__vfb in zip(column_names, data_types):
        if col_name in partition_cols:
            continue
        aanft__eio = None
        if isinstance(beco__vfb, bodo.DatetimeArrayType):
            xooq__lhakj = 'datetimetz'
            jsv__xzj = 'datetime64[ns]'
            if isinstance(beco__vfb.tz, int):
                cotj__fhhg = (bodo.libs.pd_datetime_arr_ext.
                    nanoseconds_to_offset(beco__vfb.tz))
            else:
                cotj__fhhg = pd.DatetimeTZDtype(tz=beco__vfb.tz).tz
            aanft__eio = {'timezone': pa.lib.tzinfo_to_string(cotj__fhhg)}
        elif isinstance(beco__vfb, types.Array) or beco__vfb == boolean_array:
            xooq__lhakj = jsv__xzj = beco__vfb.dtype.name
            if jsv__xzj.startswith('datetime'):
                xooq__lhakj = 'datetime'
        elif is_str_arr_type(beco__vfb):
            xooq__lhakj = 'unicode'
            jsv__xzj = 'object'
        elif beco__vfb == binary_array_type:
            xooq__lhakj = 'bytes'
            jsv__xzj = 'object'
        elif isinstance(beco__vfb, DecimalArrayType):
            xooq__lhakj = jsv__xzj = 'object'
        elif isinstance(beco__vfb, IntegerArrayType):
            qmvc__ngcc = beco__vfb.dtype.name
            if qmvc__ngcc.startswith('int'):
                xooq__lhakj = 'Int' + qmvc__ngcc[3:]
            elif qmvc__ngcc.startswith('uint'):
                xooq__lhakj = 'UInt' + qmvc__ngcc[4:]
            else:
                if is_runtime_columns:
                    col_name = 'Runtime determined column of type'
                raise BodoError(
                    'to_parquet(): unknown dtype in nullable Integer column {} {}'
                    .format(col_name, beco__vfb))
            jsv__xzj = beco__vfb.dtype.name
        elif beco__vfb == datetime_date_array_type:
            xooq__lhakj = 'datetime'
            jsv__xzj = 'object'
        elif isinstance(beco__vfb, (StructArrayType, ArrayItemArrayType)):
            xooq__lhakj = 'object'
            jsv__xzj = 'object'
        else:
            if is_runtime_columns:
                col_name = 'Runtime determined column of type'
            raise BodoError(
                'to_parquet(): unsupported column type for metadata generation : {} {}'
                .format(col_name, beco__vfb))
        guiu__ggoya = {'name': col_name, 'field_name': col_name,
            'pandas_type': xooq__lhakj, 'numpy_type': jsv__xzj, 'metadata':
            aanft__eio}
        bfwrt__fjnnr['columns'].append(guiu__ggoya)
    if write_non_range_index_to_metadata:
        if isinstance(index, MultiIndexType):
            raise BodoError('to_parquet: MultiIndex not supported yet')
        if 'none' in index.name:
            yrusx__icbt = '__index_level_0__'
            igpmc__picd = None
        else:
            yrusx__icbt = '%s'
            igpmc__picd = '%s'
        bfwrt__fjnnr['index_columns'] = [yrusx__icbt]
        bfwrt__fjnnr['columns'].append({'name': igpmc__picd, 'field_name':
            yrusx__icbt, 'pandas_type': index.pandas_type_name,
            'numpy_type': index.numpy_type_name, 'metadata': None})
    elif write_rangeindex_to_metadata:
        bfwrt__fjnnr['index_columns'] = [{'kind': 'range', 'name': '%s',
            'start': '%d', 'stop': '%d', 'step': '%d'}]
    else:
        bfwrt__fjnnr['index_columns'] = []
    bfwrt__fjnnr['pandas_version'] = pd.__version__
    return bfwrt__fjnnr


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
        lep__sbdoj = []
        for qyy__ztye in partition_cols:
            try:
                idx = df.columns.index(qyy__ztye)
            except ValueError as lhazb__ppoj:
                raise BodoError(
                    f'Partition column {qyy__ztye} is not in dataframe')
            lep__sbdoj.append(idx)
    else:
        partition_cols = None
    if not is_overload_none(index) and not is_overload_constant_bool(index):
        raise BodoError('to_parquet(): index must be a constant bool or None')
    if not is_overload_int(row_group_size):
        raise BodoError('to_parquet(): row_group_size must be integer')
    from bodo.io.parquet_pio import parquet_write_table_cpp, parquet_write_table_partitioned_cpp
    mwnr__mlbnu = isinstance(df.index, bodo.hiframes.pd_index_ext.
        RangeIndexType)
    rcpy__dkc = df.index is not None and (is_overload_true(_is_parallel) or
        not is_overload_true(_is_parallel) and not mwnr__mlbnu)
    write_non_range_index_to_metadata = is_overload_true(index
        ) or is_overload_none(index) and (not mwnr__mlbnu or
        is_overload_true(_is_parallel))
    write_rangeindex_to_metadata = is_overload_none(index
        ) and mwnr__mlbnu and not is_overload_true(_is_parallel)
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
        wmz__zdm = df.runtime_data_types
        ivx__vwmb = len(wmz__zdm)
        aanft__eio = gen_pandas_parquet_metadata([''] * ivx__vwmb, wmz__zdm,
            df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=True)
        qvlo__mqmh = aanft__eio['columns'][:ivx__vwmb]
        aanft__eio['columns'] = aanft__eio['columns'][ivx__vwmb:]
        qvlo__mqmh = [json.dumps(omgtf__vzpy).replace('""', '{0}') for
            omgtf__vzpy in qvlo__mqmh]
        ilq__wrv = json.dumps(aanft__eio)
        xui__kqtn = '"columns": ['
        khjqa__qnoyl = ilq__wrv.find(xui__kqtn)
        if khjqa__qnoyl == -1:
            raise BodoError(
                'DataFrame.to_parquet(): Unexpected metadata string for runtime columns.  Please return the DataFrame to regular Python to update typing information.'
                )
        zut__lwbfv = khjqa__qnoyl + len(xui__kqtn)
        utbrk__nlsx = ilq__wrv[:zut__lwbfv]
        ilq__wrv = ilq__wrv[zut__lwbfv:]
        muh__kjyh = len(aanft__eio['columns'])
    else:
        ilq__wrv = json.dumps(gen_pandas_parquet_metadata(df.columns, df.
            data, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=False))
    if not is_overload_true(_is_parallel) and mwnr__mlbnu:
        ilq__wrv = ilq__wrv.replace('"%d"', '%d')
        if df.index.name == 'RangeIndexType(none)':
            ilq__wrv = ilq__wrv.replace('"%s"', '%s')
    if not df.is_table_format:
        nrnt__gouib = ', '.join(
            'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
            .format(i) for i in range(len(df.columns)))
    pvtk__uytsz = """def df_to_parquet(df, path, engine='auto', compression='snappy', index=None, partition_cols=None, storage_options=None, row_group_size=-1, _is_parallel=False):
"""
    if df.is_table_format:
        pvtk__uytsz += '    py_table = get_dataframe_table(df)\n'
        pvtk__uytsz += (
            '    table = py_table_to_cpp_table(py_table, py_table_typ)\n')
    else:
        pvtk__uytsz += '    info_list = [{}]\n'.format(nrnt__gouib)
        pvtk__uytsz += '    table = arr_info_list_to_table(info_list)\n'
    if df.has_runtime_cols:
        pvtk__uytsz += '    columns_index = get_dataframe_column_names(df)\n'
        pvtk__uytsz += '    names_arr = index_to_array(columns_index)\n'
        pvtk__uytsz += '    col_names = array_to_info(names_arr)\n'
    else:
        pvtk__uytsz += '    col_names = array_to_info(col_names_arr)\n'
    if is_overload_true(index) or is_overload_none(index) and rcpy__dkc:
        pvtk__uytsz += """    index_col = array_to_info(index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
        tul__nplit = True
    else:
        pvtk__uytsz += '    index_col = array_to_info(np.empty(0))\n'
        tul__nplit = False
    if df.has_runtime_cols:
        pvtk__uytsz += '    columns_lst = []\n'
        pvtk__uytsz += '    num_cols = 0\n'
        for i in range(len(df.runtime_data_types)):
            pvtk__uytsz += f'    for _ in range(len(py_table.block_{i})):\n'
            pvtk__uytsz += f"""        columns_lst.append({qvlo__mqmh[i]!r}.replace('{{0}}', '"' + names_arr[num_cols] + '"'))
"""
            pvtk__uytsz += '        num_cols += 1\n'
        if muh__kjyh:
            pvtk__uytsz += "    columns_lst.append('')\n"
        pvtk__uytsz += '    columns_str = ", ".join(columns_lst)\n'
        pvtk__uytsz += ('    metadata = """' + utbrk__nlsx +
            '""" + columns_str + """' + ilq__wrv + '"""\n')
    else:
        pvtk__uytsz += '    metadata = """' + ilq__wrv + '"""\n'
    pvtk__uytsz += '    if compression is None:\n'
    pvtk__uytsz += "        compression = 'none'\n"
    pvtk__uytsz += '    if df.index.name is not None:\n'
    pvtk__uytsz += '        name_ptr = df.index.name\n'
    pvtk__uytsz += '    else:\n'
    pvtk__uytsz += "        name_ptr = 'null'\n"
    pvtk__uytsz += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(path, parallel=_is_parallel)
"""
    mmkrp__oqxj = None
    if partition_cols:
        mmkrp__oqxj = pd.array([col_name for col_name in df.columns if 
            col_name not in partition_cols])
        uzuxr__pcabp = ', '.join(
            f'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype.categories.values)'
             for i in range(len(df.columns)) if isinstance(df.data[i],
            CategoricalArrayType) and i in lep__sbdoj)
        if uzuxr__pcabp:
            pvtk__uytsz += '    cat_info_list = [{}]\n'.format(uzuxr__pcabp)
            pvtk__uytsz += (
                '    cat_table = arr_info_list_to_table(cat_info_list)\n')
        else:
            pvtk__uytsz += '    cat_table = table\n'
        pvtk__uytsz += (
            '    col_names_no_partitions = array_to_info(col_names_no_parts_arr)\n'
            )
        pvtk__uytsz += (
            f'    part_cols_idxs = np.array({lep__sbdoj}, dtype=np.int32)\n')
        pvtk__uytsz += (
            '    parquet_write_table_partitioned_cpp(unicode_to_utf8(path),\n')
        pvtk__uytsz += """                            table, col_names, col_names_no_partitions, cat_table,
"""
        pvtk__uytsz += (
            '                            part_cols_idxs.ctypes, len(part_cols_idxs),\n'
            )
        pvtk__uytsz += (
            '                            unicode_to_utf8(compression),\n')
        pvtk__uytsz += '                            _is_parallel,\n'
        pvtk__uytsz += (
            '                            unicode_to_utf8(bucket_region),\n')
        pvtk__uytsz += '                            row_group_size)\n'
        pvtk__uytsz += '    delete_table_decref_arrays(table)\n'
        pvtk__uytsz += '    delete_info_decref_array(index_col)\n'
        pvtk__uytsz += (
            '    delete_info_decref_array(col_names_no_partitions)\n')
        pvtk__uytsz += '    delete_info_decref_array(col_names)\n'
        if uzuxr__pcabp:
            pvtk__uytsz += '    delete_table_decref_arrays(cat_table)\n'
    elif write_rangeindex_to_metadata:
        pvtk__uytsz += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        pvtk__uytsz += (
            '                            table, col_names, index_col,\n')
        pvtk__uytsz += '                            ' + str(tul__nplit) + ',\n'
        pvtk__uytsz += (
            '                            unicode_to_utf8(metadata),\n')
        pvtk__uytsz += (
            '                            unicode_to_utf8(compression),\n')
        pvtk__uytsz += (
            '                            _is_parallel, 1, df.index.start,\n')
        pvtk__uytsz += (
            '                            df.index.stop, df.index.step,\n')
        pvtk__uytsz += (
            '                            unicode_to_utf8(name_ptr),\n')
        pvtk__uytsz += (
            '                            unicode_to_utf8(bucket_region),\n')
        pvtk__uytsz += '                            row_group_size)\n'
        pvtk__uytsz += '    delete_table_decref_arrays(table)\n'
        pvtk__uytsz += '    delete_info_decref_array(index_col)\n'
        pvtk__uytsz += '    delete_info_decref_array(col_names)\n'
    else:
        pvtk__uytsz += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        pvtk__uytsz += (
            '                            table, col_names, index_col,\n')
        pvtk__uytsz += '                            ' + str(tul__nplit) + ',\n'
        pvtk__uytsz += (
            '                            unicode_to_utf8(metadata),\n')
        pvtk__uytsz += (
            '                            unicode_to_utf8(compression),\n')
        pvtk__uytsz += (
            '                            _is_parallel, 0, 0, 0, 0,\n')
        pvtk__uytsz += (
            '                            unicode_to_utf8(name_ptr),\n')
        pvtk__uytsz += (
            '                            unicode_to_utf8(bucket_region),\n')
        pvtk__uytsz += '                            row_group_size)\n'
        pvtk__uytsz += '    delete_table_decref_arrays(table)\n'
        pvtk__uytsz += '    delete_info_decref_array(index_col)\n'
        pvtk__uytsz += '    delete_info_decref_array(col_names)\n'
    oepi__zgc = {}
    if df.has_runtime_cols:
        abfd__advqh = None
    else:
        for abo__ywlkk in df.columns:
            if not isinstance(abo__ywlkk, str):
                raise BodoError(
                    'DataFrame.to_parquet(): parquet must have string column names'
                    )
        abfd__advqh = pd.array(df.columns)
    exec(pvtk__uytsz, {'np': np, 'bodo': bodo, 'unicode_to_utf8':
        unicode_to_utf8, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'str_arr_from_sequence': str_arr_from_sequence,
        'parquet_write_table_cpp': parquet_write_table_cpp,
        'parquet_write_table_partitioned_cpp':
        parquet_write_table_partitioned_cpp, 'index_to_array':
        index_to_array, 'delete_info_decref_array':
        delete_info_decref_array, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'col_names_arr': abfd__advqh,
        'py_table_to_cpp_table': py_table_to_cpp_table, 'py_table_typ': df.
        table_type, 'get_dataframe_table': get_dataframe_table,
        'col_names_no_parts_arr': mmkrp__oqxj, 'get_dataframe_column_names':
        get_dataframe_column_names, 'fix_arr_dtype': fix_arr_dtype,
        'decode_if_dict_array': decode_if_dict_array,
        'decode_if_dict_table': decode_if_dict_table}, oepi__zgc)
    vmybe__capq = oepi__zgc['df_to_parquet']
    return vmybe__capq


def to_sql_exception_guard(df, name, con, schema=None, if_exists='fail',
    index=True, index_label=None, chunksize=None, dtype=None, method=None,
    _is_table_create=False, _is_parallel=False):
    rphpk__sapp = 'all_ok'
    umtkx__syy, ophp__cdlsf = bodo.ir.sql_ext.parse_dbtype(con)
    if _is_parallel and bodo.get_rank() == 0:
        urpe__jzdkk = 100
        if chunksize is None:
            tndqs__jypfu = urpe__jzdkk
        else:
            tndqs__jypfu = min(chunksize, urpe__jzdkk)
        if _is_table_create:
            df = df.iloc[:tndqs__jypfu, :]
        else:
            df = df.iloc[tndqs__jypfu:, :]
            if len(df) == 0:
                return rphpk__sapp
    aivyq__cqygu = df.columns
    try:
        if umtkx__syy == 'snowflake':
            if ophp__cdlsf and con.count(ophp__cdlsf) == 1:
                con = con.replace(ophp__cdlsf, quote(ophp__cdlsf))
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
                df.columns = [(wdufm__wfsal.upper() if wdufm__wfsal.islower
                    () else wdufm__wfsal) for wdufm__wfsal in df.columns]
            except ImportError as lhazb__ppoj:
                rphpk__sapp = (
                    "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires both snowflake-sqlalchemy and snowflake-connector-python. These can be installed by calling 'conda install -c conda-forge snowflake-sqlalchemy snowflake-connector-python' or 'pip install snowflake-sqlalchemy snowflake-connector-python'."
                    )
                return rphpk__sapp
        if umtkx__syy == 'oracle':
            import sqlalchemy as sa
            yli__ldoq = bodo.typeof(df)
            ejuhb__cre = {}
            for wdufm__wfsal, zbft__sxdig in zip(yli__ldoq.columns,
                yli__ldoq.data):
                if df[wdufm__wfsal].dtype == 'object':
                    if zbft__sxdig == datetime_date_array_type:
                        ejuhb__cre[wdufm__wfsal] = sa.types.Date
                    elif zbft__sxdig == bodo.string_array_type:
                        ejuhb__cre[wdufm__wfsal] = sa.types.VARCHAR(df[
                            wdufm__wfsal].str.len().max())
            dtype = ejuhb__cre
        try:
            df.to_sql(name, con, schema, if_exists, index, index_label,
                chunksize, dtype, method)
        except Exception as rrd__xnp:
            rphpk__sapp = rrd__xnp.args[0]
        return rphpk__sapp
    finally:
        df.columns = aivyq__cqygu


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
        ezctt__frgqb = bodo.libs.distributed_api.get_rank()
        rphpk__sapp = 'unset'
        if ezctt__frgqb != 0:
            rphpk__sapp = bcast_scalar(rphpk__sapp)
        elif ezctt__frgqb == 0:
            rphpk__sapp = to_sql_exception_guard_encaps(df, name, con,
                schema, if_exists, index, index_label, chunksize, dtype,
                method, True, _is_parallel)
            rphpk__sapp = bcast_scalar(rphpk__sapp)
        if_exists = 'append'
        if _is_parallel and rphpk__sapp == 'all_ok':
            rphpk__sapp = to_sql_exception_guard_encaps(df, name, con,
                schema, if_exists, index, index_label, chunksize, dtype,
                method, False, _is_parallel)
        if rphpk__sapp != 'all_ok':
            print('err_msg=', rphpk__sapp)
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
        yxblx__cjwzb = get_overload_const_str(path_or_buf)
        if yxblx__cjwzb.endswith(('.gz', '.bz2', '.zip', '.xz')):
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
        rtnr__ccw = bodo.io.fs_io.get_s3_bucket_region_njit(path_or_buf,
            parallel=False)
        if lines and orient == 'records':
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, True,
                unicode_to_utf8(rtnr__ccw))
            bodo.utils.utils.check_and_propagate_cpp_exception()
        else:
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, False,
                unicode_to_utf8(rtnr__ccw))
            bodo.utils.utils.check_and_propagate_cpp_exception()
    return _impl


@overload(pd.get_dummies, inline='always', no_unliteral=True)
def get_dummies(data, prefix=None, prefix_sep='_', dummy_na=False, columns=
    None, sparse=False, drop_first=False, dtype=None):
    akyi__nhvn = {'prefix': prefix, 'prefix_sep': prefix_sep, 'dummy_na':
        dummy_na, 'columns': columns, 'sparse': sparse, 'drop_first':
        drop_first, 'dtype': dtype}
    phsfy__vayvk = {'prefix': None, 'prefix_sep': '_', 'dummy_na': False,
        'columns': None, 'sparse': False, 'drop_first': False, 'dtype': None}
    check_unsupported_args('pandas.get_dummies', akyi__nhvn, phsfy__vayvk,
        package_name='pandas', module_name='General')
    if not categorical_can_construct_dataframe(data):
        raise BodoError(
            'pandas.get_dummies() only support categorical data types with explicitly known categories'
            )
    pvtk__uytsz = """def impl(data, prefix=None, prefix_sep='_', dummy_na=False, columns=None, sparse=False, drop_first=False, dtype=None,):
"""
    if isinstance(data, SeriesType):
        qpmo__rmca = data.data.dtype.categories
        pvtk__uytsz += (
            '  data_values = bodo.hiframes.pd_series_ext.get_series_data(data)\n'
            )
    else:
        qpmo__rmca = data.dtype.categories
        pvtk__uytsz += '  data_values = data\n'
    ccnv__ngm = len(qpmo__rmca)
    pvtk__uytsz += """  codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(data_values)
"""
    pvtk__uytsz += '  numba.parfors.parfor.init_prange()\n'
    pvtk__uytsz += '  n = len(data_values)\n'
    for i in range(ccnv__ngm):
        pvtk__uytsz += '  data_arr_{} = np.empty(n, np.uint8)\n'.format(i)
    pvtk__uytsz += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    pvtk__uytsz += '      if bodo.libs.array_kernels.isna(data_values, i):\n'
    for fequp__szguo in range(ccnv__ngm):
        pvtk__uytsz += '          data_arr_{}[i] = 0\n'.format(fequp__szguo)
    pvtk__uytsz += '      else:\n'
    for fjfsk__zjag in range(ccnv__ngm):
        pvtk__uytsz += '          data_arr_{0}[i] = codes[i] == {0}\n'.format(
            fjfsk__zjag)
    nrnt__gouib = ', '.join(f'data_arr_{i}' for i in range(ccnv__ngm))
    index = 'bodo.hiframes.pd_index_ext.init_range_index(0, n, 1, None)'
    if isinstance(qpmo__rmca[0], np.datetime64):
        qpmo__rmca = tuple(pd.Timestamp(wdufm__wfsal) for wdufm__wfsal in
            qpmo__rmca)
    elif isinstance(qpmo__rmca[0], np.timedelta64):
        qpmo__rmca = tuple(pd.Timedelta(wdufm__wfsal) for wdufm__wfsal in
            qpmo__rmca)
    return bodo.hiframes.dataframe_impl._gen_init_df(pvtk__uytsz,
        qpmo__rmca, nrnt__gouib, index)


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
    for frwg__uub in pd_unsupported:
        xtcb__psp = mod_name + '.' + frwg__uub.__name__
        overload(frwg__uub, no_unliteral=True)(create_unsupported_overload(
            xtcb__psp))


def _install_dataframe_unsupported():
    for cican__bvthw in dataframe_unsupported_attrs:
        eytfi__aop = 'DataFrame.' + cican__bvthw
        overload_attribute(DataFrameType, cican__bvthw)(
            create_unsupported_overload(eytfi__aop))
    for xtcb__psp in dataframe_unsupported:
        eytfi__aop = 'DataFrame.' + xtcb__psp + '()'
        overload_method(DataFrameType, xtcb__psp)(create_unsupported_overload
            (eytfi__aop))


_install_pd_unsupported('pandas', pd_unsupported)
_install_pd_unsupported('pandas.util', pd_util_unsupported)
_install_dataframe_unsupported()
