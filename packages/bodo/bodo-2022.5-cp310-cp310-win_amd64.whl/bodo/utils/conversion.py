"""
Utility functions for conversion of data such as list to array.
Need to be inlined for better optimization.
"""
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.extending import overload
import bodo
from bodo.libs.binary_arr_ext import bytes_type
from bodo.libs.bool_arr_ext import boolean_dtype
from bodo.libs.decimal_arr_ext import Decimal128Type, DecimalArrayType
from bodo.libs.nullable_tuple_ext import NullableTupleType
from bodo.utils.indexing import add_nested_counts, init_nested_counts
from bodo.utils.typing import BodoError, decode_if_dict_array, dtype_to_array_type, get_overload_const_list, get_overload_const_str, is_heterogeneous_tuple_type, is_np_arr_typ, is_overload_constant_list, is_overload_constant_str, is_overload_none, is_overload_true, is_str_arr_type, to_nullable_type
NS_DTYPE = np.dtype('M8[ns]')
TD_DTYPE = np.dtype('m8[ns]')


def coerce_to_ndarray(data, error_on_nonarray=True, use_nullable_array=None,
    scalar_to_arr_len=None):
    return data


@overload(coerce_to_ndarray)
def overload_coerce_to_ndarray(data, error_on_nonarray=True,
    use_nullable_array=None, scalar_to_arr_len=None):
    from bodo.hiframes.pd_index_ext import DatetimeIndexType, NumericIndexType, RangeIndexType, TimedeltaIndexType
    from bodo.hiframes.pd_series_ext import SeriesType
    data = types.unliteral(data)
    if isinstance(data, types.Optional) and bodo.utils.typing.is_scalar_type(
        data.type):
        data = data.type
        use_nullable_array = True
    if isinstance(data, bodo.libs.int_arr_ext.IntegerArrayType
        ) and not is_overload_none(use_nullable_array):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.int_arr_ext.
            get_int_arr_data(data))
    if data == bodo.libs.bool_arr_ext.boolean_array and not is_overload_none(
        use_nullable_array):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.bool_arr_ext.
            get_bool_arr_data(data))
    if isinstance(data, types.Array):
        if not is_overload_none(use_nullable_array) and isinstance(data.
            dtype, (types.Boolean, types.Integer)):
            if data.dtype == types.bool_:
                if data.layout != 'C':
                    return (lambda data, error_on_nonarray=True,
                        use_nullable_array=None, scalar_to_arr_len=None:
                        bodo.libs.bool_arr_ext.init_bool_array(np.
                        ascontiguousarray(data), np.full(len(data) + 7 >> 3,
                        255, np.uint8)))
                else:
                    return (lambda data, error_on_nonarray=True,
                        use_nullable_array=None, scalar_to_arr_len=None:
                        bodo.libs.bool_arr_ext.init_bool_array(data, np.
                        full(len(data) + 7 >> 3, 255, np.uint8)))
            elif data.layout != 'C':
                return (lambda data, error_on_nonarray=True,
                    use_nullable_array=None, scalar_to_arr_len=None: bodo.
                    libs.int_arr_ext.init_integer_array(np.
                    ascontiguousarray(data), np.full(len(data) + 7 >> 3, 
                    255, np.uint8)))
            else:
                return (lambda data, error_on_nonarray=True,
                    use_nullable_array=None, scalar_to_arr_len=None: bodo.
                    libs.int_arr_ext.init_integer_array(data, np.full(len(
                    data) + 7 >> 3, 255, np.uint8)))
        if data.layout != 'C':
            return (lambda data, error_on_nonarray=True, use_nullable_array
                =None, scalar_to_arr_len=None: np.ascontiguousarray(data))
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: data)
    if isinstance(data, (types.List, types.UniTuple)):
        uhjb__njz = data.dtype
        if isinstance(uhjb__njz, types.Optional):
            uhjb__njz = uhjb__njz.type
            if bodo.utils.typing.is_scalar_type(uhjb__njz):
                use_nullable_array = True
        if isinstance(uhjb__njz, (types.Boolean, types.Integer, Decimal128Type)
            ) or uhjb__njz in [bodo.hiframes.pd_timestamp_ext.
            pd_timestamp_type, bodo.hiframes.datetime_date_ext.
            datetime_date_type, bodo.hiframes.datetime_timedelta_ext.
            datetime_timedelta_type]:
            iehdc__ytmk = dtype_to_array_type(uhjb__njz)
            if not is_overload_none(use_nullable_array):
                iehdc__ytmk = to_nullable_type(iehdc__ytmk)

            def impl(data, error_on_nonarray=True, use_nullable_array=None,
                scalar_to_arr_len=None):
                bna__ayjo = len(data)
                A = bodo.utils.utils.alloc_type(bna__ayjo, iehdc__ytmk, (-1,))
                bodo.utils.utils.tuple_list_to_array(A, data, uhjb__njz)
                return A
            return impl
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: np.asarray(data))
    if isinstance(data, SeriesType):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.hiframes.pd_series_ext.
            get_series_data(data))
    if isinstance(data, (NumericIndexType, DatetimeIndexType,
        TimedeltaIndexType)):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.hiframes.pd_index_ext.
            get_index_data(data))
    if isinstance(data, RangeIndexType):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: np.arange(data._start, data._stop,
            data._step))
    if isinstance(data, types.RangeType):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: np.arange(data.start, data.stop,
            data.step))
    if not is_overload_none(scalar_to_arr_len):
        if isinstance(data, Decimal128Type):
            bfzei__yxwfw = data.precision
            baz__lri = data.scale

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                bna__ayjo = scalar_to_arr_len
                A = bodo.libs.decimal_arr_ext.alloc_decimal_array(bna__ayjo,
                    bfzei__yxwfw, baz__lri)
                for sacm__vuw in numba.parfors.parfor.internal_prange(bna__ayjo
                    ):
                    A[sacm__vuw] = data
                return A
            return impl_ts
        if data == bodo.hiframes.datetime_datetime_ext.datetime_datetime_type:
            yezef__tvadr = np.dtype('datetime64[ns]')

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                bna__ayjo = scalar_to_arr_len
                A = np.empty(bna__ayjo, yezef__tvadr)
                htbix__ova = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(data))
                rvykj__wfwsr = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                    htbix__ova)
                for sacm__vuw in numba.parfors.parfor.internal_prange(bna__ayjo
                    ):
                    A[sacm__vuw] = rvykj__wfwsr
                return A
            return impl_ts
        if (data == bodo.hiframes.datetime_timedelta_ext.
            datetime_timedelta_type):
            ftby__xzua = np.dtype('timedelta64[ns]')

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                bna__ayjo = scalar_to_arr_len
                A = np.empty(bna__ayjo, ftby__xzua)
                hjx__socjy = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(data))
                for sacm__vuw in numba.parfors.parfor.internal_prange(bna__ayjo
                    ):
                    A[sacm__vuw] = hjx__socjy
                return A
            return impl_ts
        if data == bodo.hiframes.datetime_date_ext.datetime_date_type:

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                bna__ayjo = scalar_to_arr_len
                A = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
                    bna__ayjo)
                for sacm__vuw in numba.parfors.parfor.internal_prange(bna__ayjo
                    ):
                    A[sacm__vuw] = data
                return A
            return impl_ts
        if data == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            yezef__tvadr = np.dtype('datetime64[ns]')

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                bna__ayjo = scalar_to_arr_len
                A = np.empty(scalar_to_arr_len, yezef__tvadr)
                htbix__ova = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                    data.value)
                for sacm__vuw in numba.parfors.parfor.internal_prange(bna__ayjo
                    ):
                    A[sacm__vuw] = htbix__ova
                return A
            return impl_ts
        dtype = types.unliteral(data)
        if not is_overload_none(use_nullable_array) and isinstance(dtype,
            types.Integer):

            def impl_null_integer(data, error_on_nonarray=True,
                use_nullable_array=None, scalar_to_arr_len=None):
                numba.parfors.parfor.init_prange()
                bna__ayjo = scalar_to_arr_len
                tkjs__dfmy = bodo.libs.int_arr_ext.alloc_int_array(bna__ayjo,
                    dtype)
                for sacm__vuw in numba.parfors.parfor.internal_prange(bna__ayjo
                    ):
                    tkjs__dfmy[sacm__vuw] = data
                return tkjs__dfmy
            return impl_null_integer
        if not is_overload_none(use_nullable_array) and dtype == types.bool_:

            def impl_null_bool(data, error_on_nonarray=True,
                use_nullable_array=None, scalar_to_arr_len=None):
                numba.parfors.parfor.init_prange()
                bna__ayjo = scalar_to_arr_len
                tkjs__dfmy = bodo.libs.bool_arr_ext.alloc_bool_array(bna__ayjo)
                for sacm__vuw in numba.parfors.parfor.internal_prange(bna__ayjo
                    ):
                    tkjs__dfmy[sacm__vuw] = data
                return tkjs__dfmy
            return impl_null_bool

        def impl_num(data, error_on_nonarray=True, use_nullable_array=None,
            scalar_to_arr_len=None):
            numba.parfors.parfor.init_prange()
            bna__ayjo = scalar_to_arr_len
            tkjs__dfmy = np.empty(bna__ayjo, dtype)
            for sacm__vuw in numba.parfors.parfor.internal_prange(bna__ayjo):
                tkjs__dfmy[sacm__vuw] = data
            return tkjs__dfmy
        return impl_num
    if isinstance(data, types.BaseTuple) and all(isinstance(ihrrh__ekv, (
        types.Float, types.Integer)) for ihrrh__ekv in data.types):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: np.array(data))
    if bodo.utils.utils.is_array_typ(data, False):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: data)
    if is_overload_true(error_on_nonarray):
        raise BodoError(f'cannot coerce {data} to array')
    return (lambda data, error_on_nonarray=True, use_nullable_array=None,
        scalar_to_arr_len=None: data)


def coerce_to_array(data, error_on_nonarray=True, use_nullable_array=None,
    scalar_to_arr_len=None):
    return data


@overload(coerce_to_array, no_unliteral=True)
def overload_coerce_to_array(data, error_on_nonarray=True,
    use_nullable_array=None, scalar_to_arr_len=None):
    from bodo.hiframes.pd_index_ext import BinaryIndexType, CategoricalIndexType, StringIndexType
    from bodo.hiframes.pd_series_ext import SeriesType
    data = types.unliteral(data)
    if isinstance(data, types.Optional) and bodo.utils.typing.is_scalar_type(
        data.type):
        data = data.type
        use_nullable_array = True
    if isinstance(data, SeriesType):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.hiframes.pd_series_ext.
            get_series_data(data))
    if isinstance(data, (StringIndexType, BinaryIndexType,
        CategoricalIndexType)):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.hiframes.pd_index_ext.
            get_index_data(data))
    if isinstance(data, types.List) and data.dtype in (bodo.string_type,
        bodo.bytes_type):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.str_arr_ext.
            str_arr_from_sequence(data))
    if isinstance(data, types.BaseTuple) and data.count == 0:
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.str_arr_ext.
            empty_str_arr(data))
    if isinstance(data, types.UniTuple) and isinstance(data.dtype, (types.
        UnicodeType, types.StringLiteral)) or isinstance(data, types.BaseTuple
        ) and all(isinstance(ihrrh__ekv, types.StringLiteral) for
        ihrrh__ekv in data.types):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.str_arr_ext.
            str_arr_from_sequence(data))
    if data in (bodo.string_array_type, bodo.dict_str_arr_type, bodo.
        binary_array_type, bodo.libs.bool_arr_ext.boolean_array, bodo.
        hiframes.datetime_date_ext.datetime_date_array_type, bodo.hiframes.
        datetime_timedelta_ext.datetime_timedelta_array_type, bodo.hiframes
        .split_impl.string_array_split_view_type) or isinstance(data, (bodo
        .libs.int_arr_ext.IntegerArrayType, DecimalArrayType, bodo.libs.
        interval_arr_ext.IntervalArrayType, bodo.libs.tuple_arr_ext.
        TupleArrayType, bodo.libs.struct_arr_ext.StructArrayType, bodo.
        hiframes.pd_categorical_ext.CategoricalArrayType, bodo.libs.
        csr_matrix_ext.CSRMatrixType, bodo.DatetimeArrayType)):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: data)
    if isinstance(data, (types.List, types.UniTuple)) and isinstance(data.
        dtype, types.BaseTuple):
        slyll__zpo = tuple(dtype_to_array_type(ihrrh__ekv) for ihrrh__ekv in
            data.dtype.types)

        def impl_tuple_list(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            bna__ayjo = len(data)
            arr = bodo.libs.tuple_arr_ext.pre_alloc_tuple_array(bna__ayjo,
                (-1,), slyll__zpo)
            for sacm__vuw in range(bna__ayjo):
                arr[sacm__vuw] = data[sacm__vuw]
            return arr
        return impl_tuple_list
    if isinstance(data, types.List) and (bodo.utils.utils.is_array_typ(data
        .dtype, False) or isinstance(data.dtype, types.List)):
        uzze__kur = dtype_to_array_type(data.dtype.dtype)

        def impl_array_item_arr(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            bna__ayjo = len(data)
            ihqes__txq = init_nested_counts(uzze__kur)
            for sacm__vuw in range(bna__ayjo):
                sybiw__fbewj = bodo.utils.conversion.coerce_to_array(data[
                    sacm__vuw], use_nullable_array=True)
                ihqes__txq = add_nested_counts(ihqes__txq, sybiw__fbewj)
            tkjs__dfmy = (bodo.libs.array_item_arr_ext.
                pre_alloc_array_item_array(bna__ayjo, ihqes__txq, uzze__kur))
            sbn__hoybu = bodo.libs.array_item_arr_ext.get_null_bitmap(
                tkjs__dfmy)
            for bknn__swsiq in range(bna__ayjo):
                sybiw__fbewj = bodo.utils.conversion.coerce_to_array(data[
                    bknn__swsiq], use_nullable_array=True)
                tkjs__dfmy[bknn__swsiq] = sybiw__fbewj
                bodo.libs.int_arr_ext.set_bit_to_arr(sbn__hoybu, bknn__swsiq, 1
                    )
            return tkjs__dfmy
        return impl_array_item_arr
    if not is_overload_none(scalar_to_arr_len) and isinstance(data, (types.
        UnicodeType, types.StringLiteral)):

        def impl_str(data, error_on_nonarray=True, use_nullable_array=None,
            scalar_to_arr_len=None):
            bna__ayjo = scalar_to_arr_len
            A = bodo.libs.str_arr_ext.pre_alloc_string_array(bna__ayjo, -1)
            for sacm__vuw in numba.parfors.parfor.internal_prange(bna__ayjo):
                A[sacm__vuw] = data
            return A
        return impl_str
    if isinstance(data, types.List) and isinstance(data.dtype, bodo.
        hiframes.pd_timestamp_ext.PandasTimestampType):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
            'coerce_to_array()')

        def impl_list_timestamp(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            bna__ayjo = len(data)
            A = np.empty(bna__ayjo, np.dtype('datetime64[ns]'))
            for sacm__vuw in range(bna__ayjo):
                A[sacm__vuw] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                    data[sacm__vuw].value)
            return A
        return impl_list_timestamp
    if isinstance(data, types.List) and data.dtype == bodo.pd_timedelta_type:

        def impl_list_timedelta(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            bna__ayjo = len(data)
            A = np.empty(bna__ayjo, np.dtype('timedelta64[ns]'))
            for sacm__vuw in range(bna__ayjo):
                A[sacm__vuw
                    ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                    data[sacm__vuw].value)
            return A
        return impl_list_timedelta
    if isinstance(data, bodo.hiframes.pd_timestamp_ext.PandasTimestampType):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
            'coerce_to_array()')
    if not is_overload_none(scalar_to_arr_len) and data in [bodo.
        pd_timestamp_type, bodo.pd_timedelta_type]:
        jjniy__crx = ('datetime64[ns]' if data == bodo.pd_timestamp_type else
            'timedelta64[ns]')

        def impl_timestamp(data, error_on_nonarray=True, use_nullable_array
            =None, scalar_to_arr_len=None):
            bna__ayjo = scalar_to_arr_len
            A = np.empty(bna__ayjo, jjniy__crx)
            data = bodo.utils.conversion.unbox_if_timestamp(data)
            for sacm__vuw in numba.parfors.parfor.internal_prange(bna__ayjo):
                A[sacm__vuw] = data
            return A
        return impl_timestamp
    return (lambda data, error_on_nonarray=True, use_nullable_array=None,
        scalar_to_arr_len=None: bodo.utils.conversion.coerce_to_ndarray(
        data, error_on_nonarray, use_nullable_array, scalar_to_arr_len))


def _is_str_dtype(dtype):
    return isinstance(dtype, bodo.libs.str_arr_ext.StringDtype) or isinstance(
        dtype, types.Function) and dtype.key[0
        ] == str or is_overload_constant_str(dtype) and get_overload_const_str(
        dtype) == 'str' or isinstance(dtype, types.TypeRef
        ) and dtype.instance_type == types.unicode_type


def fix_arr_dtype(data, new_dtype, copy=None, nan_to_str=True, from_series=
    False):
    return data


@overload(fix_arr_dtype, no_unliteral=True)
def overload_fix_arr_dtype(data, new_dtype, copy=None, nan_to_str=True,
    from_series=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'fix_arr_dtype()')
    xce__jjfmo = is_overload_true(copy)
    uzpg__ckp = is_overload_constant_str(new_dtype) and get_overload_const_str(
        new_dtype) == 'object'
    if is_overload_none(new_dtype) or uzpg__ckp:
        if xce__jjfmo:
            return (lambda data, new_dtype, copy=None, nan_to_str=True,
                from_series=False: data.copy())
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data)
    if isinstance(data, NullableTupleType):
        nb_dtype = bodo.utils.typing.parse_dtype(new_dtype)
        if isinstance(nb_dtype, bodo.libs.int_arr_ext.IntDtype):
            nb_dtype = nb_dtype.dtype
        wdvt__mgedb = {types.unicode_type: '', boolean_dtype: False, types.
            bool_: False, types.int8: np.int8(0), types.int16: np.int16(0),
            types.int32: np.int32(0), types.int64: np.int64(0), types.uint8:
            np.uint8(0), types.uint16: np.uint16(0), types.uint32: np.
            uint32(0), types.uint64: np.uint64(0), types.float32: np.
            float32(0), types.float64: np.float64(0), bodo.datetime64ns: pd
            .Timestamp(0), bodo.timedelta64ns: pd.Timedelta(0)}
        fqg__coiup = {types.unicode_type: str, types.bool_: bool,
            boolean_dtype: bool, types.int8: np.int8, types.int16: np.int16,
            types.int32: np.int32, types.int64: np.int64, types.uint8: np.
            uint8, types.uint16: np.uint16, types.uint32: np.uint32, types.
            uint64: np.uint64, types.float32: np.float32, types.float64: np
            .float64, bodo.datetime64ns: pd.to_datetime, bodo.timedelta64ns:
            pd.to_timedelta}
        jxq__vkoz = wdvt__mgedb.keys()
        winhs__jgnmx = list(data._tuple_typ.types)
        if nb_dtype not in jxq__vkoz:
            raise BodoError(f'type conversion to {nb_dtype} types unsupported.'
                )
        for guwsb__gtv in winhs__jgnmx:
            if guwsb__gtv == bodo.datetime64ns:
                if nb_dtype not in (types.unicode_type, types.int64, types.
                    uint64, bodo.datetime64ns):
                    raise BodoError(
                        f'invalid type conversion from {guwsb__gtv} to {nb_dtype}.'
                        )
            elif guwsb__gtv == bodo.timedelta64ns:
                if nb_dtype not in (types.unicode_type, types.int64, types.
                    uint64, bodo.timedelta64ns):
                    raise BodoError(
                        f'invalid type conversion from {guwsb__gtv} to {nb_dtype}.'
                        )
        nuzb__uxa = (
            'def impl(data, new_dtype, copy=None, nan_to_str=True, from_series=False):\n'
            )
        nuzb__uxa += '  data_tup = data._data\n'
        nuzb__uxa += '  null_tup = data._null_values\n'
        for sacm__vuw in range(len(winhs__jgnmx)):
            nuzb__uxa += f'  val_{sacm__vuw} = convert_func(default_value)\n'
            nuzb__uxa += f'  if not null_tup[{sacm__vuw}]:\n'
            nuzb__uxa += (
                f'    val_{sacm__vuw} = convert_func(data_tup[{sacm__vuw}])\n')
        eorb__xoy = ', '.join(f'val_{sacm__vuw}' for sacm__vuw in range(len
            (winhs__jgnmx)))
        nuzb__uxa += f'  vals_tup = ({eorb__xoy},)\n'
        nuzb__uxa += """  res_tup = bodo.libs.nullable_tuple_ext.build_nullable_tuple(vals_tup, null_tup)
"""
        nuzb__uxa += '  return res_tup\n'
        clkxi__cws = {}
        rvcq__asyfu = fqg__coiup[nb_dtype]
        vtpx__yqr = wdvt__mgedb[nb_dtype]
        exec(nuzb__uxa, {'bodo': bodo, 'np': np, 'pd': pd, 'default_value':
            vtpx__yqr, 'convert_func': rvcq__asyfu}, clkxi__cws)
        impl = clkxi__cws['impl']
        return impl
    if _is_str_dtype(new_dtype):
        if isinstance(data.dtype, types.Integer):

            def impl_int_str(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                numba.parfors.parfor.init_prange()
                bna__ayjo = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(bna__ayjo, -1)
                for mmk__ghhg in numba.parfors.parfor.internal_prange(bna__ayjo
                    ):
                    if bodo.libs.array_kernels.isna(data, mmk__ghhg):
                        if nan_to_str:
                            bodo.libs.str_arr_ext.str_arr_setitem_NA_str(A,
                                mmk__ghhg)
                        else:
                            bodo.libs.array_kernels.setna(A, mmk__ghhg)
                    else:
                        bodo.libs.str_arr_ext.str_arr_setitem_int_to_str(A,
                            mmk__ghhg, data[mmk__ghhg])
                return A
            return impl_int_str
        if data.dtype == bytes_type:

            def impl_binary(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                numba.parfors.parfor.init_prange()
                bna__ayjo = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(bna__ayjo, -1)
                for mmk__ghhg in numba.parfors.parfor.internal_prange(bna__ayjo
                    ):
                    if bodo.libs.array_kernels.isna(data, mmk__ghhg):
                        bodo.libs.array_kernels.setna(A, mmk__ghhg)
                    else:
                        A[mmk__ghhg] = ''.join([chr(dmjb__qio) for
                            dmjb__qio in data[mmk__ghhg]])
                return A
            return impl_binary
        if is_overload_true(from_series) and data.dtype in (bodo.
            datetime64ns, bodo.timedelta64ns):

            def impl_str_dt_series(data, new_dtype, copy=None, nan_to_str=
                True, from_series=False):
                numba.parfors.parfor.init_prange()
                bna__ayjo = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(bna__ayjo, -1)
                for mmk__ghhg in numba.parfors.parfor.internal_prange(bna__ayjo
                    ):
                    if bodo.libs.array_kernels.isna(data, mmk__ghhg):
                        if nan_to_str:
                            A[mmk__ghhg] = 'NaT'
                        else:
                            bodo.libs.array_kernels.setna(A, mmk__ghhg)
                        continue
                    A[mmk__ghhg] = str(box_if_dt64(data[mmk__ghhg]))
                return A
            return impl_str_dt_series
        else:

            def impl_str_array(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                numba.parfors.parfor.init_prange()
                bna__ayjo = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(bna__ayjo, -1)
                for mmk__ghhg in numba.parfors.parfor.internal_prange(bna__ayjo
                    ):
                    if bodo.libs.array_kernels.isna(data, mmk__ghhg):
                        if nan_to_str:
                            A[mmk__ghhg] = 'nan'
                        else:
                            bodo.libs.array_kernels.setna(A, mmk__ghhg)
                        continue
                    A[mmk__ghhg] = str(data[mmk__ghhg])
                return A
            return impl_str_array
    if isinstance(new_dtype, bodo.hiframes.pd_categorical_ext.
        PDCategoricalDtype):

        def impl_cat_dtype(data, new_dtype, copy=None, nan_to_str=True,
            from_series=False):
            bna__ayjo = len(data)
            numba.parfors.parfor.init_prange()
            ozwin__epe = (bodo.hiframes.pd_categorical_ext.
                get_label_dict_from_categories(new_dtype.categories.values))
            A = bodo.hiframes.pd_categorical_ext.alloc_categorical_array(
                bna__ayjo, new_dtype)
            bwjkk__eep = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A))
            for sacm__vuw in numba.parfors.parfor.internal_prange(bna__ayjo):
                if bodo.libs.array_kernels.isna(data, sacm__vuw):
                    bodo.libs.array_kernels.setna(A, sacm__vuw)
                    continue
                val = data[sacm__vuw]
                if val not in ozwin__epe:
                    bodo.libs.array_kernels.setna(A, sacm__vuw)
                    continue
                bwjkk__eep[sacm__vuw] = ozwin__epe[val]
            return A
        return impl_cat_dtype
    if is_overload_constant_str(new_dtype) and get_overload_const_str(new_dtype
        ) == 'category':

        def impl_category(data, new_dtype, copy=None, nan_to_str=True,
            from_series=False):
            aiieg__pdelv = bodo.libs.array_kernels.unique(data, dropna=True)
            aiieg__pdelv = pd.Series(aiieg__pdelv).sort_values().values
            aiieg__pdelv = bodo.allgatherv(aiieg__pdelv, False)
            pbdu__gznmm = bodo.hiframes.pd_categorical_ext.init_cat_dtype(bodo
                .utils.conversion.index_from_array(aiieg__pdelv, None), 
                False, None, None)
            bna__ayjo = len(data)
            numba.parfors.parfor.init_prange()
            ozwin__epe = (bodo.hiframes.pd_categorical_ext.
                get_label_dict_from_categories_no_duplicates(aiieg__pdelv))
            A = bodo.hiframes.pd_categorical_ext.alloc_categorical_array(
                bna__ayjo, pbdu__gznmm)
            bwjkk__eep = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A))
            for sacm__vuw in numba.parfors.parfor.internal_prange(bna__ayjo):
                if bodo.libs.array_kernels.isna(data, sacm__vuw):
                    bodo.libs.array_kernels.setna(A, sacm__vuw)
                    continue
                val = data[sacm__vuw]
                bwjkk__eep[sacm__vuw] = ozwin__epe[val]
            return A
        return impl_category
    nb_dtype = bodo.utils.typing.parse_dtype(new_dtype)
    if isinstance(data, bodo.libs.int_arr_ext.IntegerArrayType):
        cwig__akwuf = isinstance(nb_dtype, bodo.libs.int_arr_ext.IntDtype
            ) and data.dtype == nb_dtype.dtype
    else:
        cwig__akwuf = data.dtype == nb_dtype
    if xce__jjfmo and cwig__akwuf:
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data.copy())
    if cwig__akwuf:
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data)
    if isinstance(nb_dtype, bodo.libs.int_arr_ext.IntDtype):
        if isinstance(nb_dtype, types.Integer):
            jjniy__crx = nb_dtype
        else:
            jjniy__crx = nb_dtype.dtype
        if isinstance(data.dtype, types.Float):

            def impl_float(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                bna__ayjo = len(data)
                numba.parfors.parfor.init_prange()
                quz__puwe = bodo.libs.int_arr_ext.alloc_int_array(bna__ayjo,
                    jjniy__crx)
                for sacm__vuw in numba.parfors.parfor.internal_prange(bna__ayjo
                    ):
                    if bodo.libs.array_kernels.isna(data, sacm__vuw):
                        bodo.libs.array_kernels.setna(quz__puwe, sacm__vuw)
                    else:
                        quz__puwe[sacm__vuw] = int(data[sacm__vuw])
                return quz__puwe
            return impl_float
        else:
            if data == bodo.dict_str_arr_type:

                def impl_dict(data, new_dtype, copy=None, nan_to_str=True,
                    from_series=False):
                    return bodo.libs.dict_arr_ext.convert_dict_arr_to_int(data,
                        jjniy__crx)
                return impl_dict

            def impl(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                bna__ayjo = len(data)
                numba.parfors.parfor.init_prange()
                quz__puwe = bodo.libs.int_arr_ext.alloc_int_array(bna__ayjo,
                    jjniy__crx)
                for sacm__vuw in numba.parfors.parfor.internal_prange(bna__ayjo
                    ):
                    if bodo.libs.array_kernels.isna(data, sacm__vuw):
                        bodo.libs.array_kernels.setna(quz__puwe, sacm__vuw)
                    else:
                        quz__puwe[sacm__vuw] = np.int64(data[sacm__vuw])
                return quz__puwe
            return impl
    if isinstance(nb_dtype, types.Integer) and isinstance(data.dtype, types
        .Integer):

        def impl(data, new_dtype, copy=None, nan_to_str=True, from_series=False
            ):
            return data.astype(nb_dtype)
        return impl
    if nb_dtype == bodo.libs.bool_arr_ext.boolean_dtype:

        def impl_bool(data, new_dtype, copy=None, nan_to_str=True,
            from_series=False):
            bna__ayjo = len(data)
            numba.parfors.parfor.init_prange()
            quz__puwe = bodo.libs.bool_arr_ext.alloc_bool_array(bna__ayjo)
            for sacm__vuw in numba.parfors.parfor.internal_prange(bna__ayjo):
                if bodo.libs.array_kernels.isna(data, sacm__vuw):
                    bodo.libs.array_kernels.setna(quz__puwe, sacm__vuw)
                else:
                    quz__puwe[sacm__vuw] = bool(data[sacm__vuw])
            return quz__puwe
        return impl_bool
    if nb_dtype == bodo.datetime_date_type:
        if data.dtype == bodo.datetime64ns:

            def impl_date(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                bna__ayjo = len(data)
                tkjs__dfmy = (bodo.hiframes.datetime_date_ext.
                    alloc_datetime_date_array(bna__ayjo))
                for sacm__vuw in numba.parfors.parfor.internal_prange(bna__ayjo
                    ):
                    if bodo.libs.array_kernels.isna(data, sacm__vuw):
                        bodo.libs.array_kernels.setna(tkjs__dfmy, sacm__vuw)
                    else:
                        tkjs__dfmy[sacm__vuw
                            ] = bodo.utils.conversion.box_if_dt64(data[
                            sacm__vuw]).date()
                return tkjs__dfmy
            return impl_date
    if nb_dtype == bodo.datetime64ns:
        if data.dtype == bodo.string_type:

            def impl_str(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                return bodo.hiframes.pd_timestamp_ext.series_str_dt64_astype(
                    data)
            return impl_str
        if data == bodo.datetime_date_array_type:

            def impl_date(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                return (bodo.hiframes.pd_timestamp_ext.
                    datetime_date_arr_to_dt64_arr(data))
            return impl_date
        if isinstance(data.dtype, types.Number) or data.dtype in [bodo.
            timedelta64ns, types.bool_]:

            def impl_numeric(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                bna__ayjo = len(data)
                numba.parfors.parfor.init_prange()
                tkjs__dfmy = np.empty(bna__ayjo, dtype=np.dtype(
                    'datetime64[ns]'))
                for sacm__vuw in numba.parfors.parfor.internal_prange(bna__ayjo
                    ):
                    if bodo.libs.array_kernels.isna(data, sacm__vuw):
                        bodo.libs.array_kernels.setna(tkjs__dfmy, sacm__vuw)
                    else:
                        tkjs__dfmy[sacm__vuw
                            ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                            np.int64(data[sacm__vuw]))
                return tkjs__dfmy
            return impl_numeric
    if nb_dtype == bodo.timedelta64ns:
        if data.dtype == bodo.string_type:

            def impl_str(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                return bodo.hiframes.pd_timestamp_ext.series_str_td64_astype(
                    data)
            return impl_str
        if isinstance(data.dtype, types.Number) or data.dtype in [bodo.
            datetime64ns, types.bool_]:
            if xce__jjfmo:

                def impl_numeric(data, new_dtype, copy=None, nan_to_str=
                    True, from_series=False):
                    bna__ayjo = len(data)
                    numba.parfors.parfor.init_prange()
                    tkjs__dfmy = np.empty(bna__ayjo, dtype=np.dtype(
                        'timedelta64[ns]'))
                    for sacm__vuw in numba.parfors.parfor.internal_prange(
                        bna__ayjo):
                        if bodo.libs.array_kernels.isna(data, sacm__vuw):
                            bodo.libs.array_kernels.setna(tkjs__dfmy, sacm__vuw
                                )
                        else:
                            tkjs__dfmy[sacm__vuw] = (bodo.hiframes.
                                pd_timestamp_ext.integer_to_timedelta64(np.
                                int64(data[sacm__vuw])))
                    return tkjs__dfmy
                return impl_numeric
            else:
                return (lambda data, new_dtype, copy=None, nan_to_str=True,
                    from_series=False: data.view('int64'))
    if nb_dtype == types.int64 and data.dtype in [bodo.datetime64ns, bodo.
        timedelta64ns]:

        def impl_datelike_to_integer(data, new_dtype, copy=None, nan_to_str
            =True, from_series=False):
            bna__ayjo = len(data)
            numba.parfors.parfor.init_prange()
            A = np.empty(bna__ayjo, types.int64)
            for sacm__vuw in numba.parfors.parfor.internal_prange(bna__ayjo):
                if bodo.libs.array_kernels.isna(data, sacm__vuw):
                    bodo.libs.array_kernels.setna(A, sacm__vuw)
                else:
                    A[sacm__vuw] = np.int64(data[sacm__vuw])
            return A
        return impl_datelike_to_integer
    if data.dtype != nb_dtype:
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data.astype(nb_dtype))
    raise BodoError(f'Conversion from {data} to {new_dtype} not supported yet')


def array_type_from_dtype(dtype):
    return dtype_to_array_type(bodo.utils.typing.parse_dtype(dtype))


@overload(array_type_from_dtype)
def overload_array_type_from_dtype(dtype):
    arr_type = dtype_to_array_type(bodo.utils.typing.parse_dtype(dtype))
    return lambda dtype: arr_type


@numba.jit
def flatten_array(A):
    wixxb__hcghg = []
    bna__ayjo = len(A)
    for sacm__vuw in range(bna__ayjo):
        zaz__qjtit = A[sacm__vuw]
        for vmyzb__mvejo in zaz__qjtit:
            wixxb__hcghg.append(vmyzb__mvejo)
    return bodo.utils.conversion.coerce_to_array(wixxb__hcghg)


def parse_datetimes_from_strings(data):
    return data


@overload(parse_datetimes_from_strings, no_unliteral=True)
def overload_parse_datetimes_from_strings(data):
    assert is_str_arr_type(data
        ), 'parse_datetimes_from_strings: string array expected'

    def parse_impl(data):
        numba.parfors.parfor.init_prange()
        bna__ayjo = len(data)
        vps__jfacj = np.empty(bna__ayjo, bodo.utils.conversion.NS_DTYPE)
        for sacm__vuw in numba.parfors.parfor.internal_prange(bna__ayjo):
            vps__jfacj[sacm__vuw
                ] = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(data[
                sacm__vuw])
        return vps__jfacj
    return parse_impl


def convert_to_dt64ns(data):
    return data


@overload(convert_to_dt64ns, no_unliteral=True)
def overload_convert_to_dt64ns(data):
    if data == bodo.hiframes.datetime_date_ext.datetime_date_array_type:
        return (lambda data: bodo.hiframes.pd_timestamp_ext.
            datetime_date_arr_to_dt64_arr(data))
    if is_np_arr_typ(data, types.int64):
        return lambda data: data.view(bodo.utils.conversion.NS_DTYPE)
    if is_np_arr_typ(data, types.NPDatetime('ns')):
        return lambda data: data
    if is_str_arr_type(data):
        return lambda data: bodo.utils.conversion.parse_datetimes_from_strings(
            data)
    raise BodoError(f'invalid data type {data} for dt64 conversion')


def convert_to_td64ns(data):
    return data


@overload(convert_to_td64ns, no_unliteral=True)
def overload_convert_to_td64ns(data):
    if is_np_arr_typ(data, types.int64):
        return lambda data: data.view(bodo.utils.conversion.TD_DTYPE)
    if is_np_arr_typ(data, types.NPTimedelta('ns')):
        return lambda data: data
    if is_str_arr_type(data):
        raise BodoError('conversion to timedelta from string not supported yet'
            )
    raise BodoError(f'invalid data type {data} for timedelta64 conversion')


def convert_to_index(data, name=None):
    return data


@overload(convert_to_index, no_unliteral=True)
def overload_convert_to_index(data, name=None):
    from bodo.hiframes.pd_index_ext import BinaryIndexType, CategoricalIndexType, DatetimeIndexType, NumericIndexType, PeriodIndexType, RangeIndexType, StringIndexType, TimedeltaIndexType
    if isinstance(data, (RangeIndexType, NumericIndexType,
        DatetimeIndexType, TimedeltaIndexType, StringIndexType,
        BinaryIndexType, CategoricalIndexType, PeriodIndexType, types.NoneType)
        ):
        return lambda data, name=None: data

    def impl(data, name=None):
        mqeku__pzvr = bodo.utils.conversion.coerce_to_array(data)
        return bodo.utils.conversion.index_from_array(mqeku__pzvr, name)
    return impl


def force_convert_index(I1, I2):
    return I2


@overload(force_convert_index, no_unliteral=True)
def overload_force_convert_index(I1, I2):
    from bodo.hiframes.pd_index_ext import RangeIndexType
    if isinstance(I2, RangeIndexType):
        return lambda I1, I2: pd.RangeIndex(len(I1._data))
    return lambda I1, I2: I1


def index_from_array(data, name=None):
    return data


@overload(index_from_array, no_unliteral=True)
def overload_index_from_array(data, name=None):
    if data in [bodo.string_array_type, bodo.binary_array_type]:
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_binary_str_index(data, name))
    if data == bodo.dict_str_arr_type:
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_binary_str_index(decode_if_dict_array(data), name))
    if (data == bodo.hiframes.datetime_date_ext.datetime_date_array_type or
        data.dtype == types.NPDatetime('ns')):
        return lambda data, name=None: pd.DatetimeIndex(data, name=name)
    if data.dtype == types.NPTimedelta('ns'):
        return lambda data, name=None: pd.TimedeltaIndex(data, name=name)
    if isinstance(data.dtype, (types.Integer, types.Float, types.Boolean)):
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_numeric_index(data, name))
    if isinstance(data, bodo.libs.interval_arr_ext.IntervalArrayType):
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_interval_index(data, name))
    if isinstance(data, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_categorical_index(data, name))
    if isinstance(data, bodo.libs.pd_datetime_arr_ext.DatetimeArrayType):
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_datetime_index(data, name))
    raise BodoError(f'cannot convert {data} to Index')


def index_to_array(data):
    return data


@overload(index_to_array, no_unliteral=True)
def overload_index_to_array(I):
    from bodo.hiframes.pd_index_ext import RangeIndexType
    if isinstance(I, RangeIndexType):
        return lambda I: np.arange(I._start, I._stop, I._step)
    return lambda I: bodo.hiframes.pd_index_ext.get_index_data(I)


def false_if_none(val):
    return False if val is None else val


@overload(false_if_none, no_unliteral=True)
def overload_false_if_none(val):
    if is_overload_none(val):
        return lambda val: False
    return lambda val: val


def extract_name_if_none(data, name):
    return name


@overload(extract_name_if_none, no_unliteral=True)
def overload_extract_name_if_none(data, name):
    from bodo.hiframes.pd_index_ext import CategoricalIndexType, DatetimeIndexType, NumericIndexType, PeriodIndexType, TimedeltaIndexType
    from bodo.hiframes.pd_series_ext import SeriesType
    if not is_overload_none(name):
        return lambda data, name: name
    if isinstance(data, (NumericIndexType, DatetimeIndexType,
        TimedeltaIndexType, PeriodIndexType, CategoricalIndexType)):
        return lambda data, name: bodo.hiframes.pd_index_ext.get_index_name(
            data)
    if isinstance(data, SeriesType):
        return lambda data, name: bodo.hiframes.pd_series_ext.get_series_name(
            data)
    return lambda data, name: name


def extract_index_if_none(data, index):
    return index


@overload(extract_index_if_none, no_unliteral=True)
def overload_extract_index_if_none(data, index):
    from bodo.hiframes.pd_series_ext import SeriesType
    if not is_overload_none(index):
        return lambda data, index: index
    if isinstance(data, SeriesType):
        return (lambda data, index: bodo.hiframes.pd_series_ext.
            get_series_index(data))
    return lambda data, index: bodo.hiframes.pd_index_ext.init_range_index(
        0, len(data), 1, None)


def box_if_dt64(val):
    return val


@overload(box_if_dt64, no_unliteral=True)
def overload_box_if_dt64(val):
    if val == types.NPDatetime('ns'):
        return (lambda val: bodo.hiframes.pd_timestamp_ext.
            convert_datetime64_to_timestamp(val))
    if val == types.NPTimedelta('ns'):
        return (lambda val: bodo.hiframes.pd_timestamp_ext.
            convert_numpy_timedelta64_to_pd_timedelta(val))
    return lambda val: val


def unbox_if_timestamp(val):
    return val


@overload(unbox_if_timestamp, no_unliteral=True)
def overload_unbox_if_timestamp(val):
    if val == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
        return lambda val: bodo.hiframes.pd_timestamp_ext.integer_to_dt64(val
            .value)
    if val == bodo.hiframes.datetime_datetime_ext.datetime_datetime_type:
        return lambda val: bodo.hiframes.pd_timestamp_ext.integer_to_dt64(pd
            .Timestamp(val).value)
    if val == bodo.hiframes.datetime_timedelta_ext.pd_timedelta_type:
        return (lambda val: bodo.hiframes.pd_timestamp_ext.
            integer_to_timedelta64(val.value))
    if val == types.Optional(bodo.hiframes.pd_timestamp_ext.pd_timestamp_type):

        def impl_optional(val):
            if val is None:
                vfg__uglsu = None
            else:
                vfg__uglsu = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                    bodo.utils.indexing.unoptional(val).value)
            return vfg__uglsu
        return impl_optional
    if val == types.Optional(bodo.hiframes.datetime_timedelta_ext.
        pd_timedelta_type):

        def impl_optional_td(val):
            if val is None:
                vfg__uglsu = None
            else:
                vfg__uglsu = (bodo.hiframes.pd_timestamp_ext.
                    integer_to_timedelta64(bodo.utils.indexing.unoptional(
                    val).value))
            return vfg__uglsu
        return impl_optional_td
    return lambda val: val


def to_tuple(val):
    return val


@overload(to_tuple, no_unliteral=True)
def overload_to_tuple(val):
    if not isinstance(val, types.BaseTuple) and is_overload_constant_list(val):
        jesk__mbs = len(val.types if isinstance(val, types.LiteralList) else
            get_overload_const_list(val))
        nuzb__uxa = 'def f(val):\n'
        nfu__agjf = ','.join(f'val[{sacm__vuw}]' for sacm__vuw in range(
            jesk__mbs))
        nuzb__uxa += f'  return ({nfu__agjf},)\n'
        clkxi__cws = {}
        exec(nuzb__uxa, {}, clkxi__cws)
        impl = clkxi__cws['f']
        return impl
    assert isinstance(val, types.BaseTuple), 'tuple type expected'
    return lambda val: val


def get_array_if_series_or_index(data):
    return data


@overload(get_array_if_series_or_index)
def overload_get_array_if_series_or_index(data):
    from bodo.hiframes.pd_series_ext import SeriesType
    if isinstance(data, SeriesType):
        return lambda data: bodo.hiframes.pd_series_ext.get_series_data(data)
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):
        return lambda data: bodo.utils.conversion.coerce_to_array(data)
    if isinstance(data, bodo.hiframes.pd_index_ext.HeterogeneousIndexType):
        if not is_heterogeneous_tuple_type(data.data):

            def impl(data):
                uez__cqs = bodo.hiframes.pd_index_ext.get_index_data(data)
                return bodo.utils.conversion.coerce_to_array(uez__cqs)
            return impl

        def impl(data):
            return bodo.hiframes.pd_index_ext.get_index_data(data)
        return impl
    return lambda data: data


def extract_index_array(A):
    return np.arange(len(A))


@overload(extract_index_array, no_unliteral=True)
def overload_extract_index_array(A):
    from bodo.hiframes.pd_series_ext import SeriesType
    if isinstance(A, SeriesType):

        def impl(A):
            index = bodo.hiframes.pd_series_ext.get_series_index(A)
            sbyn__bwcrr = bodo.utils.conversion.coerce_to_array(index)
            return sbyn__bwcrr
        return impl
    return lambda A: np.arange(len(A))


def ensure_contig_if_np(arr):
    return np.ascontiguousarray(arr)


@overload(ensure_contig_if_np, no_unliteral=True)
def overload_ensure_contig_if_np(arr):
    if isinstance(arr, types.Array):
        return lambda arr: np.ascontiguousarray(arr)
    return lambda arr: arr


def struct_if_heter_dict(values, names):
    return {prl__edud: htbix__ova for prl__edud, htbix__ova in zip(names,
        values)}


@overload(struct_if_heter_dict, no_unliteral=True)
def overload_struct_if_heter_dict(values, names):
    if not types.is_homogeneous(*values.types):
        return lambda values, names: bodo.libs.struct_arr_ext.init_struct(
            values, names)
    pxd__veqq = len(values.types)
    nuzb__uxa = 'def f(values, names):\n'
    nfu__agjf = ','.join("'{}': values[{}]".format(get_overload_const_str(
        names.types[sacm__vuw]), sacm__vuw) for sacm__vuw in range(pxd__veqq))
    nuzb__uxa += '  return {{{}}}\n'.format(nfu__agjf)
    clkxi__cws = {}
    exec(nuzb__uxa, {}, clkxi__cws)
    impl = clkxi__cws['f']
    return impl
