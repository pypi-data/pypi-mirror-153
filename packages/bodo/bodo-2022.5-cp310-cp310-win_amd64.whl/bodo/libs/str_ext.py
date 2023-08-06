import operator
import re
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.typing.templates import AbstractTemplate, AttributeTemplate, bound_function, infer_getattr, infer_global, signature
from numba.extending import intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, register_jitable, register_model
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs import hstr_ext
from bodo.utils.typing import BodoError, get_overload_const_int, get_overload_const_str, is_overload_constant_int, is_overload_constant_str


def unliteral_all(args):
    return tuple(types.unliteral(a) for a in args)


ll.add_symbol('del_str', hstr_ext.del_str)
ll.add_symbol('unicode_to_utf8', hstr_ext.unicode_to_utf8)
ll.add_symbol('memcmp', hstr_ext.memcmp)
ll.add_symbol('int_to_hex', hstr_ext.int_to_hex)
string_type = types.unicode_type


@numba.njit
def contains_regex(e, in_str):
    with numba.objmode(res='bool_'):
        res = bool(e.search(in_str))
    return res


@numba.generated_jit
def str_findall_count(regex, in_str):

    def _str_findall_count_impl(regex, in_str):
        with numba.objmode(res='int64'):
            res = len(regex.findall(in_str))
        return res
    return _str_findall_count_impl


utf8_str_type = types.ArrayCTypes(types.Array(types.uint8, 1, 'C'))


@intrinsic
def unicode_to_utf8_and_len(typingctx, str_typ=None):
    assert str_typ in (string_type, types.Optional(string_type)) or isinstance(
        str_typ, types.StringLiteral)
    tgdkg__hcux = types.Tuple([utf8_str_type, types.int64])

    def codegen(context, builder, sig, args):
        nceiv__rvb, = args
        wtnt__doyp = cgutils.create_struct_proxy(string_type)(context,
            builder, value=nceiv__rvb)
        znyoj__qklrh = cgutils.create_struct_proxy(utf8_str_type)(context,
            builder)
        gqcxu__rwpfe = cgutils.create_struct_proxy(tgdkg__hcux)(context,
            builder)
        is_ascii = builder.icmp_unsigned('==', wtnt__doyp.is_ascii, lir.
            Constant(wtnt__doyp.is_ascii.type, 1))
        with builder.if_else(is_ascii) as (phm__foa, acgo__pfczd):
            with phm__foa:
                context.nrt.incref(builder, string_type, nceiv__rvb)
                znyoj__qklrh.data = wtnt__doyp.data
                znyoj__qklrh.meminfo = wtnt__doyp.meminfo
                gqcxu__rwpfe.f1 = wtnt__doyp.length
            with acgo__pfczd:
                pkcy__uqemk = lir.FunctionType(lir.IntType(64), [lir.
                    IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                    lir.IntType(64), lir.IntType(32)])
                fyos__oigp = cgutils.get_or_insert_function(builder.module,
                    pkcy__uqemk, name='unicode_to_utf8')
                ymb__yjbx = context.get_constant_null(types.voidptr)
                xixz__sxf = builder.call(fyos__oigp, [ymb__yjbx, wtnt__doyp
                    .data, wtnt__doyp.length, wtnt__doyp.kind])
                gqcxu__rwpfe.f1 = xixz__sxf
                fhv__pyw = builder.add(xixz__sxf, lir.Constant(lir.IntType(
                    64), 1))
                znyoj__qklrh.meminfo = context.nrt.meminfo_alloc_aligned(
                    builder, size=fhv__pyw, align=32)
                znyoj__qklrh.data = context.nrt.meminfo_data(builder,
                    znyoj__qklrh.meminfo)
                builder.call(fyos__oigp, [znyoj__qklrh.data, wtnt__doyp.
                    data, wtnt__doyp.length, wtnt__doyp.kind])
                builder.store(lir.Constant(lir.IntType(8), 0), builder.gep(
                    znyoj__qklrh.data, [xixz__sxf]))
        gqcxu__rwpfe.f0 = znyoj__qklrh._getvalue()
        return gqcxu__rwpfe._getvalue()
    return tgdkg__hcux(string_type), codegen


def unicode_to_utf8(s):
    return s


@overload(unicode_to_utf8)
def overload_unicode_to_utf8(s):
    return lambda s: unicode_to_utf8_and_len(s)[0]


@overload(max)
def overload_builtin_max(lhs, rhs):
    if lhs == types.unicode_type and rhs == types.unicode_type:

        def impl(lhs, rhs):
            return lhs if lhs > rhs else rhs
        return impl


@overload(min)
def overload_builtin_min(lhs, rhs):
    if lhs == types.unicode_type and rhs == types.unicode_type:

        def impl(lhs, rhs):
            return lhs if lhs < rhs else rhs
        return impl


@intrinsic
def memcmp(typingctx, dest_t, src_t, count_t=None):

    def codegen(context, builder, sig, args):
        pkcy__uqemk = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
        kitkb__tktow = cgutils.get_or_insert_function(builder.module,
            pkcy__uqemk, name='memcmp')
        return builder.call(kitkb__tktow, args)
    return types.int32(types.voidptr, types.voidptr, types.intp), codegen


def int_to_str_len(n):
    return len(str(n))


@overload(int_to_str_len)
def overload_int_to_str_len(n):
    kqzjy__wds = n(10)

    def impl(n):
        if n == 0:
            return 1
        oeeh__qveq = 0
        if n < 0:
            n = -n
            oeeh__qveq += 1
        while n > 0:
            n = n // kqzjy__wds
            oeeh__qveq += 1
        return oeeh__qveq
    return impl


class StdStringType(types.Opaque):

    def __init__(self):
        super(StdStringType, self).__init__(name='StdStringType')


std_str_type = StdStringType()
register_model(StdStringType)(models.OpaqueModel)
del_str = types.ExternalFunction('del_str', types.void(std_str_type))
get_c_str = types.ExternalFunction('get_c_str', types.voidptr(std_str_type))
dummy_use = numba.njit(lambda a: None)


@overload(int)
def int_str_overload(in_str, base=10):
    if in_str == string_type:
        if is_overload_constant_int(base) and get_overload_const_int(base
            ) == 10:

            def _str_to_int_impl(in_str, base=10):
                val = _str_to_int64(in_str._data, in_str._length)
                dummy_use(in_str)
                return val
            return _str_to_int_impl

        def _str_to_int_base_impl(in_str, base=10):
            val = _str_to_int64_base(in_str._data, in_str._length, base)
            dummy_use(in_str)
            return val
        return _str_to_int_base_impl


@infer_global(float)
class StrToFloat(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        [ddn__ujpk] = args
        if isinstance(ddn__ujpk, StdStringType):
            return signature(types.float64, ddn__ujpk)
        if ddn__ujpk == string_type:
            return signature(types.float64, ddn__ujpk)


ll.add_symbol('init_string_const', hstr_ext.init_string_const)
ll.add_symbol('get_c_str', hstr_ext.get_c_str)
ll.add_symbol('str_to_int64', hstr_ext.str_to_int64)
ll.add_symbol('str_to_uint64', hstr_ext.str_to_uint64)
ll.add_symbol('str_to_int64_base', hstr_ext.str_to_int64_base)
ll.add_symbol('str_to_float64', hstr_ext.str_to_float64)
ll.add_symbol('str_to_float32', hstr_ext.str_to_float32)
ll.add_symbol('get_str_len', hstr_ext.get_str_len)
ll.add_symbol('str_from_float32', hstr_ext.str_from_float32)
ll.add_symbol('str_from_float64', hstr_ext.str_from_float64)
get_std_str_len = types.ExternalFunction('get_str_len', signature(types.
    intp, std_str_type))
init_string_from_chars = types.ExternalFunction('init_string_const',
    std_str_type(types.voidptr, types.intp))
_str_to_int64 = types.ExternalFunction('str_to_int64', signature(types.
    int64, types.voidptr, types.int64))
_str_to_uint64 = types.ExternalFunction('str_to_uint64', signature(types.
    uint64, types.voidptr, types.int64))
_str_to_int64_base = types.ExternalFunction('str_to_int64_base', signature(
    types.int64, types.voidptr, types.int64, types.int64))


def gen_unicode_to_std_str(context, builder, unicode_val):
    wtnt__doyp = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    pkcy__uqemk = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
        IntType(8).as_pointer(), lir.IntType(64)])
    gtpu__gsh = cgutils.get_or_insert_function(builder.module, pkcy__uqemk,
        name='init_string_const')
    return builder.call(gtpu__gsh, [wtnt__doyp.data, wtnt__doyp.length])


def gen_std_str_to_unicode(context, builder, std_str_val, del_str=False):
    kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

    def _std_str_to_unicode(std_str):
        length = bodo.libs.str_ext.get_std_str_len(std_str)
        gkuxe__kkq = numba.cpython.unicode._empty_string(kind, length, 1)
        bodo.libs.str_arr_ext._memcpy(gkuxe__kkq._data, bodo.libs.str_ext.
            get_c_str(std_str), length, 1)
        if del_str:
            bodo.libs.str_ext.del_str(std_str)
        return gkuxe__kkq
    val = context.compile_internal(builder, _std_str_to_unicode,
        string_type(bodo.libs.str_ext.std_str_type), [std_str_val])
    return val


def gen_get_unicode_chars(context, builder, unicode_val):
    wtnt__doyp = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    return wtnt__doyp.data


@intrinsic
def unicode_to_std_str(typingctx, unicode_t=None):

    def codegen(context, builder, sig, args):
        return gen_unicode_to_std_str(context, builder, args[0])
    return std_str_type(string_type), codegen


@intrinsic
def std_str_to_unicode(typingctx, unicode_t=None):

    def codegen(context, builder, sig, args):
        return gen_std_str_to_unicode(context, builder, args[0], True)
    return string_type(std_str_type), codegen


class RandomAccessStringArrayType(types.ArrayCompatible):

    def __init__(self):
        super(RandomAccessStringArrayType, self).__init__(name=
            'RandomAccessStringArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return string_type

    def copy(self):
        RandomAccessStringArrayType()


random_access_string_array = RandomAccessStringArrayType()


@register_model(RandomAccessStringArrayType)
class RandomAccessStringArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        sri__gwcx = [('data', types.List(string_type))]
        models.StructModel.__init__(self, dmm, fe_type, sri__gwcx)


make_attribute_wrapper(RandomAccessStringArrayType, 'data', '_data')


@intrinsic
def alloc_random_access_string_array(typingctx, n_t=None):

    def codegen(context, builder, sig, args):
        whro__ooy, = args
        sqnm__cenhs = types.List(string_type)
        sly__xayh = numba.cpython.listobj.ListInstance.allocate(context,
            builder, sqnm__cenhs, whro__ooy)
        sly__xayh.size = whro__ooy
        vcvvy__ogc = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        vcvvy__ogc.data = sly__xayh.value
        return vcvvy__ogc._getvalue()
    return random_access_string_array(types.intp), codegen


@overload(operator.getitem, no_unliteral=True)
def random_access_str_arr_getitem(A, ind):
    if A != random_access_string_array:
        return
    if isinstance(ind, types.Integer):
        return lambda A, ind: A._data[ind]


@overload(operator.setitem)
def random_access_str_arr_setitem(A, idx, val):
    if A != random_access_string_array:
        return
    if isinstance(idx, types.Integer):
        assert val == string_type

        def impl_scalar(A, idx, val):
            A._data[idx] = val
        return impl_scalar


@overload(len, no_unliteral=True)
def overload_str_arr_len(A):
    if A == random_access_string_array:
        return lambda A: len(A._data)


@overload_attribute(RandomAccessStringArrayType, 'shape')
def overload_str_arr_shape(A):
    return lambda A: (len(A._data),)


def alloc_random_access_str_arr_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_libs_str_ext_alloc_random_access_string_array
    ) = alloc_random_access_str_arr_equiv
str_from_float32 = types.ExternalFunction('str_from_float32', types.void(
    types.voidptr, types.float32))
str_from_float64 = types.ExternalFunction('str_from_float64', types.void(
    types.voidptr, types.float64))


def float_to_str(s, v):
    pass


@overload(float_to_str)
def float_to_str_overload(s, v):
    assert isinstance(v, types.Float)
    if v == types.float32:
        return lambda s, v: str_from_float32(s._data, v)
    return lambda s, v: str_from_float64(s._data, v)


@overload(str)
def float_str_overload(v):
    if isinstance(v, types.Float):
        kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(v):
            if v == 0:
                return '0.0'
            ywqgg__klsa = 0
            aaw__qdi = v
            if aaw__qdi < 0:
                ywqgg__klsa = 1
                aaw__qdi = -aaw__qdi
            if aaw__qdi < 1:
                cnzlo__hnhm = 1
            else:
                cnzlo__hnhm = 1 + int(np.floor(np.log10(aaw__qdi)))
            length = ywqgg__klsa + cnzlo__hnhm + 1 + 6
            s = numba.cpython.unicode._malloc_string(kind, 1, length, True)
            float_to_str(s, v)
            return s
        return impl


@overload(format, no_unliteral=True)
def overload_format(value, format_spec=''):
    if is_overload_constant_str(format_spec) and get_overload_const_str(
        format_spec) == '':

        def impl_fast(value, format_spec=''):
            return str(value)
        return impl_fast

    def impl(value, format_spec=''):
        with numba.objmode(res='string'):
            res = format(value, format_spec)
        return res
    return impl


@lower_cast(StdStringType, types.float64)
def cast_str_to_float64(context, builder, fromty, toty, val):
    pkcy__uqemk = lir.FunctionType(lir.DoubleType(), [lir.IntType(8).
        as_pointer()])
    gtpu__gsh = cgutils.get_or_insert_function(builder.module, pkcy__uqemk,
        name='str_to_float64')
    res = builder.call(gtpu__gsh, (val,))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(StdStringType, types.float32)
def cast_str_to_float32(context, builder, fromty, toty, val):
    pkcy__uqemk = lir.FunctionType(lir.FloatType(), [lir.IntType(8).
        as_pointer()])
    gtpu__gsh = cgutils.get_or_insert_function(builder.module, pkcy__uqemk,
        name='str_to_float32')
    res = builder.call(gtpu__gsh, (val,))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(string_type, types.float64)
def cast_unicode_str_to_float64(context, builder, fromty, toty, val):
    std_str = gen_unicode_to_std_str(context, builder, val)
    return cast_str_to_float64(context, builder, std_str_type, toty, std_str)


@lower_cast(string_type, types.float32)
def cast_unicode_str_to_float32(context, builder, fromty, toty, val):
    std_str = gen_unicode_to_std_str(context, builder, val)
    return cast_str_to_float32(context, builder, std_str_type, toty, std_str)


@lower_cast(string_type, types.int64)
@lower_cast(string_type, types.int32)
@lower_cast(string_type, types.int16)
@lower_cast(string_type, types.int8)
def cast_unicode_str_to_int64(context, builder, fromty, toty, val):
    wtnt__doyp = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    pkcy__uqemk = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType
        (8).as_pointer(), lir.IntType(64)])
    gtpu__gsh = cgutils.get_or_insert_function(builder.module, pkcy__uqemk,
        name='str_to_int64')
    res = builder.call(gtpu__gsh, (wtnt__doyp.data, wtnt__doyp.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(string_type, types.uint64)
@lower_cast(string_type, types.uint32)
@lower_cast(string_type, types.uint16)
@lower_cast(string_type, types.uint8)
def cast_unicode_str_to_uint64(context, builder, fromty, toty, val):
    wtnt__doyp = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    pkcy__uqemk = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType
        (8).as_pointer(), lir.IntType(64)])
    gtpu__gsh = cgutils.get_or_insert_function(builder.module, pkcy__uqemk,
        name='str_to_uint64')
    res = builder.call(gtpu__gsh, (wtnt__doyp.data, wtnt__doyp.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@infer_getattr
class StringAttribute(AttributeTemplate):
    key = types.UnicodeType

    @bound_function('str.format', no_unliteral=True)
    def resolve_format(self, string_typ, args, kws):
        kws = dict(kws)
        ukwsi__afz = ', '.join('e{}'.format(keo__ztsb) for keo__ztsb in
            range(len(args)))
        if ukwsi__afz:
            ukwsi__afz += ', '
        hyn__tly = ', '.join("{} = ''".format(a) for a in kws.keys())
        mgvwo__dkqxw = f'def format_stub(string, {ukwsi__afz} {hyn__tly}):\n'
        mgvwo__dkqxw += '    pass\n'
        ycq__stny = {}
        exec(mgvwo__dkqxw, {}, ycq__stny)
        sbgz__vnly = ycq__stny['format_stub']
        lgys__ukvh = numba.core.utils.pysignature(sbgz__vnly)
        zudkn__wpewj = (string_typ,) + args + tuple(kws.values())
        return signature(string_typ, zudkn__wpewj).replace(pysig=lgys__ukvh)


@numba.njit(cache=True)
def str_split(arr, pat, n):
    awgf__kqj = pat is not None and len(pat) > 1
    if awgf__kqj:
        usk__iwsu = re.compile(pat)
        if n == -1:
            n = 0
    elif n == 0:
        n = -1
    sly__xayh = len(arr)
    hra__chs = 0
    noxuo__gcr = 0
    for keo__ztsb in numba.parfors.parfor.internal_prange(sly__xayh):
        if bodo.libs.array_kernels.isna(arr, keo__ztsb):
            continue
        if awgf__kqj:
            artep__soi = usk__iwsu.split(arr[keo__ztsb], maxsplit=n)
        elif pat == '':
            artep__soi = [''] + list(arr[keo__ztsb]) + ['']
        else:
            artep__soi = arr[keo__ztsb].split(pat, n)
        hra__chs += len(artep__soi)
        for s in artep__soi:
            noxuo__gcr += bodo.libs.str_arr_ext.get_utf8_size(s)
    imbf__nbjx = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        sly__xayh, (hra__chs, noxuo__gcr), bodo.libs.str_arr_ext.
        string_array_type)
    hkchu__klp = bodo.libs.array_item_arr_ext.get_offsets(imbf__nbjx)
    eapxo__cea = bodo.libs.array_item_arr_ext.get_null_bitmap(imbf__nbjx)
    tpvbr__kxl = bodo.libs.array_item_arr_ext.get_data(imbf__nbjx)
    yiuho__gct = 0
    for fcqu__hujv in numba.parfors.parfor.internal_prange(sly__xayh):
        hkchu__klp[fcqu__hujv] = yiuho__gct
        if bodo.libs.array_kernels.isna(arr, fcqu__hujv):
            bodo.libs.int_arr_ext.set_bit_to_arr(eapxo__cea, fcqu__hujv, 0)
            continue
        bodo.libs.int_arr_ext.set_bit_to_arr(eapxo__cea, fcqu__hujv, 1)
        if awgf__kqj:
            artep__soi = usk__iwsu.split(arr[fcqu__hujv], maxsplit=n)
        elif pat == '':
            artep__soi = [''] + list(arr[fcqu__hujv]) + ['']
        else:
            artep__soi = arr[fcqu__hujv].split(pat, n)
        bzaes__aaex = len(artep__soi)
        for fyvv__hjutb in range(bzaes__aaex):
            s = artep__soi[fyvv__hjutb]
            tpvbr__kxl[yiuho__gct] = s
            yiuho__gct += 1
    hkchu__klp[sly__xayh] = yiuho__gct
    return imbf__nbjx


@overload(hex)
def overload_hex(x):
    if isinstance(x, types.Integer):
        kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(x):
            x = np.int64(x)
            if x < 0:
                yvcth__vitc = '-0x'
                x = x * -1
            else:
                yvcth__vitc = '0x'
            x = np.uint64(x)
            if x == 0:
                gmy__gsth = 1
            else:
                gmy__gsth = fast_ceil_log2(x + 1)
                gmy__gsth = (gmy__gsth + 3) // 4
            length = len(yvcth__vitc) + gmy__gsth
            output = numba.cpython.unicode._empty_string(kind, length, 1)
            bodo.libs.str_arr_ext._memcpy(output._data, yvcth__vitc._data,
                len(yvcth__vitc), 1)
            int_to_hex(output, gmy__gsth, len(yvcth__vitc), x)
            return output
        return impl


@register_jitable
def fast_ceil_log2(x):
    lcvk__fnh = 0 if x & x - 1 == 0 else 1
    kdco__gssfm = [np.uint64(18446744069414584320), np.uint64(4294901760),
        np.uint64(65280), np.uint64(240), np.uint64(12), np.uint64(2)]
    eqje__gwkdc = 32
    for keo__ztsb in range(len(kdco__gssfm)):
        ihjpu__pqoj = 0 if x & kdco__gssfm[keo__ztsb] == 0 else eqje__gwkdc
        lcvk__fnh = lcvk__fnh + ihjpu__pqoj
        x = x >> ihjpu__pqoj
        eqje__gwkdc = eqje__gwkdc >> 1
    return lcvk__fnh


@intrinsic
def int_to_hex(typingctx, output, out_len, header_len, int_val):

    def codegen(context, builder, sig, args):
        output, out_len, header_len, int_val = args
        png__ykgqq = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=output)
        pkcy__uqemk = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(64)])
        jfuh__kgu = cgutils.get_or_insert_function(builder.module,
            pkcy__uqemk, name='int_to_hex')
        coif__bxhdt = builder.inttoptr(builder.add(builder.ptrtoint(
            png__ykgqq.data, lir.IntType(64)), header_len), lir.IntType(8).
            as_pointer())
        builder.call(jfuh__kgu, (coif__bxhdt, out_len, int_val))
    return types.void(output, out_len, header_len, int_val), codegen


def alloc_empty_bytes_or_string_data(typ, kind, length, is_ascii=0):
    pass


@overload(alloc_empty_bytes_or_string_data)
def overload_alloc_empty_bytes_or_string_data(typ, kind, length, is_ascii=0):
    typ = typ.instance_type if isinstance(typ, types.TypeRef) else typ
    if typ == bodo.bytes_type:
        return lambda typ, kind, length, is_ascii=0: np.empty(length, np.uint8)
    if typ == string_type:
        return (lambda typ, kind, length, is_ascii=0: numba.cpython.unicode
            ._empty_string(kind, length, is_ascii))
    raise BodoError(
        f'Internal Error: Expected Bytes or String type, found {typ}')


def get_unicode_or_numpy_data(val):
    pass


@overload(get_unicode_or_numpy_data)
def overload_get_unicode_or_numpy_data(val):
    if val == string_type:
        return lambda val: val._data
    if isinstance(val, types.Array):
        return lambda val: val.ctypes
    raise BodoError(
        f'Internal Error: Expected String or Numpy Array, found {val}')
