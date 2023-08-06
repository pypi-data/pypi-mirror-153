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
        oly__ihyr = [('data', fe_type.tuple_typ), ('null_values', fe_type.
            null_typ)]
        super(NullableTupleModel, self).__init__(dmm, fe_type, oly__ihyr)


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
        srewi__gsxxk = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        srewi__gsxxk.data = data_tuple
        srewi__gsxxk.null_values = null_values
        context.nrt.incref(builder, signature.args[0], data_tuple)
        context.nrt.incref(builder, signature.args[1], null_values)
        return srewi__gsxxk._getvalue()
    sig = NullableTupleType(data_tuple, null_values)(data_tuple, null_values)
    return sig, codegen


@box(NullableTupleType)
def box_nullable_tuple(typ, val, c):
    pyng__tqflg = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    c.context.nrt.incref(c.builder, typ.tuple_typ, pyng__tqflg.data)
    c.context.nrt.incref(c.builder, typ.null_typ, pyng__tqflg.null_values)
    skqag__islod = c.pyapi.from_native_value(typ.tuple_typ, pyng__tqflg.
        data, c.env_manager)
    btjr__yajci = c.pyapi.from_native_value(typ.null_typ, pyng__tqflg.
        null_values, c.env_manager)
    kao__qxa = c.context.get_constant(types.int64, len(typ.tuple_typ))
    lqyd__psd = c.pyapi.list_new(kao__qxa)
    with cgutils.for_range(c.builder, kao__qxa) as oxz__rmef:
        i = oxz__rmef.index
        jfjl__qfvzt = c.pyapi.long_from_longlong(i)
        feei__srit = c.pyapi.object_getitem(btjr__yajci, jfjl__qfvzt)
        ecugn__dup = c.pyapi.to_native_value(types.bool_, feei__srit).value
        with c.builder.if_else(ecugn__dup) as (cnz__vmwgg, qjh__widbx):
            with cnz__vmwgg:
                c.pyapi.list_setitem(lqyd__psd, i, c.pyapi.make_none())
            with qjh__widbx:
                ajyuu__tpeu = c.pyapi.object_getitem(skqag__islod, jfjl__qfvzt)
                c.pyapi.list_setitem(lqyd__psd, i, ajyuu__tpeu)
        c.pyapi.decref(jfjl__qfvzt)
        c.pyapi.decref(feei__srit)
    bvwe__xkfva = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    pibz__nkpr = c.pyapi.call_function_objargs(bvwe__xkfva, (lqyd__psd,))
    c.pyapi.decref(skqag__islod)
    c.pyapi.decref(btjr__yajci)
    c.pyapi.decref(bvwe__xkfva)
    c.pyapi.decref(lqyd__psd)
    c.context.nrt.decref(c.builder, typ, val)
    return pibz__nkpr


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
    srewi__gsxxk = cgutils.create_struct_proxy(sig.args[0])(context,
        builder, value=args[0])
    impl = context.get_function('getiter', sig.return_type(sig.args[0].
        tuple_typ))
    return impl(builder, (srewi__gsxxk.data,))


@overload(operator.eq)
def nullable_tuple_eq(val1, val2):
    if not isinstance(val1, NullableTupleType) or not isinstance(val2,
        NullableTupleType):
        return
    if val1 != val2:
        return lambda val1, val2: False
    fjg__bfr = 'def impl(val1, val2):\n'
    fjg__bfr += '    data_tup1 = val1._data\n'
    fjg__bfr += '    null_tup1 = val1._null_values\n'
    fjg__bfr += '    data_tup2 = val2._data\n'
    fjg__bfr += '    null_tup2 = val2._null_values\n'
    jes__kytrj = val1._tuple_typ
    for i in range(len(jes__kytrj)):
        fjg__bfr += f'    null1_{i} = null_tup1[{i}]\n'
        fjg__bfr += f'    null2_{i} = null_tup2[{i}]\n'
        fjg__bfr += f'    data1_{i} = data_tup1[{i}]\n'
        fjg__bfr += f'    data2_{i} = data_tup2[{i}]\n'
        fjg__bfr += f'    if null1_{i} != null2_{i}:\n'
        fjg__bfr += '        return False\n'
        fjg__bfr += f'    if null1_{i} and (data1_{i} != data2_{i}):\n'
        fjg__bfr += f'        return False\n'
    fjg__bfr += f'    return True\n'
    rcqhq__vrhn = {}
    exec(fjg__bfr, {}, rcqhq__vrhn)
    impl = rcqhq__vrhn['impl']
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
    fjg__bfr = 'def impl(nullable_tup):\n'
    fjg__bfr += '    data_tup = nullable_tup._data\n'
    fjg__bfr += '    null_tup = nullable_tup._null_values\n'
    fjg__bfr += '    tl = numba.cpython.hashing._Py_uhash_t(len(data_tup))\n'
    fjg__bfr += '    acc = _PyHASH_XXPRIME_5\n'
    jes__kytrj = nullable_tup._tuple_typ
    for i in range(len(jes__kytrj)):
        fjg__bfr += f'    null_val_{i} = null_tup[{i}]\n'
        fjg__bfr += f'    null_lane_{i} = hash(null_val_{i})\n'
        fjg__bfr += (
            f'    if null_lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n'
            )
        fjg__bfr += '        return -1\n'
        fjg__bfr += f'    acc += null_lane_{i} * _PyHASH_XXPRIME_2\n'
        fjg__bfr += '    acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n'
        fjg__bfr += '    acc *= _PyHASH_XXPRIME_1\n'
        fjg__bfr += f'    if not null_val_{i}:\n'
        fjg__bfr += f'        lane_{i} = hash(data_tup[{i}])\n'
        fjg__bfr += (
            f'        if lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n')
        fjg__bfr += f'            return -1\n'
        fjg__bfr += f'        acc += lane_{i} * _PyHASH_XXPRIME_2\n'
        fjg__bfr += (
            '        acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n')
        fjg__bfr += '        acc *= _PyHASH_XXPRIME_1\n'
    fjg__bfr += """    acc += tl ^ (_PyHASH_XXPRIME_5 ^ numba.cpython.hashing._Py_uhash_t(3527539))
"""
    fjg__bfr += '    if acc == numba.cpython.hashing._Py_uhash_t(-1):\n'
    fjg__bfr += (
        '        return numba.cpython.hashing.process_return(1546275796)\n')
    fjg__bfr += '    return numba.cpython.hashing.process_return(acc)\n'
    rcqhq__vrhn = {}
    exec(fjg__bfr, {'numba': numba, '_PyHASH_XXPRIME_1': _PyHASH_XXPRIME_1,
        '_PyHASH_XXPRIME_2': _PyHASH_XXPRIME_2, '_PyHASH_XXPRIME_5':
        _PyHASH_XXPRIME_5}, rcqhq__vrhn)
    impl = rcqhq__vrhn['impl']
    return impl
