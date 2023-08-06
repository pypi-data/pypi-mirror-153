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
        bofbf__horn = [('data', fe_type.tuple_typ), ('null_values', fe_type
            .null_typ)]
        super(NullableTupleModel, self).__init__(dmm, fe_type, bofbf__horn)


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
        leia__lpfj = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        leia__lpfj.data = data_tuple
        leia__lpfj.null_values = null_values
        context.nrt.incref(builder, signature.args[0], data_tuple)
        context.nrt.incref(builder, signature.args[1], null_values)
        return leia__lpfj._getvalue()
    sig = NullableTupleType(data_tuple, null_values)(data_tuple, null_values)
    return sig, codegen


@box(NullableTupleType)
def box_nullable_tuple(typ, val, c):
    jnxu__qqr = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    c.context.nrt.incref(c.builder, typ.tuple_typ, jnxu__qqr.data)
    c.context.nrt.incref(c.builder, typ.null_typ, jnxu__qqr.null_values)
    hlm__xue = c.pyapi.from_native_value(typ.tuple_typ, jnxu__qqr.data, c.
        env_manager)
    niht__dyhgf = c.pyapi.from_native_value(typ.null_typ, jnxu__qqr.
        null_values, c.env_manager)
    nvr__upnvv = c.context.get_constant(types.int64, len(typ.tuple_typ))
    utjm__ljsfg = c.pyapi.list_new(nvr__upnvv)
    with cgutils.for_range(c.builder, nvr__upnvv) as rtsmc__ktmy:
        i = rtsmc__ktmy.index
        hwi__pqjy = c.pyapi.long_from_longlong(i)
        yze__rbg = c.pyapi.object_getitem(niht__dyhgf, hwi__pqjy)
        gbl__zhzzz = c.pyapi.to_native_value(types.bool_, yze__rbg).value
        with c.builder.if_else(gbl__zhzzz) as (hrg__ykbmw, dwymc__pezbk):
            with hrg__ykbmw:
                c.pyapi.list_setitem(utjm__ljsfg, i, c.pyapi.make_none())
            with dwymc__pezbk:
                uqbxl__srx = c.pyapi.object_getitem(hlm__xue, hwi__pqjy)
                c.pyapi.list_setitem(utjm__ljsfg, i, uqbxl__srx)
        c.pyapi.decref(hwi__pqjy)
        c.pyapi.decref(yze__rbg)
    fsc__smch = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    tjg__kxm = c.pyapi.call_function_objargs(fsc__smch, (utjm__ljsfg,))
    c.pyapi.decref(hlm__xue)
    c.pyapi.decref(niht__dyhgf)
    c.pyapi.decref(fsc__smch)
    c.pyapi.decref(utjm__ljsfg)
    c.context.nrt.decref(c.builder, typ, val)
    return tjg__kxm


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
    leia__lpfj = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    impl = context.get_function('getiter', sig.return_type(sig.args[0].
        tuple_typ))
    return impl(builder, (leia__lpfj.data,))


@overload(operator.eq)
def nullable_tuple_eq(val1, val2):
    if not isinstance(val1, NullableTupleType) or not isinstance(val2,
        NullableTupleType):
        return
    if val1 != val2:
        return lambda val1, val2: False
    kaqqu__kop = 'def impl(val1, val2):\n'
    kaqqu__kop += '    data_tup1 = val1._data\n'
    kaqqu__kop += '    null_tup1 = val1._null_values\n'
    kaqqu__kop += '    data_tup2 = val2._data\n'
    kaqqu__kop += '    null_tup2 = val2._null_values\n'
    kdlr__nifww = val1._tuple_typ
    for i in range(len(kdlr__nifww)):
        kaqqu__kop += f'    null1_{i} = null_tup1[{i}]\n'
        kaqqu__kop += f'    null2_{i} = null_tup2[{i}]\n'
        kaqqu__kop += f'    data1_{i} = data_tup1[{i}]\n'
        kaqqu__kop += f'    data2_{i} = data_tup2[{i}]\n'
        kaqqu__kop += f'    if null1_{i} != null2_{i}:\n'
        kaqqu__kop += '        return False\n'
        kaqqu__kop += f'    if null1_{i} and (data1_{i} != data2_{i}):\n'
        kaqqu__kop += f'        return False\n'
    kaqqu__kop += f'    return True\n'
    rhdj__qqt = {}
    exec(kaqqu__kop, {}, rhdj__qqt)
    impl = rhdj__qqt['impl']
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
    kaqqu__kop = 'def impl(nullable_tup):\n'
    kaqqu__kop += '    data_tup = nullable_tup._data\n'
    kaqqu__kop += '    null_tup = nullable_tup._null_values\n'
    kaqqu__kop += '    tl = numba.cpython.hashing._Py_uhash_t(len(data_tup))\n'
    kaqqu__kop += '    acc = _PyHASH_XXPRIME_5\n'
    kdlr__nifww = nullable_tup._tuple_typ
    for i in range(len(kdlr__nifww)):
        kaqqu__kop += f'    null_val_{i} = null_tup[{i}]\n'
        kaqqu__kop += f'    null_lane_{i} = hash(null_val_{i})\n'
        kaqqu__kop += (
            f'    if null_lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n'
            )
        kaqqu__kop += '        return -1\n'
        kaqqu__kop += f'    acc += null_lane_{i} * _PyHASH_XXPRIME_2\n'
        kaqqu__kop += '    acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n'
        kaqqu__kop += '    acc *= _PyHASH_XXPRIME_1\n'
        kaqqu__kop += f'    if not null_val_{i}:\n'
        kaqqu__kop += f'        lane_{i} = hash(data_tup[{i}])\n'
        kaqqu__kop += (
            f'        if lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n')
        kaqqu__kop += f'            return -1\n'
        kaqqu__kop += f'        acc += lane_{i} * _PyHASH_XXPRIME_2\n'
        kaqqu__kop += (
            '        acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n')
        kaqqu__kop += '        acc *= _PyHASH_XXPRIME_1\n'
    kaqqu__kop += """    acc += tl ^ (_PyHASH_XXPRIME_5 ^ numba.cpython.hashing._Py_uhash_t(3527539))
"""
    kaqqu__kop += '    if acc == numba.cpython.hashing._Py_uhash_t(-1):\n'
    kaqqu__kop += (
        '        return numba.cpython.hashing.process_return(1546275796)\n')
    kaqqu__kop += '    return numba.cpython.hashing.process_return(acc)\n'
    rhdj__qqt = {}
    exec(kaqqu__kop, {'numba': numba, '_PyHASH_XXPRIME_1':
        _PyHASH_XXPRIME_1, '_PyHASH_XXPRIME_2': _PyHASH_XXPRIME_2,
        '_PyHASH_XXPRIME_5': _PyHASH_XXPRIME_5}, rhdj__qqt)
    impl = rhdj__qqt['impl']
    return impl
