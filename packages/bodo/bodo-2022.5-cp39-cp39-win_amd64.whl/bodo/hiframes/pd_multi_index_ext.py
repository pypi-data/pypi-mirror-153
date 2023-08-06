"""Support for MultiIndex type of Pandas
"""
import operator
import numba
import pandas as pd
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, register_model, typeof_impl, unbox
from bodo.utils.conversion import ensure_contig_if_np
from bodo.utils.typing import BodoError, check_unsupported_args, dtype_to_array_type, get_val_type_maybe_str_literal, is_overload_none


class MultiIndexType(types.ArrayCompatible):

    def __init__(self, array_types, names_typ=None, name_typ=None):
        names_typ = (types.none,) * len(array_types
            ) if names_typ is None else names_typ
        name_typ = types.none if name_typ is None else name_typ
        self.array_types = array_types
        self.names_typ = names_typ
        self.name_typ = name_typ
        super(MultiIndexType, self).__init__(name=
            'MultiIndexType({}, {}, {})'.format(array_types, names_typ,
            name_typ))
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return MultiIndexType(self.array_types, self.names_typ, self.name_typ)

    @property
    def nlevels(self):
        return len(self.array_types)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(MultiIndexType)
class MultiIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        vsj__hpz = [('data', types.Tuple(fe_type.array_types)), ('names',
            types.Tuple(fe_type.names_typ)), ('name', fe_type.name_typ)]
        super(MultiIndexModel, self).__init__(dmm, fe_type, vsj__hpz)


make_attribute_wrapper(MultiIndexType, 'data', '_data')
make_attribute_wrapper(MultiIndexType, 'names', '_names')
make_attribute_wrapper(MultiIndexType, 'name', '_name')


@typeof_impl.register(pd.MultiIndex)
def typeof_multi_index(val, c):
    array_types = tuple(numba.typeof(val.levels[ocu__rtsc].values) for
        ocu__rtsc in range(val.nlevels))
    return MultiIndexType(array_types, tuple(get_val_type_maybe_str_literal
        (hdq__bzt) for hdq__bzt in val.names), numba.typeof(val.name))


@box(MultiIndexType)
def box_multi_index(typ, val, c):
    hzllk__tcj = c.context.insert_const_string(c.builder.module, 'pandas')
    phq__mmck = c.pyapi.import_module_noblock(hzllk__tcj)
    yhjc__xoc = c.pyapi.object_getattr_string(phq__mmck, 'MultiIndex')
    ypq__efde = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Tuple(typ.array_types), ypq__efde
        .data)
    rbgsm__dpv = c.pyapi.from_native_value(types.Tuple(typ.array_types),
        ypq__efde.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Tuple(typ.names_typ), ypq__efde.names
        )
    myt__hwo = c.pyapi.from_native_value(types.Tuple(typ.names_typ),
        ypq__efde.names, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, ypq__efde.name)
    rgvp__qtqmw = c.pyapi.from_native_value(typ.name_typ, ypq__efde.name, c
        .env_manager)
    agjad__puli = c.pyapi.borrow_none()
    xovmp__yvhpk = c.pyapi.call_method(yhjc__xoc, 'from_arrays', (
        rbgsm__dpv, agjad__puli, myt__hwo))
    c.pyapi.object_setattr_string(xovmp__yvhpk, 'name', rgvp__qtqmw)
    c.pyapi.decref(rbgsm__dpv)
    c.pyapi.decref(myt__hwo)
    c.pyapi.decref(rgvp__qtqmw)
    c.pyapi.decref(phq__mmck)
    c.pyapi.decref(yhjc__xoc)
    c.context.nrt.decref(c.builder, typ, val)
    return xovmp__yvhpk


@unbox(MultiIndexType)
def unbox_multi_index(typ, val, c):
    irm__ykgz = []
    wlil__ssbzp = []
    for ocu__rtsc in range(typ.nlevels):
        jgdzw__mtv = c.pyapi.unserialize(c.pyapi.serialize_object(ocu__rtsc))
        sxvg__hgxsd = c.pyapi.call_method(val, 'get_level_values', (
            jgdzw__mtv,))
        gomd__azgi = c.pyapi.object_getattr_string(sxvg__hgxsd, 'values')
        c.pyapi.decref(sxvg__hgxsd)
        c.pyapi.decref(jgdzw__mtv)
        mtsu__dqw = c.pyapi.to_native_value(typ.array_types[ocu__rtsc],
            gomd__azgi).value
        irm__ykgz.append(mtsu__dqw)
        wlil__ssbzp.append(gomd__azgi)
    if isinstance(types.Tuple(typ.array_types), types.UniTuple):
        data = cgutils.pack_array(c.builder, irm__ykgz)
    else:
        data = cgutils.pack_struct(c.builder, irm__ykgz)
    myt__hwo = c.pyapi.object_getattr_string(val, 'names')
    rzci__ncm = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    qav__dlr = c.pyapi.call_function_objargs(rzci__ncm, (myt__hwo,))
    names = c.pyapi.to_native_value(types.Tuple(typ.names_typ), qav__dlr).value
    rgvp__qtqmw = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, rgvp__qtqmw).value
    ypq__efde = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ypq__efde.data = data
    ypq__efde.names = names
    ypq__efde.name = name
    for gomd__azgi in wlil__ssbzp:
        c.pyapi.decref(gomd__azgi)
    c.pyapi.decref(myt__hwo)
    c.pyapi.decref(rzci__ncm)
    c.pyapi.decref(qav__dlr)
    c.pyapi.decref(rgvp__qtqmw)
    return NativeValue(ypq__efde._getvalue())


def from_product_error_checking(iterables, sortorder, names):
    ttjia__ttez = 'pandas.MultiIndex.from_product'
    bicck__yfnt = dict(sortorder=sortorder)
    ihs__srspn = dict(sortorder=None)
    check_unsupported_args(ttjia__ttez, bicck__yfnt, ihs__srspn,
        package_name='pandas', module_name='Index')
    if not (is_overload_none(names) or isinstance(names, types.BaseTuple)):
        raise BodoError(f'{ttjia__ttez}: names must be None or a tuple.')
    elif not isinstance(iterables, types.BaseTuple):
        raise BodoError(f'{ttjia__ttez}: iterables must be a tuple.')
    elif not is_overload_none(names) and len(iterables) != len(names):
        raise BodoError(
            f'{ttjia__ttez}: iterables and names must be of the same length.')


def from_product(iterable, sortorder=None, names=None):
    pass


@overload(from_product)
def from_product_overload(iterables, sortorder=None, names=None):
    from_product_error_checking(iterables, sortorder, names)
    array_types = tuple(dtype_to_array_type(iterable.dtype) for iterable in
        iterables)
    if is_overload_none(names):
        names_typ = tuple([types.none] * len(iterables))
    else:
        names_typ = names.types
    xcvcj__vihkw = MultiIndexType(array_types, names_typ)
    juidd__xfhr = f'from_product_multiindex{numba.core.ir_utils.next_label()}'
    setattr(types, juidd__xfhr, xcvcj__vihkw)
    rhfjt__naw = f"""
def impl(iterables, sortorder=None, names=None):
    with numba.objmode(mi='{juidd__xfhr}'):
        mi = pd.MultiIndex.from_product(iterables, names=names)
    return mi
"""
    pesx__zahik = {}
    exec(rhfjt__naw, globals(), pesx__zahik)
    rps__hgwp = pesx__zahik['impl']
    return rps__hgwp


@intrinsic
def init_multi_index(typingctx, data, names, name=None):
    name = types.none if name is None else name
    names = types.Tuple(names.types)

    def codegen(context, builder, signature, args):
        ivu__tem, nskbo__bplbt, iands__ood = args
        yvu__lqhpo = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        yvu__lqhpo.data = ivu__tem
        yvu__lqhpo.names = nskbo__bplbt
        yvu__lqhpo.name = iands__ood
        context.nrt.incref(builder, signature.args[0], ivu__tem)
        context.nrt.incref(builder, signature.args[1], nskbo__bplbt)
        context.nrt.incref(builder, signature.args[2], iands__ood)
        return yvu__lqhpo._getvalue()
    tchmg__pjq = MultiIndexType(data.types, names.types, name)
    return tchmg__pjq(data, names, name), codegen


@overload(len, no_unliteral=True)
def overload_len_pd_multiindex(A):
    if isinstance(A, MultiIndexType):
        return lambda A: len(A._data[0])


@overload(operator.getitem, no_unliteral=True)
def overload_multi_index_getitem(I, ind):
    if not isinstance(I, MultiIndexType):
        return
    if not isinstance(ind, types.Integer):
        agmc__kjm = len(I.array_types)
        rhfjt__naw = 'def impl(I, ind):\n'
        rhfjt__naw += '  data = I._data\n'
        rhfjt__naw += ('  return init_multi_index(({},), I._names, I._name)\n'
            .format(', '.join(
            f'ensure_contig_if_np(data[{ocu__rtsc}][ind])' for ocu__rtsc in
            range(agmc__kjm))))
        pesx__zahik = {}
        exec(rhfjt__naw, {'init_multi_index': init_multi_index,
            'ensure_contig_if_np': ensure_contig_if_np}, pesx__zahik)
        rps__hgwp = pesx__zahik['impl']
        return rps__hgwp


@lower_builtin(operator.is_, MultiIndexType, MultiIndexType)
def multi_index_is(context, builder, sig, args):
    edpq__glp, eiiuf__bzs = sig.args
    if edpq__glp != eiiuf__bzs:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._data is b._data and a._names is b._names and a._name is
            b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)
