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
    gyygr__ymzd = tuple(val.columns.to_list())
    bhuv__pkama = get_hiframes_dtypes(val)
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and len(val._bodo_meta['type_metadata'
        ][1]) == len(val.columns) and val._bodo_meta['type_metadata'][0] is not
        None):
        qvmj__eip = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        qvmj__eip = numba.typeof(val.index)
    vgd__rhm = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    arz__kuqzc = len(bhuv__pkama) >= TABLE_FORMAT_THRESHOLD
    return DataFrameType(bhuv__pkama, qvmj__eip, gyygr__ymzd, vgd__rhm,
        is_table_format=arz__kuqzc)


@typeof_impl.register(pd.Series)
def typeof_pd_series(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    vgd__rhm = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and val._bodo_meta['type_metadata'][0]
         is not None):
        gyc__shujf = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        gyc__shujf = numba.typeof(val.index)
    dtype = _infer_series_dtype(val)
    pcff__mrt = dtype_to_array_type(dtype)
    if _use_dict_str_type and pcff__mrt == string_array_type:
        pcff__mrt = bodo.dict_str_arr_type
    return SeriesType(dtype, data=pcff__mrt, index=gyc__shujf, name_typ=
        numba.typeof(val.name), dist=vgd__rhm)


@unbox(DataFrameType)
def unbox_dataframe(typ, val, c):
    check_runtime_cols_unsupported(typ, 'Unboxing')
    lrgor__nujhs = c.pyapi.object_getattr_string(val, 'index')
    tjf__erjhr = c.pyapi.to_native_value(typ.index, lrgor__nujhs).value
    c.pyapi.decref(lrgor__nujhs)
    if typ.is_table_format:
        lzwrt__dowzk = cgutils.create_struct_proxy(typ.table_type)(c.
            context, c.builder)
        lzwrt__dowzk.parent = val
        for xgh__kzfsu, lvxhm__oni in typ.table_type.type_to_blk.items():
            gur__lfdm = c.context.get_constant(types.int64, len(typ.
                table_type.block_to_arr_ind[lvxhm__oni]))
            sfai__lgn, tvdu__yuy = ListInstance.allocate_ex(c.context, c.
                builder, types.List(xgh__kzfsu), gur__lfdm)
            tvdu__yuy.size = gur__lfdm
            setattr(lzwrt__dowzk, f'block_{lvxhm__oni}', tvdu__yuy.value)
        wpidc__ewfkv = c.pyapi.call_method(val, '__len__', ())
        wjbyq__kqjwn = c.pyapi.long_as_longlong(wpidc__ewfkv)
        c.pyapi.decref(wpidc__ewfkv)
        lzwrt__dowzk.len = wjbyq__kqjwn
        mpp__wdny = c.context.make_tuple(c.builder, types.Tuple([typ.
            table_type]), [lzwrt__dowzk._getvalue()])
    else:
        eygl__hddkx = [c.context.get_constant_null(xgh__kzfsu) for
            xgh__kzfsu in typ.data]
        mpp__wdny = c.context.make_tuple(c.builder, types.Tuple(typ.data),
            eygl__hddkx)
    wixfw__xagu = construct_dataframe(c.context, c.builder, typ, mpp__wdny,
        tjf__erjhr, val, None)
    return NativeValue(wixfw__xagu)


def get_hiframes_dtypes(df):
    if (hasattr(df, '_bodo_meta') and df._bodo_meta is not None and 
        'type_metadata' in df._bodo_meta and df._bodo_meta['type_metadata']
         is not None and len(df._bodo_meta['type_metadata'][1]) == len(df.
        columns)):
        lhmjc__vkw = df._bodo_meta['type_metadata'][1]
    else:
        lhmjc__vkw = [None] * len(df.columns)
    leut__krc = [dtype_to_array_type(_infer_series_dtype(df.iloc[:, i],
        array_metadata=lhmjc__vkw[i])) for i in range(len(df.columns))]
    leut__krc = [(bodo.dict_str_arr_type if _use_dict_str_type and 
        xgh__kzfsu == string_array_type else xgh__kzfsu) for xgh__kzfsu in
        leut__krc]
    return tuple(leut__krc)


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
    oav__cymg, typ = _dtype_from_type_enum_list_recursor(typ_enum_list)
    if len(oav__cymg) != 0:
        raise_bodo_error(
            f"""Unexpected Internal Error while converting typing metadata: Dtype list was not fully consumed.
 Input typ_enum_list: {typ_enum_list}.
Remainder: {oav__cymg}. Please file the error here: https://github.com/Bodo-inc/Feedback"""
            )
    return typ


def _dtype_from_type_enum_list_recursor(typ_enum_list):
    if len(typ_enum_list) == 0:
        raise_bodo_error('Unable to infer dtype from empty typ_enum_list')
    elif typ_enum_list[0] in _one_to_one_enum_to_type_map:
        return typ_enum_list[1:], _one_to_one_enum_to_type_map[typ_enum_list[0]
            ]
    elif typ_enum_list[0] == SeriesDtypeEnum.IntegerArray.value:
        opyzc__hhcw, typ = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        return opyzc__hhcw, IntegerArrayType(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.ARRAY.value:
        opyzc__hhcw, typ = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        return opyzc__hhcw, dtype_to_array_type(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.Decimal.value:
        iysac__uvf = typ_enum_list[1]
        nxc__hqvb = typ_enum_list[2]
        return typ_enum_list[3:], Decimal128Type(iysac__uvf, nxc__hqvb)
    elif typ_enum_list[0] == SeriesDtypeEnum.STRUCT.value:
        ydram__jrzmb = typ_enum_list[1]
        qktvx__kgvpg = tuple(typ_enum_list[2:2 + ydram__jrzmb])
        iyg__tmh = typ_enum_list[2 + ydram__jrzmb:]
        nbxiu__gjpj = []
        for i in range(ydram__jrzmb):
            iyg__tmh, iunz__bberq = _dtype_from_type_enum_list_recursor(
                iyg__tmh)
            nbxiu__gjpj.append(iunz__bberq)
        return iyg__tmh, StructType(tuple(nbxiu__gjpj), qktvx__kgvpg)
    elif typ_enum_list[0] == SeriesDtypeEnum.Literal.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'Literal' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        bdgbr__qtzf = typ_enum_list[1]
        iyg__tmh = typ_enum_list[2:]
        return iyg__tmh, bdgbr__qtzf
    elif typ_enum_list[0] == SeriesDtypeEnum.LiteralType.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'LiteralType' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        bdgbr__qtzf = typ_enum_list[1]
        iyg__tmh = typ_enum_list[2:]
        return iyg__tmh, numba.types.literal(bdgbr__qtzf)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalType.value:
        iyg__tmh, ovrwr__jkl = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        iyg__tmh, ndw__ktzjc = _dtype_from_type_enum_list_recursor(iyg__tmh)
        iyg__tmh, otle__zemuw = _dtype_from_type_enum_list_recursor(iyg__tmh)
        iyg__tmh, iylt__ewv = _dtype_from_type_enum_list_recursor(iyg__tmh)
        iyg__tmh, abbj__rwoze = _dtype_from_type_enum_list_recursor(iyg__tmh)
        return iyg__tmh, PDCategoricalDtype(ovrwr__jkl, ndw__ktzjc,
            otle__zemuw, iylt__ewv, abbj__rwoze)
    elif typ_enum_list[0] == SeriesDtypeEnum.DatetimeIndexType.value:
        iyg__tmh, svfcz__zyv = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return iyg__tmh, DatetimeIndexType(svfcz__zyv)
    elif typ_enum_list[0] == SeriesDtypeEnum.NumericIndexType.value:
        iyg__tmh, dtype = _dtype_from_type_enum_list_recursor(typ_enum_list[1:]
            )
        iyg__tmh, svfcz__zyv = _dtype_from_type_enum_list_recursor(iyg__tmh)
        iyg__tmh, iylt__ewv = _dtype_from_type_enum_list_recursor(iyg__tmh)
        return iyg__tmh, NumericIndexType(dtype, svfcz__zyv, iylt__ewv)
    elif typ_enum_list[0] == SeriesDtypeEnum.PeriodIndexType.value:
        iyg__tmh, wvxmx__wtmxf = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        iyg__tmh, svfcz__zyv = _dtype_from_type_enum_list_recursor(iyg__tmh)
        return iyg__tmh, PeriodIndexType(wvxmx__wtmxf, svfcz__zyv)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalIndexType.value:
        iyg__tmh, iylt__ewv = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        iyg__tmh, svfcz__zyv = _dtype_from_type_enum_list_recursor(iyg__tmh)
        return iyg__tmh, CategoricalIndexType(iylt__ewv, svfcz__zyv)
    elif typ_enum_list[0] == SeriesDtypeEnum.RangeIndexType.value:
        iyg__tmh, svfcz__zyv = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return iyg__tmh, RangeIndexType(svfcz__zyv)
    elif typ_enum_list[0] == SeriesDtypeEnum.StringIndexType.value:
        iyg__tmh, svfcz__zyv = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return iyg__tmh, StringIndexType(svfcz__zyv)
    elif typ_enum_list[0] == SeriesDtypeEnum.BinaryIndexType.value:
        iyg__tmh, svfcz__zyv = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return iyg__tmh, BinaryIndexType(svfcz__zyv)
    elif typ_enum_list[0] == SeriesDtypeEnum.TimedeltaIndexType.value:
        iyg__tmh, svfcz__zyv = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return iyg__tmh, TimedeltaIndexType(svfcz__zyv)
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
        sygu__bcfzc = get_overload_const_int(typ)
        if numba.types.maybe_literal(sygu__bcfzc) == typ:
            return [SeriesDtypeEnum.LiteralType.value, sygu__bcfzc]
    elif is_overload_constant_str(typ):
        sygu__bcfzc = get_overload_const_str(typ)
        if numba.types.maybe_literal(sygu__bcfzc) == typ:
            return [SeriesDtypeEnum.LiteralType.value, sygu__bcfzc]
    elif is_overload_constant_bool(typ):
        sygu__bcfzc = get_overload_const_bool(typ)
        if numba.types.maybe_literal(sygu__bcfzc) == typ:
            return [SeriesDtypeEnum.LiteralType.value, sygu__bcfzc]
    elif isinstance(typ, IntegerArrayType):
        return [SeriesDtypeEnum.IntegerArray.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif bodo.utils.utils.is_array_typ(typ, False):
        return [SeriesDtypeEnum.ARRAY.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif isinstance(typ, StructType):
        qdzt__pjl = [SeriesDtypeEnum.STRUCT.value, len(typ.names)]
        for yozl__ygdn in typ.names:
            qdzt__pjl.append(yozl__ygdn)
        for vcuz__jsrc in typ.data:
            qdzt__pjl += _dtype_to_type_enum_list_recursor(vcuz__jsrc)
        return qdzt__pjl
    elif isinstance(typ, bodo.libs.decimal_arr_ext.Decimal128Type):
        return [SeriesDtypeEnum.Decimal.value, typ.precision, typ.scale]
    elif isinstance(typ, PDCategoricalDtype):
        puy__lppl = _dtype_to_type_enum_list_recursor(typ.categories)
        mvmow__ummja = _dtype_to_type_enum_list_recursor(typ.elem_type)
        lkspq__apm = _dtype_to_type_enum_list_recursor(typ.ordered)
        gaao__yae = _dtype_to_type_enum_list_recursor(typ.data)
        rzrg__and = _dtype_to_type_enum_list_recursor(typ.int_type)
        return [SeriesDtypeEnum.CategoricalType.value
            ] + puy__lppl + mvmow__ummja + lkspq__apm + gaao__yae + rzrg__and
    elif isinstance(typ, DatetimeIndexType):
        return [SeriesDtypeEnum.DatetimeIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, NumericIndexType):
        if upcast_numeric_index:
            if isinstance(typ.dtype, types.Float):
                jeozz__jpm = types.float64
                ppcqn__bdc = types.Array(jeozz__jpm, 1, 'C')
            elif typ.dtype in {types.int8, types.int16, types.int32, types.
                int64}:
                jeozz__jpm = types.int64
                if isinstance(typ.data, IntegerArrayType):
                    ppcqn__bdc = IntegerArrayType(jeozz__jpm)
                else:
                    ppcqn__bdc = types.Array(jeozz__jpm, 1, 'C')
            elif typ.dtype in {types.uint8, types.uint16, types.uint32,
                types.uint64}:
                jeozz__jpm = types.uint64
                if isinstance(typ.data, IntegerArrayType):
                    ppcqn__bdc = IntegerArrayType(jeozz__jpm)
                else:
                    ppcqn__bdc = types.Array(jeozz__jpm, 1, 'C')
            elif typ.dtype == types.bool_:
                jeozz__jpm = typ.dtype
                ppcqn__bdc = typ.data
            else:
                raise GuardException('Unable to convert type')
            return [SeriesDtypeEnum.NumericIndexType.value
                ] + _dtype_to_type_enum_list_recursor(jeozz__jpm
                ) + _dtype_to_type_enum_list_recursor(typ.name_typ
                ) + _dtype_to_type_enum_list_recursor(ppcqn__bdc)
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
                stw__nojnh = S._bodo_meta['type_metadata'][1]
                return _dtype_from_type_enum_list(stw__nojnh)
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
        dwv__nnt = S.dtype.unit
        if dwv__nnt != 'ns':
            raise BodoError("Timezone-aware datetime data requires 'ns' units")
        uva__iuess = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(S.
            dtype.tz)
        return PandasDatetimeTZDtype(uva__iuess)
    try:
        return numpy_support.from_dtype(S.dtype)
    except:
        raise BodoError(
            f'data type {S.dtype} for column {S.name} not supported yet')


def _get_use_df_parent_obj_flag(builder, context, pyapi, parent_obj, n_cols):
    if n_cols is None:
        return context.get_constant(types.bool_, False)
    nzmz__qtom = cgutils.is_not_null(builder, parent_obj)
    xbut__gxo = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with builder.if_then(nzmz__qtom):
        bltfk__gjgq = pyapi.object_getattr_string(parent_obj, 'columns')
        wpidc__ewfkv = pyapi.call_method(bltfk__gjgq, '__len__', ())
        builder.store(pyapi.long_as_longlong(wpidc__ewfkv), xbut__gxo)
        pyapi.decref(wpidc__ewfkv)
        pyapi.decref(bltfk__gjgq)
    use_parent_obj = builder.and_(nzmz__qtom, builder.icmp_unsigned('==',
        builder.load(xbut__gxo), context.get_constant(types.int64, n_cols)))
    return use_parent_obj


def _get_df_columns_obj(c, builder, context, pyapi, df_typ, dataframe_payload):
    if df_typ.has_runtime_cols:
        onk__igav = df_typ.runtime_colname_typ
        context.nrt.incref(builder, onk__igav, dataframe_payload.columns)
        return pyapi.from_native_value(onk__igav, dataframe_payload.columns,
            c.env_manager)
    if all(isinstance(c, int) for c in df_typ.columns):
        rowt__dgve = np.array(df_typ.columns, 'int64')
    elif all(isinstance(c, str) for c in df_typ.columns):
        rowt__dgve = pd.array(df_typ.columns, 'string')
    else:
        rowt__dgve = df_typ.columns
    rmex__lew = numba.typeof(rowt__dgve)
    vrun__dlpyx = context.get_constant_generic(builder, rmex__lew, rowt__dgve)
    jztag__fltro = pyapi.from_native_value(rmex__lew, vrun__dlpyx, c.
        env_manager)
    return jztag__fltro


def _create_initial_df_object(builder, context, pyapi, c, df_typ, obj,
    dataframe_payload, res, use_parent_obj):
    with c.builder.if_else(use_parent_obj) as (lxth__osj, bsk__kiy):
        with lxth__osj:
            pyapi.incref(obj)
            fmcp__ddgk = context.insert_const_string(c.builder.module, 'numpy')
            owoux__ajzmm = pyapi.import_module_noblock(fmcp__ddgk)
            if df_typ.has_runtime_cols:
                rjsg__yacmw = 0
            else:
                rjsg__yacmw = len(df_typ.columns)
            tqhgi__yadtk = pyapi.long_from_longlong(lir.Constant(lir.
                IntType(64), rjsg__yacmw))
            nun__qijrx = pyapi.call_method(owoux__ajzmm, 'arange', (
                tqhgi__yadtk,))
            pyapi.object_setattr_string(obj, 'columns', nun__qijrx)
            pyapi.decref(owoux__ajzmm)
            pyapi.decref(nun__qijrx)
            pyapi.decref(tqhgi__yadtk)
        with bsk__kiy:
            context.nrt.incref(builder, df_typ.index, dataframe_payload.index)
            qzun__fgm = c.pyapi.from_native_value(df_typ.index,
                dataframe_payload.index, c.env_manager)
            fmcp__ddgk = context.insert_const_string(c.builder.module, 'pandas'
                )
            owoux__ajzmm = pyapi.import_module_noblock(fmcp__ddgk)
            df_obj = pyapi.call_method(owoux__ajzmm, 'DataFrame', (pyapi.
                borrow_none(), qzun__fgm))
            pyapi.decref(owoux__ajzmm)
            pyapi.decref(qzun__fgm)
            builder.store(df_obj, res)


@box(DataFrameType)
def box_dataframe(typ, val, c):
    from bodo.hiframes.table import box_table
    context = c.context
    builder = c.builder
    pyapi = c.pyapi
    dataframe_payload = bodo.hiframes.pd_dataframe_ext.get_dataframe_payload(c
        .context, c.builder, typ, val)
    wex__vbmv = cgutils.create_struct_proxy(typ)(context, builder, value=val)
    n_cols = len(typ.columns) if not typ.has_runtime_cols else None
    obj = wex__vbmv.parent
    res = cgutils.alloca_once_value(builder, obj)
    use_parent_obj = _get_use_df_parent_obj_flag(builder, context, pyapi,
        obj, n_cols)
    _create_initial_df_object(builder, context, pyapi, c, typ, obj,
        dataframe_payload, res, use_parent_obj)
    if typ.is_table_format:
        illy__prumx = typ.table_type
        lzwrt__dowzk = builder.extract_value(dataframe_payload.data, 0)
        context.nrt.incref(builder, illy__prumx, lzwrt__dowzk)
        fwtpe__zvb = box_table(illy__prumx, lzwrt__dowzk, c, builder.not_(
            use_parent_obj))
        with builder.if_else(use_parent_obj) as (ufazg__wxuw, uympa__fdoys):
            with ufazg__wxuw:
                pir__zpc = pyapi.object_getattr_string(fwtpe__zvb, 'arrays')
                vbrf__ami = c.pyapi.make_none()
                if n_cols is None:
                    wpidc__ewfkv = pyapi.call_method(pir__zpc, '__len__', ())
                    gur__lfdm = pyapi.long_as_longlong(wpidc__ewfkv)
                    pyapi.decref(wpidc__ewfkv)
                else:
                    gur__lfdm = context.get_constant(types.int64, n_cols)
                with cgutils.for_range(builder, gur__lfdm) as dai__uufd:
                    i = dai__uufd.index
                    zlwc__wqx = pyapi.list_getitem(pir__zpc, i)
                    ahf__yvmrx = c.builder.icmp_unsigned('!=', zlwc__wqx,
                        vbrf__ami)
                    with builder.if_then(ahf__yvmrx):
                        qgv__efuts = pyapi.long_from_longlong(i)
                        df_obj = builder.load(res)
                        pyapi.object_setitem(df_obj, qgv__efuts, zlwc__wqx)
                        pyapi.decref(qgv__efuts)
                pyapi.decref(pir__zpc)
                pyapi.decref(vbrf__ami)
            with uympa__fdoys:
                df_obj = builder.load(res)
                qzun__fgm = pyapi.object_getattr_string(df_obj, 'index')
                clcne__agey = c.pyapi.call_method(fwtpe__zvb, 'to_pandas',
                    (qzun__fgm,))
                builder.store(clcne__agey, res)
                pyapi.decref(df_obj)
                pyapi.decref(qzun__fgm)
        pyapi.decref(fwtpe__zvb)
    else:
        iuz__kgyzz = [builder.extract_value(dataframe_payload.data, i) for
            i in range(n_cols)]
        ycs__hev = typ.data
        for i, mcoqm__qchp, pcff__mrt in zip(range(n_cols), iuz__kgyzz,
            ycs__hev):
            kzuu__cvmi = cgutils.alloca_once_value(builder, mcoqm__qchp)
            wuwk__txxt = cgutils.alloca_once_value(builder, context.
                get_constant_null(pcff__mrt))
            ahf__yvmrx = builder.not_(is_ll_eq(builder, kzuu__cvmi, wuwk__txxt)
                )
            sow__uvrn = builder.or_(builder.not_(use_parent_obj), builder.
                and_(use_parent_obj, ahf__yvmrx))
            with builder.if_then(sow__uvrn):
                qgv__efuts = pyapi.long_from_longlong(context.get_constant(
                    types.int64, i))
                context.nrt.incref(builder, pcff__mrt, mcoqm__qchp)
                arr_obj = pyapi.from_native_value(pcff__mrt, mcoqm__qchp, c
                    .env_manager)
                df_obj = builder.load(res)
                pyapi.object_setitem(df_obj, qgv__efuts, arr_obj)
                pyapi.decref(arr_obj)
                pyapi.decref(qgv__efuts)
    df_obj = builder.load(res)
    jztag__fltro = _get_df_columns_obj(c, builder, context, pyapi, typ,
        dataframe_payload)
    pyapi.object_setattr_string(df_obj, 'columns', jztag__fltro)
    pyapi.decref(jztag__fltro)
    _set_bodo_meta_dataframe(c, df_obj, typ)
    c.context.nrt.decref(c.builder, typ, val)
    return df_obj


def get_df_obj_column_codegen(context, builder, pyapi, df_obj, col_ind,
    data_typ):
    vbrf__ami = pyapi.borrow_none()
    chkxc__sfmsy = pyapi.unserialize(pyapi.serialize_object(slice))
    atd__olly = pyapi.call_function_objargs(chkxc__sfmsy, [vbrf__ami])
    cmzm__bjtm = pyapi.long_from_longlong(col_ind)
    ows__rehkl = pyapi.tuple_pack([atd__olly, cmzm__bjtm])
    xauh__ucerq = pyapi.object_getattr_string(df_obj, 'iloc')
    lgde__hqc = pyapi.object_getitem(xauh__ucerq, ows__rehkl)
    if isinstance(data_typ, bodo.DatetimeArrayType):
        iaqfu__pnd = pyapi.object_getattr_string(lgde__hqc, 'array')
    else:
        iaqfu__pnd = pyapi.object_getattr_string(lgde__hqc, 'values')
    if isinstance(data_typ, types.Array):
        ghrr__bib = context.insert_const_string(builder.module, 'numpy')
        gwamg__uzso = pyapi.import_module_noblock(ghrr__bib)
        arr_obj = pyapi.call_method(gwamg__uzso, 'ascontiguousarray', (
            iaqfu__pnd,))
        pyapi.decref(iaqfu__pnd)
        pyapi.decref(gwamg__uzso)
    else:
        arr_obj = iaqfu__pnd
    pyapi.decref(chkxc__sfmsy)
    pyapi.decref(atd__olly)
    pyapi.decref(cmzm__bjtm)
    pyapi.decref(ows__rehkl)
    pyapi.decref(xauh__ucerq)
    pyapi.decref(lgde__hqc)
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
        wex__vbmv = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        arr_obj = get_df_obj_column_codegen(context, builder, pyapi,
            wex__vbmv.parent, args[1], data_typ)
        wecdj__kdhk = _unbox_series_data(data_typ.dtype, data_typ, arr_obj, c)
        c.pyapi.decref(arr_obj)
        dataframe_payload = (bodo.hiframes.pd_dataframe_ext.
            get_dataframe_payload(c.context, c.builder, df_typ, args[0]))
        if df_typ.is_table_format:
            lzwrt__dowzk = cgutils.create_struct_proxy(df_typ.table_type)(c
                .context, c.builder, builder.extract_value(
                dataframe_payload.data, 0))
            lvxhm__oni = df_typ.table_type.type_to_blk[data_typ]
            mrbt__ehwy = getattr(lzwrt__dowzk, f'block_{lvxhm__oni}')
            pxn__saoua = ListInstance(c.context, c.builder, types.List(
                data_typ), mrbt__ehwy)
            njpcn__vpn = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[col_ind])
            pxn__saoua.inititem(njpcn__vpn, wecdj__kdhk.value, incref=False)
        else:
            dataframe_payload.data = builder.insert_value(dataframe_payload
                .data, wecdj__kdhk.value, col_ind)
        ksmxc__htz = DataFramePayloadType(df_typ)
        hnz__prui = context.nrt.meminfo_data(builder, wex__vbmv.meminfo)
        vha__ecnsb = context.get_value_type(ksmxc__htz).as_pointer()
        hnz__prui = builder.bitcast(hnz__prui, vha__ecnsb)
        builder.store(dataframe_payload._getvalue(), hnz__prui)
    return signature(types.none, df, i), codegen


@numba.njit
def unbox_col_if_needed(df, i):
    if bodo.hiframes.pd_dataframe_ext.has_parent(df
        ) and bodo.hiframes.pd_dataframe_ext._column_needs_unboxing(df, i):
        bodo.hiframes.boxing.unbox_dataframe_column(df, i)


@unbox(SeriesType)
def unbox_series(typ, val, c):
    if isinstance(typ.data, DatetimeArrayType):
        iaqfu__pnd = c.pyapi.object_getattr_string(val, 'array')
    else:
        iaqfu__pnd = c.pyapi.object_getattr_string(val, 'values')
    if isinstance(typ.data, types.Array):
        ghrr__bib = c.context.insert_const_string(c.builder.module, 'numpy')
        gwamg__uzso = c.pyapi.import_module_noblock(ghrr__bib)
        arr_obj = c.pyapi.call_method(gwamg__uzso, 'ascontiguousarray', (
            iaqfu__pnd,))
        c.pyapi.decref(iaqfu__pnd)
        c.pyapi.decref(gwamg__uzso)
    else:
        arr_obj = iaqfu__pnd
    jexr__kdvr = _unbox_series_data(typ.dtype, typ.data, arr_obj, c).value
    qzun__fgm = c.pyapi.object_getattr_string(val, 'index')
    tjf__erjhr = c.pyapi.to_native_value(typ.index, qzun__fgm).value
    uzp__skw = c.pyapi.object_getattr_string(val, 'name')
    aridr__hcm = c.pyapi.to_native_value(typ.name_typ, uzp__skw).value
    vzkf__cqjja = bodo.hiframes.pd_series_ext.construct_series(c.context, c
        .builder, typ, jexr__kdvr, tjf__erjhr, aridr__hcm)
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(qzun__fgm)
    c.pyapi.decref(uzp__skw)
    return NativeValue(vzkf__cqjja)


def _unbox_series_data(dtype, data_typ, arr_obj, c):
    if data_typ == string_array_split_view_type:
        tilx__fcz = c.context.make_helper(c.builder,
            string_array_split_view_type)
        return NativeValue(tilx__fcz._getvalue())
    return c.pyapi.to_native_value(data_typ, arr_obj)


@box(HeterogeneousSeriesType)
@box(SeriesType)
def box_series(typ, val, c):
    fmcp__ddgk = c.context.insert_const_string(c.builder.module, 'pandas')
    ypwto__lgst = c.pyapi.import_module_noblock(fmcp__ddgk)
    vbks__qhqel = bodo.hiframes.pd_series_ext.get_series_payload(c.context,
        c.builder, typ, val)
    c.context.nrt.incref(c.builder, typ.data, vbks__qhqel.data)
    c.context.nrt.incref(c.builder, typ.index, vbks__qhqel.index)
    c.context.nrt.incref(c.builder, typ.name_typ, vbks__qhqel.name)
    arr_obj = c.pyapi.from_native_value(typ.data, vbks__qhqel.data, c.
        env_manager)
    qzun__fgm = c.pyapi.from_native_value(typ.index, vbks__qhqel.index, c.
        env_manager)
    uzp__skw = c.pyapi.from_native_value(typ.name_typ, vbks__qhqel.name, c.
        env_manager)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        dtype = c.pyapi.unserialize(c.pyapi.serialize_object(object))
    else:
        dtype = c.pyapi.make_none()
    res = c.pyapi.call_method(ypwto__lgst, 'Series', (arr_obj, qzun__fgm,
        dtype, uzp__skw))
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(qzun__fgm)
    c.pyapi.decref(uzp__skw)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        c.pyapi.decref(dtype)
    _set_bodo_meta_series(res, c, typ)
    c.pyapi.decref(ypwto__lgst)
    c.context.nrt.decref(c.builder, typ, val)
    return res


def type_enum_list_to_py_list_obj(pyapi, context, builder, env_manager,
    typ_list):
    sej__ydxqr = []
    for gsvry__rnou in typ_list:
        if isinstance(gsvry__rnou, int) and not isinstance(gsvry__rnou, bool):
            awxbw__umz = pyapi.long_from_longlong(lir.Constant(lir.IntType(
                64), gsvry__rnou))
        else:
            nci__uovur = numba.typeof(gsvry__rnou)
            ckd__yto = context.get_constant_generic(builder, nci__uovur,
                gsvry__rnou)
            awxbw__umz = pyapi.from_native_value(nci__uovur, ckd__yto,
                env_manager)
        sej__ydxqr.append(awxbw__umz)
    xcsos__qrge = pyapi.list_pack(sej__ydxqr)
    for val in sej__ydxqr:
        pyapi.decref(val)
    return xcsos__qrge


def _set_bodo_meta_dataframe(c, obj, typ):
    pyapi = c.pyapi
    context = c.context
    builder = c.builder
    rdoa__bhdtd = not typ.has_runtime_cols and (not typ.is_table_format or 
        len(typ.columns) < TABLE_FORMAT_THRESHOLD)
    kcgr__pclig = 2 if rdoa__bhdtd else 1
    cnf__febqn = pyapi.dict_new(kcgr__pclig)
    zqtxx__dkve = pyapi.long_from_longlong(lir.Constant(lir.IntType(64),
        typ.dist.value))
    pyapi.dict_setitem_string(cnf__febqn, 'dist', zqtxx__dkve)
    pyapi.decref(zqtxx__dkve)
    if rdoa__bhdtd:
        kbwj__lvk = _dtype_to_type_enum_list(typ.index)
        if kbwj__lvk != None:
            pshw__pdvc = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, kbwj__lvk)
        else:
            pshw__pdvc = pyapi.make_none()
        atord__rdd = []
        for dtype in typ.data:
            typ_list = _dtype_to_type_enum_list(dtype)
            if typ_list != None:
                xcsos__qrge = type_enum_list_to_py_list_obj(pyapi, context,
                    builder, c.env_manager, typ_list)
            else:
                xcsos__qrge = pyapi.make_none()
            atord__rdd.append(xcsos__qrge)
        pejy__jumgf = pyapi.list_pack(atord__rdd)
        ilpp__npf = pyapi.list_pack([pshw__pdvc, pejy__jumgf])
        for val in atord__rdd:
            pyapi.decref(val)
        pyapi.dict_setitem_string(cnf__febqn, 'type_metadata', ilpp__npf)
    pyapi.object_setattr_string(obj, '_bodo_meta', cnf__febqn)
    pyapi.decref(cnf__febqn)


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
    cnf__febqn = pyapi.dict_new(2)
    zqtxx__dkve = pyapi.long_from_longlong(lir.Constant(lir.IntType(64),
        typ.dist.value))
    kbwj__lvk = _dtype_to_type_enum_list(typ.index)
    if kbwj__lvk != None:
        pshw__pdvc = type_enum_list_to_py_list_obj(pyapi, context, builder,
            c.env_manager, kbwj__lvk)
    else:
        pshw__pdvc = pyapi.make_none()
    dtype = get_series_dtype_handle_null_int_and_hetrogenous(typ)
    if dtype != None:
        typ_list = _dtype_to_type_enum_list(dtype)
        if typ_list != None:
            polw__wue = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, typ_list)
        else:
            polw__wue = pyapi.make_none()
    else:
        polw__wue = pyapi.make_none()
    ikd__lno = pyapi.list_pack([pshw__pdvc, polw__wue])
    pyapi.dict_setitem_string(cnf__febqn, 'type_metadata', ikd__lno)
    pyapi.decref(ikd__lno)
    pyapi.dict_setitem_string(cnf__febqn, 'dist', zqtxx__dkve)
    pyapi.object_setattr_string(obj, '_bodo_meta', cnf__febqn)
    pyapi.decref(cnf__febqn)
    pyapi.decref(zqtxx__dkve)


@typeof_impl.register(np.ndarray)
def _typeof_ndarray(val, c):
    try:
        dtype = numba.np.numpy_support.from_dtype(val.dtype)
    except NotImplementedError as kdz__utkg:
        dtype = types.pyobject
    if dtype == types.pyobject:
        return _infer_ndarray_obj_dtype(val)
    ktvb__qswfs = numba.np.numpy_support.map_layout(val)
    tqx__kah = not val.flags.writeable
    return types.Array(dtype, val.ndim, ktvb__qswfs, readonly=tqx__kah)


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
    aaqky__truy = val[i]
    if isinstance(aaqky__truy, str):
        return (bodo.dict_str_arr_type if _use_dict_str_type else
            string_array_type)
    elif isinstance(aaqky__truy, bytes):
        return binary_array_type
    elif isinstance(aaqky__truy, bool):
        return bodo.libs.bool_arr_ext.boolean_array
    elif isinstance(aaqky__truy, (int, np.int8, np.int16, np.int32, np.
        int64, np.uint8, np.uint16, np.uint32, np.uint64)):
        return bodo.libs.int_arr_ext.IntegerArrayType(numba.typeof(aaqky__truy)
            )
    elif isinstance(aaqky__truy, (dict, Dict)) and all(isinstance(
        sxn__uahrl, str) for sxn__uahrl in aaqky__truy.keys()):
        qktvx__kgvpg = tuple(aaqky__truy.keys())
        evh__cgy = tuple(_get_struct_value_arr_type(v) for v in aaqky__truy
            .values())
        return StructArrayType(evh__cgy, qktvx__kgvpg)
    elif isinstance(aaqky__truy, (dict, Dict)):
        uuloa__aevtf = numba.typeof(_value_to_array(list(aaqky__truy.keys())))
        zis__cgwjs = numba.typeof(_value_to_array(list(aaqky__truy.values())))
        uuloa__aevtf = to_str_arr_if_dict_array(uuloa__aevtf)
        zis__cgwjs = to_str_arr_if_dict_array(zis__cgwjs)
        return MapArrayType(uuloa__aevtf, zis__cgwjs)
    elif isinstance(aaqky__truy, tuple):
        evh__cgy = tuple(_get_struct_value_arr_type(v) for v in aaqky__truy)
        return TupleArrayType(evh__cgy)
    if isinstance(aaqky__truy, (list, np.ndarray, pd.arrays.BooleanArray,
        pd.arrays.IntegerArray, pd.arrays.StringArray)):
        if isinstance(aaqky__truy, list):
            aaqky__truy = _value_to_array(aaqky__truy)
        igsb__wobu = numba.typeof(aaqky__truy)
        igsb__wobu = to_str_arr_if_dict_array(igsb__wobu)
        return ArrayItemArrayType(igsb__wobu)
    if isinstance(aaqky__truy, datetime.date):
        return datetime_date_array_type
    if isinstance(aaqky__truy, datetime.timedelta):
        return datetime_timedelta_array_type
    if isinstance(aaqky__truy, decimal.Decimal):
        return DecimalArrayType(38, 18)
    raise BodoError(f'Unsupported object array with first value: {aaqky__truy}'
        )


def _value_to_array(val):
    assert isinstance(val, (list, dict, Dict))
    if isinstance(val, (dict, Dict)):
        val = dict(val)
        return np.array([val], np.object_)
    nalap__ijtkn = val.copy()
    nalap__ijtkn.append(None)
    mcoqm__qchp = np.array(nalap__ijtkn, np.object_)
    if len(val) and isinstance(val[0], float):
        mcoqm__qchp = np.array(val, np.float64)
    return mcoqm__qchp


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
    pcff__mrt = dtype_to_array_type(numba.typeof(v))
    if isinstance(v, (int, bool)):
        pcff__mrt = to_nullable_type(pcff__mrt)
    return pcff__mrt
