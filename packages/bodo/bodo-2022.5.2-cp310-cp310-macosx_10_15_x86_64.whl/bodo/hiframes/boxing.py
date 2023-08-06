"""
Boxing and unboxing support for DataFrame, Series, etc.
"""
import datetime
import decimal
import warnings
from enum import Enum
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.ir_utils import GuardException, guard
from numba.core.typing import signature
from numba.cpython.listobj import ListInstance
from numba.extending import NativeValue, box, intrinsic, typeof_impl, unbox
from numba.np import numpy_support
from numba.typed.typeddict import Dict
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import PDCategoricalDtype
from bodo.hiframes.pd_dataframe_ext import DataFramePayloadType, DataFrameType, check_runtime_cols_unsupported, construct_dataframe
from bodo.hiframes.pd_index_ext import BinaryIndexType, CategoricalIndexType, DatetimeIndexType, NumericIndexType, PeriodIndexType, RangeIndexType, StringIndexType, TimedeltaIndexType
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
from bodo.hiframes.split_impl import string_array_split_view_type
from bodo.libs import hstr_ext
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.decimal_arr_ext import Decimal128Type, DecimalArrayType
from bodo.libs.int_arr_ext import IntDtype, IntegerArrayType, typeof_pd_int_dtype
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.pd_datetime_arr_ext import DatetimeArrayType, PandasDatetimeTZDtype
from bodo.libs.str_arr_ext import string_array_type, string_type
from bodo.libs.str_ext import string_type
from bodo.libs.struct_arr_ext import StructArrayType, StructType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.typing import BodoError, BodoWarning, dtype_to_array_type, get_overload_const_bool, get_overload_const_int, get_overload_const_str, is_overload_constant_bool, is_overload_constant_int, is_overload_constant_str, raise_bodo_error, to_nullable_type, to_str_arr_if_dict_array
ll.add_symbol('is_np_array', hstr_ext.is_np_array)
ll.add_symbol('array_size', hstr_ext.array_size)
ll.add_symbol('array_getptr1', hstr_ext.array_getptr1)
TABLE_FORMAT_THRESHOLD = 20
_use_dict_str_type = False


def _set_bodo_meta_in_pandas():
    if '_bodo_meta' not in pd.Series._metadata:
        pd.Series._metadata.append('_bodo_meta')
    if '_bodo_meta' not in pd.DataFrame._metadata:
        pd.DataFrame._metadata.append('_bodo_meta')


_set_bodo_meta_in_pandas()


@typeof_impl.register(pd.DataFrame)
def typeof_pd_dataframe(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    jeklf__clqaq = tuple(val.columns.to_list())
    lov__fjj = get_hiframes_dtypes(val)
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and len(val._bodo_meta['type_metadata'
        ][1]) == len(val.columns) and val._bodo_meta['type_metadata'][0] is not
        None):
        alb__fphpy = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        alb__fphpy = numba.typeof(val.index)
    mbmv__tumc = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    lipl__phrqh = len(lov__fjj) >= TABLE_FORMAT_THRESHOLD
    return DataFrameType(lov__fjj, alb__fphpy, jeklf__clqaq, mbmv__tumc,
        is_table_format=lipl__phrqh)


@typeof_impl.register(pd.Series)
def typeof_pd_series(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    mbmv__tumc = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and val._bodo_meta['type_metadata'][0]
         is not None):
        oma__ifh = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        oma__ifh = numba.typeof(val.index)
    dtype = _infer_series_dtype(val)
    aqz__vkln = dtype_to_array_type(dtype)
    if _use_dict_str_type and aqz__vkln == string_array_type:
        aqz__vkln = bodo.dict_str_arr_type
    return SeriesType(dtype, data=aqz__vkln, index=oma__ifh, name_typ=numba
        .typeof(val.name), dist=mbmv__tumc)


@unbox(DataFrameType)
def unbox_dataframe(typ, val, c):
    check_runtime_cols_unsupported(typ, 'Unboxing')
    uewz__gcmy = c.pyapi.object_getattr_string(val, 'index')
    egcn__asgdy = c.pyapi.to_native_value(typ.index, uewz__gcmy).value
    c.pyapi.decref(uewz__gcmy)
    if typ.is_table_format:
        qydt__cln = cgutils.create_struct_proxy(typ.table_type)(c.context,
            c.builder)
        qydt__cln.parent = val
        for hfwqb__zlb, giqo__lqe in typ.table_type.type_to_blk.items():
            wcb__zrnk = c.context.get_constant(types.int64, len(typ.
                table_type.block_to_arr_ind[giqo__lqe]))
            nyv__hvt, dzu__tbo = ListInstance.allocate_ex(c.context, c.
                builder, types.List(hfwqb__zlb), wcb__zrnk)
            dzu__tbo.size = wcb__zrnk
            setattr(qydt__cln, f'block_{giqo__lqe}', dzu__tbo.value)
        ngfj__yxsxp = c.pyapi.call_method(val, '__len__', ())
        noq__dvjny = c.pyapi.long_as_longlong(ngfj__yxsxp)
        c.pyapi.decref(ngfj__yxsxp)
        qydt__cln.len = noq__dvjny
        orl__fpq = c.context.make_tuple(c.builder, types.Tuple([typ.
            table_type]), [qydt__cln._getvalue()])
    else:
        mnswd__qxmza = [c.context.get_constant_null(hfwqb__zlb) for
            hfwqb__zlb in typ.data]
        orl__fpq = c.context.make_tuple(c.builder, types.Tuple(typ.data),
            mnswd__qxmza)
    qkuy__cjj = construct_dataframe(c.context, c.builder, typ, orl__fpq,
        egcn__asgdy, val, None)
    return NativeValue(qkuy__cjj)


def get_hiframes_dtypes(df):
    if (hasattr(df, '_bodo_meta') and df._bodo_meta is not None and 
        'type_metadata' in df._bodo_meta and df._bodo_meta['type_metadata']
         is not None and len(df._bodo_meta['type_metadata'][1]) == len(df.
        columns)):
        pulp__yej = df._bodo_meta['type_metadata'][1]
    else:
        pulp__yej = [None] * len(df.columns)
    gbxc__dyz = [dtype_to_array_type(_infer_series_dtype(df.iloc[:, i],
        array_metadata=pulp__yej[i])) for i in range(len(df.columns))]
    gbxc__dyz = [(bodo.dict_str_arr_type if _use_dict_str_type and 
        hfwqb__zlb == string_array_type else hfwqb__zlb) for hfwqb__zlb in
        gbxc__dyz]
    return tuple(gbxc__dyz)


class SeriesDtypeEnum(Enum):
    Int8 = 0
    UInt8 = 1
    Int32 = 2
    UInt32 = 3
    Int64 = 4
    UInt64 = 7
    Float32 = 5
    Float64 = 6
    Int16 = 8
    UInt16 = 9
    STRING = 10
    Bool = 11
    Decimal = 12
    Datime_Date = 13
    NP_Datetime64ns = 14
    NP_Timedelta64ns = 15
    Int128 = 16
    LIST = 18
    STRUCT = 19
    BINARY = 21
    ARRAY = 22
    PD_nullable_Int8 = 23
    PD_nullable_UInt8 = 24
    PD_nullable_Int16 = 25
    PD_nullable_UInt16 = 26
    PD_nullable_Int32 = 27
    PD_nullable_UInt32 = 28
    PD_nullable_Int64 = 29
    PD_nullable_UInt64 = 30
    PD_nullable_bool = 31
    CategoricalType = 32
    NoneType = 33
    Literal = 34
    IntegerArray = 35
    RangeIndexType = 36
    DatetimeIndexType = 37
    NumericIndexType = 38
    PeriodIndexType = 39
    IntervalIndexType = 40
    CategoricalIndexType = 41
    StringIndexType = 42
    BinaryIndexType = 43
    TimedeltaIndexType = 44
    LiteralType = 45


_one_to_one_type_to_enum_map = {types.int8: SeriesDtypeEnum.Int8.value,
    types.uint8: SeriesDtypeEnum.UInt8.value, types.int32: SeriesDtypeEnum.
    Int32.value, types.uint32: SeriesDtypeEnum.UInt32.value, types.int64:
    SeriesDtypeEnum.Int64.value, types.uint64: SeriesDtypeEnum.UInt64.value,
    types.float32: SeriesDtypeEnum.Float32.value, types.float64:
    SeriesDtypeEnum.Float64.value, types.NPDatetime('ns'): SeriesDtypeEnum.
    NP_Datetime64ns.value, types.NPTimedelta('ns'): SeriesDtypeEnum.
    NP_Timedelta64ns.value, types.bool_: SeriesDtypeEnum.Bool.value, types.
    int16: SeriesDtypeEnum.Int16.value, types.uint16: SeriesDtypeEnum.
    UInt16.value, types.Integer('int128', 128): SeriesDtypeEnum.Int128.
    value, bodo.hiframes.datetime_date_ext.datetime_date_type:
    SeriesDtypeEnum.Datime_Date.value, IntDtype(types.int8):
    SeriesDtypeEnum.PD_nullable_Int8.value, IntDtype(types.uint8):
    SeriesDtypeEnum.PD_nullable_UInt8.value, IntDtype(types.int16):
    SeriesDtypeEnum.PD_nullable_Int16.value, IntDtype(types.uint16):
    SeriesDtypeEnum.PD_nullable_UInt16.value, IntDtype(types.int32):
    SeriesDtypeEnum.PD_nullable_Int32.value, IntDtype(types.uint32):
    SeriesDtypeEnum.PD_nullable_UInt32.value, IntDtype(types.int64):
    SeriesDtypeEnum.PD_nullable_Int64.value, IntDtype(types.uint64):
    SeriesDtypeEnum.PD_nullable_UInt64.value, bytes_type: SeriesDtypeEnum.
    BINARY.value, string_type: SeriesDtypeEnum.STRING.value, bodo.bool_:
    SeriesDtypeEnum.Bool.value, types.none: SeriesDtypeEnum.NoneType.value}
_one_to_one_enum_to_type_map = {SeriesDtypeEnum.Int8.value: types.int8,
    SeriesDtypeEnum.UInt8.value: types.uint8, SeriesDtypeEnum.Int32.value:
    types.int32, SeriesDtypeEnum.UInt32.value: types.uint32,
    SeriesDtypeEnum.Int64.value: types.int64, SeriesDtypeEnum.UInt64.value:
    types.uint64, SeriesDtypeEnum.Float32.value: types.float32,
    SeriesDtypeEnum.Float64.value: types.float64, SeriesDtypeEnum.
    NP_Datetime64ns.value: types.NPDatetime('ns'), SeriesDtypeEnum.
    NP_Timedelta64ns.value: types.NPTimedelta('ns'), SeriesDtypeEnum.Int16.
    value: types.int16, SeriesDtypeEnum.UInt16.value: types.uint16,
    SeriesDtypeEnum.Int128.value: types.Integer('int128', 128),
    SeriesDtypeEnum.Datime_Date.value: bodo.hiframes.datetime_date_ext.
    datetime_date_type, SeriesDtypeEnum.PD_nullable_Int8.value: IntDtype(
    types.int8), SeriesDtypeEnum.PD_nullable_UInt8.value: IntDtype(types.
    uint8), SeriesDtypeEnum.PD_nullable_Int16.value: IntDtype(types.int16),
    SeriesDtypeEnum.PD_nullable_UInt16.value: IntDtype(types.uint16),
    SeriesDtypeEnum.PD_nullable_Int32.value: IntDtype(types.int32),
    SeriesDtypeEnum.PD_nullable_UInt32.value: IntDtype(types.uint32),
    SeriesDtypeEnum.PD_nullable_Int64.value: IntDtype(types.int64),
    SeriesDtypeEnum.PD_nullable_UInt64.value: IntDtype(types.uint64),
    SeriesDtypeEnum.BINARY.value: bytes_type, SeriesDtypeEnum.STRING.value:
    string_type, SeriesDtypeEnum.Bool.value: bodo.bool_, SeriesDtypeEnum.
    NoneType.value: types.none}


def _dtype_from_type_enum_list(typ_enum_list):
    awrp__rznjh, typ = _dtype_from_type_enum_list_recursor(typ_enum_list)
    if len(awrp__rznjh) != 0:
        raise_bodo_error(
            f"""Unexpected Internal Error while converting typing metadata: Dtype list was not fully consumed.
 Input typ_enum_list: {typ_enum_list}.
Remainder: {awrp__rznjh}. Please file the error here: https://github.com/Bodo-inc/Feedback"""
            )
    return typ


def _dtype_from_type_enum_list_recursor(typ_enum_list):
    if len(typ_enum_list) == 0:
        raise_bodo_error('Unable to infer dtype from empty typ_enum_list')
    elif typ_enum_list[0] in _one_to_one_enum_to_type_map:
        return typ_enum_list[1:], _one_to_one_enum_to_type_map[typ_enum_list[0]
            ]
    elif typ_enum_list[0] == SeriesDtypeEnum.IntegerArray.value:
        cyaxt__npbvn, typ = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        return cyaxt__npbvn, IntegerArrayType(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.ARRAY.value:
        cyaxt__npbvn, typ = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        return cyaxt__npbvn, dtype_to_array_type(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.Decimal.value:
        ycejh__swt = typ_enum_list[1]
        yft__dais = typ_enum_list[2]
        return typ_enum_list[3:], Decimal128Type(ycejh__swt, yft__dais)
    elif typ_enum_list[0] == SeriesDtypeEnum.STRUCT.value:
        wcqrf__plbm = typ_enum_list[1]
        wml__qbmlg = tuple(typ_enum_list[2:2 + wcqrf__plbm])
        brnwc__napl = typ_enum_list[2 + wcqrf__plbm:]
        dpju__ujphp = []
        for i in range(wcqrf__plbm):
            brnwc__napl, bnwr__cuut = _dtype_from_type_enum_list_recursor(
                brnwc__napl)
            dpju__ujphp.append(bnwr__cuut)
        return brnwc__napl, StructType(tuple(dpju__ujphp), wml__qbmlg)
    elif typ_enum_list[0] == SeriesDtypeEnum.Literal.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'Literal' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        kzdon__zlru = typ_enum_list[1]
        brnwc__napl = typ_enum_list[2:]
        return brnwc__napl, kzdon__zlru
    elif typ_enum_list[0] == SeriesDtypeEnum.LiteralType.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'LiteralType' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        kzdon__zlru = typ_enum_list[1]
        brnwc__napl = typ_enum_list[2:]
        return brnwc__napl, numba.types.literal(kzdon__zlru)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalType.value:
        brnwc__napl, twyzi__jsdca = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        brnwc__napl, kjndk__gye = _dtype_from_type_enum_list_recursor(
            brnwc__napl)
        brnwc__napl, yvgul__xnt = _dtype_from_type_enum_list_recursor(
            brnwc__napl)
        brnwc__napl, podop__uoe = _dtype_from_type_enum_list_recursor(
            brnwc__napl)
        brnwc__napl, ckmcg__uykv = _dtype_from_type_enum_list_recursor(
            brnwc__napl)
        return brnwc__napl, PDCategoricalDtype(twyzi__jsdca, kjndk__gye,
            yvgul__xnt, podop__uoe, ckmcg__uykv)
    elif typ_enum_list[0] == SeriesDtypeEnum.DatetimeIndexType.value:
        brnwc__napl, uas__ffrl = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return brnwc__napl, DatetimeIndexType(uas__ffrl)
    elif typ_enum_list[0] == SeriesDtypeEnum.NumericIndexType.value:
        brnwc__napl, dtype = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        brnwc__napl, uas__ffrl = _dtype_from_type_enum_list_recursor(
            brnwc__napl)
        brnwc__napl, podop__uoe = _dtype_from_type_enum_list_recursor(
            brnwc__napl)
        return brnwc__napl, NumericIndexType(dtype, uas__ffrl, podop__uoe)
    elif typ_enum_list[0] == SeriesDtypeEnum.PeriodIndexType.value:
        brnwc__napl, otuwv__bse = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        brnwc__napl, uas__ffrl = _dtype_from_type_enum_list_recursor(
            brnwc__napl)
        return brnwc__napl, PeriodIndexType(otuwv__bse, uas__ffrl)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalIndexType.value:
        brnwc__napl, podop__uoe = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        brnwc__napl, uas__ffrl = _dtype_from_type_enum_list_recursor(
            brnwc__napl)
        return brnwc__napl, CategoricalIndexType(podop__uoe, uas__ffrl)
    elif typ_enum_list[0] == SeriesDtypeEnum.RangeIndexType.value:
        brnwc__napl, uas__ffrl = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return brnwc__napl, RangeIndexType(uas__ffrl)
    elif typ_enum_list[0] == SeriesDtypeEnum.StringIndexType.value:
        brnwc__napl, uas__ffrl = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return brnwc__napl, StringIndexType(uas__ffrl)
    elif typ_enum_list[0] == SeriesDtypeEnum.BinaryIndexType.value:
        brnwc__napl, uas__ffrl = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return brnwc__napl, BinaryIndexType(uas__ffrl)
    elif typ_enum_list[0] == SeriesDtypeEnum.TimedeltaIndexType.value:
        brnwc__napl, uas__ffrl = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return brnwc__napl, TimedeltaIndexType(uas__ffrl)
    else:
        raise_bodo_error(
            f'Unexpected Internal Error while converting typing metadata: unable to infer dtype for type enum {typ_enum_list[0]}. Please file the error here: https://github.com/Bodo-inc/Feedback'
            )


def _dtype_to_type_enum_list(typ):
    return guard(_dtype_to_type_enum_list_recursor, typ)


def _dtype_to_type_enum_list_recursor(typ, upcast_numeric_index=True):
    if typ.__hash__ and typ in _one_to_one_type_to_enum_map:
        return [_one_to_one_type_to_enum_map[typ]]
    if isinstance(typ, (dict, int, list, tuple, str, bool, bytes, float)):
        return [SeriesDtypeEnum.Literal.value, typ]
    elif typ is None:
        return [SeriesDtypeEnum.Literal.value, typ]
    elif is_overload_constant_int(typ):
        mttq__fniw = get_overload_const_int(typ)
        if numba.types.maybe_literal(mttq__fniw) == typ:
            return [SeriesDtypeEnum.LiteralType.value, mttq__fniw]
    elif is_overload_constant_str(typ):
        mttq__fniw = get_overload_const_str(typ)
        if numba.types.maybe_literal(mttq__fniw) == typ:
            return [SeriesDtypeEnum.LiteralType.value, mttq__fniw]
    elif is_overload_constant_bool(typ):
        mttq__fniw = get_overload_const_bool(typ)
        if numba.types.maybe_literal(mttq__fniw) == typ:
            return [SeriesDtypeEnum.LiteralType.value, mttq__fniw]
    elif isinstance(typ, IntegerArrayType):
        return [SeriesDtypeEnum.IntegerArray.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif bodo.utils.utils.is_array_typ(typ, False):
        return [SeriesDtypeEnum.ARRAY.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif isinstance(typ, StructType):
        wqt__ypulm = [SeriesDtypeEnum.STRUCT.value, len(typ.names)]
        for mxh__glvyq in typ.names:
            wqt__ypulm.append(mxh__glvyq)
        for gkw__zubl in typ.data:
            wqt__ypulm += _dtype_to_type_enum_list_recursor(gkw__zubl)
        return wqt__ypulm
    elif isinstance(typ, bodo.libs.decimal_arr_ext.Decimal128Type):
        return [SeriesDtypeEnum.Decimal.value, typ.precision, typ.scale]
    elif isinstance(typ, PDCategoricalDtype):
        moo__blme = _dtype_to_type_enum_list_recursor(typ.categories)
        ibwr__odizi = _dtype_to_type_enum_list_recursor(typ.elem_type)
        jebo__pav = _dtype_to_type_enum_list_recursor(typ.ordered)
        xpql__nki = _dtype_to_type_enum_list_recursor(typ.data)
        owzes__abmj = _dtype_to_type_enum_list_recursor(typ.int_type)
        return [SeriesDtypeEnum.CategoricalType.value
            ] + moo__blme + ibwr__odizi + jebo__pav + xpql__nki + owzes__abmj
    elif isinstance(typ, DatetimeIndexType):
        return [SeriesDtypeEnum.DatetimeIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, NumericIndexType):
        if upcast_numeric_index:
            if isinstance(typ.dtype, types.Float):
                xepd__ily = types.float64
                bjo__roeya = types.Array(xepd__ily, 1, 'C')
            elif typ.dtype in {types.int8, types.int16, types.int32, types.
                int64}:
                xepd__ily = types.int64
                if isinstance(typ.data, IntegerArrayType):
                    bjo__roeya = IntegerArrayType(xepd__ily)
                else:
                    bjo__roeya = types.Array(xepd__ily, 1, 'C')
            elif typ.dtype in {types.uint8, types.uint16, types.uint32,
                types.uint64}:
                xepd__ily = types.uint64
                if isinstance(typ.data, IntegerArrayType):
                    bjo__roeya = IntegerArrayType(xepd__ily)
                else:
                    bjo__roeya = types.Array(xepd__ily, 1, 'C')
            elif typ.dtype == types.bool_:
                xepd__ily = typ.dtype
                bjo__roeya = typ.data
            else:
                raise GuardException('Unable to convert type')
            return [SeriesDtypeEnum.NumericIndexType.value
                ] + _dtype_to_type_enum_list_recursor(xepd__ily
                ) + _dtype_to_type_enum_list_recursor(typ.name_typ
                ) + _dtype_to_type_enum_list_recursor(bjo__roeya)
        else:
            return [SeriesDtypeEnum.NumericIndexType.value
                ] + _dtype_to_type_enum_list_recursor(typ.dtype
                ) + _dtype_to_type_enum_list_recursor(typ.name_typ
                ) + _dtype_to_type_enum_list_recursor(typ.data)
    elif isinstance(typ, PeriodIndexType):
        return [SeriesDtypeEnum.PeriodIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.freq
            ) + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, CategoricalIndexType):
        return [SeriesDtypeEnum.CategoricalIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.data
            ) + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, RangeIndexType):
        return [SeriesDtypeEnum.RangeIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, StringIndexType):
        return [SeriesDtypeEnum.StringIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, BinaryIndexType):
        return [SeriesDtypeEnum.BinaryIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, TimedeltaIndexType):
        return [SeriesDtypeEnum.TimedeltaIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    else:
        raise GuardException('Unable to convert type')


def _infer_series_dtype(S, array_metadata=None):
    if S.dtype == np.dtype('O'):
        if len(S.values) == 0:
            if array_metadata != None:
                return _dtype_from_type_enum_list(array_metadata).dtype
            elif hasattr(S, '_bodo_meta'
                ) and S._bodo_meta is not None and 'type_metadata' in S._bodo_meta and S._bodo_meta[
                'type_metadata'][1] is not None:
                okcf__ittb = S._bodo_meta['type_metadata'][1]
                return _dtype_from_type_enum_list(okcf__ittb)
        return numba.typeof(S.values).dtype
    if isinstance(S.dtype, pd.core.arrays.integer._IntegerDtype):
        return typeof_pd_int_dtype(S.dtype, None)
    elif isinstance(S.dtype, pd.CategoricalDtype):
        return bodo.typeof(S.dtype)
    elif isinstance(S.dtype, pd.StringDtype):
        return string_type
    elif isinstance(S.dtype, pd.BooleanDtype):
        return types.bool_
    if isinstance(S.dtype, pd.DatetimeTZDtype):
        som__ozfjf = S.dtype.unit
        if som__ozfjf != 'ns':
            raise BodoError("Timezone-aware datetime data requires 'ns' units")
        bclfy__vzon = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(S.
            dtype.tz)
        return PandasDatetimeTZDtype(bclfy__vzon)
    try:
        return numpy_support.from_dtype(S.dtype)
    except:
        raise BodoError(
            f'data type {S.dtype} for column {S.name} not supported yet')


def _get_use_df_parent_obj_flag(builder, context, pyapi, parent_obj, n_cols):
    if n_cols is None:
        return context.get_constant(types.bool_, False)
    thlpz__jsmg = cgutils.is_not_null(builder, parent_obj)
    ckn__cahl = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with builder.if_then(thlpz__jsmg):
        fmzr__tdf = pyapi.object_getattr_string(parent_obj, 'columns')
        ngfj__yxsxp = pyapi.call_method(fmzr__tdf, '__len__', ())
        builder.store(pyapi.long_as_longlong(ngfj__yxsxp), ckn__cahl)
        pyapi.decref(ngfj__yxsxp)
        pyapi.decref(fmzr__tdf)
    use_parent_obj = builder.and_(thlpz__jsmg, builder.icmp_unsigned('==',
        builder.load(ckn__cahl), context.get_constant(types.int64, n_cols)))
    return use_parent_obj


def _get_df_columns_obj(c, builder, context, pyapi, df_typ, dataframe_payload):
    if df_typ.has_runtime_cols:
        mpvq__ubc = df_typ.runtime_colname_typ
        context.nrt.incref(builder, mpvq__ubc, dataframe_payload.columns)
        return pyapi.from_native_value(mpvq__ubc, dataframe_payload.columns,
            c.env_manager)
    if all(isinstance(c, int) for c in df_typ.columns):
        bzzcx__ynjyp = np.array(df_typ.columns, 'int64')
    elif all(isinstance(c, str) for c in df_typ.columns):
        bzzcx__ynjyp = pd.array(df_typ.columns, 'string')
    else:
        bzzcx__ynjyp = df_typ.columns
    hmwug__rzajv = numba.typeof(bzzcx__ynjyp)
    mwm__uzxh = context.get_constant_generic(builder, hmwug__rzajv,
        bzzcx__ynjyp)
    tztn__hpb = pyapi.from_native_value(hmwug__rzajv, mwm__uzxh, c.env_manager)
    return tztn__hpb


def _create_initial_df_object(builder, context, pyapi, c, df_typ, obj,
    dataframe_payload, res, use_parent_obj):
    with c.builder.if_else(use_parent_obj) as (ysw__zhndf, bno__ygzv):
        with ysw__zhndf:
            pyapi.incref(obj)
            orwv__agsl = context.insert_const_string(c.builder.module, 'numpy')
            nxxxf__bgt = pyapi.import_module_noblock(orwv__agsl)
            if df_typ.has_runtime_cols:
                nhut__oujy = 0
            else:
                nhut__oujy = len(df_typ.columns)
            veyr__bjrzd = pyapi.long_from_longlong(lir.Constant(lir.IntType
                (64), nhut__oujy))
            axp__ofd = pyapi.call_method(nxxxf__bgt, 'arange', (veyr__bjrzd,))
            pyapi.object_setattr_string(obj, 'columns', axp__ofd)
            pyapi.decref(nxxxf__bgt)
            pyapi.decref(axp__ofd)
            pyapi.decref(veyr__bjrzd)
        with bno__ygzv:
            context.nrt.incref(builder, df_typ.index, dataframe_payload.index)
            auxqm__ztb = c.pyapi.from_native_value(df_typ.index,
                dataframe_payload.index, c.env_manager)
            orwv__agsl = context.insert_const_string(c.builder.module, 'pandas'
                )
            nxxxf__bgt = pyapi.import_module_noblock(orwv__agsl)
            df_obj = pyapi.call_method(nxxxf__bgt, 'DataFrame', (pyapi.
                borrow_none(), auxqm__ztb))
            pyapi.decref(nxxxf__bgt)
            pyapi.decref(auxqm__ztb)
            builder.store(df_obj, res)


@box(DataFrameType)
def box_dataframe(typ, val, c):
    from bodo.hiframes.table import box_table
    context = c.context
    builder = c.builder
    pyapi = c.pyapi
    dataframe_payload = bodo.hiframes.pd_dataframe_ext.get_dataframe_payload(c
        .context, c.builder, typ, val)
    ewyfp__hsnvd = cgutils.create_struct_proxy(typ)(context, builder, value=val
        )
    n_cols = len(typ.columns) if not typ.has_runtime_cols else None
    obj = ewyfp__hsnvd.parent
    res = cgutils.alloca_once_value(builder, obj)
    use_parent_obj = _get_use_df_parent_obj_flag(builder, context, pyapi,
        obj, n_cols)
    _create_initial_df_object(builder, context, pyapi, c, typ, obj,
        dataframe_payload, res, use_parent_obj)
    if typ.is_table_format:
        uoc__moav = typ.table_type
        qydt__cln = builder.extract_value(dataframe_payload.data, 0)
        context.nrt.incref(builder, uoc__moav, qydt__cln)
        nhzif__jwul = box_table(uoc__moav, qydt__cln, c, builder.not_(
            use_parent_obj))
        with builder.if_else(use_parent_obj) as (nkngk__frt, olpx__iur):
            with nkngk__frt:
                sfsi__nmjn = pyapi.object_getattr_string(nhzif__jwul, 'arrays')
                xnf__alwlh = c.pyapi.make_none()
                if n_cols is None:
                    ngfj__yxsxp = pyapi.call_method(sfsi__nmjn, '__len__', ())
                    wcb__zrnk = pyapi.long_as_longlong(ngfj__yxsxp)
                    pyapi.decref(ngfj__yxsxp)
                else:
                    wcb__zrnk = context.get_constant(types.int64, n_cols)
                with cgutils.for_range(builder, wcb__zrnk) as kye__evjn:
                    i = kye__evjn.index
                    evsxe__vuwtn = pyapi.list_getitem(sfsi__nmjn, i)
                    kve__sqb = c.builder.icmp_unsigned('!=', evsxe__vuwtn,
                        xnf__alwlh)
                    with builder.if_then(kve__sqb):
                        ibps__ujt = pyapi.long_from_longlong(i)
                        df_obj = builder.load(res)
                        pyapi.object_setitem(df_obj, ibps__ujt, evsxe__vuwtn)
                        pyapi.decref(ibps__ujt)
                pyapi.decref(sfsi__nmjn)
                pyapi.decref(xnf__alwlh)
            with olpx__iur:
                df_obj = builder.load(res)
                auxqm__ztb = pyapi.object_getattr_string(df_obj, 'index')
                squnh__sry = c.pyapi.call_method(nhzif__jwul, 'to_pandas',
                    (auxqm__ztb,))
                builder.store(squnh__sry, res)
                pyapi.decref(df_obj)
                pyapi.decref(auxqm__ztb)
        pyapi.decref(nhzif__jwul)
    else:
        fwnaa__urgub = [builder.extract_value(dataframe_payload.data, i) for
            i in range(n_cols)]
        raf__dem = typ.data
        for i, hxs__rbdw, aqz__vkln in zip(range(n_cols), fwnaa__urgub,
            raf__dem):
            lkgl__rvdko = cgutils.alloca_once_value(builder, hxs__rbdw)
            iqe__bvxg = cgutils.alloca_once_value(builder, context.
                get_constant_null(aqz__vkln))
            kve__sqb = builder.not_(is_ll_eq(builder, lkgl__rvdko, iqe__bvxg))
            iipqn__gytdd = builder.or_(builder.not_(use_parent_obj),
                builder.and_(use_parent_obj, kve__sqb))
            with builder.if_then(iipqn__gytdd):
                ibps__ujt = pyapi.long_from_longlong(context.get_constant(
                    types.int64, i))
                context.nrt.incref(builder, aqz__vkln, hxs__rbdw)
                arr_obj = pyapi.from_native_value(aqz__vkln, hxs__rbdw, c.
                    env_manager)
                df_obj = builder.load(res)
                pyapi.object_setitem(df_obj, ibps__ujt, arr_obj)
                pyapi.decref(arr_obj)
                pyapi.decref(ibps__ujt)
    df_obj = builder.load(res)
    tztn__hpb = _get_df_columns_obj(c, builder, context, pyapi, typ,
        dataframe_payload)
    pyapi.object_setattr_string(df_obj, 'columns', tztn__hpb)
    pyapi.decref(tztn__hpb)
    _set_bodo_meta_dataframe(c, df_obj, typ)
    c.context.nrt.decref(c.builder, typ, val)
    return df_obj


def get_df_obj_column_codegen(context, builder, pyapi, df_obj, col_ind,
    data_typ):
    xnf__alwlh = pyapi.borrow_none()
    fqti__biua = pyapi.unserialize(pyapi.serialize_object(slice))
    obpu__aqb = pyapi.call_function_objargs(fqti__biua, [xnf__alwlh])
    dveeq__durm = pyapi.long_from_longlong(col_ind)
    uph__aqvpe = pyapi.tuple_pack([obpu__aqb, dveeq__durm])
    ceilf__deamm = pyapi.object_getattr_string(df_obj, 'iloc')
    leuzl__cde = pyapi.object_getitem(ceilf__deamm, uph__aqvpe)
    if isinstance(data_typ, bodo.DatetimeArrayType):
        fhe__czo = pyapi.object_getattr_string(leuzl__cde, 'array')
    else:
        fhe__czo = pyapi.object_getattr_string(leuzl__cde, 'values')
    if isinstance(data_typ, types.Array):
        zlt__iqzrw = context.insert_const_string(builder.module, 'numpy')
        xlsc__scf = pyapi.import_module_noblock(zlt__iqzrw)
        arr_obj = pyapi.call_method(xlsc__scf, 'ascontiguousarray', (fhe__czo,)
            )
        pyapi.decref(fhe__czo)
        pyapi.decref(xlsc__scf)
    else:
        arr_obj = fhe__czo
    pyapi.decref(fqti__biua)
    pyapi.decref(obpu__aqb)
    pyapi.decref(dveeq__durm)
    pyapi.decref(uph__aqvpe)
    pyapi.decref(ceilf__deamm)
    pyapi.decref(leuzl__cde)
    return arr_obj


@intrinsic
def unbox_dataframe_column(typingctx, df, i=None):
    assert isinstance(df, DataFrameType) and is_overload_constant_int(i)

    def codegen(context, builder, sig, args):
        pyapi = context.get_python_api(builder)
        c = numba.core.pythonapi._UnboxContext(context, builder, pyapi)
        df_typ = sig.args[0]
        col_ind = get_overload_const_int(sig.args[1])
        data_typ = df_typ.data[col_ind]
        ewyfp__hsnvd = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        arr_obj = get_df_obj_column_codegen(context, builder, pyapi,
            ewyfp__hsnvd.parent, args[1], data_typ)
        jcsd__bsrfr = _unbox_series_data(data_typ.dtype, data_typ, arr_obj, c)
        c.pyapi.decref(arr_obj)
        dataframe_payload = (bodo.hiframes.pd_dataframe_ext.
            get_dataframe_payload(c.context, c.builder, df_typ, args[0]))
        if df_typ.is_table_format:
            qydt__cln = cgutils.create_struct_proxy(df_typ.table_type)(c.
                context, c.builder, builder.extract_value(dataframe_payload
                .data, 0))
            giqo__lqe = df_typ.table_type.type_to_blk[data_typ]
            haf__xta = getattr(qydt__cln, f'block_{giqo__lqe}')
            uhq__octjm = ListInstance(c.context, c.builder, types.List(
                data_typ), haf__xta)
            nidab__hmjd = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[col_ind])
            uhq__octjm.inititem(nidab__hmjd, jcsd__bsrfr.value, incref=False)
        else:
            dataframe_payload.data = builder.insert_value(dataframe_payload
                .data, jcsd__bsrfr.value, col_ind)
        mij__tol = DataFramePayloadType(df_typ)
        yizlq__qpscc = context.nrt.meminfo_data(builder, ewyfp__hsnvd.meminfo)
        sqar__vhl = context.get_value_type(mij__tol).as_pointer()
        yizlq__qpscc = builder.bitcast(yizlq__qpscc, sqar__vhl)
        builder.store(dataframe_payload._getvalue(), yizlq__qpscc)
    return signature(types.none, df, i), codegen


@numba.njit
def unbox_col_if_needed(df, i):
    if bodo.hiframes.pd_dataframe_ext.has_parent(df
        ) and bodo.hiframes.pd_dataframe_ext._column_needs_unboxing(df, i):
        bodo.hiframes.boxing.unbox_dataframe_column(df, i)


@unbox(SeriesType)
def unbox_series(typ, val, c):
    if isinstance(typ.data, DatetimeArrayType):
        fhe__czo = c.pyapi.object_getattr_string(val, 'array')
    else:
        fhe__czo = c.pyapi.object_getattr_string(val, 'values')
    if isinstance(typ.data, types.Array):
        zlt__iqzrw = c.context.insert_const_string(c.builder.module, 'numpy')
        xlsc__scf = c.pyapi.import_module_noblock(zlt__iqzrw)
        arr_obj = c.pyapi.call_method(xlsc__scf, 'ascontiguousarray', (
            fhe__czo,))
        c.pyapi.decref(fhe__czo)
        c.pyapi.decref(xlsc__scf)
    else:
        arr_obj = fhe__czo
    ivy__zbyt = _unbox_series_data(typ.dtype, typ.data, arr_obj, c).value
    auxqm__ztb = c.pyapi.object_getattr_string(val, 'index')
    egcn__asgdy = c.pyapi.to_native_value(typ.index, auxqm__ztb).value
    nfqz__fuv = c.pyapi.object_getattr_string(val, 'name')
    zelae__uooj = c.pyapi.to_native_value(typ.name_typ, nfqz__fuv).value
    vzak__zzca = bodo.hiframes.pd_series_ext.construct_series(c.context, c.
        builder, typ, ivy__zbyt, egcn__asgdy, zelae__uooj)
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(auxqm__ztb)
    c.pyapi.decref(nfqz__fuv)
    return NativeValue(vzak__zzca)


def _unbox_series_data(dtype, data_typ, arr_obj, c):
    if data_typ == string_array_split_view_type:
        fir__hrbk = c.context.make_helper(c.builder,
            string_array_split_view_type)
        return NativeValue(fir__hrbk._getvalue())
    return c.pyapi.to_native_value(data_typ, arr_obj)


@box(HeterogeneousSeriesType)
@box(SeriesType)
def box_series(typ, val, c):
    orwv__agsl = c.context.insert_const_string(c.builder.module, 'pandas')
    jwd__ufc = c.pyapi.import_module_noblock(orwv__agsl)
    bor__fqzi = bodo.hiframes.pd_series_ext.get_series_payload(c.context, c
        .builder, typ, val)
    c.context.nrt.incref(c.builder, typ.data, bor__fqzi.data)
    c.context.nrt.incref(c.builder, typ.index, bor__fqzi.index)
    c.context.nrt.incref(c.builder, typ.name_typ, bor__fqzi.name)
    arr_obj = c.pyapi.from_native_value(typ.data, bor__fqzi.data, c.env_manager
        )
    auxqm__ztb = c.pyapi.from_native_value(typ.index, bor__fqzi.index, c.
        env_manager)
    nfqz__fuv = c.pyapi.from_native_value(typ.name_typ, bor__fqzi.name, c.
        env_manager)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        dtype = c.pyapi.unserialize(c.pyapi.serialize_object(object))
    else:
        dtype = c.pyapi.make_none()
    res = c.pyapi.call_method(jwd__ufc, 'Series', (arr_obj, auxqm__ztb,
        dtype, nfqz__fuv))
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(auxqm__ztb)
    c.pyapi.decref(nfqz__fuv)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        c.pyapi.decref(dtype)
    _set_bodo_meta_series(res, c, typ)
    c.pyapi.decref(jwd__ufc)
    c.context.nrt.decref(c.builder, typ, val)
    return res


def type_enum_list_to_py_list_obj(pyapi, context, builder, env_manager,
    typ_list):
    wdk__emxib = []
    for pdwc__mmgqm in typ_list:
        if isinstance(pdwc__mmgqm, int) and not isinstance(pdwc__mmgqm, bool):
            gktd__mgvch = pyapi.long_from_longlong(lir.Constant(lir.IntType
                (64), pdwc__mmgqm))
        else:
            oga__snp = numba.typeof(pdwc__mmgqm)
            uyix__cgdn = context.get_constant_generic(builder, oga__snp,
                pdwc__mmgqm)
            gktd__mgvch = pyapi.from_native_value(oga__snp, uyix__cgdn,
                env_manager)
        wdk__emxib.append(gktd__mgvch)
    lxyhc__cpm = pyapi.list_pack(wdk__emxib)
    for val in wdk__emxib:
        pyapi.decref(val)
    return lxyhc__cpm


def _set_bodo_meta_dataframe(c, obj, typ):
    pyapi = c.pyapi
    context = c.context
    builder = c.builder
    flgo__pgf = not typ.has_runtime_cols and (not typ.is_table_format or 
        len(typ.columns) < TABLE_FORMAT_THRESHOLD)
    mwi__ennv = 2 if flgo__pgf else 1
    ukjup__auv = pyapi.dict_new(mwi__ennv)
    gvoxb__jhpo = pyapi.long_from_longlong(lir.Constant(lir.IntType(64),
        typ.dist.value))
    pyapi.dict_setitem_string(ukjup__auv, 'dist', gvoxb__jhpo)
    pyapi.decref(gvoxb__jhpo)
    if flgo__pgf:
        vuuu__koi = _dtype_to_type_enum_list(typ.index)
        if vuuu__koi != None:
            mqfuw__lvwcl = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, vuuu__koi)
        else:
            mqfuw__lvwcl = pyapi.make_none()
        ywrn__sma = []
        for dtype in typ.data:
            typ_list = _dtype_to_type_enum_list(dtype)
            if typ_list != None:
                lxyhc__cpm = type_enum_list_to_py_list_obj(pyapi, context,
                    builder, c.env_manager, typ_list)
            else:
                lxyhc__cpm = pyapi.make_none()
            ywrn__sma.append(lxyhc__cpm)
        ehsvb__fbo = pyapi.list_pack(ywrn__sma)
        zotkt__fut = pyapi.list_pack([mqfuw__lvwcl, ehsvb__fbo])
        for val in ywrn__sma:
            pyapi.decref(val)
        pyapi.dict_setitem_string(ukjup__auv, 'type_metadata', zotkt__fut)
    pyapi.object_setattr_string(obj, '_bodo_meta', ukjup__auv)
    pyapi.decref(ukjup__auv)


def get_series_dtype_handle_null_int_and_hetrogenous(series_typ):
    if isinstance(series_typ, HeterogeneousSeriesType):
        return None
    if isinstance(series_typ.dtype, types.Number) and isinstance(series_typ
        .data, IntegerArrayType):
        return IntDtype(series_typ.dtype)
    return series_typ.dtype


def _set_bodo_meta_series(obj, c, typ):
    pyapi = c.pyapi
    context = c.context
    builder = c.builder
    ukjup__auv = pyapi.dict_new(2)
    gvoxb__jhpo = pyapi.long_from_longlong(lir.Constant(lir.IntType(64),
        typ.dist.value))
    vuuu__koi = _dtype_to_type_enum_list(typ.index)
    if vuuu__koi != None:
        mqfuw__lvwcl = type_enum_list_to_py_list_obj(pyapi, context,
            builder, c.env_manager, vuuu__koi)
    else:
        mqfuw__lvwcl = pyapi.make_none()
    dtype = get_series_dtype_handle_null_int_and_hetrogenous(typ)
    if dtype != None:
        typ_list = _dtype_to_type_enum_list(dtype)
        if typ_list != None:
            nbys__ckjhb = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, typ_list)
        else:
            nbys__ckjhb = pyapi.make_none()
    else:
        nbys__ckjhb = pyapi.make_none()
    quq__gtu = pyapi.list_pack([mqfuw__lvwcl, nbys__ckjhb])
    pyapi.dict_setitem_string(ukjup__auv, 'type_metadata', quq__gtu)
    pyapi.decref(quq__gtu)
    pyapi.dict_setitem_string(ukjup__auv, 'dist', gvoxb__jhpo)
    pyapi.object_setattr_string(obj, '_bodo_meta', ukjup__auv)
    pyapi.decref(ukjup__auv)
    pyapi.decref(gvoxb__jhpo)


@typeof_impl.register(np.ndarray)
def _typeof_ndarray(val, c):
    try:
        dtype = numba.np.numpy_support.from_dtype(val.dtype)
    except NotImplementedError as jauet__ptq:
        dtype = types.pyobject
    if dtype == types.pyobject:
        return _infer_ndarray_obj_dtype(val)
    anc__nfjsi = numba.np.numpy_support.map_layout(val)
    nujef__rnh = not val.flags.writeable
    return types.Array(dtype, val.ndim, anc__nfjsi, readonly=nujef__rnh)


def _infer_ndarray_obj_dtype(val):
    if not val.dtype == np.dtype('O'):
        raise BodoError('Unsupported array dtype: {}'.format(val.dtype))
    i = 0
    while i < len(val) and (pd.api.types.is_scalar(val[i]) and pd.isna(val[
        i]) or not pd.api.types.is_scalar(val[i]) and len(val[i]) == 0):
        i += 1
    if i == len(val):
        warnings.warn(BodoWarning(
            'Empty object array passed to Bodo, which causes ambiguity in typing. This can cause errors in parallel execution.'
            ))
        return (bodo.dict_str_arr_type if _use_dict_str_type else
            string_array_type)
    tsrta__lndsw = val[i]
    if isinstance(tsrta__lndsw, str):
        return (bodo.dict_str_arr_type if _use_dict_str_type else
            string_array_type)
    elif isinstance(tsrta__lndsw, bytes):
        return binary_array_type
    elif isinstance(tsrta__lndsw, bool):
        return bodo.libs.bool_arr_ext.boolean_array
    elif isinstance(tsrta__lndsw, (int, np.int8, np.int16, np.int32, np.
        int64, np.uint8, np.uint16, np.uint32, np.uint64)):
        return bodo.libs.int_arr_ext.IntegerArrayType(numba.typeof(
            tsrta__lndsw))
    elif isinstance(tsrta__lndsw, (dict, Dict)) and all(isinstance(
        loqd__csda, str) for loqd__csda in tsrta__lndsw.keys()):
        wml__qbmlg = tuple(tsrta__lndsw.keys())
        spjgp__sexq = tuple(_get_struct_value_arr_type(v) for v in
            tsrta__lndsw.values())
        return StructArrayType(spjgp__sexq, wml__qbmlg)
    elif isinstance(tsrta__lndsw, (dict, Dict)):
        lpxj__rqt = numba.typeof(_value_to_array(list(tsrta__lndsw.keys())))
        zihet__qrjha = numba.typeof(_value_to_array(list(tsrta__lndsw.
            values())))
        lpxj__rqt = to_str_arr_if_dict_array(lpxj__rqt)
        zihet__qrjha = to_str_arr_if_dict_array(zihet__qrjha)
        return MapArrayType(lpxj__rqt, zihet__qrjha)
    elif isinstance(tsrta__lndsw, tuple):
        spjgp__sexq = tuple(_get_struct_value_arr_type(v) for v in tsrta__lndsw
            )
        return TupleArrayType(spjgp__sexq)
    if isinstance(tsrta__lndsw, (list, np.ndarray, pd.arrays.BooleanArray,
        pd.arrays.IntegerArray, pd.arrays.StringArray)):
        if isinstance(tsrta__lndsw, list):
            tsrta__lndsw = _value_to_array(tsrta__lndsw)
        ansuu__zvn = numba.typeof(tsrta__lndsw)
        ansuu__zvn = to_str_arr_if_dict_array(ansuu__zvn)
        return ArrayItemArrayType(ansuu__zvn)
    if isinstance(tsrta__lndsw, datetime.date):
        return datetime_date_array_type
    if isinstance(tsrta__lndsw, datetime.timedelta):
        return datetime_timedelta_array_type
    if isinstance(tsrta__lndsw, decimal.Decimal):
        return DecimalArrayType(38, 18)
    raise BodoError(
        f'Unsupported object array with first value: {tsrta__lndsw}')


def _value_to_array(val):
    assert isinstance(val, (list, dict, Dict))
    if isinstance(val, (dict, Dict)):
        val = dict(val)
        return np.array([val], np.object_)
    udqv__iui = val.copy()
    udqv__iui.append(None)
    hxs__rbdw = np.array(udqv__iui, np.object_)
    if len(val) and isinstance(val[0], float):
        hxs__rbdw = np.array(val, np.float64)
    return hxs__rbdw


def _get_struct_value_arr_type(v):
    if isinstance(v, (dict, Dict)):
        return numba.typeof(_value_to_array(v))
    if isinstance(v, list):
        return dtype_to_array_type(numba.typeof(_value_to_array(v)))
    if pd.api.types.is_scalar(v) and pd.isna(v):
        warnings.warn(BodoWarning(
            'Field value in struct array is NA, which causes ambiguity in typing. This can cause errors in parallel execution.'
            ))
        return string_array_type
    aqz__vkln = dtype_to_array_type(numba.typeof(v))
    if isinstance(v, (int, bool)):
        aqz__vkln = to_nullable_type(aqz__vkln)
    return aqz__vkln
