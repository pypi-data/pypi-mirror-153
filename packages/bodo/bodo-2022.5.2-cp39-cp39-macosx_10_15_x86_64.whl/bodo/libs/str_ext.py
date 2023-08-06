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
    kmen__sqec = types.Tuple([utf8_str_type, types.int64])

    def codegen(context, builder, sig, args):
        cnx__mxrp, = args
        bkc__ezd = cgutils.create_struct_proxy(string_type)(context,
            builder, value=cnx__mxrp)
        ryfr__mohyo = cgutils.create_struct_proxy(utf8_str_type)(context,
            builder)
        ubncf__hrff = cgutils.create_struct_proxy(kmen__sqec)(context, builder)
        is_ascii = builder.icmp_unsigned('==', bkc__ezd.is_ascii, lir.
            Constant(bkc__ezd.is_ascii.type, 1))
        with builder.if_else(is_ascii) as (bau__xfy, gssu__ozsc):
            with bau__xfy:
                context.nrt.incref(builder, string_type, cnx__mxrp)
                ryfr__mohyo.data = bkc__ezd.data
                ryfr__mohyo.meminfo = bkc__ezd.meminfo
                ubncf__hrff.f1 = bkc__ezd.length
            with gssu__ozsc:
                tpc__mtfla = lir.FunctionType(lir.IntType(64), [lir.IntType
                    (8).as_pointer(), lir.IntType(8).as_pointer(), lir.
                    IntType(64), lir.IntType(32)])
                drqm__bvti = cgutils.get_or_insert_function(builder.module,
                    tpc__mtfla, name='unicode_to_utf8')
                qonlr__gsktz = context.get_constant_null(types.voidptr)
                cofbw__ojce = builder.call(drqm__bvti, [qonlr__gsktz,
                    bkc__ezd.data, bkc__ezd.length, bkc__ezd.kind])
                ubncf__hrff.f1 = cofbw__ojce
                ykhac__uhyr = builder.add(cofbw__ojce, lir.Constant(lir.
                    IntType(64), 1))
                ryfr__mohyo.meminfo = context.nrt.meminfo_alloc_aligned(builder
                    , size=ykhac__uhyr, align=32)
                ryfr__mohyo.data = context.nrt.meminfo_data(builder,
                    ryfr__mohyo.meminfo)
                builder.call(drqm__bvti, [ryfr__mohyo.data, bkc__ezd.data,
                    bkc__ezd.length, bkc__ezd.kind])
                builder.store(lir.Constant(lir.IntType(8), 0), builder.gep(
                    ryfr__mohyo.data, [cofbw__ojce]))
        ubncf__hrff.f0 = ryfr__mohyo._getvalue()
        return ubncf__hrff._getvalue()
    return kmen__sqec(string_type), codegen


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
        tpc__mtfla = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
        ippay__qgarl = cgutils.get_or_insert_function(builder.module,
            tpc__mtfla, name='memcmp')
        return builder.call(ippay__qgarl, args)
    return types.int32(types.voidptr, types.voidptr, types.intp), codegen


def int_to_str_len(n):
    return len(str(n))


@overload(int_to_str_len)
def overload_int_to_str_len(n):
    jwj__ebk = n(10)

    def impl(n):
        if n == 0:
            return 1
        taukf__upks = 0
        if n < 0:
            n = -n
            taukf__upks += 1
        while n > 0:
            n = n // jwj__ebk
            taukf__upks += 1
        return taukf__upks
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
        [anaoo__tzhs] = args
        if isinstance(anaoo__tzhs, StdStringType):
            return signature(types.float64, anaoo__tzhs)
        if anaoo__tzhs == string_type:
            return signature(types.float64, anaoo__tzhs)


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
    bkc__ezd = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    tpc__mtfla = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType
        (8).as_pointer(), lir.IntType(64)])
    jgfn__zjib = cgutils.get_or_insert_function(builder.module, tpc__mtfla,
        name='init_string_const')
    return builder.call(jgfn__zjib, [bkc__ezd.data, bkc__ezd.length])


def gen_std_str_to_unicode(context, builder, std_str_val, del_str=False):
    kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

    def _std_str_to_unicode(std_str):
        length = bodo.libs.str_ext.get_std_str_len(std_str)
        ljnl__lybn = numba.cpython.unicode._empty_string(kind, length, 1)
        bodo.libs.str_arr_ext._memcpy(ljnl__lybn._data, bodo.libs.str_ext.
            get_c_str(std_str), length, 1)
        if del_str:
            bodo.libs.str_ext.del_str(std_str)
        return ljnl__lybn
    val = context.compile_internal(builder, _std_str_to_unicode,
        string_type(bodo.libs.str_ext.std_str_type), [std_str_val])
    return val


def gen_get_unicode_chars(context, builder, unicode_val):
    bkc__ezd = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    return bkc__ezd.data


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
        kpycp__yft = [('data', types.List(string_type))]
        models.StructModel.__init__(self, dmm, fe_type, kpycp__yft)


make_attribute_wrapper(RandomAccessStringArrayType, 'data', '_data')


@intrinsic
def alloc_random_access_string_array(typingctx, n_t=None):

    def codegen(context, builder, sig, args):
        vupli__sidf, = args
        pfnv__vko = types.List(string_type)
        aqgo__vei = numba.cpython.listobj.ListInstance.allocate(context,
            builder, pfnv__vko, vupli__sidf)
        aqgo__vei.size = vupli__sidf
        ridfh__nhxmp = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        ridfh__nhxmp.data = aqgo__vei.value
        return ridfh__nhxmp._getvalue()
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
            njpy__bar = 0
            haj__yuep = v
            if haj__yuep < 0:
                njpy__bar = 1
                haj__yuep = -haj__yuep
            if haj__yuep < 1:
                zwc__gnrny = 1
            else:
                zwc__gnrny = 1 + int(np.floor(np.log10(haj__yuep)))
            length = njpy__bar + zwc__gnrny + 1 + 6
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
    tpc__mtfla = lir.FunctionType(lir.DoubleType(), [lir.IntType(8).
        as_pointer()])
    jgfn__zjib = cgutils.get_or_insert_function(builder.module, tpc__mtfla,
        name='str_to_float64')
    res = builder.call(jgfn__zjib, (val,))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(StdStringType, types.float32)
def cast_str_to_float32(context, builder, fromty, toty, val):
    tpc__mtfla = lir.FunctionType(lir.FloatType(), [lir.IntType(8).
        as_pointer()])
    jgfn__zjib = cgutils.get_or_insert_function(builder.module, tpc__mtfla,
        name='str_to_float32')
    res = builder.call(jgfn__zjib, (val,))
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
    bkc__ezd = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    tpc__mtfla = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType(
        8).as_pointer(), lir.IntType(64)])
    jgfn__zjib = cgutils.get_or_insert_function(builder.module, tpc__mtfla,
        name='str_to_int64')
    res = builder.call(jgfn__zjib, (bkc__ezd.data, bkc__ezd.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(string_type, types.uint64)
@lower_cast(string_type, types.uint32)
@lower_cast(string_type, types.uint16)
@lower_cast(string_type, types.uint8)
def cast_unicode_str_to_uint64(context, builder, fromty, toty, val):
    bkc__ezd = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    tpc__mtfla = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType(
        8).as_pointer(), lir.IntType(64)])
    jgfn__zjib = cgutils.get_or_insert_function(builder.module, tpc__mtfla,
        name='str_to_uint64')
    res = builder.call(jgfn__zjib, (bkc__ezd.data, bkc__ezd.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@infer_getattr
class StringAttribute(AttributeTemplate):
    key = types.UnicodeType

    @bound_function('str.format', no_unliteral=True)
    def resolve_format(self, string_typ, args, kws):
        kws = dict(kws)
        yohbd__ybl = ', '.join('e{}'.format(khpus__spm) for khpus__spm in
            range(len(args)))
        if yohbd__ybl:
            yohbd__ybl += ', '
        orjxv__elob = ', '.join("{} = ''".format(a) for a in kws.keys())
        maepo__fzt = f'def format_stub(string, {yohbd__ybl} {orjxv__elob}):\n'
        maepo__fzt += '    pass\n'
        pfyc__nod = {}
        exec(maepo__fzt, {}, pfyc__nod)
        ruxor__aont = pfyc__nod['format_stub']
        youpa__zupd = numba.core.utils.pysignature(ruxor__aont)
        udqsm__kalo = (string_typ,) + args + tuple(kws.values())
        return signature(string_typ, udqsm__kalo).replace(pysig=youpa__zupd)


@numba.njit(cache=True)
def str_split(arr, pat, n):
    jogcy__zwzuw = pat is not None and len(pat) > 1
    if jogcy__zwzuw:
        fiv__tzcyn = re.compile(pat)
        if n == -1:
            n = 0
    elif n == 0:
        n = -1
    aqgo__vei = len(arr)
    awwqu__glofb = 0
    xplx__hlwlz = 0
    for khpus__spm in numba.parfors.parfor.internal_prange(aqgo__vei):
        if bodo.libs.array_kernels.isna(arr, khpus__spm):
            continue
        if jogcy__zwzuw:
            sial__qrnc = fiv__tzcyn.split(arr[khpus__spm], maxsplit=n)
        elif pat == '':
            sial__qrnc = [''] + list(arr[khpus__spm]) + ['']
        else:
            sial__qrnc = arr[khpus__spm].split(pat, n)
        awwqu__glofb += len(sial__qrnc)
        for s in sial__qrnc:
            xplx__hlwlz += bodo.libs.str_arr_ext.get_utf8_size(s)
    cnwy__cjx = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        aqgo__vei, (awwqu__glofb, xplx__hlwlz), bodo.libs.str_arr_ext.
        string_array_type)
    uecnm__jsjsy = bodo.libs.array_item_arr_ext.get_offsets(cnwy__cjx)
    obrtm__yac = bodo.libs.array_item_arr_ext.get_null_bitmap(cnwy__cjx)
    mwmot__vrd = bodo.libs.array_item_arr_ext.get_data(cnwy__cjx)
    ihd__axhx = 0
    for bln__jzyde in numba.parfors.parfor.internal_prange(aqgo__vei):
        uecnm__jsjsy[bln__jzyde] = ihd__axhx
        if bodo.libs.array_kernels.isna(arr, bln__jzyde):
            bodo.libs.int_arr_ext.set_bit_to_arr(obrtm__yac, bln__jzyde, 0)
            continue
        bodo.libs.int_arr_ext.set_bit_to_arr(obrtm__yac, bln__jzyde, 1)
        if jogcy__zwzuw:
            sial__qrnc = fiv__tzcyn.split(arr[bln__jzyde], maxsplit=n)
        elif pat == '':
            sial__qrnc = [''] + list(arr[bln__jzyde]) + ['']
        else:
            sial__qrnc = arr[bln__jzyde].split(pat, n)
        xcx__mvvo = len(sial__qrnc)
        for wwg__jdthf in range(xcx__mvvo):
            s = sial__qrnc[wwg__jdthf]
            mwmot__vrd[ihd__axhx] = s
            ihd__axhx += 1
    uecnm__jsjsy[aqgo__vei] = ihd__axhx
    return cnwy__cjx


@overload(hex)
def overload_hex(x):
    if isinstance(x, types.Integer):
        kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(x):
            x = np.int64(x)
            if x < 0:
                euhj__gqeb = '-0x'
                x = x * -1
            else:
                euhj__gqeb = '0x'
            x = np.uint64(x)
            if x == 0:
                cijkw__bokg = 1
            else:
                cijkw__bokg = fast_ceil_log2(x + 1)
                cijkw__bokg = (cijkw__bokg + 3) // 4
            length = len(euhj__gqeb) + cijkw__bokg
            output = numba.cpython.unicode._empty_string(kind, length, 1)
            bodo.libs.str_arr_ext._memcpy(output._data, euhj__gqeb._data,
                len(euhj__gqeb), 1)
            int_to_hex(output, cijkw__bokg, len(euhj__gqeb), x)
            return output
        return impl


@register_jitable
def fast_ceil_log2(x):
    hgsv__xgk = 0 if x & x - 1 == 0 else 1
    vcsb__vudqh = [np.uint64(18446744069414584320), np.uint64(4294901760),
        np.uint64(65280), np.uint64(240), np.uint64(12), np.uint64(2)]
    kci__bngr = 32
    for khpus__spm in range(len(vcsb__vudqh)):
        xec__zkti = 0 if x & vcsb__vudqh[khpus__spm] == 0 else kci__bngr
        hgsv__xgk = hgsv__xgk + xec__zkti
        x = x >> xec__zkti
        kci__bngr = kci__bngr >> 1
    return hgsv__xgk


@intrinsic
def int_to_hex(typingctx, output, out_len, header_len, int_val):

    def codegen(context, builder, sig, args):
        output, out_len, header_len, int_val = args
        sfc__dfpu = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=output)
        tpc__mtfla = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(64)])
        vkp__bcqcl = cgutils.get_or_insert_function(builder.module,
            tpc__mtfla, name='int_to_hex')
        dob__ozehv = builder.inttoptr(builder.add(builder.ptrtoint(
            sfc__dfpu.data, lir.IntType(64)), header_len), lir.IntType(8).
            as_pointer())
        builder.call(vkp__bcqcl, (dob__ozehv, out_len, int_val))
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
