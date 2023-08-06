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
    cke__nbzlr = tuple(val.columns.to_list())
    hkhh__yyjnu = get_hiframes_dtypes(val)
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and len(val._bodo_meta['type_metadata'
        ][1]) == len(val.columns) and val._bodo_meta['type_metadata'][0] is not
        None):
        xos__akea = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        xos__akea = numba.typeof(val.index)
    qyqfc__zqqr = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    pidnv__fjkes = len(hkhh__yyjnu) >= TABLE_FORMAT_THRESHOLD
    return DataFrameType(hkhh__yyjnu, xos__akea, cke__nbzlr, qyqfc__zqqr,
        is_table_format=pidnv__fjkes)


@typeof_impl.register(pd.Series)
def typeof_pd_series(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    qyqfc__zqqr = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and val._bodo_meta['type_metadata'][0]
         is not None):
        cmj__rvp = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        cmj__rvp = numba.typeof(val.index)
    dtype = _infer_series_dtype(val)
    aea__jiku = dtype_to_array_type(dtype)
    if _use_dict_str_type and aea__jiku == string_array_type:
        aea__jiku = bodo.dict_str_arr_type
    return SeriesType(dtype, data=aea__jiku, index=cmj__rvp, name_typ=numba
        .typeof(val.name), dist=qyqfc__zqqr)


@unbox(DataFrameType)
def unbox_dataframe(typ, val, c):
    check_runtime_cols_unsupported(typ, 'Unboxing')
    fysai__eppyg = c.pyapi.object_getattr_string(val, 'index')
    wrcft__ssxs = c.pyapi.to_native_value(typ.index, fysai__eppyg).value
    c.pyapi.decref(fysai__eppyg)
    if typ.is_table_format:
        ozi__aztwl = cgutils.create_struct_proxy(typ.table_type)(c.context,
            c.builder)
        ozi__aztwl.parent = val
        for hjd__ksa, hmsdm__oazuz in typ.table_type.type_to_blk.items():
            opz__reb = c.context.get_constant(types.int64, len(typ.
                table_type.block_to_arr_ind[hmsdm__oazuz]))
            cpl__thdp, fujq__zhu = ListInstance.allocate_ex(c.context, c.
                builder, types.List(hjd__ksa), opz__reb)
            fujq__zhu.size = opz__reb
            setattr(ozi__aztwl, f'block_{hmsdm__oazuz}', fujq__zhu.value)
        somzv__uxrbr = c.pyapi.call_method(val, '__len__', ())
        ctbaf__ypbr = c.pyapi.long_as_longlong(somzv__uxrbr)
        c.pyapi.decref(somzv__uxrbr)
        ozi__aztwl.len = ctbaf__ypbr
        ynz__ykxya = c.context.make_tuple(c.builder, types.Tuple([typ.
            table_type]), [ozi__aztwl._getvalue()])
    else:
        dyny__ergo = [c.context.get_constant_null(hjd__ksa) for hjd__ksa in
            typ.data]
        ynz__ykxya = c.context.make_tuple(c.builder, types.Tuple(typ.data),
            dyny__ergo)
    hwjuc__eixrz = construct_dataframe(c.context, c.builder, typ,
        ynz__ykxya, wrcft__ssxs, val, None)
    return NativeValue(hwjuc__eixrz)


def get_hiframes_dtypes(df):
    if (hasattr(df, '_bodo_meta') and df._bodo_meta is not None and 
        'type_metadata' in df._bodo_meta and df._bodo_meta['type_metadata']
         is not None and len(df._bodo_meta['type_metadata'][1]) == len(df.
        columns)):
        irxm__unch = df._bodo_meta['type_metadata'][1]
    else:
        irxm__unch = [None] * len(df.columns)
    mwo__ljq = [dtype_to_array_type(_infer_series_dtype(df.iloc[:, i],
        array_metadata=irxm__unch[i])) for i in range(len(df.columns))]
    mwo__ljq = [(bodo.dict_str_arr_type if _use_dict_str_type and hjd__ksa ==
        string_array_type else hjd__ksa) for hjd__ksa in mwo__ljq]
    return tuple(mwo__ljq)


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
    oio__clsn, typ = _dtype_from_type_enum_list_recursor(typ_enum_list)
    if len(oio__clsn) != 0:
        raise_bodo_error(
            f"""Unexpected Internal Error while converting typing metadata: Dtype list was not fully consumed.
 Input typ_enum_list: {typ_enum_list}.
Remainder: {oio__clsn}. Please file the error here: https://github.com/Bodo-inc/Feedback"""
            )
    return typ


def _dtype_from_type_enum_list_recursor(typ_enum_list):
    if len(typ_enum_list) == 0:
        raise_bodo_error('Unable to infer dtype from empty typ_enum_list')
    elif typ_enum_list[0] in _one_to_one_enum_to_type_map:
        return typ_enum_list[1:], _one_to_one_enum_to_type_map[typ_enum_list[0]
            ]
    elif typ_enum_list[0] == SeriesDtypeEnum.IntegerArray.value:
        siez__zhn, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:])
        return siez__zhn, IntegerArrayType(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.ARRAY.value:
        siez__zhn, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:])
        return siez__zhn, dtype_to_array_type(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.Decimal.value:
        quzyt__irgax = typ_enum_list[1]
        avraz__hmtik = typ_enum_list[2]
        return typ_enum_list[3:], Decimal128Type(quzyt__irgax, avraz__hmtik)
    elif typ_enum_list[0] == SeriesDtypeEnum.STRUCT.value:
        bkdt__turfr = typ_enum_list[1]
        wtbx__ugks = tuple(typ_enum_list[2:2 + bkdt__turfr])
        duim__jmng = typ_enum_list[2 + bkdt__turfr:]
        pthnh__kdf = []
        for i in range(bkdt__turfr):
            duim__jmng, jqu__hhiu = _dtype_from_type_enum_list_recursor(
                duim__jmng)
            pthnh__kdf.append(jqu__hhiu)
        return duim__jmng, StructType(tuple(pthnh__kdf), wtbx__ugks)
    elif typ_enum_list[0] == SeriesDtypeEnum.Literal.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'Literal' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        juztu__hkb = typ_enum_list[1]
        duim__jmng = typ_enum_list[2:]
        return duim__jmng, juztu__hkb
    elif typ_enum_list[0] == SeriesDtypeEnum.LiteralType.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'LiteralType' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        juztu__hkb = typ_enum_list[1]
        duim__jmng = typ_enum_list[2:]
        return duim__jmng, numba.types.literal(juztu__hkb)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalType.value:
        duim__jmng, wfln__yfovg = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        duim__jmng, uwcv__ctxl = _dtype_from_type_enum_list_recursor(duim__jmng
            )
        duim__jmng, lpwu__dyhg = _dtype_from_type_enum_list_recursor(duim__jmng
            )
        duim__jmng, qql__caqx = _dtype_from_type_enum_list_recursor(duim__jmng)
        duim__jmng, cjyoi__jjbng = _dtype_from_type_enum_list_recursor(
            duim__jmng)
        return duim__jmng, PDCategoricalDtype(wfln__yfovg, uwcv__ctxl,
            lpwu__dyhg, qql__caqx, cjyoi__jjbng)
    elif typ_enum_list[0] == SeriesDtypeEnum.DatetimeIndexType.value:
        duim__jmng, rbe__eucvd = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return duim__jmng, DatetimeIndexType(rbe__eucvd)
    elif typ_enum_list[0] == SeriesDtypeEnum.NumericIndexType.value:
        duim__jmng, dtype = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        duim__jmng, rbe__eucvd = _dtype_from_type_enum_list_recursor(duim__jmng
            )
        duim__jmng, qql__caqx = _dtype_from_type_enum_list_recursor(duim__jmng)
        return duim__jmng, NumericIndexType(dtype, rbe__eucvd, qql__caqx)
    elif typ_enum_list[0] == SeriesDtypeEnum.PeriodIndexType.value:
        duim__jmng, cfird__hqvzb = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        duim__jmng, rbe__eucvd = _dtype_from_type_enum_list_recursor(duim__jmng
            )
        return duim__jmng, PeriodIndexType(cfird__hqvzb, rbe__eucvd)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalIndexType.value:
        duim__jmng, qql__caqx = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        duim__jmng, rbe__eucvd = _dtype_from_type_enum_list_recursor(duim__jmng
            )
        return duim__jmng, CategoricalIndexType(qql__caqx, rbe__eucvd)
    elif typ_enum_list[0] == SeriesDtypeEnum.RangeIndexType.value:
        duim__jmng, rbe__eucvd = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return duim__jmng, RangeIndexType(rbe__eucvd)
    elif typ_enum_list[0] == SeriesDtypeEnum.StringIndexType.value:
        duim__jmng, rbe__eucvd = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return duim__jmng, StringIndexType(rbe__eucvd)
    elif typ_enum_list[0] == SeriesDtypeEnum.BinaryIndexType.value:
        duim__jmng, rbe__eucvd = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return duim__jmng, BinaryIndexType(rbe__eucvd)
    elif typ_enum_list[0] == SeriesDtypeEnum.TimedeltaIndexType.value:
        duim__jmng, rbe__eucvd = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return duim__jmng, TimedeltaIndexType(rbe__eucvd)
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
        nopft__plsb = get_overload_const_int(typ)
        if numba.types.maybe_literal(nopft__plsb) == typ:
            return [SeriesDtypeEnum.LiteralType.value, nopft__plsb]
    elif is_overload_constant_str(typ):
        nopft__plsb = get_overload_const_str(typ)
        if numba.types.maybe_literal(nopft__plsb) == typ:
            return [SeriesDtypeEnum.LiteralType.value, nopft__plsb]
    elif is_overload_constant_bool(typ):
        nopft__plsb = get_overload_const_bool(typ)
        if numba.types.maybe_literal(nopft__plsb) == typ:
            return [SeriesDtypeEnum.LiteralType.value, nopft__plsb]
    elif isinstance(typ, IntegerArrayType):
        return [SeriesDtypeEnum.IntegerArray.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif bodo.utils.utils.is_array_typ(typ, False):
        return [SeriesDtypeEnum.ARRAY.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif isinstance(typ, StructType):
        gjlvo__juc = [SeriesDtypeEnum.STRUCT.value, len(typ.names)]
        for nprob__rwvgb in typ.names:
            gjlvo__juc.append(nprob__rwvgb)
        for bdkc__mwnw in typ.data:
            gjlvo__juc += _dtype_to_type_enum_list_recursor(bdkc__mwnw)
        return gjlvo__juc
    elif isinstance(typ, bodo.libs.decimal_arr_ext.Decimal128Type):
        return [SeriesDtypeEnum.Decimal.value, typ.precision, typ.scale]
    elif isinstance(typ, PDCategoricalDtype):
        mhfon__dxpu = _dtype_to_type_enum_list_recursor(typ.categories)
        rpo__jykg = _dtype_to_type_enum_list_recursor(typ.elem_type)
        xawuz__tbu = _dtype_to_type_enum_list_recursor(typ.ordered)
        bqxwy__phpb = _dtype_to_type_enum_list_recursor(typ.data)
        scy__bhul = _dtype_to_type_enum_list_recursor(typ.int_type)
        return [SeriesDtypeEnum.CategoricalType.value
            ] + mhfon__dxpu + rpo__jykg + xawuz__tbu + bqxwy__phpb + scy__bhul
    elif isinstance(typ, DatetimeIndexType):
        return [SeriesDtypeEnum.DatetimeIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, NumericIndexType):
        if upcast_numeric_index:
            if isinstance(typ.dtype, types.Float):
                mdfhu__yvub = types.float64
                itflt__ltio = types.Array(mdfhu__yvub, 1, 'C')
            elif typ.dtype in {types.int8, types.int16, types.int32, types.
                int64}:
                mdfhu__yvub = types.int64
                if isinstance(typ.data, IntegerArrayType):
                    itflt__ltio = IntegerArrayType(mdfhu__yvub)
                else:
                    itflt__ltio = types.Array(mdfhu__yvub, 1, 'C')
            elif typ.dtype in {types.uint8, types.uint16, types.uint32,
                types.uint64}:
                mdfhu__yvub = types.uint64
                if isinstance(typ.data, IntegerArrayType):
                    itflt__ltio = IntegerArrayType(mdfhu__yvub)
                else:
                    itflt__ltio = types.Array(mdfhu__yvub, 1, 'C')
            elif typ.dtype == types.bool_:
                mdfhu__yvub = typ.dtype
                itflt__ltio = typ.data
            else:
                raise GuardException('Unable to convert type')
            return [SeriesDtypeEnum.NumericIndexType.value
                ] + _dtype_to_type_enum_list_recursor(mdfhu__yvub
                ) + _dtype_to_type_enum_list_recursor(typ.name_typ
                ) + _dtype_to_type_enum_list_recursor(itflt__ltio)
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
                bnrj__bcgz = S._bodo_meta['type_metadata'][1]
                return _dtype_from_type_enum_list(bnrj__bcgz)
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
        glnb__mkx = S.dtype.unit
        if glnb__mkx != 'ns':
            raise BodoError("Timezone-aware datetime data requires 'ns' units")
        xgu__ndj = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(S.dtype.tz)
        return PandasDatetimeTZDtype(xgu__ndj)
    try:
        return numpy_support.from_dtype(S.dtype)
    except:
        raise BodoError(
            f'data type {S.dtype} for column {S.name} not supported yet')


def _get_use_df_parent_obj_flag(builder, context, pyapi, parent_obj, n_cols):
    if n_cols is None:
        return context.get_constant(types.bool_, False)
    nxumd__doz = cgutils.is_not_null(builder, parent_obj)
    hovca__jjzag = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with builder.if_then(nxumd__doz):
        geey__ueyv = pyapi.object_getattr_string(parent_obj, 'columns')
        somzv__uxrbr = pyapi.call_method(geey__ueyv, '__len__', ())
        builder.store(pyapi.long_as_longlong(somzv__uxrbr), hovca__jjzag)
        pyapi.decref(somzv__uxrbr)
        pyapi.decref(geey__ueyv)
    use_parent_obj = builder.and_(nxumd__doz, builder.icmp_unsigned('==',
        builder.load(hovca__jjzag), context.get_constant(types.int64, n_cols)))
    return use_parent_obj


def _get_df_columns_obj(c, builder, context, pyapi, df_typ, dataframe_payload):
    if df_typ.has_runtime_cols:
        djmc__xmva = df_typ.runtime_colname_typ
        context.nrt.incref(builder, djmc__xmva, dataframe_payload.columns)
        return pyapi.from_native_value(djmc__xmva, dataframe_payload.
            columns, c.env_manager)
    if all(isinstance(c, int) for c in df_typ.columns):
        vlkfr__caqr = np.array(df_typ.columns, 'int64')
    elif all(isinstance(c, str) for c in df_typ.columns):
        vlkfr__caqr = pd.array(df_typ.columns, 'string')
    else:
        vlkfr__caqr = df_typ.columns
    ely__yyhdj = numba.typeof(vlkfr__caqr)
    uhejm__ocgpi = context.get_constant_generic(builder, ely__yyhdj,
        vlkfr__caqr)
    tvd__zkxb = pyapi.from_native_value(ely__yyhdj, uhejm__ocgpi, c.env_manager
        )
    return tvd__zkxb


def _create_initial_df_object(builder, context, pyapi, c, df_typ, obj,
    dataframe_payload, res, use_parent_obj):
    with c.builder.if_else(use_parent_obj) as (yckqp__velw, ehm__pyk):
        with yckqp__velw:
            pyapi.incref(obj)
            azti__qfea = context.insert_const_string(c.builder.module, 'numpy')
            nrf__eyp = pyapi.import_module_noblock(azti__qfea)
            if df_typ.has_runtime_cols:
                yqj__gpod = 0
            else:
                yqj__gpod = len(df_typ.columns)
            prpl__ejos = pyapi.long_from_longlong(lir.Constant(lir.IntType(
                64), yqj__gpod))
            jrntu__ula = pyapi.call_method(nrf__eyp, 'arange', (prpl__ejos,))
            pyapi.object_setattr_string(obj, 'columns', jrntu__ula)
            pyapi.decref(nrf__eyp)
            pyapi.decref(jrntu__ula)
            pyapi.decref(prpl__ejos)
        with ehm__pyk:
            context.nrt.incref(builder, df_typ.index, dataframe_payload.index)
            ybgk__zahs = c.pyapi.from_native_value(df_typ.index,
                dataframe_payload.index, c.env_manager)
            azti__qfea = context.insert_const_string(c.builder.module, 'pandas'
                )
            nrf__eyp = pyapi.import_module_noblock(azti__qfea)
            df_obj = pyapi.call_method(nrf__eyp, 'DataFrame', (pyapi.
                borrow_none(), ybgk__zahs))
            pyapi.decref(nrf__eyp)
            pyapi.decref(ybgk__zahs)
            builder.store(df_obj, res)


@box(DataFrameType)
def box_dataframe(typ, val, c):
    from bodo.hiframes.table import box_table
    context = c.context
    builder = c.builder
    pyapi = c.pyapi
    dataframe_payload = bodo.hiframes.pd_dataframe_ext.get_dataframe_payload(c
        .context, c.builder, typ, val)
    apm__utv = cgutils.create_struct_proxy(typ)(context, builder, value=val)
    n_cols = len(typ.columns) if not typ.has_runtime_cols else None
    obj = apm__utv.parent
    res = cgutils.alloca_once_value(builder, obj)
    use_parent_obj = _get_use_df_parent_obj_flag(builder, context, pyapi,
        obj, n_cols)
    _create_initial_df_object(builder, context, pyapi, c, typ, obj,
        dataframe_payload, res, use_parent_obj)
    if typ.is_table_format:
        izoj__xoa = typ.table_type
        ozi__aztwl = builder.extract_value(dataframe_payload.data, 0)
        context.nrt.incref(builder, izoj__xoa, ozi__aztwl)
        icee__ijq = box_table(izoj__xoa, ozi__aztwl, c, builder.not_(
            use_parent_obj))
        with builder.if_else(use_parent_obj) as (hap__nyywg, zisnw__xym):
            with hap__nyywg:
                had__xvohp = pyapi.object_getattr_string(icee__ijq, 'arrays')
                mpi__pqn = c.pyapi.make_none()
                if n_cols is None:
                    somzv__uxrbr = pyapi.call_method(had__xvohp, '__len__', ())
                    opz__reb = pyapi.long_as_longlong(somzv__uxrbr)
                    pyapi.decref(somzv__uxrbr)
                else:
                    opz__reb = context.get_constant(types.int64, n_cols)
                with cgutils.for_range(builder, opz__reb) as fklvo__ghz:
                    i = fklvo__ghz.index
                    evxga__jilhu = pyapi.list_getitem(had__xvohp, i)
                    dvqi__jzxio = c.builder.icmp_unsigned('!=',
                        evxga__jilhu, mpi__pqn)
                    with builder.if_then(dvqi__jzxio):
                        ioinn__hkoh = pyapi.long_from_longlong(i)
                        df_obj = builder.load(res)
                        pyapi.object_setitem(df_obj, ioinn__hkoh, evxga__jilhu)
                        pyapi.decref(ioinn__hkoh)
                pyapi.decref(had__xvohp)
                pyapi.decref(mpi__pqn)
            with zisnw__xym:
                df_obj = builder.load(res)
                ybgk__zahs = pyapi.object_getattr_string(df_obj, 'index')
                nev__aylg = c.pyapi.call_method(icee__ijq, 'to_pandas', (
                    ybgk__zahs,))
                builder.store(nev__aylg, res)
                pyapi.decref(df_obj)
                pyapi.decref(ybgk__zahs)
        pyapi.decref(icee__ijq)
    else:
        ahe__cjqny = [builder.extract_value(dataframe_payload.data, i) for
            i in range(n_cols)]
        snl__mvwei = typ.data
        for i, skz__ohzdb, aea__jiku in zip(range(n_cols), ahe__cjqny,
            snl__mvwei):
            bqzti__aotsl = cgutils.alloca_once_value(builder, skz__ohzdb)
            xzxxn__ckno = cgutils.alloca_once_value(builder, context.
                get_constant_null(aea__jiku))
            dvqi__jzxio = builder.not_(is_ll_eq(builder, bqzti__aotsl,
                xzxxn__ckno))
            aqog__jqjo = builder.or_(builder.not_(use_parent_obj), builder.
                and_(use_parent_obj, dvqi__jzxio))
            with builder.if_then(aqog__jqjo):
                ioinn__hkoh = pyapi.long_from_longlong(context.get_constant
                    (types.int64, i))
                context.nrt.incref(builder, aea__jiku, skz__ohzdb)
                arr_obj = pyapi.from_native_value(aea__jiku, skz__ohzdb, c.
                    env_manager)
                df_obj = builder.load(res)
                pyapi.object_setitem(df_obj, ioinn__hkoh, arr_obj)
                pyapi.decref(arr_obj)
                pyapi.decref(ioinn__hkoh)
    df_obj = builder.load(res)
    tvd__zkxb = _get_df_columns_obj(c, builder, context, pyapi, typ,
        dataframe_payload)
    pyapi.object_setattr_string(df_obj, 'columns', tvd__zkxb)
    pyapi.decref(tvd__zkxb)
    _set_bodo_meta_dataframe(c, df_obj, typ)
    c.context.nrt.decref(c.builder, typ, val)
    return df_obj


def get_df_obj_column_codegen(context, builder, pyapi, df_obj, col_ind,
    data_typ):
    mpi__pqn = pyapi.borrow_none()
    yvwu__mpuk = pyapi.unserialize(pyapi.serialize_object(slice))
    aphp__ywga = pyapi.call_function_objargs(yvwu__mpuk, [mpi__pqn])
    aeh__kbfi = pyapi.long_from_longlong(col_ind)
    kdr__vvi = pyapi.tuple_pack([aphp__ywga, aeh__kbfi])
    kfa__vvt = pyapi.object_getattr_string(df_obj, 'iloc')
    mfcw__ulxx = pyapi.object_getitem(kfa__vvt, kdr__vvi)
    if isinstance(data_typ, bodo.DatetimeArrayType):
        bbl__xfvms = pyapi.object_getattr_string(mfcw__ulxx, 'array')
    else:
        bbl__xfvms = pyapi.object_getattr_string(mfcw__ulxx, 'values')
    if isinstance(data_typ, types.Array):
        yids__kiam = context.insert_const_string(builder.module, 'numpy')
        eue__fbuw = pyapi.import_module_noblock(yids__kiam)
        arr_obj = pyapi.call_method(eue__fbuw, 'ascontiguousarray', (
            bbl__xfvms,))
        pyapi.decref(bbl__xfvms)
        pyapi.decref(eue__fbuw)
    else:
        arr_obj = bbl__xfvms
    pyapi.decref(yvwu__mpuk)
    pyapi.decref(aphp__ywga)
    pyapi.decref(aeh__kbfi)
    pyapi.decref(kdr__vvi)
    pyapi.decref(kfa__vvt)
    pyapi.decref(mfcw__ulxx)
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
        apm__utv = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        arr_obj = get_df_obj_column_codegen(context, builder, pyapi,
            apm__utv.parent, args[1], data_typ)
        gjb__iaizx = _unbox_series_data(data_typ.dtype, data_typ, arr_obj, c)
        c.pyapi.decref(arr_obj)
        dataframe_payload = (bodo.hiframes.pd_dataframe_ext.
            get_dataframe_payload(c.context, c.builder, df_typ, args[0]))
        if df_typ.is_table_format:
            ozi__aztwl = cgutils.create_struct_proxy(df_typ.table_type)(c.
                context, c.builder, builder.extract_value(dataframe_payload
                .data, 0))
            hmsdm__oazuz = df_typ.table_type.type_to_blk[data_typ]
            mfwi__cbmyd = getattr(ozi__aztwl, f'block_{hmsdm__oazuz}')
            ufr__wzr = ListInstance(c.context, c.builder, types.List(
                data_typ), mfwi__cbmyd)
            iktmv__xdye = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[col_ind])
            ufr__wzr.inititem(iktmv__xdye, gjb__iaizx.value, incref=False)
        else:
            dataframe_payload.data = builder.insert_value(dataframe_payload
                .data, gjb__iaizx.value, col_ind)
        osz__gsiw = DataFramePayloadType(df_typ)
        rjfby__ciywm = context.nrt.meminfo_data(builder, apm__utv.meminfo)
        twzyy__ntkrw = context.get_value_type(osz__gsiw).as_pointer()
        rjfby__ciywm = builder.bitcast(rjfby__ciywm, twzyy__ntkrw)
        builder.store(dataframe_payload._getvalue(), rjfby__ciywm)
    return signature(types.none, df, i), codegen


@numba.njit
def unbox_col_if_needed(df, i):
    if bodo.hiframes.pd_dataframe_ext.has_parent(df
        ) and bodo.hiframes.pd_dataframe_ext._column_needs_unboxing(df, i):
        bodo.hiframes.boxing.unbox_dataframe_column(df, i)


@unbox(SeriesType)
def unbox_series(typ, val, c):
    if isinstance(typ.data, DatetimeArrayType):
        bbl__xfvms = c.pyapi.object_getattr_string(val, 'array')
    else:
        bbl__xfvms = c.pyapi.object_getattr_string(val, 'values')
    if isinstance(typ.data, types.Array):
        yids__kiam = c.context.insert_const_string(c.builder.module, 'numpy')
        eue__fbuw = c.pyapi.import_module_noblock(yids__kiam)
        arr_obj = c.pyapi.call_method(eue__fbuw, 'ascontiguousarray', (
            bbl__xfvms,))
        c.pyapi.decref(bbl__xfvms)
        c.pyapi.decref(eue__fbuw)
    else:
        arr_obj = bbl__xfvms
    msmb__wobd = _unbox_series_data(typ.dtype, typ.data, arr_obj, c).value
    ybgk__zahs = c.pyapi.object_getattr_string(val, 'index')
    wrcft__ssxs = c.pyapi.to_native_value(typ.index, ybgk__zahs).value
    zdhi__azit = c.pyapi.object_getattr_string(val, 'name')
    qfy__gwk = c.pyapi.to_native_value(typ.name_typ, zdhi__azit).value
    qav__fte = bodo.hiframes.pd_series_ext.construct_series(c.context, c.
        builder, typ, msmb__wobd, wrcft__ssxs, qfy__gwk)
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(ybgk__zahs)
    c.pyapi.decref(zdhi__azit)
    return NativeValue(qav__fte)


def _unbox_series_data(dtype, data_typ, arr_obj, c):
    if data_typ == string_array_split_view_type:
        ztnkp__gxf = c.context.make_helper(c.builder,
            string_array_split_view_type)
        return NativeValue(ztnkp__gxf._getvalue())
    return c.pyapi.to_native_value(data_typ, arr_obj)


@box(HeterogeneousSeriesType)
@box(SeriesType)
def box_series(typ, val, c):
    azti__qfea = c.context.insert_const_string(c.builder.module, 'pandas')
    ekly__yrx = c.pyapi.import_module_noblock(azti__qfea)
    gttxr__wvz = bodo.hiframes.pd_series_ext.get_series_payload(c.context,
        c.builder, typ, val)
    c.context.nrt.incref(c.builder, typ.data, gttxr__wvz.data)
    c.context.nrt.incref(c.builder, typ.index, gttxr__wvz.index)
    c.context.nrt.incref(c.builder, typ.name_typ, gttxr__wvz.name)
    arr_obj = c.pyapi.from_native_value(typ.data, gttxr__wvz.data, c.
        env_manager)
    ybgk__zahs = c.pyapi.from_native_value(typ.index, gttxr__wvz.index, c.
        env_manager)
    zdhi__azit = c.pyapi.from_native_value(typ.name_typ, gttxr__wvz.name, c
        .env_manager)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        dtype = c.pyapi.unserialize(c.pyapi.serialize_object(object))
    else:
        dtype = c.pyapi.make_none()
    res = c.pyapi.call_method(ekly__yrx, 'Series', (arr_obj, ybgk__zahs,
        dtype, zdhi__azit))
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(ybgk__zahs)
    c.pyapi.decref(zdhi__azit)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        c.pyapi.decref(dtype)
    _set_bodo_meta_series(res, c, typ)
    c.pyapi.decref(ekly__yrx)
    c.context.nrt.decref(c.builder, typ, val)
    return res


def type_enum_list_to_py_list_obj(pyapi, context, builder, env_manager,
    typ_list):
    zlgvu__ugxu = []
    for xcb__vvsaf in typ_list:
        if isinstance(xcb__vvsaf, int) and not isinstance(xcb__vvsaf, bool):
            mhx__ryxb = pyapi.long_from_longlong(lir.Constant(lir.IntType(
                64), xcb__vvsaf))
        else:
            zgowg__hhev = numba.typeof(xcb__vvsaf)
            dgl__vsx = context.get_constant_generic(builder, zgowg__hhev,
                xcb__vvsaf)
            mhx__ryxb = pyapi.from_native_value(zgowg__hhev, dgl__vsx,
                env_manager)
        zlgvu__ugxu.append(mhx__ryxb)
    raqt__xwy = pyapi.list_pack(zlgvu__ugxu)
    for val in zlgvu__ugxu:
        pyapi.decref(val)
    return raqt__xwy


def _set_bodo_meta_dataframe(c, obj, typ):
    pyapi = c.pyapi
    context = c.context
    builder = c.builder
    sjb__vxwo = not typ.has_runtime_cols and (not typ.is_table_format or 
        len(typ.columns) < TABLE_FORMAT_THRESHOLD)
    wif__hssj = 2 if sjb__vxwo else 1
    fqjt__fmpjd = pyapi.dict_new(wif__hssj)
    mek__obe = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ.
        dist.value))
    pyapi.dict_setitem_string(fqjt__fmpjd, 'dist', mek__obe)
    pyapi.decref(mek__obe)
    if sjb__vxwo:
        xomhf__lzbb = _dtype_to_type_enum_list(typ.index)
        if xomhf__lzbb != None:
            mawki__yhzz = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, xomhf__lzbb)
        else:
            mawki__yhzz = pyapi.make_none()
        wxa__lmzw = []
        for dtype in typ.data:
            typ_list = _dtype_to_type_enum_list(dtype)
            if typ_list != None:
                raqt__xwy = type_enum_list_to_py_list_obj(pyapi, context,
                    builder, c.env_manager, typ_list)
            else:
                raqt__xwy = pyapi.make_none()
            wxa__lmzw.append(raqt__xwy)
        ldha__jyeqr = pyapi.list_pack(wxa__lmzw)
        hlx__rosk = pyapi.list_pack([mawki__yhzz, ldha__jyeqr])
        for val in wxa__lmzw:
            pyapi.decref(val)
        pyapi.dict_setitem_string(fqjt__fmpjd, 'type_metadata', hlx__rosk)
    pyapi.object_setattr_string(obj, '_bodo_meta', fqjt__fmpjd)
    pyapi.decref(fqjt__fmpjd)


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
    fqjt__fmpjd = pyapi.dict_new(2)
    mek__obe = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ.
        dist.value))
    xomhf__lzbb = _dtype_to_type_enum_list(typ.index)
    if xomhf__lzbb != None:
        mawki__yhzz = type_enum_list_to_py_list_obj(pyapi, context, builder,
            c.env_manager, xomhf__lzbb)
    else:
        mawki__yhzz = pyapi.make_none()
    dtype = get_series_dtype_handle_null_int_and_hetrogenous(typ)
    if dtype != None:
        typ_list = _dtype_to_type_enum_list(dtype)
        if typ_list != None:
            mpiar__rtsjs = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, typ_list)
        else:
            mpiar__rtsjs = pyapi.make_none()
    else:
        mpiar__rtsjs = pyapi.make_none()
    wszc__jnv = pyapi.list_pack([mawki__yhzz, mpiar__rtsjs])
    pyapi.dict_setitem_string(fqjt__fmpjd, 'type_metadata', wszc__jnv)
    pyapi.decref(wszc__jnv)
    pyapi.dict_setitem_string(fqjt__fmpjd, 'dist', mek__obe)
    pyapi.object_setattr_string(obj, '_bodo_meta', fqjt__fmpjd)
    pyapi.decref(fqjt__fmpjd)
    pyapi.decref(mek__obe)


@typeof_impl.register(np.ndarray)
def _typeof_ndarray(val, c):
    try:
        dtype = numba.np.numpy_support.from_dtype(val.dtype)
    except NotImplementedError as fxwxj__ufer:
        dtype = types.pyobject
    if dtype == types.pyobject:
        return _infer_ndarray_obj_dtype(val)
    sst__ynn = numba.np.numpy_support.map_layout(val)
    prgze__szxx = not val.flags.writeable
    return types.Array(dtype, val.ndim, sst__ynn, readonly=prgze__szxx)


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
    sxjo__rdu = val[i]
    if isinstance(sxjo__rdu, str):
        return (bodo.dict_str_arr_type if _use_dict_str_type else
            string_array_type)
    elif isinstance(sxjo__rdu, bytes):
        return binary_array_type
    elif isinstance(sxjo__rdu, bool):
        return bodo.libs.bool_arr_ext.boolean_array
    elif isinstance(sxjo__rdu, (int, np.int8, np.int16, np.int32, np.int64,
        np.uint8, np.uint16, np.uint32, np.uint64)):
        return bodo.libs.int_arr_ext.IntegerArrayType(numba.typeof(sxjo__rdu))
    elif isinstance(sxjo__rdu, (dict, Dict)) and all(isinstance(prfu__qfggp,
        str) for prfu__qfggp in sxjo__rdu.keys()):
        wtbx__ugks = tuple(sxjo__rdu.keys())
        jsuzw__pfpv = tuple(_get_struct_value_arr_type(v) for v in
            sxjo__rdu.values())
        return StructArrayType(jsuzw__pfpv, wtbx__ugks)
    elif isinstance(sxjo__rdu, (dict, Dict)):
        gppr__laf = numba.typeof(_value_to_array(list(sxjo__rdu.keys())))
        odmhz__zvtoo = numba.typeof(_value_to_array(list(sxjo__rdu.values())))
        gppr__laf = to_str_arr_if_dict_array(gppr__laf)
        odmhz__zvtoo = to_str_arr_if_dict_array(odmhz__zvtoo)
        return MapArrayType(gppr__laf, odmhz__zvtoo)
    elif isinstance(sxjo__rdu, tuple):
        jsuzw__pfpv = tuple(_get_struct_value_arr_type(v) for v in sxjo__rdu)
        return TupleArrayType(jsuzw__pfpv)
    if isinstance(sxjo__rdu, (list, np.ndarray, pd.arrays.BooleanArray, pd.
        arrays.IntegerArray, pd.arrays.StringArray)):
        if isinstance(sxjo__rdu, list):
            sxjo__rdu = _value_to_array(sxjo__rdu)
        zdbax__doz = numba.typeof(sxjo__rdu)
        zdbax__doz = to_str_arr_if_dict_array(zdbax__doz)
        return ArrayItemArrayType(zdbax__doz)
    if isinstance(sxjo__rdu, datetime.date):
        return datetime_date_array_type
    if isinstance(sxjo__rdu, datetime.timedelta):
        return datetime_timedelta_array_type
    if isinstance(sxjo__rdu, decimal.Decimal):
        return DecimalArrayType(38, 18)
    raise BodoError(f'Unsupported object array with first value: {sxjo__rdu}')


def _value_to_array(val):
    assert isinstance(val, (list, dict, Dict))
    if isinstance(val, (dict, Dict)):
        val = dict(val)
        return np.array([val], np.object_)
    sccrl__athg = val.copy()
    sccrl__athg.append(None)
    skz__ohzdb = np.array(sccrl__athg, np.object_)
    if len(val) and isinstance(val[0], float):
        skz__ohzdb = np.array(val, np.float64)
    return skz__ohzdb


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
    aea__jiku = dtype_to_array_type(numba.typeof(v))
    if isinstance(v, (int, bool)):
        aea__jiku = to_nullable_type(aea__jiku)
    return aea__jiku
