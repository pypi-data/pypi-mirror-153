"""
Helper functions for transformations.
"""
import itertools
import math
import operator
import types as pytypes
from collections import namedtuple
import numba
import numpy as np
import pandas as pd
from numba.core import ir, ir_utils, types
from numba.core.ir_utils import GuardException, build_definitions, compile_to_numba_ir, compute_cfg_from_blocks, find_callname, find_const, get_definition, guard, is_setitem, mk_unique_var, replace_arg_nodes, require
from numba.core.registry import CPUDispatcher
from numba.core.typing.templates import fold_arguments
import bodo
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.struct_arr_ext import StructArrayType, StructType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.typing import BodoConstUpdatedError, BodoError, can_literalize_type, get_literal_value, get_overload_const_bool, get_overload_const_list, is_literal_type, is_overload_constant_bool
from bodo.utils.utils import is_array_typ, is_assign, is_call, is_expr
ReplaceFunc = namedtuple('ReplaceFunc', ['func', 'arg_types', 'args',
    'glbls', 'inline_bodo_calls', 'run_full_pipeline', 'pre_nodes'])
bodo_types_with_params = {'ArrayItemArrayType', 'CSRMatrixType',
    'CategoricalArrayType', 'CategoricalIndexType', 'DataFrameType',
    'DatetimeIndexType', 'Decimal128Type', 'DecimalArrayType',
    'IntegerArrayType', 'IntervalArrayType', 'IntervalIndexType', 'List',
    'MapArrayType', 'NumericIndexType', 'PDCategoricalDtype',
    'PeriodIndexType', 'RangeIndexType', 'SeriesType', 'StringIndexType',
    'BinaryIndexType', 'StructArrayType', 'TimedeltaIndexType',
    'TupleArrayType'}
container_update_method_names = ('clear', 'pop', 'popitem', 'update', 'add',
    'difference_update', 'discard', 'intersection_update', 'remove',
    'symmetric_difference_update', 'append', 'extend', 'insert', 'reverse',
    'sort')
no_side_effect_call_tuples = {(int,), (list,), (set,), (dict,), (min,), (
    max,), (abs,), (len,), (bool,), (str,), ('ceil', math), ('init_series',
    'pd_series_ext', 'hiframes', bodo), ('get_series_data', 'pd_series_ext',
    'hiframes', bodo), ('get_series_index', 'pd_series_ext', 'hiframes',
    bodo), ('get_series_name', 'pd_series_ext', 'hiframes', bodo), (
    'get_index_data', 'pd_index_ext', 'hiframes', bodo), ('get_index_name',
    'pd_index_ext', 'hiframes', bodo), ('init_binary_str_index',
    'pd_index_ext', 'hiframes', bodo), ('init_numeric_index',
    'pd_index_ext', 'hiframes', bodo), ('init_categorical_index',
    'pd_index_ext', 'hiframes', bodo), ('_dti_val_finalize', 'pd_index_ext',
    'hiframes', bodo), ('init_datetime_index', 'pd_index_ext', 'hiframes',
    bodo), ('init_timedelta_index', 'pd_index_ext', 'hiframes', bodo), (
    'init_range_index', 'pd_index_ext', 'hiframes', bodo), (
    'init_heter_index', 'pd_index_ext', 'hiframes', bodo), (
    'get_int_arr_data', 'int_arr_ext', 'libs', bodo), ('get_int_arr_bitmap',
    'int_arr_ext', 'libs', bodo), ('init_integer_array', 'int_arr_ext',
    'libs', bodo), ('alloc_int_array', 'int_arr_ext', 'libs', bodo), (
    'inplace_eq', 'str_arr_ext', 'libs', bodo), ('get_bool_arr_data',
    'bool_arr_ext', 'libs', bodo), ('get_bool_arr_bitmap', 'bool_arr_ext',
    'libs', bodo), ('init_bool_array', 'bool_arr_ext', 'libs', bodo), (
    'alloc_bool_array', 'bool_arr_ext', 'libs', bodo), (
    'datetime_date_arr_to_dt64_arr', 'pd_timestamp_ext', 'hiframes', bodo),
    (bodo.libs.bool_arr_ext.compute_or_body,), (bodo.libs.bool_arr_ext.
    compute_and_body,), ('alloc_datetime_date_array', 'datetime_date_ext',
    'hiframes', bodo), ('alloc_datetime_timedelta_array',
    'datetime_timedelta_ext', 'hiframes', bodo), ('cat_replace',
    'pd_categorical_ext', 'hiframes', bodo), ('init_categorical_array',
    'pd_categorical_ext', 'hiframes', bodo), ('alloc_categorical_array',
    'pd_categorical_ext', 'hiframes', bodo), ('get_categorical_arr_codes',
    'pd_categorical_ext', 'hiframes', bodo), ('_sum_handle_nan',
    'series_kernels', 'hiframes', bodo), ('_box_cat_val', 'series_kernels',
    'hiframes', bodo), ('_mean_handle_nan', 'series_kernels', 'hiframes',
    bodo), ('_var_handle_mincount', 'series_kernels', 'hiframes', bodo), (
    '_compute_var_nan_count_ddof', 'series_kernels', 'hiframes', bodo), (
    '_sem_handle_nan', 'series_kernels', 'hiframes', bodo), ('dist_return',
    'distributed_api', 'libs', bodo), ('rep_return', 'distributed_api',
    'libs', bodo), ('init_dataframe', 'pd_dataframe_ext', 'hiframes', bodo),
    ('get_dataframe_data', 'pd_dataframe_ext', 'hiframes', bodo), (
    'get_dataframe_table', 'pd_dataframe_ext', 'hiframes', bodo), (
    'get_dataframe_column_names', 'pd_dataframe_ext', 'hiframes', bodo), (
    'get_table_data', 'table', 'hiframes', bodo), ('get_dataframe_index',
    'pd_dataframe_ext', 'hiframes', bodo), ('init_rolling',
    'pd_rolling_ext', 'hiframes', bodo), ('init_groupby', 'pd_groupby_ext',
    'hiframes', bodo), ('calc_nitems', 'array_kernels', 'libs', bodo), (
    'concat', 'array_kernels', 'libs', bodo), ('unique', 'array_kernels',
    'libs', bodo), ('nunique', 'array_kernels', 'libs', bodo), ('quantile',
    'array_kernels', 'libs', bodo), ('explode', 'array_kernels', 'libs',
    bodo), ('explode_no_index', 'array_kernels', 'libs', bodo), (
    'get_arr_lens', 'array_kernels', 'libs', bodo), (
    'str_arr_from_sequence', 'str_arr_ext', 'libs', bodo), (
    'get_str_arr_str_length', 'str_arr_ext', 'libs', bodo), (
    'parse_datetime_str', 'pd_timestamp_ext', 'hiframes', bodo), (
    'integer_to_dt64', 'pd_timestamp_ext', 'hiframes', bodo), (
    'dt64_to_integer', 'pd_timestamp_ext', 'hiframes', bodo), (
    'timedelta64_to_integer', 'pd_timestamp_ext', 'hiframes', bodo), (
    'integer_to_timedelta64', 'pd_timestamp_ext', 'hiframes', bodo), (
    'npy_datetimestruct_to_datetime', 'pd_timestamp_ext', 'hiframes', bodo),
    ('isna', 'array_kernels', 'libs', bodo), ('copy',), (
    'from_iterable_impl', 'typing', 'utils', bodo), ('chain', itertools), (
    'groupby',), ('rolling',), (pd.CategoricalDtype,), (bodo.hiframes.
    pd_categorical_ext.get_code_for_value,), ('asarray', np), ('int32', np),
    ('int64', np), ('float64', np), ('float32', np), ('bool_', np), ('full',
    np), ('round', np), ('isnan', np), ('isnat', np), ('arange', np), (
    'internal_prange', 'parfor', numba), ('internal_prange', 'parfor',
    'parfors', numba), ('empty_inferred', 'ndarray', 'unsafe', numba), (
    '_slice_span', 'unicode', numba), ('_normalize_slice', 'unicode', numba
    ), ('init_session_builder', 'pyspark_ext', 'libs', bodo), (
    'init_session', 'pyspark_ext', 'libs', bodo), ('init_spark_df',
    'pyspark_ext', 'libs', bodo), ('h5size', 'h5_api', 'io', bodo), (
    'pre_alloc_struct_array', 'struct_arr_ext', 'libs', bodo), (bodo.libs.
    struct_arr_ext.pre_alloc_struct_array,), ('pre_alloc_tuple_array',
    'tuple_arr_ext', 'libs', bodo), (bodo.libs.tuple_arr_ext.
    pre_alloc_tuple_array,), ('pre_alloc_array_item_array',
    'array_item_arr_ext', 'libs', bodo), (bodo.libs.array_item_arr_ext.
    pre_alloc_array_item_array,), ('dist_reduce', 'distributed_api', 'libs',
    bodo), (bodo.libs.distributed_api.dist_reduce,), (
    'pre_alloc_string_array', 'str_arr_ext', 'libs', bodo), (bodo.libs.
    str_arr_ext.pre_alloc_string_array,), ('pre_alloc_binary_array',
    'binary_arr_ext', 'libs', bodo), (bodo.libs.binary_arr_ext.
    pre_alloc_binary_array,), ('pre_alloc_map_array', 'map_arr_ext', 'libs',
    bodo), (bodo.libs.map_arr_ext.pre_alloc_map_array,), (
    'convert_dict_arr_to_int', 'dict_arr_ext', 'libs', bodo), (
    'cat_dict_str', 'dict_arr_ext', 'libs', bodo), ('str_replace',
    'dict_arr_ext', 'libs', bodo), ('dict_arr_eq', 'dict_arr_ext', 'libs',
    bodo), ('dict_arr_ne', 'dict_arr_ext', 'libs', bodo), ('str_startswith',
    'dict_arr_ext', 'libs', bodo), ('str_endswith', 'dict_arr_ext', 'libs',
    bodo), ('str_contains_non_regex', 'dict_arr_ext', 'libs', bodo), (
    'str_series_contains_regex', 'dict_arr_ext', 'libs', bodo), (
    'str_capitalize', 'dict_arr_ext', 'libs', bodo), ('str_lower',
    'dict_arr_ext', 'libs', bodo), ('str_swapcase', 'dict_arr_ext', 'libs',
    bodo), ('str_title', 'dict_arr_ext', 'libs', bodo), ('str_upper',
    'dict_arr_ext', 'libs', bodo), ('str_center', 'dict_arr_ext', 'libs',
    bodo), ('str_get', 'dict_arr_ext', 'libs', bodo), ('str_repeat_int',
    'dict_arr_ext', 'libs', bodo), ('str_lstrip', 'dict_arr_ext', 'libs',
    bodo), ('str_rstrip', 'dict_arr_ext', 'libs', bodo), ('str_strip',
    'dict_arr_ext', 'libs', bodo), ('str_zfill', 'dict_arr_ext', 'libs',
    bodo), ('str_ljust', 'dict_arr_ext', 'libs', bodo), ('str_rjust',
    'dict_arr_ext', 'libs', bodo), ('str_find', 'dict_arr_ext', 'libs',
    bodo), ('str_slice', 'dict_arr_ext', 'libs', bodo), ('prange', bodo), (
    bodo.prange,), ('objmode', bodo), (bodo.objmode,), (
    'get_label_dict_from_categories', 'pd_categorial_ext', 'hiframes', bodo
    ), ('get_label_dict_from_categories_no_duplicates', 'pd_categorial_ext',
    'hiframes', bodo), ('build_nullable_tuple', 'nullable_tuple_ext',
    'libs', bodo), ('generate_mappable_table_func', 'table_utils', 'utils',
    bodo)}


def remove_hiframes(rhs, lives, call_list):
    gyrmu__fmr = tuple(call_list)
    if gyrmu__fmr in no_side_effect_call_tuples:
        return True
    if gyrmu__fmr == (bodo.hiframes.pd_index_ext.init_range_index,):
        return True
    if len(call_list) == 4 and call_list[1:] == ['conversion', 'utils', bodo]:
        return True
    if isinstance(call_list[-1], pytypes.ModuleType) and call_list[-1
        ].__name__ == 'bodosql':
        return True
    if len(call_list) == 2 and call_list[0] == 'copy':
        return True
    if call_list == ['h5read', 'h5_api', 'io', bodo] and rhs.args[5
        ].name not in lives:
        return True
    if call_list == ['move_str_binary_arr_payload', 'str_arr_ext', 'libs', bodo
        ] and rhs.args[0].name not in lives:
        return True
    if call_list == ['setna', 'array_kernels', 'libs', bodo] and rhs.args[0
        ].name not in lives:
        return True
    if call_list == ['set_table_data', 'table', 'hiframes', bodo] and rhs.args[
        0].name not in lives:
        return True
    if call_list == ['ensure_column_unboxed', 'table', 'hiframes', bodo
        ] and rhs.args[0].name not in lives and rhs.args[1].name not in lives:
        return True
    if call_list == ['generate_table_nbytes', 'table_utils', 'utils', bodo
        ] and rhs.args[1].name not in lives:
        return True
    if len(gyrmu__fmr) == 1 and tuple in getattr(gyrmu__fmr[0], '__mro__', ()):
        return True
    return False


numba.core.ir_utils.remove_call_handlers.append(remove_hiframes)


def compile_func_single_block(func, args, ret_var, typing_info=None,
    extra_globals=None, infer_types=True, run_untyped_pass=False, flags=
    None, replace_globals=True):
    xars__hhmn = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd, 'math':
        math}
    if extra_globals is not None:
        xars__hhmn.update(extra_globals)
    if not replace_globals:
        xars__hhmn = func.__globals__
    loc = ir.Loc('', 0)
    if ret_var:
        loc = ret_var.loc
    if typing_info and infer_types:
        loc = typing_info.curr_loc
        f_ir = compile_to_numba_ir(func, xars__hhmn, typingctx=typing_info.
            typingctx, targetctx=typing_info.targetctx, arg_typs=tuple(
            typing_info.typemap[jfxeb__yqgjz.name] for jfxeb__yqgjz in args
            ), typemap=typing_info.typemap, calltypes=typing_info.calltypes)
    else:
        f_ir = compile_to_numba_ir(func, xars__hhmn)
    assert len(f_ir.blocks
        ) == 1, 'only single block functions supported in compile_func_single_block()'
    if run_untyped_pass:
        mmbo__dnq = tuple(typing_info.typemap[jfxeb__yqgjz.name] for
            jfxeb__yqgjz in args)
        twi__gowx = bodo.transforms.untyped_pass.UntypedPass(f_ir,
            typing_info.typingctx, mmbo__dnq, {}, {}, flags)
        twi__gowx.run()
    gck__ett = f_ir.blocks.popitem()[1]
    replace_arg_nodes(gck__ett, args)
    kxw__rudz = gck__ett.body[:-2]
    update_locs(kxw__rudz[len(args):], loc)
    for stmt in kxw__rudz[:len(args)]:
        stmt.target.loc = loc
    if ret_var is not None:
        kov__idfst = gck__ett.body[-2]
        assert is_assign(kov__idfst) and is_expr(kov__idfst.value, 'cast')
        kmt__ywy = kov__idfst.value.value
        kxw__rudz.append(ir.Assign(kmt__ywy, ret_var, loc))
    return kxw__rudz


def update_locs(node_list, loc):
    for stmt in node_list:
        stmt.loc = loc
        for jwq__dlnr in stmt.list_vars():
            jwq__dlnr.loc = loc
        if is_assign(stmt):
            stmt.value.loc = loc


def get_stmt_defs(stmt):
    if is_assign(stmt):
        return set([stmt.target.name])
    if type(stmt) in numba.core.analysis.ir_extension_usedefs:
        ipvv__fdtr = numba.core.analysis.ir_extension_usedefs[type(stmt)]
        lek__jrawa, xztm__yfrw = ipvv__fdtr(stmt)
        return xztm__yfrw
    return set()


def get_const_value(var, func_ir, err_msg, typemap=None, arg_types=None,
    file_info=None):
    if hasattr(var, 'loc'):
        loc = var.loc
    else:
        loc = None
    try:
        iir__spafa = get_const_value_inner(func_ir, var, arg_types, typemap,
            file_info=file_info)
        if isinstance(iir__spafa, ir.UndefinedType):
            jidv__iwkzk = func_ir.get_definition(var.name).name
            raise BodoError(f"name '{jidv__iwkzk}' is not defined", loc=loc)
    except GuardException as xsrd__zqgyb:
        raise BodoError(err_msg, loc=loc)
    return iir__spafa


def get_const_value_inner(func_ir, var, arg_types=None, typemap=None,
    updated_containers=None, file_info=None, pyobject_to_literal=False,
    literalize_args=True):
    require(isinstance(var, ir.Var))
    hpvrq__uhl = get_definition(func_ir, var)
    cjjn__cpeva = None
    if typemap is not None:
        cjjn__cpeva = typemap.get(var.name, None)
    if isinstance(hpvrq__uhl, ir.Arg) and arg_types is not None:
        cjjn__cpeva = arg_types[hpvrq__uhl.index]
    if updated_containers and var.name in updated_containers:
        raise BodoConstUpdatedError(
            f"variable '{var.name}' is updated inplace using '{updated_containers[var.name]}'"
            )
    if is_literal_type(cjjn__cpeva):
        return get_literal_value(cjjn__cpeva)
    if isinstance(hpvrq__uhl, (ir.Const, ir.Global, ir.FreeVar)):
        iir__spafa = hpvrq__uhl.value
        return iir__spafa
    if literalize_args and isinstance(hpvrq__uhl, ir.Arg
        ) and can_literalize_type(cjjn__cpeva, pyobject_to_literal):
        raise numba.core.errors.ForceLiteralArg({hpvrq__uhl.index}, loc=var
            .loc, file_infos={hpvrq__uhl.index: file_info} if file_info is not
            None else None)
    if is_expr(hpvrq__uhl, 'binop'):
        if file_info and hpvrq__uhl.fn == operator.add:
            try:
                hvwv__jrorb = get_const_value_inner(func_ir, hpvrq__uhl.lhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(hvwv__jrorb, True)
                livrr__fbt = get_const_value_inner(func_ir, hpvrq__uhl.rhs,
                    arg_types, typemap, updated_containers, file_info)
                return hpvrq__uhl.fn(hvwv__jrorb, livrr__fbt)
            except (GuardException, BodoConstUpdatedError) as xsrd__zqgyb:
                pass
            try:
                livrr__fbt = get_const_value_inner(func_ir, hpvrq__uhl.rhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(livrr__fbt, False)
                hvwv__jrorb = get_const_value_inner(func_ir, hpvrq__uhl.lhs,
                    arg_types, typemap, updated_containers, file_info)
                return hpvrq__uhl.fn(hvwv__jrorb, livrr__fbt)
            except (GuardException, BodoConstUpdatedError) as xsrd__zqgyb:
                pass
        hvwv__jrorb = get_const_value_inner(func_ir, hpvrq__uhl.lhs,
            arg_types, typemap, updated_containers)
        livrr__fbt = get_const_value_inner(func_ir, hpvrq__uhl.rhs,
            arg_types, typemap, updated_containers)
        return hpvrq__uhl.fn(hvwv__jrorb, livrr__fbt)
    if is_expr(hpvrq__uhl, 'unary'):
        iir__spafa = get_const_value_inner(func_ir, hpvrq__uhl.value,
            arg_types, typemap, updated_containers)
        return hpvrq__uhl.fn(iir__spafa)
    if is_expr(hpvrq__uhl, 'getattr') and typemap:
        ejb__xwkx = typemap.get(hpvrq__uhl.value.name, None)
        if isinstance(ejb__xwkx, bodo.hiframes.pd_dataframe_ext.DataFrameType
            ) and hpvrq__uhl.attr == 'columns':
            return pd.Index(ejb__xwkx.columns)
        if isinstance(ejb__xwkx, types.SliceType):
            dxy__njdb = get_definition(func_ir, hpvrq__uhl.value)
            require(is_call(dxy__njdb))
            ipirc__bkoua = find_callname(func_ir, dxy__njdb)
            pnswi__thu = False
            if ipirc__bkoua == ('_normalize_slice', 'numba.cpython.unicode'):
                require(hpvrq__uhl.attr in ('start', 'step'))
                dxy__njdb = get_definition(func_ir, dxy__njdb.args[0])
                pnswi__thu = True
            require(find_callname(func_ir, dxy__njdb) == ('slice', 'builtins'))
            if len(dxy__njdb.args) == 1:
                if hpvrq__uhl.attr == 'start':
                    return 0
                if hpvrq__uhl.attr == 'step':
                    return 1
                require(hpvrq__uhl.attr == 'stop')
                return get_const_value_inner(func_ir, dxy__njdb.args[0],
                    arg_types, typemap, updated_containers)
            if hpvrq__uhl.attr == 'start':
                iir__spafa = get_const_value_inner(func_ir, dxy__njdb.args[
                    0], arg_types, typemap, updated_containers)
                if iir__spafa is None:
                    iir__spafa = 0
                if pnswi__thu:
                    require(iir__spafa == 0)
                return iir__spafa
            if hpvrq__uhl.attr == 'stop':
                assert not pnswi__thu
                return get_const_value_inner(func_ir, dxy__njdb.args[1],
                    arg_types, typemap, updated_containers)
            require(hpvrq__uhl.attr == 'step')
            if len(dxy__njdb.args) == 2:
                return 1
            else:
                iir__spafa = get_const_value_inner(func_ir, dxy__njdb.args[
                    2], arg_types, typemap, updated_containers)
                if iir__spafa is None:
                    iir__spafa = 1
                if pnswi__thu:
                    require(iir__spafa == 1)
                return iir__spafa
    if is_expr(hpvrq__uhl, 'getattr'):
        return getattr(get_const_value_inner(func_ir, hpvrq__uhl.value,
            arg_types, typemap, updated_containers), hpvrq__uhl.attr)
    if is_expr(hpvrq__uhl, 'getitem'):
        value = get_const_value_inner(func_ir, hpvrq__uhl.value, arg_types,
            typemap, updated_containers)
        index = get_const_value_inner(func_ir, hpvrq__uhl.index, arg_types,
            typemap, updated_containers)
        return value[index]
    auaml__osr = guard(find_callname, func_ir, hpvrq__uhl, typemap)
    if auaml__osr is not None and len(auaml__osr) == 2 and auaml__osr[0
        ] == 'keys' and isinstance(auaml__osr[1], ir.Var):
        zjtbk__lscfz = hpvrq__uhl.func
        hpvrq__uhl = get_definition(func_ir, auaml__osr[1])
        cqbv__wntpv = auaml__osr[1].name
        if updated_containers and cqbv__wntpv in updated_containers:
            raise BodoConstUpdatedError(
                "variable '{}' is updated inplace using '{}'".format(
                cqbv__wntpv, updated_containers[cqbv__wntpv]))
        require(is_expr(hpvrq__uhl, 'build_map'))
        vals = [jwq__dlnr[0] for jwq__dlnr in hpvrq__uhl.items]
        sgsm__fhv = guard(get_definition, func_ir, zjtbk__lscfz)
        assert isinstance(sgsm__fhv, ir.Expr) and sgsm__fhv.attr == 'keys'
        sgsm__fhv.attr = 'copy'
        return [get_const_value_inner(func_ir, jwq__dlnr, arg_types,
            typemap, updated_containers) for jwq__dlnr in vals]
    if is_expr(hpvrq__uhl, 'build_map'):
        return {get_const_value_inner(func_ir, jwq__dlnr[0], arg_types,
            typemap, updated_containers): get_const_value_inner(func_ir,
            jwq__dlnr[1], arg_types, typemap, updated_containers) for
            jwq__dlnr in hpvrq__uhl.items}
    if is_expr(hpvrq__uhl, 'build_tuple'):
        return tuple(get_const_value_inner(func_ir, jwq__dlnr, arg_types,
            typemap, updated_containers) for jwq__dlnr in hpvrq__uhl.items)
    if is_expr(hpvrq__uhl, 'build_list'):
        return [get_const_value_inner(func_ir, jwq__dlnr, arg_types,
            typemap, updated_containers) for jwq__dlnr in hpvrq__uhl.items]
    if is_expr(hpvrq__uhl, 'build_set'):
        return {get_const_value_inner(func_ir, jwq__dlnr, arg_types,
            typemap, updated_containers) for jwq__dlnr in hpvrq__uhl.items}
    if auaml__osr == ('list', 'builtins'):
        values = get_const_value_inner(func_ir, hpvrq__uhl.args[0],
            arg_types, typemap, updated_containers)
        if isinstance(values, set):
            values = sorted(values)
        return list(values)
    if auaml__osr == ('set', 'builtins'):
        return set(get_const_value_inner(func_ir, hpvrq__uhl.args[0],
            arg_types, typemap, updated_containers))
    if auaml__osr == ('range', 'builtins') and len(hpvrq__uhl.args) == 1:
        return range(get_const_value_inner(func_ir, hpvrq__uhl.args[0],
            arg_types, typemap, updated_containers))
    if auaml__osr == ('slice', 'builtins'):
        return slice(*tuple(get_const_value_inner(func_ir, jwq__dlnr,
            arg_types, typemap, updated_containers) for jwq__dlnr in
            hpvrq__uhl.args))
    if auaml__osr == ('str', 'builtins'):
        return str(get_const_value_inner(func_ir, hpvrq__uhl.args[0],
            arg_types, typemap, updated_containers))
    if auaml__osr == ('bool', 'builtins'):
        return bool(get_const_value_inner(func_ir, hpvrq__uhl.args[0],
            arg_types, typemap, updated_containers))
    if auaml__osr == ('format', 'builtins'):
        jfxeb__yqgjz = get_const_value_inner(func_ir, hpvrq__uhl.args[0],
            arg_types, typemap, updated_containers)
        kwm__txhv = get_const_value_inner(func_ir, hpvrq__uhl.args[1],
            arg_types, typemap, updated_containers) if len(hpvrq__uhl.args
            ) > 1 else ''
        return format(jfxeb__yqgjz, kwm__txhv)
    if auaml__osr in (('init_binary_str_index',
        'bodo.hiframes.pd_index_ext'), ('init_numeric_index',
        'bodo.hiframes.pd_index_ext'), ('init_categorical_index',
        'bodo.hiframes.pd_index_ext'), ('init_datetime_index',
        'bodo.hiframes.pd_index_ext'), ('init_timedelta_index',
        'bodo.hiframes.pd_index_ext'), ('init_heter_index',
        'bodo.hiframes.pd_index_ext')):
        return pd.Index(get_const_value_inner(func_ir, hpvrq__uhl.args[0],
            arg_types, typemap, updated_containers))
    if auaml__osr == ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'):
        return np.array(get_const_value_inner(func_ir, hpvrq__uhl.args[0],
            arg_types, typemap, updated_containers))
    if auaml__osr == ('init_range_index', 'bodo.hiframes.pd_index_ext'):
        return pd.RangeIndex(get_const_value_inner(func_ir, hpvrq__uhl.args
            [0], arg_types, typemap, updated_containers),
            get_const_value_inner(func_ir, hpvrq__uhl.args[1], arg_types,
            typemap, updated_containers), get_const_value_inner(func_ir,
            hpvrq__uhl.args[2], arg_types, typemap, updated_containers))
    if auaml__osr == ('len', 'builtins') and typemap and isinstance(typemap
        .get(hpvrq__uhl.args[0].name, None), types.BaseTuple):
        return len(typemap[hpvrq__uhl.args[0].name])
    if auaml__osr == ('len', 'builtins'):
        nedv__tqxcv = guard(get_definition, func_ir, hpvrq__uhl.args[0])
        if isinstance(nedv__tqxcv, ir.Expr) and nedv__tqxcv.op in (
            'build_tuple', 'build_list', 'build_set', 'build_map'):
            return len(nedv__tqxcv.items)
        return len(get_const_value_inner(func_ir, hpvrq__uhl.args[0],
            arg_types, typemap, updated_containers))
    if auaml__osr == ('CategoricalDtype', 'pandas'):
        kws = dict(hpvrq__uhl.kws)
        qclg__mtngq = get_call_expr_arg('CategoricalDtype', hpvrq__uhl.args,
            kws, 0, 'categories', '')
        cox__jlzu = get_call_expr_arg('CategoricalDtype', hpvrq__uhl.args,
            kws, 1, 'ordered', False)
        if cox__jlzu is not False:
            cox__jlzu = get_const_value_inner(func_ir, cox__jlzu, arg_types,
                typemap, updated_containers)
        if qclg__mtngq == '':
            qclg__mtngq = None
        else:
            qclg__mtngq = get_const_value_inner(func_ir, qclg__mtngq,
                arg_types, typemap, updated_containers)
        return pd.CategoricalDtype(qclg__mtngq, cox__jlzu)
    if auaml__osr == ('dtype', 'numpy'):
        return np.dtype(get_const_value_inner(func_ir, hpvrq__uhl.args[0],
            arg_types, typemap, updated_containers))
    if auaml__osr is not None and len(auaml__osr) == 2 and auaml__osr[1
        ] == 'pandas' and auaml__osr[0] in ('Int8Dtype', 'Int16Dtype',
        'Int32Dtype', 'Int64Dtype', 'UInt8Dtype', 'UInt16Dtype',
        'UInt32Dtype', 'UInt64Dtype'):
        return getattr(pd, auaml__osr[0])()
    if auaml__osr is not None and len(auaml__osr) == 2 and isinstance(
        auaml__osr[1], ir.Var):
        iir__spafa = get_const_value_inner(func_ir, auaml__osr[1],
            arg_types, typemap, updated_containers)
        args = [get_const_value_inner(func_ir, jwq__dlnr, arg_types,
            typemap, updated_containers) for jwq__dlnr in hpvrq__uhl.args]
        kws = {wgrkf__han[0]: get_const_value_inner(func_ir, wgrkf__han[1],
            arg_types, typemap, updated_containers) for wgrkf__han in
            hpvrq__uhl.kws}
        return getattr(iir__spafa, auaml__osr[0])(*args, **kws)
    if auaml__osr is not None and len(auaml__osr) == 2 and auaml__osr[1
        ] == 'bodo' and auaml__osr[0] in bodo_types_with_params:
        args = tuple(get_const_value_inner(func_ir, jwq__dlnr, arg_types,
            typemap, updated_containers) for jwq__dlnr in hpvrq__uhl.args)
        kwargs = {jidv__iwkzk: get_const_value_inner(func_ir, jwq__dlnr,
            arg_types, typemap, updated_containers) for jidv__iwkzk,
            jwq__dlnr in dict(hpvrq__uhl.kws).items()}
        return getattr(bodo, auaml__osr[0])(*args, **kwargs)
    if is_call(hpvrq__uhl) and typemap and isinstance(typemap.get(
        hpvrq__uhl.func.name, None), types.Dispatcher):
        py_func = typemap[hpvrq__uhl.func.name].dispatcher.py_func
        require(hpvrq__uhl.vararg is None)
        args = tuple(get_const_value_inner(func_ir, jwq__dlnr, arg_types,
            typemap, updated_containers) for jwq__dlnr in hpvrq__uhl.args)
        kwargs = {jidv__iwkzk: get_const_value_inner(func_ir, jwq__dlnr,
            arg_types, typemap, updated_containers) for jidv__iwkzk,
            jwq__dlnr in dict(hpvrq__uhl.kws).items()}
        arg_types = tuple(bodo.typeof(jwq__dlnr) for jwq__dlnr in args)
        kw_types = {igb__wiemo: bodo.typeof(jwq__dlnr) for igb__wiemo,
            jwq__dlnr in kwargs.items()}
        require(_func_is_pure(py_func, arg_types, kw_types))
        return py_func(*args, **kwargs)
    raise GuardException('Constant value not found')


def _func_is_pure(py_func, arg_types, kw_types):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    from bodo.hiframes.pd_series_ext import SeriesType
    from bodo.ir.csv_ext import CsvReader
    from bodo.ir.json_ext import JsonReader
    from bodo.ir.parquet_ext import ParquetReader
    from bodo.ir.sql_ext import SqlReader
    f_ir, typemap, unutk__igaqa, unutk__igaqa = (bodo.compiler.
        get_func_type_info(py_func, arg_types, kw_types))
    for block in f_ir.blocks.values():
        for stmt in block.body:
            if isinstance(stmt, ir.Print):
                return False
            if isinstance(stmt, (CsvReader, JsonReader, ParquetReader,
                SqlReader)):
                return False
            if is_setitem(stmt) and isinstance(guard(get_definition, f_ir,
                stmt.target), ir.Arg):
                return False
            if is_assign(stmt):
                rhs = stmt.value
                if isinstance(rhs, ir.Yield):
                    return False
                if is_call(rhs):
                    zcxvz__xuxx = guard(get_definition, f_ir, rhs.func)
                    if isinstance(zcxvz__xuxx, ir.Const) and isinstance(
                        zcxvz__xuxx.value, numba.core.dispatcher.
                        ObjModeLiftedWith):
                        return False
                    xmkf__ewg = guard(find_callname, f_ir, rhs)
                    if xmkf__ewg is None:
                        return False
                    func_name, dutm__ozluq = xmkf__ewg
                    if dutm__ozluq == 'pandas' and func_name.startswith('read_'
                        ):
                        return False
                    if xmkf__ewg in (('fromfile', 'numpy'), ('file_read',
                        'bodo.io.np_io')):
                        return False
                    if xmkf__ewg == ('File', 'h5py'):
                        return False
                    if isinstance(dutm__ozluq, ir.Var):
                        cjjn__cpeva = typemap[dutm__ozluq.name]
                        if isinstance(cjjn__cpeva, (DataFrameType, SeriesType)
                            ) and func_name in ('to_csv', 'to_excel',
                            'to_json', 'to_sql', 'to_pickle', 'to_parquet',
                            'info'):
                            return False
                        if isinstance(cjjn__cpeva, types.Array
                            ) and func_name == 'tofile':
                            return False
                        if isinstance(cjjn__cpeva, bodo.LoggingLoggerType):
                            return False
                        if str(cjjn__cpeva).startswith('Mpl'):
                            return False
                        if (func_name in container_update_method_names and
                            isinstance(guard(get_definition, f_ir,
                            dutm__ozluq), ir.Arg)):
                            return False
                    if dutm__ozluq in ('numpy.random', 'time', 'logging',
                        'matplotlib.pyplot'):
                        return False
    return True


def fold_argument_types(pysig, args, kws):

    def normal_handler(index, param, value):
        return value

    def default_handler(index, param, default):
        return types.Omitted(default)

    def stararg_handler(index, param, values):
        return types.StarArgTuple(values)
    args = fold_arguments(pysig, args, kws, normal_handler, default_handler,
        stararg_handler)
    return args


def get_const_func_output_type(func, arg_types, kw_types, typing_context,
    target_context, is_udf=True):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
    py_func = None
    if isinstance(func, types.MakeFunctionLiteral):
        lyp__zrzgg = func.literal_value.code
        npan__qcfy = {'np': np, 'pd': pd, 'numba': numba, 'bodo': bodo}
        if hasattr(func.literal_value, 'globals'):
            npan__qcfy = func.literal_value.globals
        f_ir = numba.core.ir_utils.get_ir_of_code(npan__qcfy, lyp__zrzgg)
        fix_struct_return(f_ir)
        typemap, nvx__xvojc, rhg__fyrwf, unutk__igaqa = (numba.core.
            typed_passes.type_inference_stage(typing_context,
            target_context, f_ir, arg_types, None))
    elif isinstance(func, bodo.utils.typing.FunctionLiteral):
        py_func = func.literal_value
        f_ir, typemap, rhg__fyrwf, nvx__xvojc = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    elif isinstance(func, CPUDispatcher):
        py_func = func.py_func
        f_ir, typemap, rhg__fyrwf, nvx__xvojc = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    else:
        if not isinstance(func, types.Dispatcher):
            if isinstance(func, types.Function):
                raise BodoError(
                    f'Bodo does not support built-in functions yet, {func}')
            else:
                raise BodoError(f'Function type expected, not {func}')
        py_func = func.dispatcher.py_func
        f_ir, typemap, rhg__fyrwf, nvx__xvojc = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    if is_udf and isinstance(nvx__xvojc, types.DictType):
        ojnmj__jwp = guard(get_struct_keynames, f_ir, typemap)
        if ojnmj__jwp is not None:
            nvx__xvojc = StructType((nvx__xvojc.value_type,) * len(
                ojnmj__jwp), ojnmj__jwp)
    if is_udf and isinstance(nvx__xvojc, (SeriesType, HeterogeneousSeriesType)
        ):
        jvc__vooz = numba.core.registry.cpu_target.typing_context
        uov__rbwj = numba.core.registry.cpu_target.target_context
        tuub__nfsy = bodo.transforms.series_pass.SeriesPass(f_ir, jvc__vooz,
            uov__rbwj, typemap, rhg__fyrwf, {})
        tuub__nfsy.run()
        tuub__nfsy.run()
        tuub__nfsy.run()
        viwze__kvvt = compute_cfg_from_blocks(f_ir.blocks)
        amb__cbbn = [guard(_get_const_series_info, f_ir.blocks[hxah__wgv],
            f_ir, typemap) for hxah__wgv in viwze__kvvt.exit_points() if
            isinstance(f_ir.blocks[hxah__wgv].body[-1], ir.Return)]
        if None in amb__cbbn or len(pd.Series(amb__cbbn).unique()) != 1:
            nvx__xvojc.const_info = None
        else:
            nvx__xvojc.const_info = amb__cbbn[0]
    return nvx__xvojc


def _get_const_series_info(block, f_ir, typemap):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType
    assert isinstance(block.body[-1], ir.Return)
    yyvew__jxagt = block.body[-1].value
    humrf__dzzan = get_definition(f_ir, yyvew__jxagt)
    require(is_expr(humrf__dzzan, 'cast'))
    humrf__dzzan = get_definition(f_ir, humrf__dzzan.value)
    require(is_call(humrf__dzzan) and find_callname(f_ir, humrf__dzzan) ==
        ('init_series', 'bodo.hiframes.pd_series_ext'))
    nqgqu__jcb = humrf__dzzan.args[1]
    sfis__ijqhb = tuple(get_const_value_inner(f_ir, nqgqu__jcb, typemap=
        typemap))
    if isinstance(typemap[yyvew__jxagt.name], HeterogeneousSeriesType):
        return len(typemap[yyvew__jxagt.name].data), sfis__ijqhb
    vtyel__tmljg = humrf__dzzan.args[0]
    mtsg__ruh = get_definition(f_ir, vtyel__tmljg)
    func_name, jxdu__jym = find_callname(f_ir, mtsg__ruh)
    if is_call(mtsg__ruh) and bodo.utils.utils.is_alloc_callname(func_name,
        jxdu__jym):
        iof__rphf = mtsg__ruh.args[0]
        rip__eacn = get_const_value_inner(f_ir, iof__rphf, typemap=typemap)
        return rip__eacn, sfis__ijqhb
    if is_call(mtsg__ruh) and find_callname(f_ir, mtsg__ruh) in [('asarray',
        'numpy'), ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'), (
        'build_nullable_tuple', 'bodo.libs.nullable_tuple_ext')]:
        vtyel__tmljg = mtsg__ruh.args[0]
        mtsg__ruh = get_definition(f_ir, vtyel__tmljg)
    require(is_expr(mtsg__ruh, 'build_tuple') or is_expr(mtsg__ruh,
        'build_list'))
    return len(mtsg__ruh.items), sfis__ijqhb


def extract_keyvals_from_struct_map(f_ir, build_map, loc, scope, typemap=None):
    jevc__nrnn = []
    yodk__sgys = []
    values = []
    for igb__wiemo, jwq__dlnr in build_map.items:
        inmso__tohg = find_const(f_ir, igb__wiemo)
        require(isinstance(inmso__tohg, str))
        yodk__sgys.append(inmso__tohg)
        jevc__nrnn.append(igb__wiemo)
        values.append(jwq__dlnr)
    ghqli__cmiqp = ir.Var(scope, mk_unique_var('val_tup'), loc)
    mpagh__qfo = ir.Assign(ir.Expr.build_tuple(values, loc), ghqli__cmiqp, loc)
    f_ir._definitions[ghqli__cmiqp.name] = [mpagh__qfo.value]
    kovd__fhrci = ir.Var(scope, mk_unique_var('key_tup'), loc)
    way__kqdw = ir.Assign(ir.Expr.build_tuple(jevc__nrnn, loc), kovd__fhrci,
        loc)
    f_ir._definitions[kovd__fhrci.name] = [way__kqdw.value]
    if typemap is not None:
        typemap[ghqli__cmiqp.name] = types.Tuple([typemap[jwq__dlnr.name] for
            jwq__dlnr in values])
        typemap[kovd__fhrci.name] = types.Tuple([typemap[jwq__dlnr.name] for
            jwq__dlnr in jevc__nrnn])
    return yodk__sgys, ghqli__cmiqp, mpagh__qfo, kovd__fhrci, way__kqdw


def _replace_const_map_return(f_ir, block, label):
    require(isinstance(block.body[-1], ir.Return))
    ukpm__fbl = block.body[-1].value
    giwpx__defhu = guard(get_definition, f_ir, ukpm__fbl)
    require(is_expr(giwpx__defhu, 'cast'))
    humrf__dzzan = guard(get_definition, f_ir, giwpx__defhu.value)
    require(is_expr(humrf__dzzan, 'build_map'))
    require(len(humrf__dzzan.items) > 0)
    loc = block.loc
    scope = block.scope
    yodk__sgys, ghqli__cmiqp, mpagh__qfo, kovd__fhrci, way__kqdw = (
        extract_keyvals_from_struct_map(f_ir, humrf__dzzan, loc, scope))
    forl__eifs = ir.Var(scope, mk_unique_var('conv_call'), loc)
    qwq__tqhb = ir.Assign(ir.Global('struct_if_heter_dict', bodo.utils.
        conversion.struct_if_heter_dict, loc), forl__eifs, loc)
    f_ir._definitions[forl__eifs.name] = [qwq__tqhb.value]
    yrp__qkbr = ir.Var(scope, mk_unique_var('struct_val'), loc)
    egp__ifudu = ir.Assign(ir.Expr.call(forl__eifs, [ghqli__cmiqp,
        kovd__fhrci], {}, loc), yrp__qkbr, loc)
    f_ir._definitions[yrp__qkbr.name] = [egp__ifudu.value]
    giwpx__defhu.value = yrp__qkbr
    humrf__dzzan.items = [(igb__wiemo, igb__wiemo) for igb__wiemo,
        unutk__igaqa in humrf__dzzan.items]
    block.body = block.body[:-2] + [mpagh__qfo, way__kqdw, qwq__tqhb,
        egp__ifudu] + block.body[-2:]
    return tuple(yodk__sgys)


def get_struct_keynames(f_ir, typemap):
    viwze__kvvt = compute_cfg_from_blocks(f_ir.blocks)
    jtiu__pqy = list(viwze__kvvt.exit_points())[0]
    block = f_ir.blocks[jtiu__pqy]
    require(isinstance(block.body[-1], ir.Return))
    ukpm__fbl = block.body[-1].value
    giwpx__defhu = guard(get_definition, f_ir, ukpm__fbl)
    require(is_expr(giwpx__defhu, 'cast'))
    humrf__dzzan = guard(get_definition, f_ir, giwpx__defhu.value)
    require(is_call(humrf__dzzan) and find_callname(f_ir, humrf__dzzan) ==
        ('struct_if_heter_dict', 'bodo.utils.conversion'))
    return get_overload_const_list(typemap[humrf__dzzan.args[1].name])


def fix_struct_return(f_ir):
    yaeg__afcqg = None
    viwze__kvvt = compute_cfg_from_blocks(f_ir.blocks)
    for jtiu__pqy in viwze__kvvt.exit_points():
        yaeg__afcqg = guard(_replace_const_map_return, f_ir, f_ir.blocks[
            jtiu__pqy], jtiu__pqy)
    return yaeg__afcqg


def update_node_list_definitions(node_list, func_ir):
    loc = ir.Loc('', 0)
    ytpy__mgyow = ir.Block(ir.Scope(None, loc), loc)
    ytpy__mgyow.body = node_list
    build_definitions({(0): ytpy__mgyow}, func_ir._definitions)
    return


NESTED_TUP_SENTINEL = '$BODO_NESTED_TUP'


def gen_const_val_str(c):
    if isinstance(c, tuple):
        return "'{}{}', ".format(NESTED_TUP_SENTINEL, len(c)) + ', '.join(
            gen_const_val_str(jwq__dlnr) for jwq__dlnr in c)
    if isinstance(c, str):
        return "'{}'".format(c)
    if isinstance(c, (pd.Timestamp, pd.Timedelta, float)):
        return "'{}'".format(c)
    return str(c)


def gen_const_tup(vals):
    nlkl__hqnn = ', '.join(gen_const_val_str(c) for c in vals)
    return '({}{})'.format(nlkl__hqnn, ',' if len(vals) == 1 else '')


def get_const_tup_vals(c_typ):
    vals = get_overload_const_list(c_typ)
    return _get_original_nested_tups(vals)


def _get_original_nested_tups(vals):
    for eib__xedto in range(len(vals) - 1, -1, -1):
        jwq__dlnr = vals[eib__xedto]
        if isinstance(jwq__dlnr, str) and jwq__dlnr.startswith(
            NESTED_TUP_SENTINEL):
            fkwx__bhf = int(jwq__dlnr[len(NESTED_TUP_SENTINEL):])
            return _get_original_nested_tups(tuple(vals[:eib__xedto]) + (
                tuple(vals[eib__xedto + 1:eib__xedto + fkwx__bhf + 1]),) +
                tuple(vals[eib__xedto + fkwx__bhf + 1:]))
    return tuple(vals)


def get_call_expr_arg(f_name, args, kws, arg_no, arg_name, default=None,
    err_msg=None, use_default=False):
    jfxeb__yqgjz = None
    if len(args) > arg_no and arg_no >= 0:
        jfxeb__yqgjz = args[arg_no]
        if arg_name in kws:
            err_msg = (
                f"{f_name}() got multiple values for argument '{arg_name}'")
            raise BodoError(err_msg)
    elif arg_name in kws:
        jfxeb__yqgjz = kws[arg_name]
    if jfxeb__yqgjz is None:
        if use_default or default is not None:
            return default
        if err_msg is None:
            err_msg = "{} requires '{}' argument".format(f_name, arg_name)
        raise BodoError(err_msg)
    return jfxeb__yqgjz


def set_call_expr_arg(var, args, kws, arg_no, arg_name, add_if_missing=False):
    if len(args) > arg_no:
        args[arg_no] = var
    elif add_if_missing or arg_name in kws:
        kws[arg_name] = var
    else:
        raise BodoError('cannot set call argument since does not exist')


def avoid_udf_inline(py_func, arg_types, kw_types):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    f_ir = numba.core.compiler.run_frontend(py_func, inline_closures=True)
    if '_bodo_inline' in kw_types and is_overload_constant_bool(kw_types[
        '_bodo_inline']):
        return not get_overload_const_bool(kw_types['_bodo_inline'])
    if any(isinstance(t, DataFrameType) for t in arg_types + tuple(kw_types
        .values())):
        return True
    for block in f_ir.blocks.values():
        if isinstance(block.body[-1], (ir.Raise, ir.StaticRaise)):
            return True
        for stmt in block.body:
            if isinstance(stmt, ir.EnterWith):
                return True
    return False


def replace_func(pass_info, func, args, const=False, pre_nodes=None,
    extra_globals=None, pysig=None, kws=None, inline_bodo_calls=False,
    run_full_pipeline=False):
    xars__hhmn = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd}
    if extra_globals is not None:
        xars__hhmn.update(extra_globals)
    func.__globals__.update(xars__hhmn)
    if pysig is not None:
        pre_nodes = [] if pre_nodes is None else pre_nodes
        scope = next(iter(pass_info.func_ir.blocks.values())).scope
        loc = scope.loc

        def normal_handler(index, param, default):
            return default

        def default_handler(index, param, default):
            pxxd__vbwuf = ir.Var(scope, mk_unique_var('defaults'), loc)
            try:
                pass_info.typemap[pxxd__vbwuf.name] = types.literal(default)
            except:
                pass_info.typemap[pxxd__vbwuf.name] = numba.typeof(default)
            hoow__psilp = ir.Assign(ir.Const(default, loc), pxxd__vbwuf, loc)
            pre_nodes.append(hoow__psilp)
            return pxxd__vbwuf
        args = numba.core.typing.fold_arguments(pysig, args, kws,
            normal_handler, default_handler, normal_handler)
    mmbo__dnq = tuple(pass_info.typemap[jwq__dlnr.name] for jwq__dlnr in args)
    if const:
        lld__efmm = []
        for eib__xedto, jfxeb__yqgjz in enumerate(args):
            iir__spafa = guard(find_const, pass_info.func_ir, jfxeb__yqgjz)
            if iir__spafa:
                lld__efmm.append(types.literal(iir__spafa))
            else:
                lld__efmm.append(mmbo__dnq[eib__xedto])
        mmbo__dnq = tuple(lld__efmm)
    return ReplaceFunc(func, mmbo__dnq, args, xars__hhmn, inline_bodo_calls,
        run_full_pipeline, pre_nodes)


def is_var_size_item_array_type(t):
    assert is_array_typ(t, False)
    return t == string_array_type or isinstance(t, ArrayItemArrayType
        ) or isinstance(t, StructArrayType) and any(
        is_var_size_item_array_type(ubbs__kbrtm) for ubbs__kbrtm in t.data)


def gen_init_varsize_alloc_sizes(t):
    if t == string_array_type:
        ofk__ick = 'num_chars_{}'.format(ir_utils.next_label())
        return f'  {ofk__ick} = 0\n', (ofk__ick,)
    if isinstance(t, ArrayItemArrayType):
        ptp__hhaap, ycn__ihhpd = gen_init_varsize_alloc_sizes(t.dtype)
        ofk__ick = 'num_items_{}'.format(ir_utils.next_label())
        return f'  {ofk__ick} = 0\n' + ptp__hhaap, (ofk__ick,) + ycn__ihhpd
    return '', ()


def gen_varsize_item_sizes(t, item, var_names):
    if t == string_array_type:
        return '    {} += bodo.libs.str_arr_ext.get_utf8_size({})\n'.format(
            var_names[0], item)
    if isinstance(t, ArrayItemArrayType):
        return '    {} += len({})\n'.format(var_names[0], item
            ) + gen_varsize_array_counts(t.dtype, item, var_names[1:])
    return ''


def gen_varsize_array_counts(t, item, var_names):
    if t == string_array_type:
        return ('    {} += bodo.libs.str_arr_ext.get_num_total_chars({})\n'
            .format(var_names[0], item))
    return ''


def get_type_alloc_counts(t):
    if isinstance(t, (StructArrayType, TupleArrayType)):
        return 1 + sum(get_type_alloc_counts(ubbs__kbrtm.dtype) for
            ubbs__kbrtm in t.data)
    if isinstance(t, ArrayItemArrayType) or t == string_array_type:
        return 1 + get_type_alloc_counts(t.dtype)
    if isinstance(t, MapArrayType):
        return get_type_alloc_counts(t.key_arr_type) + get_type_alloc_counts(t
            .value_arr_type)
    if bodo.utils.utils.is_array_typ(t, False) or t == bodo.string_type:
        return 1
    if isinstance(t, StructType):
        return sum(get_type_alloc_counts(ubbs__kbrtm) for ubbs__kbrtm in t.data
            )
    if isinstance(t, types.BaseTuple):
        return sum(get_type_alloc_counts(ubbs__kbrtm) for ubbs__kbrtm in t.
            types)
    return 0


def find_udf_str_name(obj_dtype, func_name, typing_context, caller_name):
    ftp__yna = typing_context.resolve_getattr(obj_dtype, func_name)
    if ftp__yna is None:
        irdl__ayemg = types.misc.Module(np)
        try:
            ftp__yna = typing_context.resolve_getattr(irdl__ayemg, func_name)
        except AttributeError as xsrd__zqgyb:
            ftp__yna = None
        if ftp__yna is None:
            raise BodoError(
                f"{caller_name}(): No Pandas method or Numpy function found with the name '{func_name}'."
                )
    return ftp__yna


def get_udf_str_return_type(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    ftp__yna = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(ftp__yna, types.BoundFunction):
        if axis is not None:
            hgsnw__blw = ftp__yna.get_call_type(typing_context, (), {'axis':
                axis})
        else:
            hgsnw__blw = ftp__yna.get_call_type(typing_context, (), {})
        return hgsnw__blw.return_type
    else:
        if bodo.utils.typing.is_numpy_ufunc(ftp__yna):
            hgsnw__blw = ftp__yna.get_call_type(typing_context, (obj_dtype,
                ), {})
            return hgsnw__blw.return_type
        raise BodoError(
            f"{caller_name}(): Only Pandas methods and np.ufunc are supported as string literals. '{func_name}' not supported."
            )


def get_pandas_method_str_impl(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    ftp__yna = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(ftp__yna, types.BoundFunction):
        bms__xboq = ftp__yna.template
        if axis is not None:
            return bms__xboq._overload_func(obj_dtype, axis=axis)
        else:
            return bms__xboq._overload_func(obj_dtype)
    return None


def dict_to_const_keys_var_values_lists(dict_var, func_ir, arg_types,
    typemap, updated_containers, require_const_map, label):
    require(isinstance(dict_var, ir.Var))
    leea__pmd = get_definition(func_ir, dict_var)
    require(isinstance(leea__pmd, ir.Expr))
    require(leea__pmd.op == 'build_map')
    fzjga__fsjb = leea__pmd.items
    jevc__nrnn = []
    values = []
    ysle__xendu = False
    for eib__xedto in range(len(fzjga__fsjb)):
        vfl__kri, value = fzjga__fsjb[eib__xedto]
        try:
            bkmfn__jbrlp = get_const_value_inner(func_ir, vfl__kri,
                arg_types, typemap, updated_containers)
            jevc__nrnn.append(bkmfn__jbrlp)
            values.append(value)
        except GuardException as xsrd__zqgyb:
            require_const_map[vfl__kri] = label
            ysle__xendu = True
    if ysle__xendu:
        raise GuardException
    return jevc__nrnn, values


def _get_const_keys_from_dict(args, func_ir, build_map, err_msg, loc):
    try:
        jevc__nrnn = tuple(get_const_value_inner(func_ir, t[0], args) for t in
            build_map.items)
    except GuardException as xsrd__zqgyb:
        raise BodoError(err_msg, loc)
    if not all(isinstance(c, (str, int)) for c in jevc__nrnn):
        raise BodoError(err_msg, loc)
    return jevc__nrnn


def _convert_const_key_dict(args, func_ir, build_map, err_msg, scope, loc,
    output_sentinel_tuple=False):
    jevc__nrnn = _get_const_keys_from_dict(args, func_ir, build_map,
        err_msg, loc)
    dpv__mrbe = []
    vesjh__dvbm = [bodo.transforms.typing_pass._create_const_var(igb__wiemo,
        'dict_key', scope, loc, dpv__mrbe) for igb__wiemo in jevc__nrnn]
    xywc__dyry = [t[1] for t in build_map.items]
    if output_sentinel_tuple:
        nao__quh = ir.Var(scope, mk_unique_var('sentinel'), loc)
        thv__nqnd = ir.Var(scope, mk_unique_var('dict_tup'), loc)
        dpv__mrbe.append(ir.Assign(ir.Const('__bodo_tup', loc), nao__quh, loc))
        fqaz__mgd = [nao__quh] + vesjh__dvbm + xywc__dyry
        dpv__mrbe.append(ir.Assign(ir.Expr.build_tuple(fqaz__mgd, loc),
            thv__nqnd, loc))
        return (thv__nqnd,), dpv__mrbe
    else:
        rqkzg__snx = ir.Var(scope, mk_unique_var('values_tup'), loc)
        drybb__qej = ir.Var(scope, mk_unique_var('idx_tup'), loc)
        dpv__mrbe.append(ir.Assign(ir.Expr.build_tuple(xywc__dyry, loc),
            rqkzg__snx, loc))
        dpv__mrbe.append(ir.Assign(ir.Expr.build_tuple(vesjh__dvbm, loc),
            drybb__qej, loc))
        return (rqkzg__snx, drybb__qej), dpv__mrbe
