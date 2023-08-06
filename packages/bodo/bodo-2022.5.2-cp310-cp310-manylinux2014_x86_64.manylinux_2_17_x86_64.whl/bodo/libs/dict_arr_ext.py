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
        uomd__nord = [('data', fe_type.data), ('indices',
            dict_indices_arr_type), ('has_global_dictionary', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, uomd__nord)


make_attribute_wrapper(DictionaryArrayType, 'data', '_data')
make_attribute_wrapper(DictionaryArrayType, 'indices', '_indices')
make_attribute_wrapper(DictionaryArrayType, 'has_global_dictionary',
    '_has_global_dictionary')
lower_builtin('getiter', dict_str_arr_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_dict_arr(typingctx, data_t, indices_t, glob_dict_t=None):
    assert indices_t == dict_indices_arr_type, 'invalid indices type for dict array'

    def codegen(context, builder, signature, args):
        zpg__yesav, nrxcb__wmhyw, kqpgm__ijtun = args
        ixx__uezr = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        ixx__uezr.data = zpg__yesav
        ixx__uezr.indices = nrxcb__wmhyw
        ixx__uezr.has_global_dictionary = kqpgm__ijtun
        context.nrt.incref(builder, signature.args[0], zpg__yesav)
        context.nrt.incref(builder, signature.args[1], nrxcb__wmhyw)
        return ixx__uezr._getvalue()
    wvzva__frf = DictionaryArrayType(data_t)
    ynpm__ehodf = wvzva__frf(data_t, indices_t, types.bool_)
    return ynpm__ehodf, codegen


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
        frbr__iggx = c.pyapi.unserialize(c.pyapi.serialize_object(
            to_pa_dict_arr))
        val = c.pyapi.call_function_objargs(frbr__iggx, [val])
        c.pyapi.decref(frbr__iggx)
    ixx__uezr = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    lwek__cmg = c.pyapi.object_getattr_string(val, 'dictionary')
    rdder__wqve = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_,
        False))
    akghn__ymsko = c.pyapi.call_method(lwek__cmg, 'to_numpy', (rdder__wqve,))
    ixx__uezr.data = c.unbox(typ.data, akghn__ymsko).value
    spe__bmjb = c.pyapi.object_getattr_string(val, 'indices')
    rrh__wgxc = c.context.insert_const_string(c.builder.module, 'pandas')
    pms__msslt = c.pyapi.import_module_noblock(rrh__wgxc)
    yaxq__wtryo = c.pyapi.string_from_constant_string('Int32')
    pvq__xbwi = c.pyapi.call_method(pms__msslt, 'array', (spe__bmjb,
        yaxq__wtryo))
    ixx__uezr.indices = c.unbox(dict_indices_arr_type, pvq__xbwi).value
    ixx__uezr.has_global_dictionary = c.context.get_constant(types.bool_, False
        )
    c.pyapi.decref(lwek__cmg)
    c.pyapi.decref(rdder__wqve)
    c.pyapi.decref(akghn__ymsko)
    c.pyapi.decref(spe__bmjb)
    c.pyapi.decref(pms__msslt)
    c.pyapi.decref(yaxq__wtryo)
    c.pyapi.decref(pvq__xbwi)
    if bodo.hiframes.boxing._use_dict_str_type:
        c.pyapi.decref(val)
    sshq__hvd = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ixx__uezr._getvalue(), is_error=sshq__hvd)


@box(DictionaryArrayType)
def box_dict_arr(typ, val, c):
    ixx__uezr = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ == dict_str_arr_type:
        c.context.nrt.incref(c.builder, typ.data, ixx__uezr.data)
        wydk__kvzl = c.box(typ.data, ixx__uezr.data)
        pkpm__xlq = cgutils.create_struct_proxy(dict_indices_arr_type)(c.
            context, c.builder, ixx__uezr.indices)
        krrli__ujc = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), c.
            pyapi.pyobj, lir.IntType(32).as_pointer(), lir.IntType(8).
            as_pointer()])
        edruh__osjz = cgutils.get_or_insert_function(c.builder.module,
            krrli__ujc, name='box_dict_str_array')
        mqml__wktjx = cgutils.create_struct_proxy(types.Array(types.int32, 
            1, 'C'))(c.context, c.builder, pkpm__xlq.data)
        cbumw__jun = c.builder.extract_value(mqml__wktjx.shape, 0)
        iej__djss = mqml__wktjx.data
        nrduz__bum = cgutils.create_struct_proxy(types.Array(types.int8, 1,
            'C'))(c.context, c.builder, pkpm__xlq.null_bitmap).data
        akghn__ymsko = c.builder.call(edruh__osjz, [cbumw__jun, wydk__kvzl,
            iej__djss, nrduz__bum])
        c.pyapi.decref(wydk__kvzl)
    else:
        rrh__wgxc = c.context.insert_const_string(c.builder.module, 'pyarrow')
        azw__cavlp = c.pyapi.import_module_noblock(rrh__wgxc)
        aryr__wtqk = c.pyapi.object_getattr_string(azw__cavlp,
            'DictionaryArray')
        c.context.nrt.incref(c.builder, typ.data, ixx__uezr.data)
        wydk__kvzl = c.box(typ.data, ixx__uezr.data)
        c.context.nrt.incref(c.builder, dict_indices_arr_type, ixx__uezr.
            indices)
        spe__bmjb = c.box(dict_indices_arr_type, ixx__uezr.indices)
        oaku__koqrx = c.pyapi.call_method(aryr__wtqk, 'from_arrays', (
            spe__bmjb, wydk__kvzl))
        rdder__wqve = c.pyapi.bool_from_bool(c.context.get_constant(types.
            bool_, False))
        akghn__ymsko = c.pyapi.call_method(oaku__koqrx, 'to_numpy', (
            rdder__wqve,))
        c.pyapi.decref(azw__cavlp)
        c.pyapi.decref(wydk__kvzl)
        c.pyapi.decref(spe__bmjb)
        c.pyapi.decref(aryr__wtqk)
        c.pyapi.decref(oaku__koqrx)
        c.pyapi.decref(rdder__wqve)
    c.context.nrt.decref(c.builder, typ, val)
    return akghn__ymsko


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
    hde__ubvar = pyval.dictionary.to_numpy(False)
    ewpcn__ikvd = pd.array(pyval.indices, 'Int32')
    hde__ubvar = context.get_constant_generic(builder, typ.data, hde__ubvar)
    ewpcn__ikvd = context.get_constant_generic(builder,
        dict_indices_arr_type, ewpcn__ikvd)
    hiye__fkx = context.get_constant(types.bool_, False)
    ygdd__gnc = lir.Constant.literal_struct([hde__ubvar, ewpcn__ikvd,
        hiye__fkx])
    return ygdd__gnc


@overload(operator.getitem, no_unliteral=True)
def dict_arr_getitem(A, ind):
    if not isinstance(A, DictionaryArrayType):
        return
    if isinstance(ind, types.Integer):

        def dict_arr_getitem_impl(A, ind):
            if bodo.libs.array_kernels.isna(A._indices, ind):
                return ''
            hpc__gsy = A._indices[ind]
            return A._data[hpc__gsy]
        return dict_arr_getitem_impl
    return lambda A, ind: init_dict_arr(A._data, A._indices[ind], A.
        _has_global_dictionary)


@overload_method(DictionaryArrayType, '_decode', no_unliteral=True)
def overload_dict_arr_decode(A):

    def impl(A):
        zpg__yesav = A._data
        nrxcb__wmhyw = A._indices
        cbumw__jun = len(nrxcb__wmhyw)
        zacwq__ycgos = [get_str_arr_item_length(zpg__yesav, i) for i in
            range(len(zpg__yesav))]
        nrj__zbp = 0
        for i in range(cbumw__jun):
            if not bodo.libs.array_kernels.isna(nrxcb__wmhyw, i):
                nrj__zbp += zacwq__ycgos[nrxcb__wmhyw[i]]
        sriha__dtbmw = pre_alloc_string_array(cbumw__jun, nrj__zbp)
        for i in range(cbumw__jun):
            if bodo.libs.array_kernels.isna(nrxcb__wmhyw, i):
                bodo.libs.array_kernels.setna(sriha__dtbmw, i)
                continue
            ind = nrxcb__wmhyw[i]
            if bodo.libs.array_kernels.isna(zpg__yesav, ind):
                bodo.libs.array_kernels.setna(sriha__dtbmw, i)
                continue
            sriha__dtbmw[i] = zpg__yesav[ind]
        return sriha__dtbmw
    return impl


@overload(operator.setitem)
def dict_arr_setitem(A, idx, val):
    if not isinstance(A, DictionaryArrayType):
        return
    raise_bodo_error(
        "DictionaryArrayType is read-only and doesn't support setitem yet")


@numba.njit(no_cpython_wrapper=True)
def find_dict_ind(arr, val):
    hpc__gsy = -1
    zpg__yesav = arr._data
    for i in range(len(zpg__yesav)):
        if bodo.libs.array_kernels.isna(zpg__yesav, i):
            continue
        if zpg__yesav[i] == val:
            hpc__gsy = i
            break
    return hpc__gsy


@numba.njit(no_cpython_wrapper=True)
def dict_arr_eq(arr, val):
    cbumw__jun = len(arr)
    hpc__gsy = find_dict_ind(arr, val)
    if hpc__gsy == -1:
        return init_bool_array(np.full(cbumw__jun, False, np.bool_), arr.
            _indices._null_bitmap.copy())
    return arr._indices == hpc__gsy


@numba.njit(no_cpython_wrapper=True)
def dict_arr_ne(arr, val):
    cbumw__jun = len(arr)
    hpc__gsy = find_dict_ind(arr, val)
    if hpc__gsy == -1:
        return init_bool_array(np.full(cbumw__jun, True, np.bool_), arr.
            _indices._null_bitmap.copy())
    return arr._indices != hpc__gsy


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
        bsig__uayt = arr._data
        dnjla__qetf = bodo.libs.int_arr_ext.alloc_int_array(len(bsig__uayt),
            dtype)
        for gsj__tpc in range(len(bsig__uayt)):
            if bodo.libs.array_kernels.isna(bsig__uayt, gsj__tpc):
                bodo.libs.array_kernels.setna(dnjla__qetf, gsj__tpc)
                continue
            dnjla__qetf[gsj__tpc] = np.int64(bsig__uayt[gsj__tpc])
        cbumw__jun = len(arr)
        nrxcb__wmhyw = arr._indices
        sriha__dtbmw = bodo.libs.int_arr_ext.alloc_int_array(cbumw__jun, dtype)
        for i in range(cbumw__jun):
            if bodo.libs.array_kernels.isna(nrxcb__wmhyw, i):
                bodo.libs.array_kernels.setna(sriha__dtbmw, i)
                continue
            sriha__dtbmw[i] = dnjla__qetf[nrxcb__wmhyw[i]]
        return sriha__dtbmw
    return impl


def cat_dict_str(arrs, sep):
    pass


@overload(cat_dict_str)
def cat_dict_str_overload(arrs, sep):
    xdydo__sjiob = len(arrs)
    cprd__vvac = 'def impl(arrs, sep):\n'
    cprd__vvac += '  ind_map = {}\n'
    cprd__vvac += '  out_strs = []\n'
    cprd__vvac += '  n = len(arrs[0])\n'
    for i in range(xdydo__sjiob):
        cprd__vvac += f'  indices{i} = arrs[{i}]._indices\n'
    for i in range(xdydo__sjiob):
        cprd__vvac += f'  data{i} = arrs[{i}]._data\n'
    cprd__vvac += (
        '  out_indices = bodo.libs.int_arr_ext.alloc_int_array(n, np.int32)\n')
    cprd__vvac += '  for i in range(n):\n'
    oxx__fhmyh = ' or '.join([f'bodo.libs.array_kernels.isna(arrs[{i}], i)' for
        i in range(xdydo__sjiob)])
    cprd__vvac += f'    if {oxx__fhmyh}:\n'
    cprd__vvac += '      bodo.libs.array_kernels.setna(out_indices, i)\n'
    cprd__vvac += '      continue\n'
    for i in range(xdydo__sjiob):
        cprd__vvac += f'    ind{i} = indices{i}[i]\n'
    yextd__mgb = '(' + ', '.join(f'ind{i}' for i in range(xdydo__sjiob)) + ')'
    cprd__vvac += f'    if {yextd__mgb} not in ind_map:\n'
    cprd__vvac += '      out_ind = len(out_strs)\n'
    cprd__vvac += f'      ind_map[{yextd__mgb}] = out_ind\n'
    bkdu__qyh = "''" if is_overload_none(sep) else 'sep'
    kxl__dldr = ', '.join([f'data{i}[ind{i}]' for i in range(xdydo__sjiob)])
    cprd__vvac += f'      v = {bkdu__qyh}.join([{kxl__dldr}])\n'
    cprd__vvac += '      out_strs.append(v)\n'
    cprd__vvac += '    else:\n'
    cprd__vvac += f'      out_ind = ind_map[{yextd__mgb}]\n'
    cprd__vvac += '    out_indices[i] = out_ind\n'
    cprd__vvac += (
        '  out_str_arr = bodo.libs.str_arr_ext.str_arr_from_sequence(out_strs)\n'
        )
    cprd__vvac += """  return bodo.libs.dict_arr_ext.init_dict_arr(out_str_arr, out_indices, False)
"""
    kkr__qvy = {}
    exec(cprd__vvac, {'bodo': bodo, 'numba': numba, 'np': np}, kkr__qvy)
    impl = kkr__qvy['impl']
    return impl


@lower_cast(DictionaryArrayType, StringArrayType)
def cast_dict_str_arr_to_str_arr(context, builder, fromty, toty, val):
    if fromty != dict_str_arr_type:
        return
    acfu__fvrzv = bodo.utils.typing.decode_if_dict_array_overload(fromty)
    ynpm__ehodf = toty(fromty)
    dqls__icmnt = context.compile_internal(builder, acfu__fvrzv,
        ynpm__ehodf, (val,))
    return impl_ret_new_ref(context, builder, toty, dqls__icmnt)


@register_jitable
def str_replace(arr, pat, repl, flags, regex):
    hde__ubvar = arr._data
    lach__mdhdu = len(hde__ubvar)
    std__chfut = pre_alloc_string_array(lach__mdhdu, -1)
    if regex:
        hwrtr__vewh = re.compile(pat, flags)
        for i in range(lach__mdhdu):
            if bodo.libs.array_kernels.isna(hde__ubvar, i):
                bodo.libs.array_kernels.setna(std__chfut, i)
                continue
            std__chfut[i] = hwrtr__vewh.sub(repl=repl, string=hde__ubvar[i])
    else:
        for i in range(lach__mdhdu):
            if bodo.libs.array_kernels.isna(hde__ubvar, i):
                bodo.libs.array_kernels.setna(std__chfut, i)
                continue
            std__chfut[i] = hde__ubvar[i].replace(pat, repl)
    return init_dict_arr(std__chfut, arr._indices.copy(), arr.
        _has_global_dictionary)


@register_jitable
def str_startswith(arr, pat, na):
    ixx__uezr = arr._data
    wwa__abpx = len(ixx__uezr)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(wwa__abpx)
    for i in range(wwa__abpx):
        dict_arr_out[i] = ixx__uezr[i].startswith(pat)
    ewpcn__ikvd = arr._indices
    zsmua__rbc = len(ewpcn__ikvd)
    sriha__dtbmw = bodo.libs.bool_arr_ext.alloc_bool_array(zsmua__rbc)
    for i in range(zsmua__rbc):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(sriha__dtbmw, i)
        else:
            sriha__dtbmw[i] = dict_arr_out[ewpcn__ikvd[i]]
    return sriha__dtbmw


@register_jitable
def str_endswith(arr, pat, na):
    ixx__uezr = arr._data
    wwa__abpx = len(ixx__uezr)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(wwa__abpx)
    for i in range(wwa__abpx):
        dict_arr_out[i] = ixx__uezr[i].endswith(pat)
    ewpcn__ikvd = arr._indices
    zsmua__rbc = len(ewpcn__ikvd)
    sriha__dtbmw = bodo.libs.bool_arr_ext.alloc_bool_array(zsmua__rbc)
    for i in range(zsmua__rbc):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(sriha__dtbmw, i)
        else:
            sriha__dtbmw[i] = dict_arr_out[ewpcn__ikvd[i]]
    return sriha__dtbmw


@numba.njit
def str_series_contains_regex(arr, pat, case, flags, na, regex):
    ixx__uezr = arr._data
    vjg__fldyh = pd.Series(ixx__uezr)
    with numba.objmode(dict_arr_out=bodo.boolean_array):
        dict_arr_out = vjg__fldyh.array._str_contains(pat, case, flags, na,
            regex)
    ewpcn__ikvd = arr._indices
    zsmua__rbc = len(ewpcn__ikvd)
    sriha__dtbmw = bodo.libs.bool_arr_ext.alloc_bool_array(zsmua__rbc)
    for i in range(zsmua__rbc):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(sriha__dtbmw, i)
        else:
            sriha__dtbmw[i] = dict_arr_out[ewpcn__ikvd[i]]
    return sriha__dtbmw


@register_jitable
def str_contains_non_regex(arr, pat, case):
    ixx__uezr = arr._data
    wwa__abpx = len(ixx__uezr)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(wwa__abpx)
    if not case:
        akb__pzc = pat.upper()
    for i in range(wwa__abpx):
        if case:
            dict_arr_out[i] = pat in ixx__uezr[i]
        else:
            dict_arr_out[i] = akb__pzc in ixx__uezr[i].upper()
    ewpcn__ikvd = arr._indices
    zsmua__rbc = len(ewpcn__ikvd)
    sriha__dtbmw = bodo.libs.bool_arr_ext.alloc_bool_array(zsmua__rbc)
    for i in range(zsmua__rbc):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(sriha__dtbmw, i)
        else:
            sriha__dtbmw[i] = dict_arr_out[ewpcn__ikvd[i]]
    return sriha__dtbmw


def create_simple_str2str_methods(func_name, func_args):
    cprd__vvac = f"""def str_{func_name}({', '.join(func_args)}):
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
    kkr__qvy = {}
    exec(cprd__vvac, {'bodo': bodo, 'numba': numba, 'init_dict_arr':
        init_dict_arr}, kkr__qvy)
    return kkr__qvy[f'str_{func_name}']


def _register_simple_str2str_methods():
    prn__qocgo = {**dict.fromkeys(['capitalize', 'lower', 'swapcase',
        'title', 'upper'], ('arr',)), **dict.fromkeys(['lstrip', 'rstrip',
        'strip'], ('arr', 'to_strip')), **dict.fromkeys(['center', 'ljust',
        'rjust'], ('arr', 'width', 'fillchar')), **dict.fromkeys(['zfill'],
        ('arr', 'width'))}
    for func_name in prn__qocgo.keys():
        ncvns__krmp = create_simple_str2str_methods(func_name, prn__qocgo[
            func_name])
        ncvns__krmp = register_jitable(ncvns__krmp)
        globals()[f'str_{func_name}'] = ncvns__krmp


_register_simple_str2str_methods()


@register_jitable
def str_find(arr, sub, start, end):
    hde__ubvar = arr._data
    ewpcn__ikvd = arr._indices
    lach__mdhdu = len(hde__ubvar)
    zsmua__rbc = len(ewpcn__ikvd)
    xfwbg__tfa = bodo.libs.int_arr_ext.alloc_int_array(lach__mdhdu, np.int64)
    pkcur__sqa = bodo.libs.int_arr_ext.alloc_int_array(zsmua__rbc, np.int64)
    for i in range(lach__mdhdu):
        if bodo.libs.array_kernels.isna(hde__ubvar, i):
            bodo.libs.array_kernels.setna(xfwbg__tfa, i)
            continue
        xfwbg__tfa[i] = hde__ubvar[i].find(sub, start, end)
    for i in range(zsmua__rbc):
        if bodo.libs.array_kernels.isna(arr, i
            ) or bodo.libs.array_kernels.isna(xfwbg__tfa, ewpcn__ikvd[i]):
            bodo.libs.array_kernels.setna(pkcur__sqa, i)
        else:
            pkcur__sqa[i] = xfwbg__tfa[ewpcn__ikvd[i]]
    return pkcur__sqa


@register_jitable
def str_slice(arr, start, stop, step):
    hde__ubvar = arr._data
    lach__mdhdu = len(hde__ubvar)
    std__chfut = bodo.libs.str_arr_ext.pre_alloc_string_array(lach__mdhdu, -1)
    for i in range(lach__mdhdu):
        if bodo.libs.array_kernels.isna(hde__ubvar, i):
            bodo.libs.array_kernels.setna(std__chfut, i)
            continue
        std__chfut[i] = hde__ubvar[i][start:stop:step]
    return init_dict_arr(std__chfut, arr._indices.copy(), arr.
        _has_global_dictionary)


@register_jitable
def str_get(arr, i):
    hde__ubvar = arr._data
    ewpcn__ikvd = arr._indices
    lach__mdhdu = len(hde__ubvar)
    zsmua__rbc = len(ewpcn__ikvd)
    std__chfut = pre_alloc_string_array(lach__mdhdu, -1)
    sriha__dtbmw = pre_alloc_string_array(zsmua__rbc, -1)
    for gsj__tpc in range(lach__mdhdu):
        if bodo.libs.array_kernels.isna(hde__ubvar, gsj__tpc) or not -len(
            hde__ubvar[gsj__tpc]) <= i < len(hde__ubvar[gsj__tpc]):
            bodo.libs.array_kernels.setna(std__chfut, gsj__tpc)
            continue
        std__chfut[gsj__tpc] = hde__ubvar[gsj__tpc][i]
    for gsj__tpc in range(zsmua__rbc):
        if bodo.libs.array_kernels.isna(ewpcn__ikvd, gsj__tpc
            ) or bodo.libs.array_kernels.isna(std__chfut, ewpcn__ikvd[gsj__tpc]
            ):
            bodo.libs.array_kernels.setna(sriha__dtbmw, gsj__tpc)
            continue
        sriha__dtbmw[gsj__tpc] = std__chfut[ewpcn__ikvd[gsj__tpc]]
    return sriha__dtbmw


@register_jitable
def str_repeat_int(arr, repeats):
    hde__ubvar = arr._data
    lach__mdhdu = len(hde__ubvar)
    std__chfut = pre_alloc_string_array(lach__mdhdu, -1)
    for i in range(lach__mdhdu):
        if bodo.libs.array_kernels.isna(hde__ubvar, i):
            bodo.libs.array_kernels.setna(std__chfut, i)
            continue
        std__chfut[i] = hde__ubvar[i] * repeats
    return init_dict_arr(std__chfut, arr._indices.copy(), arr.
        _has_global_dictionary)
