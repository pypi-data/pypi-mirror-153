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
        wuo__yuokj = [('data', fe_type.tuple_typ), ('null_values', fe_type.
            null_typ)]
        super(NullableTupleModel, self).__init__(dmm, fe_type, wuo__yuokj)


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
        wlfkt__zjxo = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        wlfkt__zjxo.data = data_tuple
        wlfkt__zjxo.null_values = null_values
        context.nrt.incref(builder, signature.args[0], data_tuple)
        context.nrt.incref(builder, signature.args[1], null_values)
        return wlfkt__zjxo._getvalue()
    sig = NullableTupleType(data_tuple, null_values)(data_tuple, null_values)
    return sig, codegen


@box(NullableTupleType)
def box_nullable_tuple(typ, val, c):
    yiag__hzl = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    c.context.nrt.incref(c.builder, typ.tuple_typ, yiag__hzl.data)
    c.context.nrt.incref(c.builder, typ.null_typ, yiag__hzl.null_values)
    xqckp__jfg = c.pyapi.from_native_value(typ.tuple_typ, yiag__hzl.data, c
        .env_manager)
    niml__imy = c.pyapi.from_native_value(typ.null_typ, yiag__hzl.
        null_values, c.env_manager)
    xjx__yozn = c.context.get_constant(types.int64, len(typ.tuple_typ))
    zrd__thh = c.pyapi.list_new(xjx__yozn)
    with cgutils.for_range(c.builder, xjx__yozn) as tiobe__wwj:
        i = tiobe__wwj.index
        yihho__zkqy = c.pyapi.long_from_longlong(i)
        snf__tvn = c.pyapi.object_getitem(niml__imy, yihho__zkqy)
        ahkxe__dwpk = c.pyapi.to_native_value(types.bool_, snf__tvn).value
        with c.builder.if_else(ahkxe__dwpk) as (dlta__qvuf, ctbxg__fvauj):
            with dlta__qvuf:
                c.pyapi.list_setitem(zrd__thh, i, c.pyapi.make_none())
            with ctbxg__fvauj:
                evdul__wfr = c.pyapi.object_getitem(xqckp__jfg, yihho__zkqy)
                c.pyapi.list_setitem(zrd__thh, i, evdul__wfr)
        c.pyapi.decref(yihho__zkqy)
        c.pyapi.decref(snf__tvn)
    yfb__rbw = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    kusq__njuvt = c.pyapi.call_function_objargs(yfb__rbw, (zrd__thh,))
    c.pyapi.decref(xqckp__jfg)
    c.pyapi.decref(niml__imy)
    c.pyapi.decref(yfb__rbw)
    c.pyapi.decref(zrd__thh)
    c.context.nrt.decref(c.builder, typ, val)
    return kusq__njuvt


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
    wlfkt__zjxo = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    impl = context.get_function('getiter', sig.return_type(sig.args[0].
        tuple_typ))
    return impl(builder, (wlfkt__zjxo.data,))


@overload(operator.eq)
def nullable_tuple_eq(val1, val2):
    if not isinstance(val1, NullableTupleType) or not isinstance(val2,
        NullableTupleType):
        return
    if val1 != val2:
        return lambda val1, val2: False
    kqya__oevtb = 'def impl(val1, val2):\n'
    kqya__oevtb += '    data_tup1 = val1._data\n'
    kqya__oevtb += '    null_tup1 = val1._null_values\n'
    kqya__oevtb += '    data_tup2 = val2._data\n'
    kqya__oevtb += '    null_tup2 = val2._null_values\n'
    qeokk__tpgpb = val1._tuple_typ
    for i in range(len(qeokk__tpgpb)):
        kqya__oevtb += f'    null1_{i} = null_tup1[{i}]\n'
        kqya__oevtb += f'    null2_{i} = null_tup2[{i}]\n'
        kqya__oevtb += f'    data1_{i} = data_tup1[{i}]\n'
        kqya__oevtb += f'    data2_{i} = data_tup2[{i}]\n'
        kqya__oevtb += f'    if null1_{i} != null2_{i}:\n'
        kqya__oevtb += '        return False\n'
        kqya__oevtb += f'    if null1_{i} and (data1_{i} != data2_{i}):\n'
        kqya__oevtb += f'        return False\n'
    kqya__oevtb += f'    return True\n'
    mdlt__bgujq = {}
    exec(kqya__oevtb, {}, mdlt__bgujq)
    impl = mdlt__bgujq['impl']
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
    kqya__oevtb = 'def impl(nullable_tup):\n'
    kqya__oevtb += '    data_tup = nullable_tup._data\n'
    kqya__oevtb += '    null_tup = nullable_tup._null_values\n'
    kqya__oevtb += (
        '    tl = numba.cpython.hashing._Py_uhash_t(len(data_tup))\n')
    kqya__oevtb += '    acc = _PyHASH_XXPRIME_5\n'
    qeokk__tpgpb = nullable_tup._tuple_typ
    for i in range(len(qeokk__tpgpb)):
        kqya__oevtb += f'    null_val_{i} = null_tup[{i}]\n'
        kqya__oevtb += f'    null_lane_{i} = hash(null_val_{i})\n'
        kqya__oevtb += (
            f'    if null_lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n'
            )
        kqya__oevtb += '        return -1\n'
        kqya__oevtb += f'    acc += null_lane_{i} * _PyHASH_XXPRIME_2\n'
        kqya__oevtb += (
            '    acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n')
        kqya__oevtb += '    acc *= _PyHASH_XXPRIME_1\n'
        kqya__oevtb += f'    if not null_val_{i}:\n'
        kqya__oevtb += f'        lane_{i} = hash(data_tup[{i}])\n'
        kqya__oevtb += (
            f'        if lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n')
        kqya__oevtb += f'            return -1\n'
        kqya__oevtb += f'        acc += lane_{i} * _PyHASH_XXPRIME_2\n'
        kqya__oevtb += (
            '        acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n')
        kqya__oevtb += '        acc *= _PyHASH_XXPRIME_1\n'
    kqya__oevtb += """    acc += tl ^ (_PyHASH_XXPRIME_5 ^ numba.cpython.hashing._Py_uhash_t(3527539))
"""
    kqya__oevtb += '    if acc == numba.cpython.hashing._Py_uhash_t(-1):\n'
    kqya__oevtb += (
        '        return numba.cpython.hashing.process_return(1546275796)\n')
    kqya__oevtb += '    return numba.cpython.hashing.process_return(acc)\n'
    mdlt__bgujq = {}
    exec(kqya__oevtb, {'numba': numba, '_PyHASH_XXPRIME_1':
        _PyHASH_XXPRIME_1, '_PyHASH_XXPRIME_2': _PyHASH_XXPRIME_2,
        '_PyHASH_XXPRIME_5': _PyHASH_XXPRIME_5}, mdlt__bgujq)
    impl = mdlt__bgujq['impl']
    return impl
