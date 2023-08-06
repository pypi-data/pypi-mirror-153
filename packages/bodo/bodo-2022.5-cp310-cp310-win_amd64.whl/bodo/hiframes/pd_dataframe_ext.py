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
            rtsfh__cznp = f'{len(self.data)} columns of types {set(self.data)}'
            cpv__vshk = (
                f"('{self.columns[0]}', '{self.columns[1]}', ..., '{self.columns[-1]}')"
                )
            return (
                f'dataframe({rtsfh__cznp}, {self.index}, {cpv__vshk}, {self.dist}, {self.is_table_format})'
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
        return {hkgsg__nlrn: i for i, hkgsg__nlrn in enumerate(self.columns)}

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
            xytv__llxe = (self.index if self.index == other.index else self
                .index.unify(typingctx, other.index))
            data = tuple(kjvs__yti.unify(typingctx, afcs__vvzku) if 
                kjvs__yti != afcs__vvzku else kjvs__yti for kjvs__yti,
                afcs__vvzku in zip(self.data, other.data))
            dist = Distribution(min(self.dist.value, other.dist.value))
            if xytv__llxe is not None and None not in data:
                return DataFrameType(data, xytv__llxe, self.columns, dist,
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
        return all(kjvs__yti.is_precise() for kjvs__yti in self.data
            ) and self.index.is_precise()

    def replace_col_type(self, col_name, new_type):
        if col_name not in self.columns:
            raise ValueError(
                f"DataFrameType.replace_col_type replaced column must be found in the DataFrameType. '{col_name}' not found in DataFrameType with columns {self.columns}"
                )
        bqxpb__peu = self.columns.index(col_name)
        mdk__lzwvn = tuple(list(self.data[:bqxpb__peu]) + [new_type] + list
            (self.data[bqxpb__peu + 1:]))
        return DataFrameType(mdk__lzwvn, self.index, self.columns, self.
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
        bxd__clezy = [('data', data_typ), ('index', fe_type.df_type.index),
            ('parent', types.pyobject)]
        if fe_type.df_type.has_runtime_cols:
            bxd__clezy.append(('columns', fe_type.df_type.runtime_colname_typ))
        super(DataFramePayloadModel, self).__init__(dmm, fe_type, bxd__clezy)


@register_model(DataFrameType)
class DataFrameModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = DataFramePayloadType(fe_type)
        bxd__clezy = [('meminfo', types.MemInfoPointer(payload_type)), (
            'parent', types.pyobject)]
        super(DataFrameModel, self).__init__(dmm, fe_type, bxd__clezy)


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
        dlo__vixx = 'n',
        rhks__zbhnq = {'n': 5}
        gqnh__yidk, dcxw__efel = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, dlo__vixx, rhks__zbhnq)
        qlen__dbzx = dcxw__efel[0]
        if not is_overload_int(qlen__dbzx):
            raise BodoError(f"{func_name}(): 'n' must be an Integer")
        msb__pnu = df.copy(is_table_format=False)
        return msb__pnu(*dcxw__efel).replace(pysig=gqnh__yidk)

    @bound_function('df.corr')
    def resolve_corr(self, df, args, kws):
        func_name = 'DataFrame.corr'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        kbpzo__bqq = (df,) + args
        dlo__vixx = 'df', 'method', 'min_periods'
        rhks__zbhnq = {'method': 'pearson', 'min_periods': 1}
        xoxi__bwm = 'method',
        gqnh__yidk, dcxw__efel = bodo.utils.typing.fold_typing_args(func_name,
            kbpzo__bqq, kws, dlo__vixx, rhks__zbhnq, xoxi__bwm)
        rkb__rti = dcxw__efel[2]
        if not is_overload_int(rkb__rti):
            raise BodoError(f"{func_name}(): 'min_periods' must be an Integer")
        idksn__tvho = []
        bly__unc = []
        for hkgsg__nlrn, yjwgh__cut in zip(df.columns, df.data):
            if bodo.utils.typing._is_pandas_numeric_dtype(yjwgh__cut.dtype):
                idksn__tvho.append(hkgsg__nlrn)
                bly__unc.append(types.Array(types.float64, 1, 'A'))
        if len(idksn__tvho) == 0:
            raise_bodo_error('DataFrame.corr(): requires non-empty dataframe')
        bly__unc = tuple(bly__unc)
        idksn__tvho = tuple(idksn__tvho)
        index_typ = bodo.utils.typing.type_col_to_index(idksn__tvho)
        msb__pnu = DataFrameType(bly__unc, index_typ, idksn__tvho)
        return msb__pnu(*dcxw__efel).replace(pysig=gqnh__yidk)

    @bound_function('df.pipe', no_unliteral=True)
    def resolve_pipe(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.pipe()')
        return bodo.hiframes.pd_groupby_ext.resolve_obj_pipe(self, df, args,
            kws, 'DataFrame')

    @bound_function('df.apply', no_unliteral=True)
    def resolve_apply(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.apply()')
        kws = dict(kws)
        icqdk__tiq = args[0] if len(args) > 0 else kws.pop('func', None)
        axis = args[1] if len(args) > 1 else kws.pop('axis', types.literal(0))
        kedbp__ghg = args[2] if len(args) > 2 else kws.pop('raw', types.
            literal(False))
        zwdw__cdj = args[3] if len(args) > 3 else kws.pop('result_type',
            types.none)
        rgvqp__dejth = args[4] if len(args) > 4 else kws.pop('args', types.
            Tuple([]))
        lksk__upz = dict(raw=kedbp__ghg, result_type=zwdw__cdj)
        qtobs__swrg = dict(raw=False, result_type=None)
        check_unsupported_args('Dataframe.apply', lksk__upz, qtobs__swrg,
            package_name='pandas', module_name='DataFrame')
        gjqnx__bfx = True
        if types.unliteral(icqdk__tiq) == types.unicode_type:
            if not is_overload_constant_str(icqdk__tiq):
                raise BodoError(
                    f'DataFrame.apply(): string argument (for builtins) must be a compile time constant'
                    )
            gjqnx__bfx = False
        if not is_overload_constant_int(axis):
            raise BodoError(
                'Dataframe.apply(): axis argument must be a compile time constant.'
                )
        rrxy__vxpgc = get_overload_const_int(axis)
        if gjqnx__bfx and rrxy__vxpgc != 1:
            raise BodoError(
                'Dataframe.apply(): only axis=1 supported for user-defined functions'
                )
        elif rrxy__vxpgc not in (0, 1):
            raise BodoError('Dataframe.apply(): axis must be either 0 or 1')
        aelzz__tghl = []
        for arr_typ in df.data:
            aext__pmxr = SeriesType(arr_typ.dtype, arr_typ, df.index,
                string_type)
            iisha__iwuh = self.context.resolve_function_type(operator.
                getitem, (SeriesIlocType(aext__pmxr), types.int64), {}
                ).return_type
            aelzz__tghl.append(iisha__iwuh)
        hgjie__ysi = types.none
        tlq__syuu = HeterogeneousIndexType(types.BaseTuple.from_types(tuple
            (types.literal(hkgsg__nlrn) for hkgsg__nlrn in df.columns)), None)
        ltwil__lhcoc = types.BaseTuple.from_types(aelzz__tghl)
        wrort__pje = types.Tuple([types.bool_] * len(ltwil__lhcoc))
        lejt__ywc = bodo.NullableTupleType(ltwil__lhcoc, wrort__pje)
        xlv__kegx = df.index.dtype
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df.index,
            'DataFrame.apply()')
        if xlv__kegx == types.NPDatetime('ns'):
            xlv__kegx = bodo.pd_timestamp_type
        if xlv__kegx == types.NPTimedelta('ns'):
            xlv__kegx = bodo.pd_timedelta_type
        if is_heterogeneous_tuple_type(ltwil__lhcoc):
            tma__wid = HeterogeneousSeriesType(lejt__ywc, tlq__syuu, xlv__kegx)
        else:
            tma__wid = SeriesType(ltwil__lhcoc.dtype, lejt__ywc, tlq__syuu,
                xlv__kegx)
        akl__wicxy = tma__wid,
        if rgvqp__dejth is not None:
            akl__wicxy += tuple(rgvqp__dejth.types)
        try:
            if not gjqnx__bfx:
                rcznu__tbu = bodo.utils.transform.get_udf_str_return_type(df,
                    get_overload_const_str(icqdk__tiq), self.context,
                    'DataFrame.apply', axis if rrxy__vxpgc == 1 else None)
            else:
                rcznu__tbu = get_const_func_output_type(icqdk__tiq,
                    akl__wicxy, kws, self.context, numba.core.registry.
                    cpu_target.target_context)
        except Exception as sokr__bpel:
            raise_bodo_error(get_udf_error_msg('DataFrame.apply()', sokr__bpel)
                )
        if gjqnx__bfx:
            if not (is_overload_constant_int(axis) and 
                get_overload_const_int(axis) == 1):
                raise BodoError(
                    'Dataframe.apply(): only user-defined functions with axis=1 supported'
                    )
            if isinstance(rcznu__tbu, (SeriesType, HeterogeneousSeriesType)
                ) and rcznu__tbu.const_info is None:
                raise BodoError(
                    'Invalid Series output in UDF (Series with constant length and constant Index value expected)'
                    )
            if isinstance(rcznu__tbu, HeterogeneousSeriesType):
                borqk__qnj, xwq__dhm = rcznu__tbu.const_info
                if isinstance(rcznu__tbu.data, bodo.libs.nullable_tuple_ext
                    .NullableTupleType):
                    sxt__dts = rcznu__tbu.data.tuple_typ.types
                elif isinstance(rcznu__tbu.data, types.Tuple):
                    sxt__dts = rcznu__tbu.data.types
                else:
                    raise_bodo_error(
                        'df.apply(): Unexpected Series return type for Heterogeneous data'
                        )
                ceq__bmph = tuple(to_nullable_type(dtype_to_array_type(
                    qqffn__hqxhy)) for qqffn__hqxhy in sxt__dts)
                qat__ilk = DataFrameType(ceq__bmph, df.index, xwq__dhm)
            elif isinstance(rcznu__tbu, SeriesType):
                yueqz__wph, xwq__dhm = rcznu__tbu.const_info
                ceq__bmph = tuple(to_nullable_type(dtype_to_array_type(
                    rcznu__tbu.dtype)) for borqk__qnj in range(yueqz__wph))
                qat__ilk = DataFrameType(ceq__bmph, df.index, xwq__dhm)
            else:
                xke__bch = get_udf_out_arr_type(rcznu__tbu)
                qat__ilk = SeriesType(xke__bch.dtype, xke__bch, df.index, None)
        else:
            qat__ilk = rcznu__tbu
        qbyq__ukdcs = ', '.join("{} = ''".format(kjvs__yti) for kjvs__yti in
            kws.keys())
        ezw__epg = f"""def apply_stub(func, axis=0, raw=False, result_type=None, args=(), {qbyq__ukdcs}):
"""
        ezw__epg += '    pass\n'
        vfg__zksc = {}
        exec(ezw__epg, {}, vfg__zksc)
        vadl__cogt = vfg__zksc['apply_stub']
        gqnh__yidk = numba.core.utils.pysignature(vadl__cogt)
        pqz__ymz = (icqdk__tiq, axis, kedbp__ghg, zwdw__cdj, rgvqp__dejth
            ) + tuple(kws.values())
        return signature(qat__ilk, *pqz__ymz).replace(pysig=gqnh__yidk)

    @bound_function('df.plot', no_unliteral=True)
    def resolve_plot(self, df, args, kws):
        func_name = 'DataFrame.plot'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        dlo__vixx = ('x', 'y', 'kind', 'figsize', 'ax', 'subplots',
            'sharex', 'sharey', 'layout', 'use_index', 'title', 'grid',
            'legend', 'style', 'logx', 'logy', 'loglog', 'xticks', 'yticks',
            'xlim', 'ylim', 'rot', 'fontsize', 'colormap', 'table', 'yerr',
            'xerr', 'secondary_y', 'sort_columns', 'xlabel', 'ylabel',
            'position', 'stacked', 'mark_right', 'include_bool', 'backend')
        rhks__zbhnq = {'x': None, 'y': None, 'kind': 'line', 'figsize':
            None, 'ax': None, 'subplots': False, 'sharex': None, 'sharey': 
            False, 'layout': None, 'use_index': True, 'title': None, 'grid':
            None, 'legend': True, 'style': None, 'logx': False, 'logy': 
            False, 'loglog': False, 'xticks': None, 'yticks': None, 'xlim':
            None, 'ylim': None, 'rot': None, 'fontsize': None, 'colormap':
            None, 'table': False, 'yerr': None, 'xerr': None, 'secondary_y':
            False, 'sort_columns': False, 'xlabel': None, 'ylabel': None,
            'position': 0.5, 'stacked': False, 'mark_right': True,
            'include_bool': False, 'backend': None}
        xoxi__bwm = ('subplots', 'sharex', 'sharey', 'layout', 'use_index',
            'grid', 'style', 'logx', 'logy', 'loglog', 'xlim', 'ylim',
            'rot', 'colormap', 'table', 'yerr', 'xerr', 'sort_columns',
            'secondary_y', 'colorbar', 'position', 'stacked', 'mark_right',
            'include_bool', 'backend')
        gqnh__yidk, dcxw__efel = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, dlo__vixx, rhks__zbhnq, xoxi__bwm)
        ajmu__wqjm = dcxw__efel[2]
        if not is_overload_constant_str(ajmu__wqjm):
            raise BodoError(
                f"{func_name}: kind must be a constant string and one of ('line', 'scatter')."
                )
        xzkr__zbs = dcxw__efel[0]
        if not is_overload_none(xzkr__zbs) and not (is_overload_int(
            xzkr__zbs) or is_overload_constant_str(xzkr__zbs)):
            raise BodoError(
                f'{func_name}: x must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(xzkr__zbs):
            yrao__sis = get_overload_const_str(xzkr__zbs)
            if yrao__sis not in df.columns:
                raise BodoError(f'{func_name}: {yrao__sis} column not found.')
        elif is_overload_int(xzkr__zbs):
            owjly__wzqsh = get_overload_const_int(xzkr__zbs)
            if owjly__wzqsh > len(df.columns):
                raise BodoError(
                    f'{func_name}: x: {owjly__wzqsh} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            xzkr__zbs = df.columns[xzkr__zbs]
        bpz__iwby = dcxw__efel[1]
        if not is_overload_none(bpz__iwby) and not (is_overload_int(
            bpz__iwby) or is_overload_constant_str(bpz__iwby)):
            raise BodoError(
                'df.plot(): y must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(bpz__iwby):
            aei__yiuux = get_overload_const_str(bpz__iwby)
            if aei__yiuux not in df.columns:
                raise BodoError(f'{func_name}: {aei__yiuux} column not found.')
        elif is_overload_int(bpz__iwby):
            wjayq__eau = get_overload_const_int(bpz__iwby)
            if wjayq__eau > len(df.columns):
                raise BodoError(
                    f'{func_name}: y: {wjayq__eau} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            bpz__iwby = df.columns[bpz__iwby]
        ytsvi__ipytl = dcxw__efel[3]
        if not is_overload_none(ytsvi__ipytl) and not is_tuple_like_type(
            ytsvi__ipytl):
            raise BodoError(
                f'{func_name}: figsize must be a constant numeric tuple (width, height) or None.'
                )
        czqhn__dhhnb = dcxw__efel[10]
        if not is_overload_none(czqhn__dhhnb) and not is_overload_constant_str(
            czqhn__dhhnb):
            raise BodoError(
                f'{func_name}: title must be a constant string or None.')
        ssqly__ppdz = dcxw__efel[12]
        if not is_overload_bool(ssqly__ppdz):
            raise BodoError(f'{func_name}: legend must be a boolean type.')
        hngr__wqvhs = dcxw__efel[17]
        if not is_overload_none(hngr__wqvhs) and not is_tuple_like_type(
            hngr__wqvhs):
            raise BodoError(
                f'{func_name}: xticks must be a constant tuple or None.')
        tmjl__cbjf = dcxw__efel[18]
        if not is_overload_none(tmjl__cbjf) and not is_tuple_like_type(
            tmjl__cbjf):
            raise BodoError(
                f'{func_name}: yticks must be a constant tuple or None.')
        hzsw__wktyx = dcxw__efel[22]
        if not is_overload_none(hzsw__wktyx) and not is_overload_int(
            hzsw__wktyx):
            raise BodoError(
                f'{func_name}: fontsize must be an integer or None.')
        icvxj__nbre = dcxw__efel[29]
        if not is_overload_none(icvxj__nbre) and not is_overload_constant_str(
            icvxj__nbre):
            raise BodoError(
                f'{func_name}: xlabel must be a constant string or None.')
        nvc__vcwi = dcxw__efel[30]
        if not is_overload_none(nvc__vcwi) and not is_overload_constant_str(
            nvc__vcwi):
            raise BodoError(
                f'{func_name}: ylabel must be a constant string or None.')
        mad__zpsbw = types.List(types.mpl_line_2d_type)
        ajmu__wqjm = get_overload_const_str(ajmu__wqjm)
        if ajmu__wqjm == 'scatter':
            if is_overload_none(xzkr__zbs) and is_overload_none(bpz__iwby):
                raise BodoError(
                    f'{func_name}: {ajmu__wqjm} requires an x and y column.')
            elif is_overload_none(xzkr__zbs):
                raise BodoError(
                    f'{func_name}: {ajmu__wqjm} x column is missing.')
            elif is_overload_none(bpz__iwby):
                raise BodoError(
                    f'{func_name}: {ajmu__wqjm} y column is missing.')
            mad__zpsbw = types.mpl_path_collection_type
        elif ajmu__wqjm != 'line':
            raise BodoError(f'{func_name}: {ajmu__wqjm} plot is not supported.'
                )
        return signature(mad__zpsbw, *dcxw__efel).replace(pysig=gqnh__yidk)

    def generic_resolve(self, df, attr):
        if self._is_existing_attr(attr):
            return
        check_runtime_cols_unsupported(df,
            'Acessing DataFrame columns by attribute')
        if attr in df.columns:
            dcr__xcy = df.columns.index(attr)
            arr_typ = df.data[dcr__xcy]
            return SeriesType(arr_typ.dtype, arr_typ, df.index, types.
                StringLiteral(attr))
        if len(df.columns) > 0 and isinstance(df.columns[0], tuple):
            wwxo__vxorz = []
            mdk__lzwvn = []
            exxy__stsd = False
            for i, brgla__hitt in enumerate(df.columns):
                if brgla__hitt[0] != attr:
                    continue
                exxy__stsd = True
                wwxo__vxorz.append(brgla__hitt[1] if len(brgla__hitt) == 2 else
                    brgla__hitt[1:])
                mdk__lzwvn.append(df.data[i])
            if exxy__stsd:
                return DataFrameType(tuple(mdk__lzwvn), df.index, tuple(
                    wwxo__vxorz))


DataFrameAttribute._no_unliteral = True


@overload(operator.getitem, no_unliteral=True)
def namedtuple_getitem_overload(tup, idx):
    if isinstance(tup, types.BaseNamedTuple) and is_overload_constant_str(idx):
        dqk__uma = get_overload_const_str(idx)
        val_ind = tup.instance_class._fields.index(dqk__uma)
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
        ngk__eksit = builder.extract_value(payload.data, i)
        context.nrt.decref(builder, df_type.data[i], ngk__eksit)
    context.nrt.decref(builder, df_type.index, payload.index)


def define_df_dtor(context, builder, df_type, payload_type):
    dczjf__mluuc = builder.module
    vrt__nshs = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    awzy__zorqp = cgutils.get_or_insert_function(dczjf__mluuc, vrt__nshs,
        name='.dtor.df.{}'.format(df_type))
    if not awzy__zorqp.is_declaration:
        return awzy__zorqp
    awzy__zorqp.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(awzy__zorqp.append_basic_block())
    xkobk__xmmkv = awzy__zorqp.args[0]
    ajpqq__bmyhp = context.get_value_type(payload_type).as_pointer()
    zcc__cmb = builder.bitcast(xkobk__xmmkv, ajpqq__bmyhp)
    payload = context.make_helper(builder, payload_type, ref=zcc__cmb)
    decref_df_data(context, builder, payload, df_type)
    has_parent = cgutils.is_not_null(builder, payload.parent)
    with builder.if_then(has_parent):
        mttv__rcl = context.get_python_api(builder)
        upsvb__nbmu = mttv__rcl.gil_ensure()
        mttv__rcl.decref(payload.parent)
        mttv__rcl.gil_release(upsvb__nbmu)
    builder.ret_void()
    return awzy__zorqp


def construct_dataframe(context, builder, df_type, data_tup, index_val,
    parent=None, colnames=None):
    payload_type = DataFramePayloadType(df_type)
    rgj__mnu = cgutils.create_struct_proxy(payload_type)(context, builder)
    rgj__mnu.data = data_tup
    rgj__mnu.index = index_val
    if colnames is not None:
        assert df_type.has_runtime_cols, 'construct_dataframe can only provide colnames if columns are determined at runtime'
        rgj__mnu.columns = colnames
    jqm__psvi = context.get_value_type(payload_type)
    fesc__xlljp = context.get_abi_sizeof(jqm__psvi)
    eylc__xgbm = define_df_dtor(context, builder, df_type, payload_type)
    rqmsd__wvpqv = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, fesc__xlljp), eylc__xgbm)
    wei__gfivo = context.nrt.meminfo_data(builder, rqmsd__wvpqv)
    aatwv__nks = builder.bitcast(wei__gfivo, jqm__psvi.as_pointer())
    lymhv__nki = cgutils.create_struct_proxy(df_type)(context, builder)
    lymhv__nki.meminfo = rqmsd__wvpqv
    if parent is None:
        lymhv__nki.parent = cgutils.get_null_value(lymhv__nki.parent.type)
    else:
        lymhv__nki.parent = parent
        rgj__mnu.parent = parent
        has_parent = cgutils.is_not_null(builder, parent)
        with builder.if_then(has_parent):
            mttv__rcl = context.get_python_api(builder)
            upsvb__nbmu = mttv__rcl.gil_ensure()
            mttv__rcl.incref(parent)
            mttv__rcl.gil_release(upsvb__nbmu)
    builder.store(rgj__mnu._getvalue(), aatwv__nks)
    return lymhv__nki._getvalue()


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
        dcpc__mohzd = [data_typ.dtype.arr_types.dtype] * len(data_typ.dtype
            .arr_types)
    else:
        dcpc__mohzd = [qqffn__hqxhy for qqffn__hqxhy in data_typ.dtype.
            arr_types]
    rck__lji = DataFrameType(tuple(dcpc__mohzd + [colnames_index_typ]),
        index_typ, None, is_table_format=True)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup, index, col_names = args
        parent = None
        fbch__nkixn = construct_dataframe(context, builder, df_type,
            data_tup, index, parent, col_names)
        context.nrt.incref(builder, data_typ, data_tup)
        context.nrt.incref(builder, index_typ, index)
        context.nrt.incref(builder, colnames_index_typ, col_names)
        return fbch__nkixn
    sig = signature(rck__lji, data_typ, index_typ, colnames_index_typ)
    return sig, codegen


@intrinsic
def init_dataframe(typingctx, data_tup_typ, index_typ, col_names_typ=None):
    assert is_pd_index_type(index_typ) or isinstance(index_typ, MultiIndexType
        ), 'init_dataframe(): invalid index type'
    yueqz__wph = len(data_tup_typ.types)
    if yueqz__wph == 0:
        column_names = ()
    elif isinstance(col_names_typ, types.TypeRef):
        column_names = col_names_typ.instance_type.columns
    else:
        column_names = get_const_tup_vals(col_names_typ)
    if yueqz__wph == 1 and isinstance(data_tup_typ.types[0], TableType):
        yueqz__wph = len(data_tup_typ.types[0].arr_types)
    assert len(column_names
        ) == yueqz__wph, 'init_dataframe(): number of column names does not match number of columns'
    is_table_format = False
    vitov__gyfim = data_tup_typ.types
    if yueqz__wph != 0 and isinstance(data_tup_typ.types[0], TableType):
        vitov__gyfim = data_tup_typ.types[0].arr_types
        is_table_format = True
    rck__lji = DataFrameType(vitov__gyfim, index_typ, column_names,
        is_table_format=is_table_format)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup = args[0]
        index_val = args[1]
        parent = None
        if is_table_format:
            pulo__mpab = cgutils.create_struct_proxy(rck__lji.table_type)(
                context, builder, builder.extract_value(data_tup, 0))
            parent = pulo__mpab.parent
        fbch__nkixn = construct_dataframe(context, builder, df_type,
            data_tup, index_val, parent, None)
        context.nrt.incref(builder, data_tup_typ, data_tup)
        context.nrt.incref(builder, index_typ, index_val)
        return fbch__nkixn
    sig = signature(rck__lji, data_tup_typ, index_typ, col_names_typ)
    return sig, codegen


@intrinsic
def has_parent(typingctx, df=None):
    check_runtime_cols_unsupported(df, 'has_parent')

    def codegen(context, builder, sig, args):
        lymhv__nki = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        return cgutils.is_not_null(builder, lymhv__nki.parent)
    return signature(types.bool_, df), codegen


@intrinsic
def _column_needs_unboxing(typingctx, df_typ, i_typ=None):
    check_runtime_cols_unsupported(df_typ, '_column_needs_unboxing')
    assert isinstance(df_typ, DataFrameType) and is_overload_constant_int(i_typ
        )

    def codegen(context, builder, sig, args):
        rgj__mnu = get_dataframe_payload(context, builder, df_typ, args[0])
        fdtl__pvp = get_overload_const_int(i_typ)
        arr_typ = df_typ.data[fdtl__pvp]
        if df_typ.is_table_format:
            pulo__mpab = cgutils.create_struct_proxy(df_typ.table_type)(context
                , builder, builder.extract_value(rgj__mnu.data, 0))
            olwb__bxff = df_typ.table_type.type_to_blk[arr_typ]
            fcg__kng = getattr(pulo__mpab, f'block_{olwb__bxff}')
            wnx__hefkq = ListInstance(context, builder, types.List(arr_typ),
                fcg__kng)
            kulcu__xvr = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[fdtl__pvp])
            ngk__eksit = wnx__hefkq.getitem(kulcu__xvr)
        else:
            ngk__eksit = builder.extract_value(rgj__mnu.data, fdtl__pvp)
        oke__xah = cgutils.alloca_once_value(builder, ngk__eksit)
        jsgzy__zwjhy = cgutils.alloca_once_value(builder, context.
            get_constant_null(arr_typ))
        return is_ll_eq(builder, oke__xah, jsgzy__zwjhy)
    return signature(types.bool_, df_typ, i_typ), codegen


def get_dataframe_payload(context, builder, df_type, value):
    rqmsd__wvpqv = cgutils.create_struct_proxy(df_type)(context, builder, value
        ).meminfo
    payload_type = DataFramePayloadType(df_type)
    payload = context.nrt.meminfo_data(builder, rqmsd__wvpqv)
    ajpqq__bmyhp = context.get_value_type(payload_type).as_pointer()
    payload = builder.bitcast(payload, ajpqq__bmyhp)
    return context.make_helper(builder, payload_type, ref=payload)


@intrinsic
def _get_dataframe_data(typingctx, df_typ=None):
    check_runtime_cols_unsupported(df_typ, '_get_dataframe_data')
    rck__lji = types.Tuple(df_typ.data)
    if df_typ.is_table_format:
        rck__lji = types.Tuple([TableType(df_typ.data)])
    sig = signature(rck__lji, df_typ)

    def codegen(context, builder, signature, args):
        rgj__mnu = get_dataframe_payload(context, builder, signature.args[0
            ], args[0])
        return impl_ret_borrowed(context, builder, signature.return_type,
            rgj__mnu.data)
    return sig, codegen


@intrinsic
def get_dataframe_index(typingctx, df_typ=None):

    def codegen(context, builder, signature, args):
        rgj__mnu = get_dataframe_payload(context, builder, signature.args[0
            ], args[0])
        return impl_ret_borrowed(context, builder, df_typ.index, rgj__mnu.index
            )
    rck__lji = df_typ.index
    sig = signature(rck__lji, df_typ)
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
        msb__pnu = df.data[i]
        return msb__pnu(*args)


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
        rgj__mnu = get_dataframe_payload(context, builder, signature.args[0
            ], args[0])
        return impl_ret_borrowed(context, builder, df_typ.table_type,
            builder.extract_value(rgj__mnu.data, 0))
    return df_typ.table_type(df_typ), codegen


@intrinsic
def get_dataframe_column_names(typingctx, df_typ=None):
    assert df_typ.has_runtime_cols, 'get_dataframe_column_names() expects columns to be determined at runtime'

    def codegen(context, builder, signature, args):
        rgj__mnu = get_dataframe_payload(context, builder, signature.args[0
            ], args[0])
        return impl_ret_borrowed(context, builder, df_typ.
            runtime_colname_typ, rgj__mnu.columns)
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
    ltwil__lhcoc = self.typemap[data_tup.name]
    if any(is_tuple_like_type(qqffn__hqxhy) for qqffn__hqxhy in
        ltwil__lhcoc.types):
        return None
    if equiv_set.has_shape(data_tup):
        irmi__keecv = equiv_set.get_shape(data_tup)
        if len(irmi__keecv) > 1:
            equiv_set.insert_equiv(*irmi__keecv)
        if len(irmi__keecv) > 0:
            tlq__syuu = self.typemap[index.name]
            if not isinstance(tlq__syuu, HeterogeneousIndexType
                ) and equiv_set.has_shape(index):
                equiv_set.insert_equiv(irmi__keecv[0], index)
            return ArrayAnalysis.AnalyzeResult(shape=(irmi__keecv[0], len(
                irmi__keecv)), pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_dataframe_ext_init_dataframe
    ) = init_dataframe_equiv


def get_dataframe_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    cwcbk__slz = args[0]
    data_types = self.typemap[cwcbk__slz.name].data
    if any(is_tuple_like_type(qqffn__hqxhy) for qqffn__hqxhy in data_types):
        return None
    if equiv_set.has_shape(cwcbk__slz):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            cwcbk__slz)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_data
    ) = get_dataframe_data_equiv


def get_dataframe_index_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 1 and not kws
    cwcbk__slz = args[0]
    tlq__syuu = self.typemap[cwcbk__slz.name].index
    if isinstance(tlq__syuu, HeterogeneousIndexType):
        return None
    if equiv_set.has_shape(cwcbk__slz):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            cwcbk__slz)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_index
    ) = get_dataframe_index_equiv


def get_dataframe_table_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    cwcbk__slz = args[0]
    if equiv_set.has_shape(cwcbk__slz):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            cwcbk__slz), pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_table
    ) = get_dataframe_table_equiv


def get_dataframe_column_names_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    cwcbk__slz = args[0]
    if equiv_set.has_shape(cwcbk__slz):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            cwcbk__slz)[1], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_column_names
    ) = get_dataframe_column_names_equiv


@intrinsic
def set_dataframe_data(typingctx, df_typ, c_ind_typ, arr_typ=None):
    check_runtime_cols_unsupported(df_typ, 'set_dataframe_data')
    assert is_overload_constant_int(c_ind_typ)
    fdtl__pvp = get_overload_const_int(c_ind_typ)
    if df_typ.data[fdtl__pvp] != arr_typ:
        raise BodoError(
            'Changing dataframe column data type inplace is not supported in conditionals/loops or for dataframe arguments'
            )

    def codegen(context, builder, signature, args):
        sqka__jqps, borqk__qnj, ticco__ttoao = args
        rgj__mnu = get_dataframe_payload(context, builder, df_typ, sqka__jqps)
        if df_typ.is_table_format:
            pulo__mpab = cgutils.create_struct_proxy(df_typ.table_type)(context
                , builder, builder.extract_value(rgj__mnu.data, 0))
            olwb__bxff = df_typ.table_type.type_to_blk[arr_typ]
            fcg__kng = getattr(pulo__mpab, f'block_{olwb__bxff}')
            wnx__hefkq = ListInstance(context, builder, types.List(arr_typ),
                fcg__kng)
            kulcu__xvr = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[fdtl__pvp])
            wnx__hefkq.setitem(kulcu__xvr, ticco__ttoao, True)
        else:
            ngk__eksit = builder.extract_value(rgj__mnu.data, fdtl__pvp)
            context.nrt.decref(builder, df_typ.data[fdtl__pvp], ngk__eksit)
            rgj__mnu.data = builder.insert_value(rgj__mnu.data,
                ticco__ttoao, fdtl__pvp)
            context.nrt.incref(builder, arr_typ, ticco__ttoao)
        lymhv__nki = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=sqka__jqps)
        payload_type = DataFramePayloadType(df_typ)
        zcc__cmb = context.nrt.meminfo_data(builder, lymhv__nki.meminfo)
        ajpqq__bmyhp = context.get_value_type(payload_type).as_pointer()
        zcc__cmb = builder.bitcast(zcc__cmb, ajpqq__bmyhp)
        builder.store(rgj__mnu._getvalue(), zcc__cmb)
        return impl_ret_borrowed(context, builder, df_typ, sqka__jqps)
    sig = signature(df_typ, df_typ, c_ind_typ, arr_typ)
    return sig, codegen


@intrinsic
def set_df_index(typingctx, df_t, index_t=None):
    check_runtime_cols_unsupported(df_t, 'set_df_index')

    def codegen(context, builder, signature, args):
        uezbl__mhf = args[0]
        index_val = args[1]
        df_typ = signature.args[0]
        aqpwf__wum = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=uezbl__mhf)
        ktoo__xwcfn = get_dataframe_payload(context, builder, df_typ,
            uezbl__mhf)
        lymhv__nki = construct_dataframe(context, builder, signature.
            return_type, ktoo__xwcfn.data, index_val, aqpwf__wum.parent, None)
        context.nrt.incref(builder, index_t, index_val)
        context.nrt.incref(builder, types.Tuple(df_t.data), ktoo__xwcfn.data)
        return lymhv__nki
    rck__lji = DataFrameType(df_t.data, index_t, df_t.columns, df_t.dist,
        df_t.is_table_format)
    sig = signature(rck__lji, df_t, index_t)
    return sig, codegen


@intrinsic
def set_df_column_with_reflect(typingctx, df_type, cname_type, arr_type=None):
    check_runtime_cols_unsupported(df_type, 'set_df_column_with_reflect')
    assert is_literal_type(cname_type), 'constant column name expected'
    col_name = get_literal_value(cname_type)
    yueqz__wph = len(df_type.columns)
    lrzl__gigh = yueqz__wph
    pbjdn__guroy = df_type.data
    column_names = df_type.columns
    index_typ = df_type.index
    fzy__kauf = col_name not in df_type.columns
    fdtl__pvp = yueqz__wph
    if fzy__kauf:
        pbjdn__guroy += arr_type,
        column_names += col_name,
        lrzl__gigh += 1
    else:
        fdtl__pvp = df_type.columns.index(col_name)
        pbjdn__guroy = tuple(arr_type if i == fdtl__pvp else pbjdn__guroy[i
            ] for i in range(yueqz__wph))

    def codegen(context, builder, signature, args):
        sqka__jqps, borqk__qnj, ticco__ttoao = args
        in_dataframe_payload = get_dataframe_payload(context, builder,
            df_type, sqka__jqps)
        ntjzp__hzkqy = cgutils.create_struct_proxy(df_type)(context,
            builder, value=sqka__jqps)
        if df_type.is_table_format:
            hvpj__ntxzk = df_type.table_type
            qpd__vhjlh = builder.extract_value(in_dataframe_payload.data, 0)
            zbvuw__ixhik = TableType(pbjdn__guroy)
            jjv__pzumd = set_table_data_codegen(context, builder,
                hvpj__ntxzk, qpd__vhjlh, zbvuw__ixhik, arr_type,
                ticco__ttoao, fdtl__pvp, fzy__kauf)
            data_tup = context.make_tuple(builder, types.Tuple([
                zbvuw__ixhik]), [jjv__pzumd])
        else:
            vitov__gyfim = [(builder.extract_value(in_dataframe_payload.
                data, i) if i != fdtl__pvp else ticco__ttoao) for i in
                range(yueqz__wph)]
            if fzy__kauf:
                vitov__gyfim.append(ticco__ttoao)
            for cwcbk__slz, txtt__ysduq in zip(vitov__gyfim, pbjdn__guroy):
                context.nrt.incref(builder, txtt__ysduq, cwcbk__slz)
            data_tup = context.make_tuple(builder, types.Tuple(pbjdn__guroy
                ), vitov__gyfim)
        index_val = in_dataframe_payload.index
        context.nrt.incref(builder, index_typ, index_val)
        jkhvz__yqs = construct_dataframe(context, builder, signature.
            return_type, data_tup, index_val, ntjzp__hzkqy.parent, None)
        if not fzy__kauf and arr_type == df_type.data[fdtl__pvp]:
            decref_df_data(context, builder, in_dataframe_payload, df_type)
            payload_type = DataFramePayloadType(df_type)
            zcc__cmb = context.nrt.meminfo_data(builder, ntjzp__hzkqy.meminfo)
            ajpqq__bmyhp = context.get_value_type(payload_type).as_pointer()
            zcc__cmb = builder.bitcast(zcc__cmb, ajpqq__bmyhp)
            kydt__ehy = get_dataframe_payload(context, builder, df_type,
                jkhvz__yqs)
            builder.store(kydt__ehy._getvalue(), zcc__cmb)
            context.nrt.incref(builder, index_typ, index_val)
            if df_type.is_table_format:
                context.nrt.incref(builder, zbvuw__ixhik, builder.
                    extract_value(data_tup, 0))
            else:
                for cwcbk__slz, txtt__ysduq in zip(vitov__gyfim, pbjdn__guroy):
                    context.nrt.incref(builder, txtt__ysduq, cwcbk__slz)
        has_parent = cgutils.is_not_null(builder, ntjzp__hzkqy.parent)
        with builder.if_then(has_parent):
            mttv__rcl = context.get_python_api(builder)
            upsvb__nbmu = mttv__rcl.gil_ensure()
            yayhi__kjkzm = context.get_env_manager(builder)
            context.nrt.incref(builder, arr_type, ticco__ttoao)
            hkgsg__nlrn = numba.core.pythonapi._BoxContext(context, builder,
                mttv__rcl, yayhi__kjkzm)
            cdcco__lsg = hkgsg__nlrn.pyapi.from_native_value(arr_type,
                ticco__ttoao, hkgsg__nlrn.env_manager)
            if isinstance(col_name, str):
                wci__puf = context.insert_const_string(builder.module, col_name
                    )
                fjp__lyt = mttv__rcl.string_from_string(wci__puf)
            else:
                assert isinstance(col_name, int)
                fjp__lyt = mttv__rcl.long_from_longlong(context.
                    get_constant(types.intp, col_name))
            mttv__rcl.object_setitem(ntjzp__hzkqy.parent, fjp__lyt, cdcco__lsg)
            mttv__rcl.decref(cdcco__lsg)
            mttv__rcl.decref(fjp__lyt)
            mttv__rcl.gil_release(upsvb__nbmu)
        return jkhvz__yqs
    rck__lji = DataFrameType(pbjdn__guroy, index_typ, column_names, df_type
        .dist, df_type.is_table_format)
    sig = signature(rck__lji, df_type, cname_type, arr_type)
    return sig, codegen


@lower_constant(DataFrameType)
def lower_constant_dataframe(context, builder, df_type, pyval):
    check_runtime_cols_unsupported(df_type, 'lowering a constant DataFrame')
    yueqz__wph = len(pyval.columns)
    vitov__gyfim = []
    for i in range(yueqz__wph):
        tpv__gpuw = pyval.iloc[:, i]
        if isinstance(df_type.data[i], bodo.DatetimeArrayType):
            cdcco__lsg = tpv__gpuw.array
        else:
            cdcco__lsg = tpv__gpuw.values
        vitov__gyfim.append(cdcco__lsg)
    vitov__gyfim = tuple(vitov__gyfim)
    if df_type.is_table_format:
        pulo__mpab = context.get_constant_generic(builder, df_type.
            table_type, Table(vitov__gyfim))
        data_tup = lir.Constant.literal_struct([pulo__mpab])
    else:
        data_tup = lir.Constant.literal_struct([context.
            get_constant_generic(builder, df_type.data[i], brgla__hitt) for
            i, brgla__hitt in enumerate(vitov__gyfim)])
    index_val = context.get_constant_generic(builder, df_type.index, pyval.
        index)
    twkd__itqy = context.get_constant_null(types.pyobject)
    payload = lir.Constant.literal_struct([data_tup, index_val, twkd__itqy])
    payload = cgutils.global_constant(builder, '.const.payload', payload
        ).bitcast(cgutils.voidptr_t)
    nzqiv__hbge = context.get_constant(types.int64, -1)
    opq__iqkun = context.get_constant_null(types.voidptr)
    rqmsd__wvpqv = lir.Constant.literal_struct([nzqiv__hbge, opq__iqkun,
        opq__iqkun, payload, nzqiv__hbge])
    rqmsd__wvpqv = cgutils.global_constant(builder, '.const.meminfo',
        rqmsd__wvpqv).bitcast(cgutils.voidptr_t)
    return lir.Constant.literal_struct([rqmsd__wvpqv, twkd__itqy])


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
        xytv__llxe = context.cast(builder, in_dataframe_payload.index,
            fromty.index, toty.index)
    else:
        xytv__llxe = in_dataframe_payload.index
        context.nrt.incref(builder, fromty.index, xytv__llxe)
    if (fromty.is_table_format == toty.is_table_format and fromty.data ==
        toty.data):
        mdk__lzwvn = in_dataframe_payload.data
        if fromty.is_table_format:
            context.nrt.incref(builder, types.Tuple([fromty.table_type]),
                mdk__lzwvn)
        else:
            context.nrt.incref(builder, types.BaseTuple.from_types(fromty.
                data), mdk__lzwvn)
    elif not fromty.is_table_format and toty.is_table_format:
        mdk__lzwvn = _cast_df_data_to_table_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    elif fromty.is_table_format and not toty.is_table_format:
        mdk__lzwvn = _cast_df_data_to_tuple_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    elif fromty.is_table_format and toty.is_table_format:
        mdk__lzwvn = _cast_df_data_keep_table_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    else:
        mdk__lzwvn = _cast_df_data_keep_tuple_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    return construct_dataframe(context, builder, toty, mdk__lzwvn,
        xytv__llxe, in_dataframe_payload.parent, None)


def _cast_empty_df(context, builder, toty):
    yvf__tdd = {}
    if isinstance(toty.index, RangeIndexType):
        index = 'bodo.hiframes.pd_index_ext.init_range_index(0, 0, 1, None)'
    else:
        hmtla__ncu = get_index_data_arr_types(toty.index)[0]
        hljfc__zxx = bodo.utils.transform.get_type_alloc_counts(hmtla__ncu) - 1
        dbr__nkbk = ', '.join('0' for borqk__qnj in range(hljfc__zxx))
        index = (
            'bodo.utils.conversion.index_from_array(bodo.utils.utils.alloc_type(0, index_arr_type, ({}{})))'
            .format(dbr__nkbk, ', ' if hljfc__zxx == 1 else ''))
        yvf__tdd['index_arr_type'] = hmtla__ncu
    ojfvj__ixg = []
    for i, arr_typ in enumerate(toty.data):
        hljfc__zxx = bodo.utils.transform.get_type_alloc_counts(arr_typ) - 1
        dbr__nkbk = ', '.join('0' for borqk__qnj in range(hljfc__zxx))
        ymyt__yjo = ('bodo.utils.utils.alloc_type(0, arr_type{}, ({}{}))'.
            format(i, dbr__nkbk, ', ' if hljfc__zxx == 1 else ''))
        ojfvj__ixg.append(ymyt__yjo)
        yvf__tdd[f'arr_type{i}'] = arr_typ
    ojfvj__ixg = ', '.join(ojfvj__ixg)
    ezw__epg = 'def impl():\n'
    gyhjs__oqjr = bodo.hiframes.dataframe_impl._gen_init_df(ezw__epg, toty.
        columns, ojfvj__ixg, index, yvf__tdd)
    df = context.compile_internal(builder, gyhjs__oqjr, toty(), [])
    return df


def _cast_df_data_to_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame to table format')
    yeyz__oftq = toty.table_type
    pulo__mpab = cgutils.create_struct_proxy(yeyz__oftq)(context, builder)
    pulo__mpab.parent = in_dataframe_payload.parent
    for qqffn__hqxhy, olwb__bxff in yeyz__oftq.type_to_blk.items():
        ruokf__veusc = context.get_constant(types.int64, len(yeyz__oftq.
            block_to_arr_ind[olwb__bxff]))
        borqk__qnj, aoyw__kbx = ListInstance.allocate_ex(context, builder,
            types.List(qqffn__hqxhy), ruokf__veusc)
        aoyw__kbx.size = ruokf__veusc
        setattr(pulo__mpab, f'block_{olwb__bxff}', aoyw__kbx.value)
    for i, qqffn__hqxhy in enumerate(fromty.data):
        ggzlm__uoq = toty.data[i]
        if qqffn__hqxhy != ggzlm__uoq:
            zoe__vok = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*zoe__vok)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        ngk__eksit = builder.extract_value(in_dataframe_payload.data, i)
        if qqffn__hqxhy != ggzlm__uoq:
            puuv__wrnl = context.cast(builder, ngk__eksit, qqffn__hqxhy,
                ggzlm__uoq)
            qes__lfhuj = False
        else:
            puuv__wrnl = ngk__eksit
            qes__lfhuj = True
        olwb__bxff = yeyz__oftq.type_to_blk[qqffn__hqxhy]
        fcg__kng = getattr(pulo__mpab, f'block_{olwb__bxff}')
        wnx__hefkq = ListInstance(context, builder, types.List(qqffn__hqxhy
            ), fcg__kng)
        kulcu__xvr = context.get_constant(types.int64, yeyz__oftq.
            block_offsets[i])
        wnx__hefkq.setitem(kulcu__xvr, puuv__wrnl, qes__lfhuj)
    data_tup = context.make_tuple(builder, types.Tuple([yeyz__oftq]), [
        pulo__mpab._getvalue()])
    return data_tup


def _cast_df_data_keep_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame columns')
    vitov__gyfim = []
    for i in range(len(fromty.data)):
        if fromty.data[i] != toty.data[i]:
            zoe__vok = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*zoe__vok)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
            ngk__eksit = builder.extract_value(in_dataframe_payload.data, i)
            puuv__wrnl = context.cast(builder, ngk__eksit, fromty.data[i],
                toty.data[i])
            qes__lfhuj = False
        else:
            puuv__wrnl = builder.extract_value(in_dataframe_payload.data, i)
            qes__lfhuj = True
        if qes__lfhuj:
            context.nrt.incref(builder, toty.data[i], puuv__wrnl)
        vitov__gyfim.append(puuv__wrnl)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), vitov__gyfim
        )
    return data_tup


def _cast_df_data_keep_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting table format DataFrame columns')
    hvpj__ntxzk = fromty.table_type
    qpd__vhjlh = cgutils.create_struct_proxy(hvpj__ntxzk)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    zbvuw__ixhik = toty.table_type
    jjv__pzumd = cgutils.create_struct_proxy(zbvuw__ixhik)(context, builder)
    jjv__pzumd.parent = in_dataframe_payload.parent
    for qqffn__hqxhy, olwb__bxff in zbvuw__ixhik.type_to_blk.items():
        ruokf__veusc = context.get_constant(types.int64, len(zbvuw__ixhik.
            block_to_arr_ind[olwb__bxff]))
        borqk__qnj, aoyw__kbx = ListInstance.allocate_ex(context, builder,
            types.List(qqffn__hqxhy), ruokf__veusc)
        aoyw__kbx.size = ruokf__veusc
        setattr(jjv__pzumd, f'block_{olwb__bxff}', aoyw__kbx.value)
    for i in range(len(fromty.data)):
        ilh__zwgqb = fromty.data[i]
        ggzlm__uoq = toty.data[i]
        if ilh__zwgqb != ggzlm__uoq:
            zoe__vok = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*zoe__vok)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        cdhnu__zjx = hvpj__ntxzk.type_to_blk[ilh__zwgqb]
        rhbo__tlk = getattr(qpd__vhjlh, f'block_{cdhnu__zjx}')
        mvg__ayzay = ListInstance(context, builder, types.List(ilh__zwgqb),
            rhbo__tlk)
        amee__tcgq = context.get_constant(types.int64, hvpj__ntxzk.
            block_offsets[i])
        ngk__eksit = mvg__ayzay.getitem(amee__tcgq)
        if ilh__zwgqb != ggzlm__uoq:
            puuv__wrnl = context.cast(builder, ngk__eksit, ilh__zwgqb,
                ggzlm__uoq)
            qes__lfhuj = False
        else:
            puuv__wrnl = ngk__eksit
            qes__lfhuj = True
        ysg__dkb = zbvuw__ixhik.type_to_blk[qqffn__hqxhy]
        aoyw__kbx = getattr(jjv__pzumd, f'block_{ysg__dkb}')
        dnooe__kvikg = ListInstance(context, builder, types.List(ggzlm__uoq
            ), aoyw__kbx)
        zqos__cqzoz = context.get_constant(types.int64, zbvuw__ixhik.
            block_offsets[i])
        dnooe__kvikg.setitem(zqos__cqzoz, puuv__wrnl, qes__lfhuj)
    data_tup = context.make_tuple(builder, types.Tuple([zbvuw__ixhik]), [
        jjv__pzumd._getvalue()])
    return data_tup


def _cast_df_data_to_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(fromty,
        'casting table format to traditional DataFrame')
    yeyz__oftq = fromty.table_type
    pulo__mpab = cgutils.create_struct_proxy(yeyz__oftq)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    vitov__gyfim = []
    for i, qqffn__hqxhy in enumerate(toty.data):
        ilh__zwgqb = fromty.data[i]
        if qqffn__hqxhy != ilh__zwgqb:
            zoe__vok = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*zoe__vok)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        olwb__bxff = yeyz__oftq.type_to_blk[qqffn__hqxhy]
        fcg__kng = getattr(pulo__mpab, f'block_{olwb__bxff}')
        wnx__hefkq = ListInstance(context, builder, types.List(qqffn__hqxhy
            ), fcg__kng)
        kulcu__xvr = context.get_constant(types.int64, yeyz__oftq.
            block_offsets[i])
        ngk__eksit = wnx__hefkq.getitem(kulcu__xvr)
        if qqffn__hqxhy != ilh__zwgqb:
            puuv__wrnl = context.cast(builder, ngk__eksit, ilh__zwgqb,
                qqffn__hqxhy)
            qes__lfhuj = False
        else:
            puuv__wrnl = ngk__eksit
            qes__lfhuj = True
        if qes__lfhuj:
            context.nrt.incref(builder, qqffn__hqxhy, puuv__wrnl)
        vitov__gyfim.append(puuv__wrnl)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), vitov__gyfim
        )
    return data_tup


@overload(pd.DataFrame, inline='always', no_unliteral=True)
def pd_dataframe_overload(data=None, index=None, columns=None, dtype=None,
    copy=False):
    if not is_overload_constant_bool(copy):
        raise BodoError(
            "pd.DataFrame(): 'copy' argument should be a constant boolean")
    copy = get_overload_const(copy)
    svl__rmztc, ojfvj__ixg, index_arg = _get_df_args(data, index, columns,
        dtype, copy)
    fjyoh__mjfmy = gen_const_tup(svl__rmztc)
    ezw__epg = (
        'def _init_df(data=None, index=None, columns=None, dtype=None, copy=False):\n'
        )
    ezw__epg += (
        '  return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, {}, {})\n'
        .format(ojfvj__ixg, index_arg, fjyoh__mjfmy))
    vfg__zksc = {}
    exec(ezw__epg, {'bodo': bodo, 'np': np}, vfg__zksc)
    ipey__akc = vfg__zksc['_init_df']
    return ipey__akc


@intrinsic
def _tuple_to_table_format_decoded(typingctx, df_typ):
    assert not df_typ.is_table_format, '_tuple_to_table_format requires a tuple format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    rck__lji = DataFrameType(to_str_arr_if_dict_array(df_typ.data), df_typ.
        index, df_typ.columns, dist=df_typ.dist, is_table_format=True)
    sig = signature(rck__lji, df_typ)
    return sig, codegen


@intrinsic
def _table_to_tuple_format_decoded(typingctx, df_typ):
    assert df_typ.is_table_format, '_tuple_to_table_format requires a table format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    rck__lji = DataFrameType(to_str_arr_if_dict_array(df_typ.data), df_typ.
        index, df_typ.columns, dist=df_typ.dist, is_table_format=False)
    sig = signature(rck__lji, df_typ)
    return sig, codegen


def _get_df_args(data, index, columns, dtype, copy):
    imm__spngl = ''
    if not is_overload_none(dtype):
        imm__spngl = '.astype(dtype)'
    index_is_none = is_overload_none(index)
    index_arg = 'bodo.utils.conversion.convert_to_index(index)'
    if isinstance(data, types.BaseTuple):
        if not data.types[0] == types.StringLiteral('__bodo_tup'):
            raise BodoError('pd.DataFrame tuple input data not supported yet')
        assert len(data.types) % 2 == 1, 'invalid const dict tuple structure'
        yueqz__wph = (len(data.types) - 1) // 2
        ihzs__mpmru = [qqffn__hqxhy.literal_value for qqffn__hqxhy in data.
            types[1:yueqz__wph + 1]]
        data_val_types = dict(zip(ihzs__mpmru, data.types[yueqz__wph + 1:]))
        vitov__gyfim = ['data[{}]'.format(i) for i in range(yueqz__wph + 1,
            2 * yueqz__wph + 1)]
        data_dict = dict(zip(ihzs__mpmru, vitov__gyfim))
        if is_overload_none(index):
            for i, qqffn__hqxhy in enumerate(data.types[yueqz__wph + 1:]):
                if isinstance(qqffn__hqxhy, SeriesType):
                    index_arg = (
                        'bodo.hiframes.pd_series_ext.get_series_index(data[{}])'
                        .format(yueqz__wph + 1 + i))
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
        eegre__amiv = '.copy()' if copy else ''
        qeqx__hlsb = get_overload_const_list(columns)
        yueqz__wph = len(qeqx__hlsb)
        data_val_types = {hkgsg__nlrn: data.copy(ndim=1) for hkgsg__nlrn in
            qeqx__hlsb}
        vitov__gyfim = ['data[:,{}]{}'.format(i, eegre__amiv) for i in
            range(yueqz__wph)]
        data_dict = dict(zip(qeqx__hlsb, vitov__gyfim))
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
    ojfvj__ixg = '({},)'.format(', '.join(
        'bodo.utils.conversion.coerce_to_array({}, True, scalar_to_arr_len={}){}'
        .format(data_dict[hkgsg__nlrn], df_len, imm__spngl) for hkgsg__nlrn in
        col_names))
    if len(col_names) == 0:
        ojfvj__ixg = '()'
    return col_names, ojfvj__ixg, index_arg


def _get_df_len_from_info(data_dict, data_val_types, col_names,
    index_is_none, index_arg):
    df_len = '0'
    for hkgsg__nlrn in col_names:
        if hkgsg__nlrn in data_dict and is_iterable_type(data_val_types[
            hkgsg__nlrn]):
            df_len = 'len({})'.format(data_dict[hkgsg__nlrn])
            break
    if df_len == '0' and not index_is_none:
        df_len = f'len({index_arg})'
    return df_len


def _fill_null_arrays(data_dict, col_names, df_len, dtype):
    if all(hkgsg__nlrn in data_dict for hkgsg__nlrn in col_names):
        return
    if is_overload_none(dtype):
        dtype = 'bodo.string_array_type'
    else:
        dtype = 'bodo.utils.conversion.array_type_from_dtype(dtype)'
    irs__bikf = 'bodo.libs.array_kernels.gen_na_array({}, {})'.format(df_len,
        dtype)
    for hkgsg__nlrn in col_names:
        if hkgsg__nlrn not in data_dict:
            data_dict[hkgsg__nlrn] = irs__bikf


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
            qqffn__hqxhy = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(
                df)
            return len(qqffn__hqxhy)
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
        aesn__xvel = idx.literal_value
        if isinstance(aesn__xvel, int):
            msb__pnu = tup.types[aesn__xvel]
        elif isinstance(aesn__xvel, slice):
            msb__pnu = types.BaseTuple.from_types(tup.types[aesn__xvel])
        return signature(msb__pnu, *args)


GetItemTuple.prefer_literal = True


@lower_builtin(operator.getitem, types.BaseTuple, types.IntegerLiteral)
@lower_builtin(operator.getitem, types.BaseTuple, types.SliceLiteral)
def getitem_tuple_lower(context, builder, sig, args):
    etltc__rmvku, idx = sig.args
    idx = idx.literal_value
    tup, borqk__qnj = args
    if isinstance(idx, int):
        if idx < 0:
            idx += len(etltc__rmvku)
        if not 0 <= idx < len(etltc__rmvku):
            raise IndexError('cannot index at %d in %s' % (idx, etltc__rmvku))
        jjwd__sbav = builder.extract_value(tup, idx)
    elif isinstance(idx, slice):
        zfz__cjb = cgutils.unpack_tuple(builder, tup)[idx]
        jjwd__sbav = context.make_tuple(builder, sig.return_type, zfz__cjb)
    else:
        raise NotImplementedError('unexpected index %r for %s' % (idx, sig.
            args[0]))
    return impl_ret_borrowed(context, builder, sig.return_type, jjwd__sbav)


def join_dummy(left_df, right_df, left_on, right_on, how, suffix_x,
    suffix_y, is_join, indicator, _bodo_na_equal, gen_cond):
    return left_df


@infer_global(join_dummy)
class JoinTyper(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        from bodo.utils.typing import is_overload_str
        assert not kws
        (left_df, right_df, left_on, right_on, rmam__mxuf, suffix_x,
            suffix_y, is_join, indicator, _bodo_na_equal, ihdq__apod) = args
        left_on = get_overload_const_list(left_on)
        right_on = get_overload_const_list(right_on)
        ons__sgtdy = set(left_on) & set(right_on)
        wrx__nxuq = set(left_df.columns) & set(right_df.columns)
        rzxyo__prhi = wrx__nxuq - ons__sgtdy
        sjjd__toljz = '$_bodo_index_' in left_on
        vzcfg__cuvt = '$_bodo_index_' in right_on
        how = get_overload_const_str(rmam__mxuf)
        beeg__rrvhg = how in {'left', 'outer'}
        mzfn__bxr = how in {'right', 'outer'}
        columns = []
        data = []
        if sjjd__toljz:
            nsj__couk = bodo.utils.typing.get_index_data_arr_types(left_df.
                index)[0]
        else:
            nsj__couk = left_df.data[left_df.columns.index(left_on[0])]
        if vzcfg__cuvt:
            rmhx__wlli = bodo.utils.typing.get_index_data_arr_types(right_df
                .index)[0]
        else:
            rmhx__wlli = right_df.data[right_df.columns.index(right_on[0])]
        if sjjd__toljz and not vzcfg__cuvt and not is_join.literal_value:
            smkrz__dlpoh = right_on[0]
            if smkrz__dlpoh in left_df.columns:
                columns.append(smkrz__dlpoh)
                if (rmhx__wlli == bodo.dict_str_arr_type and nsj__couk ==
                    bodo.string_array_type):
                    xyuuk__llj = bodo.string_array_type
                else:
                    xyuuk__llj = rmhx__wlli
                data.append(xyuuk__llj)
        if vzcfg__cuvt and not sjjd__toljz and not is_join.literal_value:
            ifzi__fxh = left_on[0]
            if ifzi__fxh in right_df.columns:
                columns.append(ifzi__fxh)
                if (nsj__couk == bodo.dict_str_arr_type and rmhx__wlli ==
                    bodo.string_array_type):
                    xyuuk__llj = bodo.string_array_type
                else:
                    xyuuk__llj = nsj__couk
                data.append(xyuuk__llj)
        for ilh__zwgqb, tpv__gpuw in zip(left_df.data, left_df.columns):
            columns.append(str(tpv__gpuw) + suffix_x.literal_value if 
                tpv__gpuw in rzxyo__prhi else tpv__gpuw)
            if tpv__gpuw in ons__sgtdy:
                if ilh__zwgqb == bodo.dict_str_arr_type:
                    ilh__zwgqb = right_df.data[right_df.columns.index(
                        tpv__gpuw)]
                data.append(ilh__zwgqb)
            else:
                if (ilh__zwgqb == bodo.dict_str_arr_type and tpv__gpuw in
                    left_on):
                    if vzcfg__cuvt:
                        ilh__zwgqb = rmhx__wlli
                    else:
                        zfbx__pvcmh = left_on.index(tpv__gpuw)
                        ghezy__ugpl = right_on[zfbx__pvcmh]
                        ilh__zwgqb = right_df.data[right_df.columns.index(
                            ghezy__ugpl)]
                if mzfn__bxr:
                    ilh__zwgqb = to_nullable_type(ilh__zwgqb)
                data.append(ilh__zwgqb)
        for ilh__zwgqb, tpv__gpuw in zip(right_df.data, right_df.columns):
            if tpv__gpuw not in ons__sgtdy:
                columns.append(str(tpv__gpuw) + suffix_y.literal_value if 
                    tpv__gpuw in rzxyo__prhi else tpv__gpuw)
                if (ilh__zwgqb == bodo.dict_str_arr_type and tpv__gpuw in
                    right_on):
                    if sjjd__toljz:
                        ilh__zwgqb = nsj__couk
                    else:
                        zfbx__pvcmh = right_on.index(tpv__gpuw)
                        otgxa__teei = left_on[zfbx__pvcmh]
                        ilh__zwgqb = left_df.data[left_df.columns.index(
                            otgxa__teei)]
                if beeg__rrvhg:
                    ilh__zwgqb = to_nullable_type(ilh__zwgqb)
                data.append(ilh__zwgqb)
        crhdo__bpd = get_overload_const_bool(indicator)
        if crhdo__bpd:
            columns.append('_merge')
            data.append(bodo.CategoricalArrayType(bodo.PDCategoricalDtype((
                'left_only', 'right_only', 'both'), bodo.string_type, False)))
        index_typ = RangeIndexType(types.none)
        if sjjd__toljz and vzcfg__cuvt and not is_overload_str(how, 'asof'):
            index_typ = left_df.index
            if isinstance(index_typ, bodo.hiframes.pd_index_ext.RangeIndexType
                ):
                index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types
                    .int64)
        elif sjjd__toljz and not vzcfg__cuvt:
            index_typ = right_df.index
            if isinstance(index_typ, bodo.hiframes.pd_index_ext.RangeIndexType
                ):
                index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types
                    .int64)
        elif vzcfg__cuvt and not sjjd__toljz:
            index_typ = left_df.index
            if isinstance(index_typ, bodo.hiframes.pd_index_ext.RangeIndexType
                ):
                index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types
                    .int64)
        gfcpy__iamhm = DataFrameType(tuple(data), index_typ, tuple(columns))
        return signature(gfcpy__iamhm, *args)


JoinTyper._no_unliteral = True


@lower_builtin(join_dummy, types.VarArg(types.Any))
def lower_join_dummy(context, builder, sig, args):
    lymhv__nki = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return lymhv__nki._getvalue()


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
    lksk__upz = dict(join=join, join_axes=join_axes, keys=keys, levels=
        levels, names=names, verify_integrity=verify_integrity, sort=sort,
        copy=copy)
    rhks__zbhnq = dict(join='outer', join_axes=None, keys=None, levels=None,
        names=None, verify_integrity=False, sort=None, copy=True)
    check_unsupported_args('pandas.concat', lksk__upz, rhks__zbhnq,
        package_name='pandas', module_name='General')
    ezw__epg = """def impl(objs, axis=0, join='outer', join_axes=None, ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False, sort=None, copy=True):
"""
    if axis == 1:
        if not isinstance(objs, types.BaseTuple):
            raise_bodo_error(
                'Only tuple argument for pd.concat(axis=1) expected')
        index = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len(objs[0]), 1, None)'
            )
        stoog__ygub = 0
        ojfvj__ixg = []
        names = []
        for i, ywvqv__cjm in enumerate(objs.types):
            assert isinstance(ywvqv__cjm, (SeriesType, DataFrameType))
            check_runtime_cols_unsupported(ywvqv__cjm, 'pandas.concat()')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                ywvqv__cjm, 'pandas.concat()')
            if isinstance(ywvqv__cjm, SeriesType):
                names.append(str(stoog__ygub))
                stoog__ygub += 1
                ojfvj__ixg.append(
                    'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'
                    .format(i))
            else:
                names.extend(ywvqv__cjm.columns)
                for jsp__thh in range(len(ywvqv__cjm.data)):
                    ojfvj__ixg.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, jsp__thh))
        return bodo.hiframes.dataframe_impl._gen_init_df(ezw__epg, names,
            ', '.join(ojfvj__ixg), index)
    if axis != 0:
        raise_bodo_error('pd.concat(): axis must be 0 or 1')
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        DataFrameType):
        assert all(isinstance(qqffn__hqxhy, DataFrameType) for qqffn__hqxhy in
            objs.types)
        kemy__ivai = []
        for df in objs.types:
            check_runtime_cols_unsupported(df, 'pandas.concat()')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
                'pandas.concat()')
            kemy__ivai.extend(df.columns)
        kemy__ivai = list(dict.fromkeys(kemy__ivai).keys())
        dcpc__mohzd = {}
        for stoog__ygub, hkgsg__nlrn in enumerate(kemy__ivai):
            for i, df in enumerate(objs.types):
                if hkgsg__nlrn in df.column_index:
                    dcpc__mohzd[f'arr_typ{stoog__ygub}'] = df.data[df.
                        column_index[hkgsg__nlrn]]
                    break
        assert len(dcpc__mohzd) == len(kemy__ivai)
        itsdw__bnfi = []
        for stoog__ygub, hkgsg__nlrn in enumerate(kemy__ivai):
            args = []
            for i, df in enumerate(objs.types):
                if hkgsg__nlrn in df.column_index:
                    fdtl__pvp = df.column_index[hkgsg__nlrn]
                    args.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, fdtl__pvp))
                else:
                    args.append(
                        'bodo.libs.array_kernels.gen_na_array(len(objs[{}]), arr_typ{})'
                        .format(i, stoog__ygub))
            ezw__epg += ('  A{} = bodo.libs.array_kernels.concat(({},))\n'.
                format(stoog__ygub, ', '.join(args)))
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
        return bodo.hiframes.dataframe_impl._gen_init_df(ezw__epg,
            kemy__ivai, ', '.join('A{}'.format(i) for i in range(len(
            kemy__ivai))), index, dcpc__mohzd)
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        SeriesType):
        assert all(isinstance(qqffn__hqxhy, SeriesType) for qqffn__hqxhy in
            objs.types)
        ezw__epg += ('  out_arr = bodo.libs.array_kernels.concat(({},))\n'.
            format(', '.join(
            'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'.format(
            i) for i in range(len(objs.types)))))
        if ignore_index:
            ezw__epg += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            ezw__epg += (
                """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)))))
        ezw__epg += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        vfg__zksc = {}
        exec(ezw__epg, {'bodo': bodo, 'np': np, 'numba': numba}, vfg__zksc)
        return vfg__zksc['impl']
    if isinstance(objs, types.List) and isinstance(objs.dtype, DataFrameType):
        check_runtime_cols_unsupported(objs.dtype, 'pandas.concat()')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(objs.
            dtype, 'pandas.concat()')
        df_type = objs.dtype
        for stoog__ygub, hkgsg__nlrn in enumerate(df_type.columns):
            ezw__epg += '  arrs{} = []\n'.format(stoog__ygub)
            ezw__epg += '  for i in range(len(objs)):\n'
            ezw__epg += '    df = objs[i]\n'
            ezw__epg += (
                """    arrs{0}.append(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0}))
"""
                .format(stoog__ygub))
            ezw__epg += (
                '  out_arr{0} = bodo.libs.array_kernels.concat(arrs{0})\n'.
                format(stoog__ygub))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr0), 1, None)'
                )
        else:
            ezw__epg += '  arrs_index = []\n'
            ezw__epg += '  for i in range(len(objs)):\n'
            ezw__epg += '    df = objs[i]\n'
            ezw__epg += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
            if objs.dtype.index.name_typ == types.none:
                name = None
            else:
                name = objs.dtype.index.name_typ.literal_value
            index = f"""bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index), {name!r})
"""
        return bodo.hiframes.dataframe_impl._gen_init_df(ezw__epg, df_type.
            columns, ', '.join('out_arr{}'.format(i) for i in range(len(
            df_type.columns))), index)
    if isinstance(objs, types.List) and isinstance(objs.dtype, SeriesType):
        ezw__epg += '  arrs = []\n'
        ezw__epg += '  for i in range(len(objs)):\n'
        ezw__epg += (
            '    arrs.append(bodo.hiframes.pd_series_ext.get_series_data(objs[i]))\n'
            )
        ezw__epg += '  out_arr = bodo.libs.array_kernels.concat(arrs)\n'
        if ignore_index:
            ezw__epg += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            ezw__epg += '  arrs_index = []\n'
            ezw__epg += '  for i in range(len(objs)):\n'
            ezw__epg += '    S = objs[i]\n'
            ezw__epg += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(S)))
"""
            ezw__epg += """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index))
"""
        ezw__epg += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        vfg__zksc = {}
        exec(ezw__epg, {'bodo': bodo, 'np': np, 'numba': numba}, vfg__zksc)
        return vfg__zksc['impl']
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
        rck__lji = df.copy(index=index, is_table_format=False)
        return signature(rck__lji, *args)


SortDummyTyper._no_unliteral = True


@lower_builtin(sort_values_dummy, types.VarArg(types.Any))
def lower_sort_values_dummy(context, builder, sig, args):
    if sig.return_type == types.none:
        return
    ysw__ntqi = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return ysw__ntqi._getvalue()


@overload_method(DataFrameType, 'itertuples', inline='always', no_unliteral
    =True)
def itertuples_overload(df, index=True, name='Pandas'):
    check_runtime_cols_unsupported(df, 'DataFrame.itertuples()')
    lksk__upz = dict(index=index, name=name)
    rhks__zbhnq = dict(index=True, name='Pandas')
    check_unsupported_args('DataFrame.itertuples', lksk__upz, rhks__zbhnq,
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
        dcpc__mohzd = (types.Array(types.int64, 1, 'C'),) + df.data
        hiv__aqej = bodo.hiframes.dataframe_impl.DataFrameTupleIterator(columns
            , dcpc__mohzd)
        return signature(hiv__aqej, *args)


@lower_builtin(itertuples_dummy, types.VarArg(types.Any))
def lower_itertuples_dummy(context, builder, sig, args):
    ysw__ntqi = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return ysw__ntqi._getvalue()


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
    ysw__ntqi = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return ysw__ntqi._getvalue()


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
    ysw__ntqi = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return ysw__ntqi._getvalue()


@numba.generated_jit(nopython=True)
def pivot_impl(index_tup, columns_tup, values_tup, pivot_values,
    index_names, columns_name, value_names, check_duplicates=True, parallel
    =False):
    if not is_overload_constant_bool(check_duplicates):
        raise BodoError(
            'pivot_impl(): check_duplicates must be a constant boolean')
    qxlyy__hrhk = get_overload_const_bool(check_duplicates)
    ciro__pbe = not is_overload_none(value_names)
    wpvhc__zaq = isinstance(values_tup, types.UniTuple)
    if wpvhc__zaq:
        kvk__dkdcd = [to_nullable_type(values_tup.dtype)]
    else:
        kvk__dkdcd = [to_nullable_type(txtt__ysduq) for txtt__ysduq in
            values_tup]
    ezw__epg = 'def impl(\n'
    ezw__epg += """    index_tup, columns_tup, values_tup, pivot_values, index_names, columns_name, value_names, check_duplicates=True, parallel=False
"""
    ezw__epg += '):\n'
    ezw__epg += '    if parallel:\n'
    njs__mojqf = ', '.join([f'array_to_info(index_tup[{i}])' for i in range
        (len(index_tup))] + [f'array_to_info(columns_tup[{i}])' for i in
        range(len(columns_tup))] + [f'array_to_info(values_tup[{i}])' for i in
        range(len(values_tup))])
    ezw__epg += f'        info_list = [{njs__mojqf}]\n'
    ezw__epg += '        cpp_table = arr_info_list_to_table(info_list)\n'
    ezw__epg += (
        f'        out_cpp_table = shuffle_table(cpp_table, {len(index_tup)}, parallel, 0)\n'
        )
    titus__ewdya = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i}), index_tup[{i}])'
         for i in range(len(index_tup))])
    wueg__adm = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup)}), columns_tup[{i}])'
         for i in range(len(columns_tup))])
    unvn__guxd = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup) + len(columns_tup)}), values_tup[{i}])'
         for i in range(len(values_tup))])
    ezw__epg += f'        index_tup = ({titus__ewdya},)\n'
    ezw__epg += f'        columns_tup = ({wueg__adm},)\n'
    ezw__epg += f'        values_tup = ({unvn__guxd},)\n'
    ezw__epg += '        delete_table(cpp_table)\n'
    ezw__epg += '        delete_table(out_cpp_table)\n'
    ezw__epg += '    columns_arr = columns_tup[0]\n'
    if wpvhc__zaq:
        ezw__epg += '    values_arrs = [arr for arr in values_tup]\n'
    ezw__epg += """    unique_index_arr_tup, row_vector = bodo.libs.array_ops.array_unique_vector_map(
"""
    ezw__epg += '        index_tup\n'
    ezw__epg += '    )\n'
    ezw__epg += '    n_rows = len(unique_index_arr_tup[0])\n'
    ezw__epg += '    num_values_arrays = len(values_tup)\n'
    ezw__epg += '    n_unique_pivots = len(pivot_values)\n'
    if wpvhc__zaq:
        ezw__epg += '    n_cols = num_values_arrays * n_unique_pivots\n'
    else:
        ezw__epg += '    n_cols = n_unique_pivots\n'
    ezw__epg += '    col_map = {}\n'
    ezw__epg += '    for i in range(n_unique_pivots):\n'
    ezw__epg += '        if bodo.libs.array_kernels.isna(pivot_values, i):\n'
    ezw__epg += '            raise ValueError(\n'
    ezw__epg += """                "DataFrame.pivot(): NA values in 'columns' array not supported\"
"""
    ezw__epg += '            )\n'
    ezw__epg += '        col_map[pivot_values[i]] = i\n'
    nxssr__dzlw = False
    for i, swg__vlep in enumerate(kvk__dkdcd):
        if is_str_arr_type(swg__vlep):
            nxssr__dzlw = True
            ezw__epg += (
                f'    len_arrs_{i} = [np.zeros(n_rows, np.int64) for _ in range(n_cols)]\n'
                )
            ezw__epg += f'    total_lens_{i} = np.zeros(n_cols, np.int64)\n'
    if nxssr__dzlw:
        if qxlyy__hrhk:
            ezw__epg += '    nbytes = (n_rows + 7) >> 3\n'
            ezw__epg += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
        ezw__epg += '    for i in range(len(columns_arr)):\n'
        ezw__epg += '        col_name = columns_arr[i]\n'
        ezw__epg += '        pivot_idx = col_map[col_name]\n'
        ezw__epg += '        row_idx = row_vector[i]\n'
        if qxlyy__hrhk:
            ezw__epg += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
            ezw__epg += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
            ezw__epg += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
            ezw__epg += '        else:\n'
            ezw__epg += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
        if wpvhc__zaq:
            ezw__epg += '        for j in range(num_values_arrays):\n'
            ezw__epg += (
                '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
            ezw__epg += '            len_arr = len_arrs_0[col_idx]\n'
            ezw__epg += '            values_arr = values_arrs[j]\n'
            ezw__epg += (
                '            if not bodo.libs.array_kernels.isna(values_arr, i):\n'
                )
            ezw__epg += (
                '                len_arr[row_idx] = len(values_arr[i])\n')
            ezw__epg += (
                '                total_lens_0[col_idx] += len(values_arr[i])\n'
                )
        else:
            for i, swg__vlep in enumerate(kvk__dkdcd):
                if is_str_arr_type(swg__vlep):
                    ezw__epg += f"""        if not bodo.libs.array_kernels.isna(values_tup[{i}], i):
"""
                    ezw__epg += f"""            len_arrs_{i}[pivot_idx][row_idx] = len(values_tup[{i}][i])
"""
                    ezw__epg += f"""            total_lens_{i}[pivot_idx] += len(values_tup[{i}][i])
"""
    for i, swg__vlep in enumerate(kvk__dkdcd):
        if is_str_arr_type(swg__vlep):
            ezw__epg += f'    data_arrs_{i} = [\n'
            ezw__epg += (
                '        bodo.libs.str_arr_ext.gen_na_str_array_lens(\n')
            ezw__epg += (
                f'            n_rows, total_lens_{i}[i], len_arrs_{i}[i]\n')
            ezw__epg += '        )\n'
            ezw__epg += '        for i in range(n_cols)\n'
            ezw__epg += '    ]\n'
        else:
            ezw__epg += f'    data_arrs_{i} = [\n'
            ezw__epg += (
                f'        bodo.libs.array_kernels.gen_na_array(n_rows, data_arr_typ_{i})\n'
                )
            ezw__epg += '        for _ in range(n_cols)\n'
            ezw__epg += '    ]\n'
    if not nxssr__dzlw and qxlyy__hrhk:
        ezw__epg += '    nbytes = (n_rows + 7) >> 3\n'
        ezw__epg += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
    ezw__epg += '    for i in range(len(columns_arr)):\n'
    ezw__epg += '        col_name = columns_arr[i]\n'
    ezw__epg += '        pivot_idx = col_map[col_name]\n'
    ezw__epg += '        row_idx = row_vector[i]\n'
    if not nxssr__dzlw and qxlyy__hrhk:
        ezw__epg += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
        ezw__epg += (
            '        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):\n'
            )
        ezw__epg += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
        ezw__epg += '        else:\n'
        ezw__epg += (
            '            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)\n'
            )
    if wpvhc__zaq:
        ezw__epg += '        for j in range(num_values_arrays):\n'
        ezw__epg += (
            '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
        ezw__epg += '            col_arr = data_arrs_0[col_idx]\n'
        ezw__epg += '            values_arr = values_arrs[j]\n'
        ezw__epg += (
            '            if bodo.libs.array_kernels.isna(values_arr, i):\n')
        ezw__epg += (
            '                bodo.libs.array_kernels.setna(col_arr, row_idx)\n'
            )
        ezw__epg += '            else:\n'
        ezw__epg += '                col_arr[row_idx] = values_arr[i]\n'
    else:
        for i, swg__vlep in enumerate(kvk__dkdcd):
            ezw__epg += f'        col_arr_{i} = data_arrs_{i}[pivot_idx]\n'
            ezw__epg += (
                f'        if bodo.libs.array_kernels.isna(values_tup[{i}], i):\n'
                )
            ezw__epg += (
                f'            bodo.libs.array_kernels.setna(col_arr_{i}, row_idx)\n'
                )
            ezw__epg += f'        else:\n'
            ezw__epg += (
                f'            col_arr_{i}[row_idx] = values_tup[{i}][i]\n')
    if len(index_tup) == 1:
        ezw__epg += """    index = bodo.utils.conversion.index_from_array(unique_index_arr_tup[0], index_names[0])
"""
    else:
        ezw__epg += """    index = bodo.hiframes.pd_multi_index_ext.init_multi_index(unique_index_arr_tup, index_names, None)
"""
    if ciro__pbe:
        ezw__epg += '    num_rows = len(value_names) * len(pivot_values)\n'
        if is_str_arr_type(value_names):
            ezw__epg += '    total_chars = 0\n'
            ezw__epg += '    for i in range(len(value_names)):\n'
            ezw__epg += '        total_chars += len(value_names[i])\n'
            ezw__epg += """    new_value_names = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(pivot_values))
"""
        else:
            ezw__epg += """    new_value_names = bodo.utils.utils.alloc_type(num_rows, value_names, (-1,))
"""
        if is_str_arr_type(pivot_values):
            ezw__epg += '    total_chars = 0\n'
            ezw__epg += '    for i in range(len(pivot_values)):\n'
            ezw__epg += '        total_chars += len(pivot_values[i])\n'
            ezw__epg += """    new_pivot_values = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(value_names))
"""
        else:
            ezw__epg += """    new_pivot_values = bodo.utils.utils.alloc_type(num_rows, pivot_values, (-1,))
"""
        ezw__epg += '    for i in range(len(value_names)):\n'
        ezw__epg += '        for j in range(len(pivot_values)):\n'
        ezw__epg += (
            '            new_value_names[(i * len(pivot_values)) + j] = value_names[i]\n'
            )
        ezw__epg += (
            '            new_pivot_values[(i * len(pivot_values)) + j] = pivot_values[j]\n'
            )
        ezw__epg += """    column_index = bodo.hiframes.pd_multi_index_ext.init_multi_index((new_value_names, new_pivot_values), (None, columns_name), None)
"""
    else:
        ezw__epg += """    column_index =  bodo.utils.conversion.index_from_array(pivot_values, columns_name)
"""
    qowqj__jmgi = ', '.join(f'data_arrs_{i}' for i in range(len(kvk__dkdcd)))
    ezw__epg += f"""    table = bodo.hiframes.table.init_runtime_table_from_lists(({qowqj__jmgi},), n_rows)
"""
    ezw__epg += (
        '    return bodo.hiframes.pd_dataframe_ext.init_runtime_cols_dataframe(\n'
        )
    ezw__epg += '        (table,), index, column_index\n'
    ezw__epg += '    )\n'
    vfg__zksc = {}
    wkw__kxak = {f'data_arr_typ_{i}': swg__vlep for i, swg__vlep in
        enumerate(kvk__dkdcd)}
    efxz__qcsit = {'bodo': bodo, 'np': np, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'info_from_table': info_from_table, **wkw__kxak}
    exec(ezw__epg, efxz__qcsit, vfg__zksc)
    impl = vfg__zksc['impl']
    return impl


def gen_pandas_parquet_metadata(column_names, data_types, index,
    write_non_range_index_to_metadata, write_rangeindex_to_metadata,
    partition_cols=None, is_runtime_columns=False):
    ruhqz__umt = {}
    ruhqz__umt['columns'] = []
    if partition_cols is None:
        partition_cols = []
    for col_name, rcvqn__ojf in zip(column_names, data_types):
        if col_name in partition_cols:
            continue
        dhy__jhxoj = None
        if isinstance(rcvqn__ojf, bodo.DatetimeArrayType):
            uiw__jtpdb = 'datetimetz'
            svasu__shp = 'datetime64[ns]'
            if isinstance(rcvqn__ojf.tz, int):
                gsu__srff = (bodo.libs.pd_datetime_arr_ext.
                    nanoseconds_to_offset(rcvqn__ojf.tz))
            else:
                gsu__srff = pd.DatetimeTZDtype(tz=rcvqn__ojf.tz).tz
            dhy__jhxoj = {'timezone': pa.lib.tzinfo_to_string(gsu__srff)}
        elif isinstance(rcvqn__ojf, types.Array
            ) or rcvqn__ojf == boolean_array:
            uiw__jtpdb = svasu__shp = rcvqn__ojf.dtype.name
            if svasu__shp.startswith('datetime'):
                uiw__jtpdb = 'datetime'
        elif is_str_arr_type(rcvqn__ojf):
            uiw__jtpdb = 'unicode'
            svasu__shp = 'object'
        elif rcvqn__ojf == binary_array_type:
            uiw__jtpdb = 'bytes'
            svasu__shp = 'object'
        elif isinstance(rcvqn__ojf, DecimalArrayType):
            uiw__jtpdb = svasu__shp = 'object'
        elif isinstance(rcvqn__ojf, IntegerArrayType):
            pjcu__odhj = rcvqn__ojf.dtype.name
            if pjcu__odhj.startswith('int'):
                uiw__jtpdb = 'Int' + pjcu__odhj[3:]
            elif pjcu__odhj.startswith('uint'):
                uiw__jtpdb = 'UInt' + pjcu__odhj[4:]
            else:
                if is_runtime_columns:
                    col_name = 'Runtime determined column of type'
                raise BodoError(
                    'to_parquet(): unknown dtype in nullable Integer column {} {}'
                    .format(col_name, rcvqn__ojf))
            svasu__shp = rcvqn__ojf.dtype.name
        elif rcvqn__ojf == datetime_date_array_type:
            uiw__jtpdb = 'datetime'
            svasu__shp = 'object'
        elif isinstance(rcvqn__ojf, (StructArrayType, ArrayItemArrayType)):
            uiw__jtpdb = 'object'
            svasu__shp = 'object'
        else:
            if is_runtime_columns:
                col_name = 'Runtime determined column of type'
            raise BodoError(
                'to_parquet(): unsupported column type for metadata generation : {} {}'
                .format(col_name, rcvqn__ojf))
        kxsfw__gpf = {'name': col_name, 'field_name': col_name,
            'pandas_type': uiw__jtpdb, 'numpy_type': svasu__shp, 'metadata':
            dhy__jhxoj}
        ruhqz__umt['columns'].append(kxsfw__gpf)
    if write_non_range_index_to_metadata:
        if isinstance(index, MultiIndexType):
            raise BodoError('to_parquet: MultiIndex not supported yet')
        if 'none' in index.name:
            ucylv__ixvj = '__index_level_0__'
            gpw__uvp = None
        else:
            ucylv__ixvj = '%s'
            gpw__uvp = '%s'
        ruhqz__umt['index_columns'] = [ucylv__ixvj]
        ruhqz__umt['columns'].append({'name': gpw__uvp, 'field_name':
            ucylv__ixvj, 'pandas_type': index.pandas_type_name,
            'numpy_type': index.numpy_type_name, 'metadata': None})
    elif write_rangeindex_to_metadata:
        ruhqz__umt['index_columns'] = [{'kind': 'range', 'name': '%s',
            'start': '%d', 'stop': '%d', 'step': '%d'}]
    else:
        ruhqz__umt['index_columns'] = []
    ruhqz__umt['pandas_version'] = pd.__version__
    return ruhqz__umt


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
        zcshy__upy = []
        for bap__zgn in partition_cols:
            try:
                idx = df.columns.index(bap__zgn)
            except ValueError as wafvt__zelyg:
                raise BodoError(
                    f'Partition column {bap__zgn} is not in dataframe')
            zcshy__upy.append(idx)
    else:
        partition_cols = None
    if not is_overload_none(index) and not is_overload_constant_bool(index):
        raise BodoError('to_parquet(): index must be a constant bool or None')
    if not is_overload_int(row_group_size):
        raise BodoError('to_parquet(): row_group_size must be integer')
    from bodo.io.parquet_pio import parquet_write_table_cpp, parquet_write_table_partitioned_cpp
    yrv__lczoi = isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType
        )
    nmasx__tzil = df.index is not None and (is_overload_true(_is_parallel) or
        not is_overload_true(_is_parallel) and not yrv__lczoi)
    write_non_range_index_to_metadata = is_overload_true(index
        ) or is_overload_none(index) and (not yrv__lczoi or
        is_overload_true(_is_parallel))
    write_rangeindex_to_metadata = is_overload_none(index
        ) and yrv__lczoi and not is_overload_true(_is_parallel)
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
        vltpv__jlwfs = df.runtime_data_types
        cynmc__dijo = len(vltpv__jlwfs)
        dhy__jhxoj = gen_pandas_parquet_metadata([''] * cynmc__dijo,
            vltpv__jlwfs, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=True)
        hss__roh = dhy__jhxoj['columns'][:cynmc__dijo]
        dhy__jhxoj['columns'] = dhy__jhxoj['columns'][cynmc__dijo:]
        hss__roh = [json.dumps(xzkr__zbs).replace('""', '{0}') for
            xzkr__zbs in hss__roh]
        wssjx__bkp = json.dumps(dhy__jhxoj)
        tnb__wllzq = '"columns": ['
        mfov__kld = wssjx__bkp.find(tnb__wllzq)
        if mfov__kld == -1:
            raise BodoError(
                'DataFrame.to_parquet(): Unexpected metadata string for runtime columns.  Please return the DataFrame to regular Python to update typing information.'
                )
        otm__ylb = mfov__kld + len(tnb__wllzq)
        zoj__szp = wssjx__bkp[:otm__ylb]
        wssjx__bkp = wssjx__bkp[otm__ylb:]
        hln__ovrf = len(dhy__jhxoj['columns'])
    else:
        wssjx__bkp = json.dumps(gen_pandas_parquet_metadata(df.columns, df.
            data, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=False))
    if not is_overload_true(_is_parallel) and yrv__lczoi:
        wssjx__bkp = wssjx__bkp.replace('"%d"', '%d')
        if df.index.name == 'RangeIndexType(none)':
            wssjx__bkp = wssjx__bkp.replace('"%s"', '%s')
    if not df.is_table_format:
        ojfvj__ixg = ', '.join(
            'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
            .format(i) for i in range(len(df.columns)))
    ezw__epg = """def df_to_parquet(df, path, engine='auto', compression='snappy', index=None, partition_cols=None, storage_options=None, row_group_size=-1, _is_parallel=False):
"""
    if df.is_table_format:
        ezw__epg += '    py_table = get_dataframe_table(df)\n'
        ezw__epg += (
            '    table = py_table_to_cpp_table(py_table, py_table_typ)\n')
    else:
        ezw__epg += '    info_list = [{}]\n'.format(ojfvj__ixg)
        ezw__epg += '    table = arr_info_list_to_table(info_list)\n'
    if df.has_runtime_cols:
        ezw__epg += '    columns_index = get_dataframe_column_names(df)\n'
        ezw__epg += '    names_arr = index_to_array(columns_index)\n'
        ezw__epg += '    col_names = array_to_info(names_arr)\n'
    else:
        ezw__epg += '    col_names = array_to_info(col_names_arr)\n'
    if is_overload_true(index) or is_overload_none(index) and nmasx__tzil:
        ezw__epg += """    index_col = array_to_info(index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
        mtur__aat = True
    else:
        ezw__epg += '    index_col = array_to_info(np.empty(0))\n'
        mtur__aat = False
    if df.has_runtime_cols:
        ezw__epg += '    columns_lst = []\n'
        ezw__epg += '    num_cols = 0\n'
        for i in range(len(df.runtime_data_types)):
            ezw__epg += f'    for _ in range(len(py_table.block_{i})):\n'
            ezw__epg += f"""        columns_lst.append({hss__roh[i]!r}.replace('{{0}}', '"' + names_arr[num_cols] + '"'))
"""
            ezw__epg += '        num_cols += 1\n'
        if hln__ovrf:
            ezw__epg += "    columns_lst.append('')\n"
        ezw__epg += '    columns_str = ", ".join(columns_lst)\n'
        ezw__epg += ('    metadata = """' + zoj__szp +
            '""" + columns_str + """' + wssjx__bkp + '"""\n')
    else:
        ezw__epg += '    metadata = """' + wssjx__bkp + '"""\n'
    ezw__epg += '    if compression is None:\n'
    ezw__epg += "        compression = 'none'\n"
    ezw__epg += '    if df.index.name is not None:\n'
    ezw__epg += '        name_ptr = df.index.name\n'
    ezw__epg += '    else:\n'
    ezw__epg += "        name_ptr = 'null'\n"
    ezw__epg += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(path, parallel=_is_parallel)
"""
    glr__gzaa = None
    if partition_cols:
        glr__gzaa = pd.array([col_name for col_name in df.columns if 
            col_name not in partition_cols])
        rprn__umx = ', '.join(
            f'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype.categories.values)'
             for i in range(len(df.columns)) if isinstance(df.data[i],
            CategoricalArrayType) and i in zcshy__upy)
        if rprn__umx:
            ezw__epg += '    cat_info_list = [{}]\n'.format(rprn__umx)
            ezw__epg += (
                '    cat_table = arr_info_list_to_table(cat_info_list)\n')
        else:
            ezw__epg += '    cat_table = table\n'
        ezw__epg += (
            '    col_names_no_partitions = array_to_info(col_names_no_parts_arr)\n'
            )
        ezw__epg += (
            f'    part_cols_idxs = np.array({zcshy__upy}, dtype=np.int32)\n')
        ezw__epg += (
            '    parquet_write_table_partitioned_cpp(unicode_to_utf8(path),\n')
        ezw__epg += """                            table, col_names, col_names_no_partitions, cat_table,
"""
        ezw__epg += (
            '                            part_cols_idxs.ctypes, len(part_cols_idxs),\n'
            )
        ezw__epg += (
            '                            unicode_to_utf8(compression),\n')
        ezw__epg += '                            _is_parallel,\n'
        ezw__epg += (
            '                            unicode_to_utf8(bucket_region),\n')
        ezw__epg += '                            row_group_size)\n'
        ezw__epg += '    delete_table_decref_arrays(table)\n'
        ezw__epg += '    delete_info_decref_array(index_col)\n'
        ezw__epg += '    delete_info_decref_array(col_names_no_partitions)\n'
        ezw__epg += '    delete_info_decref_array(col_names)\n'
        if rprn__umx:
            ezw__epg += '    delete_table_decref_arrays(cat_table)\n'
    elif write_rangeindex_to_metadata:
        ezw__epg += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        ezw__epg += (
            '                            table, col_names, index_col,\n')
        ezw__epg += '                            ' + str(mtur__aat) + ',\n'
        ezw__epg += '                            unicode_to_utf8(metadata),\n'
        ezw__epg += (
            '                            unicode_to_utf8(compression),\n')
        ezw__epg += (
            '                            _is_parallel, 1, df.index.start,\n')
        ezw__epg += (
            '                            df.index.stop, df.index.step,\n')
        ezw__epg += '                            unicode_to_utf8(name_ptr),\n'
        ezw__epg += (
            '                            unicode_to_utf8(bucket_region),\n')
        ezw__epg += '                            row_group_size)\n'
        ezw__epg += '    delete_table_decref_arrays(table)\n'
        ezw__epg += '    delete_info_decref_array(index_col)\n'
        ezw__epg += '    delete_info_decref_array(col_names)\n'
    else:
        ezw__epg += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        ezw__epg += (
            '                            table, col_names, index_col,\n')
        ezw__epg += '                            ' + str(mtur__aat) + ',\n'
        ezw__epg += '                            unicode_to_utf8(metadata),\n'
        ezw__epg += (
            '                            unicode_to_utf8(compression),\n')
        ezw__epg += '                            _is_parallel, 0, 0, 0, 0,\n'
        ezw__epg += '                            unicode_to_utf8(name_ptr),\n'
        ezw__epg += (
            '                            unicode_to_utf8(bucket_region),\n')
        ezw__epg += '                            row_group_size)\n'
        ezw__epg += '    delete_table_decref_arrays(table)\n'
        ezw__epg += '    delete_info_decref_array(index_col)\n'
        ezw__epg += '    delete_info_decref_array(col_names)\n'
    vfg__zksc = {}
    if df.has_runtime_cols:
        axy__dxw = None
    else:
        for tpv__gpuw in df.columns:
            if not isinstance(tpv__gpuw, str):
                raise BodoError(
                    'DataFrame.to_parquet(): parquet must have string column names'
                    )
        axy__dxw = pd.array(df.columns)
    exec(ezw__epg, {'np': np, 'bodo': bodo, 'unicode_to_utf8':
        unicode_to_utf8, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'str_arr_from_sequence': str_arr_from_sequence,
        'parquet_write_table_cpp': parquet_write_table_cpp,
        'parquet_write_table_partitioned_cpp':
        parquet_write_table_partitioned_cpp, 'index_to_array':
        index_to_array, 'delete_info_decref_array':
        delete_info_decref_array, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'col_names_arr': axy__dxw,
        'py_table_to_cpp_table': py_table_to_cpp_table, 'py_table_typ': df.
        table_type, 'get_dataframe_table': get_dataframe_table,
        'col_names_no_parts_arr': glr__gzaa, 'get_dataframe_column_names':
        get_dataframe_column_names, 'fix_arr_dtype': fix_arr_dtype,
        'decode_if_dict_array': decode_if_dict_array,
        'decode_if_dict_table': decode_if_dict_table}, vfg__zksc)
    czz__rsc = vfg__zksc['df_to_parquet']
    return czz__rsc


def to_sql_exception_guard(df, name, con, schema=None, if_exists='fail',
    index=True, index_label=None, chunksize=None, dtype=None, method=None,
    _is_table_create=False, _is_parallel=False):
    snngd__jdr = 'all_ok'
    kzflr__cjq, alvc__vxbm = bodo.ir.sql_ext.parse_dbtype(con)
    if _is_parallel and bodo.get_rank() == 0:
        qbgv__brvke = 100
        if chunksize is None:
            yat__ekggk = qbgv__brvke
        else:
            yat__ekggk = min(chunksize, qbgv__brvke)
        if _is_table_create:
            df = df.iloc[:yat__ekggk, :]
        else:
            df = df.iloc[yat__ekggk:, :]
            if len(df) == 0:
                return snngd__jdr
    eit__nrul = df.columns
    try:
        if kzflr__cjq == 'snowflake':
            if alvc__vxbm and con.count(alvc__vxbm) == 1:
                con = con.replace(alvc__vxbm, quote(alvc__vxbm))
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
                df.columns = [(hkgsg__nlrn.upper() if hkgsg__nlrn.islower()
                     else hkgsg__nlrn) for hkgsg__nlrn in df.columns]
            except ImportError as wafvt__zelyg:
                snngd__jdr = (
                    "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires both snowflake-sqlalchemy and snowflake-connector-python. These can be installed by calling 'conda install -c conda-forge snowflake-sqlalchemy snowflake-connector-python' or 'pip install snowflake-sqlalchemy snowflake-connector-python'."
                    )
                return snngd__jdr
        if kzflr__cjq == 'oracle':
            import sqlalchemy as sa
            nwsqp__awos = bodo.typeof(df)
            sda__god = {}
            for hkgsg__nlrn, mhhj__hzun in zip(nwsqp__awos.columns,
                nwsqp__awos.data):
                if df[hkgsg__nlrn].dtype == 'object':
                    if mhhj__hzun == datetime_date_array_type:
                        sda__god[hkgsg__nlrn] = sa.types.Date
                    elif mhhj__hzun == bodo.string_array_type:
                        sda__god[hkgsg__nlrn] = sa.types.VARCHAR(df[
                            hkgsg__nlrn].str.len().max())
            dtype = sda__god
        try:
            df.to_sql(name, con, schema, if_exists, index, index_label,
                chunksize, dtype, method)
        except Exception as sokr__bpel:
            snngd__jdr = sokr__bpel.args[0]
        return snngd__jdr
    finally:
        df.columns = eit__nrul


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
        iyil__uge = bodo.libs.distributed_api.get_rank()
        snngd__jdr = 'unset'
        if iyil__uge != 0:
            snngd__jdr = bcast_scalar(snngd__jdr)
        elif iyil__uge == 0:
            snngd__jdr = to_sql_exception_guard_encaps(df, name, con,
                schema, if_exists, index, index_label, chunksize, dtype,
                method, True, _is_parallel)
            snngd__jdr = bcast_scalar(snngd__jdr)
        if_exists = 'append'
        if _is_parallel and snngd__jdr == 'all_ok':
            snngd__jdr = to_sql_exception_guard_encaps(df, name, con,
                schema, if_exists, index, index_label, chunksize, dtype,
                method, False, _is_parallel)
        if snngd__jdr != 'all_ok':
            print('err_msg=', snngd__jdr)
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
        vrf__uulma = get_overload_const_str(path_or_buf)
        if vrf__uulma.endswith(('.gz', '.bz2', '.zip', '.xz')):
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
        glnkv__qyt = bodo.io.fs_io.get_s3_bucket_region_njit(path_or_buf,
            parallel=False)
        if lines and orient == 'records':
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, True,
                unicode_to_utf8(glnkv__qyt))
            bodo.utils.utils.check_and_propagate_cpp_exception()
        else:
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, False,
                unicode_to_utf8(glnkv__qyt))
            bodo.utils.utils.check_and_propagate_cpp_exception()
    return _impl


@overload(pd.get_dummies, inline='always', no_unliteral=True)
def get_dummies(data, prefix=None, prefix_sep='_', dummy_na=False, columns=
    None, sparse=False, drop_first=False, dtype=None):
    ywus__imm = {'prefix': prefix, 'prefix_sep': prefix_sep, 'dummy_na':
        dummy_na, 'columns': columns, 'sparse': sparse, 'drop_first':
        drop_first, 'dtype': dtype}
    moqg__wsj = {'prefix': None, 'prefix_sep': '_', 'dummy_na': False,
        'columns': None, 'sparse': False, 'drop_first': False, 'dtype': None}
    check_unsupported_args('pandas.get_dummies', ywus__imm, moqg__wsj,
        package_name='pandas', module_name='General')
    if not categorical_can_construct_dataframe(data):
        raise BodoError(
            'pandas.get_dummies() only support categorical data types with explicitly known categories'
            )
    ezw__epg = """def impl(data, prefix=None, prefix_sep='_', dummy_na=False, columns=None, sparse=False, drop_first=False, dtype=None,):
"""
    if isinstance(data, SeriesType):
        zrv__wxp = data.data.dtype.categories
        ezw__epg += (
            '  data_values = bodo.hiframes.pd_series_ext.get_series_data(data)\n'
            )
    else:
        zrv__wxp = data.dtype.categories
        ezw__epg += '  data_values = data\n'
    yueqz__wph = len(zrv__wxp)
    ezw__epg += """  codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(data_values)
"""
    ezw__epg += '  numba.parfors.parfor.init_prange()\n'
    ezw__epg += '  n = len(data_values)\n'
    for i in range(yueqz__wph):
        ezw__epg += '  data_arr_{} = np.empty(n, np.uint8)\n'.format(i)
    ezw__epg += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    ezw__epg += '      if bodo.libs.array_kernels.isna(data_values, i):\n'
    for jsp__thh in range(yueqz__wph):
        ezw__epg += '          data_arr_{}[i] = 0\n'.format(jsp__thh)
    ezw__epg += '      else:\n'
    for fjno__ezi in range(yueqz__wph):
        ezw__epg += '          data_arr_{0}[i] = codes[i] == {0}\n'.format(
            fjno__ezi)
    ojfvj__ixg = ', '.join(f'data_arr_{i}' for i in range(yueqz__wph))
    index = 'bodo.hiframes.pd_index_ext.init_range_index(0, n, 1, None)'
    if isinstance(zrv__wxp[0], np.datetime64):
        zrv__wxp = tuple(pd.Timestamp(hkgsg__nlrn) for hkgsg__nlrn in zrv__wxp)
    elif isinstance(zrv__wxp[0], np.timedelta64):
        zrv__wxp = tuple(pd.Timedelta(hkgsg__nlrn) for hkgsg__nlrn in zrv__wxp)
    return bodo.hiframes.dataframe_impl._gen_init_df(ezw__epg, zrv__wxp,
        ojfvj__ixg, index)


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
    for unebx__hmbnx in pd_unsupported:
        escjv__zwgw = mod_name + '.' + unebx__hmbnx.__name__
        overload(unebx__hmbnx, no_unliteral=True)(create_unsupported_overload
            (escjv__zwgw))


def _install_dataframe_unsupported():
    for ghhs__nbomg in dataframe_unsupported_attrs:
        kgeoh__osevi = 'DataFrame.' + ghhs__nbomg
        overload_attribute(DataFrameType, ghhs__nbomg)(
            create_unsupported_overload(kgeoh__osevi))
    for escjv__zwgw in dataframe_unsupported:
        kgeoh__osevi = 'DataFrame.' + escjv__zwgw + '()'
        overload_method(DataFrameType, escjv__zwgw)(create_unsupported_overload
            (kgeoh__osevi))


_install_pd_unsupported('pandas', pd_unsupported)
_install_pd_unsupported('pandas.util', pd_util_unsupported)
_install_dataframe_unsupported()
