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
        bfgb__zqn = [('data', fe_type.data), ('indices',
            dict_indices_arr_type), ('has_global_dictionary', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, bfgb__zqn)


make_attribute_wrapper(DictionaryArrayType, 'data', '_data')
make_attribute_wrapper(DictionaryArrayType, 'indices', '_indices')
make_attribute_wrapper(DictionaryArrayType, 'has_global_dictionary',
    '_has_global_dictionary')
lower_builtin('getiter', dict_str_arr_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_dict_arr(typingctx, data_t, indices_t, glob_dict_t=None):
    assert indices_t == dict_indices_arr_type, 'invalid indices type for dict array'

    def codegen(context, builder, signature, args):
        zyu__aidis, wgnpq__hchv, nncfm__jkjh = args
        bfsux__pzq = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        bfsux__pzq.data = zyu__aidis
        bfsux__pzq.indices = wgnpq__hchv
        bfsux__pzq.has_global_dictionary = nncfm__jkjh
        context.nrt.incref(builder, signature.args[0], zyu__aidis)
        context.nrt.incref(builder, signature.args[1], wgnpq__hchv)
        return bfsux__pzq._getvalue()
    mzl__gyy = DictionaryArrayType(data_t)
    qxs__btg = mzl__gyy(data_t, indices_t, types.bool_)
    return qxs__btg, codegen


@typeof_impl.register(pa.DictionaryArray)
def typeof_dict_value(val, c):
    if val.type.value_type == pa.string():
        return dict_str_arr_type


def to_pa_dict_arr(A):
    if isinstance(A, pa.DictionaryArray):
        return A
    for i in range(len(A)):
        if pd.isna(A[i]):
            A[i] = None
    return pa.array(A).dictionary_encode()


@unbox(DictionaryArrayType)
def unbox_dict_arr(typ, val, c):
    if bodo.hiframes.boxing._use_dict_str_type:
        dycxp__hzrc = c.pyapi.unserialize(c.pyapi.serialize_object(
            to_pa_dict_arr))
        val = c.pyapi.call_function_objargs(dycxp__hzrc, [val])
        c.pyapi.decref(dycxp__hzrc)
    bfsux__pzq = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    myhop__wnkgr = c.pyapi.object_getattr_string(val, 'dictionary')
    kswq__mqwmk = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_,
        False))
    hrxaz__cdf = c.pyapi.call_method(myhop__wnkgr, 'to_numpy', (kswq__mqwmk,))
    bfsux__pzq.data = c.unbox(typ.data, hrxaz__cdf).value
    ogz__stk = c.pyapi.object_getattr_string(val, 'indices')
    noo__bmjj = c.context.insert_const_string(c.builder.module, 'pandas')
    mwf__arxzh = c.pyapi.import_module_noblock(noo__bmjj)
    ukd__gtl = c.pyapi.string_from_constant_string('Int32')
    rjzrk__kovbf = c.pyapi.call_method(mwf__arxzh, 'array', (ogz__stk,
        ukd__gtl))
    bfsux__pzq.indices = c.unbox(dict_indices_arr_type, rjzrk__kovbf).value
    bfsux__pzq.has_global_dictionary = c.context.get_constant(types.bool_, 
        False)
    c.pyapi.decref(myhop__wnkgr)
    c.pyapi.decref(kswq__mqwmk)
    c.pyapi.decref(hrxaz__cdf)
    c.pyapi.decref(ogz__stk)
    c.pyapi.decref(mwf__arxzh)
    c.pyapi.decref(ukd__gtl)
    c.pyapi.decref(rjzrk__kovbf)
    if bodo.hiframes.boxing._use_dict_str_type:
        c.pyapi.decref(val)
    kkcu__onzvu = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(bfsux__pzq._getvalue(), is_error=kkcu__onzvu)


@box(DictionaryArrayType)
def box_dict_arr(typ, val, c):
    bfsux__pzq = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ == dict_str_arr_type:
        c.context.nrt.incref(c.builder, typ.data, bfsux__pzq.data)
        mag__cwe = c.box(typ.data, bfsux__pzq.data)
        ckvnj__demrx = cgutils.create_struct_proxy(dict_indices_arr_type)(c
            .context, c.builder, bfsux__pzq.indices)
        kbb__zhrh = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), c.
            pyapi.pyobj, lir.IntType(32).as_pointer(), lir.IntType(8).
            as_pointer()])
        fav__ewkoj = cgutils.get_or_insert_function(c.builder.module,
            kbb__zhrh, name='box_dict_str_array')
        kwg__qdy = cgutils.create_struct_proxy(types.Array(types.int32, 1, 'C')
            )(c.context, c.builder, ckvnj__demrx.data)
        pup__hudb = c.builder.extract_value(kwg__qdy.shape, 0)
        exmjk__cyjtt = kwg__qdy.data
        ziae__dix = cgutils.create_struct_proxy(types.Array(types.int8, 1, 'C')
            )(c.context, c.builder, ckvnj__demrx.null_bitmap).data
        hrxaz__cdf = c.builder.call(fav__ewkoj, [pup__hudb, mag__cwe,
            exmjk__cyjtt, ziae__dix])
        c.pyapi.decref(mag__cwe)
    else:
        noo__bmjj = c.context.insert_const_string(c.builder.module, 'pyarrow')
        yynbo__nlgrc = c.pyapi.import_module_noblock(noo__bmjj)
        ftdwm__sbj = c.pyapi.object_getattr_string(yynbo__nlgrc,
            'DictionaryArray')
        c.context.nrt.incref(c.builder, typ.data, bfsux__pzq.data)
        mag__cwe = c.box(typ.data, bfsux__pzq.data)
        c.context.nrt.incref(c.builder, dict_indices_arr_type, bfsux__pzq.
            indices)
        ogz__stk = c.box(dict_indices_arr_type, bfsux__pzq.indices)
        iru__wjm = c.pyapi.call_method(ftdwm__sbj, 'from_arrays', (ogz__stk,
            mag__cwe))
        kswq__mqwmk = c.pyapi.bool_from_bool(c.context.get_constant(types.
            bool_, False))
        hrxaz__cdf = c.pyapi.call_method(iru__wjm, 'to_numpy', (kswq__mqwmk,))
        c.pyapi.decref(yynbo__nlgrc)
        c.pyapi.decref(mag__cwe)
        c.pyapi.decref(ogz__stk)
        c.pyapi.decref(ftdwm__sbj)
        c.pyapi.decref(iru__wjm)
        c.pyapi.decref(kswq__mqwmk)
    c.context.nrt.decref(c.builder, typ, val)
    return hrxaz__cdf


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
    vvtb__pagq = pyval.dictionary.to_numpy(False)
    xgzjt__bjndd = pd.array(pyval.indices, 'Int32')
    vvtb__pagq = context.get_constant_generic(builder, typ.data, vvtb__pagq)
    xgzjt__bjndd = context.get_constant_generic(builder,
        dict_indices_arr_type, xgzjt__bjndd)
    msbjg__fdg = context.get_constant(types.bool_, False)
    esexi__vknkr = lir.Constant.literal_struct([vvtb__pagq, xgzjt__bjndd,
        msbjg__fdg])
    return esexi__vknkr


@overload(operator.getitem, no_unliteral=True)
def dict_arr_getitem(A, ind):
    if not isinstance(A, DictionaryArrayType):
        return
    if isinstance(ind, types.Integer):

        def dict_arr_getitem_impl(A, ind):
            if bodo.libs.array_kernels.isna(A._indices, ind):
                return ''
            nko__nzhlv = A._indices[ind]
            return A._data[nko__nzhlv]
        return dict_arr_getitem_impl
    return lambda A, ind: init_dict_arr(A._data, A._indices[ind], A.
        _has_global_dictionary)


@overload_method(DictionaryArrayType, '_decode', no_unliteral=True)
def overload_dict_arr_decode(A):

    def impl(A):
        zyu__aidis = A._data
        wgnpq__hchv = A._indices
        pup__hudb = len(wgnpq__hchv)
        iktxf__hmnpo = [get_str_arr_item_length(zyu__aidis, i) for i in
            range(len(zyu__aidis))]
        tul__dipyi = 0
        for i in range(pup__hudb):
            if not bodo.libs.array_kernels.isna(wgnpq__hchv, i):
                tul__dipyi += iktxf__hmnpo[wgnpq__hchv[i]]
        yyco__vzgm = pre_alloc_string_array(pup__hudb, tul__dipyi)
        for i in range(pup__hudb):
            if bodo.libs.array_kernels.isna(wgnpq__hchv, i):
                bodo.libs.array_kernels.setna(yyco__vzgm, i)
                continue
            ind = wgnpq__hchv[i]
            if bodo.libs.array_kernels.isna(zyu__aidis, ind):
                bodo.libs.array_kernels.setna(yyco__vzgm, i)
                continue
            yyco__vzgm[i] = zyu__aidis[ind]
        return yyco__vzgm
    return impl


@overload(operator.setitem)
def dict_arr_setitem(A, idx, val):
    if not isinstance(A, DictionaryArrayType):
        return
    raise_bodo_error(
        "DictionaryArrayType is read-only and doesn't support setitem yet")


@numba.njit(no_cpython_wrapper=True)
def find_dict_ind(arr, val):
    nko__nzhlv = -1
    zyu__aidis = arr._data
    for i in range(len(zyu__aidis)):
        if bodo.libs.array_kernels.isna(zyu__aidis, i):
            continue
        if zyu__aidis[i] == val:
            nko__nzhlv = i
            break
    return nko__nzhlv


@numba.njit(no_cpython_wrapper=True)
def dict_arr_eq(arr, val):
    pup__hudb = len(arr)
    nko__nzhlv = find_dict_ind(arr, val)
    if nko__nzhlv == -1:
        return init_bool_array(np.full(pup__hudb, False, np.bool_), arr.
            _indices._null_bitmap.copy())
    return arr._indices == nko__nzhlv


@numba.njit(no_cpython_wrapper=True)
def dict_arr_ne(arr, val):
    pup__hudb = len(arr)
    nko__nzhlv = find_dict_ind(arr, val)
    if nko__nzhlv == -1:
        return init_bool_array(np.full(pup__hudb, True, np.bool_), arr.
            _indices._null_bitmap.copy())
    return arr._indices != nko__nzhlv


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
        cbxpa__lyoes = arr._data
        tetr__hxo = bodo.libs.int_arr_ext.alloc_int_array(len(cbxpa__lyoes),
            dtype)
        for pporj__aniv in range(len(cbxpa__lyoes)):
            if bodo.libs.array_kernels.isna(cbxpa__lyoes, pporj__aniv):
                bodo.libs.array_kernels.setna(tetr__hxo, pporj__aniv)
                continue
            tetr__hxo[pporj__aniv] = np.int64(cbxpa__lyoes[pporj__aniv])
        pup__hudb = len(arr)
        wgnpq__hchv = arr._indices
        yyco__vzgm = bodo.libs.int_arr_ext.alloc_int_array(pup__hudb, dtype)
        for i in range(pup__hudb):
            if bodo.libs.array_kernels.isna(wgnpq__hchv, i):
                bodo.libs.array_kernels.setna(yyco__vzgm, i)
                continue
            yyco__vzgm[i] = tetr__hxo[wgnpq__hchv[i]]
        return yyco__vzgm
    return impl


def cat_dict_str(arrs, sep):
    pass


@overload(cat_dict_str)
def cat_dict_str_overload(arrs, sep):
    vhxz__kcqrv = len(arrs)
    vutb__uzfl = 'def impl(arrs, sep):\n'
    vutb__uzfl += '  ind_map = {}\n'
    vutb__uzfl += '  out_strs = []\n'
    vutb__uzfl += '  n = len(arrs[0])\n'
    for i in range(vhxz__kcqrv):
        vutb__uzfl += f'  indices{i} = arrs[{i}]._indices\n'
    for i in range(vhxz__kcqrv):
        vutb__uzfl += f'  data{i} = arrs[{i}]._data\n'
    vutb__uzfl += (
        '  out_indices = bodo.libs.int_arr_ext.alloc_int_array(n, np.int32)\n')
    vutb__uzfl += '  for i in range(n):\n'
    kkth__ogfib = ' or '.join([
        f'bodo.libs.array_kernels.isna(arrs[{i}], i)' for i in range(
        vhxz__kcqrv)])
    vutb__uzfl += f'    if {kkth__ogfib}:\n'
    vutb__uzfl += '      bodo.libs.array_kernels.setna(out_indices, i)\n'
    vutb__uzfl += '      continue\n'
    for i in range(vhxz__kcqrv):
        vutb__uzfl += f'    ind{i} = indices{i}[i]\n'
    edod__kvy = '(' + ', '.join(f'ind{i}' for i in range(vhxz__kcqrv)) + ')'
    vutb__uzfl += f'    if {edod__kvy} not in ind_map:\n'
    vutb__uzfl += '      out_ind = len(out_strs)\n'
    vutb__uzfl += f'      ind_map[{edod__kvy}] = out_ind\n'
    lrju__txl = "''" if is_overload_none(sep) else 'sep'
    xiywk__llkhw = ', '.join([f'data{i}[ind{i}]' for i in range(vhxz__kcqrv)])
    vutb__uzfl += f'      v = {lrju__txl}.join([{xiywk__llkhw}])\n'
    vutb__uzfl += '      out_strs.append(v)\n'
    vutb__uzfl += '    else:\n'
    vutb__uzfl += f'      out_ind = ind_map[{edod__kvy}]\n'
    vutb__uzfl += '    out_indices[i] = out_ind\n'
    vutb__uzfl += (
        '  out_str_arr = bodo.libs.str_arr_ext.str_arr_from_sequence(out_strs)\n'
        )
    vutb__uzfl += """  return bodo.libs.dict_arr_ext.init_dict_arr(out_str_arr, out_indices, False)
"""
    ftm__ism = {}
    exec(vutb__uzfl, {'bodo': bodo, 'numba': numba, 'np': np}, ftm__ism)
    impl = ftm__ism['impl']
    return impl


@lower_cast(DictionaryArrayType, StringArrayType)
def cast_dict_str_arr_to_str_arr(context, builder, fromty, toty, val):
    if fromty != dict_str_arr_type:
        return
    kmdni__ozxm = bodo.utils.typing.decode_if_dict_array_overload(fromty)
    qxs__btg = toty(fromty)
    gav__abdp = context.compile_internal(builder, kmdni__ozxm, qxs__btg, (val,)
        )
    return impl_ret_new_ref(context, builder, toty, gav__abdp)


@register_jitable
def str_replace(arr, pat, repl, flags, regex):
    vvtb__pagq = arr._data
    xva__wwt = len(vvtb__pagq)
    rmdpa__mrbi = pre_alloc_string_array(xva__wwt, -1)
    if regex:
        mdkd__yzrhq = re.compile(pat, flags)
        for i in range(xva__wwt):
            if bodo.libs.array_kernels.isna(vvtb__pagq, i):
                bodo.libs.array_kernels.setna(rmdpa__mrbi, i)
                continue
            rmdpa__mrbi[i] = mdkd__yzrhq.sub(repl=repl, string=vvtb__pagq[i])
    else:
        for i in range(xva__wwt):
            if bodo.libs.array_kernels.isna(vvtb__pagq, i):
                bodo.libs.array_kernels.setna(rmdpa__mrbi, i)
                continue
            rmdpa__mrbi[i] = vvtb__pagq[i].replace(pat, repl)
    return init_dict_arr(rmdpa__mrbi, arr._indices.copy(), arr.
        _has_global_dictionary)


@register_jitable
def str_startswith(arr, pat, na):
    bfsux__pzq = arr._data
    fuowp__zpjel = len(bfsux__pzq)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(fuowp__zpjel)
    for i in range(fuowp__zpjel):
        dict_arr_out[i] = bfsux__pzq[i].startswith(pat)
    xgzjt__bjndd = arr._indices
    qmga__uyted = len(xgzjt__bjndd)
    yyco__vzgm = bodo.libs.bool_arr_ext.alloc_bool_array(qmga__uyted)
    for i in range(qmga__uyted):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(yyco__vzgm, i)
        else:
            yyco__vzgm[i] = dict_arr_out[xgzjt__bjndd[i]]
    return yyco__vzgm


@register_jitable
def str_endswith(arr, pat, na):
    bfsux__pzq = arr._data
    fuowp__zpjel = len(bfsux__pzq)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(fuowp__zpjel)
    for i in range(fuowp__zpjel):
        dict_arr_out[i] = bfsux__pzq[i].endswith(pat)
    xgzjt__bjndd = arr._indices
    qmga__uyted = len(xgzjt__bjndd)
    yyco__vzgm = bodo.libs.bool_arr_ext.alloc_bool_array(qmga__uyted)
    for i in range(qmga__uyted):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(yyco__vzgm, i)
        else:
            yyco__vzgm[i] = dict_arr_out[xgzjt__bjndd[i]]
    return yyco__vzgm


@numba.njit
def str_series_contains_regex(arr, pat, case, flags, na, regex):
    bfsux__pzq = arr._data
    ewqd__ahp = pd.Series(bfsux__pzq)
    with numba.objmode(dict_arr_out=bodo.boolean_array):
        dict_arr_out = ewqd__ahp.array._str_contains(pat, case, flags, na,
            regex)
    xgzjt__bjndd = arr._indices
    qmga__uyted = len(xgzjt__bjndd)
    yyco__vzgm = bodo.libs.bool_arr_ext.alloc_bool_array(qmga__uyted)
    for i in range(qmga__uyted):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(yyco__vzgm, i)
        else:
            yyco__vzgm[i] = dict_arr_out[xgzjt__bjndd[i]]
    return yyco__vzgm


@register_jitable
def str_contains_non_regex(arr, pat, case):
    bfsux__pzq = arr._data
    fuowp__zpjel = len(bfsux__pzq)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(fuowp__zpjel)
    if not case:
        jwf__mbnmt = pat.upper()
    for i in range(fuowp__zpjel):
        if case:
            dict_arr_out[i] = pat in bfsux__pzq[i]
        else:
            dict_arr_out[i] = jwf__mbnmt in bfsux__pzq[i].upper()
    xgzjt__bjndd = arr._indices
    qmga__uyted = len(xgzjt__bjndd)
    yyco__vzgm = bodo.libs.bool_arr_ext.alloc_bool_array(qmga__uyted)
    for i in range(qmga__uyted):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(yyco__vzgm, i)
        else:
            yyco__vzgm[i] = dict_arr_out[xgzjt__bjndd[i]]
    return yyco__vzgm


def create_simple_str2str_methods(func_name, func_args):
    vutb__uzfl = f"""def str_{func_name}({', '.join(func_args)}):
    data_arr = arr._data
    n_data = len(data_arr)
    out_str_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n_data, -1)
    for i in range(n_data):
        if bodo.libs.array_kernels.isna(data_arr, i):
            bodo.libs.array_kernels.setna(out_str_arr, i)
            continue
        out_str_arr[i] = data_arr[i].{func_name}({', '.join(func_args[1:])})
    return init_dict_arr(out_str_arr, arr._indices.copy(), arr._has_global_dictionary)
"""
    ftm__ism = {}
    exec(vutb__uzfl, {'bodo': bodo, 'numba': numba, 'init_dict_arr':
        init_dict_arr}, ftm__ism)
    return ftm__ism[f'str_{func_name}']


def _register_simple_str2str_methods():
    jpx__dvund = {**dict.fromkeys(['capitalize', 'lower', 'swapcase',
        'title', 'upper'], ('arr',)), **dict.fromkeys(['lstrip', 'rstrip',
        'strip'], ('arr', 'to_strip')), **dict.fromkeys(['center', 'ljust',
        'rjust'], ('arr', 'width', 'fillchar')), **dict.fromkeys(['zfill'],
        ('arr', 'width'))}
    for func_name in jpx__dvund.keys():
        zif__ely = create_simple_str2str_methods(func_name, jpx__dvund[
            func_name])
        zif__ely = register_jitable(zif__ely)
        globals()[f'str_{func_name}'] = zif__ely


_register_simple_str2str_methods()


@register_jitable
def str_find(arr, sub, start, end):
    vvtb__pagq = arr._data
    xgzjt__bjndd = arr._indices
    xva__wwt = len(vvtb__pagq)
    qmga__uyted = len(xgzjt__bjndd)
    affac__auzh = bodo.libs.int_arr_ext.alloc_int_array(xva__wwt, np.int64)
    qtg__yov = bodo.libs.int_arr_ext.alloc_int_array(qmga__uyted, np.int64)
    for i in range(xva__wwt):
        if bodo.libs.array_kernels.isna(vvtb__pagq, i):
            bodo.libs.array_kernels.setna(affac__auzh, i)
            continue
        affac__auzh[i] = vvtb__pagq[i].find(sub, start, end)
    for i in range(qmga__uyted):
        if bodo.libs.array_kernels.isna(arr, i
            ) or bodo.libs.array_kernels.isna(affac__auzh, xgzjt__bjndd[i]):
            bodo.libs.array_kernels.setna(qtg__yov, i)
        else:
            qtg__yov[i] = affac__auzh[xgzjt__bjndd[i]]
    return qtg__yov


@register_jitable
def str_slice(arr, start, stop, step):
    vvtb__pagq = arr._data
    xva__wwt = len(vvtb__pagq)
    rmdpa__mrbi = bodo.libs.str_arr_ext.pre_alloc_string_array(xva__wwt, -1)
    for i in range(xva__wwt):
        if bodo.libs.array_kernels.isna(vvtb__pagq, i):
            bodo.libs.array_kernels.setna(rmdpa__mrbi, i)
            continue
        rmdpa__mrbi[i] = vvtb__pagq[i][start:stop:step]
    return init_dict_arr(rmdpa__mrbi, arr._indices.copy(), arr.
        _has_global_dictionary)


@register_jitable
def str_get(arr, i):
    vvtb__pagq = arr._data
    xgzjt__bjndd = arr._indices
    xva__wwt = len(vvtb__pagq)
    qmga__uyted = len(xgzjt__bjndd)
    rmdpa__mrbi = pre_alloc_string_array(xva__wwt, -1)
    yyco__vzgm = pre_alloc_string_array(qmga__uyted, -1)
    for pporj__aniv in range(xva__wwt):
        if bodo.libs.array_kernels.isna(vvtb__pagq, pporj__aniv) or not -len(
            vvtb__pagq[pporj__aniv]) <= i < len(vvtb__pagq[pporj__aniv]):
            bodo.libs.array_kernels.setna(rmdpa__mrbi, pporj__aniv)
            continue
        rmdpa__mrbi[pporj__aniv] = vvtb__pagq[pporj__aniv][i]
    for pporj__aniv in range(qmga__uyted):
        if bodo.libs.array_kernels.isna(xgzjt__bjndd, pporj__aniv
            ) or bodo.libs.array_kernels.isna(rmdpa__mrbi, xgzjt__bjndd[
            pporj__aniv]):
            bodo.libs.array_kernels.setna(yyco__vzgm, pporj__aniv)
            continue
        yyco__vzgm[pporj__aniv] = rmdpa__mrbi[xgzjt__bjndd[pporj__aniv]]
    return yyco__vzgm


@register_jitable
def str_repeat_int(arr, repeats):
    vvtb__pagq = arr._data
    xva__wwt = len(vvtb__pagq)
    rmdpa__mrbi = pre_alloc_string_array(xva__wwt, -1)
    for i in range(xva__wwt):
        if bodo.libs.array_kernels.isna(vvtb__pagq, i):
            bodo.libs.array_kernels.setna(rmdpa__mrbi, i)
            continue
        rmdpa__mrbi[i] = vvtb__pagq[i] * repeats
    return init_dict_arr(rmdpa__mrbi, arr._indices.copy(), arr.
        _has_global_dictionary)
