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
        oen__zxhc = lhs.data if isinstance(lhs, SeriesType) else lhs
        mmges__qusfi = rhs.data if isinstance(rhs, SeriesType) else rhs
        if oen__zxhc in (bodo.pd_timestamp_type, bodo.pd_timedelta_type
            ) and mmges__qusfi.dtype in (bodo.datetime64ns, bodo.timedelta64ns
            ):
            oen__zxhc = mmges__qusfi.dtype
        elif mmges__qusfi in (bodo.pd_timestamp_type, bodo.pd_timedelta_type
            ) and oen__zxhc.dtype in (bodo.datetime64ns, bodo.timedelta64ns):
            mmges__qusfi = oen__zxhc.dtype
        cxvi__ynnco = oen__zxhc, mmges__qusfi
        lhso__keys = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            etv__gaf = self.context.resolve_function_type(self.key,
                cxvi__ynnco, {}).return_type
        except Exception as qzdm__wicr:
            raise BodoError(lhso__keys)
        if is_overload_bool(etv__gaf):
            raise BodoError(lhso__keys)
        xpja__wgcmy = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        hkn__nkhg = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        qlie__mnlhe = types.bool_
        ptspk__ecd = SeriesType(qlie__mnlhe, etv__gaf, xpja__wgcmy, hkn__nkhg)
        return ptspk__ecd(*args)


def series_cmp_op_lower(op):

    def lower_impl(context, builder, sig, args):
        bqohm__jue = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if bqohm__jue is None:
            bqohm__jue = create_overload_cmp_operator(op)(*sig.args)
        return context.compile_internal(builder, bqohm__jue, sig, args)
    return lower_impl


class SeriesAndOrTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        lhs, rhs = args
        if not (isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType)):
            return
        oen__zxhc = lhs.data if isinstance(lhs, SeriesType) else lhs
        mmges__qusfi = rhs.data if isinstance(rhs, SeriesType) else rhs
        cxvi__ynnco = oen__zxhc, mmges__qusfi
        lhso__keys = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            etv__gaf = self.context.resolve_function_type(self.key,
                cxvi__ynnco, {}).return_type
        except Exception as gpx__krmwl:
            raise BodoError(lhso__keys)
        xpja__wgcmy = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        hkn__nkhg = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        qlie__mnlhe = etv__gaf.dtype
        ptspk__ecd = SeriesType(qlie__mnlhe, etv__gaf, xpja__wgcmy, hkn__nkhg)
        return ptspk__ecd(*args)


def lower_series_and_or(op):

    def lower_and_or_impl(context, builder, sig, args):
        bqohm__jue = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if bqohm__jue is None:
            lhs, rhs = sig.args
            if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType
                ):
                bqohm__jue = (bodo.hiframes.dataframe_impl.
                    create_binary_op_overload(op)(*sig.args))
        return context.compile_internal(builder, bqohm__jue, sig, args)
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
            bqohm__jue = (bodo.hiframes.datetime_timedelta_ext.
                create_cmp_op_overload(op))
            return bqohm__jue(lhs, rhs)
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
            bqohm__jue = (bodo.hiframes.datetime_timedelta_ext.
                pd_create_cmp_op_overload(op))
            return bqohm__jue(lhs, rhs)
        if cmp_timestamp_or_date(lhs, rhs):
            return (bodo.hiframes.pd_timestamp_ext.
                create_timestamp_cmp_op_overload(op)(lhs, rhs))
        if cmp_op_supported_by_numba(lhs, rhs):
            return
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_cmp_operator


def add_dt_td_and_dt_date(lhs, rhs):
    dfjt__ubtm = lhs == datetime_timedelta_type and rhs == datetime_date_type
    gxy__yag = rhs == datetime_timedelta_type and lhs == datetime_date_type
    return dfjt__ubtm or gxy__yag


def add_timestamp(lhs, rhs):
    zsvd__xsc = lhs == pd_timestamp_type and is_timedelta_type(rhs)
    fmsls__cwqk = is_timedelta_type(lhs) and rhs == pd_timestamp_type
    return zsvd__xsc or fmsls__cwqk


def add_datetime_and_timedeltas(lhs, rhs):
    jgz__ndybc = [datetime_timedelta_type, pd_timedelta_type]
    lcx__inm = [datetime_timedelta_type, pd_timedelta_type,
        datetime_datetime_type]
    emlvo__jyewz = lhs in jgz__ndybc and rhs in jgz__ndybc
    xojyq__hxfjz = (lhs == datetime_datetime_type and rhs in jgz__ndybc or 
        rhs == datetime_datetime_type and lhs in jgz__ndybc)
    return emlvo__jyewz or xojyq__hxfjz


def mul_string_arr_and_int(lhs, rhs):
    mmges__qusfi = isinstance(lhs, types.Integer) and is_str_arr_type(rhs)
    oen__zxhc = is_str_arr_type(lhs) and isinstance(rhs, types.Integer)
    return mmges__qusfi or oen__zxhc


def mul_timedelta_and_int(lhs, rhs):
    dfjt__ubtm = lhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(rhs, types.Integer)
    gxy__yag = rhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(lhs, types.Integer)
    return dfjt__ubtm or gxy__yag


def mul_date_offset_and_int(lhs, rhs):
    zbfj__uhc = lhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(rhs, types.Integer)
    xgfu__dapxv = rhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(lhs, types.Integer)
    return zbfj__uhc or xgfu__dapxv


def sub_offset_to_datetime_or_timestamp(lhs, rhs):
    hvea__whmqj = [datetime_datetime_type, pd_timestamp_type,
        datetime_date_type]
    rtvs__zqtza = [date_offset_type, month_begin_type, month_end_type,
        week_type]
    return rhs in rtvs__zqtza and lhs in hvea__whmqj


def sub_dt_index_and_timestamp(lhs, rhs):
    hds__erokh = isinstance(lhs, DatetimeIndexType
        ) and rhs == pd_timestamp_type
    xzlsf__ewp = isinstance(rhs, DatetimeIndexType
        ) and lhs == pd_timestamp_type
    return hds__erokh or xzlsf__ewp


def sub_dt_or_td(lhs, rhs):
    cuk__tmrr = lhs == datetime_date_type and rhs == datetime_timedelta_type
    cqbo__kykrx = lhs == datetime_date_type and rhs == datetime_date_type
    kfh__yxr = (lhs == datetime_date_array_type and rhs ==
        datetime_timedelta_type)
    return cuk__tmrr or cqbo__kykrx or kfh__yxr


def sub_datetime_and_timedeltas(lhs, rhs):
    tavnl__anwzp = (is_timedelta_type(lhs) or lhs == datetime_datetime_type
        ) and is_timedelta_type(rhs)
    zwqe__djlg = (lhs == datetime_timedelta_array_type and rhs ==
        datetime_timedelta_type)
    return tavnl__anwzp or zwqe__djlg


def div_timedelta_and_int(lhs, rhs):
    emlvo__jyewz = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    otbu__bhyfa = lhs == pd_timedelta_type and isinstance(rhs, types.Integer)
    return emlvo__jyewz or otbu__bhyfa


def div_datetime_timedelta(lhs, rhs):
    emlvo__jyewz = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    otbu__bhyfa = lhs == datetime_timedelta_type and rhs == types.int64
    return emlvo__jyewz or otbu__bhyfa


def mod_timedeltas(lhs, rhs):
    rju__amoj = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    hprfk__csyd = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    return rju__amoj or hprfk__csyd


def cmp_dt_index_to_string(lhs, rhs):
    hds__erokh = isinstance(lhs, DatetimeIndexType) and types.unliteral(rhs
        ) == string_type
    xzlsf__ewp = isinstance(rhs, DatetimeIndexType) and types.unliteral(lhs
        ) == string_type
    return hds__erokh or xzlsf__ewp


def cmp_timestamp_or_date(lhs, rhs):
    yzb__xpxvy = (lhs == pd_timestamp_type and rhs == bodo.hiframes.
        datetime_date_ext.datetime_date_type)
    fnbsn__wukwi = (lhs == bodo.hiframes.datetime_date_ext.
        datetime_date_type and rhs == pd_timestamp_type)
    ysz__fvlmx = lhs == pd_timestamp_type and rhs == pd_timestamp_type
    oilss__eyxi = lhs == pd_timestamp_type and rhs == bodo.datetime64ns
    jez__ylk = rhs == pd_timestamp_type and lhs == bodo.datetime64ns
    return yzb__xpxvy or fnbsn__wukwi or ysz__fvlmx or oilss__eyxi or jez__ylk


def cmp_timeseries(lhs, rhs):
    vqvj__ovos = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (bodo
        .utils.typing.is_overload_constant_str(lhs) or lhs == bodo.libs.
        str_ext.string_type or lhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_type)
    vqp__mrm = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (bodo
        .utils.typing.is_overload_constant_str(rhs) or rhs == bodo.libs.
        str_ext.string_type or rhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_type)
    gvfqg__mdf = vqvj__ovos or vqp__mrm
    crpez__lpk = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    ywiy__vcm = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    tfx__irc = crpez__lpk or ywiy__vcm
    return gvfqg__mdf or tfx__irc


def cmp_timedeltas(lhs, rhs):
    emlvo__jyewz = [pd_timedelta_type, bodo.timedelta64ns]
    return lhs in emlvo__jyewz and rhs in emlvo__jyewz


def operand_is_index(operand):
    return is_index_type(operand) or isinstance(operand, HeterogeneousIndexType
        )


def helper_time_series_checks(operand):
    ucvnw__ctn = bodo.hiframes.pd_series_ext.is_dt64_series_typ(operand
        ) or bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(operand
        ) or operand in [datetime_timedelta_type, datetime_datetime_type,
        pd_timestamp_type]
    return ucvnw__ctn


def binary_array_cmp(lhs, rhs):
    return lhs == binary_array_type and rhs in [bytes_type, binary_array_type
        ] or lhs in [bytes_type, binary_array_type
        ] and rhs == binary_array_type


def can_cmp_date_datetime(lhs, rhs, op):
    return op in (operator.eq, operator.ne) and (lhs == datetime_date_type and
        rhs == datetime_datetime_type or lhs == datetime_datetime_type and 
        rhs == datetime_date_type)


def time_series_operation(lhs, rhs):
    jrfhx__jsrl = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == datetime_timedelta_type
    tigp__kuwly = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == datetime_timedelta_type
    spuh__kdio = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
        ) and helper_time_series_checks(rhs)
    mupt__woenq = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
        ) and helper_time_series_checks(lhs)
    return jrfhx__jsrl or tigp__kuwly or spuh__kdio or mupt__woenq


def args_td_and_int_array(lhs, rhs):
    mwg__fyvd = (isinstance(lhs, IntegerArrayType) or isinstance(lhs, types
        .Array) and isinstance(lhs.dtype, types.Integer)) or (isinstance(
        rhs, IntegerArrayType) or isinstance(rhs, types.Array) and
        isinstance(rhs.dtype, types.Integer))
    ntwm__mezte = lhs in [pd_timedelta_type] or rhs in [pd_timedelta_type]
    return mwg__fyvd and ntwm__mezte


def arith_op_supported_by_numba(op, lhs, rhs):
    if op == operator.mul:
        gxy__yag = isinstance(lhs, (types.Integer, types.Float)
            ) and isinstance(rhs, types.NPTimedelta)
        dfjt__ubtm = isinstance(rhs, (types.Integer, types.Float)
            ) and isinstance(lhs, types.NPTimedelta)
        lsswu__dpm = gxy__yag or dfjt__ubtm
        dvj__rpnao = isinstance(rhs, types.UnicodeType) and isinstance(lhs,
            types.Integer)
        slzn__cjlpm = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.Integer)
        prteu__wfsqx = dvj__rpnao or slzn__cjlpm
        rpr__tps = isinstance(lhs, types.Integer) and isinstance(rhs, types
            .Integer)
        svmk__nchag = isinstance(lhs, types.Float) and isinstance(rhs,
            types.Float)
        bbz__ockn = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        pgdby__nivyp = rpr__tps or svmk__nchag or bbz__ockn
        feybn__mscqo = isinstance(lhs, types.List) and isinstance(rhs,
            types.Integer) or isinstance(lhs, types.Integer) and isinstance(rhs
            , types.List)
        tys = types.UnicodeCharSeq, types.CharSeq, types.Bytes
        uafve__buesl = isinstance(lhs, tys) or isinstance(rhs, tys)
        hof__wiz = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
        return (lsswu__dpm or prteu__wfsqx or pgdby__nivyp or feybn__mscqo or
            uafve__buesl or hof__wiz)
    if op == operator.pow:
        ujvvt__scdx = isinstance(lhs, types.Integer) and isinstance(rhs, (
            types.IntegerLiteral, types.Integer))
        laq__wwpy = isinstance(lhs, types.Float) and isinstance(rhs, (types
            .IntegerLiteral, types.Float, types.Integer) or rhs in types.
            unsigned_domain or rhs in types.signed_domain)
        bbz__ockn = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        hof__wiz = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
        return ujvvt__scdx or laq__wwpy or bbz__ockn or hof__wiz
    if op == operator.floordiv:
        svmk__nchag = lhs in types.real_domain and rhs in types.real_domain
        rpr__tps = isinstance(lhs, types.Integer) and isinstance(rhs, types
            .Integer)
        bzco__drok = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        emlvo__jyewz = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        hof__wiz = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
        return (svmk__nchag or rpr__tps or bzco__drok or emlvo__jyewz or
            hof__wiz)
    if op == operator.truediv:
        ghdmg__zdi = lhs in machine_ints and rhs in machine_ints
        svmk__nchag = lhs in types.real_domain and rhs in types.real_domain
        bbz__ockn = lhs in types.complex_domain and rhs in types.complex_domain
        rpr__tps = isinstance(lhs, types.Integer) and isinstance(rhs, types
            .Integer)
        bzco__drok = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        fqjsi__ltam = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        emlvo__jyewz = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        hof__wiz = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
        return (ghdmg__zdi or svmk__nchag or bbz__ockn or rpr__tps or
            bzco__drok or fqjsi__ltam or emlvo__jyewz or hof__wiz)
    if op == operator.mod:
        ghdmg__zdi = lhs in machine_ints and rhs in machine_ints
        svmk__nchag = lhs in types.real_domain and rhs in types.real_domain
        rpr__tps = isinstance(lhs, types.Integer) and isinstance(rhs, types
            .Integer)
        bzco__drok = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        hof__wiz = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
        return ghdmg__zdi or svmk__nchag or rpr__tps or bzco__drok or hof__wiz
    if op == operator.add or op == operator.sub:
        lsswu__dpm = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            types.NPTimedelta)
        dqq__pusj = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPDatetime)
        femrr__yru = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPTimedelta)
        aiq__pkp = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
        rpr__tps = isinstance(lhs, types.Integer) and isinstance(rhs, types
            .Integer)
        svmk__nchag = isinstance(lhs, types.Float) and isinstance(rhs,
            types.Float)
        bbz__ockn = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        pgdby__nivyp = rpr__tps or svmk__nchag or bbz__ockn
        hof__wiz = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
        emkx__mwm = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
            types.BaseTuple)
        feybn__mscqo = isinstance(lhs, types.List) and isinstance(rhs,
            types.List)
        kphyu__ymz = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeType)
        wuuaj__idz = isinstance(rhs, types.UnicodeCharSeq) and isinstance(lhs,
            types.UnicodeType)
        vspx__jfa = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeCharSeq)
        veq__fspjr = isinstance(lhs, (types.CharSeq, types.Bytes)
            ) and isinstance(rhs, (types.CharSeq, types.Bytes))
        hld__usrd = kphyu__ymz or wuuaj__idz or vspx__jfa or veq__fspjr
        prteu__wfsqx = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeType)
        nksfy__nsrqr = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeCharSeq)
        lma__sqhzn = prteu__wfsqx or nksfy__nsrqr
        wpa__umlv = lhs == types.NPTimedelta and rhs == types.NPDatetime
        weck__xkjnb = (emkx__mwm or feybn__mscqo or hld__usrd or lma__sqhzn or
            wpa__umlv)
        mkd__ksih = op == operator.add and weck__xkjnb
        return (lsswu__dpm or dqq__pusj or femrr__yru or aiq__pkp or
            pgdby__nivyp or hof__wiz or mkd__ksih)


def cmp_op_supported_by_numba(lhs, rhs):
    hof__wiz = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
    feybn__mscqo = isinstance(lhs, types.ListType) and isinstance(rhs,
        types.ListType)
    lsswu__dpm = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
        types.NPTimedelta)
    twu__hfckb = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
        types.NPDatetime)
    unicode_types = (types.UnicodeType, types.StringLiteral, types.CharSeq,
        types.Bytes, types.UnicodeCharSeq)
    prteu__wfsqx = isinstance(lhs, unicode_types) and isinstance(rhs,
        unicode_types)
    emkx__mwm = isinstance(lhs, types.BaseTuple) and isinstance(rhs, types.
        BaseTuple)
    aiq__pkp = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
    pgdby__nivyp = isinstance(lhs, types.Number) and isinstance(rhs, types.
        Number)
    numw__jozep = isinstance(lhs, types.Boolean) and isinstance(rhs, types.
        Boolean)
    yktgu__olly = isinstance(lhs, types.NoneType) or isinstance(rhs, types.
        NoneType)
    ajr__ffd = isinstance(lhs, types.DictType) and isinstance(rhs, types.
        DictType)
    wpok__wyrzp = isinstance(lhs, types.EnumMember) and isinstance(rhs,
        types.EnumMember)
    xhps__gvudc = isinstance(lhs, types.Literal) and isinstance(rhs, types.
        Literal)
    return (feybn__mscqo or lsswu__dpm or twu__hfckb or prteu__wfsqx or
        emkx__mwm or aiq__pkp or pgdby__nivyp or numw__jozep or yktgu__olly or
        ajr__ffd or hof__wiz or wpok__wyrzp or xhps__gvudc)


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
        cee__iou = create_overload_cmp_operator(op)
        overload(op, no_unliteral=True)(cee__iou)


_install_cmp_ops()


def install_arith_ops():
    for op in (operator.add, operator.sub, operator.mul, operator.truediv,
        operator.floordiv, operator.mod, operator.pow):
        cee__iou = create_overload_arith_op(op)
        overload(op, no_unliteral=True)(cee__iou)


install_arith_ops()
