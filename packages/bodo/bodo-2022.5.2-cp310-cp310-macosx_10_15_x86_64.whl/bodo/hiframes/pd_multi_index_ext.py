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
        ehny__njhy = [('data', types.Tuple(fe_type.array_types)), ('names',
            types.Tuple(fe_type.names_typ)), ('name', fe_type.name_typ)]
        super(MultiIndexModel, self).__init__(dmm, fe_type, ehny__njhy)


make_attribute_wrapper(MultiIndexType, 'data', '_data')
make_attribute_wrapper(MultiIndexType, 'names', '_names')
make_attribute_wrapper(MultiIndexType, 'name', '_name')


@typeof_impl.register(pd.MultiIndex)
def typeof_multi_index(val, c):
    array_types = tuple(numba.typeof(val.levels[ybbi__ibc].values) for
        ybbi__ibc in range(val.nlevels))
    return MultiIndexType(array_types, tuple(get_val_type_maybe_str_literal
        (jsvmd__jzof) for jsvmd__jzof in val.names), numba.typeof(val.name))


@box(MultiIndexType)
def box_multi_index(typ, val, c):
    rmai__esqnw = c.context.insert_const_string(c.builder.module, 'pandas')
    mwb__cqrl = c.pyapi.import_module_noblock(rmai__esqnw)
    axh__xsj = c.pyapi.object_getattr_string(mwb__cqrl, 'MultiIndex')
    zhyhg__tvt = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Tuple(typ.array_types),
        zhyhg__tvt.data)
    iikn__afvb = c.pyapi.from_native_value(types.Tuple(typ.array_types),
        zhyhg__tvt.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Tuple(typ.names_typ), zhyhg__tvt.
        names)
    nsezt__zsz = c.pyapi.from_native_value(types.Tuple(typ.names_typ),
        zhyhg__tvt.names, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, zhyhg__tvt.name)
    djk__vpw = c.pyapi.from_native_value(typ.name_typ, zhyhg__tvt.name, c.
        env_manager)
    igv__rsey = c.pyapi.borrow_none()
    zhlya__ycy = c.pyapi.call_method(axh__xsj, 'from_arrays', (iikn__afvb,
        igv__rsey, nsezt__zsz))
    c.pyapi.object_setattr_string(zhlya__ycy, 'name', djk__vpw)
    c.pyapi.decref(iikn__afvb)
    c.pyapi.decref(nsezt__zsz)
    c.pyapi.decref(djk__vpw)
    c.pyapi.decref(mwb__cqrl)
    c.pyapi.decref(axh__xsj)
    c.context.nrt.decref(c.builder, typ, val)
    return zhlya__ycy


@unbox(MultiIndexType)
def unbox_multi_index(typ, val, c):
    biotb__tgwbw = []
    ylnyg__njr = []
    for ybbi__ibc in range(typ.nlevels):
        mhb__iail = c.pyapi.unserialize(c.pyapi.serialize_object(ybbi__ibc))
        ydhqy__fzako = c.pyapi.call_method(val, 'get_level_values', (
            mhb__iail,))
        ike__ftdpl = c.pyapi.object_getattr_string(ydhqy__fzako, 'values')
        c.pyapi.decref(ydhqy__fzako)
        c.pyapi.decref(mhb__iail)
        odsp__uac = c.pyapi.to_native_value(typ.array_types[ybbi__ibc],
            ike__ftdpl).value
        biotb__tgwbw.append(odsp__uac)
        ylnyg__njr.append(ike__ftdpl)
    if isinstance(types.Tuple(typ.array_types), types.UniTuple):
        data = cgutils.pack_array(c.builder, biotb__tgwbw)
    else:
        data = cgutils.pack_struct(c.builder, biotb__tgwbw)
    nsezt__zsz = c.pyapi.object_getattr_string(val, 'names')
    hdlj__suke = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    npxug__qsd = c.pyapi.call_function_objargs(hdlj__suke, (nsezt__zsz,))
    names = c.pyapi.to_native_value(types.Tuple(typ.names_typ), npxug__qsd
        ).value
    djk__vpw = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, djk__vpw).value
    zhyhg__tvt = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    zhyhg__tvt.data = data
    zhyhg__tvt.names = names
    zhyhg__tvt.name = name
    for ike__ftdpl in ylnyg__njr:
        c.pyapi.decref(ike__ftdpl)
    c.pyapi.decref(nsezt__zsz)
    c.pyapi.decref(hdlj__suke)
    c.pyapi.decref(npxug__qsd)
    c.pyapi.decref(djk__vpw)
    return NativeValue(zhyhg__tvt._getvalue())


def from_product_error_checking(iterables, sortorder, names):
    ckzid__jinvr = 'pandas.MultiIndex.from_product'
    imyo__ftta = dict(sortorder=sortorder)
    rva__ycxl = dict(sortorder=None)
    check_unsupported_args(ckzid__jinvr, imyo__ftta, rva__ycxl,
        package_name='pandas', module_name='Index')
    if not (is_overload_none(names) or isinstance(names, types.BaseTuple)):
        raise BodoError(f'{ckzid__jinvr}: names must be None or a tuple.')
    elif not isinstance(iterables, types.BaseTuple):
        raise BodoError(f'{ckzid__jinvr}: iterables must be a tuple.')
    elif not is_overload_none(names) and len(iterables) != len(names):
        raise BodoError(
            f'{ckzid__jinvr}: iterables and names must be of the same length.')


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
    xwi__mlpqe = MultiIndexType(array_types, names_typ)
    mmv__raftp = f'from_product_multiindex{numba.core.ir_utils.next_label()}'
    setattr(types, mmv__raftp, xwi__mlpqe)
    gfj__ofwct = f"""
def impl(iterables, sortorder=None, names=None):
    with numba.objmode(mi='{mmv__raftp}'):
        mi = pd.MultiIndex.from_product(iterables, names=names)
    return mi
"""
    hsd__ljoqo = {}
    exec(gfj__ofwct, globals(), hsd__ljoqo)
    jwid__oal = hsd__ljoqo['impl']
    return jwid__oal


@intrinsic
def init_multi_index(typingctx, data, names, name=None):
    name = types.none if name is None else name
    names = types.Tuple(names.types)

    def codegen(context, builder, signature, args):
        lbcw__eaeur, xtrh__tsuat, qeyph__amquy = args
        cvoqd__xdg = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        cvoqd__xdg.data = lbcw__eaeur
        cvoqd__xdg.names = xtrh__tsuat
        cvoqd__xdg.name = qeyph__amquy
        context.nrt.incref(builder, signature.args[0], lbcw__eaeur)
        context.nrt.incref(builder, signature.args[1], xtrh__tsuat)
        context.nrt.incref(builder, signature.args[2], qeyph__amquy)
        return cvoqd__xdg._getvalue()
    ssy__bzej = MultiIndexType(data.types, names.types, name)
    return ssy__bzej(data, names, name), codegen


@overload(len, no_unliteral=True)
def overload_len_pd_multiindex(A):
    if isinstance(A, MultiIndexType):
        return lambda A: len(A._data[0])


@overload(operator.getitem, no_unliteral=True)
def overload_multi_index_getitem(I, ind):
    if not isinstance(I, MultiIndexType):
        return
    if not isinstance(ind, types.Integer):
        rcnp__qzrw = len(I.array_types)
        gfj__ofwct = 'def impl(I, ind):\n'
        gfj__ofwct += '  data = I._data\n'
        gfj__ofwct += ('  return init_multi_index(({},), I._names, I._name)\n'
            .format(', '.join(
            f'ensure_contig_if_np(data[{ybbi__ibc}][ind])' for ybbi__ibc in
            range(rcnp__qzrw))))
        hsd__ljoqo = {}
        exec(gfj__ofwct, {'init_multi_index': init_multi_index,
            'ensure_contig_if_np': ensure_contig_if_np}, hsd__ljoqo)
        jwid__oal = hsd__ljoqo['impl']
        return jwid__oal


@lower_builtin(operator.is_, MultiIndexType, MultiIndexType)
def multi_index_is(context, builder, sig, args):
    byya__kem, oyk__imo = sig.args
    if byya__kem != oyk__imo:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._data is b._data and a._names is b._names and a._name is
            b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)
