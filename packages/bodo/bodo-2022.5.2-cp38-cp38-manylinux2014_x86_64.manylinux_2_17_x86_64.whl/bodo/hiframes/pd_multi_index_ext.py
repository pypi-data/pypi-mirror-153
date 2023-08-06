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
        vupjw__pou = [('data', types.Tuple(fe_type.array_types)), ('names',
            types.Tuple(fe_type.names_typ)), ('name', fe_type.name_typ)]
        super(MultiIndexModel, self).__init__(dmm, fe_type, vupjw__pou)


make_attribute_wrapper(MultiIndexType, 'data', '_data')
make_attribute_wrapper(MultiIndexType, 'names', '_names')
make_attribute_wrapper(MultiIndexType, 'name', '_name')


@typeof_impl.register(pd.MultiIndex)
def typeof_multi_index(val, c):
    array_types = tuple(numba.typeof(val.levels[prsak__agb].values) for
        prsak__agb in range(val.nlevels))
    return MultiIndexType(array_types, tuple(get_val_type_maybe_str_literal
        (yuey__twv) for yuey__twv in val.names), numba.typeof(val.name))


@box(MultiIndexType)
def box_multi_index(typ, val, c):
    upy__hksgn = c.context.insert_const_string(c.builder.module, 'pandas')
    juhru__zfagg = c.pyapi.import_module_noblock(upy__hksgn)
    sxb__zuba = c.pyapi.object_getattr_string(juhru__zfagg, 'MultiIndex')
    bijfj__trrk = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Tuple(typ.array_types),
        bijfj__trrk.data)
    cplyg__ycir = c.pyapi.from_native_value(types.Tuple(typ.array_types),
        bijfj__trrk.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Tuple(typ.names_typ), bijfj__trrk
        .names)
    tgtyz__hzhd = c.pyapi.from_native_value(types.Tuple(typ.names_typ),
        bijfj__trrk.names, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, bijfj__trrk.name)
    qsjhh__ehf = c.pyapi.from_native_value(typ.name_typ, bijfj__trrk.name,
        c.env_manager)
    nxwx__tbus = c.pyapi.borrow_none()
    xja__wdkzd = c.pyapi.call_method(sxb__zuba, 'from_arrays', (cplyg__ycir,
        nxwx__tbus, tgtyz__hzhd))
    c.pyapi.object_setattr_string(xja__wdkzd, 'name', qsjhh__ehf)
    c.pyapi.decref(cplyg__ycir)
    c.pyapi.decref(tgtyz__hzhd)
    c.pyapi.decref(qsjhh__ehf)
    c.pyapi.decref(juhru__zfagg)
    c.pyapi.decref(sxb__zuba)
    c.context.nrt.decref(c.builder, typ, val)
    return xja__wdkzd


@unbox(MultiIndexType)
def unbox_multi_index(typ, val, c):
    uzgew__arhql = []
    cnow__ffg = []
    for prsak__agb in range(typ.nlevels):
        zahm__ljsn = c.pyapi.unserialize(c.pyapi.serialize_object(prsak__agb))
        zbdda__krgdp = c.pyapi.call_method(val, 'get_level_values', (
            zahm__ljsn,))
        eejo__ogr = c.pyapi.object_getattr_string(zbdda__krgdp, 'values')
        c.pyapi.decref(zbdda__krgdp)
        c.pyapi.decref(zahm__ljsn)
        vyowj__pfmr = c.pyapi.to_native_value(typ.array_types[prsak__agb],
            eejo__ogr).value
        uzgew__arhql.append(vyowj__pfmr)
        cnow__ffg.append(eejo__ogr)
    if isinstance(types.Tuple(typ.array_types), types.UniTuple):
        data = cgutils.pack_array(c.builder, uzgew__arhql)
    else:
        data = cgutils.pack_struct(c.builder, uzgew__arhql)
    tgtyz__hzhd = c.pyapi.object_getattr_string(val, 'names')
    nalyl__gokh = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    husl__nhe = c.pyapi.call_function_objargs(nalyl__gokh, (tgtyz__hzhd,))
    names = c.pyapi.to_native_value(types.Tuple(typ.names_typ), husl__nhe
        ).value
    qsjhh__ehf = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, qsjhh__ehf).value
    bijfj__trrk = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    bijfj__trrk.data = data
    bijfj__trrk.names = names
    bijfj__trrk.name = name
    for eejo__ogr in cnow__ffg:
        c.pyapi.decref(eejo__ogr)
    c.pyapi.decref(tgtyz__hzhd)
    c.pyapi.decref(nalyl__gokh)
    c.pyapi.decref(husl__nhe)
    c.pyapi.decref(qsjhh__ehf)
    return NativeValue(bijfj__trrk._getvalue())


def from_product_error_checking(iterables, sortorder, names):
    uwuwo__qbh = 'pandas.MultiIndex.from_product'
    qqf__ubw = dict(sortorder=sortorder)
    yyqw__orqs = dict(sortorder=None)
    check_unsupported_args(uwuwo__qbh, qqf__ubw, yyqw__orqs, package_name=
        'pandas', module_name='Index')
    if not (is_overload_none(names) or isinstance(names, types.BaseTuple)):
        raise BodoError(f'{uwuwo__qbh}: names must be None or a tuple.')
    elif not isinstance(iterables, types.BaseTuple):
        raise BodoError(f'{uwuwo__qbh}: iterables must be a tuple.')
    elif not is_overload_none(names) and len(iterables) != len(names):
        raise BodoError(
            f'{uwuwo__qbh}: iterables and names must be of the same length.')


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
    hakiu__hjabr = MultiIndexType(array_types, names_typ)
    zxryc__yvv = f'from_product_multiindex{numba.core.ir_utils.next_label()}'
    setattr(types, zxryc__yvv, hakiu__hjabr)
    mry__qzqyp = f"""
def impl(iterables, sortorder=None, names=None):
    with numba.objmode(mi='{zxryc__yvv}'):
        mi = pd.MultiIndex.from_product(iterables, names=names)
    return mi
"""
    xpqk__npcf = {}
    exec(mry__qzqyp, globals(), xpqk__npcf)
    vza__zdq = xpqk__npcf['impl']
    return vza__zdq


@intrinsic
def init_multi_index(typingctx, data, names, name=None):
    name = types.none if name is None else name
    names = types.Tuple(names.types)

    def codegen(context, builder, signature, args):
        hvfnd__gsei, cbobz__ubvj, bagw__mljsc = args
        tead__ruz = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        tead__ruz.data = hvfnd__gsei
        tead__ruz.names = cbobz__ubvj
        tead__ruz.name = bagw__mljsc
        context.nrt.incref(builder, signature.args[0], hvfnd__gsei)
        context.nrt.incref(builder, signature.args[1], cbobz__ubvj)
        context.nrt.incref(builder, signature.args[2], bagw__mljsc)
        return tead__ruz._getvalue()
    yld__qyj = MultiIndexType(data.types, names.types, name)
    return yld__qyj(data, names, name), codegen


@overload(len, no_unliteral=True)
def overload_len_pd_multiindex(A):
    if isinstance(A, MultiIndexType):
        return lambda A: len(A._data[0])


@overload(operator.getitem, no_unliteral=True)
def overload_multi_index_getitem(I, ind):
    if not isinstance(I, MultiIndexType):
        return
    if not isinstance(ind, types.Integer):
        nrc__jft = len(I.array_types)
        mry__qzqyp = 'def impl(I, ind):\n'
        mry__qzqyp += '  data = I._data\n'
        mry__qzqyp += ('  return init_multi_index(({},), I._names, I._name)\n'
            .format(', '.join(
            f'ensure_contig_if_np(data[{prsak__agb}][ind])' for prsak__agb in
            range(nrc__jft))))
        xpqk__npcf = {}
        exec(mry__qzqyp, {'init_multi_index': init_multi_index,
            'ensure_contig_if_np': ensure_contig_if_np}, xpqk__npcf)
        vza__zdq = xpqk__npcf['impl']
        return vza__zdq


@lower_builtin(operator.is_, MultiIndexType, MultiIndexType)
def multi_index_is(context, builder, sig, args):
    mll__pzw, dhkag__oca = sig.args
    if mll__pzw != dhkag__oca:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._data is b._data and a._names is b._names and a._name is
            b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)
