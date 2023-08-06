"""
Collection of utility functions. Needs to be refactored in separate files.
"""
import hashlib
import inspect
import keyword
import re
import warnings
from enum import Enum
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, ir, ir_utils, types
from numba.core.imputils import lower_builtin, lower_constant
from numba.core.ir_utils import find_callname, find_const, get_definition, guard, mk_unique_var, require
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, overload
from numba.np.arrayobj import get_itemsize, make_array, populate_array
import bodo
from bodo.libs.binary_arr_ext import bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import num_total_chars, pre_alloc_string_array, string_array_type
from bodo.libs.str_ext import string_type
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.typing import NOT_CONSTANT, BodoError, BodoWarning, MetaType, is_str_arr_type
int128_type = types.Integer('int128', 128)


class CTypeEnum(Enum):
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
    Date = 13
    Datetime = 14
    Timedelta = 15
    Int128 = 16
    LIST = 18
    STRUCT = 19
    BINARY = 20


_numba_to_c_type_map = {types.int8: CTypeEnum.Int8.value, types.uint8:
    CTypeEnum.UInt8.value, types.int32: CTypeEnum.Int32.value, types.uint32:
    CTypeEnum.UInt32.value, types.int64: CTypeEnum.Int64.value, types.
    uint64: CTypeEnum.UInt64.value, types.float32: CTypeEnum.Float32.value,
    types.float64: CTypeEnum.Float64.value, types.NPDatetime('ns'):
    CTypeEnum.Datetime.value, types.NPTimedelta('ns'): CTypeEnum.Timedelta.
    value, types.bool_: CTypeEnum.Bool.value, types.int16: CTypeEnum.Int16.
    value, types.uint16: CTypeEnum.UInt16.value, int128_type: CTypeEnum.
    Int128.value}
numba.core.errors.error_extras = {'unsupported_error': '', 'typing': '',
    'reportable': '', 'interpreter': '', 'constant_inference': ''}
np_alloc_callnames = 'empty', 'zeros', 'ones', 'full'
CONST_DICT_SLOW_WARN_THRESHOLD = 100
CONST_LIST_SLOW_WARN_THRESHOLD = 100000


def unliteral_all(args):
    return tuple(types.unliteral(a) for a in args)


def get_constant(func_ir, var, default=NOT_CONSTANT):
    seszl__dtau = guard(get_definition, func_ir, var)
    if seszl__dtau is None:
        return default
    if isinstance(seszl__dtau, ir.Const):
        return seszl__dtau.value
    if isinstance(seszl__dtau, ir.Var):
        return get_constant(func_ir, seszl__dtau, default)
    return default


def numba_to_c_type(t):
    if isinstance(t, bodo.libs.decimal_arr_ext.Decimal128Type):
        return CTypeEnum.Decimal.value
    if t == bodo.hiframes.datetime_date_ext.datetime_date_type:
        return CTypeEnum.Date.value
    return _numba_to_c_type_map[t]


def is_alloc_callname(func_name, mod_name):
    return isinstance(mod_name, str) and (mod_name == 'numpy' and func_name in
        np_alloc_callnames or func_name == 'empty_inferred' and mod_name in
        ('numba.extending', 'numba.np.unsafe.ndarray') or func_name ==
        'pre_alloc_string_array' and mod_name == 'bodo.libs.str_arr_ext' or
        func_name == 'pre_alloc_binary_array' and mod_name ==
        'bodo.libs.binary_arr_ext' or func_name ==
        'alloc_random_access_string_array' and mod_name ==
        'bodo.libs.str_ext' or func_name == 'pre_alloc_array_item_array' and
        mod_name == 'bodo.libs.array_item_arr_ext' or func_name ==
        'pre_alloc_struct_array' and mod_name == 'bodo.libs.struct_arr_ext' or
        func_name == 'pre_alloc_map_array' and mod_name ==
        'bodo.libs.map_arr_ext' or func_name == 'pre_alloc_tuple_array' and
        mod_name == 'bodo.libs.tuple_arr_ext' or func_name ==
        'alloc_bool_array' and mod_name == 'bodo.libs.bool_arr_ext' or 
        func_name == 'alloc_int_array' and mod_name ==
        'bodo.libs.int_arr_ext' or func_name == 'alloc_datetime_date_array' and
        mod_name == 'bodo.hiframes.datetime_date_ext' or func_name ==
        'alloc_datetime_timedelta_array' and mod_name ==
        'bodo.hiframes.datetime_timedelta_ext' or func_name ==
        'alloc_decimal_array' and mod_name == 'bodo.libs.decimal_arr_ext' or
        func_name == 'alloc_categorical_array' and mod_name ==
        'bodo.hiframes.pd_categorical_ext' or func_name == 'gen_na_array' and
        mod_name == 'bodo.libs.array_kernels')


def find_build_tuple(func_ir, var):
    require(isinstance(var, (ir.Var, str)))
    mqwcv__pyemz = get_definition(func_ir, var)
    require(isinstance(mqwcv__pyemz, ir.Expr))
    require(mqwcv__pyemz.op == 'build_tuple')
    return mqwcv__pyemz.items


def cprint(*s):
    print(*s)


@infer_global(cprint)
class CprintInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.none, *unliteral_all(args))


typ_to_format = {types.int32: 'd', types.uint32: 'u', types.int64: 'lld',
    types.uint64: 'llu', types.float32: 'f', types.float64: 'lf', types.
    voidptr: 's'}


@lower_builtin(cprint, types.VarArg(types.Any))
def cprint_lower(context, builder, sig, args):
    for eyqr__dxgb, val in enumerate(args):
        typ = sig.args[eyqr__dxgb]
        if isinstance(typ, types.ArrayCTypes):
            cgutils.printf(builder, '%p ', val)
            continue
        xts__yrtys = typ_to_format[typ]
        cgutils.printf(builder, '%{} '.format(xts__yrtys), val)
    cgutils.printf(builder, '\n')
    return context.get_dummy_value()


def is_whole_slice(typemap, func_ir, var, accept_stride=False):
    require(typemap[var.name] == types.slice2_type or accept_stride and 
        typemap[var.name] == types.slice3_type)
    tcs__his = get_definition(func_ir, var)
    require(isinstance(tcs__his, ir.Expr) and tcs__his.op == 'call')
    assert len(tcs__his.args) == 2 or accept_stride and len(tcs__his.args) == 3
    assert find_callname(func_ir, tcs__his) == ('slice', 'builtins')
    zwtg__ywgml = get_definition(func_ir, tcs__his.args[0])
    lgl__qvb = get_definition(func_ir, tcs__his.args[1])
    require(isinstance(zwtg__ywgml, ir.Const) and zwtg__ywgml.value == None)
    require(isinstance(lgl__qvb, ir.Const) and lgl__qvb.value == None)
    return True


def is_slice_equiv_arr(arr_var, index_var, func_ir, equiv_set,
    accept_stride=False):
    qtsuo__psfy = get_definition(func_ir, index_var)
    require(find_callname(func_ir, qtsuo__psfy) == ('slice', 'builtins'))
    require(len(qtsuo__psfy.args) in (2, 3))
    require(find_const(func_ir, qtsuo__psfy.args[0]) in (0, None))
    require(equiv_set.is_equiv(qtsuo__psfy.args[1], arr_var.name + '#0'))
    require(accept_stride or len(qtsuo__psfy.args) == 2 or find_const(
        func_ir, qtsuo__psfy.args[2]) == 1)
    return True


def get_slice_step(typemap, func_ir, var):
    require(typemap[var.name] == types.slice3_type)
    tcs__his = get_definition(func_ir, var)
    require(isinstance(tcs__his, ir.Expr) and tcs__his.op == 'call')
    assert len(tcs__his.args) == 3
    return tcs__his.args[2]


def is_array_typ(var_typ, include_index_series=True):
    return is_np_array_typ(var_typ) or var_typ in (string_array_type, bodo.
        binary_array_type, bodo.dict_str_arr_type, bodo.hiframes.split_impl
        .string_array_split_view_type, bodo.hiframes.datetime_date_ext.
        datetime_date_array_type, bodo.hiframes.datetime_timedelta_ext.
        datetime_timedelta_array_type, boolean_array, bodo.libs.str_ext.
        random_access_string_array) or isinstance(var_typ, (
        IntegerArrayType, bodo.libs.decimal_arr_ext.DecimalArrayType, bodo.
        hiframes.pd_categorical_ext.CategoricalArrayType, bodo.libs.
        array_item_arr_ext.ArrayItemArrayType, bodo.libs.struct_arr_ext.
        StructArrayType, bodo.libs.interval_arr_ext.IntervalArrayType, bodo
        .libs.tuple_arr_ext.TupleArrayType, bodo.libs.map_arr_ext.
        MapArrayType, bodo.libs.csr_matrix_ext.CSRMatrixType, bodo.
        DatetimeArrayType)) or include_index_series and (isinstance(var_typ,
        (bodo.hiframes.pd_series_ext.SeriesType, bodo.hiframes.
        pd_multi_index_ext.MultiIndexType)) or bodo.hiframes.pd_index_ext.
        is_pd_index_type(var_typ))


def is_np_array_typ(var_typ):
    return isinstance(var_typ, types.Array)


def is_distributable_typ(var_typ):
    return is_array_typ(var_typ) or isinstance(var_typ, bodo.hiframes.table
        .TableType) or isinstance(var_typ, bodo.hiframes.pd_dataframe_ext.
        DataFrameType) or isinstance(var_typ, types.List
        ) and is_distributable_typ(var_typ.dtype) or isinstance(var_typ,
        types.DictType) and is_distributable_typ(var_typ.value_type)


def is_distributable_tuple_typ(var_typ):
    return isinstance(var_typ, types.BaseTuple) and any(
        is_distributable_typ(t) or is_distributable_tuple_typ(t) for t in
        var_typ.types) or isinstance(var_typ, types.List
        ) and is_distributable_tuple_typ(var_typ.dtype) or isinstance(var_typ,
        types.DictType) and is_distributable_tuple_typ(var_typ.value_type
        ) or isinstance(var_typ, types.iterators.EnumerateType) and (
        is_distributable_typ(var_typ.yield_type[1]) or
        is_distributable_tuple_typ(var_typ.yield_type[1]))


@numba.generated_jit(nopython=True, cache=True)
def build_set_seen_na(A):

    def impl(A):
        s = dict()
        eenim__hvlau = False
        for eyqr__dxgb in range(len(A)):
            if bodo.libs.array_kernels.isna(A, eyqr__dxgb):
                eenim__hvlau = True
                continue
            s[A[eyqr__dxgb]] = 0
        return s, eenim__hvlau
    return impl


def empty_like_type(n, arr):
    return np.empty(n, arr.dtype)


@overload(empty_like_type, no_unliteral=True)
def empty_like_type_overload(n, arr):
    if isinstance(arr, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        return (lambda n, arr: bodo.hiframes.pd_categorical_ext.
            alloc_categorical_array(n, arr.dtype))
    if isinstance(arr, types.Array):
        return lambda n, arr: np.empty(n, arr.dtype)
    if isinstance(arr, types.List) and arr.dtype == string_type:

        def empty_like_type_str_list(n, arr):
            return [''] * n
        return empty_like_type_str_list
    if isinstance(arr, types.List) and arr.dtype == bytes_type:

        def empty_like_type_binary_list(n, arr):
            return [b''] * n
        return empty_like_type_binary_list
    if isinstance(arr, IntegerArrayType):
        gmp__aztx = arr.dtype

        def empty_like_type_int_arr(n, arr):
            return bodo.libs.int_arr_ext.alloc_int_array(n, gmp__aztx)
        return empty_like_type_int_arr
    if arr == boolean_array:

        def empty_like_type_bool_arr(n, arr):
            return bodo.libs.bool_arr_ext.alloc_bool_array(n)
        return empty_like_type_bool_arr
    if arr == bodo.hiframes.datetime_date_ext.datetime_date_array_type:

        def empty_like_type_datetime_date_arr(n, arr):
            return bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(n)
        return empty_like_type_datetime_date_arr
    if (arr == bodo.hiframes.datetime_timedelta_ext.
        datetime_timedelta_array_type):

        def empty_like_type_datetime_timedelta_arr(n, arr):
            return (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(n))
        return empty_like_type_datetime_timedelta_arr
    if isinstance(arr, bodo.libs.decimal_arr_ext.DecimalArrayType):
        precision = arr.precision
        scale = arr.scale

        def empty_like_type_decimal_arr(n, arr):
            return bodo.libs.decimal_arr_ext.alloc_decimal_array(n,
                precision, scale)
        return empty_like_type_decimal_arr
    assert arr == string_array_type

    def empty_like_type_str_arr(n, arr):
        cxwc__zndq = 20
        if len(arr) != 0:
            cxwc__zndq = num_total_chars(arr) // len(arr)
        return pre_alloc_string_array(n, n * cxwc__zndq)
    return empty_like_type_str_arr


def _empty_nd_impl(context, builder, arrtype, shapes):
    ypyf__ouxj = make_array(arrtype)
    rjcj__ougz = ypyf__ouxj(context, builder)
    khdd__phkws = context.get_data_type(arrtype.dtype)
    fnxex__ibl = context.get_constant(types.intp, get_itemsize(context,
        arrtype))
    abpax__tdf = context.get_constant(types.intp, 1)
    brr__sxuz = lir.Constant(lir.IntType(1), 0)
    for s in shapes:
        fuos__cewk = builder.smul_with_overflow(abpax__tdf, s)
        abpax__tdf = builder.extract_value(fuos__cewk, 0)
        brr__sxuz = builder.or_(brr__sxuz, builder.extract_value(fuos__cewk, 1)
            )
    if arrtype.ndim == 0:
        zmhxn__gadiu = ()
    elif arrtype.layout == 'C':
        zmhxn__gadiu = [fnxex__ibl]
        for guhaf__bou in reversed(shapes[1:]):
            zmhxn__gadiu.append(builder.mul(zmhxn__gadiu[-1], guhaf__bou))
        zmhxn__gadiu = tuple(reversed(zmhxn__gadiu))
    elif arrtype.layout == 'F':
        zmhxn__gadiu = [fnxex__ibl]
        for guhaf__bou in shapes[:-1]:
            zmhxn__gadiu.append(builder.mul(zmhxn__gadiu[-1], guhaf__bou))
        zmhxn__gadiu = tuple(zmhxn__gadiu)
    else:
        raise NotImplementedError(
            "Don't know how to allocate array with layout '{0}'.".format(
            arrtype.layout))
    hejnz__iis = builder.smul_with_overflow(abpax__tdf, fnxex__ibl)
    lesd__pvpf = builder.extract_value(hejnz__iis, 0)
    brr__sxuz = builder.or_(brr__sxuz, builder.extract_value(hejnz__iis, 1))
    with builder.if_then(brr__sxuz, likely=False):
        cgutils.printf(builder,
            'array is too big; `arr.size * arr.dtype.itemsize` is larger than the maximum possible size.'
            )
    dtype = arrtype.dtype
    ffi__nyj = context.get_preferred_array_alignment(dtype)
    wjun__mlih = context.get_constant(types.uint32, ffi__nyj)
    aef__qtjt = context.nrt.meminfo_alloc_aligned(builder, size=lesd__pvpf,
        align=wjun__mlih)
    data = context.nrt.meminfo_data(builder, aef__qtjt)
    knomy__swscg = context.get_value_type(types.intp)
    upt__mfu = cgutils.pack_array(builder, shapes, ty=knomy__swscg)
    pjle__cljd = cgutils.pack_array(builder, zmhxn__gadiu, ty=knomy__swscg)
    populate_array(rjcj__ougz, data=builder.bitcast(data, khdd__phkws.
        as_pointer()), shape=upt__mfu, strides=pjle__cljd, itemsize=
        fnxex__ibl, meminfo=aef__qtjt)
    return rjcj__ougz


if bodo.numba_compat._check_numba_change:
    lines = inspect.getsource(numba.np.arrayobj._empty_nd_impl)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b6a998927680caa35917a553c79704e9d813d8f1873d83a5f8513837c159fa29':
        warnings.warn('numba.np.arrayobj._empty_nd_impl has changed')


def alloc_arr_tup(n, arr_tup, init_vals=()):
    dqrt__uvf = []
    for fxjyz__zjjoz in arr_tup:
        dqrt__uvf.append(np.empty(n, fxjyz__zjjoz.dtype))
    return tuple(dqrt__uvf)


@overload(alloc_arr_tup, no_unliteral=True)
def alloc_arr_tup_overload(n, data, init_vals=()):
    kunj__kpbwt = data.count
    czk__kij = ','.join(['empty_like_type(n, data[{}])'.format(eyqr__dxgb) for
        eyqr__dxgb in range(kunj__kpbwt)])
    if init_vals != ():
        czk__kij = ','.join(['np.full(n, init_vals[{}], data[{}].dtype)'.
            format(eyqr__dxgb, eyqr__dxgb) for eyqr__dxgb in range(
            kunj__kpbwt)])
    gmdu__rmb = 'def f(n, data, init_vals=()):\n'
    gmdu__rmb += '  return ({}{})\n'.format(czk__kij, ',' if kunj__kpbwt ==
        1 else '')
    csdo__cec = {}
    exec(gmdu__rmb, {'empty_like_type': empty_like_type, 'np': np}, csdo__cec)
    yeoqa__snp = csdo__cec['f']
    return yeoqa__snp


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def tuple_to_scalar(n):
    if isinstance(n, types.BaseTuple) and len(n.types) == 1:
        return lambda n: n[0]
    return lambda n: n


def alloc_type(n, t, s=None):
    return np.empty(n, t.dtype)


@overload(alloc_type)
def overload_alloc_type(n, t, s=None):
    typ = t.instance_type if isinstance(t, types.TypeRef) else t
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(typ,
        'bodo.alloc_type()')
    if is_str_arr_type(typ):
        return (lambda n, t, s=None: bodo.libs.str_arr_ext.
            pre_alloc_string_array(n, s[0]))
    if typ == bodo.binary_array_type:
        return (lambda n, t, s=None: bodo.libs.binary_arr_ext.
            pre_alloc_binary_array(n, s[0]))
    if isinstance(typ, bodo.libs.array_item_arr_ext.ArrayItemArrayType):
        dtype = typ.dtype
        return (lambda n, t, s=None: bodo.libs.array_item_arr_ext.
            pre_alloc_array_item_array(n, s, dtype))
    if isinstance(typ, bodo.libs.struct_arr_ext.StructArrayType):
        dtypes = typ.data
        names = typ.names
        return (lambda n, t, s=None: bodo.libs.struct_arr_ext.
            pre_alloc_struct_array(n, s, dtypes, names))
    if isinstance(typ, bodo.libs.map_arr_ext.MapArrayType):
        struct_typ = bodo.libs.struct_arr_ext.StructArrayType((typ.
            key_arr_type, typ.value_arr_type), ('key', 'value'))
        return lambda n, t, s=None: bodo.libs.map_arr_ext.pre_alloc_map_array(n
            , s, struct_typ)
    if isinstance(typ, bodo.libs.tuple_arr_ext.TupleArrayType):
        dtypes = typ.data
        return (lambda n, t, s=None: bodo.libs.tuple_arr_ext.
            pre_alloc_tuple_array(n, s, dtypes))
    if isinstance(typ, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        if isinstance(t, types.TypeRef):
            if typ.dtype.categories is None:
                raise BodoError(
                    'UDFs or Groupbys that return Categorical values must have categories known at compile time.'
                    )
            is_ordered = typ.dtype.ordered
            int_type = typ.dtype.int_type
            new_cats_arr = pd.CategoricalDtype(typ.dtype.categories, is_ordered
                ).categories.values
            new_cats_tup = MetaType(tuple(new_cats_arr))
            return (lambda n, t, s=None: bodo.hiframes.pd_categorical_ext.
                alloc_categorical_array(n, bodo.hiframes.pd_categorical_ext
                .init_cat_dtype(bodo.utils.conversion.index_from_array(
                new_cats_arr), is_ordered, int_type, new_cats_tup)))
        else:
            return (lambda n, t, s=None: bodo.hiframes.pd_categorical_ext.
                alloc_categorical_array(n, t.dtype))
    if typ.dtype == bodo.hiframes.datetime_date_ext.datetime_date_type:
        return (lambda n, t, s=None: bodo.hiframes.datetime_date_ext.
            alloc_datetime_date_array(n))
    if (typ.dtype == bodo.hiframes.datetime_timedelta_ext.
        datetime_timedelta_type):
        return (lambda n, t, s=None: bodo.hiframes.datetime_timedelta_ext.
            alloc_datetime_timedelta_array(n))
    if isinstance(typ, DecimalArrayType):
        precision = typ.dtype.precision
        scale = typ.dtype.scale
        return (lambda n, t, s=None: bodo.libs.decimal_arr_ext.
            alloc_decimal_array(n, precision, scale))
    dtype = numba.np.numpy_support.as_dtype(typ.dtype)
    if isinstance(typ, IntegerArrayType):
        return lambda n, t, s=None: bodo.libs.int_arr_ext.alloc_int_array(n,
            dtype)
    if typ == boolean_array:
        return lambda n, t, s=None: bodo.libs.bool_arr_ext.alloc_bool_array(n)
    return lambda n, t, s=None: np.empty(n, dtype)


def astype(A, t):
    return A.astype(t.dtype)


@overload(astype, no_unliteral=True)
def overload_astype(A, t):
    typ = t.instance_type if isinstance(t, types.TypeRef) else t
    dtype = typ.dtype
    if A == typ:
        return lambda A, t: A
    if isinstance(A, (types.Array, IntegerArrayType)) and isinstance(typ,
        types.Array):
        return lambda A, t: A.astype(dtype)
    if isinstance(typ, IntegerArrayType):
        return lambda A, t: bodo.libs.int_arr_ext.init_integer_array(A.
            astype(dtype), np.full(len(A) + 7 >> 3, 255, np.uint8))
    if (A == bodo.libs.dict_arr_ext.dict_str_arr_type and typ == bodo.
        string_array_type):
        return lambda A, t: bodo.utils.typing.decode_if_dict_array(A)
    raise BodoError(f'cannot convert array type {A} to {typ}')


def full_type(n, val, t):
    return np.full(n, val, t.dtype)


@overload(full_type, no_unliteral=True)
def overload_full_type(n, val, t):
    typ = t.instance_type if isinstance(t, types.TypeRef) else t
    if isinstance(typ, types.Array):
        dtype = numba.np.numpy_support.as_dtype(typ.dtype)
        return lambda n, val, t: np.full(n, val, dtype)
    if isinstance(typ, IntegerArrayType):
        dtype = numba.np.numpy_support.as_dtype(typ.dtype)
        return lambda n, val, t: bodo.libs.int_arr_ext.init_integer_array(np
            .full(n, val, dtype), np.full(tuple_to_scalar(n) + 7 >> 3, 255,
            np.uint8))
    if typ == boolean_array:
        return lambda n, val, t: bodo.libs.bool_arr_ext.init_bool_array(np.
            full(n, val, np.bool_), np.full(tuple_to_scalar(n) + 7 >> 3, 
            255, np.uint8))
    if typ == string_array_type:

        def impl_str(n, val, t):
            hwlaj__cspy = n * bodo.libs.str_arr_ext.get_utf8_size(val)
            A = pre_alloc_string_array(n, hwlaj__cspy)
            for eyqr__dxgb in range(n):
                A[eyqr__dxgb] = val
            return A
        return impl_str

    def impl(n, val, t):
        A = alloc_type(n, typ, (-1,))
        for eyqr__dxgb in range(n):
            A[eyqr__dxgb] = val
        return A
    return impl


@intrinsic
def is_null_pointer(typingctx, ptr_typ=None):

    def codegen(context, builder, signature, args):
        kkuyw__eos, = args
        ocqom__ynvmo = context.get_constant_null(ptr_typ)
        return builder.icmp_unsigned('==', kkuyw__eos, ocqom__ynvmo)
    return types.bool_(ptr_typ), codegen


@intrinsic
def is_null_value(typingctx, val_typ=None):

    def codegen(context, builder, signature, args):
        val, = args
        fhsg__puotj = cgutils.alloca_once_value(builder, val)
        hwpyb__xvazv = cgutils.alloca_once_value(builder, context.
            get_constant_null(val_typ))
        return is_ll_eq(builder, fhsg__puotj, hwpyb__xvazv)
    return types.bool_(val_typ), codegen


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def tuple_list_to_array(A, data, elem_type):
    elem_type = elem_type.instance_type if isinstance(elem_type, types.TypeRef
        ) else elem_type
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'tuple_list_to_array()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(elem_type,
        'tuple_list_to_array()')
    gmdu__rmb = 'def impl(A, data, elem_type):\n'
    gmdu__rmb += '  for i, d in enumerate(data):\n'
    if elem_type == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
        gmdu__rmb += '    A[i] = bodo.utils.conversion.unbox_if_timestamp(d)\n'
    else:
        gmdu__rmb += '    A[i] = d\n'
    csdo__cec = {}
    exec(gmdu__rmb, {'bodo': bodo}, csdo__cec)
    impl = csdo__cec['impl']
    return impl


def object_length(c, obj):
    svnx__pfdx = c.context.get_argument_type(types.pyobject)
    dkxra__tvtdi = lir.FunctionType(lir.IntType(64), [svnx__pfdx])
    dwyzk__bynu = cgutils.get_or_insert_function(c.builder.module,
        dkxra__tvtdi, name='PyObject_Length')
    return c.builder.call(dwyzk__bynu, (obj,))


@intrinsic
def incref(typingctx, data=None):

    def codegen(context, builder, signature, args):
        zww__ahek, = args
        context.nrt.incref(builder, signature.args[0], zww__ahek)
    return types.void(data), codegen


def gen_getitem(out_var, in_var, ind, calltypes, nodes):
    vcpcv__pfi = out_var.loc
    kljql__gnon = ir.Expr.static_getitem(in_var, ind, None, vcpcv__pfi)
    calltypes[kljql__gnon] = None
    nodes.append(ir.Assign(kljql__gnon, out_var, vcpcv__pfi))


def is_static_getsetitem(node):
    return is_expr(node, 'static_getitem') or isinstance(node, ir.StaticSetItem
        )


def get_getsetitem_index_var(node, typemap, nodes):
    index_var = node.index_var if is_static_getsetitem(node) else node.index
    if index_var is None:
        assert is_static_getsetitem(node)
        try:
            rwt__wiab = types.literal(node.index)
        except:
            rwt__wiab = numba.typeof(node.index)
        index_var = ir.Var(node.value.scope, ir_utils.mk_unique_var(
            'dummy_index'), node.loc)
        typemap[index_var.name] = rwt__wiab
        nodes.append(ir.Assign(ir.Const(node.index, node.loc), index_var,
            node.loc))
    return index_var


import copy
ir.Const.__deepcopy__ = lambda self, memo: ir.Const(self.value, copy.
    deepcopy(self.loc))


def is_call_assign(stmt):
    return isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr
        ) and stmt.value.op == 'call'


def is_call(expr):
    return isinstance(expr, ir.Expr) and expr.op == 'call'


def is_var_assign(inst):
    return isinstance(inst, ir.Assign) and isinstance(inst.value, ir.Var)


def is_assign(inst):
    return isinstance(inst, ir.Assign)


def is_expr(val, op):
    return isinstance(val, ir.Expr) and val.op == op


def sanitize_varname(varname):
    if isinstance(varname, (tuple, list)):
        varname = '_'.join(sanitize_varname(v) for v in varname)
    varname = str(varname)
    igoss__xcgl = re.sub('\\W+', '_', varname)
    if not igoss__xcgl or not igoss__xcgl[0].isalpha():
        igoss__xcgl = '_' + igoss__xcgl
    if not igoss__xcgl.isidentifier() or keyword.iskeyword(igoss__xcgl):
        igoss__xcgl = mk_unique_var('new_name').replace('.', '_')
    return igoss__xcgl


def dump_node_list(node_list):
    for n in node_list:
        print('   ', n)


def debug_prints():
    return numba.core.config.DEBUG_ARRAY_OPT == 1


@overload(reversed)
def list_reverse(A):
    if isinstance(A, types.List):

        def impl_reversed(A):
            xlk__rujhr = len(A)
            for eyqr__dxgb in range(xlk__rujhr):
                yield A[xlk__rujhr - 1 - eyqr__dxgb]
        return impl_reversed


@numba.njit
def count_nonnan(a):
    return np.count_nonzero(~np.isnan(a))


@numba.njit
def nanvar_ddof1(a):
    vkm__smkli = count_nonnan(a)
    if vkm__smkli <= 1:
        return np.nan
    return np.nanvar(a) * (vkm__smkli / (vkm__smkli - 1))


@numba.njit
def nanstd_ddof1(a):
    return np.sqrt(nanvar_ddof1(a))


def has_supported_h5py():
    try:
        import h5py
        from bodo.io import _hdf5
    except ImportError as vkg__xkql:
        wkmtz__mfmt = False
    else:
        wkmtz__mfmt = h5py.version.hdf5_version_tuple[1] in (10, 12)
    return wkmtz__mfmt


def check_h5py():
    if not has_supported_h5py():
        raise BodoError("install 'h5py' package to enable hdf5 support")


def has_pyarrow():
    try:
        import pyarrow
    except ImportError as vkg__xkql:
        gjhe__uxa = False
    else:
        gjhe__uxa = True
    return gjhe__uxa


def has_scipy():
    try:
        import scipy
    except ImportError as vkg__xkql:
        rlfqo__lgy = False
    else:
        rlfqo__lgy = True
    return rlfqo__lgy


@intrinsic
def check_and_propagate_cpp_exception(typingctx):

    def codegen(context, builder, sig, args):
        slo__lqrxq = context.get_python_api(builder)
        nof__htelp = slo__lqrxq.err_occurred()
        jaigi__tlgvm = cgutils.is_not_null(builder, nof__htelp)
        with builder.if_then(jaigi__tlgvm):
            builder.ret(numba.core.callconv.RETCODE_EXC)
    return types.void(), codegen


def inlined_check_and_propagate_cpp_exception(context, builder):
    slo__lqrxq = context.get_python_api(builder)
    nof__htelp = slo__lqrxq.err_occurred()
    jaigi__tlgvm = cgutils.is_not_null(builder, nof__htelp)
    with builder.if_then(jaigi__tlgvm):
        builder.ret(numba.core.callconv.RETCODE_EXC)


@numba.njit
def check_java_installation(fname):
    with numba.objmode():
        check_java_installation_(fname)


def check_java_installation_(fname):
    if not fname.startswith('hdfs://'):
        return
    import shutil
    if not shutil.which('java'):
        qme__survh = (
            "Java not found. Make sure openjdk is installed for hdfs. openjdk can be installed by calling 'conda install openjdk=8 -c conda-forge'."
            )
        raise BodoError(qme__survh)


dt_err = """
        If you are trying to set NULL values for timedelta64 in regular Python, 

        consider using np.timedelta64('nat') instead of None
        """


@lower_constant(types.List)
def lower_constant_list(context, builder, typ, pyval):
    if len(pyval) > CONST_LIST_SLOW_WARN_THRESHOLD:
        warnings.warn(BodoWarning(
            'Using large global lists can result in long compilation times. Please pass large lists as arguments to JIT functions or use arrays.'
            ))
    emxv__lwfp = []
    for a in pyval:
        if bodo.typeof(a) != typ.dtype:
            raise BodoError(
                f'Values in list must have the same data type for type stability. Expected: {typ.dtype}, Actual: {bodo.typeof(a)}'
                )
        emxv__lwfp.append(context.get_constant_generic(builder, typ.dtype, a))
    ksj__wmowb = context.get_constant_generic(builder, types.int64, len(pyval))
    ydv__xduic = context.get_constant_generic(builder, types.bool_, False)
    cvd__pzs = context.get_constant_null(types.pyobject)
    xywc__xbj = lir.Constant.literal_struct([ksj__wmowb, ksj__wmowb,
        ydv__xduic] + emxv__lwfp)
    xywc__xbj = cgutils.global_constant(builder, '.const.payload', xywc__xbj
        ).bitcast(cgutils.voidptr_t)
    khypz__eax = context.get_constant(types.int64, -1)
    pnygw__kizut = context.get_constant_null(types.voidptr)
    aef__qtjt = lir.Constant.literal_struct([khypz__eax, pnygw__kizut,
        pnygw__kizut, xywc__xbj, khypz__eax])
    aef__qtjt = cgutils.global_constant(builder, '.const.meminfo', aef__qtjt
        ).bitcast(cgutils.voidptr_t)
    return lir.Constant.literal_struct([aef__qtjt, cvd__pzs])


@lower_constant(types.Set)
def lower_constant_set(context, builder, typ, pyval):
    for a in pyval:
        if bodo.typeof(a) != typ.dtype:
            raise BodoError(
                f'Values in set must have the same data type for type stability. Expected: {typ.dtype}, Actual: {bodo.typeof(a)}'
                )
    jdagn__svqv = types.List(typ.dtype)
    wev__xnc = context.get_constant_generic(builder, jdagn__svqv, list(pyval))
    qbf__iagce = context.compile_internal(builder, lambda l: set(l), types.
        Set(typ.dtype)(jdagn__svqv), [wev__xnc])
    return qbf__iagce


def lower_const_dict_fast_path(context, builder, typ, pyval):
    from bodo.utils.typing import can_replace
    mulmm__fqbx = pd.Series(pyval.keys()).values
    fbuzr__zzp = pd.Series(pyval.values()).values
    ljioe__iwpez = bodo.typeof(mulmm__fqbx)
    nrokq__dnmk = bodo.typeof(fbuzr__zzp)
    require(ljioe__iwpez.dtype == typ.key_type or can_replace(typ.key_type,
        ljioe__iwpez.dtype))
    require(nrokq__dnmk.dtype == typ.value_type or can_replace(typ.
        value_type, nrokq__dnmk.dtype))
    bmj__aab = context.get_constant_generic(builder, ljioe__iwpez, mulmm__fqbx)
    gfc__rnmxk = context.get_constant_generic(builder, nrokq__dnmk, fbuzr__zzp)

    def create_dict(keys, vals):
        xqdbv__nmpw = {}
        for k, v in zip(keys, vals):
            xqdbv__nmpw[k] = v
        return xqdbv__nmpw
    nzdb__fpl = context.compile_internal(builder, create_dict, typ(
        ljioe__iwpez, nrokq__dnmk), [bmj__aab, gfc__rnmxk])
    return nzdb__fpl


@lower_constant(types.DictType)
def lower_constant_dict(context, builder, typ, pyval):
    try:
        return lower_const_dict_fast_path(context, builder, typ, pyval)
    except:
        pass
    if len(pyval) > CONST_DICT_SLOW_WARN_THRESHOLD:
        warnings.warn(BodoWarning(
            'Using large global dictionaries can result in long compilation times. Please pass large dictionaries as arguments to JIT functions.'
            ))
    yonxn__iwfz = typ.key_type
    pjpk__mdi = typ.value_type

    def make_dict():
        return numba.typed.Dict.empty(yonxn__iwfz, pjpk__mdi)
    nzdb__fpl = context.compile_internal(builder, make_dict, typ(), [])

    def set_dict_val(d, k, v):
        d[k] = v
    for k, v in pyval.items():
        qjesu__pwt = context.get_constant_generic(builder, yonxn__iwfz, k)
        hegop__scekp = context.get_constant_generic(builder, pjpk__mdi, v)
        context.compile_internal(builder, set_dict_val, types.none(typ,
            yonxn__iwfz, pjpk__mdi), [nzdb__fpl, qjesu__pwt, hegop__scekp])
    return nzdb__fpl
