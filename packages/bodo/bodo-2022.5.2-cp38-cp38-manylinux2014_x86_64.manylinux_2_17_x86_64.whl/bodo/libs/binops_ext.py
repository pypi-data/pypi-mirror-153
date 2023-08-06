""" Implementation of binary operators for the different types.
    Currently implemented operators:
        arith: add, sub, mul, truediv, floordiv, mod, pow
        cmp: lt, le, eq, ne, ge, gt
"""
import operator
import numba
from numba.core import types
from numba.core.imputils import lower_builtin
from numba.core.typing.builtins import machine_ints
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import overload
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type, datetime_date_type, datetime_timedelta_type
from bodo.hiframes.datetime_timedelta_ext import datetime_datetime_type, datetime_timedelta_array_type, pd_timedelta_type
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import DatetimeIndexType, HeterogeneousIndexType, is_index_type
from bodo.hiframes.pd_offsets_ext import date_offset_type, month_begin_type, month_end_type, week_type
from bodo.hiframes.pd_timestamp_ext import pd_timestamp_type
from bodo.hiframes.series_impl import SeriesType
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import Decimal128Type
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_ext import string_type
from bodo.utils.typing import BodoError, is_overload_bool, is_str_arr_type, is_timedelta_type


class SeriesCmpOpTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        lhs, rhs = args
        if cmp_timeseries(lhs, rhs) or (isinstance(lhs, DataFrameType) or
            isinstance(rhs, DataFrameType)) or not (isinstance(lhs,
            SeriesType) or isinstance(rhs, SeriesType)):
            return
        gkjr__kjqzq = lhs.data if isinstance(lhs, SeriesType) else lhs
        coeku__lwgpp = rhs.data if isinstance(rhs, SeriesType) else rhs
        if gkjr__kjqzq in (bodo.pd_timestamp_type, bodo.pd_timedelta_type
            ) and coeku__lwgpp.dtype in (bodo.datetime64ns, bodo.timedelta64ns
            ):
            gkjr__kjqzq = coeku__lwgpp.dtype
        elif coeku__lwgpp in (bodo.pd_timestamp_type, bodo.pd_timedelta_type
            ) and gkjr__kjqzq.dtype in (bodo.datetime64ns, bodo.timedelta64ns):
            coeku__lwgpp = gkjr__kjqzq.dtype
        peq__bdu = gkjr__kjqzq, coeku__lwgpp
        ogqp__ljd = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            wcik__awwdf = self.context.resolve_function_type(self.key,
                peq__bdu, {}).return_type
        except Exception as cezd__lbxbo:
            raise BodoError(ogqp__ljd)
        if is_overload_bool(wcik__awwdf):
            raise BodoError(ogqp__ljd)
        nac__lfqf = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        efpi__lndk = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        imjb__ovd = types.bool_
        kno__vfzy = SeriesType(imjb__ovd, wcik__awwdf, nac__lfqf, efpi__lndk)
        return kno__vfzy(*args)


def series_cmp_op_lower(op):

    def lower_impl(context, builder, sig, args):
        odlyo__xpuj = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if odlyo__xpuj is None:
            odlyo__xpuj = create_overload_cmp_operator(op)(*sig.args)
        return context.compile_internal(builder, odlyo__xpuj, sig, args)
    return lower_impl


class SeriesAndOrTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        lhs, rhs = args
        if not (isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType)):
            return
        gkjr__kjqzq = lhs.data if isinstance(lhs, SeriesType) else lhs
        coeku__lwgpp = rhs.data if isinstance(rhs, SeriesType) else rhs
        peq__bdu = gkjr__kjqzq, coeku__lwgpp
        ogqp__ljd = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            wcik__awwdf = self.context.resolve_function_type(self.key,
                peq__bdu, {}).return_type
        except Exception as ryemy__oyn:
            raise BodoError(ogqp__ljd)
        nac__lfqf = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        efpi__lndk = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        imjb__ovd = wcik__awwdf.dtype
        kno__vfzy = SeriesType(imjb__ovd, wcik__awwdf, nac__lfqf, efpi__lndk)
        return kno__vfzy(*args)


def lower_series_and_or(op):

    def lower_and_or_impl(context, builder, sig, args):
        odlyo__xpuj = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if odlyo__xpuj is None:
            lhs, rhs = sig.args
            if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType
                ):
                odlyo__xpuj = (bodo.hiframes.dataframe_impl.
                    create_binary_op_overload(op)(*sig.args))
        return context.compile_internal(builder, odlyo__xpuj, sig, args)
    return lower_and_or_impl


def overload_add_operator_scalars(lhs, rhs):
    if lhs == week_type or rhs == week_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_week_offset_type(lhs, rhs))
    if lhs == month_begin_type or rhs == month_begin_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_month_begin_offset_type(lhs, rhs))
    if lhs == month_end_type or rhs == month_end_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_month_end_offset_type(lhs, rhs))
    if lhs == date_offset_type or rhs == date_offset_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_date_offset_type(lhs, rhs))
    if add_timestamp(lhs, rhs):
        return bodo.hiframes.pd_timestamp_ext.overload_add_operator_timestamp(
            lhs, rhs)
    if add_dt_td_and_dt_date(lhs, rhs):
        return (bodo.hiframes.datetime_date_ext.
            overload_add_operator_datetime_date(lhs, rhs))
    if add_datetime_and_timedeltas(lhs, rhs):
        return (bodo.hiframes.datetime_timedelta_ext.
            overload_add_operator_datetime_timedelta(lhs, rhs))
    raise_error_if_not_numba_supported(operator.add, lhs, rhs)


def overload_sub_operator_scalars(lhs, rhs):
    if sub_offset_to_datetime_or_timestamp(lhs, rhs):
        return bodo.hiframes.pd_offsets_ext.overload_sub_operator_offsets(lhs,
            rhs)
    if lhs == pd_timestamp_type and rhs in [pd_timestamp_type,
        datetime_timedelta_type, pd_timedelta_type]:
        return bodo.hiframes.pd_timestamp_ext.overload_sub_operator_timestamp(
            lhs, rhs)
    if sub_dt_or_td(lhs, rhs):
        return (bodo.hiframes.datetime_date_ext.
            overload_sub_operator_datetime_date(lhs, rhs))
    if sub_datetime_and_timedeltas(lhs, rhs):
        return (bodo.hiframes.datetime_timedelta_ext.
            overload_sub_operator_datetime_timedelta(lhs, rhs))
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:
        return (bodo.hiframes.datetime_datetime_ext.
            overload_sub_operator_datetime_datetime(lhs, rhs))
    raise_error_if_not_numba_supported(operator.sub, lhs, rhs)


def create_overload_arith_op(op):

    def overload_arith_operator(lhs, rhs):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(lhs,
            f'{op} operator')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(rhs,
            f'{op} operator')
        if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType):
            return bodo.hiframes.dataframe_impl.create_binary_op_overload(op)(
                lhs, rhs)
        if time_series_operation(lhs, rhs) and op in [operator.add,
            operator.sub]:
            return bodo.hiframes.series_dt_impl.create_bin_op_overload(op)(lhs,
                rhs)
        if isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType):
            return bodo.hiframes.series_impl.create_binary_op_overload(op)(lhs,
                rhs)
        if sub_dt_index_and_timestamp(lhs, rhs) and op == operator.sub:
            return (bodo.hiframes.pd_index_ext.
                overload_sub_operator_datetime_index(lhs, rhs))
        if operand_is_index(lhs) or operand_is_index(rhs):
            return bodo.hiframes.pd_index_ext.create_binary_op_overload(op)(lhs
                , rhs)
        if args_td_and_int_array(lhs, rhs):
            return bodo.libs.int_arr_ext.get_int_array_op_pd_td(op)(lhs, rhs)
        if isinstance(lhs, IntegerArrayType) or isinstance(rhs,
            IntegerArrayType):
            return bodo.libs.int_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if lhs == boolean_array or rhs == boolean_array:
            return bodo.libs.bool_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if op == operator.add and (is_str_arr_type(lhs) or types.unliteral(
            lhs) == string_type):
            return bodo.libs.str_arr_ext.overload_add_operator_string_array(lhs
                , rhs)
        if op == operator.add:
            return overload_add_operator_scalars(lhs, rhs)
        if op == operator.sub:
            return overload_sub_operator_scalars(lhs, rhs)
        if op == operator.mul:
            if mul_timedelta_and_int(lhs, rhs):
                return (bodo.hiframes.datetime_timedelta_ext.
                    overload_mul_operator_timedelta(lhs, rhs))
            if mul_string_arr_and_int(lhs, rhs):
                return bodo.libs.str_arr_ext.overload_mul_operator_str_arr(lhs,
                    rhs)
            if mul_date_offset_and_int(lhs, rhs):
                return (bodo.hiframes.pd_offsets_ext.
                    overload_mul_date_offset_types(lhs, rhs))
            raise_error_if_not_numba_supported(op, lhs, rhs)
        if op in [operator.truediv, operator.floordiv]:
            if div_timedelta_and_int(lhs, rhs):
                if op == operator.truediv:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_truediv_operator_pd_timedelta(lhs, rhs))
                else:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_floordiv_operator_pd_timedelta(lhs, rhs))
            if div_datetime_timedelta(lhs, rhs):
                if op == operator.truediv:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_truediv_operator_dt_timedelta(lhs, rhs))
                else:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_floordiv_operator_dt_timedelta(lhs, rhs))
            raise_error_if_not_numba_supported(op, lhs, rhs)
        if op == operator.mod:
            if mod_timedeltas(lhs, rhs):
                return (bodo.hiframes.datetime_timedelta_ext.
                    overload_mod_operator_timedeltas(lhs, rhs))
            raise_error_if_not_numba_supported(op, lhs, rhs)
        if op == operator.pow:
            raise_error_if_not_numba_supported(op, lhs, rhs)
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_arith_operator


def create_overload_cmp_operator(op):

    def overload_cmp_operator(lhs, rhs):
        if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType):
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(lhs,
                f'{op} operator')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(rhs,
                f'{op} operator')
            return bodo.hiframes.dataframe_impl.create_binary_op_overload(op)(
                lhs, rhs)
        if cmp_timeseries(lhs, rhs):
            return bodo.hiframes.series_dt_impl.create_cmp_op_overload(op)(lhs,
                rhs)
        if isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType):
            return
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(lhs,
            f'{op} operator')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(rhs,
            f'{op} operator')
        if lhs == datetime_date_array_type or rhs == datetime_date_array_type:
            return bodo.hiframes.datetime_date_ext.create_cmp_op_overload_arr(
                op)(lhs, rhs)
        if (lhs == datetime_timedelta_array_type or rhs ==
            datetime_timedelta_array_type):
            odlyo__xpuj = (bodo.hiframes.datetime_timedelta_ext.
                create_cmp_op_overload(op))
            return odlyo__xpuj(lhs, rhs)
        if is_str_arr_type(lhs) or is_str_arr_type(rhs):
            return bodo.libs.str_arr_ext.create_binary_op_overload(op)(lhs, rhs
                )
        if isinstance(lhs, Decimal128Type) and isinstance(rhs, Decimal128Type):
            return bodo.libs.decimal_arr_ext.decimal_create_cmp_op_overload(op
                )(lhs, rhs)
        if lhs == boolean_array or rhs == boolean_array:
            return bodo.libs.bool_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if isinstance(lhs, IntegerArrayType) or isinstance(rhs,
            IntegerArrayType):
            return bodo.libs.int_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if binary_array_cmp(lhs, rhs):
            return bodo.libs.binary_arr_ext.create_binary_cmp_op_overload(op)(
                lhs, rhs)
        if cmp_dt_index_to_string(lhs, rhs):
            return bodo.hiframes.pd_index_ext.overload_binop_dti_str(op)(lhs,
                rhs)
        if operand_is_index(lhs) or operand_is_index(rhs):
            return bodo.hiframes.pd_index_ext.create_binary_op_overload(op)(lhs
                , rhs)
        if lhs == datetime_date_type and rhs == datetime_date_type:
            return bodo.hiframes.datetime_date_ext.create_cmp_op_overload(op)(
                lhs, rhs)
        if can_cmp_date_datetime(lhs, rhs, op):
            return (bodo.hiframes.datetime_date_ext.
                create_datetime_date_cmp_op_overload(op)(lhs, rhs))
        if lhs == datetime_datetime_type and rhs == datetime_datetime_type:
            return bodo.hiframes.datetime_datetime_ext.create_cmp_op_overload(
                op)(lhs, rhs)
        if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:
            return bodo.hiframes.datetime_timedelta_ext.create_cmp_op_overload(
                op)(lhs, rhs)
        if cmp_timedeltas(lhs, rhs):
            odlyo__xpuj = (bodo.hiframes.datetime_timedelta_ext.
                pd_create_cmp_op_overload(op))
            return odlyo__xpuj(lhs, rhs)
        if cmp_timestamp_or_date(lhs, rhs):
            return (bodo.hiframes.pd_timestamp_ext.
                create_timestamp_cmp_op_overload(op)(lhs, rhs))
        if cmp_op_supported_by_numba(lhs, rhs):
            return
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_cmp_operator


def add_dt_td_and_dt_date(lhs, rhs):
    dvse__ypsta = lhs == datetime_timedelta_type and rhs == datetime_date_type
    szj__reg = rhs == datetime_timedelta_type and lhs == datetime_date_type
    return dvse__ypsta or szj__reg


def add_timestamp(lhs, rhs):
    mzkjh__oapx = lhs == pd_timestamp_type and is_timedelta_type(rhs)
    ggrtw__nlr = is_timedelta_type(lhs) and rhs == pd_timestamp_type
    return mzkjh__oapx or ggrtw__nlr


def add_datetime_and_timedeltas(lhs, rhs):
    uzfqk__ewpn = [datetime_timedelta_type, pd_timedelta_type]
    riixu__hzker = [datetime_timedelta_type, pd_timedelta_type,
        datetime_datetime_type]
    nqrm__trlbd = lhs in uzfqk__ewpn and rhs in uzfqk__ewpn
    gbgb__wfmec = (lhs == datetime_datetime_type and rhs in uzfqk__ewpn or 
        rhs == datetime_datetime_type and lhs in uzfqk__ewpn)
    return nqrm__trlbd or gbgb__wfmec


def mul_string_arr_and_int(lhs, rhs):
    coeku__lwgpp = isinstance(lhs, types.Integer) and is_str_arr_type(rhs)
    gkjr__kjqzq = is_str_arr_type(lhs) and isinstance(rhs, types.Integer)
    return coeku__lwgpp or gkjr__kjqzq


def mul_timedelta_and_int(lhs, rhs):
    dvse__ypsta = lhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(rhs, types.Integer)
    szj__reg = rhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(lhs, types.Integer)
    return dvse__ypsta or szj__reg


def mul_date_offset_and_int(lhs, rhs):
    ebhu__dsgja = lhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(rhs, types.Integer)
    vnzgr__keees = rhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(lhs, types.Integer)
    return ebhu__dsgja or vnzgr__keees


def sub_offset_to_datetime_or_timestamp(lhs, rhs):
    jkb__qrf = [datetime_datetime_type, pd_timestamp_type, datetime_date_type]
    cqfbb__txw = [date_offset_type, month_begin_type, month_end_type, week_type
        ]
    return rhs in cqfbb__txw and lhs in jkb__qrf


def sub_dt_index_and_timestamp(lhs, rhs):
    qwmj__grch = isinstance(lhs, DatetimeIndexType
        ) and rhs == pd_timestamp_type
    vdkk__yxe = isinstance(rhs, DatetimeIndexType) and lhs == pd_timestamp_type
    return qwmj__grch or vdkk__yxe


def sub_dt_or_td(lhs, rhs):
    nsu__bepa = lhs == datetime_date_type and rhs == datetime_timedelta_type
    bqg__zmq = lhs == datetime_date_type and rhs == datetime_date_type
    hwini__sdy = (lhs == datetime_date_array_type and rhs ==
        datetime_timedelta_type)
    return nsu__bepa or bqg__zmq or hwini__sdy


def sub_datetime_and_timedeltas(lhs, rhs):
    mwlxe__obsx = (is_timedelta_type(lhs) or lhs == datetime_datetime_type
        ) and is_timedelta_type(rhs)
    sytii__dxpmg = (lhs == datetime_timedelta_array_type and rhs ==
        datetime_timedelta_type)
    return mwlxe__obsx or sytii__dxpmg


def div_timedelta_and_int(lhs, rhs):
    nqrm__trlbd = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    lxgum__ufow = lhs == pd_timedelta_type and isinstance(rhs, types.Integer)
    return nqrm__trlbd or lxgum__ufow


def div_datetime_timedelta(lhs, rhs):
    nqrm__trlbd = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    lxgum__ufow = lhs == datetime_timedelta_type and rhs == types.int64
    return nqrm__trlbd or lxgum__ufow


def mod_timedeltas(lhs, rhs):
    ekeg__shu = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    gkpxl__aoq = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    return ekeg__shu or gkpxl__aoq


def cmp_dt_index_to_string(lhs, rhs):
    qwmj__grch = isinstance(lhs, DatetimeIndexType) and types.unliteral(rhs
        ) == string_type
    vdkk__yxe = isinstance(rhs, DatetimeIndexType) and types.unliteral(lhs
        ) == string_type
    return qwmj__grch or vdkk__yxe


def cmp_timestamp_or_date(lhs, rhs):
    kek__lzass = (lhs == pd_timestamp_type and rhs == bodo.hiframes.
        datetime_date_ext.datetime_date_type)
    fbwof__vogkg = (lhs == bodo.hiframes.datetime_date_ext.
        datetime_date_type and rhs == pd_timestamp_type)
    ohso__yshpv = lhs == pd_timestamp_type and rhs == pd_timestamp_type
    pif__maq = lhs == pd_timestamp_type and rhs == bodo.datetime64ns
    lhfm__nwvgy = rhs == pd_timestamp_type and lhs == bodo.datetime64ns
    return kek__lzass or fbwof__vogkg or ohso__yshpv or pif__maq or lhfm__nwvgy


def cmp_timeseries(lhs, rhs):
    axpo__wul = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (bodo
        .utils.typing.is_overload_constant_str(lhs) or lhs == bodo.libs.
        str_ext.string_type or lhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_type)
    opet__tangx = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (bodo
        .utils.typing.is_overload_constant_str(rhs) or rhs == bodo.libs.
        str_ext.string_type or rhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_type)
    rgbfn__ocu = axpo__wul or opet__tangx
    lfad__dcn = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    yrl__qjy = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    cbzuh__ddcs = lfad__dcn or yrl__qjy
    return rgbfn__ocu or cbzuh__ddcs


def cmp_timedeltas(lhs, rhs):
    nqrm__trlbd = [pd_timedelta_type, bodo.timedelta64ns]
    return lhs in nqrm__trlbd and rhs in nqrm__trlbd


def operand_is_index(operand):
    return is_index_type(operand) or isinstance(operand, HeterogeneousIndexType
        )


def helper_time_series_checks(operand):
    qyfwf__rnjd = bodo.hiframes.pd_series_ext.is_dt64_series_typ(operand
        ) or bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(operand
        ) or operand in [datetime_timedelta_type, datetime_datetime_type,
        pd_timestamp_type]
    return qyfwf__rnjd


def binary_array_cmp(lhs, rhs):
    return lhs == binary_array_type and rhs in [bytes_type, binary_array_type
        ] or lhs in [bytes_type, binary_array_type
        ] and rhs == binary_array_type


def can_cmp_date_datetime(lhs, rhs, op):
    return op in (operator.eq, operator.ne) and (lhs == datetime_date_type and
        rhs == datetime_datetime_type or lhs == datetime_datetime_type and 
        rhs == datetime_date_type)


def time_series_operation(lhs, rhs):
    mbl__ffbj = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == datetime_timedelta_type
    giv__wdquz = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == datetime_timedelta_type
    zgv__mqoft = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
        ) and helper_time_series_checks(rhs)
    hvitf__xxwkk = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
        ) and helper_time_series_checks(lhs)
    return mbl__ffbj or giv__wdquz or zgv__mqoft or hvitf__xxwkk


def args_td_and_int_array(lhs, rhs):
    ivud__lmwf = (isinstance(lhs, IntegerArrayType) or isinstance(lhs,
        types.Array) and isinstance(lhs.dtype, types.Integer)) or (isinstance
        (rhs, IntegerArrayType) or isinstance(rhs, types.Array) and
        isinstance(rhs.dtype, types.Integer))
    txkq__myv = lhs in [pd_timedelta_type] or rhs in [pd_timedelta_type]
    return ivud__lmwf and txkq__myv


def arith_op_supported_by_numba(op, lhs, rhs):
    if op == operator.mul:
        szj__reg = isinstance(lhs, (types.Integer, types.Float)
            ) and isinstance(rhs, types.NPTimedelta)
        dvse__ypsta = isinstance(rhs, (types.Integer, types.Float)
            ) and isinstance(lhs, types.NPTimedelta)
        ckyz__zhzzn = szj__reg or dvse__ypsta
        qxnr__ndm = isinstance(rhs, types.UnicodeType) and isinstance(lhs,
            types.Integer)
        lggl__nho = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.Integer)
        dnkvy__ajy = qxnr__ndm or lggl__nho
        agry__ukrz = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        wxoq__wrc = isinstance(lhs, types.Float) and isinstance(rhs, types.
            Float)
        srhjz__ahwl = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        rzle__jwb = agry__ukrz or wxoq__wrc or srhjz__ahwl
        sluyz__bmf = isinstance(lhs, types.List) and isinstance(rhs, types.
            Integer) or isinstance(lhs, types.Integer) and isinstance(rhs,
            types.List)
        tys = types.UnicodeCharSeq, types.CharSeq, types.Bytes
        dgokw__kbjns = isinstance(lhs, tys) or isinstance(rhs, tys)
        uta__elqug = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return (ckyz__zhzzn or dnkvy__ajy or rzle__jwb or sluyz__bmf or
            dgokw__kbjns or uta__elqug)
    if op == operator.pow:
        yhdll__gyl = isinstance(lhs, types.Integer) and isinstance(rhs, (
            types.IntegerLiteral, types.Integer))
        rubvz__phy = isinstance(lhs, types.Float) and isinstance(rhs, (
            types.IntegerLiteral, types.Float, types.Integer) or rhs in
            types.unsigned_domain or rhs in types.signed_domain)
        srhjz__ahwl = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        uta__elqug = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return yhdll__gyl or rubvz__phy or srhjz__ahwl or uta__elqug
    if op == operator.floordiv:
        wxoq__wrc = lhs in types.real_domain and rhs in types.real_domain
        agry__ukrz = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        ncknq__clg = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        nqrm__trlbd = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        uta__elqug = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return (wxoq__wrc or agry__ukrz or ncknq__clg or nqrm__trlbd or
            uta__elqug)
    if op == operator.truediv:
        udnl__yncon = lhs in machine_ints and rhs in machine_ints
        wxoq__wrc = lhs in types.real_domain and rhs in types.real_domain
        srhjz__ahwl = (lhs in types.complex_domain and rhs in types.
            complex_domain)
        agry__ukrz = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        ncknq__clg = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        ujq__rvyz = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        nqrm__trlbd = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        uta__elqug = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return (udnl__yncon or wxoq__wrc or srhjz__ahwl or agry__ukrz or
            ncknq__clg or ujq__rvyz or nqrm__trlbd or uta__elqug)
    if op == operator.mod:
        udnl__yncon = lhs in machine_ints and rhs in machine_ints
        wxoq__wrc = lhs in types.real_domain and rhs in types.real_domain
        agry__ukrz = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        ncknq__clg = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        uta__elqug = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return (udnl__yncon or wxoq__wrc or agry__ukrz or ncknq__clg or
            uta__elqug)
    if op == operator.add or op == operator.sub:
        ckyz__zhzzn = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            types.NPTimedelta)
        bhaoz__xtq = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPDatetime)
        pxge__ayrff = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPTimedelta)
        nzgs__gtx = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
        agry__ukrz = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        wxoq__wrc = isinstance(lhs, types.Float) and isinstance(rhs, types.
            Float)
        srhjz__ahwl = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        rzle__jwb = agry__ukrz or wxoq__wrc or srhjz__ahwl
        uta__elqug = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        utcjv__pnife = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
            types.BaseTuple)
        sluyz__bmf = isinstance(lhs, types.List) and isinstance(rhs, types.List
            )
        wrh__gcao = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeType)
        wyc__rdk = isinstance(rhs, types.UnicodeCharSeq) and isinstance(lhs,
            types.UnicodeType)
        wyr__wgki = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeCharSeq)
        qrx__gfln = isinstance(lhs, (types.CharSeq, types.Bytes)
            ) and isinstance(rhs, (types.CharSeq, types.Bytes))
        jynpw__itzg = wrh__gcao or wyc__rdk or wyr__wgki or qrx__gfln
        dnkvy__ajy = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeType)
        ysoan__qbllp = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeCharSeq)
        yitu__vvn = dnkvy__ajy or ysoan__qbllp
        seu__azxkn = lhs == types.NPTimedelta and rhs == types.NPDatetime
        avlvo__ytm = (utcjv__pnife or sluyz__bmf or jynpw__itzg or
            yitu__vvn or seu__azxkn)
        rqqp__lrx = op == operator.add and avlvo__ytm
        return (ckyz__zhzzn or bhaoz__xtq or pxge__ayrff or nzgs__gtx or
            rzle__jwb or uta__elqug or rqqp__lrx)


def cmp_op_supported_by_numba(lhs, rhs):
    uta__elqug = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
    sluyz__bmf = isinstance(lhs, types.ListType) and isinstance(rhs, types.
        ListType)
    ckyz__zhzzn = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
        types.NPTimedelta)
    nzit__vgy = isinstance(lhs, types.NPDatetime) and isinstance(rhs, types
        .NPDatetime)
    unicode_types = (types.UnicodeType, types.StringLiteral, types.CharSeq,
        types.Bytes, types.UnicodeCharSeq)
    dnkvy__ajy = isinstance(lhs, unicode_types) and isinstance(rhs,
        unicode_types)
    utcjv__pnife = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
        types.BaseTuple)
    nzgs__gtx = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
    rzle__jwb = isinstance(lhs, types.Number) and isinstance(rhs, types.Number)
    lkti__nqmt = isinstance(lhs, types.Boolean) and isinstance(rhs, types.
        Boolean)
    ufva__zmrbo = isinstance(lhs, types.NoneType) or isinstance(rhs, types.
        NoneType)
    bfvyv__eggf = isinstance(lhs, types.DictType) and isinstance(rhs, types
        .DictType)
    cieo__bvm = isinstance(lhs, types.EnumMember) and isinstance(rhs, types
        .EnumMember)
    yht__ykut = isinstance(lhs, types.Literal) and isinstance(rhs, types.
        Literal)
    return (sluyz__bmf or ckyz__zhzzn or nzit__vgy or dnkvy__ajy or
        utcjv__pnife or nzgs__gtx or rzle__jwb or lkti__nqmt or ufva__zmrbo or
        bfvyv__eggf or uta__elqug or cieo__bvm or yht__ykut)


def raise_error_if_not_numba_supported(op, lhs, rhs):
    if arith_op_supported_by_numba(op, lhs, rhs):
        return
    raise BodoError(
        f'{op} operator not supported for data types {lhs} and {rhs}.')


def _install_series_and_or():
    for op in (operator.or_, operator.and_):
        infer_global(op)(SeriesAndOrTyper)
        lower_impl = lower_series_and_or(op)
        lower_builtin(op, SeriesType, SeriesType)(lower_impl)
        lower_builtin(op, SeriesType, types.Any)(lower_impl)
        lower_builtin(op, types.Any, SeriesType)(lower_impl)


_install_series_and_or()


def _install_cmp_ops():
    for op in (operator.lt, operator.eq, operator.ne, operator.ge, operator
        .gt, operator.le):
        infer_global(op)(SeriesCmpOpTemplate)
        lower_impl = series_cmp_op_lower(op)
        lower_builtin(op, SeriesType, SeriesType)(lower_impl)
        lower_builtin(op, SeriesType, types.Any)(lower_impl)
        lower_builtin(op, types.Any, SeriesType)(lower_impl)
        unmj__pcqql = create_overload_cmp_operator(op)
        overload(op, no_unliteral=True)(unmj__pcqql)


_install_cmp_ops()


def install_arith_ops():
    for op in (operator.add, operator.sub, operator.mul, operator.truediv,
        operator.floordiv, operator.mod, operator.pow):
        unmj__pcqql = create_overload_arith_op(op)
        overload(op, no_unliteral=True)(unmj__pcqql)


install_arith_ops()
