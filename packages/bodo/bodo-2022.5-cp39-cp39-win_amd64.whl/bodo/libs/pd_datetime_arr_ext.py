"""DatetimeArray extension for Pandas DatetimeArray with timezone support."""
import operator
import numba
import pandas as pd
import pytz
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.utils.conversion import ensure_contig_if_np
from bodo.utils.typing import BodoArrayIterator, BodoError, get_literal_value, is_list_like_index_type, is_overload_constant_int, is_overload_constant_str, raise_bodo_error


class PandasDatetimeTZDtype(types.Type):

    def __init__(self, tz):
        if isinstance(tz, (pytz._FixedOffset, pytz.tzinfo.BaseTzInfo)):
            tz = get_pytz_type_info(tz)
        if not isinstance(tz, (int, str)):
            raise BodoError(
                'Timezone must be either a valid pytz type with a zone or a fixed offset'
                )
        self.tz = tz
        super(PandasDatetimeTZDtype, self).__init__(name=
            f'PandasDatetimeTZDtype[{tz}]')


def get_pytz_type_info(pytz_type):
    if isinstance(pytz_type, pytz._FixedOffset):
        nhl__lcjne = pd.Timedelta(pytz_type._offset).value
    else:
        nhl__lcjne = pytz_type.zone
        if nhl__lcjne not in pytz.all_timezones_set:
            raise BodoError(
                'Unsupported timezone type. Timezones must be a fixedOffset or contain a zone found in pytz.all_timezones'
                )
    return nhl__lcjne


def nanoseconds_to_offset(nanoseconds):
    kyfpp__tge = nanoseconds // (60 * 1000 * 1000 * 1000)
    return pytz.FixedOffset(kyfpp__tge)


class DatetimeArrayType(types.IterableType, types.ArrayCompatible):

    def __init__(self, tz):
        if isinstance(tz, (pytz._FixedOffset, pytz.tzinfo.BaseTzInfo)):
            tz = get_pytz_type_info(tz)
        if not isinstance(tz, (int, str)):
            raise BodoError(
                'Timezone must be either a valid pytz type with a zone or a fixed offset'
                )
        self.tz = tz
        self._data_array_type = types.Array(types.NPDatetime('ns'), 1, 'C')
        self._dtype = PandasDatetimeTZDtype(tz)
        super(DatetimeArrayType, self).__init__(name=
            f'PandasDatetimeArray[{tz}]')

    @property
    def data_array_type(self):
        return self._data_array_type

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def iterator_type(self):
        return BodoArrayIterator(self)

    @property
    def dtype(self):
        return self._dtype

    def copy(self):
        return DatetimeArrayType(self.tz)


@register_model(DatetimeArrayType)
class PandasDatetimeArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        kyzvo__ayp = [('data', fe_type.data_array_type)]
        models.StructModel.__init__(self, dmm, fe_type, kyzvo__ayp)


make_attribute_wrapper(DatetimeArrayType, 'data', '_data')


@typeof_impl.register(pd.arrays.DatetimeArray)
def typeof_pd_datetime_array(val, c):
    if val.tz is None:
        raise BodoError(
            "Cannot support timezone naive pd.arrays.DatetimeArray. Please convert to a numpy array with .astype('datetime64[ns]')."
            )
    else:
        return DatetimeArrayType(val.dtype.tz)


@unbox(DatetimeArrayType)
def unbox_pd_datetime_array(typ, val, c):
    ncy__jlne = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    vmtx__hjtuw = c.pyapi.string_from_constant_string('datetime64[ns]')
    plptz__lsjgw = c.pyapi.call_method(val, 'to_numpy', (vmtx__hjtuw,))
    ncy__jlne.data = c.unbox(typ.data_array_type, plptz__lsjgw).value
    c.pyapi.decref(plptz__lsjgw)
    ihwyl__vqw = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ncy__jlne._getvalue(), is_error=ihwyl__vqw)


@box(DatetimeArrayType)
def box_pd_datetime_array(typ, val, c):
    ncy__jlne = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    c.context.nrt.incref(c.builder, typ.data_array_type, ncy__jlne.data)
    bofkm__qjurm = c.pyapi.from_native_value(typ.data_array_type, ncy__jlne
        .data, c.env_manager)
    gmmz__gcr = c.context.get_constant_generic(c.builder, types.
        unicode_type, 'ns')
    vkvgb__lvcs = c.pyapi.from_native_value(types.unicode_type, gmmz__gcr,
        c.env_manager)
    if isinstance(typ.tz, str):
        flre__elace = c.context.get_constant_generic(c.builder, types.
            unicode_type, typ.tz)
        rvjim__nnj = c.pyapi.from_native_value(types.unicode_type,
            flre__elace, c.env_manager)
    else:
        sbr__xyavk = nanoseconds_to_offset(typ.tz)
        rvjim__nnj = c.pyapi.unserialize(c.pyapi.serialize_object(sbr__xyavk))
    neg__pfcyc = c.context.insert_const_string(c.builder.module, 'pandas')
    zyji__xrw = c.pyapi.import_module_noblock(neg__pfcyc)
    ajbdn__khk = c.pyapi.call_method(zyji__xrw, 'DatetimeTZDtype', (
        vkvgb__lvcs, rvjim__nnj))
    tmrf__wzetw = c.pyapi.object_getattr_string(zyji__xrw, 'arrays')
    czuy__zplnx = c.pyapi.call_method(tmrf__wzetw, 'DatetimeArray', (
        bofkm__qjurm, ajbdn__khk))
    c.pyapi.decref(bofkm__qjurm)
    c.pyapi.decref(vkvgb__lvcs)
    c.pyapi.decref(rvjim__nnj)
    c.pyapi.decref(zyji__xrw)
    c.pyapi.decref(ajbdn__khk)
    c.pyapi.decref(tmrf__wzetw)
    c.context.nrt.decref(c.builder, typ, val)
    return czuy__zplnx


@intrinsic
def init_pandas_datetime_array(typingctx, data, tz):

    def codegen(context, builder, sig, args):
        data, tz = args
        udbky__clga = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        udbky__clga.data = data
        context.nrt.incref(builder, sig.args[0], data)
        return udbky__clga._getvalue()
    if is_overload_constant_str(tz) or is_overload_constant_int(tz):
        flre__elace = get_literal_value(tz)
    else:
        raise BodoError('tz must be a constant string or Fixed Offset')
    fwbj__yekl = DatetimeArrayType(flre__elace)
    sig = fwbj__yekl(fwbj__yekl.data_array_type, tz)
    return sig, codegen


@overload(len, no_unliteral=True)
def overload_pd_datetime_arr_len(A):
    if isinstance(A, DatetimeArrayType):
        return lambda A: len(A._data)


@lower_constant(DatetimeArrayType)
def lower_constant_pd_datetime_arr(context, builder, typ, pyval):
    vbyt__pqnja = context.get_constant_generic(builder, typ.data_array_type,
        pyval.to_numpy('datetime64[ns]'))
    sgt__mrxkx = lir.Constant.literal_struct([vbyt__pqnja])
    return sgt__mrxkx


@overload_attribute(DatetimeArrayType, 'shape')
def overload_pd_datetime_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(DatetimeArrayType, 'nbytes')
def overload_pd_datetime_arr_nbytes(A):
    return lambda A: A._data.nbytes


@overload_method(DatetimeArrayType, 'tz_convert', no_unliteral=True)
def overload_pd_datetime_tz_convert(A, tz):
    if tz == types.none:
        raise_bodo_error('tz_convert(): tz must be a string or Fixed Offset')
    else:

        def impl(A, tz):
            return init_pandas_datetime_array(A._data.copy(), tz)
    return impl


@overload_method(DatetimeArrayType, 'copy', no_unliteral=True)
def overload_pd_datetime_tz_convert(A):
    tz = A.tz

    def impl(A):
        return init_pandas_datetime_array(A._data.copy(), tz)
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_getitem(A, ind):
    if not isinstance(A, DatetimeArrayType):
        return
    tz = A.tz
    if isinstance(ind, types.Integer):

        def impl(A, ind):
            return bodo.hiframes.pd_timestamp_ext.convert_val_to_timestamp(bodo
                .hiframes.pd_timestamp_ext.dt64_to_integer(A._data[ind]), tz)
        return impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            ind = bodo.utils.conversion.coerce_to_ndarray(ind)
            wzhk__ietog = ensure_contig_if_np(A._data[ind])
            return init_pandas_datetime_array(wzhk__ietog, tz)
        return impl_bool
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            wzhk__ietog = ensure_contig_if_np(A._data[ind])
            return init_pandas_datetime_array(wzhk__ietog, tz)
        return impl_slice
    raise BodoError(
        'operator.getitem with DatetimeArrayType is only supported with an integer index, boolean array, or slice.'
        )


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def unwrap_tz_array(A):
    if isinstance(A, DatetimeArrayType):
        return lambda A: A._data
    return lambda A: A


def unwrap_tz_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    lty__vttg = args[0]
    if equiv_set.has_shape(lty__vttg):
        return ArrayAnalysis.AnalyzeResult(shape=lty__vttg, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_libs_pd_datetime_arr_ext_unwrap_tz_array
    ) = unwrap_tz_array_equiv
