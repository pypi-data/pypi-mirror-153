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
        nwktg__qxs = lhs.data if isinstance(lhs, SeriesType) else lhs
        oqxjc__awd = rhs.data if isinstance(rhs, SeriesType) else rhs
        if nwktg__qxs in (bodo.pd_timestamp_type, bodo.pd_timedelta_type
            ) and oqxjc__awd.dtype in (bodo.datetime64ns, bodo.timedelta64ns):
            nwktg__qxs = oqxjc__awd.dtype
        elif oqxjc__awd in (bodo.pd_timestamp_type, bodo.pd_timedelta_type
            ) and nwktg__qxs.dtype in (bodo.datetime64ns, bodo.timedelta64ns):
            oqxjc__awd = nwktg__qxs.dtype
        fpb__pwsjb = nwktg__qxs, oqxjc__awd
        qwzn__harn = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            zfaj__dhf = self.context.resolve_function_type(self.key,
                fpb__pwsjb, {}).return_type
        except Exception as hfi__mcktu:
            raise BodoError(qwzn__harn)
        if is_overload_bool(zfaj__dhf):
            raise BodoError(qwzn__harn)
        uttj__hjgb = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        crvih__bjyo = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        hocz__bjnqg = types.bool_
        nrs__fkm = SeriesType(hocz__bjnqg, zfaj__dhf, uttj__hjgb, crvih__bjyo)
        return nrs__fkm(*args)


def series_cmp_op_lower(op):

    def lower_impl(context, builder, sig, args):
        dhjkx__lsw = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if dhjkx__lsw is None:
            dhjkx__lsw = create_overload_cmp_operator(op)(*sig.args)
        return context.compile_internal(builder, dhjkx__lsw, sig, args)
    return lower_impl


class SeriesAndOrTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        lhs, rhs = args
        if not (isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType)):
            return
        nwktg__qxs = lhs.data if isinstance(lhs, SeriesType) else lhs
        oqxjc__awd = rhs.data if isinstance(rhs, SeriesType) else rhs
        fpb__pwsjb = nwktg__qxs, oqxjc__awd
        qwzn__harn = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            zfaj__dhf = self.context.resolve_function_type(self.key,
                fpb__pwsjb, {}).return_type
        except Exception as szik__qatjl:
            raise BodoError(qwzn__harn)
        uttj__hjgb = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        crvih__bjyo = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        hocz__bjnqg = zfaj__dhf.dtype
        nrs__fkm = SeriesType(hocz__bjnqg, zfaj__dhf, uttj__hjgb, crvih__bjyo)
        return nrs__fkm(*args)


def lower_series_and_or(op):

    def lower_and_or_impl(context, builder, sig, args):
        dhjkx__lsw = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if dhjkx__lsw is None:
            lhs, rhs = sig.args
            if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType
                ):
                dhjkx__lsw = (bodo.hiframes.dataframe_impl.
                    create_binary_op_overload(op)(*sig.args))
        return context.compile_internal(builder, dhjkx__lsw, sig, args)
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
            dhjkx__lsw = (bodo.hiframes.datetime_timedelta_ext.
                create_cmp_op_overload(op))
            return dhjkx__lsw(lhs, rhs)
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
            dhjkx__lsw = (bodo.hiframes.datetime_timedelta_ext.
                pd_create_cmp_op_overload(op))
            return dhjkx__lsw(lhs, rhs)
        if cmp_timestamp_or_date(lhs, rhs):
            return (bodo.hiframes.pd_timestamp_ext.
                create_timestamp_cmp_op_overload(op)(lhs, rhs))
        if cmp_op_supported_by_numba(lhs, rhs):
            return
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_cmp_operator


def add_dt_td_and_dt_date(lhs, rhs):
    mnvz__hnje = lhs == datetime_timedelta_type and rhs == datetime_date_type
    bvur__bozrv = rhs == datetime_timedelta_type and lhs == datetime_date_type
    return mnvz__hnje or bvur__bozrv


def add_timestamp(lhs, rhs):
    tqnri__thlf = lhs == pd_timestamp_type and is_timedelta_type(rhs)
    icwz__rbin = is_timedelta_type(lhs) and rhs == pd_timestamp_type
    return tqnri__thlf or icwz__rbin


def add_datetime_and_timedeltas(lhs, rhs):
    cjhcn__pzf = [datetime_timedelta_type, pd_timedelta_type]
    siomg__ggf = [datetime_timedelta_type, pd_timedelta_type,
        datetime_datetime_type]
    osa__lyirq = lhs in cjhcn__pzf and rhs in cjhcn__pzf
    cvae__tehg = (lhs == datetime_datetime_type and rhs in cjhcn__pzf or 
        rhs == datetime_datetime_type and lhs in cjhcn__pzf)
    return osa__lyirq or cvae__tehg


def mul_string_arr_and_int(lhs, rhs):
    oqxjc__awd = isinstance(lhs, types.Integer) and is_str_arr_type(rhs)
    nwktg__qxs = is_str_arr_type(lhs) and isinstance(rhs, types.Integer)
    return oqxjc__awd or nwktg__qxs


def mul_timedelta_and_int(lhs, rhs):
    mnvz__hnje = lhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(rhs, types.Integer)
    bvur__bozrv = rhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(lhs, types.Integer)
    return mnvz__hnje or bvur__bozrv


def mul_date_offset_and_int(lhs, rhs):
    nnyz__awkfe = lhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(rhs, types.Integer)
    egzvz__ysh = rhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(lhs, types.Integer)
    return nnyz__awkfe or egzvz__ysh


def sub_offset_to_datetime_or_timestamp(lhs, rhs):
    hit__ulgn = [datetime_datetime_type, pd_timestamp_type, datetime_date_type]
    xbsui__evy = [date_offset_type, month_begin_type, month_end_type, week_type
        ]
    return rhs in xbsui__evy and lhs in hit__ulgn


def sub_dt_index_and_timestamp(lhs, rhs):
    wxf__zrm = isinstance(lhs, DatetimeIndexType) and rhs == pd_timestamp_type
    cqv__opfph = isinstance(rhs, DatetimeIndexType
        ) and lhs == pd_timestamp_type
    return wxf__zrm or cqv__opfph


def sub_dt_or_td(lhs, rhs):
    jjea__mdq = lhs == datetime_date_type and rhs == datetime_timedelta_type
    lcgz__cvh = lhs == datetime_date_type and rhs == datetime_date_type
    pcs__pfqeu = (lhs == datetime_date_array_type and rhs ==
        datetime_timedelta_type)
    return jjea__mdq or lcgz__cvh or pcs__pfqeu


def sub_datetime_and_timedeltas(lhs, rhs):
    onxj__orzf = (is_timedelta_type(lhs) or lhs == datetime_datetime_type
        ) and is_timedelta_type(rhs)
    bim__katdn = (lhs == datetime_timedelta_array_type and rhs ==
        datetime_timedelta_type)
    return onxj__orzf or bim__katdn


def div_timedelta_and_int(lhs, rhs):
    osa__lyirq = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    zwo__fbhab = lhs == pd_timedelta_type and isinstance(rhs, types.Integer)
    return osa__lyirq or zwo__fbhab


def div_datetime_timedelta(lhs, rhs):
    osa__lyirq = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    zwo__fbhab = lhs == datetime_timedelta_type and rhs == types.int64
    return osa__lyirq or zwo__fbhab


def mod_timedeltas(lhs, rhs):
    wles__qakbl = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    nvxo__sfx = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    return wles__qakbl or nvxo__sfx


def cmp_dt_index_to_string(lhs, rhs):
    wxf__zrm = isinstance(lhs, DatetimeIndexType) and types.unliteral(rhs
        ) == string_type
    cqv__opfph = isinstance(rhs, DatetimeIndexType) and types.unliteral(lhs
        ) == string_type
    return wxf__zrm or cqv__opfph


def cmp_timestamp_or_date(lhs, rhs):
    dwht__chvtc = (lhs == pd_timestamp_type and rhs == bodo.hiframes.
        datetime_date_ext.datetime_date_type)
    pubk__ydbwr = (lhs == bodo.hiframes.datetime_date_ext.
        datetime_date_type and rhs == pd_timestamp_type)
    unqtu__ianyx = lhs == pd_timestamp_type and rhs == pd_timestamp_type
    bhr__cnlk = lhs == pd_timestamp_type and rhs == bodo.datetime64ns
    iktva__fcha = rhs == pd_timestamp_type and lhs == bodo.datetime64ns
    return (dwht__chvtc or pubk__ydbwr or unqtu__ianyx or bhr__cnlk or
        iktva__fcha)


def cmp_timeseries(lhs, rhs):
    uzl__rrw = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (bodo
        .utils.typing.is_overload_constant_str(lhs) or lhs == bodo.libs.
        str_ext.string_type or lhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_type)
    gpi__mykn = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (bodo
        .utils.typing.is_overload_constant_str(rhs) or rhs == bodo.libs.
        str_ext.string_type or rhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_type)
    ltdvg__ckjs = uzl__rrw or gpi__mykn
    husw__wdl = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    bbl__risam = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    qkvc__gitw = husw__wdl or bbl__risam
    return ltdvg__ckjs or qkvc__gitw


def cmp_timedeltas(lhs, rhs):
    osa__lyirq = [pd_timedelta_type, bodo.timedelta64ns]
    return lhs in osa__lyirq and rhs in osa__lyirq


def operand_is_index(operand):
    return is_index_type(operand) or isinstance(operand, HeterogeneousIndexType
        )


def helper_time_series_checks(operand):
    ksz__itj = bodo.hiframes.pd_series_ext.is_dt64_series_typ(operand
        ) or bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(operand
        ) or operand in [datetime_timedelta_type, datetime_datetime_type,
        pd_timestamp_type]
    return ksz__itj


def binary_array_cmp(lhs, rhs):
    return lhs == binary_array_type and rhs in [bytes_type, binary_array_type
        ] or lhs in [bytes_type, binary_array_type
        ] and rhs == binary_array_type


def can_cmp_date_datetime(lhs, rhs, op):
    return op in (operator.eq, operator.ne) and (lhs == datetime_date_type and
        rhs == datetime_datetime_type or lhs == datetime_datetime_type and 
        rhs == datetime_date_type)


def time_series_operation(lhs, rhs):
    eirks__xuwb = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == datetime_timedelta_type
    vrap__luyr = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == datetime_timedelta_type
    ddkth__scyxy = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
        ) and helper_time_series_checks(rhs)
    xks__zgu = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
        ) and helper_time_series_checks(lhs)
    return eirks__xuwb or vrap__luyr or ddkth__scyxy or xks__zgu


def args_td_and_int_array(lhs, rhs):
    vfsu__buxzm = (isinstance(lhs, IntegerArrayType) or isinstance(lhs,
        types.Array) and isinstance(lhs.dtype, types.Integer)) or (isinstance
        (rhs, IntegerArrayType) or isinstance(rhs, types.Array) and
        isinstance(rhs.dtype, types.Integer))
    gcvwd__skjk = lhs in [pd_timedelta_type] or rhs in [pd_timedelta_type]
    return vfsu__buxzm and gcvwd__skjk


def arith_op_supported_by_numba(op, lhs, rhs):
    if op == operator.mul:
        bvur__bozrv = isinstance(lhs, (types.Integer, types.Float)
            ) and isinstance(rhs, types.NPTimedelta)
        mnvz__hnje = isinstance(rhs, (types.Integer, types.Float)
            ) and isinstance(lhs, types.NPTimedelta)
        frncv__ordel = bvur__bozrv or mnvz__hnje
        rkc__ziux = isinstance(rhs, types.UnicodeType) and isinstance(lhs,
            types.Integer)
        wam__smkac = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.Integer)
        vhctv__kqbca = rkc__ziux or wam__smkac
        hik__elgm = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        dtxk__owrq = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        qizt__uqq = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        gdu__sumi = hik__elgm or dtxk__owrq or qizt__uqq
        xuzo__ngqd = isinstance(lhs, types.List) and isinstance(rhs, types.
            Integer) or isinstance(lhs, types.Integer) and isinstance(rhs,
            types.List)
        tys = types.UnicodeCharSeq, types.CharSeq, types.Bytes
        badk__akn = isinstance(lhs, tys) or isinstance(rhs, tys)
        vkozc__mbxr = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        return (frncv__ordel or vhctv__kqbca or gdu__sumi or xuzo__ngqd or
            badk__akn or vkozc__mbxr)
    if op == operator.pow:
        npl__hux = isinstance(lhs, types.Integer) and isinstance(rhs, (
            types.IntegerLiteral, types.Integer))
        ivsj__taxad = isinstance(lhs, types.Float) and isinstance(rhs, (
            types.IntegerLiteral, types.Float, types.Integer) or rhs in
            types.unsigned_domain or rhs in types.signed_domain)
        qizt__uqq = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        vkozc__mbxr = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        return npl__hux or ivsj__taxad or qizt__uqq or vkozc__mbxr
    if op == operator.floordiv:
        dtxk__owrq = lhs in types.real_domain and rhs in types.real_domain
        hik__elgm = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        ejbk__kwjs = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        osa__lyirq = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        vkozc__mbxr = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        return (dtxk__owrq or hik__elgm or ejbk__kwjs or osa__lyirq or
            vkozc__mbxr)
    if op == operator.truediv:
        jqs__qdgd = lhs in machine_ints and rhs in machine_ints
        dtxk__owrq = lhs in types.real_domain and rhs in types.real_domain
        qizt__uqq = lhs in types.complex_domain and rhs in types.complex_domain
        hik__elgm = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        ejbk__kwjs = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        uzctq__vhl = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        osa__lyirq = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        vkozc__mbxr = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        return (jqs__qdgd or dtxk__owrq or qizt__uqq or hik__elgm or
            ejbk__kwjs or uzctq__vhl or osa__lyirq or vkozc__mbxr)
    if op == operator.mod:
        jqs__qdgd = lhs in machine_ints and rhs in machine_ints
        dtxk__owrq = lhs in types.real_domain and rhs in types.real_domain
        hik__elgm = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        ejbk__kwjs = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        vkozc__mbxr = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        return (jqs__qdgd or dtxk__owrq or hik__elgm or ejbk__kwjs or
            vkozc__mbxr)
    if op == operator.add or op == operator.sub:
        frncv__ordel = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            types.NPTimedelta)
        brp__gjv = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPDatetime)
        lpv__oars = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPTimedelta)
        tnpip__eny = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
        hik__elgm = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        dtxk__owrq = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        qizt__uqq = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        gdu__sumi = hik__elgm or dtxk__owrq or qizt__uqq
        vkozc__mbxr = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        fyqpm__zcsyp = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
            types.BaseTuple)
        xuzo__ngqd = isinstance(lhs, types.List) and isinstance(rhs, types.List
            )
        ydf__tynwb = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeType)
        gqnrq__tausx = isinstance(rhs, types.UnicodeCharSeq) and isinstance(lhs
            , types.UnicodeType)
        rqky__omzj = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeCharSeq)
        hkray__puazh = isinstance(lhs, (types.CharSeq, types.Bytes)
            ) and isinstance(rhs, (types.CharSeq, types.Bytes))
        arjd__htmq = ydf__tynwb or gqnrq__tausx or rqky__omzj or hkray__puazh
        vhctv__kqbca = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeType)
        fhmsh__vyoc = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeCharSeq)
        gste__uvn = vhctv__kqbca or fhmsh__vyoc
        rpkp__ccp = lhs == types.NPTimedelta and rhs == types.NPDatetime
        gnh__oooeg = (fyqpm__zcsyp or xuzo__ngqd or arjd__htmq or gste__uvn or
            rpkp__ccp)
        lzj__hjexu = op == operator.add and gnh__oooeg
        return (frncv__ordel or brp__gjv or lpv__oars or tnpip__eny or
            gdu__sumi or vkozc__mbxr or lzj__hjexu)


def cmp_op_supported_by_numba(lhs, rhs):
    vkozc__mbxr = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
    xuzo__ngqd = isinstance(lhs, types.ListType) and isinstance(rhs, types.
        ListType)
    frncv__ordel = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
        types.NPTimedelta)
    entn__vpfgj = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
        types.NPDatetime)
    unicode_types = (types.UnicodeType, types.StringLiteral, types.CharSeq,
        types.Bytes, types.UnicodeCharSeq)
    vhctv__kqbca = isinstance(lhs, unicode_types) and isinstance(rhs,
        unicode_types)
    fyqpm__zcsyp = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
        types.BaseTuple)
    tnpip__eny = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
    gdu__sumi = isinstance(lhs, types.Number) and isinstance(rhs, types.Number)
    sbqa__zrvr = isinstance(lhs, types.Boolean) and isinstance(rhs, types.
        Boolean)
    jumzp__ousi = isinstance(lhs, types.NoneType) or isinstance(rhs, types.
        NoneType)
    chfbb__bxf = isinstance(lhs, types.DictType) and isinstance(rhs, types.
        DictType)
    xftp__ektg = isinstance(lhs, types.EnumMember) and isinstance(rhs,
        types.EnumMember)
    bjf__pbag = isinstance(lhs, types.Literal) and isinstance(rhs, types.
        Literal)
    return (xuzo__ngqd or frncv__ordel or entn__vpfgj or vhctv__kqbca or
        fyqpm__zcsyp or tnpip__eny or gdu__sumi or sbqa__zrvr or
        jumzp__ousi or chfbb__bxf or vkozc__mbxr or xftp__ektg or bjf__pbag)


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
        wohj__ect = create_overload_cmp_operator(op)
        overload(op, no_unliteral=True)(wohj__ect)


_install_cmp_ops()


def install_arith_ops():
    for op in (operator.add, operator.sub, operator.mul, operator.truediv,
        operator.floordiv, operator.mod, operator.pow):
        wohj__ect = create_overload_arith_op(op)
        overload(op, no_unliteral=True)(wohj__ect)


install_arith_ops()
