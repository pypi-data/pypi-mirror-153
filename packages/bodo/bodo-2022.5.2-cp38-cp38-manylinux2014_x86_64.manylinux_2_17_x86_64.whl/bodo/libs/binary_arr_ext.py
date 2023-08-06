"""Array implementation for binary (bytes) objects, which are usually immutable.
It is equivalent to string array, except that it stores a 'bytes' object for each
element instead of 'str'.
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.extending import intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, overload, overload_attribute, overload_method
import bodo
from bodo.libs import hstr_ext
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.utils.typing import BodoError, is_list_like_index_type
_bytes_fromhex = types.ExternalFunction('bytes_fromhex', types.int64(types.
    voidptr, types.voidptr, types.uint64))
ll.add_symbol('bytes_to_hex', hstr_ext.bytes_to_hex)
ll.add_symbol('bytes_fromhex', hstr_ext.bytes_fromhex)
bytes_type = types.Bytes(types.uint8, 1, 'C', readonly=True)


class BinaryArrayType(types.IterableType, types.ArrayCompatible):

    def __init__(self):
        super(BinaryArrayType, self).__init__(name='BinaryArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return bytes_type

    def copy(self):
        return BinaryArrayType()

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self)


binary_array_type = BinaryArrayType()


@overload(len, no_unliteral=True)
def bin_arr_len_overload(bin_arr):
    if bin_arr == binary_array_type:
        return lambda bin_arr: len(bin_arr._data)


@overload_attribute(BinaryArrayType, 'size')
def bin_arr_size_overload(bin_arr):
    return lambda bin_arr: len(bin_arr._data)


@overload_attribute(BinaryArrayType, 'shape')
def bin_arr_shape_overload(bin_arr):
    return lambda bin_arr: (len(bin_arr._data),)


@overload_attribute(BinaryArrayType, 'nbytes')
def bin_arr_nbytes_overload(bin_arr):
    return lambda bin_arr: bin_arr._data.nbytes


@overload_attribute(BinaryArrayType, 'ndim')
def overload_bin_arr_ndim(A):
    return lambda A: 1


@overload_attribute(BinaryArrayType, 'dtype')
def overload_bool_arr_dtype(A):
    return lambda A: np.dtype('O')


@numba.njit
def pre_alloc_binary_array(n_bytestrs, n_chars):
    if n_chars is None:
        n_chars = -1
    bin_arr = init_binary_arr(bodo.libs.array_item_arr_ext.
        pre_alloc_array_item_array(np.int64(n_bytestrs), (np.int64(n_chars)
        ,), bodo.libs.str_arr_ext.char_arr_type))
    if n_chars == 0:
        bodo.libs.str_arr_ext.set_all_offsets_to_0(bin_arr)
    return bin_arr


@intrinsic
def init_binary_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType
        ) and data_typ.dtype == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, sig, args):
        qnvy__gzz, = args
        upqc__iyayo = context.make_helper(builder, binary_array_type)
        upqc__iyayo.data = qnvy__gzz
        context.nrt.incref(builder, data_typ, qnvy__gzz)
        return upqc__iyayo._getvalue()
    return binary_array_type(data_typ), codegen


@intrinsic
def init_bytes_type(typingctx, data_typ, length_type):
    assert data_typ == types.Array(types.uint8, 1, 'C')
    assert length_type == types.int64

    def codegen(context, builder, sig, args):
        kgnd__odtu = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        kqhoo__vhsj = args[1]
        kppqp__taz = cgutils.create_struct_proxy(bytes_type)(context, builder)
        kppqp__taz.meminfo = context.nrt.meminfo_alloc(builder, kqhoo__vhsj)
        kppqp__taz.nitems = kqhoo__vhsj
        kppqp__taz.itemsize = lir.Constant(kppqp__taz.itemsize.type, 1)
        kppqp__taz.data = context.nrt.meminfo_data(builder, kppqp__taz.meminfo)
        kppqp__taz.parent = cgutils.get_null_value(kppqp__taz.parent.type)
        kppqp__taz.shape = cgutils.pack_array(builder, [kqhoo__vhsj],
            context.get_value_type(types.intp))
        kppqp__taz.strides = kgnd__odtu.strides
        cgutils.memcpy(builder, kppqp__taz.data, kgnd__odtu.data, kqhoo__vhsj)
        return kppqp__taz._getvalue()
    return bytes_type(data_typ, length_type), codegen


@intrinsic
def cast_bytes_uint8array(typingctx, data_typ):
    assert data_typ == bytes_type

    def codegen(context, builder, sig, args):
        return impl_ret_borrowed(context, builder, sig.return_type, args[0])
    return types.Array(types.uint8, 1, 'C')(data_typ), codegen


@overload_method(BinaryArrayType, 'copy', no_unliteral=True)
def binary_arr_copy_overload(arr):

    def copy_impl(arr):
        return init_binary_arr(arr._data.copy())
    return copy_impl


@overload_method(types.Bytes, 'hex')
def binary_arr_hex(arr):
    bni__sak = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

    def impl(arr):
        kqhoo__vhsj = len(arr) * 2
        output = numba.cpython.unicode._empty_string(bni__sak, kqhoo__vhsj, 1)
        bytes_to_hex(output, arr)
        return output
    return impl


@lower_cast(types.CPointer(types.uint8), types.voidptr)
def cast_uint8_array_to_voidptr(context, builder, fromty, toty, val):
    return val


make_attribute_wrapper(types.Bytes, 'data', '_data')


@overload_method(types.Bytes, '__hash__')
def bytes_hash(arr):

    def impl(arr):
        return numba.cpython.hashing._Py_HashBytes(arr._data, len(arr))
    return impl


@intrinsic
def bytes_to_hex(typingctx, output, arr):

    def codegen(context, builder, sig, args):
        thd__rgmp = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        eeu__oypbd = cgutils.create_struct_proxy(sig.args[1])(context,
            builder, value=args[1])
        yix__ofvuw = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(64)])
        yukmp__hwmca = cgutils.get_or_insert_function(builder.module,
            yix__ofvuw, name='bytes_to_hex')
        builder.call(yukmp__hwmca, (thd__rgmp.data, eeu__oypbd.data,
            eeu__oypbd.nitems))
    return types.void(output, arr), codegen


@overload(operator.getitem, no_unliteral=True)
def binary_arr_getitem(arr, ind):
    if arr != binary_array_type:
        return
    if isinstance(ind, types.Integer):

        def impl(arr, ind):
            skss__tbkq = arr._data[ind]
            return init_bytes_type(skss__tbkq, len(skss__tbkq))
        return impl
    if is_list_like_index_type(ind) and (ind.dtype == types.bool_ or
        isinstance(ind.dtype, types.Integer)) or isinstance(ind, types.
        SliceType):
        return lambda arr, ind: init_binary_arr(arr._data[ind])
    raise BodoError(
        f'getitem for Binary Array with indexing type {ind} not supported.')


def bytes_fromhex(hex_str):
    pass


@overload(bytes_fromhex)
def overload_bytes_fromhex(hex_str):
    hex_str = types.unliteral(hex_str)
    if hex_str == bodo.string_type:
        bni__sak = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(hex_str):
            if not hex_str._is_ascii or hex_str._kind != bni__sak:
                raise TypeError(
                    'bytes.fromhex is only supported on ascii strings')
            qnvy__gzz = np.empty(len(hex_str) // 2, np.uint8)
            kqhoo__vhsj = _bytes_fromhex(qnvy__gzz.ctypes, hex_str._data,
                len(hex_str))
            jywda__jcbqw = init_bytes_type(qnvy__gzz, kqhoo__vhsj)
            return jywda__jcbqw
        return impl
    raise BodoError(f'bytes.fromhex not supported with argument type {hex_str}'
        )


@overload(operator.setitem)
def binary_arr_setitem(arr, ind, val):
    if arr != binary_array_type:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    if val != bytes_type:
        raise BodoError(
            f'setitem for Binary Array only supported with bytes value and integer indexing'
            )
    if isinstance(ind, types.Integer):

        def impl(arr, ind, val):
            arr._data[ind] = bodo.libs.binary_arr_ext.cast_bytes_uint8array(val
                )
        return impl
    raise BodoError(
        f'setitem for Binary Array with indexing type {ind} not supported.')


def create_binary_cmp_op_overload(op):

    def overload_binary_cmp(lhs, rhs):
        kwfri__woug = lhs == binary_array_type
        pslgq__mav = rhs == binary_array_type
        aenb__zfrn = 'lhs' if kwfri__woug else 'rhs'
        lvyw__zjz = 'def impl(lhs, rhs):\n'
        lvyw__zjz += '  numba.parfors.parfor.init_prange()\n'
        lvyw__zjz += f'  n = len({aenb__zfrn})\n'
        lvyw__zjz += '  out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(n)\n'
        lvyw__zjz += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        uwdu__evb = []
        if kwfri__woug:
            uwdu__evb.append('bodo.libs.array_kernels.isna(lhs, i)')
        if pslgq__mav:
            uwdu__evb.append('bodo.libs.array_kernels.isna(rhs, i)')
        lvyw__zjz += f"    if {' or '.join(uwdu__evb)}:\n"
        lvyw__zjz += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
        lvyw__zjz += '      continue\n'
        tdhmn__ltjs = 'lhs[i]' if kwfri__woug else 'lhs'
        jwgx__ezcn = 'rhs[i]' if pslgq__mav else 'rhs'
        lvyw__zjz += f'    out_arr[i] = op({tdhmn__ltjs}, {jwgx__ezcn})\n'
        lvyw__zjz += '  return out_arr\n'
        fixlc__bay = {}
        exec(lvyw__zjz, {'bodo': bodo, 'numba': numba, 'op': op}, fixlc__bay)
        return fixlc__bay['impl']
    return overload_binary_cmp


lower_builtin('getiter', binary_array_type)(numba.np.arrayobj.getiter_array)


def pre_alloc_binary_arr_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


from numba.parfors.array_analysis import ArrayAnalysis
(ArrayAnalysis._analyze_op_call_bodo_libs_binary_arr_ext_pre_alloc_binary_array
    ) = pre_alloc_binary_arr_equiv
