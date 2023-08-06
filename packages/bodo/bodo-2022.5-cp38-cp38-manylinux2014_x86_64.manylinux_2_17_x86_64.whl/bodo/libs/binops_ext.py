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
        rjes__pfhzz = lhs.data if isinstance(lhs, SeriesType) else lhs
        yzkgk__ylxr = rhs.data if isinstance(rhs, SeriesType) else rhs
        if rjes__pfhzz in (bodo.pd_timestamp_type, bodo.pd_timedelta_type
            ) and yzkgk__ylxr.dtype in (bodo.datetime64ns, bodo.timedelta64ns):
            rjes__pfhzz = yzkgk__ylxr.dtype
        elif yzkgk__ylxr in (bodo.pd_timestamp_type, bodo.pd_timedelta_type
            ) and rjes__pfhzz.dtype in (bodo.datetime64ns, bodo.timedelta64ns):
            yzkgk__ylxr = rjes__pfhzz.dtype
        mqh__wmnr = rjes__pfhzz, yzkgk__ylxr
        dhh__bpquu = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            kdl__hsg = self.context.resolve_function_type(self.key,
                mqh__wmnr, {}).return_type
        except Exception as ofw__ojg:
            raise BodoError(dhh__bpquu)
        if is_overload_bool(kdl__hsg):
            raise BodoError(dhh__bpquu)
        qcce__mhhl = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        yvn__usdw = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        nvlo__duwqe = types.bool_
        leze__zydd = SeriesType(nvlo__duwqe, kdl__hsg, qcce__mhhl, yvn__usdw)
        return leze__zydd(*args)


def series_cmp_op_lower(op):

    def lower_impl(context, builder, sig, args):
        aia__zna = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if aia__zna is None:
            aia__zna = create_overload_cmp_operator(op)(*sig.args)
        return context.compile_internal(builder, aia__zna, sig, args)
    return lower_impl


class SeriesAndOrTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        lhs, rhs = args
        if not (isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType)):
            return
        rjes__pfhzz = lhs.data if isinstance(lhs, SeriesType) else lhs
        yzkgk__ylxr = rhs.data if isinstance(rhs, SeriesType) else rhs
        mqh__wmnr = rjes__pfhzz, yzkgk__ylxr
        dhh__bpquu = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            kdl__hsg = self.context.resolve_function_type(self.key,
                mqh__wmnr, {}).return_type
        except Exception as ctfuv__mqac:
            raise BodoError(dhh__bpquu)
        qcce__mhhl = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        yvn__usdw = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        nvlo__duwqe = kdl__hsg.dtype
        leze__zydd = SeriesType(nvlo__duwqe, kdl__hsg, qcce__mhhl, yvn__usdw)
        return leze__zydd(*args)


def lower_series_and_or(op):

    def lower_and_or_impl(context, builder, sig, args):
        aia__zna = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if aia__zna is None:
            lhs, rhs = sig.args
            if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType
                ):
                aia__zna = (bodo.hiframes.dataframe_impl.
                    create_binary_op_overload(op)(*sig.args))
        return context.compile_internal(builder, aia__zna, sig, args)
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
            aia__zna = (bodo.hiframes.datetime_timedelta_ext.
                create_cmp_op_overload(op))
            return aia__zna(lhs, rhs)
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
            aia__zna = (bodo.hiframes.datetime_timedelta_ext.
                pd_create_cmp_op_overload(op))
            return aia__zna(lhs, rhs)
        if cmp_timestamp_or_date(lhs, rhs):
            return (bodo.hiframes.pd_timestamp_ext.
                create_timestamp_cmp_op_overload(op)(lhs, rhs))
        if cmp_op_supported_by_numba(lhs, rhs):
            return
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_cmp_operator


def add_dt_td_and_dt_date(lhs, rhs):
    vyh__gjboo = lhs == datetime_timedelta_type and rhs == datetime_date_type
    hmmp__gqpu = rhs == datetime_timedelta_type and lhs == datetime_date_type
    return vyh__gjboo or hmmp__gqpu


def add_timestamp(lhs, rhs):
    kttbd__jkvu = lhs == pd_timestamp_type and is_timedelta_type(rhs)
    uxqod__emz = is_timedelta_type(lhs) and rhs == pd_timestamp_type
    return kttbd__jkvu or uxqod__emz


def add_datetime_and_timedeltas(lhs, rhs):
    ivtim__bqbgg = [datetime_timedelta_type, pd_timedelta_type]
    cbk__dsth = [datetime_timedelta_type, pd_timedelta_type,
        datetime_datetime_type]
    uytea__klinn = lhs in ivtim__bqbgg and rhs in ivtim__bqbgg
    fzxa__ovpk = (lhs == datetime_datetime_type and rhs in ivtim__bqbgg or 
        rhs == datetime_datetime_type and lhs in ivtim__bqbgg)
    return uytea__klinn or fzxa__ovpk


def mul_string_arr_and_int(lhs, rhs):
    yzkgk__ylxr = isinstance(lhs, types.Integer) and is_str_arr_type(rhs)
    rjes__pfhzz = is_str_arr_type(lhs) and isinstance(rhs, types.Integer)
    return yzkgk__ylxr or rjes__pfhzz


def mul_timedelta_and_int(lhs, rhs):
    vyh__gjboo = lhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(rhs, types.Integer)
    hmmp__gqpu = rhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(lhs, types.Integer)
    return vyh__gjboo or hmmp__gqpu


def mul_date_offset_and_int(lhs, rhs):
    vdl__pkcv = lhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(rhs, types.Integer)
    gqj__vokrq = rhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(lhs, types.Integer)
    return vdl__pkcv or gqj__vokrq


def sub_offset_to_datetime_or_timestamp(lhs, rhs):
    dhfr__sqz = [datetime_datetime_type, pd_timestamp_type, datetime_date_type]
    gxeg__jastd = [date_offset_type, month_begin_type, month_end_type,
        week_type]
    return rhs in gxeg__jastd and lhs in dhfr__sqz


def sub_dt_index_and_timestamp(lhs, rhs):
    iab__zvs = isinstance(lhs, DatetimeIndexType) and rhs == pd_timestamp_type
    wkout__fofp = isinstance(rhs, DatetimeIndexType
        ) and lhs == pd_timestamp_type
    return iab__zvs or wkout__fofp


def sub_dt_or_td(lhs, rhs):
    ygtjs__tbpcn = lhs == datetime_date_type and rhs == datetime_timedelta_type
    mtpj__uikg = lhs == datetime_date_type and rhs == datetime_date_type
    asgn__itlh = (lhs == datetime_date_array_type and rhs ==
        datetime_timedelta_type)
    return ygtjs__tbpcn or mtpj__uikg or asgn__itlh


def sub_datetime_and_timedeltas(lhs, rhs):
    pgozt__lcouz = (is_timedelta_type(lhs) or lhs == datetime_datetime_type
        ) and is_timedelta_type(rhs)
    hytt__njf = (lhs == datetime_timedelta_array_type and rhs ==
        datetime_timedelta_type)
    return pgozt__lcouz or hytt__njf


def div_timedelta_and_int(lhs, rhs):
    uytea__klinn = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    xxcxo__uyf = lhs == pd_timedelta_type and isinstance(rhs, types.Integer)
    return uytea__klinn or xxcxo__uyf


def div_datetime_timedelta(lhs, rhs):
    uytea__klinn = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    xxcxo__uyf = lhs == datetime_timedelta_type and rhs == types.int64
    return uytea__klinn or xxcxo__uyf


def mod_timedeltas(lhs, rhs):
    ithqp__hrsgi = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    gwynt__tpl = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    return ithqp__hrsgi or gwynt__tpl


def cmp_dt_index_to_string(lhs, rhs):
    iab__zvs = isinstance(lhs, DatetimeIndexType) and types.unliteral(rhs
        ) == string_type
    wkout__fofp = isinstance(rhs, DatetimeIndexType) and types.unliteral(lhs
        ) == string_type
    return iab__zvs or wkout__fofp


def cmp_timestamp_or_date(lhs, rhs):
    nmew__ebv = (lhs == pd_timestamp_type and rhs == bodo.hiframes.
        datetime_date_ext.datetime_date_type)
    viee__kky = (lhs == bodo.hiframes.datetime_date_ext.datetime_date_type and
        rhs == pd_timestamp_type)
    cwcu__corix = lhs == pd_timestamp_type and rhs == pd_timestamp_type
    ewzs__gvr = lhs == pd_timestamp_type and rhs == bodo.datetime64ns
    bkxvq__srdt = rhs == pd_timestamp_type and lhs == bodo.datetime64ns
    return nmew__ebv or viee__kky or cwcu__corix or ewzs__gvr or bkxvq__srdt


def cmp_timeseries(lhs, rhs):
    zifey__byudr = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (
        bodo.utils.typing.is_overload_constant_str(lhs) or lhs == bodo.libs
        .str_ext.string_type or lhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_type)
    fsor__wjlpr = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (bodo
        .utils.typing.is_overload_constant_str(rhs) or rhs == bodo.libs.
        str_ext.string_type or rhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_type)
    rwn__ofehf = zifey__byudr or fsor__wjlpr
    vwedh__iut = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    nnydr__dgtm = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    igisa__fwd = vwedh__iut or nnydr__dgtm
    return rwn__ofehf or igisa__fwd


def cmp_timedeltas(lhs, rhs):
    uytea__klinn = [pd_timedelta_type, bodo.timedelta64ns]
    return lhs in uytea__klinn and rhs in uytea__klinn


def operand_is_index(operand):
    return is_index_type(operand) or isinstance(operand, HeterogeneousIndexType
        )


def helper_time_series_checks(operand):
    nfwqr__loyv = bodo.hiframes.pd_series_ext.is_dt64_series_typ(operand
        ) or bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(operand
        ) or operand in [datetime_timedelta_type, datetime_datetime_type,
        pd_timestamp_type]
    return nfwqr__loyv


def binary_array_cmp(lhs, rhs):
    return lhs == binary_array_type and rhs in [bytes_type, binary_array_type
        ] or lhs in [bytes_type, binary_array_type
        ] and rhs == binary_array_type


def can_cmp_date_datetime(lhs, rhs, op):
    return op in (operator.eq, operator.ne) and (lhs == datetime_date_type and
        rhs == datetime_datetime_type or lhs == datetime_datetime_type and 
        rhs == datetime_date_type)


def time_series_operation(lhs, rhs):
    shepg__litwe = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == datetime_timedelta_type
    jktf__qcrw = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == datetime_timedelta_type
    cucfg__emb = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
        ) and helper_time_series_checks(rhs)
    rvzm__hmswb = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
        ) and helper_time_series_checks(lhs)
    return shepg__litwe or jktf__qcrw or cucfg__emb or rvzm__hmswb


def args_td_and_int_array(lhs, rhs):
    irg__yrpr = (isinstance(lhs, IntegerArrayType) or isinstance(lhs, types
        .Array) and isinstance(lhs.dtype, types.Integer)) or (isinstance(
        rhs, IntegerArrayType) or isinstance(rhs, types.Array) and
        isinstance(rhs.dtype, types.Integer))
    vag__kqbtc = lhs in [pd_timedelta_type] or rhs in [pd_timedelta_type]
    return irg__yrpr and vag__kqbtc


def arith_op_supported_by_numba(op, lhs, rhs):
    if op == operator.mul:
        hmmp__gqpu = isinstance(lhs, (types.Integer, types.Float)
            ) and isinstance(rhs, types.NPTimedelta)
        vyh__gjboo = isinstance(rhs, (types.Integer, types.Float)
            ) and isinstance(lhs, types.NPTimedelta)
        zknv__ietno = hmmp__gqpu or vyh__gjboo
        igas__wdn = isinstance(rhs, types.UnicodeType) and isinstance(lhs,
            types.Integer)
        eqsr__vqqr = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.Integer)
        yvoo__piw = igas__wdn or eqsr__vqqr
        nzvl__bkqj = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        wori__drrpj = isinstance(lhs, types.Float) and isinstance(rhs,
            types.Float)
        bwts__suzqp = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        jeew__sohd = nzvl__bkqj or wori__drrpj or bwts__suzqp
        cjegr__xfano = isinstance(lhs, types.List) and isinstance(rhs,
            types.Integer) or isinstance(lhs, types.Integer) and isinstance(rhs
            , types.List)
        tys = types.UnicodeCharSeq, types.CharSeq, types.Bytes
        brvb__dlt = isinstance(lhs, tys) or isinstance(rhs, tys)
        qrdp__bnkni = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        return (zknv__ietno or yvoo__piw or jeew__sohd or cjegr__xfano or
            brvb__dlt or qrdp__bnkni)
    if op == operator.pow:
        ohg__htoa = isinstance(lhs, types.Integer) and isinstance(rhs, (
            types.IntegerLiteral, types.Integer))
        dncfi__jphyh = isinstance(lhs, types.Float) and isinstance(rhs, (
            types.IntegerLiteral, types.Float, types.Integer) or rhs in
            types.unsigned_domain or rhs in types.signed_domain)
        bwts__suzqp = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        qrdp__bnkni = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        return ohg__htoa or dncfi__jphyh or bwts__suzqp or qrdp__bnkni
    if op == operator.floordiv:
        wori__drrpj = lhs in types.real_domain and rhs in types.real_domain
        nzvl__bkqj = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        apfr__cag = isinstance(lhs, types.Float) and isinstance(rhs, types.
            Float)
        uytea__klinn = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        qrdp__bnkni = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        return (wori__drrpj or nzvl__bkqj or apfr__cag or uytea__klinn or
            qrdp__bnkni)
    if op == operator.truediv:
        oxokz__rdxjz = lhs in machine_ints and rhs in machine_ints
        wori__drrpj = lhs in types.real_domain and rhs in types.real_domain
        bwts__suzqp = (lhs in types.complex_domain and rhs in types.
            complex_domain)
        nzvl__bkqj = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        apfr__cag = isinstance(lhs, types.Float) and isinstance(rhs, types.
            Float)
        cqysc__slw = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        uytea__klinn = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        qrdp__bnkni = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        return (oxokz__rdxjz or wori__drrpj or bwts__suzqp or nzvl__bkqj or
            apfr__cag or cqysc__slw or uytea__klinn or qrdp__bnkni)
    if op == operator.mod:
        oxokz__rdxjz = lhs in machine_ints and rhs in machine_ints
        wori__drrpj = lhs in types.real_domain and rhs in types.real_domain
        nzvl__bkqj = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        apfr__cag = isinstance(lhs, types.Float) and isinstance(rhs, types.
            Float)
        qrdp__bnkni = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        return (oxokz__rdxjz or wori__drrpj or nzvl__bkqj or apfr__cag or
            qrdp__bnkni)
    if op == operator.add or op == operator.sub:
        zknv__ietno = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            types.NPTimedelta)
        hel__pfs = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPDatetime)
        yah__hhlws = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPTimedelta)
        ozf__ihow = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
        nzvl__bkqj = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        wori__drrpj = isinstance(lhs, types.Float) and isinstance(rhs,
            types.Float)
        bwts__suzqp = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        jeew__sohd = nzvl__bkqj or wori__drrpj or bwts__suzqp
        qrdp__bnkni = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        dne__djdo = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
            types.BaseTuple)
        cjegr__xfano = isinstance(lhs, types.List) and isinstance(rhs,
            types.List)
        gfcfl__eswz = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeType)
        btyq__rbs = isinstance(rhs, types.UnicodeCharSeq) and isinstance(lhs,
            types.UnicodeType)
        radij__wjwxt = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs
            , types.UnicodeCharSeq)
        jxhny__vtzp = isinstance(lhs, (types.CharSeq, types.Bytes)
            ) and isinstance(rhs, (types.CharSeq, types.Bytes))
        sqgr__tlkj = gfcfl__eswz or btyq__rbs or radij__wjwxt or jxhny__vtzp
        yvoo__piw = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeType)
        xnrhf__udq = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeCharSeq)
        prxcc__detfa = yvoo__piw or xnrhf__udq
        gjjm__usab = lhs == types.NPTimedelta and rhs == types.NPDatetime
        xusq__izhrg = (dne__djdo or cjegr__xfano or sqgr__tlkj or
            prxcc__detfa or gjjm__usab)
        qvr__nafeo = op == operator.add and xusq__izhrg
        return (zknv__ietno or hel__pfs or yah__hhlws or ozf__ihow or
            jeew__sohd or qrdp__bnkni or qvr__nafeo)


def cmp_op_supported_by_numba(lhs, rhs):
    qrdp__bnkni = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
    cjegr__xfano = isinstance(lhs, types.ListType) and isinstance(rhs,
        types.ListType)
    zknv__ietno = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
        types.NPTimedelta)
    jon__ymmx = isinstance(lhs, types.NPDatetime) and isinstance(rhs, types
        .NPDatetime)
    unicode_types = (types.UnicodeType, types.StringLiteral, types.CharSeq,
        types.Bytes, types.UnicodeCharSeq)
    yvoo__piw = isinstance(lhs, unicode_types) and isinstance(rhs,
        unicode_types)
    dne__djdo = isinstance(lhs, types.BaseTuple) and isinstance(rhs, types.
        BaseTuple)
    ozf__ihow = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
    jeew__sohd = isinstance(lhs, types.Number) and isinstance(rhs, types.Number
        )
    hmag__txfcx = isinstance(lhs, types.Boolean) and isinstance(rhs, types.
        Boolean)
    pyawe__tcvgh = isinstance(lhs, types.NoneType) or isinstance(rhs, types
        .NoneType)
    zfix__kccxo = isinstance(lhs, types.DictType) and isinstance(rhs, types
        .DictType)
    ysa__wgobn = isinstance(lhs, types.EnumMember) and isinstance(rhs,
        types.EnumMember)
    lksn__fnmr = isinstance(lhs, types.Literal) and isinstance(rhs, types.
        Literal)
    return (cjegr__xfano or zknv__ietno or jon__ymmx or yvoo__piw or
        dne__djdo or ozf__ihow or jeew__sohd or hmag__txfcx or pyawe__tcvgh or
        zfix__kccxo or qrdp__bnkni or ysa__wgobn or lksn__fnmr)


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
        azs__shsu = create_overload_cmp_operator(op)
        overload(op, no_unliteral=True)(azs__shsu)


_install_cmp_ops()


def install_arith_ops():
    for op in (operator.add, operator.sub, operator.mul, operator.truediv,
        operator.floordiv, operator.mod, operator.pow):
        azs__shsu = create_overload_arith_op(op)
        overload(op, no_unliteral=True)(azs__shsu)


install_arith_ops()
