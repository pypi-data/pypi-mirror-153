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
    jgri__vyb = types.Tuple([utf8_str_type, types.int64])

    def codegen(context, builder, sig, args):
        hrgd__vqy, = args
        pxc__gmhhe = cgutils.create_struct_proxy(string_type)(context,
            builder, value=hrgd__vqy)
        snqa__vefrh = cgutils.create_struct_proxy(utf8_str_type)(context,
            builder)
        arstq__trkbj = cgutils.create_struct_proxy(jgri__vyb)(context, builder)
        is_ascii = builder.icmp_unsigned('==', pxc__gmhhe.is_ascii, lir.
            Constant(pxc__gmhhe.is_ascii.type, 1))
        with builder.if_else(is_ascii) as (bwa__mhga, yzixc__anhak):
            with bwa__mhga:
                context.nrt.incref(builder, string_type, hrgd__vqy)
                snqa__vefrh.data = pxc__gmhhe.data
                snqa__vefrh.meminfo = pxc__gmhhe.meminfo
                arstq__trkbj.f1 = pxc__gmhhe.length
            with yzixc__anhak:
                qbagp__lzlqm = lir.FunctionType(lir.IntType(64), [lir.
                    IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                    lir.IntType(64), lir.IntType(32)])
                fbv__ndz = cgutils.get_or_insert_function(builder.module,
                    qbagp__lzlqm, name='unicode_to_utf8')
                rztra__hvh = context.get_constant_null(types.voidptr)
                vmhu__hju = builder.call(fbv__ndz, [rztra__hvh, pxc__gmhhe.
                    data, pxc__gmhhe.length, pxc__gmhhe.kind])
                arstq__trkbj.f1 = vmhu__hju
                efp__zem = builder.add(vmhu__hju, lir.Constant(lir.IntType(
                    64), 1))
                snqa__vefrh.meminfo = context.nrt.meminfo_alloc_aligned(builder
                    , size=efp__zem, align=32)
                snqa__vefrh.data = context.nrt.meminfo_data(builder,
                    snqa__vefrh.meminfo)
                builder.call(fbv__ndz, [snqa__vefrh.data, pxc__gmhhe.data,
                    pxc__gmhhe.length, pxc__gmhhe.kind])
                builder.store(lir.Constant(lir.IntType(8), 0), builder.gep(
                    snqa__vefrh.data, [vmhu__hju]))
        arstq__trkbj.f0 = snqa__vefrh._getvalue()
        return arstq__trkbj._getvalue()
    return jgri__vyb(string_type), codegen


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
        qbagp__lzlqm = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
        fqwd__ftz = cgutils.get_or_insert_function(builder.module,
            qbagp__lzlqm, name='memcmp')
        return builder.call(fqwd__ftz, args)
    return types.int32(types.voidptr, types.voidptr, types.intp), codegen


def int_to_str_len(n):
    return len(str(n))


@overload(int_to_str_len)
def overload_int_to_str_len(n):
    ombo__ompc = n(10)

    def impl(n):
        if n == 0:
            return 1
        wvn__fxl = 0
        if n < 0:
            n = -n
            wvn__fxl += 1
        while n > 0:
            n = n // ombo__ompc
            wvn__fxl += 1
        return wvn__fxl
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
        [ckgo__jumct] = args
        if isinstance(ckgo__jumct, StdStringType):
            return signature(types.float64, ckgo__jumct)
        if ckgo__jumct == string_type:
            return signature(types.float64, ckgo__jumct)


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
    pxc__gmhhe = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    qbagp__lzlqm = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
        IntType(8).as_pointer(), lir.IntType(64)])
    jik__wns = cgutils.get_or_insert_function(builder.module, qbagp__lzlqm,
        name='init_string_const')
    return builder.call(jik__wns, [pxc__gmhhe.data, pxc__gmhhe.length])


def gen_std_str_to_unicode(context, builder, std_str_val, del_str=False):
    kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

    def _std_str_to_unicode(std_str):
        length = bodo.libs.str_ext.get_std_str_len(std_str)
        ako__jcrq = numba.cpython.unicode._empty_string(kind, length, 1)
        bodo.libs.str_arr_ext._memcpy(ako__jcrq._data, bodo.libs.str_ext.
            get_c_str(std_str), length, 1)
        if del_str:
            bodo.libs.str_ext.del_str(std_str)
        return ako__jcrq
    val = context.compile_internal(builder, _std_str_to_unicode,
        string_type(bodo.libs.str_ext.std_str_type), [std_str_val])
    return val


def gen_get_unicode_chars(context, builder, unicode_val):
    pxc__gmhhe = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    return pxc__gmhhe.data


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
        mum__hfsc = [('data', types.List(string_type))]
        models.StructModel.__init__(self, dmm, fe_type, mum__hfsc)


make_attribute_wrapper(RandomAccessStringArrayType, 'data', '_data')


@intrinsic
def alloc_random_access_string_array(typingctx, n_t=None):

    def codegen(context, builder, sig, args):
        wpmps__midml, = args
        ebej__ixq = types.List(string_type)
        pox__olts = numba.cpython.listobj.ListInstance.allocate(context,
            builder, ebej__ixq, wpmps__midml)
        pox__olts.size = wpmps__midml
        fttr__nysuc = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        fttr__nysuc.data = pox__olts.value
        return fttr__nysuc._getvalue()
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
            vbf__tmip = 0
            jte__sjw = v
            if jte__sjw < 0:
                vbf__tmip = 1
                jte__sjw = -jte__sjw
            if jte__sjw < 1:
                wsqj__ryi = 1
            else:
                wsqj__ryi = 1 + int(np.floor(np.log10(jte__sjw)))
            length = vbf__tmip + wsqj__ryi + 1 + 6
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
    qbagp__lzlqm = lir.FunctionType(lir.DoubleType(), [lir.IntType(8).
        as_pointer()])
    jik__wns = cgutils.get_or_insert_function(builder.module, qbagp__lzlqm,
        name='str_to_float64')
    res = builder.call(jik__wns, (val,))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(StdStringType, types.float32)
def cast_str_to_float32(context, builder, fromty, toty, val):
    qbagp__lzlqm = lir.FunctionType(lir.FloatType(), [lir.IntType(8).
        as_pointer()])
    jik__wns = cgutils.get_or_insert_function(builder.module, qbagp__lzlqm,
        name='str_to_float32')
    res = builder.call(jik__wns, (val,))
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
    pxc__gmhhe = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    qbagp__lzlqm = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.
        IntType(8).as_pointer(), lir.IntType(64)])
    jik__wns = cgutils.get_or_insert_function(builder.module, qbagp__lzlqm,
        name='str_to_int64')
    res = builder.call(jik__wns, (pxc__gmhhe.data, pxc__gmhhe.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(string_type, types.uint64)
@lower_cast(string_type, types.uint32)
@lower_cast(string_type, types.uint16)
@lower_cast(string_type, types.uint8)
def cast_unicode_str_to_uint64(context, builder, fromty, toty, val):
    pxc__gmhhe = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    qbagp__lzlqm = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.
        IntType(8).as_pointer(), lir.IntType(64)])
    jik__wns = cgutils.get_or_insert_function(builder.module, qbagp__lzlqm,
        name='str_to_uint64')
    res = builder.call(jik__wns, (pxc__gmhhe.data, pxc__gmhhe.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@infer_getattr
class StringAttribute(AttributeTemplate):
    key = types.UnicodeType

    @bound_function('str.format', no_unliteral=True)
    def resolve_format(self, string_typ, args, kws):
        kws = dict(kws)
        behyr__ppbuw = ', '.join('e{}'.format(bsfg__vewj) for bsfg__vewj in
            range(len(args)))
        if behyr__ppbuw:
            behyr__ppbuw += ', '
        mac__tio = ', '.join("{} = ''".format(a) for a in kws.keys())
        lktcn__dlko = f'def format_stub(string, {behyr__ppbuw} {mac__tio}):\n'
        lktcn__dlko += '    pass\n'
        cky__gwvf = {}
        exec(lktcn__dlko, {}, cky__gwvf)
        pacqn__lty = cky__gwvf['format_stub']
        vxvcq__liake = numba.core.utils.pysignature(pacqn__lty)
        qptu__edia = (string_typ,) + args + tuple(kws.values())
        return signature(string_typ, qptu__edia).replace(pysig=vxvcq__liake)


@numba.njit(cache=True)
def str_split(arr, pat, n):
    yyly__ajc = pat is not None and len(pat) > 1
    if yyly__ajc:
        qyxaj__and = re.compile(pat)
        if n == -1:
            n = 0
    elif n == 0:
        n = -1
    pox__olts = len(arr)
    yok__vjt = 0
    iupve__leg = 0
    for bsfg__vewj in numba.parfors.parfor.internal_prange(pox__olts):
        if bodo.libs.array_kernels.isna(arr, bsfg__vewj):
            continue
        if yyly__ajc:
            zfu__eyr = qyxaj__and.split(arr[bsfg__vewj], maxsplit=n)
        elif pat == '':
            zfu__eyr = [''] + list(arr[bsfg__vewj]) + ['']
        else:
            zfu__eyr = arr[bsfg__vewj].split(pat, n)
        yok__vjt += len(zfu__eyr)
        for s in zfu__eyr:
            iupve__leg += bodo.libs.str_arr_ext.get_utf8_size(s)
    tbok__nvz = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        pox__olts, (yok__vjt, iupve__leg), bodo.libs.str_arr_ext.
        string_array_type)
    rqm__uugg = bodo.libs.array_item_arr_ext.get_offsets(tbok__nvz)
    fmpoh__gkar = bodo.libs.array_item_arr_ext.get_null_bitmap(tbok__nvz)
    rqw__xqax = bodo.libs.array_item_arr_ext.get_data(tbok__nvz)
    fvdky__vvpci = 0
    for etac__bhk in numba.parfors.parfor.internal_prange(pox__olts):
        rqm__uugg[etac__bhk] = fvdky__vvpci
        if bodo.libs.array_kernels.isna(arr, etac__bhk):
            bodo.libs.int_arr_ext.set_bit_to_arr(fmpoh__gkar, etac__bhk, 0)
            continue
        bodo.libs.int_arr_ext.set_bit_to_arr(fmpoh__gkar, etac__bhk, 1)
        if yyly__ajc:
            zfu__eyr = qyxaj__and.split(arr[etac__bhk], maxsplit=n)
        elif pat == '':
            zfu__eyr = [''] + list(arr[etac__bhk]) + ['']
        else:
            zfu__eyr = arr[etac__bhk].split(pat, n)
        rpdwd__juhx = len(zfu__eyr)
        for cyzs__zgybg in range(rpdwd__juhx):
            s = zfu__eyr[cyzs__zgybg]
            rqw__xqax[fvdky__vvpci] = s
            fvdky__vvpci += 1
    rqm__uugg[pox__olts] = fvdky__vvpci
    return tbok__nvz


@overload(hex)
def overload_hex(x):
    if isinstance(x, types.Integer):
        kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(x):
            x = np.int64(x)
            if x < 0:
                sep__ysx = '-0x'
                x = x * -1
            else:
                sep__ysx = '0x'
            x = np.uint64(x)
            if x == 0:
                uagkc__eoani = 1
            else:
                uagkc__eoani = fast_ceil_log2(x + 1)
                uagkc__eoani = (uagkc__eoani + 3) // 4
            length = len(sep__ysx) + uagkc__eoani
            output = numba.cpython.unicode._empty_string(kind, length, 1)
            bodo.libs.str_arr_ext._memcpy(output._data, sep__ysx._data, len
                (sep__ysx), 1)
            int_to_hex(output, uagkc__eoani, len(sep__ysx), x)
            return output
        return impl


@register_jitable
def fast_ceil_log2(x):
    ttbhg__lfl = 0 if x & x - 1 == 0 else 1
    nyqzm__pkkq = [np.uint64(18446744069414584320), np.uint64(4294901760),
        np.uint64(65280), np.uint64(240), np.uint64(12), np.uint64(2)]
    dwfas__bqjru = 32
    for bsfg__vewj in range(len(nyqzm__pkkq)):
        ehq__wdtpc = 0 if x & nyqzm__pkkq[bsfg__vewj] == 0 else dwfas__bqjru
        ttbhg__lfl = ttbhg__lfl + ehq__wdtpc
        x = x >> ehq__wdtpc
        dwfas__bqjru = dwfas__bqjru >> 1
    return ttbhg__lfl


@intrinsic
def int_to_hex(typingctx, output, out_len, header_len, int_val):

    def codegen(context, builder, sig, args):
        output, out_len, header_len, int_val = args
        xqda__bkt = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=output)
        qbagp__lzlqm = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(64)])
        tua__vvfzi = cgutils.get_or_insert_function(builder.module,
            qbagp__lzlqm, name='int_to_hex')
        gies__ztas = builder.inttoptr(builder.add(builder.ptrtoint(
            xqda__bkt.data, lir.IntType(64)), header_len), lir.IntType(8).
            as_pointer())
        builder.call(tua__vvfzi, (gies__ztas, out_len, int_val))
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
