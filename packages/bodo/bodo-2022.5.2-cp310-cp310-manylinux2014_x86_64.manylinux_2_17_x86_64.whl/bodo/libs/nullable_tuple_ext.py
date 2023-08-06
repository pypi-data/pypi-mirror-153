"""
Wrapper class for Tuples that supports tracking null entries.
This is primarily used for maintaining null information for
Series values used in df.apply
"""
import operator
import numba
from numba.core import cgutils, types
from numba.extending import box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_method, register_model


class NullableTupleType(types.IterableType):

    def __init__(self, tuple_typ, null_typ):
        self._tuple_typ = tuple_typ
        self._null_typ = null_typ
        super(NullableTupleType, self).__init__(name=
            f'NullableTupleType({tuple_typ}, {null_typ})')

    @property
    def tuple_typ(self):
        return self._tuple_typ

    @property
    def null_typ(self):
        return self._null_typ

    def __getitem__(self, i):
        return self._tuple_typ[i]

    @property
    def key(self):
        return self._tuple_typ

    @property
    def dtype(self):
        return self.tuple_typ.dtype

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    @property
    def iterator_type(self):
        return self.tuple_typ.iterator_type

    def __len__(self):
        return len(self.tuple_typ)


@register_model(NullableTupleType)
class NullableTupleModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        maskh__ofa = [('data', fe_type.tuple_typ), ('null_values', fe_type.
            null_typ)]
        super(NullableTupleModel, self).__init__(dmm, fe_type, maskh__ofa)


make_attribute_wrapper(NullableTupleType, 'data', '_data')
make_attribute_wrapper(NullableTupleType, 'null_values', '_null_values')


@intrinsic
def build_nullable_tuple(typingctx, data_tuple, null_values):
    assert isinstance(data_tuple, types.BaseTuple
        ), "build_nullable_tuple 'data_tuple' argument must be a tuple"
    assert isinstance(null_values, types.BaseTuple
        ), "build_nullable_tuple 'null_values' argument must be a tuple"
    data_tuple = types.unliteral(data_tuple)
    null_values = types.unliteral(null_values)

    def codegen(context, builder, signature, args):
        data_tuple, null_values = args
        mar__jqe = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        mar__jqe.data = data_tuple
        mar__jqe.null_values = null_values
        context.nrt.incref(builder, signature.args[0], data_tuple)
        context.nrt.incref(builder, signature.args[1], null_values)
        return mar__jqe._getvalue()
    sig = NullableTupleType(data_tuple, null_values)(data_tuple, null_values)
    return sig, codegen


@box(NullableTupleType)
def box_nullable_tuple(typ, val, c):
    mlkph__ulmw = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    c.context.nrt.incref(c.builder, typ.tuple_typ, mlkph__ulmw.data)
    c.context.nrt.incref(c.builder, typ.null_typ, mlkph__ulmw.null_values)
    jqn__fkt = c.pyapi.from_native_value(typ.tuple_typ, mlkph__ulmw.data, c
        .env_manager)
    jyjo__htq = c.pyapi.from_native_value(typ.null_typ, mlkph__ulmw.
        null_values, c.env_manager)
    csa__ccfo = c.context.get_constant(types.int64, len(typ.tuple_typ))
    bsj__xxxj = c.pyapi.list_new(csa__ccfo)
    with cgutils.for_range(c.builder, csa__ccfo) as ebeq__cowf:
        i = ebeq__cowf.index
        difk__ajmr = c.pyapi.long_from_longlong(i)
        rwto__rimry = c.pyapi.object_getitem(jyjo__htq, difk__ajmr)
        hynp__qoil = c.pyapi.to_native_value(types.bool_, rwto__rimry).value
        with c.builder.if_else(hynp__qoil) as (iktt__ywp, gaml__duri):
            with iktt__ywp:
                c.pyapi.list_setitem(bsj__xxxj, i, c.pyapi.make_none())
            with gaml__duri:
                qwfe__nsb = c.pyapi.object_getitem(jqn__fkt, difk__ajmr)
                c.pyapi.list_setitem(bsj__xxxj, i, qwfe__nsb)
        c.pyapi.decref(difk__ajmr)
        c.pyapi.decref(rwto__rimry)
    qjqsp__nyer = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    okctj__avhvd = c.pyapi.call_function_objargs(qjqsp__nyer, (bsj__xxxj,))
    c.pyapi.decref(jqn__fkt)
    c.pyapi.decref(jyjo__htq)
    c.pyapi.decref(qjqsp__nyer)
    c.pyapi.decref(bsj__xxxj)
    c.context.nrt.decref(c.builder, typ, val)
    return okctj__avhvd


@overload(operator.getitem)
def overload_getitem(A, idx):
    if not isinstance(A, NullableTupleType):
        return
    return lambda A, idx: A._data[idx]


@overload(len)
def overload_len(A):
    if not isinstance(A, NullableTupleType):
        return
    return lambda A: len(A._data)


@lower_builtin('getiter', NullableTupleType)
def nullable_tuple_getiter(context, builder, sig, args):
    mar__jqe = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    impl = context.get_function('getiter', sig.return_type(sig.args[0].
        tuple_typ))
    return impl(builder, (mar__jqe.data,))


@overload(operator.eq)
def nullable_tuple_eq(val1, val2):
    if not isinstance(val1, NullableTupleType) or not isinstance(val2,
        NullableTupleType):
        return
    if val1 != val2:
        return lambda val1, val2: False
    cuctw__qkp = 'def impl(val1, val2):\n'
    cuctw__qkp += '    data_tup1 = val1._data\n'
    cuctw__qkp += '    null_tup1 = val1._null_values\n'
    cuctw__qkp += '    data_tup2 = val2._data\n'
    cuctw__qkp += '    null_tup2 = val2._null_values\n'
    bqae__fin = val1._tuple_typ
    for i in range(len(bqae__fin)):
        cuctw__qkp += f'    null1_{i} = null_tup1[{i}]\n'
        cuctw__qkp += f'    null2_{i} = null_tup2[{i}]\n'
        cuctw__qkp += f'    data1_{i} = data_tup1[{i}]\n'
        cuctw__qkp += f'    data2_{i} = data_tup2[{i}]\n'
        cuctw__qkp += f'    if null1_{i} != null2_{i}:\n'
        cuctw__qkp += '        return False\n'
        cuctw__qkp += f'    if null1_{i} and (data1_{i} != data2_{i}):\n'
        cuctw__qkp += f'        return False\n'
    cuctw__qkp += f'    return True\n'
    iogj__hhznh = {}
    exec(cuctw__qkp, {}, iogj__hhznh)
    impl = iogj__hhznh['impl']
    return impl


@overload_method(NullableTupleType, '__hash__')
def nullable_tuple_hash(val):

    def impl(val):
        return _nullable_tuple_hash(val)
    return impl


_PyHASH_XXPRIME_1 = numba.cpython.hashing._PyHASH_XXPRIME_1
_PyHASH_XXPRIME_2 = numba.cpython.hashing._PyHASH_XXPRIME_1
_PyHASH_XXPRIME_5 = numba.cpython.hashing._PyHASH_XXPRIME_1


@numba.generated_jit(nopython=True)
def _nullable_tuple_hash(nullable_tup):
    cuctw__qkp = 'def impl(nullable_tup):\n'
    cuctw__qkp += '    data_tup = nullable_tup._data\n'
    cuctw__qkp += '    null_tup = nullable_tup._null_values\n'
    cuctw__qkp += '    tl = numba.cpython.hashing._Py_uhash_t(len(data_tup))\n'
    cuctw__qkp += '    acc = _PyHASH_XXPRIME_5\n'
    bqae__fin = nullable_tup._tuple_typ
    for i in range(len(bqae__fin)):
        cuctw__qkp += f'    null_val_{i} = null_tup[{i}]\n'
        cuctw__qkp += f'    null_lane_{i} = hash(null_val_{i})\n'
        cuctw__qkp += (
            f'    if null_lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n'
            )
        cuctw__qkp += '        return -1\n'
        cuctw__qkp += f'    acc += null_lane_{i} * _PyHASH_XXPRIME_2\n'
        cuctw__qkp += '    acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n'
        cuctw__qkp += '    acc *= _PyHASH_XXPRIME_1\n'
        cuctw__qkp += f'    if not null_val_{i}:\n'
        cuctw__qkp += f'        lane_{i} = hash(data_tup[{i}])\n'
        cuctw__qkp += (
            f'        if lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n')
        cuctw__qkp += f'            return -1\n'
        cuctw__qkp += f'        acc += lane_{i} * _PyHASH_XXPRIME_2\n'
        cuctw__qkp += (
            '        acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n')
        cuctw__qkp += '        acc *= _PyHASH_XXPRIME_1\n'
    cuctw__qkp += """    acc += tl ^ (_PyHASH_XXPRIME_5 ^ numba.cpython.hashing._Py_uhash_t(3527539))
"""
    cuctw__qkp += '    if acc == numba.cpython.hashing._Py_uhash_t(-1):\n'
    cuctw__qkp += (
        '        return numba.cpython.hashing.process_return(1546275796)\n')
    cuctw__qkp += '    return numba.cpython.hashing.process_return(acc)\n'
    iogj__hhznh = {}
    exec(cuctw__qkp, {'numba': numba, '_PyHASH_XXPRIME_1':
        _PyHASH_XXPRIME_1, '_PyHASH_XXPRIME_2': _PyHASH_XXPRIME_2,
        '_PyHASH_XXPRIME_5': _PyHASH_XXPRIME_5}, iogj__hhznh)
    impl = iogj__hhznh['impl']
    return impl
