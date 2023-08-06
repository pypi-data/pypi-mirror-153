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
        vylap__btgd = [('data', fe_type.data), ('indices',
            dict_indices_arr_type), ('has_global_dictionary', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, vylap__btgd)


make_attribute_wrapper(DictionaryArrayType, 'data', '_data')
make_attribute_wrapper(DictionaryArrayType, 'indices', '_indices')
make_attribute_wrapper(DictionaryArrayType, 'has_global_dictionary',
    '_has_global_dictionary')
lower_builtin('getiter', dict_str_arr_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_dict_arr(typingctx, data_t, indices_t, glob_dict_t=None):
    assert indices_t == dict_indices_arr_type, 'invalid indices type for dict array'

    def codegen(context, builder, signature, args):
        gcy__vib, mfvff__vfgny, zkiqa__mbudg = args
        ctv__fxpta = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        ctv__fxpta.data = gcy__vib
        ctv__fxpta.indices = mfvff__vfgny
        ctv__fxpta.has_global_dictionary = zkiqa__mbudg
        context.nrt.incref(builder, signature.args[0], gcy__vib)
        context.nrt.incref(builder, signature.args[1], mfvff__vfgny)
        return ctv__fxpta._getvalue()
    rgcf__quc = DictionaryArrayType(data_t)
    infvd__hhxrs = rgcf__quc(data_t, indices_t, types.bool_)
    return infvd__hhxrs, codegen


@typeof_impl.register(pa.DictionaryArray)
def typeof_dict_value(val, c):
    if val.type.value_type == pa.string():
        return dict_str_arr_type


def to_pa_dict_arr(A):
    if isinstance(A, pa.DictionaryArray):
        return A
    for qcjcq__uph in range(len(A)):
        if pd.isna(A[qcjcq__uph]):
            A[qcjcq__uph] = None
    return pa.array(A).dictionary_encode()


@unbox(DictionaryArrayType)
def unbox_dict_arr(typ, val, c):
    if bodo.hiframes.boxing._use_dict_str_type:
        jos__dzjd = c.pyapi.unserialize(c.pyapi.serialize_object(
            to_pa_dict_arr))
        val = c.pyapi.call_function_objargs(jos__dzjd, [val])
        c.pyapi.decref(jos__dzjd)
    ctv__fxpta = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ekyb__fpokz = c.pyapi.object_getattr_string(val, 'dictionary')
    dpo__kjj = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_, 
        False))
    qlhiy__bgd = c.pyapi.call_method(ekyb__fpokz, 'to_numpy', (dpo__kjj,))
    ctv__fxpta.data = c.unbox(typ.data, qlhiy__bgd).value
    bvceh__gcorv = c.pyapi.object_getattr_string(val, 'indices')
    csvho__lil = c.context.insert_const_string(c.builder.module, 'pandas')
    xemme__oof = c.pyapi.import_module_noblock(csvho__lil)
    mafv__ivl = c.pyapi.string_from_constant_string('Int32')
    bnyu__hdsl = c.pyapi.call_method(xemme__oof, 'array', (bvceh__gcorv,
        mafv__ivl))
    ctv__fxpta.indices = c.unbox(dict_indices_arr_type, bnyu__hdsl).value
    ctv__fxpta.has_global_dictionary = c.context.get_constant(types.bool_, 
        False)
    c.pyapi.decref(ekyb__fpokz)
    c.pyapi.decref(dpo__kjj)
    c.pyapi.decref(qlhiy__bgd)
    c.pyapi.decref(bvceh__gcorv)
    c.pyapi.decref(xemme__oof)
    c.pyapi.decref(mafv__ivl)
    c.pyapi.decref(bnyu__hdsl)
    if bodo.hiframes.boxing._use_dict_str_type:
        c.pyapi.decref(val)
    vspd__iigo = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ctv__fxpta._getvalue(), is_error=vspd__iigo)


@box(DictionaryArrayType)
def box_dict_arr(typ, val, c):
    ctv__fxpta = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ == dict_str_arr_type:
        c.context.nrt.incref(c.builder, typ.data, ctv__fxpta.data)
        jrsrr__udax = c.box(typ.data, ctv__fxpta.data)
        afbp__neh = cgutils.create_struct_proxy(dict_indices_arr_type)(c.
            context, c.builder, ctv__fxpta.indices)
        xgznl__kgxzz = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), c.
            pyapi.pyobj, lir.IntType(32).as_pointer(), lir.IntType(8).
            as_pointer()])
        cftej__pbuk = cgutils.get_or_insert_function(c.builder.module,
            xgznl__kgxzz, name='box_dict_str_array')
        myscn__lekgj = cgutils.create_struct_proxy(types.Array(types.int32,
            1, 'C'))(c.context, c.builder, afbp__neh.data)
        udg__kdpl = c.builder.extract_value(myscn__lekgj.shape, 0)
        ahz__ntcl = myscn__lekgj.data
        mbho__qriz = cgutils.create_struct_proxy(types.Array(types.int8, 1,
            'C'))(c.context, c.builder, afbp__neh.null_bitmap).data
        qlhiy__bgd = c.builder.call(cftej__pbuk, [udg__kdpl, jrsrr__udax,
            ahz__ntcl, mbho__qriz])
        c.pyapi.decref(jrsrr__udax)
    else:
        csvho__lil = c.context.insert_const_string(c.builder.module, 'pyarrow')
        jnaz__vhe = c.pyapi.import_module_noblock(csvho__lil)
        zmtbs__bhwac = c.pyapi.object_getattr_string(jnaz__vhe,
            'DictionaryArray')
        c.context.nrt.incref(c.builder, typ.data, ctv__fxpta.data)
        jrsrr__udax = c.box(typ.data, ctv__fxpta.data)
        c.context.nrt.incref(c.builder, dict_indices_arr_type, ctv__fxpta.
            indices)
        bvceh__gcorv = c.box(dict_indices_arr_type, ctv__fxpta.indices)
        xbggv__njy = c.pyapi.call_method(zmtbs__bhwac, 'from_arrays', (
            bvceh__gcorv, jrsrr__udax))
        dpo__kjj = c.pyapi.bool_from_bool(c.context.get_constant(types.
            bool_, False))
        qlhiy__bgd = c.pyapi.call_method(xbggv__njy, 'to_numpy', (dpo__kjj,))
        c.pyapi.decref(jnaz__vhe)
        c.pyapi.decref(jrsrr__udax)
        c.pyapi.decref(bvceh__gcorv)
        c.pyapi.decref(zmtbs__bhwac)
        c.pyapi.decref(xbggv__njy)
        c.pyapi.decref(dpo__kjj)
    c.context.nrt.decref(c.builder, typ, val)
    return qlhiy__bgd


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
    wegap__bhyht = pyval.dictionary.to_numpy(False)
    rhs__marwb = pd.array(pyval.indices, 'Int32')
    wegap__bhyht = context.get_constant_generic(builder, typ.data, wegap__bhyht
        )
    rhs__marwb = context.get_constant_generic(builder,
        dict_indices_arr_type, rhs__marwb)
    ksmf__ttak = context.get_constant(types.bool_, False)
    ubuod__dmv = lir.Constant.literal_struct([wegap__bhyht, rhs__marwb,
        ksmf__ttak])
    return ubuod__dmv


@overload(operator.getitem, no_unliteral=True)
def dict_arr_getitem(A, ind):
    if not isinstance(A, DictionaryArrayType):
        return
    if isinstance(ind, types.Integer):

        def dict_arr_getitem_impl(A, ind):
            if bodo.libs.array_kernels.isna(A._indices, ind):
                return ''
            nlbvb__lnyw = A._indices[ind]
            return A._data[nlbvb__lnyw]
        return dict_arr_getitem_impl
    return lambda A, ind: init_dict_arr(A._data, A._indices[ind], A.
        _has_global_dictionary)


@overload_method(DictionaryArrayType, '_decode', no_unliteral=True)
def overload_dict_arr_decode(A):

    def impl(A):
        gcy__vib = A._data
        mfvff__vfgny = A._indices
        udg__kdpl = len(mfvff__vfgny)
        ytjvs__oysnf = [get_str_arr_item_length(gcy__vib, qcjcq__uph) for
            qcjcq__uph in range(len(gcy__vib))]
        yzsd__xutp = 0
        for qcjcq__uph in range(udg__kdpl):
            if not bodo.libs.array_kernels.isna(mfvff__vfgny, qcjcq__uph):
                yzsd__xutp += ytjvs__oysnf[mfvff__vfgny[qcjcq__uph]]
        lxomi__zhsmo = pre_alloc_string_array(udg__kdpl, yzsd__xutp)
        for qcjcq__uph in range(udg__kdpl):
            if bodo.libs.array_kernels.isna(mfvff__vfgny, qcjcq__uph):
                bodo.libs.array_kernels.setna(lxomi__zhsmo, qcjcq__uph)
                continue
            ind = mfvff__vfgny[qcjcq__uph]
            if bodo.libs.array_kernels.isna(gcy__vib, ind):
                bodo.libs.array_kernels.setna(lxomi__zhsmo, qcjcq__uph)
                continue
            lxomi__zhsmo[qcjcq__uph] = gcy__vib[ind]
        return lxomi__zhsmo
    return impl


@overload(operator.setitem)
def dict_arr_setitem(A, idx, val):
    if not isinstance(A, DictionaryArrayType):
        return
    raise_bodo_error(
        "DictionaryArrayType is read-only and doesn't support setitem yet")


@numba.njit(no_cpython_wrapper=True)
def find_dict_ind(arr, val):
    nlbvb__lnyw = -1
    gcy__vib = arr._data
    for qcjcq__uph in range(len(gcy__vib)):
        if bodo.libs.array_kernels.isna(gcy__vib, qcjcq__uph):
            continue
        if gcy__vib[qcjcq__uph] == val:
            nlbvb__lnyw = qcjcq__uph
            break
    return nlbvb__lnyw


@numba.njit(no_cpython_wrapper=True)
def dict_arr_eq(arr, val):
    udg__kdpl = len(arr)
    nlbvb__lnyw = find_dict_ind(arr, val)
    if nlbvb__lnyw == -1:
        return init_bool_array(np.full(udg__kdpl, False, np.bool_), arr.
            _indices._null_bitmap.copy())
    return arr._indices == nlbvb__lnyw


@numba.njit(no_cpython_wrapper=True)
def dict_arr_ne(arr, val):
    udg__kdpl = len(arr)
    nlbvb__lnyw = find_dict_ind(arr, val)
    if nlbvb__lnyw == -1:
        return init_bool_array(np.full(udg__kdpl, True, np.bool_), arr.
            _indices._null_bitmap.copy())
    return arr._indices != nlbvb__lnyw


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
        kpi__hzjm = arr._data
        caozr__syir = bodo.libs.int_arr_ext.alloc_int_array(len(kpi__hzjm),
            dtype)
        for ytzc__obi in range(len(kpi__hzjm)):
            if bodo.libs.array_kernels.isna(kpi__hzjm, ytzc__obi):
                bodo.libs.array_kernels.setna(caozr__syir, ytzc__obi)
                continue
            caozr__syir[ytzc__obi] = np.int64(kpi__hzjm[ytzc__obi])
        udg__kdpl = len(arr)
        mfvff__vfgny = arr._indices
        lxomi__zhsmo = bodo.libs.int_arr_ext.alloc_int_array(udg__kdpl, dtype)
        for qcjcq__uph in range(udg__kdpl):
            if bodo.libs.array_kernels.isna(mfvff__vfgny, qcjcq__uph):
                bodo.libs.array_kernels.setna(lxomi__zhsmo, qcjcq__uph)
                continue
            lxomi__zhsmo[qcjcq__uph] = caozr__syir[mfvff__vfgny[qcjcq__uph]]
        return lxomi__zhsmo
    return impl


def cat_dict_str(arrs, sep):
    pass


@overload(cat_dict_str)
def cat_dict_str_overload(arrs, sep):
    lgvq__upr = len(arrs)
    xzn__ihtjo = 'def impl(arrs, sep):\n'
    xzn__ihtjo += '  ind_map = {}\n'
    xzn__ihtjo += '  out_strs = []\n'
    xzn__ihtjo += '  n = len(arrs[0])\n'
    for qcjcq__uph in range(lgvq__upr):
        xzn__ihtjo += f'  indices{qcjcq__uph} = arrs[{qcjcq__uph}]._indices\n'
    for qcjcq__uph in range(lgvq__upr):
        xzn__ihtjo += f'  data{qcjcq__uph} = arrs[{qcjcq__uph}]._data\n'
    xzn__ihtjo += (
        '  out_indices = bodo.libs.int_arr_ext.alloc_int_array(n, np.int32)\n')
    xzn__ihtjo += '  for i in range(n):\n'
    rkoyu__fca = ' or '.join([
        f'bodo.libs.array_kernels.isna(arrs[{qcjcq__uph}], i)' for
        qcjcq__uph in range(lgvq__upr)])
    xzn__ihtjo += f'    if {rkoyu__fca}:\n'
    xzn__ihtjo += '      bodo.libs.array_kernels.setna(out_indices, i)\n'
    xzn__ihtjo += '      continue\n'
    for qcjcq__uph in range(lgvq__upr):
        xzn__ihtjo += f'    ind{qcjcq__uph} = indices{qcjcq__uph}[i]\n'
    dozc__hwzt = '(' + ', '.join(f'ind{qcjcq__uph}' for qcjcq__uph in range
        (lgvq__upr)) + ')'
    xzn__ihtjo += f'    if {dozc__hwzt} not in ind_map:\n'
    xzn__ihtjo += '      out_ind = len(out_strs)\n'
    xzn__ihtjo += f'      ind_map[{dozc__hwzt}] = out_ind\n'
    naa__kdp = "''" if is_overload_none(sep) else 'sep'
    dnkq__ngue = ', '.join([f'data{qcjcq__uph}[ind{qcjcq__uph}]' for
        qcjcq__uph in range(lgvq__upr)])
    xzn__ihtjo += f'      v = {naa__kdp}.join([{dnkq__ngue}])\n'
    xzn__ihtjo += '      out_strs.append(v)\n'
    xzn__ihtjo += '    else:\n'
    xzn__ihtjo += f'      out_ind = ind_map[{dozc__hwzt}]\n'
    xzn__ihtjo += '    out_indices[i] = out_ind\n'
    xzn__ihtjo += (
        '  out_str_arr = bodo.libs.str_arr_ext.str_arr_from_sequence(out_strs)\n'
        )
    xzn__ihtjo += """  return bodo.libs.dict_arr_ext.init_dict_arr(out_str_arr, out_indices, False)
"""
    agf__jlkbs = {}
    exec(xzn__ihtjo, {'bodo': bodo, 'numba': numba, 'np': np}, agf__jlkbs)
    impl = agf__jlkbs['impl']
    return impl


@lower_cast(DictionaryArrayType, StringArrayType)
def cast_dict_str_arr_to_str_arr(context, builder, fromty, toty, val):
    if fromty != dict_str_arr_type:
        return
    ewnhs__rbzx = bodo.utils.typing.decode_if_dict_array_overload(fromty)
    infvd__hhxrs = toty(fromty)
    zqko__mcjfy = context.compile_internal(builder, ewnhs__rbzx,
        infvd__hhxrs, (val,))
    return impl_ret_new_ref(context, builder, toty, zqko__mcjfy)


@register_jitable
def str_replace(arr, pat, repl, flags, regex):
    wegap__bhyht = arr._data
    iuj__cwu = len(wegap__bhyht)
    wiba__tqocb = pre_alloc_string_array(iuj__cwu, -1)
    if regex:
        dox__wtk = re.compile(pat, flags)
        for qcjcq__uph in range(iuj__cwu):
            if bodo.libs.array_kernels.isna(wegap__bhyht, qcjcq__uph):
                bodo.libs.array_kernels.setna(wiba__tqocb, qcjcq__uph)
                continue
            wiba__tqocb[qcjcq__uph] = dox__wtk.sub(repl=repl, string=
                wegap__bhyht[qcjcq__uph])
    else:
        for qcjcq__uph in range(iuj__cwu):
            if bodo.libs.array_kernels.isna(wegap__bhyht, qcjcq__uph):
                bodo.libs.array_kernels.setna(wiba__tqocb, qcjcq__uph)
                continue
            wiba__tqocb[qcjcq__uph] = wegap__bhyht[qcjcq__uph].replace(pat,
                repl)
    return init_dict_arr(wiba__tqocb, arr._indices.copy(), arr.
        _has_global_dictionary)


@register_jitable
def str_startswith(arr, pat, na):
    ctv__fxpta = arr._data
    vmn__hjn = len(ctv__fxpta)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(vmn__hjn)
    for qcjcq__uph in range(vmn__hjn):
        dict_arr_out[qcjcq__uph] = ctv__fxpta[qcjcq__uph].startswith(pat)
    rhs__marwb = arr._indices
    fkf__gzpy = len(rhs__marwb)
    lxomi__zhsmo = bodo.libs.bool_arr_ext.alloc_bool_array(fkf__gzpy)
    for qcjcq__uph in range(fkf__gzpy):
        if bodo.libs.array_kernels.isna(arr, qcjcq__uph):
            bodo.libs.array_kernels.setna(lxomi__zhsmo, qcjcq__uph)
        else:
            lxomi__zhsmo[qcjcq__uph] = dict_arr_out[rhs__marwb[qcjcq__uph]]
    return lxomi__zhsmo


@register_jitable
def str_endswith(arr, pat, na):
    ctv__fxpta = arr._data
    vmn__hjn = len(ctv__fxpta)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(vmn__hjn)
    for qcjcq__uph in range(vmn__hjn):
        dict_arr_out[qcjcq__uph] = ctv__fxpta[qcjcq__uph].endswith(pat)
    rhs__marwb = arr._indices
    fkf__gzpy = len(rhs__marwb)
    lxomi__zhsmo = bodo.libs.bool_arr_ext.alloc_bool_array(fkf__gzpy)
    for qcjcq__uph in range(fkf__gzpy):
        if bodo.libs.array_kernels.isna(arr, qcjcq__uph):
            bodo.libs.array_kernels.setna(lxomi__zhsmo, qcjcq__uph)
        else:
            lxomi__zhsmo[qcjcq__uph] = dict_arr_out[rhs__marwb[qcjcq__uph]]
    return lxomi__zhsmo


@numba.njit
def str_series_contains_regex(arr, pat, case, flags, na, regex):
    ctv__fxpta = arr._data
    nlqe__dsb = pd.Series(ctv__fxpta)
    with numba.objmode(dict_arr_out=bodo.boolean_array):
        dict_arr_out = nlqe__dsb.array._str_contains(pat, case, flags, na,
            regex)
    rhs__marwb = arr._indices
    fkf__gzpy = len(rhs__marwb)
    lxomi__zhsmo = bodo.libs.bool_arr_ext.alloc_bool_array(fkf__gzpy)
    for qcjcq__uph in range(fkf__gzpy):
        if bodo.libs.array_kernels.isna(arr, qcjcq__uph):
            bodo.libs.array_kernels.setna(lxomi__zhsmo, qcjcq__uph)
        else:
            lxomi__zhsmo[qcjcq__uph] = dict_arr_out[rhs__marwb[qcjcq__uph]]
    return lxomi__zhsmo


@register_jitable
def str_contains_non_regex(arr, pat, case):
    ctv__fxpta = arr._data
    vmn__hjn = len(ctv__fxpta)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(vmn__hjn)
    if not case:
        vim__ibif = pat.upper()
    for qcjcq__uph in range(vmn__hjn):
        if case:
            dict_arr_out[qcjcq__uph] = pat in ctv__fxpta[qcjcq__uph]
        else:
            dict_arr_out[qcjcq__uph] = vim__ibif in ctv__fxpta[qcjcq__uph
                ].upper()
    rhs__marwb = arr._indices
    fkf__gzpy = len(rhs__marwb)
    lxomi__zhsmo = bodo.libs.bool_arr_ext.alloc_bool_array(fkf__gzpy)
    for qcjcq__uph in range(fkf__gzpy):
        if bodo.libs.array_kernels.isna(arr, qcjcq__uph):
            bodo.libs.array_kernels.setna(lxomi__zhsmo, qcjcq__uph)
        else:
            lxomi__zhsmo[qcjcq__uph] = dict_arr_out[rhs__marwb[qcjcq__uph]]
    return lxomi__zhsmo


def create_simple_str2str_methods(func_name):
    xzn__ihtjo = f"""def str_{func_name}(arr):
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
    agf__jlkbs = {}
    exec(xzn__ihtjo, {'bodo': bodo, 'numba': numba, 'init_dict_arr':
        init_dict_arr}, agf__jlkbs)
    return agf__jlkbs[f'str_{func_name}']


def _register_simple_str2str_methods():
    marz__fnxg = ['capitalize', 'lower', 'swapcase', 'title', 'upper']
    for ewnhs__rbzx in marz__fnxg:
        qcygc__jti = create_simple_str2str_methods(ewnhs__rbzx)
        qcygc__jti = register_jitable(qcygc__jti)
        globals()[f'str_{ewnhs__rbzx}'] = qcygc__jti


_register_simple_str2str_methods()


@register_jitable
def str_center(arr, width, fillchar):
    wegap__bhyht = arr._data
    iuj__cwu = len(wegap__bhyht)
    wiba__tqocb = pre_alloc_string_array(iuj__cwu, -1)
    for qcjcq__uph in range(iuj__cwu):
        if bodo.libs.array_kernels.isna(wegap__bhyht, qcjcq__uph):
            wiba__tqocb[qcjcq__uph] = ''
            bodo.libs.array_kernels.setna(wiba__tqocb, qcjcq__uph)
            continue
        wiba__tqocb[qcjcq__uph] = wegap__bhyht[qcjcq__uph].center(width,
            fillchar)
    return init_dict_arr(wiba__tqocb, arr._indices.copy(), arr.
        _has_global_dictionary)
