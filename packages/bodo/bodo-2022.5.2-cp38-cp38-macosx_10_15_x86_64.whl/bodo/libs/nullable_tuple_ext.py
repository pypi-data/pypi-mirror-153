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
        xrgxc__rdygq = [('data', fe_type.tuple_typ), ('null_values',
            fe_type.null_typ)]
        super(NullableTupleModel, self).__init__(dmm, fe_type, xrgxc__rdygq)


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
        ymo__jiq = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        ymo__jiq.data = data_tuple
        ymo__jiq.null_values = null_values
        context.nrt.incref(builder, signature.args[0], data_tuple)
        context.nrt.incref(builder, signature.args[1], null_values)
        return ymo__jiq._getvalue()
    sig = NullableTupleType(data_tuple, null_values)(data_tuple, null_values)
    return sig, codegen


@box(NullableTupleType)
def box_nullable_tuple(typ, val, c):
    nzgf__khc = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    c.context.nrt.incref(c.builder, typ.tuple_typ, nzgf__khc.data)
    c.context.nrt.incref(c.builder, typ.null_typ, nzgf__khc.null_values)
    tglz__lymt = c.pyapi.from_native_value(typ.tuple_typ, nzgf__khc.data, c
        .env_manager)
    dxnj__haxxw = c.pyapi.from_native_value(typ.null_typ, nzgf__khc.
        null_values, c.env_manager)
    pwsey__abqfs = c.context.get_constant(types.int64, len(typ.tuple_typ))
    plcr__eimc = c.pyapi.list_new(pwsey__abqfs)
    with cgutils.for_range(c.builder, pwsey__abqfs) as rrzuq__ttdvi:
        i = rrzuq__ttdvi.index
        fshd__lcqq = c.pyapi.long_from_longlong(i)
        ymg__abgq = c.pyapi.object_getitem(dxnj__haxxw, fshd__lcqq)
        dss__bvi = c.pyapi.to_native_value(types.bool_, ymg__abgq).value
        with c.builder.if_else(dss__bvi) as (eiq__nbsyd, qme__wpxs):
            with eiq__nbsyd:
                c.pyapi.list_setitem(plcr__eimc, i, c.pyapi.make_none())
            with qme__wpxs:
                cgyg__ghqu = c.pyapi.object_getitem(tglz__lymt, fshd__lcqq)
                c.pyapi.list_setitem(plcr__eimc, i, cgyg__ghqu)
        c.pyapi.decref(fshd__lcqq)
        c.pyapi.decref(ymg__abgq)
    svjre__yyw = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    opemr__udl = c.pyapi.call_function_objargs(svjre__yyw, (plcr__eimc,))
    c.pyapi.decref(tglz__lymt)
    c.pyapi.decref(dxnj__haxxw)
    c.pyapi.decref(svjre__yyw)
    c.pyapi.decref(plcr__eimc)
    c.context.nrt.decref(c.builder, typ, val)
    return opemr__udl


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
    ymo__jiq = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    impl = context.get_function('getiter', sig.return_type(sig.args[0].
        tuple_typ))
    return impl(builder, (ymo__jiq.data,))


@overload(operator.eq)
def nullable_tuple_eq(val1, val2):
    if not isinstance(val1, NullableTupleType) or not isinstance(val2,
        NullableTupleType):
        return
    if val1 != val2:
        return lambda val1, val2: False
    bsrrk__rrd = 'def impl(val1, val2):\n'
    bsrrk__rrd += '    data_tup1 = val1._data\n'
    bsrrk__rrd += '    null_tup1 = val1._null_values\n'
    bsrrk__rrd += '    data_tup2 = val2._data\n'
    bsrrk__rrd += '    null_tup2 = val2._null_values\n'
    pug__elfqi = val1._tuple_typ
    for i in range(len(pug__elfqi)):
        bsrrk__rrd += f'    null1_{i} = null_tup1[{i}]\n'
        bsrrk__rrd += f'    null2_{i} = null_tup2[{i}]\n'
        bsrrk__rrd += f'    data1_{i} = data_tup1[{i}]\n'
        bsrrk__rrd += f'    data2_{i} = data_tup2[{i}]\n'
        bsrrk__rrd += f'    if null1_{i} != null2_{i}:\n'
        bsrrk__rrd += '        return False\n'
        bsrrk__rrd += f'    if null1_{i} and (data1_{i} != data2_{i}):\n'
        bsrrk__rrd += f'        return False\n'
    bsrrk__rrd += f'    return True\n'
    kkml__xda = {}
    exec(bsrrk__rrd, {}, kkml__xda)
    impl = kkml__xda['impl']
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
    bsrrk__rrd = 'def impl(nullable_tup):\n'
    bsrrk__rrd += '    data_tup = nullable_tup._data\n'
    bsrrk__rrd += '    null_tup = nullable_tup._null_values\n'
    bsrrk__rrd += '    tl = numba.cpython.hashing._Py_uhash_t(len(data_tup))\n'
    bsrrk__rrd += '    acc = _PyHASH_XXPRIME_5\n'
    pug__elfqi = nullable_tup._tuple_typ
    for i in range(len(pug__elfqi)):
        bsrrk__rrd += f'    null_val_{i} = null_tup[{i}]\n'
        bsrrk__rrd += f'    null_lane_{i} = hash(null_val_{i})\n'
        bsrrk__rrd += (
            f'    if null_lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n'
            )
        bsrrk__rrd += '        return -1\n'
        bsrrk__rrd += f'    acc += null_lane_{i} * _PyHASH_XXPRIME_2\n'
        bsrrk__rrd += '    acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n'
        bsrrk__rrd += '    acc *= _PyHASH_XXPRIME_1\n'
        bsrrk__rrd += f'    if not null_val_{i}:\n'
        bsrrk__rrd += f'        lane_{i} = hash(data_tup[{i}])\n'
        bsrrk__rrd += (
            f'        if lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n')
        bsrrk__rrd += f'            return -1\n'
        bsrrk__rrd += f'        acc += lane_{i} * _PyHASH_XXPRIME_2\n'
        bsrrk__rrd += (
            '        acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n')
        bsrrk__rrd += '        acc *= _PyHASH_XXPRIME_1\n'
    bsrrk__rrd += """    acc += tl ^ (_PyHASH_XXPRIME_5 ^ numba.cpython.hashing._Py_uhash_t(3527539))
"""
    bsrrk__rrd += '    if acc == numba.cpython.hashing._Py_uhash_t(-1):\n'
    bsrrk__rrd += (
        '        return numba.cpython.hashing.process_return(1546275796)\n')
    bsrrk__rrd += '    return numba.cpython.hashing.process_return(acc)\n'
    kkml__xda = {}
    exec(bsrrk__rrd, {'numba': numba, '_PyHASH_XXPRIME_1':
        _PyHASH_XXPRIME_1, '_PyHASH_XXPRIME_2': _PyHASH_XXPRIME_2,
        '_PyHASH_XXPRIME_5': _PyHASH_XXPRIME_5}, kkml__xda)
    impl = kkml__xda['impl']
    return impl
