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
        spakb__zlw = [('data', fe_type.data), ('indices',
            dict_indices_arr_type), ('has_global_dictionary', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, spakb__zlw)


make_attribute_wrapper(DictionaryArrayType, 'data', '_data')
make_attribute_wrapper(DictionaryArrayType, 'indices', '_indices')
make_attribute_wrapper(DictionaryArrayType, 'has_global_dictionary',
    '_has_global_dictionary')
lower_builtin('getiter', dict_str_arr_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_dict_arr(typingctx, data_t, indices_t, glob_dict_t=None):
    assert indices_t == dict_indices_arr_type, 'invalid indices type for dict array'

    def codegen(context, builder, signature, args):
        yem__oqe, cek__wgicl, yfey__pime = args
        rrkke__mzkt = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        rrkke__mzkt.data = yem__oqe
        rrkke__mzkt.indices = cek__wgicl
        rrkke__mzkt.has_global_dictionary = yfey__pime
        context.nrt.incref(builder, signature.args[0], yem__oqe)
        context.nrt.incref(builder, signature.args[1], cek__wgicl)
        return rrkke__mzkt._getvalue()
    ixn__eds = DictionaryArrayType(data_t)
    zbpc__vywam = ixn__eds(data_t, indices_t, types.bool_)
    return zbpc__vywam, codegen


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
        jotmu__zcnam = c.pyapi.unserialize(c.pyapi.serialize_object(
            to_pa_dict_arr))
        val = c.pyapi.call_function_objargs(jotmu__zcnam, [val])
        c.pyapi.decref(jotmu__zcnam)
    rrkke__mzkt = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    rqvaq__auz = c.pyapi.object_getattr_string(val, 'dictionary')
    vnomp__utrqn = c.pyapi.bool_from_bool(c.context.get_constant(types.
        bool_, False))
    wggxc__qhj = c.pyapi.call_method(rqvaq__auz, 'to_numpy', (vnomp__utrqn,))
    rrkke__mzkt.data = c.unbox(typ.data, wggxc__qhj).value
    jiayt__clgqs = c.pyapi.object_getattr_string(val, 'indices')
    mhdk__wxq = c.context.insert_const_string(c.builder.module, 'pandas')
    kke__uqawl = c.pyapi.import_module_noblock(mhdk__wxq)
    uzxo__tpxc = c.pyapi.string_from_constant_string('Int32')
    msdqy__sto = c.pyapi.call_method(kke__uqawl, 'array', (jiayt__clgqs,
        uzxo__tpxc))
    rrkke__mzkt.indices = c.unbox(dict_indices_arr_type, msdqy__sto).value
    rrkke__mzkt.has_global_dictionary = c.context.get_constant(types.bool_,
        False)
    c.pyapi.decref(rqvaq__auz)
    c.pyapi.decref(vnomp__utrqn)
    c.pyapi.decref(wggxc__qhj)
    c.pyapi.decref(jiayt__clgqs)
    c.pyapi.decref(kke__uqawl)
    c.pyapi.decref(uzxo__tpxc)
    c.pyapi.decref(msdqy__sto)
    if bodo.hiframes.boxing._use_dict_str_type:
        c.pyapi.decref(val)
    fyyc__dgej = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(rrkke__mzkt._getvalue(), is_error=fyyc__dgej)


@box(DictionaryArrayType)
def box_dict_arr(typ, val, c):
    rrkke__mzkt = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ == dict_str_arr_type:
        c.context.nrt.incref(c.builder, typ.data, rrkke__mzkt.data)
        atn__zysn = c.box(typ.data, rrkke__mzkt.data)
        ihap__yqek = cgutils.create_struct_proxy(dict_indices_arr_type)(c.
            context, c.builder, rrkke__mzkt.indices)
        fxzt__xdtfy = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), c.
            pyapi.pyobj, lir.IntType(32).as_pointer(), lir.IntType(8).
            as_pointer()])
        mnhfd__qtl = cgutils.get_or_insert_function(c.builder.module,
            fxzt__xdtfy, name='box_dict_str_array')
        wkqr__eea = cgutils.create_struct_proxy(types.Array(types.int32, 1,
            'C'))(c.context, c.builder, ihap__yqek.data)
        rqyg__tls = c.builder.extract_value(wkqr__eea.shape, 0)
        bqjfu__cpue = wkqr__eea.data
        szthi__enh = cgutils.create_struct_proxy(types.Array(types.int8, 1,
            'C'))(c.context, c.builder, ihap__yqek.null_bitmap).data
        wggxc__qhj = c.builder.call(mnhfd__qtl, [rqyg__tls, atn__zysn,
            bqjfu__cpue, szthi__enh])
        c.pyapi.decref(atn__zysn)
    else:
        mhdk__wxq = c.context.insert_const_string(c.builder.module, 'pyarrow')
        dgdl__dtpv = c.pyapi.import_module_noblock(mhdk__wxq)
        qvc__bug = c.pyapi.object_getattr_string(dgdl__dtpv, 'DictionaryArray')
        c.context.nrt.incref(c.builder, typ.data, rrkke__mzkt.data)
        atn__zysn = c.box(typ.data, rrkke__mzkt.data)
        c.context.nrt.incref(c.builder, dict_indices_arr_type, rrkke__mzkt.
            indices)
        jiayt__clgqs = c.box(dict_indices_arr_type, rrkke__mzkt.indices)
        gcbu__rykta = c.pyapi.call_method(qvc__bug, 'from_arrays', (
            jiayt__clgqs, atn__zysn))
        vnomp__utrqn = c.pyapi.bool_from_bool(c.context.get_constant(types.
            bool_, False))
        wggxc__qhj = c.pyapi.call_method(gcbu__rykta, 'to_numpy', (
            vnomp__utrqn,))
        c.pyapi.decref(dgdl__dtpv)
        c.pyapi.decref(atn__zysn)
        c.pyapi.decref(jiayt__clgqs)
        c.pyapi.decref(qvc__bug)
        c.pyapi.decref(gcbu__rykta)
        c.pyapi.decref(vnomp__utrqn)
    c.context.nrt.decref(c.builder, typ, val)
    return wggxc__qhj


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
    zmp__uxzn = pyval.dictionary.to_numpy(False)
    oukws__cpdvz = pd.array(pyval.indices, 'Int32')
    zmp__uxzn = context.get_constant_generic(builder, typ.data, zmp__uxzn)
    oukws__cpdvz = context.get_constant_generic(builder,
        dict_indices_arr_type, oukws__cpdvz)
    jmxzh__yjr = context.get_constant(types.bool_, False)
    yodh__twi = lir.Constant.literal_struct([zmp__uxzn, oukws__cpdvz,
        jmxzh__yjr])
    return yodh__twi


@overload(operator.getitem, no_unliteral=True)
def dict_arr_getitem(A, ind):
    if not isinstance(A, DictionaryArrayType):
        return
    if isinstance(ind, types.Integer):

        def dict_arr_getitem_impl(A, ind):
            if bodo.libs.array_kernels.isna(A._indices, ind):
                return ''
            hflr__migt = A._indices[ind]
            return A._data[hflr__migt]
        return dict_arr_getitem_impl
    return lambda A, ind: init_dict_arr(A._data, A._indices[ind], A.
        _has_global_dictionary)


@overload_method(DictionaryArrayType, '_decode', no_unliteral=True)
def overload_dict_arr_decode(A):

    def impl(A):
        yem__oqe = A._data
        cek__wgicl = A._indices
        rqyg__tls = len(cek__wgicl)
        wlmst__lis = [get_str_arr_item_length(yem__oqe, i) for i in range(
            len(yem__oqe))]
        vtsv__mernf = 0
        for i in range(rqyg__tls):
            if not bodo.libs.array_kernels.isna(cek__wgicl, i):
                vtsv__mernf += wlmst__lis[cek__wgicl[i]]
        tpq__swfqr = pre_alloc_string_array(rqyg__tls, vtsv__mernf)
        for i in range(rqyg__tls):
            if bodo.libs.array_kernels.isna(cek__wgicl, i):
                bodo.libs.array_kernels.setna(tpq__swfqr, i)
                continue
            ind = cek__wgicl[i]
            if bodo.libs.array_kernels.isna(yem__oqe, ind):
                bodo.libs.array_kernels.setna(tpq__swfqr, i)
                continue
            tpq__swfqr[i] = yem__oqe[ind]
        return tpq__swfqr
    return impl


@overload(operator.setitem)
def dict_arr_setitem(A, idx, val):
    if not isinstance(A, DictionaryArrayType):
        return
    raise_bodo_error(
        "DictionaryArrayType is read-only and doesn't support setitem yet")


@numba.njit(no_cpython_wrapper=True)
def find_dict_ind(arr, val):
    hflr__migt = -1
    yem__oqe = arr._data
    for i in range(len(yem__oqe)):
        if bodo.libs.array_kernels.isna(yem__oqe, i):
            continue
        if yem__oqe[i] == val:
            hflr__migt = i
            break
    return hflr__migt


@numba.njit(no_cpython_wrapper=True)
def dict_arr_eq(arr, val):
    rqyg__tls = len(arr)
    hflr__migt = find_dict_ind(arr, val)
    if hflr__migt == -1:
        return init_bool_array(np.full(rqyg__tls, False, np.bool_), arr.
            _indices._null_bitmap.copy())
    return arr._indices == hflr__migt


@numba.njit(no_cpython_wrapper=True)
def dict_arr_ne(arr, val):
    rqyg__tls = len(arr)
    hflr__migt = find_dict_ind(arr, val)
    if hflr__migt == -1:
        return init_bool_array(np.full(rqyg__tls, True, np.bool_), arr.
            _indices._null_bitmap.copy())
    return arr._indices != hflr__migt


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
        ppg__mbdcj = arr._data
        smq__dnpzp = bodo.libs.int_arr_ext.alloc_int_array(len(ppg__mbdcj),
            dtype)
        for fbzqc__zil in range(len(ppg__mbdcj)):
            if bodo.libs.array_kernels.isna(ppg__mbdcj, fbzqc__zil):
                bodo.libs.array_kernels.setna(smq__dnpzp, fbzqc__zil)
                continue
            smq__dnpzp[fbzqc__zil] = np.int64(ppg__mbdcj[fbzqc__zil])
        rqyg__tls = len(arr)
        cek__wgicl = arr._indices
        tpq__swfqr = bodo.libs.int_arr_ext.alloc_int_array(rqyg__tls, dtype)
        for i in range(rqyg__tls):
            if bodo.libs.array_kernels.isna(cek__wgicl, i):
                bodo.libs.array_kernels.setna(tpq__swfqr, i)
                continue
            tpq__swfqr[i] = smq__dnpzp[cek__wgicl[i]]
        return tpq__swfqr
    return impl


def cat_dict_str(arrs, sep):
    pass


@overload(cat_dict_str)
def cat_dict_str_overload(arrs, sep):
    lkql__qlvj = len(arrs)
    jta__zscl = 'def impl(arrs, sep):\n'
    jta__zscl += '  ind_map = {}\n'
    jta__zscl += '  out_strs = []\n'
    jta__zscl += '  n = len(arrs[0])\n'
    for i in range(lkql__qlvj):
        jta__zscl += f'  indices{i} = arrs[{i}]._indices\n'
    for i in range(lkql__qlvj):
        jta__zscl += f'  data{i} = arrs[{i}]._data\n'
    jta__zscl += (
        '  out_indices = bodo.libs.int_arr_ext.alloc_int_array(n, np.int32)\n')
    jta__zscl += '  for i in range(n):\n'
    henam__dwj = ' or '.join([f'bodo.libs.array_kernels.isna(arrs[{i}], i)' for
        i in range(lkql__qlvj)])
    jta__zscl += f'    if {henam__dwj}:\n'
    jta__zscl += '      bodo.libs.array_kernels.setna(out_indices, i)\n'
    jta__zscl += '      continue\n'
    for i in range(lkql__qlvj):
        jta__zscl += f'    ind{i} = indices{i}[i]\n'
    hdvot__jxq = '(' + ', '.join(f'ind{i}' for i in range(lkql__qlvj)) + ')'
    jta__zscl += f'    if {hdvot__jxq} not in ind_map:\n'
    jta__zscl += '      out_ind = len(out_strs)\n'
    jta__zscl += f'      ind_map[{hdvot__jxq}] = out_ind\n'
    hqfer__nxkx = "''" if is_overload_none(sep) else 'sep'
    glbo__pblp = ', '.join([f'data{i}[ind{i}]' for i in range(lkql__qlvj)])
    jta__zscl += f'      v = {hqfer__nxkx}.join([{glbo__pblp}])\n'
    jta__zscl += '      out_strs.append(v)\n'
    jta__zscl += '    else:\n'
    jta__zscl += f'      out_ind = ind_map[{hdvot__jxq}]\n'
    jta__zscl += '    out_indices[i] = out_ind\n'
    jta__zscl += (
        '  out_str_arr = bodo.libs.str_arr_ext.str_arr_from_sequence(out_strs)\n'
        )
    jta__zscl += (
        '  return bodo.libs.dict_arr_ext.init_dict_arr(out_str_arr, out_indices, False)\n'
        )
    olqo__epg = {}
    exec(jta__zscl, {'bodo': bodo, 'numba': numba, 'np': np}, olqo__epg)
    impl = olqo__epg['impl']
    return impl


@lower_cast(DictionaryArrayType, StringArrayType)
def cast_dict_str_arr_to_str_arr(context, builder, fromty, toty, val):
    if fromty != dict_str_arr_type:
        return
    iycoa__hmzrp = bodo.utils.typing.decode_if_dict_array_overload(fromty)
    zbpc__vywam = toty(fromty)
    npahp__ssj = context.compile_internal(builder, iycoa__hmzrp,
        zbpc__vywam, (val,))
    return impl_ret_new_ref(context, builder, toty, npahp__ssj)


@register_jitable
def str_replace(arr, pat, repl, flags, regex):
    zmp__uxzn = arr._data
    hxzx__yacsj = len(zmp__uxzn)
    cyj__arjr = pre_alloc_string_array(hxzx__yacsj, -1)
    if regex:
        sxsls__qgons = re.compile(pat, flags)
        for i in range(hxzx__yacsj):
            if bodo.libs.array_kernels.isna(zmp__uxzn, i):
                bodo.libs.array_kernels.setna(cyj__arjr, i)
                continue
            cyj__arjr[i] = sxsls__qgons.sub(repl=repl, string=zmp__uxzn[i])
    else:
        for i in range(hxzx__yacsj):
            if bodo.libs.array_kernels.isna(zmp__uxzn, i):
                bodo.libs.array_kernels.setna(cyj__arjr, i)
                continue
            cyj__arjr[i] = zmp__uxzn[i].replace(pat, repl)
    return init_dict_arr(cyj__arjr, arr._indices.copy(), arr.
        _has_global_dictionary)


@register_jitable
def str_startswith(arr, pat, na):
    rrkke__mzkt = arr._data
    wus__reqjg = len(rrkke__mzkt)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(wus__reqjg)
    for i in range(wus__reqjg):
        dict_arr_out[i] = rrkke__mzkt[i].startswith(pat)
    oukws__cpdvz = arr._indices
    zlpce__esni = len(oukws__cpdvz)
    tpq__swfqr = bodo.libs.bool_arr_ext.alloc_bool_array(zlpce__esni)
    for i in range(zlpce__esni):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(tpq__swfqr, i)
        else:
            tpq__swfqr[i] = dict_arr_out[oukws__cpdvz[i]]
    return tpq__swfqr


@register_jitable
def str_endswith(arr, pat, na):
    rrkke__mzkt = arr._data
    wus__reqjg = len(rrkke__mzkt)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(wus__reqjg)
    for i in range(wus__reqjg):
        dict_arr_out[i] = rrkke__mzkt[i].endswith(pat)
    oukws__cpdvz = arr._indices
    zlpce__esni = len(oukws__cpdvz)
    tpq__swfqr = bodo.libs.bool_arr_ext.alloc_bool_array(zlpce__esni)
    for i in range(zlpce__esni):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(tpq__swfqr, i)
        else:
            tpq__swfqr[i] = dict_arr_out[oukws__cpdvz[i]]
    return tpq__swfqr


@numba.njit
def str_series_contains_regex(arr, pat, case, flags, na, regex):
    rrkke__mzkt = arr._data
    oyh__lidbe = pd.Series(rrkke__mzkt)
    with numba.objmode(dict_arr_out=bodo.boolean_array):
        dict_arr_out = oyh__lidbe.array._str_contains(pat, case, flags, na,
            regex)
    oukws__cpdvz = arr._indices
    zlpce__esni = len(oukws__cpdvz)
    tpq__swfqr = bodo.libs.bool_arr_ext.alloc_bool_array(zlpce__esni)
    for i in range(zlpce__esni):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(tpq__swfqr, i)
        else:
            tpq__swfqr[i] = dict_arr_out[oukws__cpdvz[i]]
    return tpq__swfqr


@register_jitable
def str_contains_non_regex(arr, pat, case):
    rrkke__mzkt = arr._data
    wus__reqjg = len(rrkke__mzkt)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(wus__reqjg)
    if not case:
        hxj__nma = pat.upper()
    for i in range(wus__reqjg):
        if case:
            dict_arr_out[i] = pat in rrkke__mzkt[i]
        else:
            dict_arr_out[i] = hxj__nma in rrkke__mzkt[i].upper()
    oukws__cpdvz = arr._indices
    zlpce__esni = len(oukws__cpdvz)
    tpq__swfqr = bodo.libs.bool_arr_ext.alloc_bool_array(zlpce__esni)
    for i in range(zlpce__esni):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(tpq__swfqr, i)
        else:
            tpq__swfqr[i] = dict_arr_out[oukws__cpdvz[i]]
    return tpq__swfqr


def create_simple_str2str_methods(func_name, func_args):
    jta__zscl = f"""def str_{func_name}({', '.join(func_args)}):
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
    olqo__epg = {}
    exec(jta__zscl, {'bodo': bodo, 'numba': numba, 'init_dict_arr':
        init_dict_arr}, olqo__epg)
    return olqo__epg[f'str_{func_name}']


def _register_simple_str2str_methods():
    yamx__ycxb = {**dict.fromkeys(['capitalize', 'lower', 'swapcase',
        'title', 'upper'], ('arr',)), **dict.fromkeys(['lstrip', 'rstrip',
        'strip'], ('arr', 'to_strip')), **dict.fromkeys(['center', 'ljust',
        'rjust'], ('arr', 'width', 'fillchar')), **dict.fromkeys(['zfill'],
        ('arr', 'width'))}
    for func_name in yamx__ycxb.keys():
        ita__xpgz = create_simple_str2str_methods(func_name, yamx__ycxb[
            func_name])
        ita__xpgz = register_jitable(ita__xpgz)
        globals()[f'str_{func_name}'] = ita__xpgz


_register_simple_str2str_methods()


@register_jitable
def str_find(arr, sub, start, end):
    zmp__uxzn = arr._data
    oukws__cpdvz = arr._indices
    hxzx__yacsj = len(zmp__uxzn)
    zlpce__esni = len(oukws__cpdvz)
    zpq__udz = bodo.libs.int_arr_ext.alloc_int_array(hxzx__yacsj, np.int64)
    mwc__axi = bodo.libs.int_arr_ext.alloc_int_array(zlpce__esni, np.int64)
    for i in range(hxzx__yacsj):
        if bodo.libs.array_kernels.isna(zmp__uxzn, i):
            bodo.libs.array_kernels.setna(zpq__udz, i)
            continue
        zpq__udz[i] = zmp__uxzn[i].find(sub, start, end)
    for i in range(zlpce__esni):
        if bodo.libs.array_kernels.isna(arr, i
            ) or bodo.libs.array_kernels.isna(zpq__udz, oukws__cpdvz[i]):
            bodo.libs.array_kernels.setna(mwc__axi, i)
        else:
            mwc__axi[i] = zpq__udz[oukws__cpdvz[i]]
    return mwc__axi


@register_jitable
def str_slice(arr, start, stop, step):
    zmp__uxzn = arr._data
    hxzx__yacsj = len(zmp__uxzn)
    cyj__arjr = bodo.libs.str_arr_ext.pre_alloc_string_array(hxzx__yacsj, -1)
    for i in range(hxzx__yacsj):
        if bodo.libs.array_kernels.isna(zmp__uxzn, i):
            bodo.libs.array_kernels.setna(cyj__arjr, i)
            continue
        cyj__arjr[i] = zmp__uxzn[i][start:stop:step]
    return init_dict_arr(cyj__arjr, arr._indices.copy(), arr.
        _has_global_dictionary)


@register_jitable
def str_get(arr, i):
    zmp__uxzn = arr._data
    oukws__cpdvz = arr._indices
    hxzx__yacsj = len(zmp__uxzn)
    zlpce__esni = len(oukws__cpdvz)
    cyj__arjr = pre_alloc_string_array(hxzx__yacsj, -1)
    tpq__swfqr = pre_alloc_string_array(zlpce__esni, -1)
    for fbzqc__zil in range(hxzx__yacsj):
        if bodo.libs.array_kernels.isna(zmp__uxzn, fbzqc__zil) or not -len(
            zmp__uxzn[fbzqc__zil]) <= i < len(zmp__uxzn[fbzqc__zil]):
            bodo.libs.array_kernels.setna(cyj__arjr, fbzqc__zil)
            continue
        cyj__arjr[fbzqc__zil] = zmp__uxzn[fbzqc__zil][i]
    for fbzqc__zil in range(zlpce__esni):
        if bodo.libs.array_kernels.isna(oukws__cpdvz, fbzqc__zil
            ) or bodo.libs.array_kernels.isna(cyj__arjr, oukws__cpdvz[
            fbzqc__zil]):
            bodo.libs.array_kernels.setna(tpq__swfqr, fbzqc__zil)
            continue
        tpq__swfqr[fbzqc__zil] = cyj__arjr[oukws__cpdvz[fbzqc__zil]]
    return tpq__swfqr


@register_jitable
def str_repeat_int(arr, repeats):
    zmp__uxzn = arr._data
    hxzx__yacsj = len(zmp__uxzn)
    cyj__arjr = pre_alloc_string_array(hxzx__yacsj, -1)
    for i in range(hxzx__yacsj):
        if bodo.libs.array_kernels.isna(zmp__uxzn, i):
            bodo.libs.array_kernels.setna(cyj__arjr, i)
            continue
        cyj__arjr[i] = zmp__uxzn[i] * repeats
    return init_dict_arr(cyj__arjr, arr._indices.copy(), arr.
        _has_global_dictionary)
