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
        mzt__ngw = [('data', types.Tuple(fe_type.array_types)), ('names',
            types.Tuple(fe_type.names_typ)), ('name', fe_type.name_typ)]
        super(MultiIndexModel, self).__init__(dmm, fe_type, mzt__ngw)


make_attribute_wrapper(MultiIndexType, 'data', '_data')
make_attribute_wrapper(MultiIndexType, 'names', '_names')
make_attribute_wrapper(MultiIndexType, 'name', '_name')


@typeof_impl.register(pd.MultiIndex)
def typeof_multi_index(val, c):
    array_types = tuple(numba.typeof(val.levels[qdim__eqy].values) for
        qdim__eqy in range(val.nlevels))
    return MultiIndexType(array_types, tuple(get_val_type_maybe_str_literal
        (mvhvu__kvmj) for mvhvu__kvmj in val.names), numba.typeof(val.name))


@box(MultiIndexType)
def box_multi_index(typ, val, c):
    gxuk__nydxp = c.context.insert_const_string(c.builder.module, 'pandas')
    ugm__fsqpx = c.pyapi.import_module_noblock(gxuk__nydxp)
    sfvne__qtz = c.pyapi.object_getattr_string(ugm__fsqpx, 'MultiIndex')
    oqtj__ici = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Tuple(typ.array_types), oqtj__ici
        .data)
    mixl__sel = c.pyapi.from_native_value(types.Tuple(typ.array_types),
        oqtj__ici.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Tuple(typ.names_typ), oqtj__ici.names
        )
    ivpvd__odga = c.pyapi.from_native_value(types.Tuple(typ.names_typ),
        oqtj__ici.names, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, oqtj__ici.name)
    weqx__llcac = c.pyapi.from_native_value(typ.name_typ, oqtj__ici.name, c
        .env_manager)
    hyd__phs = c.pyapi.borrow_none()
    shj__wjr = c.pyapi.call_method(sfvne__qtz, 'from_arrays', (mixl__sel,
        hyd__phs, ivpvd__odga))
    c.pyapi.object_setattr_string(shj__wjr, 'name', weqx__llcac)
    c.pyapi.decref(mixl__sel)
    c.pyapi.decref(ivpvd__odga)
    c.pyapi.decref(weqx__llcac)
    c.pyapi.decref(ugm__fsqpx)
    c.pyapi.decref(sfvne__qtz)
    c.context.nrt.decref(c.builder, typ, val)
    return shj__wjr


@unbox(MultiIndexType)
def unbox_multi_index(typ, val, c):
    agi__ssdds = []
    fjub__gdn = []
    for qdim__eqy in range(typ.nlevels):
        attw__xtn = c.pyapi.unserialize(c.pyapi.serialize_object(qdim__eqy))
        lntd__wdp = c.pyapi.call_method(val, 'get_level_values', (attw__xtn,))
        aqgic__sva = c.pyapi.object_getattr_string(lntd__wdp, 'values')
        c.pyapi.decref(lntd__wdp)
        c.pyapi.decref(attw__xtn)
        zgr__dpdgs = c.pyapi.to_native_value(typ.array_types[qdim__eqy],
            aqgic__sva).value
        agi__ssdds.append(zgr__dpdgs)
        fjub__gdn.append(aqgic__sva)
    if isinstance(types.Tuple(typ.array_types), types.UniTuple):
        data = cgutils.pack_array(c.builder, agi__ssdds)
    else:
        data = cgutils.pack_struct(c.builder, agi__ssdds)
    ivpvd__odga = c.pyapi.object_getattr_string(val, 'names')
    hlsd__alt = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    ivg__tdsq = c.pyapi.call_function_objargs(hlsd__alt, (ivpvd__odga,))
    names = c.pyapi.to_native_value(types.Tuple(typ.names_typ), ivg__tdsq
        ).value
    weqx__llcac = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, weqx__llcac).value
    oqtj__ici = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    oqtj__ici.data = data
    oqtj__ici.names = names
    oqtj__ici.name = name
    for aqgic__sva in fjub__gdn:
        c.pyapi.decref(aqgic__sva)
    c.pyapi.decref(ivpvd__odga)
    c.pyapi.decref(hlsd__alt)
    c.pyapi.decref(ivg__tdsq)
    c.pyapi.decref(weqx__llcac)
    return NativeValue(oqtj__ici._getvalue())


def from_product_error_checking(iterables, sortorder, names):
    ygh__narqc = 'pandas.MultiIndex.from_product'
    vbs__hxxg = dict(sortorder=sortorder)
    uuc__krgt = dict(sortorder=None)
    check_unsupported_args(ygh__narqc, vbs__hxxg, uuc__krgt, package_name=
        'pandas', module_name='Index')
    if not (is_overload_none(names) or isinstance(names, types.BaseTuple)):
        raise BodoError(f'{ygh__narqc}: names must be None or a tuple.')
    elif not isinstance(iterables, types.BaseTuple):
        raise BodoError(f'{ygh__narqc}: iterables must be a tuple.')
    elif not is_overload_none(names) and len(iterables) != len(names):
        raise BodoError(
            f'{ygh__narqc}: iterables and names must be of the same length.')


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
    igv__hlqqg = MultiIndexType(array_types, names_typ)
    sgy__fxy = f'from_product_multiindex{numba.core.ir_utils.next_label()}'
    setattr(types, sgy__fxy, igv__hlqqg)
    mgcgc__pfd = f"""
def impl(iterables, sortorder=None, names=None):
    with numba.objmode(mi='{sgy__fxy}'):
        mi = pd.MultiIndex.from_product(iterables, names=names)
    return mi
"""
    mtiy__jxpg = {}
    exec(mgcgc__pfd, globals(), mtiy__jxpg)
    dwln__fdrp = mtiy__jxpg['impl']
    return dwln__fdrp


@intrinsic
def init_multi_index(typingctx, data, names, name=None):
    name = types.none if name is None else name
    names = types.Tuple(names.types)

    def codegen(context, builder, signature, args):
        sbvt__bpox, qhxx__iwyxy, mwv__igf = args
        rhqro__liib = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        rhqro__liib.data = sbvt__bpox
        rhqro__liib.names = qhxx__iwyxy
        rhqro__liib.name = mwv__igf
        context.nrt.incref(builder, signature.args[0], sbvt__bpox)
        context.nrt.incref(builder, signature.args[1], qhxx__iwyxy)
        context.nrt.incref(builder, signature.args[2], mwv__igf)
        return rhqro__liib._getvalue()
    fue__tejrp = MultiIndexType(data.types, names.types, name)
    return fue__tejrp(data, names, name), codegen


@overload(len, no_unliteral=True)
def overload_len_pd_multiindex(A):
    if isinstance(A, MultiIndexType):
        return lambda A: len(A._data[0])


@overload(operator.getitem, no_unliteral=True)
def overload_multi_index_getitem(I, ind):
    if not isinstance(I, MultiIndexType):
        return
    if not isinstance(ind, types.Integer):
        aukw__izhq = len(I.array_types)
        mgcgc__pfd = 'def impl(I, ind):\n'
        mgcgc__pfd += '  data = I._data\n'
        mgcgc__pfd += ('  return init_multi_index(({},), I._names, I._name)\n'
            .format(', '.join(
            f'ensure_contig_if_np(data[{qdim__eqy}][ind])' for qdim__eqy in
            range(aukw__izhq))))
        mtiy__jxpg = {}
        exec(mgcgc__pfd, {'init_multi_index': init_multi_index,
            'ensure_contig_if_np': ensure_contig_if_np}, mtiy__jxpg)
        dwln__fdrp = mtiy__jxpg['impl']
        return dwln__fdrp


@lower_builtin(operator.is_, MultiIndexType, MultiIndexType)
def multi_index_is(context, builder, sig, args):
    lideg__edxe, yhzbg__kpbl = sig.args
    if lideg__edxe != yhzbg__kpbl:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._data is b._data and a._names is b._names and a._name is
            b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)
