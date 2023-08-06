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
    sgf__cavjx = types.Tuple([utf8_str_type, types.int64])

    def codegen(context, builder, sig, args):
        cfx__mpnsi, = args
        ejo__sou = cgutils.create_struct_proxy(string_type)(context,
            builder, value=cfx__mpnsi)
        sugnb__ipu = cgutils.create_struct_proxy(utf8_str_type)(context,
            builder)
        uox__rivv = cgutils.create_struct_proxy(sgf__cavjx)(context, builder)
        is_ascii = builder.icmp_unsigned('==', ejo__sou.is_ascii, lir.
            Constant(ejo__sou.is_ascii.type, 1))
        with builder.if_else(is_ascii) as (hono__qcr, ttshk__jorlm):
            with hono__qcr:
                context.nrt.incref(builder, string_type, cfx__mpnsi)
                sugnb__ipu.data = ejo__sou.data
                sugnb__ipu.meminfo = ejo__sou.meminfo
                uox__rivv.f1 = ejo__sou.length
            with ttshk__jorlm:
                ykw__mne = lir.FunctionType(lir.IntType(64), [lir.IntType(8
                    ).as_pointer(), lir.IntType(8).as_pointer(), lir.
                    IntType(64), lir.IntType(32)])
                dms__hnj = cgutils.get_or_insert_function(builder.module,
                    ykw__mne, name='unicode_to_utf8')
                udjnk__jain = context.get_constant_null(types.voidptr)
                efuds__ewcs = builder.call(dms__hnj, [udjnk__jain, ejo__sou
                    .data, ejo__sou.length, ejo__sou.kind])
                uox__rivv.f1 = efuds__ewcs
                pwk__logv = builder.add(efuds__ewcs, lir.Constant(lir.
                    IntType(64), 1))
                sugnb__ipu.meminfo = context.nrt.meminfo_alloc_aligned(builder,
                    size=pwk__logv, align=32)
                sugnb__ipu.data = context.nrt.meminfo_data(builder,
                    sugnb__ipu.meminfo)
                builder.call(dms__hnj, [sugnb__ipu.data, ejo__sou.data,
                    ejo__sou.length, ejo__sou.kind])
                builder.store(lir.Constant(lir.IntType(8), 0), builder.gep(
                    sugnb__ipu.data, [efuds__ewcs]))
        uox__rivv.f0 = sugnb__ipu._getvalue()
        return uox__rivv._getvalue()
    return sgf__cavjx(string_type), codegen


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
        ykw__mne = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
        neebz__ien = cgutils.get_or_insert_function(builder.module,
            ykw__mne, name='memcmp')
        return builder.call(neebz__ien, args)
    return types.int32(types.voidptr, types.voidptr, types.intp), codegen


def int_to_str_len(n):
    return len(str(n))


@overload(int_to_str_len)
def overload_int_to_str_len(n):
    khcb__nddxh = n(10)

    def impl(n):
        if n == 0:
            return 1
        wdtu__niajl = 0
        if n < 0:
            n = -n
            wdtu__niajl += 1
        while n > 0:
            n = n // khcb__nddxh
            wdtu__niajl += 1
        return wdtu__niajl
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
        [jfqe__ciona] = args
        if isinstance(jfqe__ciona, StdStringType):
            return signature(types.float64, jfqe__ciona)
        if jfqe__ciona == string_type:
            return signature(types.float64, jfqe__ciona)


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
    ejo__sou = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    ykw__mne = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType(8
        ).as_pointer(), lir.IntType(64)])
    nnivu__vxgye = cgutils.get_or_insert_function(builder.module, ykw__mne,
        name='init_string_const')
    return builder.call(nnivu__vxgye, [ejo__sou.data, ejo__sou.length])


def gen_std_str_to_unicode(context, builder, std_str_val, del_str=False):
    kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

    def _std_str_to_unicode(std_str):
        length = bodo.libs.str_ext.get_std_str_len(std_str)
        lca__rdfhv = numba.cpython.unicode._empty_string(kind, length, 1)
        bodo.libs.str_arr_ext._memcpy(lca__rdfhv._data, bodo.libs.str_ext.
            get_c_str(std_str), length, 1)
        if del_str:
            bodo.libs.str_ext.del_str(std_str)
        return lca__rdfhv
    val = context.compile_internal(builder, _std_str_to_unicode,
        string_type(bodo.libs.str_ext.std_str_type), [std_str_val])
    return val


def gen_get_unicode_chars(context, builder, unicode_val):
    ejo__sou = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    return ejo__sou.data


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
        hgyqh__amhni = [('data', types.List(string_type))]
        models.StructModel.__init__(self, dmm, fe_type, hgyqh__amhni)


make_attribute_wrapper(RandomAccessStringArrayType, 'data', '_data')


@intrinsic
def alloc_random_access_string_array(typingctx, n_t=None):

    def codegen(context, builder, sig, args):
        efc__qzzi, = args
        dhktb__yhp = types.List(string_type)
        oic__jaakw = numba.cpython.listobj.ListInstance.allocate(context,
            builder, dhktb__yhp, efc__qzzi)
        oic__jaakw.size = efc__qzzi
        pjbh__amgmw = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        pjbh__amgmw.data = oic__jaakw.value
        return pjbh__amgmw._getvalue()
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
            xuq__lst = 0
            zgpp__tahyk = v
            if zgpp__tahyk < 0:
                xuq__lst = 1
                zgpp__tahyk = -zgpp__tahyk
            if zgpp__tahyk < 1:
                mfipb__ygck = 1
            else:
                mfipb__ygck = 1 + int(np.floor(np.log10(zgpp__tahyk)))
            length = xuq__lst + mfipb__ygck + 1 + 6
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
    ykw__mne = lir.FunctionType(lir.DoubleType(), [lir.IntType(8).as_pointer()]
        )
    nnivu__vxgye = cgutils.get_or_insert_function(builder.module, ykw__mne,
        name='str_to_float64')
    res = builder.call(nnivu__vxgye, (val,))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(StdStringType, types.float32)
def cast_str_to_float32(context, builder, fromty, toty, val):
    ykw__mne = lir.FunctionType(lir.FloatType(), [lir.IntType(8).as_pointer()])
    nnivu__vxgye = cgutils.get_or_insert_function(builder.module, ykw__mne,
        name='str_to_float32')
    res = builder.call(nnivu__vxgye, (val,))
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
    ejo__sou = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    ykw__mne = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType(8)
        .as_pointer(), lir.IntType(64)])
    nnivu__vxgye = cgutils.get_or_insert_function(builder.module, ykw__mne,
        name='str_to_int64')
    res = builder.call(nnivu__vxgye, (ejo__sou.data, ejo__sou.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(string_type, types.uint64)
@lower_cast(string_type, types.uint32)
@lower_cast(string_type, types.uint16)
@lower_cast(string_type, types.uint8)
def cast_unicode_str_to_uint64(context, builder, fromty, toty, val):
    ejo__sou = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    ykw__mne = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType(8)
        .as_pointer(), lir.IntType(64)])
    nnivu__vxgye = cgutils.get_or_insert_function(builder.module, ykw__mne,
        name='str_to_uint64')
    res = builder.call(nnivu__vxgye, (ejo__sou.data, ejo__sou.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@infer_getattr
class StringAttribute(AttributeTemplate):
    key = types.UnicodeType

    @bound_function('str.format', no_unliteral=True)
    def resolve_format(self, string_typ, args, kws):
        kws = dict(kws)
        pzil__coyx = ', '.join('e{}'.format(wspg__nvf) for wspg__nvf in
            range(len(args)))
        if pzil__coyx:
            pzil__coyx += ', '
        pckhv__hhrq = ', '.join("{} = ''".format(a) for a in kws.keys())
        vot__dgmf = f'def format_stub(string, {pzil__coyx} {pckhv__hhrq}):\n'
        vot__dgmf += '    pass\n'
        iwmqt__yhoj = {}
        exec(vot__dgmf, {}, iwmqt__yhoj)
        dghp__bygfc = iwmqt__yhoj['format_stub']
        grsp__rvin = numba.core.utils.pysignature(dghp__bygfc)
        gdamd__apfh = (string_typ,) + args + tuple(kws.values())
        return signature(string_typ, gdamd__apfh).replace(pysig=grsp__rvin)


@numba.njit(cache=True)
def str_split(arr, pat, n):
    ltpwv__wiqoo = pat is not None and len(pat) > 1
    if ltpwv__wiqoo:
        hhh__foxsa = re.compile(pat)
        if n == -1:
            n = 0
    elif n == 0:
        n = -1
    oic__jaakw = len(arr)
    pmgeu__kovo = 0
    jdrhm__rqlx = 0
    for wspg__nvf in numba.parfors.parfor.internal_prange(oic__jaakw):
        if bodo.libs.array_kernels.isna(arr, wspg__nvf):
            continue
        if ltpwv__wiqoo:
            kyrg__cae = hhh__foxsa.split(arr[wspg__nvf], maxsplit=n)
        elif pat == '':
            kyrg__cae = [''] + list(arr[wspg__nvf]) + ['']
        else:
            kyrg__cae = arr[wspg__nvf].split(pat, n)
        pmgeu__kovo += len(kyrg__cae)
        for s in kyrg__cae:
            jdrhm__rqlx += bodo.libs.str_arr_ext.get_utf8_size(s)
    jbhh__kafn = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        oic__jaakw, (pmgeu__kovo, jdrhm__rqlx), bodo.libs.str_arr_ext.
        string_array_type)
    jsno__alz = bodo.libs.array_item_arr_ext.get_offsets(jbhh__kafn)
    eyma__ijw = bodo.libs.array_item_arr_ext.get_null_bitmap(jbhh__kafn)
    uta__ljxe = bodo.libs.array_item_arr_ext.get_data(jbhh__kafn)
    mdjh__szq = 0
    for fnw__scas in numba.parfors.parfor.internal_prange(oic__jaakw):
        jsno__alz[fnw__scas] = mdjh__szq
        if bodo.libs.array_kernels.isna(arr, fnw__scas):
            bodo.libs.int_arr_ext.set_bit_to_arr(eyma__ijw, fnw__scas, 0)
            continue
        bodo.libs.int_arr_ext.set_bit_to_arr(eyma__ijw, fnw__scas, 1)
        if ltpwv__wiqoo:
            kyrg__cae = hhh__foxsa.split(arr[fnw__scas], maxsplit=n)
        elif pat == '':
            kyrg__cae = [''] + list(arr[fnw__scas]) + ['']
        else:
            kyrg__cae = arr[fnw__scas].split(pat, n)
        nwyg__jbb = len(kyrg__cae)
        for hyki__udlis in range(nwyg__jbb):
            s = kyrg__cae[hyki__udlis]
            uta__ljxe[mdjh__szq] = s
            mdjh__szq += 1
    jsno__alz[oic__jaakw] = mdjh__szq
    return jbhh__kafn


@overload(hex)
def overload_hex(x):
    if isinstance(x, types.Integer):
        kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(x):
            x = np.int64(x)
            if x < 0:
                jsb__cawqc = '-0x'
                x = x * -1
            else:
                jsb__cawqc = '0x'
            x = np.uint64(x)
            if x == 0:
                dsz__zuy = 1
            else:
                dsz__zuy = fast_ceil_log2(x + 1)
                dsz__zuy = (dsz__zuy + 3) // 4
            length = len(jsb__cawqc) + dsz__zuy
            output = numba.cpython.unicode._empty_string(kind, length, 1)
            bodo.libs.str_arr_ext._memcpy(output._data, jsb__cawqc._data,
                len(jsb__cawqc), 1)
            int_to_hex(output, dsz__zuy, len(jsb__cawqc), x)
            return output
        return impl


@register_jitable
def fast_ceil_log2(x):
    zse__kvdh = 0 if x & x - 1 == 0 else 1
    ctl__keau = [np.uint64(18446744069414584320), np.uint64(4294901760), np
        .uint64(65280), np.uint64(240), np.uint64(12), np.uint64(2)]
    epia__urr = 32
    for wspg__nvf in range(len(ctl__keau)):
        bjz__lwgu = 0 if x & ctl__keau[wspg__nvf] == 0 else epia__urr
        zse__kvdh = zse__kvdh + bjz__lwgu
        x = x >> bjz__lwgu
        epia__urr = epia__urr >> 1
    return zse__kvdh


@intrinsic
def int_to_hex(typingctx, output, out_len, header_len, int_val):

    def codegen(context, builder, sig, args):
        output, out_len, header_len, int_val = args
        slzd__zcci = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=output)
        ykw__mne = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(64)])
        jom__svsb = cgutils.get_or_insert_function(builder.module, ykw__mne,
            name='int_to_hex')
        xqo__hjup = builder.inttoptr(builder.add(builder.ptrtoint(
            slzd__zcci.data, lir.IntType(64)), header_len), lir.IntType(8).
            as_pointer())
        builder.call(jom__svsb, (xqo__hjup, out_len, int_val))
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
