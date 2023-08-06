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
def unicode_to_utf8_and_len(typingctx, str_typ):
    assert str_typ in (string_type, types.Optional(string_type)) or isinstance(
        str_typ, types.StringLiteral)
    ygofp__yihf = types.Tuple([utf8_str_type, types.int64])

    def codegen(context, builder, sig, args):
        povyl__qoei, = args
        xxd__omv = cgutils.create_struct_proxy(string_type)(context,
            builder, value=povyl__qoei)
        xjqvc__hkb = cgutils.create_struct_proxy(utf8_str_type)(context,
            builder)
        lzzjd__pbk = cgutils.create_struct_proxy(ygofp__yihf)(context, builder)
        is_ascii = builder.icmp_unsigned('==', xxd__omv.is_ascii, lir.
            Constant(xxd__omv.is_ascii.type, 1))
        with builder.if_else(is_ascii) as (esbu__siwsp, lqpi__qnx):
            with esbu__siwsp:
                context.nrt.incref(builder, string_type, povyl__qoei)
                xjqvc__hkb.data = xxd__omv.data
                xjqvc__hkb.meminfo = xxd__omv.meminfo
                lzzjd__pbk.f1 = xxd__omv.length
            with lqpi__qnx:
                ypd__jwk = lir.FunctionType(lir.IntType(64), [lir.IntType(8
                    ).as_pointer(), lir.IntType(8).as_pointer(), lir.
                    IntType(64), lir.IntType(32)])
                ezl__nqph = cgutils.get_or_insert_function(builder.module,
                    ypd__jwk, name='unicode_to_utf8')
                oeac__eykti = context.get_constant_null(types.voidptr)
                ttpfa__alfiu = builder.call(ezl__nqph, [oeac__eykti,
                    xxd__omv.data, xxd__omv.length, xxd__omv.kind])
                lzzjd__pbk.f1 = ttpfa__alfiu
                qovg__fbavr = builder.add(ttpfa__alfiu, lir.Constant(lir.
                    IntType(64), 1))
                xjqvc__hkb.meminfo = context.nrt.meminfo_alloc_aligned(builder,
                    size=qovg__fbavr, align=32)
                xjqvc__hkb.data = context.nrt.meminfo_data(builder,
                    xjqvc__hkb.meminfo)
                builder.call(ezl__nqph, [xjqvc__hkb.data, xxd__omv.data,
                    xxd__omv.length, xxd__omv.kind])
                builder.store(lir.Constant(lir.IntType(8), 0), builder.gep(
                    xjqvc__hkb.data, [ttpfa__alfiu]))
        lzzjd__pbk.f0 = xjqvc__hkb._getvalue()
        return lzzjd__pbk._getvalue()
    return ygofp__yihf(string_type), codegen


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
        ypd__jwk = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
        fem__sja = cgutils.get_or_insert_function(builder.module, ypd__jwk,
            name='memcmp')
        return builder.call(fem__sja, args)
    return types.int32(types.voidptr, types.voidptr, types.intp), codegen


def int_to_str_len(n):
    return len(str(n))


@overload(int_to_str_len)
def overload_int_to_str_len(n):
    wwgm__cwhad = n(10)

    def impl(n):
        if n == 0:
            return 1
        esoz__xedn = 0
        if n < 0:
            n = -n
            esoz__xedn += 1
        while n > 0:
            n = n // wwgm__cwhad
            esoz__xedn += 1
        return esoz__xedn
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
        [gykfn__lun] = args
        if isinstance(gykfn__lun, StdStringType):
            return signature(types.float64, gykfn__lun)
        if gykfn__lun == string_type:
            return signature(types.float64, gykfn__lun)


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
    xxd__omv = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    ypd__jwk = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType(8
        ).as_pointer(), lir.IntType(64)])
    oypcn__ich = cgutils.get_or_insert_function(builder.module, ypd__jwk,
        name='init_string_const')
    return builder.call(oypcn__ich, [xxd__omv.data, xxd__omv.length])


def gen_std_str_to_unicode(context, builder, std_str_val, del_str=False):
    kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

    def _std_str_to_unicode(std_str):
        length = bodo.libs.str_ext.get_std_str_len(std_str)
        tpjvn__nkq = numba.cpython.unicode._empty_string(kind, length, 1)
        bodo.libs.str_arr_ext._memcpy(tpjvn__nkq._data, bodo.libs.str_ext.
            get_c_str(std_str), length, 1)
        if del_str:
            bodo.libs.str_ext.del_str(std_str)
        return tpjvn__nkq
    val = context.compile_internal(builder, _std_str_to_unicode,
        string_type(bodo.libs.str_ext.std_str_type), [std_str_val])
    return val


def gen_get_unicode_chars(context, builder, unicode_val):
    xxd__omv = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    return xxd__omv.data


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
        wpucd__cber = [('data', types.List(string_type))]
        models.StructModel.__init__(self, dmm, fe_type, wpucd__cber)


make_attribute_wrapper(RandomAccessStringArrayType, 'data', '_data')


@intrinsic
def alloc_random_access_string_array(typingctx, n_t=None):

    def codegen(context, builder, sig, args):
        fmww__cqz, = args
        zzre__cst = types.List(string_type)
        etqox__cyplh = numba.cpython.listobj.ListInstance.allocate(context,
            builder, zzre__cst, fmww__cqz)
        etqox__cyplh.size = fmww__cqz
        pcef__gak = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        pcef__gak.data = etqox__cyplh.value
        return pcef__gak._getvalue()
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
            cgff__ezcmh = 0
            bbom__wtba = v
            if bbom__wtba < 0:
                cgff__ezcmh = 1
                bbom__wtba = -bbom__wtba
            if bbom__wtba < 1:
                per__thffg = 1
            else:
                per__thffg = 1 + int(np.floor(np.log10(bbom__wtba)))
            length = cgff__ezcmh + per__thffg + 1 + 6
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
    ypd__jwk = lir.FunctionType(lir.DoubleType(), [lir.IntType(8).as_pointer()]
        )
    oypcn__ich = cgutils.get_or_insert_function(builder.module, ypd__jwk,
        name='str_to_float64')
    res = builder.call(oypcn__ich, (val,))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(StdStringType, types.float32)
def cast_str_to_float32(context, builder, fromty, toty, val):
    ypd__jwk = lir.FunctionType(lir.FloatType(), [lir.IntType(8).as_pointer()])
    oypcn__ich = cgutils.get_or_insert_function(builder.module, ypd__jwk,
        name='str_to_float32')
    res = builder.call(oypcn__ich, (val,))
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
    xxd__omv = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    ypd__jwk = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType(8)
        .as_pointer(), lir.IntType(64)])
    oypcn__ich = cgutils.get_or_insert_function(builder.module, ypd__jwk,
        name='str_to_int64')
    res = builder.call(oypcn__ich, (xxd__omv.data, xxd__omv.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(string_type, types.uint64)
@lower_cast(string_type, types.uint32)
@lower_cast(string_type, types.uint16)
@lower_cast(string_type, types.uint8)
def cast_unicode_str_to_uint64(context, builder, fromty, toty, val):
    xxd__omv = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    ypd__jwk = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType(8)
        .as_pointer(), lir.IntType(64)])
    oypcn__ich = cgutils.get_or_insert_function(builder.module, ypd__jwk,
        name='str_to_uint64')
    res = builder.call(oypcn__ich, (xxd__omv.data, xxd__omv.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@infer_getattr
class StringAttribute(AttributeTemplate):
    key = types.UnicodeType

    @bound_function('str.format', no_unliteral=True)
    def resolve_format(self, string_typ, args, kws):
        kws = dict(kws)
        eiyg__yddc = ', '.join('e{}'.format(qly__sqb) for qly__sqb in range
            (len(args)))
        if eiyg__yddc:
            eiyg__yddc += ', '
        hseir__eaqvl = ', '.join("{} = ''".format(a) for a in kws.keys())
        pbemn__unin = (
            f'def format_stub(string, {eiyg__yddc} {hseir__eaqvl}):\n')
        pbemn__unin += '    pass\n'
        yno__lrbx = {}
        exec(pbemn__unin, {}, yno__lrbx)
        svol__ysyx = yno__lrbx['format_stub']
        yuec__sadb = numba.core.utils.pysignature(svol__ysyx)
        aruvj__yiup = (string_typ,) + args + tuple(kws.values())
        return signature(string_typ, aruvj__yiup).replace(pysig=yuec__sadb)


@numba.njit(cache=True)
def str_split(arr, pat, n):
    kwh__cxfn = pat is not None and len(pat) > 1
    if kwh__cxfn:
        ywkt__hoon = re.compile(pat)
        if n == -1:
            n = 0
    elif n == 0:
        n = -1
    etqox__cyplh = len(arr)
    rvfy__xzf = 0
    ncen__huh = 0
    for qly__sqb in numba.parfors.parfor.internal_prange(etqox__cyplh):
        if bodo.libs.array_kernels.isna(arr, qly__sqb):
            continue
        if kwh__cxfn:
            eej__ciih = ywkt__hoon.split(arr[qly__sqb], maxsplit=n)
        elif pat == '':
            eej__ciih = [''] + list(arr[qly__sqb]) + ['']
        else:
            eej__ciih = arr[qly__sqb].split(pat, n)
        rvfy__xzf += len(eej__ciih)
        for s in eej__ciih:
            ncen__huh += bodo.libs.str_arr_ext.get_utf8_size(s)
    ytfj__ubnh = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        etqox__cyplh, (rvfy__xzf, ncen__huh), bodo.libs.str_arr_ext.
        string_array_type)
    istsi__bnlr = bodo.libs.array_item_arr_ext.get_offsets(ytfj__ubnh)
    lnwt__xlif = bodo.libs.array_item_arr_ext.get_null_bitmap(ytfj__ubnh)
    faf__obtb = bodo.libs.array_item_arr_ext.get_data(ytfj__ubnh)
    lngmg__gld = 0
    for aoiz__ehasr in numba.parfors.parfor.internal_prange(etqox__cyplh):
        istsi__bnlr[aoiz__ehasr] = lngmg__gld
        if bodo.libs.array_kernels.isna(arr, aoiz__ehasr):
            bodo.libs.int_arr_ext.set_bit_to_arr(lnwt__xlif, aoiz__ehasr, 0)
            continue
        bodo.libs.int_arr_ext.set_bit_to_arr(lnwt__xlif, aoiz__ehasr, 1)
        if kwh__cxfn:
            eej__ciih = ywkt__hoon.split(arr[aoiz__ehasr], maxsplit=n)
        elif pat == '':
            eej__ciih = [''] + list(arr[aoiz__ehasr]) + ['']
        else:
            eej__ciih = arr[aoiz__ehasr].split(pat, n)
        ihvmp__otq = len(eej__ciih)
        for mzo__hngl in range(ihvmp__otq):
            s = eej__ciih[mzo__hngl]
            faf__obtb[lngmg__gld] = s
            lngmg__gld += 1
    istsi__bnlr[etqox__cyplh] = lngmg__gld
    return ytfj__ubnh


@overload(hex)
def overload_hex(x):
    if isinstance(x, types.Integer):
        kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(x):
            x = np.int64(x)
            if x < 0:
                hksrs__xiqqe = '-0x'
                x = x * -1
            else:
                hksrs__xiqqe = '0x'
            x = np.uint64(x)
            if x == 0:
                dljgl__rrp = 1
            else:
                dljgl__rrp = fast_ceil_log2(x + 1)
                dljgl__rrp = (dljgl__rrp + 3) // 4
            length = len(hksrs__xiqqe) + dljgl__rrp
            output = numba.cpython.unicode._empty_string(kind, length, 1)
            bodo.libs.str_arr_ext._memcpy(output._data, hksrs__xiqqe._data,
                len(hksrs__xiqqe), 1)
            int_to_hex(output, dljgl__rrp, len(hksrs__xiqqe), x)
            return output
        return impl


@register_jitable
def fast_ceil_log2(x):
    aus__ovt = 0 if x & x - 1 == 0 else 1
    vycfz__kwe = [np.uint64(18446744069414584320), np.uint64(4294901760),
        np.uint64(65280), np.uint64(240), np.uint64(12), np.uint64(2)]
    tner__ejncd = 32
    for qly__sqb in range(len(vycfz__kwe)):
        pcf__apl = 0 if x & vycfz__kwe[qly__sqb] == 0 else tner__ejncd
        aus__ovt = aus__ovt + pcf__apl
        x = x >> pcf__apl
        tner__ejncd = tner__ejncd >> 1
    return aus__ovt


@intrinsic
def int_to_hex(typingctx, output, out_len, header_len, int_val):

    def codegen(context, builder, sig, args):
        output, out_len, header_len, int_val = args
        dfsk__ady = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=output)
        ypd__jwk = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(64)])
        wrk__ajfqv = cgutils.get_or_insert_function(builder.module,
            ypd__jwk, name='int_to_hex')
        fppr__ujstq = builder.inttoptr(builder.add(builder.ptrtoint(
            dfsk__ady.data, lir.IntType(64)), header_len), lir.IntType(8).
            as_pointer())
        builder.call(wrk__ajfqv, (fppr__ujstq, out_len, int_val))
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
