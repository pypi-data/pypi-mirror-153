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
        fwi__pbrxg = [('data', types.Tuple(fe_type.array_types)), ('names',
            types.Tuple(fe_type.names_typ)), ('name', fe_type.name_typ)]
        super(MultiIndexModel, self).__init__(dmm, fe_type, fwi__pbrxg)


make_attribute_wrapper(MultiIndexType, 'data', '_data')
make_attribute_wrapper(MultiIndexType, 'names', '_names')
make_attribute_wrapper(MultiIndexType, 'name', '_name')


@typeof_impl.register(pd.MultiIndex)
def typeof_multi_index(val, c):
    array_types = tuple(numba.typeof(val.levels[zkh__aok].values) for
        zkh__aok in range(val.nlevels))
    return MultiIndexType(array_types, tuple(get_val_type_maybe_str_literal
        (snhc__hayl) for snhc__hayl in val.names), numba.typeof(val.name))


@box(MultiIndexType)
def box_multi_index(typ, val, c):
    hnql__ocfcg = c.context.insert_const_string(c.builder.module, 'pandas')
    nyyzc__ixfag = c.pyapi.import_module_noblock(hnql__ocfcg)
    wdohl__urnor = c.pyapi.object_getattr_string(nyyzc__ixfag, 'MultiIndex')
    ssrll__llqu = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Tuple(typ.array_types),
        ssrll__llqu.data)
    ygujd__uvyv = c.pyapi.from_native_value(types.Tuple(typ.array_types),
        ssrll__llqu.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Tuple(typ.names_typ), ssrll__llqu
        .names)
    swuua__fot = c.pyapi.from_native_value(types.Tuple(typ.names_typ),
        ssrll__llqu.names, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, ssrll__llqu.name)
    qpw__nkhr = c.pyapi.from_native_value(typ.name_typ, ssrll__llqu.name, c
        .env_manager)
    xaxfy__ldku = c.pyapi.borrow_none()
    gpbs__tccy = c.pyapi.call_method(wdohl__urnor, 'from_arrays', (
        ygujd__uvyv, xaxfy__ldku, swuua__fot))
    c.pyapi.object_setattr_string(gpbs__tccy, 'name', qpw__nkhr)
    c.pyapi.decref(ygujd__uvyv)
    c.pyapi.decref(swuua__fot)
    c.pyapi.decref(qpw__nkhr)
    c.pyapi.decref(nyyzc__ixfag)
    c.pyapi.decref(wdohl__urnor)
    c.context.nrt.decref(c.builder, typ, val)
    return gpbs__tccy


@unbox(MultiIndexType)
def unbox_multi_index(typ, val, c):
    xyat__ubb = []
    dyxb__qee = []
    for zkh__aok in range(typ.nlevels):
        myobi__tpnn = c.pyapi.unserialize(c.pyapi.serialize_object(zkh__aok))
        csi__fddut = c.pyapi.call_method(val, 'get_level_values', (
            myobi__tpnn,))
        omw__tokxh = c.pyapi.object_getattr_string(csi__fddut, 'values')
        c.pyapi.decref(csi__fddut)
        c.pyapi.decref(myobi__tpnn)
        grijg__cwgab = c.pyapi.to_native_value(typ.array_types[zkh__aok],
            omw__tokxh).value
        xyat__ubb.append(grijg__cwgab)
        dyxb__qee.append(omw__tokxh)
    if isinstance(types.Tuple(typ.array_types), types.UniTuple):
        data = cgutils.pack_array(c.builder, xyat__ubb)
    else:
        data = cgutils.pack_struct(c.builder, xyat__ubb)
    swuua__fot = c.pyapi.object_getattr_string(val, 'names')
    qvxaq__mbgz = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    amj__psuuo = c.pyapi.call_function_objargs(qvxaq__mbgz, (swuua__fot,))
    names = c.pyapi.to_native_value(types.Tuple(typ.names_typ), amj__psuuo
        ).value
    qpw__nkhr = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, qpw__nkhr).value
    ssrll__llqu = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ssrll__llqu.data = data
    ssrll__llqu.names = names
    ssrll__llqu.name = name
    for omw__tokxh in dyxb__qee:
        c.pyapi.decref(omw__tokxh)
    c.pyapi.decref(swuua__fot)
    c.pyapi.decref(qvxaq__mbgz)
    c.pyapi.decref(amj__psuuo)
    c.pyapi.decref(qpw__nkhr)
    return NativeValue(ssrll__llqu._getvalue())


def from_product_error_checking(iterables, sortorder, names):
    fad__iskx = 'pandas.MultiIndex.from_product'
    rapb__qdtip = dict(sortorder=sortorder)
    ezjl__inv = dict(sortorder=None)
    check_unsupported_args(fad__iskx, rapb__qdtip, ezjl__inv, package_name=
        'pandas', module_name='Index')
    if not (is_overload_none(names) or isinstance(names, types.BaseTuple)):
        raise BodoError(f'{fad__iskx}: names must be None or a tuple.')
    elif not isinstance(iterables, types.BaseTuple):
        raise BodoError(f'{fad__iskx}: iterables must be a tuple.')
    elif not is_overload_none(names) and len(iterables) != len(names):
        raise BodoError(
            f'{fad__iskx}: iterables and names must be of the same length.')


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
    tbvh__xuwmo = MultiIndexType(array_types, names_typ)
    egb__rwyfq = f'from_product_multiindex{numba.core.ir_utils.next_label()}'
    setattr(types, egb__rwyfq, tbvh__xuwmo)
    xnuwl__azwrx = f"""
def impl(iterables, sortorder=None, names=None):
    with numba.objmode(mi='{egb__rwyfq}'):
        mi = pd.MultiIndex.from_product(iterables, names=names)
    return mi
"""
    oap__jej = {}
    exec(xnuwl__azwrx, globals(), oap__jej)
    acu__ksgpw = oap__jej['impl']
    return acu__ksgpw


@intrinsic
def init_multi_index(typingctx, data, names, name=None):
    name = types.none if name is None else name
    names = types.Tuple(names.types)

    def codegen(context, builder, signature, args):
        drvu__mzdn, dnl__rfxi, whg__bsfdc = args
        jktm__nchm = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        jktm__nchm.data = drvu__mzdn
        jktm__nchm.names = dnl__rfxi
        jktm__nchm.name = whg__bsfdc
        context.nrt.incref(builder, signature.args[0], drvu__mzdn)
        context.nrt.incref(builder, signature.args[1], dnl__rfxi)
        context.nrt.incref(builder, signature.args[2], whg__bsfdc)
        return jktm__nchm._getvalue()
    wdhlc__bopl = MultiIndexType(data.types, names.types, name)
    return wdhlc__bopl(data, names, name), codegen


@overload(len, no_unliteral=True)
def overload_len_pd_multiindex(A):
    if isinstance(A, MultiIndexType):
        return lambda A: len(A._data[0])


@overload(operator.getitem, no_unliteral=True)
def overload_multi_index_getitem(I, ind):
    if not isinstance(I, MultiIndexType):
        return
    if not isinstance(ind, types.Integer):
        abv__pxqo = len(I.array_types)
        xnuwl__azwrx = 'def impl(I, ind):\n'
        xnuwl__azwrx += '  data = I._data\n'
        xnuwl__azwrx += (
            '  return init_multi_index(({},), I._names, I._name)\n'.format(
            ', '.join(f'ensure_contig_if_np(data[{zkh__aok}][ind])' for
            zkh__aok in range(abv__pxqo))))
        oap__jej = {}
        exec(xnuwl__azwrx, {'init_multi_index': init_multi_index,
            'ensure_contig_if_np': ensure_contig_if_np}, oap__jej)
        acu__ksgpw = oap__jej['impl']
        return acu__ksgpw


@lower_builtin(operator.is_, MultiIndexType, MultiIndexType)
def multi_index_is(context, builder, sig, args):
    gtcha__hph, kpet__cbpir = sig.args
    if gtcha__hph != kpet__cbpir:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._data is b._data and a._names is b._names and a._name is
            b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)
