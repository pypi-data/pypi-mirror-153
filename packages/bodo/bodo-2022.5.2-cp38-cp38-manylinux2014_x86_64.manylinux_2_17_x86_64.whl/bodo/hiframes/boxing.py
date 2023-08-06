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
    hrfa__gjc = tuple(val.columns.to_list())
    zuat__tqi = get_hiframes_dtypes(val)
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and len(val._bodo_meta['type_metadata'
        ][1]) == len(val.columns) and val._bodo_meta['type_metadata'][0] is not
        None):
        qylvq__oaz = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        qylvq__oaz = numba.typeof(val.index)
    vya__npu = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    fsh__atk = len(zuat__tqi) >= TABLE_FORMAT_THRESHOLD
    return DataFrameType(zuat__tqi, qylvq__oaz, hrfa__gjc, vya__npu,
        is_table_format=fsh__atk)


@typeof_impl.register(pd.Series)
def typeof_pd_series(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    vya__npu = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and val._bodo_meta['type_metadata'][0]
         is not None):
        rfeo__neymb = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        rfeo__neymb = numba.typeof(val.index)
    dtype = _infer_series_dtype(val)
    gmbc__nwbad = dtype_to_array_type(dtype)
    if _use_dict_str_type and gmbc__nwbad == string_array_type:
        gmbc__nwbad = bodo.dict_str_arr_type
    return SeriesType(dtype, data=gmbc__nwbad, index=rfeo__neymb, name_typ=
        numba.typeof(val.name), dist=vya__npu)


@unbox(DataFrameType)
def unbox_dataframe(typ, val, c):
    check_runtime_cols_unsupported(typ, 'Unboxing')
    cio__dnhtc = c.pyapi.object_getattr_string(val, 'index')
    kpubq__fxfl = c.pyapi.to_native_value(typ.index, cio__dnhtc).value
    c.pyapi.decref(cio__dnhtc)
    if typ.is_table_format:
        gfjc__bgmrz = cgutils.create_struct_proxy(typ.table_type)(c.context,
            c.builder)
        gfjc__bgmrz.parent = val
        for kzi__kji, qngoj__yle in typ.table_type.type_to_blk.items():
            gngv__gyni = c.context.get_constant(types.int64, len(typ.
                table_type.block_to_arr_ind[qngoj__yle]))
            kjj__eyyrc, wlzy__wbn = ListInstance.allocate_ex(c.context, c.
                builder, types.List(kzi__kji), gngv__gyni)
            wlzy__wbn.size = gngv__gyni
            setattr(gfjc__bgmrz, f'block_{qngoj__yle}', wlzy__wbn.value)
        wfcxf__uzylb = c.pyapi.call_method(val, '__len__', ())
        gwrax__oqcy = c.pyapi.long_as_longlong(wfcxf__uzylb)
        c.pyapi.decref(wfcxf__uzylb)
        gfjc__bgmrz.len = gwrax__oqcy
        pozg__umai = c.context.make_tuple(c.builder, types.Tuple([typ.
            table_type]), [gfjc__bgmrz._getvalue()])
    else:
        yiath__xsiu = [c.context.get_constant_null(kzi__kji) for kzi__kji in
            typ.data]
        pozg__umai = c.context.make_tuple(c.builder, types.Tuple(typ.data),
            yiath__xsiu)
    acql__ztmf = construct_dataframe(c.context, c.builder, typ, pozg__umai,
        kpubq__fxfl, val, None)
    return NativeValue(acql__ztmf)


def get_hiframes_dtypes(df):
    if (hasattr(df, '_bodo_meta') and df._bodo_meta is not None and 
        'type_metadata' in df._bodo_meta and df._bodo_meta['type_metadata']
         is not None and len(df._bodo_meta['type_metadata'][1]) == len(df.
        columns)):
        dgjy__tziu = df._bodo_meta['type_metadata'][1]
    else:
        dgjy__tziu = [None] * len(df.columns)
    xprcc__osv = [dtype_to_array_type(_infer_series_dtype(df.iloc[:, i],
        array_metadata=dgjy__tziu[i])) for i in range(len(df.columns))]
    xprcc__osv = [(bodo.dict_str_arr_type if _use_dict_str_type and 
        kzi__kji == string_array_type else kzi__kji) for kzi__kji in xprcc__osv
        ]
    return tuple(xprcc__osv)


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
    njw__rzu, typ = _dtype_from_type_enum_list_recursor(typ_enum_list)
    if len(njw__rzu) != 0:
        raise_bodo_error(
            f"""Unexpected Internal Error while converting typing metadata: Dtype list was not fully consumed.
 Input typ_enum_list: {typ_enum_list}.
Remainder: {njw__rzu}. Please file the error here: https://github.com/Bodo-inc/Feedback"""
            )
    return typ


def _dtype_from_type_enum_list_recursor(typ_enum_list):
    if len(typ_enum_list) == 0:
        raise_bodo_error('Unable to infer dtype from empty typ_enum_list')
    elif typ_enum_list[0] in _one_to_one_enum_to_type_map:
        return typ_enum_list[1:], _one_to_one_enum_to_type_map[typ_enum_list[0]
            ]
    elif typ_enum_list[0] == SeriesDtypeEnum.IntegerArray.value:
        uhjy__ulrk, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:]
            )
        return uhjy__ulrk, IntegerArrayType(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.ARRAY.value:
        uhjy__ulrk, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:]
            )
        return uhjy__ulrk, dtype_to_array_type(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.Decimal.value:
        klmyx__qtqu = typ_enum_list[1]
        bnpo__ubi = typ_enum_list[2]
        return typ_enum_list[3:], Decimal128Type(klmyx__qtqu, bnpo__ubi)
    elif typ_enum_list[0] == SeriesDtypeEnum.STRUCT.value:
        pdq__rdpd = typ_enum_list[1]
        keie__wauir = tuple(typ_enum_list[2:2 + pdq__rdpd])
        urk__nvps = typ_enum_list[2 + pdq__rdpd:]
        ommln__hnwh = []
        for i in range(pdq__rdpd):
            urk__nvps, uaw__ypwo = _dtype_from_type_enum_list_recursor(
                urk__nvps)
            ommln__hnwh.append(uaw__ypwo)
        return urk__nvps, StructType(tuple(ommln__hnwh), keie__wauir)
    elif typ_enum_list[0] == SeriesDtypeEnum.Literal.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'Literal' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        bnx__mpcnj = typ_enum_list[1]
        urk__nvps = typ_enum_list[2:]
        return urk__nvps, bnx__mpcnj
    elif typ_enum_list[0] == SeriesDtypeEnum.LiteralType.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'LiteralType' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        bnx__mpcnj = typ_enum_list[1]
        urk__nvps = typ_enum_list[2:]
        return urk__nvps, numba.types.literal(bnx__mpcnj)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalType.value:
        urk__nvps, ssqss__jxlm = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        urk__nvps, iqepc__msub = _dtype_from_type_enum_list_recursor(urk__nvps)
        urk__nvps, ojv__tecw = _dtype_from_type_enum_list_recursor(urk__nvps)
        urk__nvps, nrlry__odj = _dtype_from_type_enum_list_recursor(urk__nvps)
        urk__nvps, iflr__mkoeo = _dtype_from_type_enum_list_recursor(urk__nvps)
        return urk__nvps, PDCategoricalDtype(ssqss__jxlm, iqepc__msub,
            ojv__tecw, nrlry__odj, iflr__mkoeo)
    elif typ_enum_list[0] == SeriesDtypeEnum.DatetimeIndexType.value:
        urk__nvps, wufq__xrkyt = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return urk__nvps, DatetimeIndexType(wufq__xrkyt)
    elif typ_enum_list[0] == SeriesDtypeEnum.NumericIndexType.value:
        urk__nvps, dtype = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        urk__nvps, wufq__xrkyt = _dtype_from_type_enum_list_recursor(urk__nvps)
        urk__nvps, nrlry__odj = _dtype_from_type_enum_list_recursor(urk__nvps)
        return urk__nvps, NumericIndexType(dtype, wufq__xrkyt, nrlry__odj)
    elif typ_enum_list[0] == SeriesDtypeEnum.PeriodIndexType.value:
        urk__nvps, zvvhe__fkg = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        urk__nvps, wufq__xrkyt = _dtype_from_type_enum_list_recursor(urk__nvps)
        return urk__nvps, PeriodIndexType(zvvhe__fkg, wufq__xrkyt)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalIndexType.value:
        urk__nvps, nrlry__odj = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        urk__nvps, wufq__xrkyt = _dtype_from_type_enum_list_recursor(urk__nvps)
        return urk__nvps, CategoricalIndexType(nrlry__odj, wufq__xrkyt)
    elif typ_enum_list[0] == SeriesDtypeEnum.RangeIndexType.value:
        urk__nvps, wufq__xrkyt = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return urk__nvps, RangeIndexType(wufq__xrkyt)
    elif typ_enum_list[0] == SeriesDtypeEnum.StringIndexType.value:
        urk__nvps, wufq__xrkyt = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return urk__nvps, StringIndexType(wufq__xrkyt)
    elif typ_enum_list[0] == SeriesDtypeEnum.BinaryIndexType.value:
        urk__nvps, wufq__xrkyt = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return urk__nvps, BinaryIndexType(wufq__xrkyt)
    elif typ_enum_list[0] == SeriesDtypeEnum.TimedeltaIndexType.value:
        urk__nvps, wufq__xrkyt = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return urk__nvps, TimedeltaIndexType(wufq__xrkyt)
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
        dsot__hzzmy = get_overload_const_int(typ)
        if numba.types.maybe_literal(dsot__hzzmy) == typ:
            return [SeriesDtypeEnum.LiteralType.value, dsot__hzzmy]
    elif is_overload_constant_str(typ):
        dsot__hzzmy = get_overload_const_str(typ)
        if numba.types.maybe_literal(dsot__hzzmy) == typ:
            return [SeriesDtypeEnum.LiteralType.value, dsot__hzzmy]
    elif is_overload_constant_bool(typ):
        dsot__hzzmy = get_overload_const_bool(typ)
        if numba.types.maybe_literal(dsot__hzzmy) == typ:
            return [SeriesDtypeEnum.LiteralType.value, dsot__hzzmy]
    elif isinstance(typ, IntegerArrayType):
        return [SeriesDtypeEnum.IntegerArray.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif bodo.utils.utils.is_array_typ(typ, False):
        return [SeriesDtypeEnum.ARRAY.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif isinstance(typ, StructType):
        efn__pxvg = [SeriesDtypeEnum.STRUCT.value, len(typ.names)]
        for jfdz__tgl in typ.names:
            efn__pxvg.append(jfdz__tgl)
        for yur__rmxja in typ.data:
            efn__pxvg += _dtype_to_type_enum_list_recursor(yur__rmxja)
        return efn__pxvg
    elif isinstance(typ, bodo.libs.decimal_arr_ext.Decimal128Type):
        return [SeriesDtypeEnum.Decimal.value, typ.precision, typ.scale]
    elif isinstance(typ, PDCategoricalDtype):
        hbfh__hgiqa = _dtype_to_type_enum_list_recursor(typ.categories)
        rggy__mgdf = _dtype_to_type_enum_list_recursor(typ.elem_type)
        kwm__zbir = _dtype_to_type_enum_list_recursor(typ.ordered)
        uiyc__zhuk = _dtype_to_type_enum_list_recursor(typ.data)
        rhhwe__jnzq = _dtype_to_type_enum_list_recursor(typ.int_type)
        return [SeriesDtypeEnum.CategoricalType.value
            ] + hbfh__hgiqa + rggy__mgdf + kwm__zbir + uiyc__zhuk + rhhwe__jnzq
    elif isinstance(typ, DatetimeIndexType):
        return [SeriesDtypeEnum.DatetimeIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, NumericIndexType):
        if upcast_numeric_index:
            if isinstance(typ.dtype, types.Float):
                aeoey__mvj = types.float64
                frt__efo = types.Array(aeoey__mvj, 1, 'C')
            elif typ.dtype in {types.int8, types.int16, types.int32, types.
                int64}:
                aeoey__mvj = types.int64
                if isinstance(typ.data, IntegerArrayType):
                    frt__efo = IntegerArrayType(aeoey__mvj)
                else:
                    frt__efo = types.Array(aeoey__mvj, 1, 'C')
            elif typ.dtype in {types.uint8, types.uint16, types.uint32,
                types.uint64}:
                aeoey__mvj = types.uint64
                if isinstance(typ.data, IntegerArrayType):
                    frt__efo = IntegerArrayType(aeoey__mvj)
                else:
                    frt__efo = types.Array(aeoey__mvj, 1, 'C')
            elif typ.dtype == types.bool_:
                aeoey__mvj = typ.dtype
                frt__efo = typ.data
            else:
                raise GuardException('Unable to convert type')
            return [SeriesDtypeEnum.NumericIndexType.value
                ] + _dtype_to_type_enum_list_recursor(aeoey__mvj
                ) + _dtype_to_type_enum_list_recursor(typ.name_typ
                ) + _dtype_to_type_enum_list_recursor(frt__efo)
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
                eqmjv__vgm = S._bodo_meta['type_metadata'][1]
                return _dtype_from_type_enum_list(eqmjv__vgm)
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
        glxt__vwgv = S.dtype.unit
        if glxt__vwgv != 'ns':
            raise BodoError("Timezone-aware datetime data requires 'ns' units")
        elbp__pok = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(S.dtype.tz
            )
        return PandasDatetimeTZDtype(elbp__pok)
    try:
        return numpy_support.from_dtype(S.dtype)
    except:
        raise BodoError(
            f'data type {S.dtype} for column {S.name} not supported yet')


def _get_use_df_parent_obj_flag(builder, context, pyapi, parent_obj, n_cols):
    if n_cols is None:
        return context.get_constant(types.bool_, False)
    oqbgm__gxnnf = cgutils.is_not_null(builder, parent_obj)
    nan__yaa = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with builder.if_then(oqbgm__gxnnf):
        ftjt__bxn = pyapi.object_getattr_string(parent_obj, 'columns')
        wfcxf__uzylb = pyapi.call_method(ftjt__bxn, '__len__', ())
        builder.store(pyapi.long_as_longlong(wfcxf__uzylb), nan__yaa)
        pyapi.decref(wfcxf__uzylb)
        pyapi.decref(ftjt__bxn)
    use_parent_obj = builder.and_(oqbgm__gxnnf, builder.icmp_unsigned('==',
        builder.load(nan__yaa), context.get_constant(types.int64, n_cols)))
    return use_parent_obj


def _get_df_columns_obj(c, builder, context, pyapi, df_typ, dataframe_payload):
    if df_typ.has_runtime_cols:
        nlhx__qvzc = df_typ.runtime_colname_typ
        context.nrt.incref(builder, nlhx__qvzc, dataframe_payload.columns)
        return pyapi.from_native_value(nlhx__qvzc, dataframe_payload.
            columns, c.env_manager)
    if all(isinstance(c, int) for c in df_typ.columns):
        iteu__sma = np.array(df_typ.columns, 'int64')
    elif all(isinstance(c, str) for c in df_typ.columns):
        iteu__sma = pd.array(df_typ.columns, 'string')
    else:
        iteu__sma = df_typ.columns
    kjogr__bvral = numba.typeof(iteu__sma)
    qzk__xcj = context.get_constant_generic(builder, kjogr__bvral, iteu__sma)
    lks__ehbw = pyapi.from_native_value(kjogr__bvral, qzk__xcj, c.env_manager)
    return lks__ehbw


def _create_initial_df_object(builder, context, pyapi, c, df_typ, obj,
    dataframe_payload, res, use_parent_obj):
    with c.builder.if_else(use_parent_obj) as (jolc__uhk, bju__hnpjc):
        with jolc__uhk:
            pyapi.incref(obj)
            kphc__dwlx = context.insert_const_string(c.builder.module, 'numpy')
            nkpi__pslm = pyapi.import_module_noblock(kphc__dwlx)
            if df_typ.has_runtime_cols:
                aakl__rehe = 0
            else:
                aakl__rehe = len(df_typ.columns)
            pil__thp = pyapi.long_from_longlong(lir.Constant(lir.IntType(64
                ), aakl__rehe))
            ptahq__vvjb = pyapi.call_method(nkpi__pslm, 'arange', (pil__thp,))
            pyapi.object_setattr_string(obj, 'columns', ptahq__vvjb)
            pyapi.decref(nkpi__pslm)
            pyapi.decref(ptahq__vvjb)
            pyapi.decref(pil__thp)
        with bju__hnpjc:
            context.nrt.incref(builder, df_typ.index, dataframe_payload.index)
            tzwkm__xqxvy = c.pyapi.from_native_value(df_typ.index,
                dataframe_payload.index, c.env_manager)
            kphc__dwlx = context.insert_const_string(c.builder.module, 'pandas'
                )
            nkpi__pslm = pyapi.import_module_noblock(kphc__dwlx)
            df_obj = pyapi.call_method(nkpi__pslm, 'DataFrame', (pyapi.
                borrow_none(), tzwkm__xqxvy))
            pyapi.decref(nkpi__pslm)
            pyapi.decref(tzwkm__xqxvy)
            builder.store(df_obj, res)


@box(DataFrameType)
def box_dataframe(typ, val, c):
    from bodo.hiframes.table import box_table
    context = c.context
    builder = c.builder
    pyapi = c.pyapi
    dataframe_payload = bodo.hiframes.pd_dataframe_ext.get_dataframe_payload(c
        .context, c.builder, typ, val)
    hpf__hjn = cgutils.create_struct_proxy(typ)(context, builder, value=val)
    n_cols = len(typ.columns) if not typ.has_runtime_cols else None
    obj = hpf__hjn.parent
    res = cgutils.alloca_once_value(builder, obj)
    use_parent_obj = _get_use_df_parent_obj_flag(builder, context, pyapi,
        obj, n_cols)
    _create_initial_df_object(builder, context, pyapi, c, typ, obj,
        dataframe_payload, res, use_parent_obj)
    if typ.is_table_format:
        iobjx__gjmpz = typ.table_type
        gfjc__bgmrz = builder.extract_value(dataframe_payload.data, 0)
        context.nrt.incref(builder, iobjx__gjmpz, gfjc__bgmrz)
        sbmh__vlc = box_table(iobjx__gjmpz, gfjc__bgmrz, c, builder.not_(
            use_parent_obj))
        with builder.if_else(use_parent_obj) as (eewvb__cyp, dzgp__kcu):
            with eewvb__cyp:
                rycdh__fjz = pyapi.object_getattr_string(sbmh__vlc, 'arrays')
                qquey__dhmrv = c.pyapi.make_none()
                if n_cols is None:
                    wfcxf__uzylb = pyapi.call_method(rycdh__fjz, '__len__', ())
                    gngv__gyni = pyapi.long_as_longlong(wfcxf__uzylb)
                    pyapi.decref(wfcxf__uzylb)
                else:
                    gngv__gyni = context.get_constant(types.int64, n_cols)
                with cgutils.for_range(builder, gngv__gyni) as baj__ccd:
                    i = baj__ccd.index
                    ifmd__bpcp = pyapi.list_getitem(rycdh__fjz, i)
                    okeb__rtz = c.builder.icmp_unsigned('!=', ifmd__bpcp,
                        qquey__dhmrv)
                    with builder.if_then(okeb__rtz):
                        qfzv__zzzc = pyapi.long_from_longlong(i)
                        df_obj = builder.load(res)
                        pyapi.object_setitem(df_obj, qfzv__zzzc, ifmd__bpcp)
                        pyapi.decref(qfzv__zzzc)
                pyapi.decref(rycdh__fjz)
                pyapi.decref(qquey__dhmrv)
            with dzgp__kcu:
                df_obj = builder.load(res)
                tzwkm__xqxvy = pyapi.object_getattr_string(df_obj, 'index')
                ake__cuoi = c.pyapi.call_method(sbmh__vlc, 'to_pandas', (
                    tzwkm__xqxvy,))
                builder.store(ake__cuoi, res)
                pyapi.decref(df_obj)
                pyapi.decref(tzwkm__xqxvy)
        pyapi.decref(sbmh__vlc)
    else:
        ycb__xfp = [builder.extract_value(dataframe_payload.data, i) for i in
            range(n_cols)]
        qpe__swoye = typ.data
        for i, kebv__zphl, gmbc__nwbad in zip(range(n_cols), ycb__xfp,
            qpe__swoye):
            zjjc__ypjj = cgutils.alloca_once_value(builder, kebv__zphl)
            hywm__wzw = cgutils.alloca_once_value(builder, context.
                get_constant_null(gmbc__nwbad))
            okeb__rtz = builder.not_(is_ll_eq(builder, zjjc__ypjj, hywm__wzw))
            uwb__apxte = builder.or_(builder.not_(use_parent_obj), builder.
                and_(use_parent_obj, okeb__rtz))
            with builder.if_then(uwb__apxte):
                qfzv__zzzc = pyapi.long_from_longlong(context.get_constant(
                    types.int64, i))
                context.nrt.incref(builder, gmbc__nwbad, kebv__zphl)
                arr_obj = pyapi.from_native_value(gmbc__nwbad, kebv__zphl,
                    c.env_manager)
                df_obj = builder.load(res)
                pyapi.object_setitem(df_obj, qfzv__zzzc, arr_obj)
                pyapi.decref(arr_obj)
                pyapi.decref(qfzv__zzzc)
    df_obj = builder.load(res)
    lks__ehbw = _get_df_columns_obj(c, builder, context, pyapi, typ,
        dataframe_payload)
    pyapi.object_setattr_string(df_obj, 'columns', lks__ehbw)
    pyapi.decref(lks__ehbw)
    _set_bodo_meta_dataframe(c, df_obj, typ)
    c.context.nrt.decref(c.builder, typ, val)
    return df_obj


def get_df_obj_column_codegen(context, builder, pyapi, df_obj, col_ind,
    data_typ):
    qquey__dhmrv = pyapi.borrow_none()
    rgm__cltxh = pyapi.unserialize(pyapi.serialize_object(slice))
    klvjn__unok = pyapi.call_function_objargs(rgm__cltxh, [qquey__dhmrv])
    froe__brf = pyapi.long_from_longlong(col_ind)
    rptoz__gqg = pyapi.tuple_pack([klvjn__unok, froe__brf])
    gua__jxywb = pyapi.object_getattr_string(df_obj, 'iloc')
    zugu__bvy = pyapi.object_getitem(gua__jxywb, rptoz__gqg)
    if isinstance(data_typ, bodo.DatetimeArrayType):
        gewxj__ngoki = pyapi.object_getattr_string(zugu__bvy, 'array')
    else:
        gewxj__ngoki = pyapi.object_getattr_string(zugu__bvy, 'values')
    if isinstance(data_typ, types.Array):
        niu__gfoe = context.insert_const_string(builder.module, 'numpy')
        iaw__nqjjc = pyapi.import_module_noblock(niu__gfoe)
        arr_obj = pyapi.call_method(iaw__nqjjc, 'ascontiguousarray', (
            gewxj__ngoki,))
        pyapi.decref(gewxj__ngoki)
        pyapi.decref(iaw__nqjjc)
    else:
        arr_obj = gewxj__ngoki
    pyapi.decref(rgm__cltxh)
    pyapi.decref(klvjn__unok)
    pyapi.decref(froe__brf)
    pyapi.decref(rptoz__gqg)
    pyapi.decref(gua__jxywb)
    pyapi.decref(zugu__bvy)
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
        hpf__hjn = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        arr_obj = get_df_obj_column_codegen(context, builder, pyapi,
            hpf__hjn.parent, args[1], data_typ)
        ajqqj__wlrce = _unbox_series_data(data_typ.dtype, data_typ, arr_obj, c)
        c.pyapi.decref(arr_obj)
        dataframe_payload = (bodo.hiframes.pd_dataframe_ext.
            get_dataframe_payload(c.context, c.builder, df_typ, args[0]))
        if df_typ.is_table_format:
            gfjc__bgmrz = cgutils.create_struct_proxy(df_typ.table_type)(c.
                context, c.builder, builder.extract_value(dataframe_payload
                .data, 0))
            qngoj__yle = df_typ.table_type.type_to_blk[data_typ]
            kgj__twuxj = getattr(gfjc__bgmrz, f'block_{qngoj__yle}')
            ppy__gufbk = ListInstance(c.context, c.builder, types.List(
                data_typ), kgj__twuxj)
            iwji__ibicy = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[col_ind])
            ppy__gufbk.inititem(iwji__ibicy, ajqqj__wlrce.value, incref=False)
        else:
            dataframe_payload.data = builder.insert_value(dataframe_payload
                .data, ajqqj__wlrce.value, col_ind)
        lvjmg__ehcmq = DataFramePayloadType(df_typ)
        vdhnd__gtp = context.nrt.meminfo_data(builder, hpf__hjn.meminfo)
        iaoze__muza = context.get_value_type(lvjmg__ehcmq).as_pointer()
        vdhnd__gtp = builder.bitcast(vdhnd__gtp, iaoze__muza)
        builder.store(dataframe_payload._getvalue(), vdhnd__gtp)
    return signature(types.none, df, i), codegen


@numba.njit
def unbox_col_if_needed(df, i):
    if bodo.hiframes.pd_dataframe_ext.has_parent(df
        ) and bodo.hiframes.pd_dataframe_ext._column_needs_unboxing(df, i):
        bodo.hiframes.boxing.unbox_dataframe_column(df, i)


@unbox(SeriesType)
def unbox_series(typ, val, c):
    if isinstance(typ.data, DatetimeArrayType):
        gewxj__ngoki = c.pyapi.object_getattr_string(val, 'array')
    else:
        gewxj__ngoki = c.pyapi.object_getattr_string(val, 'values')
    if isinstance(typ.data, types.Array):
        niu__gfoe = c.context.insert_const_string(c.builder.module, 'numpy')
        iaw__nqjjc = c.pyapi.import_module_noblock(niu__gfoe)
        arr_obj = c.pyapi.call_method(iaw__nqjjc, 'ascontiguousarray', (
            gewxj__ngoki,))
        c.pyapi.decref(gewxj__ngoki)
        c.pyapi.decref(iaw__nqjjc)
    else:
        arr_obj = gewxj__ngoki
    kpd__wvx = _unbox_series_data(typ.dtype, typ.data, arr_obj, c).value
    tzwkm__xqxvy = c.pyapi.object_getattr_string(val, 'index')
    kpubq__fxfl = c.pyapi.to_native_value(typ.index, tzwkm__xqxvy).value
    imdnd__ygc = c.pyapi.object_getattr_string(val, 'name')
    sec__ryqkt = c.pyapi.to_native_value(typ.name_typ, imdnd__ygc).value
    pani__gyr = bodo.hiframes.pd_series_ext.construct_series(c.context, c.
        builder, typ, kpd__wvx, kpubq__fxfl, sec__ryqkt)
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(tzwkm__xqxvy)
    c.pyapi.decref(imdnd__ygc)
    return NativeValue(pani__gyr)


def _unbox_series_data(dtype, data_typ, arr_obj, c):
    if data_typ == string_array_split_view_type:
        ubpz__ecr = c.context.make_helper(c.builder,
            string_array_split_view_type)
        return NativeValue(ubpz__ecr._getvalue())
    return c.pyapi.to_native_value(data_typ, arr_obj)


@box(HeterogeneousSeriesType)
@box(SeriesType)
def box_series(typ, val, c):
    kphc__dwlx = c.context.insert_const_string(c.builder.module, 'pandas')
    jljwz__oowi = c.pyapi.import_module_noblock(kphc__dwlx)
    ogaid__cya = bodo.hiframes.pd_series_ext.get_series_payload(c.context,
        c.builder, typ, val)
    c.context.nrt.incref(c.builder, typ.data, ogaid__cya.data)
    c.context.nrt.incref(c.builder, typ.index, ogaid__cya.index)
    c.context.nrt.incref(c.builder, typ.name_typ, ogaid__cya.name)
    arr_obj = c.pyapi.from_native_value(typ.data, ogaid__cya.data, c.
        env_manager)
    tzwkm__xqxvy = c.pyapi.from_native_value(typ.index, ogaid__cya.index, c
        .env_manager)
    imdnd__ygc = c.pyapi.from_native_value(typ.name_typ, ogaid__cya.name, c
        .env_manager)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        dtype = c.pyapi.unserialize(c.pyapi.serialize_object(object))
    else:
        dtype = c.pyapi.make_none()
    res = c.pyapi.call_method(jljwz__oowi, 'Series', (arr_obj, tzwkm__xqxvy,
        dtype, imdnd__ygc))
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(tzwkm__xqxvy)
    c.pyapi.decref(imdnd__ygc)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        c.pyapi.decref(dtype)
    _set_bodo_meta_series(res, c, typ)
    c.pyapi.decref(jljwz__oowi)
    c.context.nrt.decref(c.builder, typ, val)
    return res


def type_enum_list_to_py_list_obj(pyapi, context, builder, env_manager,
    typ_list):
    sqvqu__moiy = []
    for seju__eokt in typ_list:
        if isinstance(seju__eokt, int) and not isinstance(seju__eokt, bool):
            xmpqc__zbk = pyapi.long_from_longlong(lir.Constant(lir.IntType(
                64), seju__eokt))
        else:
            qfx__jvkyo = numba.typeof(seju__eokt)
            erekr__glkbj = context.get_constant_generic(builder, qfx__jvkyo,
                seju__eokt)
            xmpqc__zbk = pyapi.from_native_value(qfx__jvkyo, erekr__glkbj,
                env_manager)
        sqvqu__moiy.append(xmpqc__zbk)
    nfq__fqbhi = pyapi.list_pack(sqvqu__moiy)
    for val in sqvqu__moiy:
        pyapi.decref(val)
    return nfq__fqbhi


def _set_bodo_meta_dataframe(c, obj, typ):
    pyapi = c.pyapi
    context = c.context
    builder = c.builder
    acd__jqc = not typ.has_runtime_cols and (not typ.is_table_format or len
        (typ.columns) < TABLE_FORMAT_THRESHOLD)
    zjs__xbqq = 2 if acd__jqc else 1
    drr__prbx = pyapi.dict_new(zjs__xbqq)
    hoan__nbn = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ.
        dist.value))
    pyapi.dict_setitem_string(drr__prbx, 'dist', hoan__nbn)
    pyapi.decref(hoan__nbn)
    if acd__jqc:
        xct__sitn = _dtype_to_type_enum_list(typ.index)
        if xct__sitn != None:
            hjwbe__lfvp = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, xct__sitn)
        else:
            hjwbe__lfvp = pyapi.make_none()
        ing__sxnzg = []
        for dtype in typ.data:
            typ_list = _dtype_to_type_enum_list(dtype)
            if typ_list != None:
                nfq__fqbhi = type_enum_list_to_py_list_obj(pyapi, context,
                    builder, c.env_manager, typ_list)
            else:
                nfq__fqbhi = pyapi.make_none()
            ing__sxnzg.append(nfq__fqbhi)
        bryj__ulike = pyapi.list_pack(ing__sxnzg)
        twhh__vcj = pyapi.list_pack([hjwbe__lfvp, bryj__ulike])
        for val in ing__sxnzg:
            pyapi.decref(val)
        pyapi.dict_setitem_string(drr__prbx, 'type_metadata', twhh__vcj)
    pyapi.object_setattr_string(obj, '_bodo_meta', drr__prbx)
    pyapi.decref(drr__prbx)


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
    drr__prbx = pyapi.dict_new(2)
    hoan__nbn = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ.
        dist.value))
    xct__sitn = _dtype_to_type_enum_list(typ.index)
    if xct__sitn != None:
        hjwbe__lfvp = type_enum_list_to_py_list_obj(pyapi, context, builder,
            c.env_manager, xct__sitn)
    else:
        hjwbe__lfvp = pyapi.make_none()
    dtype = get_series_dtype_handle_null_int_and_hetrogenous(typ)
    if dtype != None:
        typ_list = _dtype_to_type_enum_list(dtype)
        if typ_list != None:
            engqv__fen = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, typ_list)
        else:
            engqv__fen = pyapi.make_none()
    else:
        engqv__fen = pyapi.make_none()
    yzp__xqz = pyapi.list_pack([hjwbe__lfvp, engqv__fen])
    pyapi.dict_setitem_string(drr__prbx, 'type_metadata', yzp__xqz)
    pyapi.decref(yzp__xqz)
    pyapi.dict_setitem_string(drr__prbx, 'dist', hoan__nbn)
    pyapi.object_setattr_string(obj, '_bodo_meta', drr__prbx)
    pyapi.decref(drr__prbx)
    pyapi.decref(hoan__nbn)


@typeof_impl.register(np.ndarray)
def _typeof_ndarray(val, c):
    try:
        dtype = numba.np.numpy_support.from_dtype(val.dtype)
    except NotImplementedError as ibadi__zoxtg:
        dtype = types.pyobject
    if dtype == types.pyobject:
        return _infer_ndarray_obj_dtype(val)
    jvwjd__rral = numba.np.numpy_support.map_layout(val)
    rpna__zagqt = not val.flags.writeable
    return types.Array(dtype, val.ndim, jvwjd__rral, readonly=rpna__zagqt)


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
    lwa__rcg = val[i]
    if isinstance(lwa__rcg, str):
        return (bodo.dict_str_arr_type if _use_dict_str_type else
            string_array_type)
    elif isinstance(lwa__rcg, bytes):
        return binary_array_type
    elif isinstance(lwa__rcg, bool):
        return bodo.libs.bool_arr_ext.boolean_array
    elif isinstance(lwa__rcg, (int, np.int8, np.int16, np.int32, np.int64,
        np.uint8, np.uint16, np.uint32, np.uint64)):
        return bodo.libs.int_arr_ext.IntegerArrayType(numba.typeof(lwa__rcg))
    elif isinstance(lwa__rcg, (dict, Dict)) and all(isinstance(wke__dvt,
        str) for wke__dvt in lwa__rcg.keys()):
        keie__wauir = tuple(lwa__rcg.keys())
        xislc__zov = tuple(_get_struct_value_arr_type(v) for v in lwa__rcg.
            values())
        return StructArrayType(xislc__zov, keie__wauir)
    elif isinstance(lwa__rcg, (dict, Dict)):
        htok__aniv = numba.typeof(_value_to_array(list(lwa__rcg.keys())))
        jfoe__tyvq = numba.typeof(_value_to_array(list(lwa__rcg.values())))
        htok__aniv = to_str_arr_if_dict_array(htok__aniv)
        jfoe__tyvq = to_str_arr_if_dict_array(jfoe__tyvq)
        return MapArrayType(htok__aniv, jfoe__tyvq)
    elif isinstance(lwa__rcg, tuple):
        xislc__zov = tuple(_get_struct_value_arr_type(v) for v in lwa__rcg)
        return TupleArrayType(xislc__zov)
    if isinstance(lwa__rcg, (list, np.ndarray, pd.arrays.BooleanArray, pd.
        arrays.IntegerArray, pd.arrays.StringArray)):
        if isinstance(lwa__rcg, list):
            lwa__rcg = _value_to_array(lwa__rcg)
        krqaz__nuaf = numba.typeof(lwa__rcg)
        krqaz__nuaf = to_str_arr_if_dict_array(krqaz__nuaf)
        return ArrayItemArrayType(krqaz__nuaf)
    if isinstance(lwa__rcg, datetime.date):
        return datetime_date_array_type
    if isinstance(lwa__rcg, datetime.timedelta):
        return datetime_timedelta_array_type
    if isinstance(lwa__rcg, decimal.Decimal):
        return DecimalArrayType(38, 18)
    raise BodoError(f'Unsupported object array with first value: {lwa__rcg}')


def _value_to_array(val):
    assert isinstance(val, (list, dict, Dict))
    if isinstance(val, (dict, Dict)):
        val = dict(val)
        return np.array([val], np.object_)
    wdeb__ozs = val.copy()
    wdeb__ozs.append(None)
    kebv__zphl = np.array(wdeb__ozs, np.object_)
    if len(val) and isinstance(val[0], float):
        kebv__zphl = np.array(val, np.float64)
    return kebv__zphl


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
    gmbc__nwbad = dtype_to_array_type(numba.typeof(v))
    if isinstance(v, (int, bool)):
        gmbc__nwbad = to_nullable_type(gmbc__nwbad)
    return gmbc__nwbad
