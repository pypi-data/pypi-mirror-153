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
    fgr__wbemk = tuple(val.columns.to_list())
    oxl__iozk = get_hiframes_dtypes(val)
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and len(val._bodo_meta['type_metadata'
        ][1]) == len(val.columns) and val._bodo_meta['type_metadata'][0] is not
        None):
        nxv__qqncc = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        nxv__qqncc = numba.typeof(val.index)
    wzkcu__qyrtn = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    imiq__gjs = len(oxl__iozk) >= TABLE_FORMAT_THRESHOLD
    return DataFrameType(oxl__iozk, nxv__qqncc, fgr__wbemk, wzkcu__qyrtn,
        is_table_format=imiq__gjs)


@typeof_impl.register(pd.Series)
def typeof_pd_series(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    wzkcu__qyrtn = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and val._bodo_meta['type_metadata'][0]
         is not None):
        ybwnf__abfj = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        ybwnf__abfj = numba.typeof(val.index)
    dtype = _infer_series_dtype(val)
    idr__tyzg = dtype_to_array_type(dtype)
    if _use_dict_str_type and idr__tyzg == string_array_type:
        idr__tyzg = bodo.dict_str_arr_type
    return SeriesType(dtype, data=idr__tyzg, index=ybwnf__abfj, name_typ=
        numba.typeof(val.name), dist=wzkcu__qyrtn)


@unbox(DataFrameType)
def unbox_dataframe(typ, val, c):
    check_runtime_cols_unsupported(typ, 'Unboxing')
    cxf__ibfjq = c.pyapi.object_getattr_string(val, 'index')
    zcgr__raj = c.pyapi.to_native_value(typ.index, cxf__ibfjq).value
    c.pyapi.decref(cxf__ibfjq)
    if typ.is_table_format:
        odof__cuwjm = cgutils.create_struct_proxy(typ.table_type)(c.context,
            c.builder)
        odof__cuwjm.parent = val
        for vsap__xezm, vuw__jphid in typ.table_type.type_to_blk.items():
            kgizy__zff = c.context.get_constant(types.int64, len(typ.
                table_type.block_to_arr_ind[vuw__jphid]))
            dfhj__ivh, qhnn__mnze = ListInstance.allocate_ex(c.context, c.
                builder, types.List(vsap__xezm), kgizy__zff)
            qhnn__mnze.size = kgizy__zff
            setattr(odof__cuwjm, f'block_{vuw__jphid}', qhnn__mnze.value)
        qzbn__qrd = c.pyapi.call_method(val, '__len__', ())
        eii__ypu = c.pyapi.long_as_longlong(qzbn__qrd)
        c.pyapi.decref(qzbn__qrd)
        odof__cuwjm.len = eii__ypu
        bmz__pozm = c.context.make_tuple(c.builder, types.Tuple([typ.
            table_type]), [odof__cuwjm._getvalue()])
    else:
        ettsl__tbt = [c.context.get_constant_null(vsap__xezm) for
            vsap__xezm in typ.data]
        bmz__pozm = c.context.make_tuple(c.builder, types.Tuple(typ.data),
            ettsl__tbt)
    xad__dcs = construct_dataframe(c.context, c.builder, typ, bmz__pozm,
        zcgr__raj, val, None)
    return NativeValue(xad__dcs)


def get_hiframes_dtypes(df):
    if (hasattr(df, '_bodo_meta') and df._bodo_meta is not None and 
        'type_metadata' in df._bodo_meta and df._bodo_meta['type_metadata']
         is not None and len(df._bodo_meta['type_metadata'][1]) == len(df.
        columns)):
        pmx__grnu = df._bodo_meta['type_metadata'][1]
    else:
        pmx__grnu = [None] * len(df.columns)
    xyogz__mlaa = [dtype_to_array_type(_infer_series_dtype(df.iloc[:, i],
        array_metadata=pmx__grnu[i])) for i in range(len(df.columns))]
    xyogz__mlaa = [(bodo.dict_str_arr_type if _use_dict_str_type and 
        vsap__xezm == string_array_type else vsap__xezm) for vsap__xezm in
        xyogz__mlaa]
    return tuple(xyogz__mlaa)


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
    pbc__djyp, typ = _dtype_from_type_enum_list_recursor(typ_enum_list)
    if len(pbc__djyp) != 0:
        raise_bodo_error(
            f"""Unexpected Internal Error while converting typing metadata: Dtype list was not fully consumed.
 Input typ_enum_list: {typ_enum_list}.
Remainder: {pbc__djyp}. Please file the error here: https://github.com/Bodo-inc/Feedback"""
            )
    return typ


def _dtype_from_type_enum_list_recursor(typ_enum_list):
    if len(typ_enum_list) == 0:
        raise_bodo_error('Unable to infer dtype from empty typ_enum_list')
    elif typ_enum_list[0] in _one_to_one_enum_to_type_map:
        return typ_enum_list[1:], _one_to_one_enum_to_type_map[typ_enum_list[0]
            ]
    elif typ_enum_list[0] == SeriesDtypeEnum.IntegerArray.value:
        ewkch__vzp, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:]
            )
        return ewkch__vzp, IntegerArrayType(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.ARRAY.value:
        ewkch__vzp, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:]
            )
        return ewkch__vzp, dtype_to_array_type(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.Decimal.value:
        qquz__cltuv = typ_enum_list[1]
        vuenl__mqueu = typ_enum_list[2]
        return typ_enum_list[3:], Decimal128Type(qquz__cltuv, vuenl__mqueu)
    elif typ_enum_list[0] == SeriesDtypeEnum.STRUCT.value:
        fmrol__jsfh = typ_enum_list[1]
        ocffo__xualf = tuple(typ_enum_list[2:2 + fmrol__jsfh])
        nrlb__txp = typ_enum_list[2 + fmrol__jsfh:]
        qyt__gux = []
        for i in range(fmrol__jsfh):
            nrlb__txp, dkqqe__jecdv = _dtype_from_type_enum_list_recursor(
                nrlb__txp)
            qyt__gux.append(dkqqe__jecdv)
        return nrlb__txp, StructType(tuple(qyt__gux), ocffo__xualf)
    elif typ_enum_list[0] == SeriesDtypeEnum.Literal.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'Literal' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        ntv__wuqa = typ_enum_list[1]
        nrlb__txp = typ_enum_list[2:]
        return nrlb__txp, ntv__wuqa
    elif typ_enum_list[0] == SeriesDtypeEnum.LiteralType.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'LiteralType' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        ntv__wuqa = typ_enum_list[1]
        nrlb__txp = typ_enum_list[2:]
        return nrlb__txp, numba.types.literal(ntv__wuqa)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalType.value:
        nrlb__txp, hdlq__tolt = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        nrlb__txp, ruz__lbb = _dtype_from_type_enum_list_recursor(nrlb__txp)
        nrlb__txp, nroqx__sudu = _dtype_from_type_enum_list_recursor(nrlb__txp)
        nrlb__txp, gitk__mow = _dtype_from_type_enum_list_recursor(nrlb__txp)
        nrlb__txp, iik__gtro = _dtype_from_type_enum_list_recursor(nrlb__txp)
        return nrlb__txp, PDCategoricalDtype(hdlq__tolt, ruz__lbb,
            nroqx__sudu, gitk__mow, iik__gtro)
    elif typ_enum_list[0] == SeriesDtypeEnum.DatetimeIndexType.value:
        nrlb__txp, cjvi__zxocu = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return nrlb__txp, DatetimeIndexType(cjvi__zxocu)
    elif typ_enum_list[0] == SeriesDtypeEnum.NumericIndexType.value:
        nrlb__txp, dtype = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        nrlb__txp, cjvi__zxocu = _dtype_from_type_enum_list_recursor(nrlb__txp)
        nrlb__txp, gitk__mow = _dtype_from_type_enum_list_recursor(nrlb__txp)
        return nrlb__txp, NumericIndexType(dtype, cjvi__zxocu, gitk__mow)
    elif typ_enum_list[0] == SeriesDtypeEnum.PeriodIndexType.value:
        nrlb__txp, crma__zbgb = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        nrlb__txp, cjvi__zxocu = _dtype_from_type_enum_list_recursor(nrlb__txp)
        return nrlb__txp, PeriodIndexType(crma__zbgb, cjvi__zxocu)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalIndexType.value:
        nrlb__txp, gitk__mow = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        nrlb__txp, cjvi__zxocu = _dtype_from_type_enum_list_recursor(nrlb__txp)
        return nrlb__txp, CategoricalIndexType(gitk__mow, cjvi__zxocu)
    elif typ_enum_list[0] == SeriesDtypeEnum.RangeIndexType.value:
        nrlb__txp, cjvi__zxocu = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return nrlb__txp, RangeIndexType(cjvi__zxocu)
    elif typ_enum_list[0] == SeriesDtypeEnum.StringIndexType.value:
        nrlb__txp, cjvi__zxocu = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return nrlb__txp, StringIndexType(cjvi__zxocu)
    elif typ_enum_list[0] == SeriesDtypeEnum.BinaryIndexType.value:
        nrlb__txp, cjvi__zxocu = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return nrlb__txp, BinaryIndexType(cjvi__zxocu)
    elif typ_enum_list[0] == SeriesDtypeEnum.TimedeltaIndexType.value:
        nrlb__txp, cjvi__zxocu = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return nrlb__txp, TimedeltaIndexType(cjvi__zxocu)
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
        mds__zoozd = get_overload_const_int(typ)
        if numba.types.maybe_literal(mds__zoozd) == typ:
            return [SeriesDtypeEnum.LiteralType.value, mds__zoozd]
    elif is_overload_constant_str(typ):
        mds__zoozd = get_overload_const_str(typ)
        if numba.types.maybe_literal(mds__zoozd) == typ:
            return [SeriesDtypeEnum.LiteralType.value, mds__zoozd]
    elif is_overload_constant_bool(typ):
        mds__zoozd = get_overload_const_bool(typ)
        if numba.types.maybe_literal(mds__zoozd) == typ:
            return [SeriesDtypeEnum.LiteralType.value, mds__zoozd]
    elif isinstance(typ, IntegerArrayType):
        return [SeriesDtypeEnum.IntegerArray.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif bodo.utils.utils.is_array_typ(typ, False):
        return [SeriesDtypeEnum.ARRAY.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif isinstance(typ, StructType):
        bvys__pdn = [SeriesDtypeEnum.STRUCT.value, len(typ.names)]
        for itktk__qcc in typ.names:
            bvys__pdn.append(itktk__qcc)
        for nxgj__ujf in typ.data:
            bvys__pdn += _dtype_to_type_enum_list_recursor(nxgj__ujf)
        return bvys__pdn
    elif isinstance(typ, bodo.libs.decimal_arr_ext.Decimal128Type):
        return [SeriesDtypeEnum.Decimal.value, typ.precision, typ.scale]
    elif isinstance(typ, PDCategoricalDtype):
        rroam__qqivp = _dtype_to_type_enum_list_recursor(typ.categories)
        yrdeb__tvhz = _dtype_to_type_enum_list_recursor(typ.elem_type)
        lhleo__qfqn = _dtype_to_type_enum_list_recursor(typ.ordered)
        zwb__gxuc = _dtype_to_type_enum_list_recursor(typ.data)
        yfr__icfgf = _dtype_to_type_enum_list_recursor(typ.int_type)
        return [SeriesDtypeEnum.CategoricalType.value
            ] + rroam__qqivp + yrdeb__tvhz + lhleo__qfqn + zwb__gxuc + yfr__icfgf
    elif isinstance(typ, DatetimeIndexType):
        return [SeriesDtypeEnum.DatetimeIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, NumericIndexType):
        if upcast_numeric_index:
            if isinstance(typ.dtype, types.Float):
                uyvom__nlv = types.float64
                dgka__asmuh = types.Array(uyvom__nlv, 1, 'C')
            elif typ.dtype in {types.int8, types.int16, types.int32, types.
                int64}:
                uyvom__nlv = types.int64
                if isinstance(typ.data, IntegerArrayType):
                    dgka__asmuh = IntegerArrayType(uyvom__nlv)
                else:
                    dgka__asmuh = types.Array(uyvom__nlv, 1, 'C')
            elif typ.dtype in {types.uint8, types.uint16, types.uint32,
                types.uint64}:
                uyvom__nlv = types.uint64
                if isinstance(typ.data, IntegerArrayType):
                    dgka__asmuh = IntegerArrayType(uyvom__nlv)
                else:
                    dgka__asmuh = types.Array(uyvom__nlv, 1, 'C')
            elif typ.dtype == types.bool_:
                uyvom__nlv = typ.dtype
                dgka__asmuh = typ.data
            else:
                raise GuardException('Unable to convert type')
            return [SeriesDtypeEnum.NumericIndexType.value
                ] + _dtype_to_type_enum_list_recursor(uyvom__nlv
                ) + _dtype_to_type_enum_list_recursor(typ.name_typ
                ) + _dtype_to_type_enum_list_recursor(dgka__asmuh)
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
                aijjx__xiu = S._bodo_meta['type_metadata'][1]
                return _dtype_from_type_enum_list(aijjx__xiu)
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
        dsoh__uikyz = S.dtype.unit
        if dsoh__uikyz != 'ns':
            raise BodoError("Timezone-aware datetime data requires 'ns' units")
        wugsc__lwduk = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(S.
            dtype.tz)
        return PandasDatetimeTZDtype(wugsc__lwduk)
    try:
        return numpy_support.from_dtype(S.dtype)
    except:
        raise BodoError(
            f'data type {S.dtype} for column {S.name} not supported yet')


def _get_use_df_parent_obj_flag(builder, context, pyapi, parent_obj, n_cols):
    if n_cols is None:
        return context.get_constant(types.bool_, False)
    cltl__gpyq = cgutils.is_not_null(builder, parent_obj)
    wxx__srdts = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with builder.if_then(cltl__gpyq):
        wncb__vgd = pyapi.object_getattr_string(parent_obj, 'columns')
        qzbn__qrd = pyapi.call_method(wncb__vgd, '__len__', ())
        builder.store(pyapi.long_as_longlong(qzbn__qrd), wxx__srdts)
        pyapi.decref(qzbn__qrd)
        pyapi.decref(wncb__vgd)
    use_parent_obj = builder.and_(cltl__gpyq, builder.icmp_unsigned('==',
        builder.load(wxx__srdts), context.get_constant(types.int64, n_cols)))
    return use_parent_obj


def _get_df_columns_obj(c, builder, context, pyapi, df_typ, dataframe_payload):
    if df_typ.has_runtime_cols:
        ufnt__dpy = df_typ.runtime_colname_typ
        context.nrt.incref(builder, ufnt__dpy, dataframe_payload.columns)
        return pyapi.from_native_value(ufnt__dpy, dataframe_payload.columns,
            c.env_manager)
    if all(isinstance(c, int) for c in df_typ.columns):
        iga__zjkcw = np.array(df_typ.columns, 'int64')
    elif all(isinstance(c, str) for c in df_typ.columns):
        iga__zjkcw = pd.array(df_typ.columns, 'string')
    else:
        iga__zjkcw = df_typ.columns
    hareh__kjzsl = numba.typeof(iga__zjkcw)
    ueo__mwp = context.get_constant_generic(builder, hareh__kjzsl, iga__zjkcw)
    eyz__xqgsv = pyapi.from_native_value(hareh__kjzsl, ueo__mwp, c.env_manager)
    return eyz__xqgsv


def _create_initial_df_object(builder, context, pyapi, c, df_typ, obj,
    dataframe_payload, res, use_parent_obj):
    with c.builder.if_else(use_parent_obj) as (ftdnx__xran, ykfex__wpa):
        with ftdnx__xran:
            pyapi.incref(obj)
            jmvx__gcemx = context.insert_const_string(c.builder.module, 'numpy'
                )
            rxl__lsbb = pyapi.import_module_noblock(jmvx__gcemx)
            if df_typ.has_runtime_cols:
                ckg__bbjtn = 0
            else:
                ckg__bbjtn = len(df_typ.columns)
            msr__xjil = pyapi.long_from_longlong(lir.Constant(lir.IntType(
                64), ckg__bbjtn))
            pkqm__pril = pyapi.call_method(rxl__lsbb, 'arange', (msr__xjil,))
            pyapi.object_setattr_string(obj, 'columns', pkqm__pril)
            pyapi.decref(rxl__lsbb)
            pyapi.decref(pkqm__pril)
            pyapi.decref(msr__xjil)
        with ykfex__wpa:
            context.nrt.incref(builder, df_typ.index, dataframe_payload.index)
            pldm__yxbwg = c.pyapi.from_native_value(df_typ.index,
                dataframe_payload.index, c.env_manager)
            jmvx__gcemx = context.insert_const_string(c.builder.module,
                'pandas')
            rxl__lsbb = pyapi.import_module_noblock(jmvx__gcemx)
            df_obj = pyapi.call_method(rxl__lsbb, 'DataFrame', (pyapi.
                borrow_none(), pldm__yxbwg))
            pyapi.decref(rxl__lsbb)
            pyapi.decref(pldm__yxbwg)
            builder.store(df_obj, res)


@box(DataFrameType)
def box_dataframe(typ, val, c):
    from bodo.hiframes.table import box_table
    context = c.context
    builder = c.builder
    pyapi = c.pyapi
    dataframe_payload = bodo.hiframes.pd_dataframe_ext.get_dataframe_payload(c
        .context, c.builder, typ, val)
    ugx__zpk = cgutils.create_struct_proxy(typ)(context, builder, value=val)
    n_cols = len(typ.columns) if not typ.has_runtime_cols else None
    obj = ugx__zpk.parent
    res = cgutils.alloca_once_value(builder, obj)
    use_parent_obj = _get_use_df_parent_obj_flag(builder, context, pyapi,
        obj, n_cols)
    _create_initial_df_object(builder, context, pyapi, c, typ, obj,
        dataframe_payload, res, use_parent_obj)
    if typ.is_table_format:
        jxugz__hrat = typ.table_type
        odof__cuwjm = builder.extract_value(dataframe_payload.data, 0)
        context.nrt.incref(builder, jxugz__hrat, odof__cuwjm)
        tmz__igul = box_table(jxugz__hrat, odof__cuwjm, c, builder.not_(
            use_parent_obj))
        with builder.if_else(use_parent_obj) as (qbbll__tjs, jekan__tzwg):
            with qbbll__tjs:
                ahi__srrqn = pyapi.object_getattr_string(tmz__igul, 'arrays')
                cvcd__kbcyn = c.pyapi.make_none()
                if n_cols is None:
                    qzbn__qrd = pyapi.call_method(ahi__srrqn, '__len__', ())
                    kgizy__zff = pyapi.long_as_longlong(qzbn__qrd)
                    pyapi.decref(qzbn__qrd)
                else:
                    kgizy__zff = context.get_constant(types.int64, n_cols)
                with cgutils.for_range(builder, kgizy__zff) as ukxm__sman:
                    i = ukxm__sman.index
                    usyp__cstt = pyapi.list_getitem(ahi__srrqn, i)
                    uumwn__fez = c.builder.icmp_unsigned('!=', usyp__cstt,
                        cvcd__kbcyn)
                    with builder.if_then(uumwn__fez):
                        eem__hxccp = pyapi.long_from_longlong(i)
                        df_obj = builder.load(res)
                        pyapi.object_setitem(df_obj, eem__hxccp, usyp__cstt)
                        pyapi.decref(eem__hxccp)
                pyapi.decref(ahi__srrqn)
                pyapi.decref(cvcd__kbcyn)
            with jekan__tzwg:
                df_obj = builder.load(res)
                pldm__yxbwg = pyapi.object_getattr_string(df_obj, 'index')
                fpq__lxkdd = c.pyapi.call_method(tmz__igul, 'to_pandas', (
                    pldm__yxbwg,))
                builder.store(fpq__lxkdd, res)
                pyapi.decref(df_obj)
                pyapi.decref(pldm__yxbwg)
        pyapi.decref(tmz__igul)
    else:
        fwp__qpm = [builder.extract_value(dataframe_payload.data, i) for i in
            range(n_cols)]
        bdvju__onwfz = typ.data
        for i, cisr__sitz, idr__tyzg in zip(range(n_cols), fwp__qpm,
            bdvju__onwfz):
            wvmxx__cbx = cgutils.alloca_once_value(builder, cisr__sitz)
            duh__xsqv = cgutils.alloca_once_value(builder, context.
                get_constant_null(idr__tyzg))
            uumwn__fez = builder.not_(is_ll_eq(builder, wvmxx__cbx, duh__xsqv))
            yurp__afbn = builder.or_(builder.not_(use_parent_obj), builder.
                and_(use_parent_obj, uumwn__fez))
            with builder.if_then(yurp__afbn):
                eem__hxccp = pyapi.long_from_longlong(context.get_constant(
                    types.int64, i))
                context.nrt.incref(builder, idr__tyzg, cisr__sitz)
                arr_obj = pyapi.from_native_value(idr__tyzg, cisr__sitz, c.
                    env_manager)
                df_obj = builder.load(res)
                pyapi.object_setitem(df_obj, eem__hxccp, arr_obj)
                pyapi.decref(arr_obj)
                pyapi.decref(eem__hxccp)
    df_obj = builder.load(res)
    eyz__xqgsv = _get_df_columns_obj(c, builder, context, pyapi, typ,
        dataframe_payload)
    pyapi.object_setattr_string(df_obj, 'columns', eyz__xqgsv)
    pyapi.decref(eyz__xqgsv)
    _set_bodo_meta_dataframe(c, df_obj, typ)
    c.context.nrt.decref(c.builder, typ, val)
    return df_obj


def get_df_obj_column_codegen(context, builder, pyapi, df_obj, col_ind,
    data_typ):
    cvcd__kbcyn = pyapi.borrow_none()
    icknk__yaazi = pyapi.unserialize(pyapi.serialize_object(slice))
    nbmvm__cls = pyapi.call_function_objargs(icknk__yaazi, [cvcd__kbcyn])
    xateb__var = pyapi.long_from_longlong(col_ind)
    afpp__dsrku = pyapi.tuple_pack([nbmvm__cls, xateb__var])
    msr__xfes = pyapi.object_getattr_string(df_obj, 'iloc')
    otc__bgonq = pyapi.object_getitem(msr__xfes, afpp__dsrku)
    if isinstance(data_typ, bodo.DatetimeArrayType):
        gjp__jttc = pyapi.object_getattr_string(otc__bgonq, 'array')
    else:
        gjp__jttc = pyapi.object_getattr_string(otc__bgonq, 'values')
    if isinstance(data_typ, types.Array):
        fsk__yxgis = context.insert_const_string(builder.module, 'numpy')
        jum__yvzzt = pyapi.import_module_noblock(fsk__yxgis)
        arr_obj = pyapi.call_method(jum__yvzzt, 'ascontiguousarray', (
            gjp__jttc,))
        pyapi.decref(gjp__jttc)
        pyapi.decref(jum__yvzzt)
    else:
        arr_obj = gjp__jttc
    pyapi.decref(icknk__yaazi)
    pyapi.decref(nbmvm__cls)
    pyapi.decref(xateb__var)
    pyapi.decref(afpp__dsrku)
    pyapi.decref(msr__xfes)
    pyapi.decref(otc__bgonq)
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
        ugx__zpk = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        arr_obj = get_df_obj_column_codegen(context, builder, pyapi,
            ugx__zpk.parent, args[1], data_typ)
        xzw__dhfq = _unbox_series_data(data_typ.dtype, data_typ, arr_obj, c)
        c.pyapi.decref(arr_obj)
        dataframe_payload = (bodo.hiframes.pd_dataframe_ext.
            get_dataframe_payload(c.context, c.builder, df_typ, args[0]))
        if df_typ.is_table_format:
            odof__cuwjm = cgutils.create_struct_proxy(df_typ.table_type)(c.
                context, c.builder, builder.extract_value(dataframe_payload
                .data, 0))
            vuw__jphid = df_typ.table_type.type_to_blk[data_typ]
            amya__sugtk = getattr(odof__cuwjm, f'block_{vuw__jphid}')
            rlxsn__jlx = ListInstance(c.context, c.builder, types.List(
                data_typ), amya__sugtk)
            mlnw__tqgf = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[col_ind])
            rlxsn__jlx.inititem(mlnw__tqgf, xzw__dhfq.value, incref=False)
        else:
            dataframe_payload.data = builder.insert_value(dataframe_payload
                .data, xzw__dhfq.value, col_ind)
        xrie__jwp = DataFramePayloadType(df_typ)
        ixs__sdivy = context.nrt.meminfo_data(builder, ugx__zpk.meminfo)
        xny__adkf = context.get_value_type(xrie__jwp).as_pointer()
        ixs__sdivy = builder.bitcast(ixs__sdivy, xny__adkf)
        builder.store(dataframe_payload._getvalue(), ixs__sdivy)
    return signature(types.none, df, i), codegen


@numba.njit
def unbox_col_if_needed(df, i):
    if bodo.hiframes.pd_dataframe_ext.has_parent(df
        ) and bodo.hiframes.pd_dataframe_ext._column_needs_unboxing(df, i):
        bodo.hiframes.boxing.unbox_dataframe_column(df, i)


@unbox(SeriesType)
def unbox_series(typ, val, c):
    if isinstance(typ.data, DatetimeArrayType):
        gjp__jttc = c.pyapi.object_getattr_string(val, 'array')
    else:
        gjp__jttc = c.pyapi.object_getattr_string(val, 'values')
    if isinstance(typ.data, types.Array):
        fsk__yxgis = c.context.insert_const_string(c.builder.module, 'numpy')
        jum__yvzzt = c.pyapi.import_module_noblock(fsk__yxgis)
        arr_obj = c.pyapi.call_method(jum__yvzzt, 'ascontiguousarray', (
            gjp__jttc,))
        c.pyapi.decref(gjp__jttc)
        c.pyapi.decref(jum__yvzzt)
    else:
        arr_obj = gjp__jttc
    fjd__hool = _unbox_series_data(typ.dtype, typ.data, arr_obj, c).value
    pldm__yxbwg = c.pyapi.object_getattr_string(val, 'index')
    zcgr__raj = c.pyapi.to_native_value(typ.index, pldm__yxbwg).value
    jenph__eyfwg = c.pyapi.object_getattr_string(val, 'name')
    xelqn__oypdc = c.pyapi.to_native_value(typ.name_typ, jenph__eyfwg).value
    uocf__ryywx = bodo.hiframes.pd_series_ext.construct_series(c.context, c
        .builder, typ, fjd__hool, zcgr__raj, xelqn__oypdc)
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(pldm__yxbwg)
    c.pyapi.decref(jenph__eyfwg)
    return NativeValue(uocf__ryywx)


def _unbox_series_data(dtype, data_typ, arr_obj, c):
    if data_typ == string_array_split_view_type:
        ignf__jza = c.context.make_helper(c.builder,
            string_array_split_view_type)
        return NativeValue(ignf__jza._getvalue())
    return c.pyapi.to_native_value(data_typ, arr_obj)


@box(HeterogeneousSeriesType)
@box(SeriesType)
def box_series(typ, val, c):
    jmvx__gcemx = c.context.insert_const_string(c.builder.module, 'pandas')
    kgdl__sugaj = c.pyapi.import_module_noblock(jmvx__gcemx)
    wxxxr__ftfgu = bodo.hiframes.pd_series_ext.get_series_payload(c.context,
        c.builder, typ, val)
    c.context.nrt.incref(c.builder, typ.data, wxxxr__ftfgu.data)
    c.context.nrt.incref(c.builder, typ.index, wxxxr__ftfgu.index)
    c.context.nrt.incref(c.builder, typ.name_typ, wxxxr__ftfgu.name)
    arr_obj = c.pyapi.from_native_value(typ.data, wxxxr__ftfgu.data, c.
        env_manager)
    pldm__yxbwg = c.pyapi.from_native_value(typ.index, wxxxr__ftfgu.index,
        c.env_manager)
    jenph__eyfwg = c.pyapi.from_native_value(typ.name_typ, wxxxr__ftfgu.
        name, c.env_manager)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        dtype = c.pyapi.unserialize(c.pyapi.serialize_object(object))
    else:
        dtype = c.pyapi.make_none()
    res = c.pyapi.call_method(kgdl__sugaj, 'Series', (arr_obj, pldm__yxbwg,
        dtype, jenph__eyfwg))
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(pldm__yxbwg)
    c.pyapi.decref(jenph__eyfwg)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        c.pyapi.decref(dtype)
    _set_bodo_meta_series(res, c, typ)
    c.pyapi.decref(kgdl__sugaj)
    c.context.nrt.decref(c.builder, typ, val)
    return res


def type_enum_list_to_py_list_obj(pyapi, context, builder, env_manager,
    typ_list):
    frt__acvhe = []
    for yyl__ksc in typ_list:
        if isinstance(yyl__ksc, int) and not isinstance(yyl__ksc, bool):
            oiqx__ffwj = pyapi.long_from_longlong(lir.Constant(lir.IntType(
                64), yyl__ksc))
        else:
            qpdr__acab = numba.typeof(yyl__ksc)
            rae__eeh = context.get_constant_generic(builder, qpdr__acab,
                yyl__ksc)
            oiqx__ffwj = pyapi.from_native_value(qpdr__acab, rae__eeh,
                env_manager)
        frt__acvhe.append(oiqx__ffwj)
    wwo__takgy = pyapi.list_pack(frt__acvhe)
    for val in frt__acvhe:
        pyapi.decref(val)
    return wwo__takgy


def _set_bodo_meta_dataframe(c, obj, typ):
    pyapi = c.pyapi
    context = c.context
    builder = c.builder
    shwe__tkw = not typ.has_runtime_cols and (not typ.is_table_format or 
        len(typ.columns) < TABLE_FORMAT_THRESHOLD)
    duort__obwkl = 2 if shwe__tkw else 1
    fhrca__comx = pyapi.dict_new(duort__obwkl)
    wqthh__itkt = pyapi.long_from_longlong(lir.Constant(lir.IntType(64),
        typ.dist.value))
    pyapi.dict_setitem_string(fhrca__comx, 'dist', wqthh__itkt)
    pyapi.decref(wqthh__itkt)
    if shwe__tkw:
        kifpm__pbk = _dtype_to_type_enum_list(typ.index)
        if kifpm__pbk != None:
            qwdyy__adaso = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, kifpm__pbk)
        else:
            qwdyy__adaso = pyapi.make_none()
        orrw__brz = []
        for dtype in typ.data:
            typ_list = _dtype_to_type_enum_list(dtype)
            if typ_list != None:
                wwo__takgy = type_enum_list_to_py_list_obj(pyapi, context,
                    builder, c.env_manager, typ_list)
            else:
                wwo__takgy = pyapi.make_none()
            orrw__brz.append(wwo__takgy)
        keirw__klg = pyapi.list_pack(orrw__brz)
        vucx__jloek = pyapi.list_pack([qwdyy__adaso, keirw__klg])
        for val in orrw__brz:
            pyapi.decref(val)
        pyapi.dict_setitem_string(fhrca__comx, 'type_metadata', vucx__jloek)
    pyapi.object_setattr_string(obj, '_bodo_meta', fhrca__comx)
    pyapi.decref(fhrca__comx)


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
    fhrca__comx = pyapi.dict_new(2)
    wqthh__itkt = pyapi.long_from_longlong(lir.Constant(lir.IntType(64),
        typ.dist.value))
    kifpm__pbk = _dtype_to_type_enum_list(typ.index)
    if kifpm__pbk != None:
        qwdyy__adaso = type_enum_list_to_py_list_obj(pyapi, context,
            builder, c.env_manager, kifpm__pbk)
    else:
        qwdyy__adaso = pyapi.make_none()
    dtype = get_series_dtype_handle_null_int_and_hetrogenous(typ)
    if dtype != None:
        typ_list = _dtype_to_type_enum_list(dtype)
        if typ_list != None:
            zxcf__xnjf = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, typ_list)
        else:
            zxcf__xnjf = pyapi.make_none()
    else:
        zxcf__xnjf = pyapi.make_none()
    ugz__mrx = pyapi.list_pack([qwdyy__adaso, zxcf__xnjf])
    pyapi.dict_setitem_string(fhrca__comx, 'type_metadata', ugz__mrx)
    pyapi.decref(ugz__mrx)
    pyapi.dict_setitem_string(fhrca__comx, 'dist', wqthh__itkt)
    pyapi.object_setattr_string(obj, '_bodo_meta', fhrca__comx)
    pyapi.decref(fhrca__comx)
    pyapi.decref(wqthh__itkt)


@typeof_impl.register(np.ndarray)
def _typeof_ndarray(val, c):
    try:
        dtype = numba.np.numpy_support.from_dtype(val.dtype)
    except NotImplementedError as kjr__uhw:
        dtype = types.pyobject
    if dtype == types.pyobject:
        return _infer_ndarray_obj_dtype(val)
    mfdrf__xghr = numba.np.numpy_support.map_layout(val)
    cshx__kch = not val.flags.writeable
    return types.Array(dtype, val.ndim, mfdrf__xghr, readonly=cshx__kch)


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
    upmh__mbxe = val[i]
    if isinstance(upmh__mbxe, str):
        return (bodo.dict_str_arr_type if _use_dict_str_type else
            string_array_type)
    elif isinstance(upmh__mbxe, bytes):
        return binary_array_type
    elif isinstance(upmh__mbxe, bool):
        return bodo.libs.bool_arr_ext.boolean_array
    elif isinstance(upmh__mbxe, (int, np.int8, np.int16, np.int32, np.int64,
        np.uint8, np.uint16, np.uint32, np.uint64)):
        return bodo.libs.int_arr_ext.IntegerArrayType(numba.typeof(upmh__mbxe))
    elif isinstance(upmh__mbxe, (dict, Dict)) and all(isinstance(vst__pffwj,
        str) for vst__pffwj in upmh__mbxe.keys()):
        ocffo__xualf = tuple(upmh__mbxe.keys())
        hnf__nkvp = tuple(_get_struct_value_arr_type(v) for v in upmh__mbxe
            .values())
        return StructArrayType(hnf__nkvp, ocffo__xualf)
    elif isinstance(upmh__mbxe, (dict, Dict)):
        rtimc__hfymn = numba.typeof(_value_to_array(list(upmh__mbxe.keys())))
        vddm__mxkg = numba.typeof(_value_to_array(list(upmh__mbxe.values())))
        rtimc__hfymn = to_str_arr_if_dict_array(rtimc__hfymn)
        vddm__mxkg = to_str_arr_if_dict_array(vddm__mxkg)
        return MapArrayType(rtimc__hfymn, vddm__mxkg)
    elif isinstance(upmh__mbxe, tuple):
        hnf__nkvp = tuple(_get_struct_value_arr_type(v) for v in upmh__mbxe)
        return TupleArrayType(hnf__nkvp)
    if isinstance(upmh__mbxe, (list, np.ndarray, pd.arrays.BooleanArray, pd
        .arrays.IntegerArray, pd.arrays.StringArray)):
        if isinstance(upmh__mbxe, list):
            upmh__mbxe = _value_to_array(upmh__mbxe)
        zjrd__mwxl = numba.typeof(upmh__mbxe)
        zjrd__mwxl = to_str_arr_if_dict_array(zjrd__mwxl)
        return ArrayItemArrayType(zjrd__mwxl)
    if isinstance(upmh__mbxe, datetime.date):
        return datetime_date_array_type
    if isinstance(upmh__mbxe, datetime.timedelta):
        return datetime_timedelta_array_type
    if isinstance(upmh__mbxe, decimal.Decimal):
        return DecimalArrayType(38, 18)
    raise BodoError(f'Unsupported object array with first value: {upmh__mbxe}')


def _value_to_array(val):
    assert isinstance(val, (list, dict, Dict))
    if isinstance(val, (dict, Dict)):
        val = dict(val)
        return np.array([val], np.object_)
    gxfmo__bqfb = val.copy()
    gxfmo__bqfb.append(None)
    cisr__sitz = np.array(gxfmo__bqfb, np.object_)
    if len(val) and isinstance(val[0], float):
        cisr__sitz = np.array(val, np.float64)
    return cisr__sitz


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
    idr__tyzg = dtype_to_array_type(numba.typeof(v))
    if isinstance(v, (int, bool)):
        idr__tyzg = to_nullable_type(idr__tyzg)
    return idr__tyzg
