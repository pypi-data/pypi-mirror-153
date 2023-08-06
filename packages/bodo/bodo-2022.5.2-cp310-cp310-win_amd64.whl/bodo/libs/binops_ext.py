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
        rik__evb = lhs.data if isinstance(lhs, SeriesType) else lhs
        tcds__qavf = rhs.data if isinstance(rhs, SeriesType) else rhs
        if rik__evb in (bodo.pd_timestamp_type, bodo.pd_timedelta_type
            ) and tcds__qavf.dtype in (bodo.datetime64ns, bodo.timedelta64ns):
            rik__evb = tcds__qavf.dtype
        elif tcds__qavf in (bodo.pd_timestamp_type, bodo.pd_timedelta_type
            ) and rik__evb.dtype in (bodo.datetime64ns, bodo.timedelta64ns):
            tcds__qavf = rik__evb.dtype
        wptm__yql = rik__evb, tcds__qavf
        nisi__irlq = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            atns__zlqrr = self.context.resolve_function_type(self.key,
                wptm__yql, {}).return_type
        except Exception as vexo__nrbhb:
            raise BodoError(nisi__irlq)
        if is_overload_bool(atns__zlqrr):
            raise BodoError(nisi__irlq)
        twqvw__hccal = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        nsfzo__fmre = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        jzv__qcb = types.bool_
        gjbw__clf = SeriesType(jzv__qcb, atns__zlqrr, twqvw__hccal, nsfzo__fmre
            )
        return gjbw__clf(*args)


def series_cmp_op_lower(op):

    def lower_impl(context, builder, sig, args):
        jrgl__wdgh = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if jrgl__wdgh is None:
            jrgl__wdgh = create_overload_cmp_operator(op)(*sig.args)
        return context.compile_internal(builder, jrgl__wdgh, sig, args)
    return lower_impl


class SeriesAndOrTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        lhs, rhs = args
        if not (isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType)):
            return
        rik__evb = lhs.data if isinstance(lhs, SeriesType) else lhs
        tcds__qavf = rhs.data if isinstance(rhs, SeriesType) else rhs
        wptm__yql = rik__evb, tcds__qavf
        nisi__irlq = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            atns__zlqrr = self.context.resolve_function_type(self.key,
                wptm__yql, {}).return_type
        except Exception as qeyq__vwgpf:
            raise BodoError(nisi__irlq)
        twqvw__hccal = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        nsfzo__fmre = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        jzv__qcb = atns__zlqrr.dtype
        gjbw__clf = SeriesType(jzv__qcb, atns__zlqrr, twqvw__hccal, nsfzo__fmre
            )
        return gjbw__clf(*args)


def lower_series_and_or(op):

    def lower_and_or_impl(context, builder, sig, args):
        jrgl__wdgh = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if jrgl__wdgh is None:
            lhs, rhs = sig.args
            if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType
                ):
                jrgl__wdgh = (bodo.hiframes.dataframe_impl.
                    create_binary_op_overload(op)(*sig.args))
        return context.compile_internal(builder, jrgl__wdgh, sig, args)
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
            jrgl__wdgh = (bodo.hiframes.datetime_timedelta_ext.
                create_cmp_op_overload(op))
            return jrgl__wdgh(lhs, rhs)
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
            jrgl__wdgh = (bodo.hiframes.datetime_timedelta_ext.
                pd_create_cmp_op_overload(op))
            return jrgl__wdgh(lhs, rhs)
        if cmp_timestamp_or_date(lhs, rhs):
            return (bodo.hiframes.pd_timestamp_ext.
                create_timestamp_cmp_op_overload(op)(lhs, rhs))
        if cmp_op_supported_by_numba(lhs, rhs):
            return
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_cmp_operator


def add_dt_td_and_dt_date(lhs, rhs):
    pyac__elfk = lhs == datetime_timedelta_type and rhs == datetime_date_type
    yxn__evbm = rhs == datetime_timedelta_type and lhs == datetime_date_type
    return pyac__elfk or yxn__evbm


def add_timestamp(lhs, rhs):
    fzgg__vnf = lhs == pd_timestamp_type and is_timedelta_type(rhs)
    ooymo__ewrja = is_timedelta_type(lhs) and rhs == pd_timestamp_type
    return fzgg__vnf or ooymo__ewrja


def add_datetime_and_timedeltas(lhs, rhs):
    zunjp__ikh = [datetime_timedelta_type, pd_timedelta_type]
    trfvm__aenv = [datetime_timedelta_type, pd_timedelta_type,
        datetime_datetime_type]
    ixe__bgk = lhs in zunjp__ikh and rhs in zunjp__ikh
    wozhc__ugqho = (lhs == datetime_datetime_type and rhs in zunjp__ikh or 
        rhs == datetime_datetime_type and lhs in zunjp__ikh)
    return ixe__bgk or wozhc__ugqho


def mul_string_arr_and_int(lhs, rhs):
    tcds__qavf = isinstance(lhs, types.Integer) and is_str_arr_type(rhs)
    rik__evb = is_str_arr_type(lhs) and isinstance(rhs, types.Integer)
    return tcds__qavf or rik__evb


def mul_timedelta_and_int(lhs, rhs):
    pyac__elfk = lhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(rhs, types.Integer)
    yxn__evbm = rhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(lhs, types.Integer)
    return pyac__elfk or yxn__evbm


def mul_date_offset_and_int(lhs, rhs):
    xkwtm__hkr = lhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(rhs, types.Integer)
    kzhlh__pib = rhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(lhs, types.Integer)
    return xkwtm__hkr or kzhlh__pib


def sub_offset_to_datetime_or_timestamp(lhs, rhs):
    vtlaj__vzyay = [datetime_datetime_type, pd_timestamp_type,
        datetime_date_type]
    kltk__pna = [date_offset_type, month_begin_type, month_end_type, week_type]
    return rhs in kltk__pna and lhs in vtlaj__vzyay


def sub_dt_index_and_timestamp(lhs, rhs):
    hxfp__sra = isinstance(lhs, DatetimeIndexType) and rhs == pd_timestamp_type
    wjqrj__yetco = isinstance(rhs, DatetimeIndexType
        ) and lhs == pd_timestamp_type
    return hxfp__sra or wjqrj__yetco


def sub_dt_or_td(lhs, rhs):
    jpdt__pajt = lhs == datetime_date_type and rhs == datetime_timedelta_type
    ymcd__rzgpw = lhs == datetime_date_type and rhs == datetime_date_type
    amk__jtg = (lhs == datetime_date_array_type and rhs ==
        datetime_timedelta_type)
    return jpdt__pajt or ymcd__rzgpw or amk__jtg


def sub_datetime_and_timedeltas(lhs, rhs):
    ashs__olnjl = (is_timedelta_type(lhs) or lhs == datetime_datetime_type
        ) and is_timedelta_type(rhs)
    fna__vcuv = (lhs == datetime_timedelta_array_type and rhs ==
        datetime_timedelta_type)
    return ashs__olnjl or fna__vcuv


def div_timedelta_and_int(lhs, rhs):
    ixe__bgk = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    najbb__snost = lhs == pd_timedelta_type and isinstance(rhs, types.Integer)
    return ixe__bgk or najbb__snost


def div_datetime_timedelta(lhs, rhs):
    ixe__bgk = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    najbb__snost = lhs == datetime_timedelta_type and rhs == types.int64
    return ixe__bgk or najbb__snost


def mod_timedeltas(lhs, rhs):
    asjdo__bhgc = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    vdq__czw = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    return asjdo__bhgc or vdq__czw


def cmp_dt_index_to_string(lhs, rhs):
    hxfp__sra = isinstance(lhs, DatetimeIndexType) and types.unliteral(rhs
        ) == string_type
    wjqrj__yetco = isinstance(rhs, DatetimeIndexType) and types.unliteral(lhs
        ) == string_type
    return hxfp__sra or wjqrj__yetco


def cmp_timestamp_or_date(lhs, rhs):
    aeqe__pxgx = (lhs == pd_timestamp_type and rhs == bodo.hiframes.
        datetime_date_ext.datetime_date_type)
    nxzsz__uum = (lhs == bodo.hiframes.datetime_date_ext.datetime_date_type and
        rhs == pd_timestamp_type)
    vrscx__qbsgo = lhs == pd_timestamp_type and rhs == pd_timestamp_type
    diwnt__zqd = lhs == pd_timestamp_type and rhs == bodo.datetime64ns
    vsjxt__jwms = rhs == pd_timestamp_type and lhs == bodo.datetime64ns
    return (aeqe__pxgx or nxzsz__uum or vrscx__qbsgo or diwnt__zqd or
        vsjxt__jwms)


def cmp_timeseries(lhs, rhs):
    wmjo__ajw = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (bodo
        .utils.typing.is_overload_constant_str(lhs) or lhs == bodo.libs.
        str_ext.string_type or lhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_type)
    buc__qdrxt = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (bodo
        .utils.typing.is_overload_constant_str(rhs) or rhs == bodo.libs.
        str_ext.string_type or rhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_type)
    bhws__yyyet = wmjo__ajw or buc__qdrxt
    twe__ybb = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    egf__ufza = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    ruvza__wlhcz = twe__ybb or egf__ufza
    return bhws__yyyet or ruvza__wlhcz


def cmp_timedeltas(lhs, rhs):
    ixe__bgk = [pd_timedelta_type, bodo.timedelta64ns]
    return lhs in ixe__bgk and rhs in ixe__bgk


def operand_is_index(operand):
    return is_index_type(operand) or isinstance(operand, HeterogeneousIndexType
        )


def helper_time_series_checks(operand):
    fcvy__gxpq = bodo.hiframes.pd_series_ext.is_dt64_series_typ(operand
        ) or bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(operand
        ) or operand in [datetime_timedelta_type, datetime_datetime_type,
        pd_timestamp_type]
    return fcvy__gxpq


def binary_array_cmp(lhs, rhs):
    return lhs == binary_array_type and rhs in [bytes_type, binary_array_type
        ] or lhs in [bytes_type, binary_array_type
        ] and rhs == binary_array_type


def can_cmp_date_datetime(lhs, rhs, op):
    return op in (operator.eq, operator.ne) and (lhs == datetime_date_type and
        rhs == datetime_datetime_type or lhs == datetime_datetime_type and 
        rhs == datetime_date_type)


def time_series_operation(lhs, rhs):
    cob__pzu = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == datetime_timedelta_type
    pcrlb__nguqd = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == datetime_timedelta_type
    rnzzm__bces = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
        ) and helper_time_series_checks(rhs)
    baop__qkd = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
        ) and helper_time_series_checks(lhs)
    return cob__pzu or pcrlb__nguqd or rnzzm__bces or baop__qkd


def args_td_and_int_array(lhs, rhs):
    hokvs__bywh = (isinstance(lhs, IntegerArrayType) or isinstance(lhs,
        types.Array) and isinstance(lhs.dtype, types.Integer)) or (isinstance
        (rhs, IntegerArrayType) or isinstance(rhs, types.Array) and
        isinstance(rhs.dtype, types.Integer))
    wpir__niyi = lhs in [pd_timedelta_type] or rhs in [pd_timedelta_type]
    return hokvs__bywh and wpir__niyi


def arith_op_supported_by_numba(op, lhs, rhs):
    if op == operator.mul:
        yxn__evbm = isinstance(lhs, (types.Integer, types.Float)
            ) and isinstance(rhs, types.NPTimedelta)
        pyac__elfk = isinstance(rhs, (types.Integer, types.Float)
            ) and isinstance(lhs, types.NPTimedelta)
        suwi__guv = yxn__evbm or pyac__elfk
        ywp__xasav = isinstance(rhs, types.UnicodeType) and isinstance(lhs,
            types.Integer)
        qwyh__mvvk = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.Integer)
        cwlsg__aqndt = ywp__xasav or qwyh__mvvk
        jpxlu__qhn = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        cqqu__durg = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        rht__rakf = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        zmo__ogthc = jpxlu__qhn or cqqu__durg or rht__rakf
        ayv__ekauf = isinstance(lhs, types.List) and isinstance(rhs, types.
            Integer) or isinstance(lhs, types.Integer) and isinstance(rhs,
            types.List)
        tys = types.UnicodeCharSeq, types.CharSeq, types.Bytes
        jrwa__clnb = isinstance(lhs, tys) or isinstance(rhs, tys)
        lef__spn = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
        return (suwi__guv or cwlsg__aqndt or zmo__ogthc or ayv__ekauf or
            jrwa__clnb or lef__spn)
    if op == operator.pow:
        vrjm__rqoz = isinstance(lhs, types.Integer) and isinstance(rhs, (
            types.IntegerLiteral, types.Integer))
        uwtj__padp = isinstance(lhs, types.Float) and isinstance(rhs, (
            types.IntegerLiteral, types.Float, types.Integer) or rhs in
            types.unsigned_domain or rhs in types.signed_domain)
        rht__rakf = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        lef__spn = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
        return vrjm__rqoz or uwtj__padp or rht__rakf or lef__spn
    if op == operator.floordiv:
        cqqu__durg = lhs in types.real_domain and rhs in types.real_domain
        jpxlu__qhn = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        copvu__qmhyl = isinstance(lhs, types.Float) and isinstance(rhs,
            types.Float)
        ixe__bgk = isinstance(lhs, types.NPTimedelta) and isinstance(rhs, (
            types.Integer, types.Float, types.NPTimedelta))
        lef__spn = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
        return cqqu__durg or jpxlu__qhn or copvu__qmhyl or ixe__bgk or lef__spn
    if op == operator.truediv:
        aab__osbl = lhs in machine_ints and rhs in machine_ints
        cqqu__durg = lhs in types.real_domain and rhs in types.real_domain
        rht__rakf = lhs in types.complex_domain and rhs in types.complex_domain
        jpxlu__qhn = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        copvu__qmhyl = isinstance(lhs, types.Float) and isinstance(rhs,
            types.Float)
        ehik__hujd = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        ixe__bgk = isinstance(lhs, types.NPTimedelta) and isinstance(rhs, (
            types.Integer, types.Float, types.NPTimedelta))
        lef__spn = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
        return (aab__osbl or cqqu__durg or rht__rakf or jpxlu__qhn or
            copvu__qmhyl or ehik__hujd or ixe__bgk or lef__spn)
    if op == operator.mod:
        aab__osbl = lhs in machine_ints and rhs in machine_ints
        cqqu__durg = lhs in types.real_domain and rhs in types.real_domain
        jpxlu__qhn = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        copvu__qmhyl = isinstance(lhs, types.Float) and isinstance(rhs,
            types.Float)
        lef__spn = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
        return (aab__osbl or cqqu__durg or jpxlu__qhn or copvu__qmhyl or
            lef__spn)
    if op == operator.add or op == operator.sub:
        suwi__guv = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            types.NPTimedelta)
        gccw__vrf = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPDatetime)
        hvp__osat = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPTimedelta)
        bzjp__ewhd = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
        jpxlu__qhn = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        cqqu__durg = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        rht__rakf = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        zmo__ogthc = jpxlu__qhn or cqqu__durg or rht__rakf
        lef__spn = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
        amkh__ykdiw = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
            types.BaseTuple)
        ayv__ekauf = isinstance(lhs, types.List) and isinstance(rhs, types.List
            )
        hrnit__difn = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeType)
        plvyl__vshgb = isinstance(rhs, types.UnicodeCharSeq) and isinstance(lhs
            , types.UnicodeType)
        jmdlq__qju = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeCharSeq)
        bbmqf__znwe = isinstance(lhs, (types.CharSeq, types.Bytes)
            ) and isinstance(rhs, (types.CharSeq, types.Bytes))
        kdfn__hst = hrnit__difn or plvyl__vshgb or jmdlq__qju or bbmqf__znwe
        cwlsg__aqndt = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeType)
        tmheg__nvvf = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeCharSeq)
        mvjlo__teg = cwlsg__aqndt or tmheg__nvvf
        blvwe__nowp = lhs == types.NPTimedelta and rhs == types.NPDatetime
        tmegu__zdab = (amkh__ykdiw or ayv__ekauf or kdfn__hst or mvjlo__teg or
            blvwe__nowp)
        tzb__dyu = op == operator.add and tmegu__zdab
        return (suwi__guv or gccw__vrf or hvp__osat or bzjp__ewhd or
            zmo__ogthc or lef__spn or tzb__dyu)


def cmp_op_supported_by_numba(lhs, rhs):
    lef__spn = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
    ayv__ekauf = isinstance(lhs, types.ListType) and isinstance(rhs, types.
        ListType)
    suwi__guv = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
        types.NPTimedelta)
    dewe__shhs = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
        types.NPDatetime)
    unicode_types = (types.UnicodeType, types.StringLiteral, types.CharSeq,
        types.Bytes, types.UnicodeCharSeq)
    cwlsg__aqndt = isinstance(lhs, unicode_types) and isinstance(rhs,
        unicode_types)
    amkh__ykdiw = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
        types.BaseTuple)
    bzjp__ewhd = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
    zmo__ogthc = isinstance(lhs, types.Number) and isinstance(rhs, types.Number
        )
    vhctn__vues = isinstance(lhs, types.Boolean) and isinstance(rhs, types.
        Boolean)
    ghfc__ckkop = isinstance(lhs, types.NoneType) or isinstance(rhs, types.
        NoneType)
    pmgal__mmjg = isinstance(lhs, types.DictType) and isinstance(rhs, types
        .DictType)
    iiss__gkrlf = isinstance(lhs, types.EnumMember) and isinstance(rhs,
        types.EnumMember)
    aqc__pnupk = isinstance(lhs, types.Literal) and isinstance(rhs, types.
        Literal)
    return (ayv__ekauf or suwi__guv or dewe__shhs or cwlsg__aqndt or
        amkh__ykdiw or bzjp__ewhd or zmo__ogthc or vhctn__vues or
        ghfc__ckkop or pmgal__mmjg or lef__spn or iiss__gkrlf or aqc__pnupk)


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
        qgfam__wtpn = create_overload_cmp_operator(op)
        overload(op, no_unliteral=True)(qgfam__wtpn)


_install_cmp_ops()


def install_arith_ops():
    for op in (operator.add, operator.sub, operator.mul, operator.truediv,
        operator.floordiv, operator.mod, operator.pow):
        qgfam__wtpn = create_overload_arith_op(op)
        overload(op, no_unliteral=True)(qgfam__wtpn)


install_arith_ops()
