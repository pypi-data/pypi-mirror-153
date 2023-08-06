"""Dictionary encoded array data type, similar to DictionaryArray of Arrow.
The purpose is to improve memory consumption and performance over string_array_type for
string arrays that have a lot of repetitive values (typical in practice).
Can be extended to be used with types other than strings as well.
See:
https://bodo.atlassian.net/browse/BE-2295
https://bodo.atlassian.net/wiki/spaces/B/pages/993722369/Dictionary-encoded+String+Array+Support+in+Parquet+read+compute+...
https://arrow.apache.org/docs/cpp/api/array.html#dictionary-encoded
"""
import operator
import re
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
import pyarrow as pa
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_new_ref, lower_builtin, lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
import bodo
from bodo.libs import hstr_ext
from bodo.libs.bool_arr_ext import init_bool_array
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType, get_str_arr_item_length, overload_str_arr_astype, pre_alloc_string_array
from bodo.utils.typing import BodoArrayIterator, is_overload_none, raise_bodo_error
ll.add_symbol('box_dict_str_array', hstr_ext.box_dict_str_array)
dict_indices_arr_type = IntegerArrayType(types.int32)


class DictionaryArrayType(types.IterableType, types.ArrayCompatible):

    def __init__(self, arr_data_type):
        self.data = arr_data_type
        super(DictionaryArrayType, self).__init__(name=
            f'DictionaryArrayType({arr_data_type})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def iterator_type(self):
        return BodoArrayIterator(self)

    @property
    def dtype(self):
        return self.data.dtype

    def copy(self):
        return DictionaryArrayType(self.data)

    @property
    def indices_type(self):
        return dict_indices_arr_type

    @property
    def indices_dtype(self):
        return dict_indices_arr_type.dtype

    def unify(self, typingctx, other):
        if other == bodo.string_array_type:
            return bodo.string_array_type


dict_str_arr_type = DictionaryArrayType(bodo.string_array_type)


@register_model(DictionaryArrayType)
class DictionaryArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        knd__wyal = [('data', fe_type.data), ('indices',
            dict_indices_arr_type), ('has_global_dictionary', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, knd__wyal)


make_attribute_wrapper(DictionaryArrayType, 'data', '_data')
make_attribute_wrapper(DictionaryArrayType, 'indices', '_indices')
make_attribute_wrapper(DictionaryArrayType, 'has_global_dictionary',
    '_has_global_dictionary')
lower_builtin('getiter', dict_str_arr_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_dict_arr(typingctx, data_t, indices_t, glob_dict_t=None):
    assert indices_t == dict_indices_arr_type, 'invalid indices type for dict array'

    def codegen(context, builder, signature, args):
        jaxtk__frzi, fsipm__mrah, bitab__yzfm = args
        husn__kju = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        husn__kju.data = jaxtk__frzi
        husn__kju.indices = fsipm__mrah
        husn__kju.has_global_dictionary = bitab__yzfm
        context.nrt.incref(builder, signature.args[0], jaxtk__frzi)
        context.nrt.incref(builder, signature.args[1], fsipm__mrah)
        return husn__kju._getvalue()
    rgc__bdsc = DictionaryArrayType(data_t)
    poh__gqgfe = rgc__bdsc(data_t, indices_t, types.bool_)
    return poh__gqgfe, codegen


@typeof_impl.register(pa.DictionaryArray)
def typeof_dict_value(val, c):
    if val.type.value_type == pa.string():
        return dict_str_arr_type


def to_pa_dict_arr(A):
    if isinstance(A, pa.DictionaryArray):
        return A
    for ttf__lvc in range(len(A)):
        if pd.isna(A[ttf__lvc]):
            A[ttf__lvc] = None
    return pa.array(A).dictionary_encode()


@unbox(DictionaryArrayType)
def unbox_dict_arr(typ, val, c):
    if bodo.hiframes.boxing._use_dict_str_type:
        aoekg__huvx = c.pyapi.unserialize(c.pyapi.serialize_object(
            to_pa_dict_arr))
        val = c.pyapi.call_function_objargs(aoekg__huvx, [val])
        c.pyapi.decref(aoekg__huvx)
    husn__kju = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ijjnz__dav = c.pyapi.object_getattr_string(val, 'dictionary')
    hck__tejdd = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_,
        False))
    vww__dpj = c.pyapi.call_method(ijjnz__dav, 'to_numpy', (hck__tejdd,))
    husn__kju.data = c.unbox(typ.data, vww__dpj).value
    hvgm__nzx = c.pyapi.object_getattr_string(val, 'indices')
    lpn__bearr = c.context.insert_const_string(c.builder.module, 'pandas')
    afsax__lytd = c.pyapi.import_module_noblock(lpn__bearr)
    pza__frc = c.pyapi.string_from_constant_string('Int32')
    rhs__khrfs = c.pyapi.call_method(afsax__lytd, 'array', (hvgm__nzx,
        pza__frc))
    husn__kju.indices = c.unbox(dict_indices_arr_type, rhs__khrfs).value
    husn__kju.has_global_dictionary = c.context.get_constant(types.bool_, False
        )
    c.pyapi.decref(ijjnz__dav)
    c.pyapi.decref(hck__tejdd)
    c.pyapi.decref(vww__dpj)
    c.pyapi.decref(hvgm__nzx)
    c.pyapi.decref(afsax__lytd)
    c.pyapi.decref(pza__frc)
    c.pyapi.decref(rhs__khrfs)
    if bodo.hiframes.boxing._use_dict_str_type:
        c.pyapi.decref(val)
    iuyq__uik = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(husn__kju._getvalue(), is_error=iuyq__uik)


@box(DictionaryArrayType)
def box_dict_arr(typ, val, c):
    husn__kju = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ == dict_str_arr_type:
        c.context.nrt.incref(c.builder, typ.data, husn__kju.data)
        ngq__llv = c.box(typ.data, husn__kju.data)
        uio__jxmlj = cgutils.create_struct_proxy(dict_indices_arr_type)(c.
            context, c.builder, husn__kju.indices)
        ljrn__vyxfz = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), c.
            pyapi.pyobj, lir.IntType(32).as_pointer(), lir.IntType(8).
            as_pointer()])
        kmoq__fofw = cgutils.get_or_insert_function(c.builder.module,
            ljrn__vyxfz, name='box_dict_str_array')
        yxng__ltexb = cgutils.create_struct_proxy(types.Array(types.int32, 
            1, 'C'))(c.context, c.builder, uio__jxmlj.data)
        yqxi__ssvv = c.builder.extract_value(yxng__ltexb.shape, 0)
        wlmwv__ltvz = yxng__ltexb.data
        lur__vqir = cgutils.create_struct_proxy(types.Array(types.int8, 1, 'C')
            )(c.context, c.builder, uio__jxmlj.null_bitmap).data
        vww__dpj = c.builder.call(kmoq__fofw, [yqxi__ssvv, ngq__llv,
            wlmwv__ltvz, lur__vqir])
        c.pyapi.decref(ngq__llv)
    else:
        lpn__bearr = c.context.insert_const_string(c.builder.module, 'pyarrow')
        ueu__yawk = c.pyapi.import_module_noblock(lpn__bearr)
        ywzud__vdalv = c.pyapi.object_getattr_string(ueu__yawk,
            'DictionaryArray')
        c.context.nrt.incref(c.builder, typ.data, husn__kju.data)
        ngq__llv = c.box(typ.data, husn__kju.data)
        c.context.nrt.incref(c.builder, dict_indices_arr_type, husn__kju.
            indices)
        hvgm__nzx = c.box(dict_indices_arr_type, husn__kju.indices)
        yiu__rof = c.pyapi.call_method(ywzud__vdalv, 'from_arrays', (
            hvgm__nzx, ngq__llv))
        hck__tejdd = c.pyapi.bool_from_bool(c.context.get_constant(types.
            bool_, False))
        vww__dpj = c.pyapi.call_method(yiu__rof, 'to_numpy', (hck__tejdd,))
        c.pyapi.decref(ueu__yawk)
        c.pyapi.decref(ngq__llv)
        c.pyapi.decref(hvgm__nzx)
        c.pyapi.decref(ywzud__vdalv)
        c.pyapi.decref(yiu__rof)
        c.pyapi.decref(hck__tejdd)
    c.context.nrt.decref(c.builder, typ, val)
    return vww__dpj


@overload(len, no_unliteral=True)
def overload_dict_arr_len(A):
    if isinstance(A, DictionaryArrayType):
        return lambda A: len(A._indices)


@overload_attribute(DictionaryArrayType, 'shape')
def overload_dict_arr_shape(A):
    return lambda A: (len(A._indices),)


@overload_attribute(DictionaryArrayType, 'ndim')
def overload_dict_arr_ndim(A):
    return lambda A: 1


@overload_attribute(DictionaryArrayType, 'size')
def overload_dict_arr_size(A):
    return lambda A: len(A._indices)


@overload_method(DictionaryArrayType, 'tolist', no_unliteral=True)
def overload_dict_arr_tolist(A):
    return lambda A: list(A)


overload_method(DictionaryArrayType, 'astype', no_unliteral=True)(
    overload_str_arr_astype)


@overload_method(DictionaryArrayType, 'copy', no_unliteral=True)
def overload_dict_arr_copy(A):

    def copy_impl(A):
        return init_dict_arr(A._data.copy(), A._indices.copy(), A.
            _has_global_dictionary)
    return copy_impl


@overload_attribute(DictionaryArrayType, 'dtype')
def overload_dict_arr_dtype(A):
    return lambda A: A._data.dtype


@overload_attribute(DictionaryArrayType, 'nbytes')
def dict_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._indices.nbytes


@lower_constant(DictionaryArrayType)
def lower_constant_dict_arr(context, builder, typ, pyval):
    if bodo.hiframes.boxing._use_dict_str_type and isinstance(pyval, np.ndarray
        ):
        pyval = pa.array(pyval).dictionary_encode()
    jbk__prle = pyval.dictionary.to_numpy(False)
    ucw__yuxkz = pd.array(pyval.indices, 'Int32')
    jbk__prle = context.get_constant_generic(builder, typ.data, jbk__prle)
    ucw__yuxkz = context.get_constant_generic(builder,
        dict_indices_arr_type, ucw__yuxkz)
    eegai__fatyc = context.get_constant(types.bool_, False)
    mnj__amokx = lir.Constant.literal_struct([jbk__prle, ucw__yuxkz,
        eegai__fatyc])
    return mnj__amokx


@overload(operator.getitem, no_unliteral=True)
def dict_arr_getitem(A, ind):
    if not isinstance(A, DictionaryArrayType):
        return
    if isinstance(ind, types.Integer):

        def dict_arr_getitem_impl(A, ind):
            if bodo.libs.array_kernels.isna(A._indices, ind):
                return ''
            pdggp__fcoyf = A._indices[ind]
            return A._data[pdggp__fcoyf]
        return dict_arr_getitem_impl
    return lambda A, ind: init_dict_arr(A._data, A._indices[ind], A.
        _has_global_dictionary)


@overload_method(DictionaryArrayType, '_decode', no_unliteral=True)
def overload_dict_arr_decode(A):

    def impl(A):
        jaxtk__frzi = A._data
        fsipm__mrah = A._indices
        yqxi__ssvv = len(fsipm__mrah)
        ntk__dszd = [get_str_arr_item_length(jaxtk__frzi, ttf__lvc) for
            ttf__lvc in range(len(jaxtk__frzi))]
        hkir__jmrx = 0
        for ttf__lvc in range(yqxi__ssvv):
            if not bodo.libs.array_kernels.isna(fsipm__mrah, ttf__lvc):
                hkir__jmrx += ntk__dszd[fsipm__mrah[ttf__lvc]]
        jezvw__tzp = pre_alloc_string_array(yqxi__ssvv, hkir__jmrx)
        for ttf__lvc in range(yqxi__ssvv):
            if bodo.libs.array_kernels.isna(fsipm__mrah, ttf__lvc):
                bodo.libs.array_kernels.setna(jezvw__tzp, ttf__lvc)
                continue
            ind = fsipm__mrah[ttf__lvc]
            if bodo.libs.array_kernels.isna(jaxtk__frzi, ind):
                bodo.libs.array_kernels.setna(jezvw__tzp, ttf__lvc)
                continue
            jezvw__tzp[ttf__lvc] = jaxtk__frzi[ind]
        return jezvw__tzp
    return impl


@overload(operator.setitem)
def dict_arr_setitem(A, idx, val):
    if not isinstance(A, DictionaryArrayType):
        return
    raise_bodo_error(
        "DictionaryArrayType is read-only and doesn't support setitem yet")


@numba.njit(no_cpython_wrapper=True)
def find_dict_ind(arr, val):
    pdggp__fcoyf = -1
    jaxtk__frzi = arr._data
    for ttf__lvc in range(len(jaxtk__frzi)):
        if bodo.libs.array_kernels.isna(jaxtk__frzi, ttf__lvc):
            continue
        if jaxtk__frzi[ttf__lvc] == val:
            pdggp__fcoyf = ttf__lvc
            break
    return pdggp__fcoyf


@numba.njit(no_cpython_wrapper=True)
def dict_arr_eq(arr, val):
    yqxi__ssvv = len(arr)
    pdggp__fcoyf = find_dict_ind(arr, val)
    if pdggp__fcoyf == -1:
        return init_bool_array(np.full(yqxi__ssvv, False, np.bool_), arr.
            _indices._null_bitmap.copy())
    return arr._indices == pdggp__fcoyf


@numba.njit(no_cpython_wrapper=True)
def dict_arr_ne(arr, val):
    yqxi__ssvv = len(arr)
    pdggp__fcoyf = find_dict_ind(arr, val)
    if pdggp__fcoyf == -1:
        return init_bool_array(np.full(yqxi__ssvv, True, np.bool_), arr.
            _indices._null_bitmap.copy())
    return arr._indices != pdggp__fcoyf


def get_binary_op_overload(op, lhs, rhs):
    if op == operator.eq:
        if lhs == dict_str_arr_type and types.unliteral(rhs
            ) == bodo.string_type:
            return lambda lhs, rhs: dict_arr_eq(lhs, rhs)
        if rhs == dict_str_arr_type and types.unliteral(lhs
            ) == bodo.string_type:
            return lambda lhs, rhs: dict_arr_eq(rhs, lhs)
    if op == operator.ne:
        if lhs == dict_str_arr_type and types.unliteral(rhs
            ) == bodo.string_type:
            return lambda lhs, rhs: dict_arr_ne(lhs, rhs)
        if rhs == dict_str_arr_type and types.unliteral(lhs
            ) == bodo.string_type:
            return lambda lhs, rhs: dict_arr_ne(rhs, lhs)


def convert_dict_arr_to_int(arr, dtype):
    return arr


@overload(convert_dict_arr_to_int)
def convert_dict_arr_to_int_overload(arr, dtype):

    def impl(arr, dtype):
        kzom__sfl = arr._data
        fgpu__ralze = bodo.libs.int_arr_ext.alloc_int_array(len(kzom__sfl),
            dtype)
        for imru__ihse in range(len(kzom__sfl)):
            if bodo.libs.array_kernels.isna(kzom__sfl, imru__ihse):
                bodo.libs.array_kernels.setna(fgpu__ralze, imru__ihse)
                continue
            fgpu__ralze[imru__ihse] = np.int64(kzom__sfl[imru__ihse])
        yqxi__ssvv = len(arr)
        fsipm__mrah = arr._indices
        jezvw__tzp = bodo.libs.int_arr_ext.alloc_int_array(yqxi__ssvv, dtype)
        for ttf__lvc in range(yqxi__ssvv):
            if bodo.libs.array_kernels.isna(fsipm__mrah, ttf__lvc):
                bodo.libs.array_kernels.setna(jezvw__tzp, ttf__lvc)
                continue
            jezvw__tzp[ttf__lvc] = fgpu__ralze[fsipm__mrah[ttf__lvc]]
        return jezvw__tzp
    return impl


def cat_dict_str(arrs, sep):
    pass


@overload(cat_dict_str)
def cat_dict_str_overload(arrs, sep):
    wsb__buem = len(arrs)
    ieswi__jzzb = 'def impl(arrs, sep):\n'
    ieswi__jzzb += '  ind_map = {}\n'
    ieswi__jzzb += '  out_strs = []\n'
    ieswi__jzzb += '  n = len(arrs[0])\n'
    for ttf__lvc in range(wsb__buem):
        ieswi__jzzb += f'  indices{ttf__lvc} = arrs[{ttf__lvc}]._indices\n'
    for ttf__lvc in range(wsb__buem):
        ieswi__jzzb += f'  data{ttf__lvc} = arrs[{ttf__lvc}]._data\n'
    ieswi__jzzb += (
        '  out_indices = bodo.libs.int_arr_ext.alloc_int_array(n, np.int32)\n')
    ieswi__jzzb += '  for i in range(n):\n'
    ysc__kaldd = ' or '.join([
        f'bodo.libs.array_kernels.isna(arrs[{ttf__lvc}], i)' for ttf__lvc in
        range(wsb__buem)])
    ieswi__jzzb += f'    if {ysc__kaldd}:\n'
    ieswi__jzzb += '      bodo.libs.array_kernels.setna(out_indices, i)\n'
    ieswi__jzzb += '      continue\n'
    for ttf__lvc in range(wsb__buem):
        ieswi__jzzb += f'    ind{ttf__lvc} = indices{ttf__lvc}[i]\n'
    yuz__offa = '(' + ', '.join(f'ind{ttf__lvc}' for ttf__lvc in range(
        wsb__buem)) + ')'
    ieswi__jzzb += f'    if {yuz__offa} not in ind_map:\n'
    ieswi__jzzb += '      out_ind = len(out_strs)\n'
    ieswi__jzzb += f'      ind_map[{yuz__offa}] = out_ind\n'
    jne__miq = "''" if is_overload_none(sep) else 'sep'
    igmp__poj = ', '.join([f'data{ttf__lvc}[ind{ttf__lvc}]' for ttf__lvc in
        range(wsb__buem)])
    ieswi__jzzb += f'      v = {jne__miq}.join([{igmp__poj}])\n'
    ieswi__jzzb += '      out_strs.append(v)\n'
    ieswi__jzzb += '    else:\n'
    ieswi__jzzb += f'      out_ind = ind_map[{yuz__offa}]\n'
    ieswi__jzzb += '    out_indices[i] = out_ind\n'
    ieswi__jzzb += (
        '  out_str_arr = bodo.libs.str_arr_ext.str_arr_from_sequence(out_strs)\n'
        )
    ieswi__jzzb += """  return bodo.libs.dict_arr_ext.init_dict_arr(out_str_arr, out_indices, False)
"""
    anwq__zukya = {}
    exec(ieswi__jzzb, {'bodo': bodo, 'numba': numba, 'np': np}, anwq__zukya)
    impl = anwq__zukya['impl']
    return impl


@lower_cast(DictionaryArrayType, StringArrayType)
def cast_dict_str_arr_to_str_arr(context, builder, fromty, toty, val):
    if fromty != dict_str_arr_type:
        return
    kuo__jyg = bodo.utils.typing.decode_if_dict_array_overload(fromty)
    poh__gqgfe = toty(fromty)
    hjp__andv = context.compile_internal(builder, kuo__jyg, poh__gqgfe, (val,))
    return impl_ret_new_ref(context, builder, toty, hjp__andv)


@register_jitable
def str_replace(arr, pat, repl, flags, regex):
    jbk__prle = arr._data
    chgac__gpea = len(jbk__prle)
    yxf__ndl = pre_alloc_string_array(chgac__gpea, -1)
    if regex:
        rayt__szfj = re.compile(pat, flags)
        for ttf__lvc in range(chgac__gpea):
            if bodo.libs.array_kernels.isna(jbk__prle, ttf__lvc):
                bodo.libs.array_kernels.setna(yxf__ndl, ttf__lvc)
                continue
            yxf__ndl[ttf__lvc] = rayt__szfj.sub(repl=repl, string=jbk__prle
                [ttf__lvc])
    else:
        for ttf__lvc in range(chgac__gpea):
            if bodo.libs.array_kernels.isna(jbk__prle, ttf__lvc):
                bodo.libs.array_kernels.setna(yxf__ndl, ttf__lvc)
                continue
            yxf__ndl[ttf__lvc] = jbk__prle[ttf__lvc].replace(pat, repl)
    return init_dict_arr(yxf__ndl, arr._indices.copy(), arr.
        _has_global_dictionary)


@register_jitable
def str_startswith(arr, pat, na):
    husn__kju = arr._data
    njbgh__sofyb = len(husn__kju)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(njbgh__sofyb)
    for ttf__lvc in range(njbgh__sofyb):
        dict_arr_out[ttf__lvc] = husn__kju[ttf__lvc].startswith(pat)
    ucw__yuxkz = arr._indices
    oxdo__tczsz = len(ucw__yuxkz)
    jezvw__tzp = bodo.libs.bool_arr_ext.alloc_bool_array(oxdo__tczsz)
    for ttf__lvc in range(oxdo__tczsz):
        if bodo.libs.array_kernels.isna(arr, ttf__lvc):
            bodo.libs.array_kernels.setna(jezvw__tzp, ttf__lvc)
        else:
            jezvw__tzp[ttf__lvc] = dict_arr_out[ucw__yuxkz[ttf__lvc]]
    return jezvw__tzp


@register_jitable
def str_endswith(arr, pat, na):
    husn__kju = arr._data
    njbgh__sofyb = len(husn__kju)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(njbgh__sofyb)
    for ttf__lvc in range(njbgh__sofyb):
        dict_arr_out[ttf__lvc] = husn__kju[ttf__lvc].endswith(pat)
    ucw__yuxkz = arr._indices
    oxdo__tczsz = len(ucw__yuxkz)
    jezvw__tzp = bodo.libs.bool_arr_ext.alloc_bool_array(oxdo__tczsz)
    for ttf__lvc in range(oxdo__tczsz):
        if bodo.libs.array_kernels.isna(arr, ttf__lvc):
            bodo.libs.array_kernels.setna(jezvw__tzp, ttf__lvc)
        else:
            jezvw__tzp[ttf__lvc] = dict_arr_out[ucw__yuxkz[ttf__lvc]]
    return jezvw__tzp


@numba.njit
def str_series_contains_regex(arr, pat, case, flags, na, regex):
    husn__kju = arr._data
    nxwl__xyrwi = pd.Series(husn__kju)
    with numba.objmode(dict_arr_out=bodo.boolean_array):
        dict_arr_out = nxwl__xyrwi.array._str_contains(pat, case, flags, na,
            regex)
    ucw__yuxkz = arr._indices
    oxdo__tczsz = len(ucw__yuxkz)
    jezvw__tzp = bodo.libs.bool_arr_ext.alloc_bool_array(oxdo__tczsz)
    for ttf__lvc in range(oxdo__tczsz):
        if bodo.libs.array_kernels.isna(arr, ttf__lvc):
            bodo.libs.array_kernels.setna(jezvw__tzp, ttf__lvc)
        else:
            jezvw__tzp[ttf__lvc] = dict_arr_out[ucw__yuxkz[ttf__lvc]]
    return jezvw__tzp


@register_jitable
def str_contains_non_regex(arr, pat, case):
    husn__kju = arr._data
    njbgh__sofyb = len(husn__kju)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(njbgh__sofyb)
    if not case:
        wlqx__mgqv = pat.upper()
    for ttf__lvc in range(njbgh__sofyb):
        if case:
            dict_arr_out[ttf__lvc] = pat in husn__kju[ttf__lvc]
        else:
            dict_arr_out[ttf__lvc] = wlqx__mgqv in husn__kju[ttf__lvc].upper()
    ucw__yuxkz = arr._indices
    oxdo__tczsz = len(ucw__yuxkz)
    jezvw__tzp = bodo.libs.bool_arr_ext.alloc_bool_array(oxdo__tczsz)
    for ttf__lvc in range(oxdo__tczsz):
        if bodo.libs.array_kernels.isna(arr, ttf__lvc):
            bodo.libs.array_kernels.setna(jezvw__tzp, ttf__lvc)
        else:
            jezvw__tzp[ttf__lvc] = dict_arr_out[ucw__yuxkz[ttf__lvc]]
    return jezvw__tzp


def create_simple_str2str_methods(func_name):
    ieswi__jzzb = f"""def str_{func_name}(arr):
    data_arr = arr._data
    n_data = len(data_arr)
    out_str_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n_data, -1)
    for i in range(n_data):
        if bodo.libs.array_kernels.isna(data_arr, i):
            bodo.libs.array_kernels.setna(out_str_arr, i)
            continue
        out_str_arr[i] = data_arr[i].{func_name}()
    return init_dict_arr(out_str_arr, arr._indices.copy(), arr._has_global_dictionary)
"""
    anwq__zukya = {}
    exec(ieswi__jzzb, {'bodo': bodo, 'numba': numba, 'init_dict_arr':
        init_dict_arr}, anwq__zukya)
    return anwq__zukya[f'str_{func_name}']


def _register_simple_str2str_methods():
    xggzx__qnejs = ['capitalize', 'lower', 'swapcase', 'title', 'upper']
    for kuo__jyg in xggzx__qnejs:
        edhj__ndgu = create_simple_str2str_methods(kuo__jyg)
        edhj__ndgu = register_jitable(edhj__ndgu)
        globals()[f'str_{kuo__jyg}'] = edhj__ndgu


_register_simple_str2str_methods()


@register_jitable
def str_center(arr, width, fillchar):
    jbk__prle = arr._data
    chgac__gpea = len(jbk__prle)
    yxf__ndl = pre_alloc_string_array(chgac__gpea, -1)
    for ttf__lvc in range(chgac__gpea):
        if bodo.libs.array_kernels.isna(jbk__prle, ttf__lvc):
            yxf__ndl[ttf__lvc] = ''
            bodo.libs.array_kernels.setna(yxf__ndl, ttf__lvc)
            continue
        yxf__ndl[ttf__lvc] = jbk__prle[ttf__lvc].center(width, fillchar)
    return init_dict_arr(yxf__ndl, arr._indices.copy(), arr.
        _has_global_dictionary)
