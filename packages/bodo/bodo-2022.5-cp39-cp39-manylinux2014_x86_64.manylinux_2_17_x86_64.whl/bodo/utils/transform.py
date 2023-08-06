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
    bodo), ('prange', bodo), (bodo.prange,), ('objmode', bodo), (bodo.
    objmode,), ('get_label_dict_from_categories', 'pd_categorial_ext',
    'hiframes', bodo), ('get_label_dict_from_categories_no_duplicates',
    'pd_categorial_ext', 'hiframes', bodo), ('build_nullable_tuple',
    'nullable_tuple_ext', 'libs', bodo), ('generate_mappable_table_func',
    'table_utils', 'utils', bodo)}


def remove_hiframes(rhs, lives, call_list):
    jdx__zzdh = tuple(call_list)
    if jdx__zzdh in no_side_effect_call_tuples:
        return True
    if jdx__zzdh == (bodo.hiframes.pd_index_ext.init_range_index,):
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
    if len(jdx__zzdh) == 1 and tuple in getattr(jdx__zzdh[0], '__mro__', ()):
        return True
    return False


numba.core.ir_utils.remove_call_handlers.append(remove_hiframes)


def compile_func_single_block(func, args, ret_var, typing_info=None,
    extra_globals=None, infer_types=True, run_untyped_pass=False, flags=
    None, replace_globals=True):
    okbx__oyy = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd, 'math': math
        }
    if extra_globals is not None:
        okbx__oyy.update(extra_globals)
    if not replace_globals:
        okbx__oyy = func.__globals__
    loc = ir.Loc('', 0)
    if ret_var:
        loc = ret_var.loc
    if typing_info and infer_types:
        loc = typing_info.curr_loc
        f_ir = compile_to_numba_ir(func, okbx__oyy, typingctx=typing_info.
            typingctx, targetctx=typing_info.targetctx, arg_typs=tuple(
            typing_info.typemap[egnsv__uopy.name] for egnsv__uopy in args),
            typemap=typing_info.typemap, calltypes=typing_info.calltypes)
    else:
        f_ir = compile_to_numba_ir(func, okbx__oyy)
    assert len(f_ir.blocks
        ) == 1, 'only single block functions supported in compile_func_single_block()'
    if run_untyped_pass:
        ejnbb__sqlx = tuple(typing_info.typemap[egnsv__uopy.name] for
            egnsv__uopy in args)
        ivx__kiudd = bodo.transforms.untyped_pass.UntypedPass(f_ir,
            typing_info.typingctx, ejnbb__sqlx, {}, {}, flags)
        ivx__kiudd.run()
    sfbud__zgot = f_ir.blocks.popitem()[1]
    replace_arg_nodes(sfbud__zgot, args)
    zhuw__ruq = sfbud__zgot.body[:-2]
    update_locs(zhuw__ruq[len(args):], loc)
    for stmt in zhuw__ruq[:len(args)]:
        stmt.target.loc = loc
    if ret_var is not None:
        gjkb__imxc = sfbud__zgot.body[-2]
        assert is_assign(gjkb__imxc) and is_expr(gjkb__imxc.value, 'cast')
        vkar__alp = gjkb__imxc.value.value
        zhuw__ruq.append(ir.Assign(vkar__alp, ret_var, loc))
    return zhuw__ruq


def update_locs(node_list, loc):
    for stmt in node_list:
        stmt.loc = loc
        for ywrfj__tmpp in stmt.list_vars():
            ywrfj__tmpp.loc = loc
        if is_assign(stmt):
            stmt.value.loc = loc


def get_stmt_defs(stmt):
    if is_assign(stmt):
        return set([stmt.target.name])
    if type(stmt) in numba.core.analysis.ir_extension_usedefs:
        ltzb__vnqr = numba.core.analysis.ir_extension_usedefs[type(stmt)]
        pzyuw__rgqco, tvi__rfjdr = ltzb__vnqr(stmt)
        return tvi__rfjdr
    return set()


def get_const_value(var, func_ir, err_msg, typemap=None, arg_types=None,
    file_info=None):
    if hasattr(var, 'loc'):
        loc = var.loc
    else:
        loc = None
    try:
        yybiw__hak = get_const_value_inner(func_ir, var, arg_types, typemap,
            file_info=file_info)
        if isinstance(yybiw__hak, ir.UndefinedType):
            hayf__owizk = func_ir.get_definition(var.name).name
            raise BodoError(f"name '{hayf__owizk}' is not defined", loc=loc)
    except GuardException as dlywq__ntqe:
        raise BodoError(err_msg, loc=loc)
    return yybiw__hak


def get_const_value_inner(func_ir, var, arg_types=None, typemap=None,
    updated_containers=None, file_info=None, pyobject_to_literal=False,
    literalize_args=True):
    require(isinstance(var, ir.Var))
    jmvsu__onp = get_definition(func_ir, var)
    qknax__cyho = None
    if typemap is not None:
        qknax__cyho = typemap.get(var.name, None)
    if isinstance(jmvsu__onp, ir.Arg) and arg_types is not None:
        qknax__cyho = arg_types[jmvsu__onp.index]
    if updated_containers and var.name in updated_containers:
        raise BodoConstUpdatedError(
            f"variable '{var.name}' is updated inplace using '{updated_containers[var.name]}'"
            )
    if is_literal_type(qknax__cyho):
        return get_literal_value(qknax__cyho)
    if isinstance(jmvsu__onp, (ir.Const, ir.Global, ir.FreeVar)):
        yybiw__hak = jmvsu__onp.value
        return yybiw__hak
    if literalize_args and isinstance(jmvsu__onp, ir.Arg
        ) and can_literalize_type(qknax__cyho, pyobject_to_literal):
        raise numba.core.errors.ForceLiteralArg({jmvsu__onp.index}, loc=var
            .loc, file_infos={jmvsu__onp.index: file_info} if file_info is not
            None else None)
    if is_expr(jmvsu__onp, 'binop'):
        if file_info and jmvsu__onp.fn == operator.add:
            try:
                ddao__dsc = get_const_value_inner(func_ir, jmvsu__onp.lhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(ddao__dsc, True)
                pdp__wbs = get_const_value_inner(func_ir, jmvsu__onp.rhs,
                    arg_types, typemap, updated_containers, file_info)
                return jmvsu__onp.fn(ddao__dsc, pdp__wbs)
            except (GuardException, BodoConstUpdatedError) as dlywq__ntqe:
                pass
            try:
                pdp__wbs = get_const_value_inner(func_ir, jmvsu__onp.rhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(pdp__wbs, False)
                ddao__dsc = get_const_value_inner(func_ir, jmvsu__onp.lhs,
                    arg_types, typemap, updated_containers, file_info)
                return jmvsu__onp.fn(ddao__dsc, pdp__wbs)
            except (GuardException, BodoConstUpdatedError) as dlywq__ntqe:
                pass
        ddao__dsc = get_const_value_inner(func_ir, jmvsu__onp.lhs,
            arg_types, typemap, updated_containers)
        pdp__wbs = get_const_value_inner(func_ir, jmvsu__onp.rhs, arg_types,
            typemap, updated_containers)
        return jmvsu__onp.fn(ddao__dsc, pdp__wbs)
    if is_expr(jmvsu__onp, 'unary'):
        yybiw__hak = get_const_value_inner(func_ir, jmvsu__onp.value,
            arg_types, typemap, updated_containers)
        return jmvsu__onp.fn(yybiw__hak)
    if is_expr(jmvsu__onp, 'getattr') and typemap:
        bqc__quwqh = typemap.get(jmvsu__onp.value.name, None)
        if isinstance(bqc__quwqh, bodo.hiframes.pd_dataframe_ext.DataFrameType
            ) and jmvsu__onp.attr == 'columns':
            return pd.Index(bqc__quwqh.columns)
        if isinstance(bqc__quwqh, types.SliceType):
            kdwbs__esot = get_definition(func_ir, jmvsu__onp.value)
            require(is_call(kdwbs__esot))
            wrxbp__jisej = find_callname(func_ir, kdwbs__esot)
            fcgg__epb = False
            if wrxbp__jisej == ('_normalize_slice', 'numba.cpython.unicode'):
                require(jmvsu__onp.attr in ('start', 'step'))
                kdwbs__esot = get_definition(func_ir, kdwbs__esot.args[0])
                fcgg__epb = True
            require(find_callname(func_ir, kdwbs__esot) == ('slice',
                'builtins'))
            if len(kdwbs__esot.args) == 1:
                if jmvsu__onp.attr == 'start':
                    return 0
                if jmvsu__onp.attr == 'step':
                    return 1
                require(jmvsu__onp.attr == 'stop')
                return get_const_value_inner(func_ir, kdwbs__esot.args[0],
                    arg_types, typemap, updated_containers)
            if jmvsu__onp.attr == 'start':
                yybiw__hak = get_const_value_inner(func_ir, kdwbs__esot.
                    args[0], arg_types, typemap, updated_containers)
                if yybiw__hak is None:
                    yybiw__hak = 0
                if fcgg__epb:
                    require(yybiw__hak == 0)
                return yybiw__hak
            if jmvsu__onp.attr == 'stop':
                assert not fcgg__epb
                return get_const_value_inner(func_ir, kdwbs__esot.args[1],
                    arg_types, typemap, updated_containers)
            require(jmvsu__onp.attr == 'step')
            if len(kdwbs__esot.args) == 2:
                return 1
            else:
                yybiw__hak = get_const_value_inner(func_ir, kdwbs__esot.
                    args[2], arg_types, typemap, updated_containers)
                if yybiw__hak is None:
                    yybiw__hak = 1
                if fcgg__epb:
                    require(yybiw__hak == 1)
                return yybiw__hak
    if is_expr(jmvsu__onp, 'getattr'):
        return getattr(get_const_value_inner(func_ir, jmvsu__onp.value,
            arg_types, typemap, updated_containers), jmvsu__onp.attr)
    if is_expr(jmvsu__onp, 'getitem'):
        value = get_const_value_inner(func_ir, jmvsu__onp.value, arg_types,
            typemap, updated_containers)
        index = get_const_value_inner(func_ir, jmvsu__onp.index, arg_types,
            typemap, updated_containers)
        return value[index]
    fded__mbtd = guard(find_callname, func_ir, jmvsu__onp, typemap)
    if fded__mbtd is not None and len(fded__mbtd) == 2 and fded__mbtd[0
        ] == 'keys' and isinstance(fded__mbtd[1], ir.Var):
        cywv__tvcwt = jmvsu__onp.func
        jmvsu__onp = get_definition(func_ir, fded__mbtd[1])
        fsmm__dmoma = fded__mbtd[1].name
        if updated_containers and fsmm__dmoma in updated_containers:
            raise BodoConstUpdatedError(
                "variable '{}' is updated inplace using '{}'".format(
                fsmm__dmoma, updated_containers[fsmm__dmoma]))
        require(is_expr(jmvsu__onp, 'build_map'))
        vals = [ywrfj__tmpp[0] for ywrfj__tmpp in jmvsu__onp.items]
        rlg__vzlv = guard(get_definition, func_ir, cywv__tvcwt)
        assert isinstance(rlg__vzlv, ir.Expr) and rlg__vzlv.attr == 'keys'
        rlg__vzlv.attr = 'copy'
        return [get_const_value_inner(func_ir, ywrfj__tmpp, arg_types,
            typemap, updated_containers) for ywrfj__tmpp in vals]
    if is_expr(jmvsu__onp, 'build_map'):
        return {get_const_value_inner(func_ir, ywrfj__tmpp[0], arg_types,
            typemap, updated_containers): get_const_value_inner(func_ir,
            ywrfj__tmpp[1], arg_types, typemap, updated_containers) for
            ywrfj__tmpp in jmvsu__onp.items}
    if is_expr(jmvsu__onp, 'build_tuple'):
        return tuple(get_const_value_inner(func_ir, ywrfj__tmpp, arg_types,
            typemap, updated_containers) for ywrfj__tmpp in jmvsu__onp.items)
    if is_expr(jmvsu__onp, 'build_list'):
        return [get_const_value_inner(func_ir, ywrfj__tmpp, arg_types,
            typemap, updated_containers) for ywrfj__tmpp in jmvsu__onp.items]
    if is_expr(jmvsu__onp, 'build_set'):
        return {get_const_value_inner(func_ir, ywrfj__tmpp, arg_types,
            typemap, updated_containers) for ywrfj__tmpp in jmvsu__onp.items}
    if fded__mbtd == ('list', 'builtins'):
        values = get_const_value_inner(func_ir, jmvsu__onp.args[0],
            arg_types, typemap, updated_containers)
        if isinstance(values, set):
            values = sorted(values)
        return list(values)
    if fded__mbtd == ('set', 'builtins'):
        return set(get_const_value_inner(func_ir, jmvsu__onp.args[0],
            arg_types, typemap, updated_containers))
    if fded__mbtd == ('range', 'builtins') and len(jmvsu__onp.args) == 1:
        return range(get_const_value_inner(func_ir, jmvsu__onp.args[0],
            arg_types, typemap, updated_containers))
    if fded__mbtd == ('slice', 'builtins'):
        return slice(*tuple(get_const_value_inner(func_ir, ywrfj__tmpp,
            arg_types, typemap, updated_containers) for ywrfj__tmpp in
            jmvsu__onp.args))
    if fded__mbtd == ('str', 'builtins'):
        return str(get_const_value_inner(func_ir, jmvsu__onp.args[0],
            arg_types, typemap, updated_containers))
    if fded__mbtd == ('bool', 'builtins'):
        return bool(get_const_value_inner(func_ir, jmvsu__onp.args[0],
            arg_types, typemap, updated_containers))
    if fded__mbtd == ('format', 'builtins'):
        egnsv__uopy = get_const_value_inner(func_ir, jmvsu__onp.args[0],
            arg_types, typemap, updated_containers)
        azipe__woxo = get_const_value_inner(func_ir, jmvsu__onp.args[1],
            arg_types, typemap, updated_containers) if len(jmvsu__onp.args
            ) > 1 else ''
        return format(egnsv__uopy, azipe__woxo)
    if fded__mbtd in (('init_binary_str_index',
        'bodo.hiframes.pd_index_ext'), ('init_numeric_index',
        'bodo.hiframes.pd_index_ext'), ('init_categorical_index',
        'bodo.hiframes.pd_index_ext'), ('init_datetime_index',
        'bodo.hiframes.pd_index_ext'), ('init_timedelta_index',
        'bodo.hiframes.pd_index_ext'), ('init_heter_index',
        'bodo.hiframes.pd_index_ext')):
        return pd.Index(get_const_value_inner(func_ir, jmvsu__onp.args[0],
            arg_types, typemap, updated_containers))
    if fded__mbtd == ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'):
        return np.array(get_const_value_inner(func_ir, jmvsu__onp.args[0],
            arg_types, typemap, updated_containers))
    if fded__mbtd == ('init_range_index', 'bodo.hiframes.pd_index_ext'):
        return pd.RangeIndex(get_const_value_inner(func_ir, jmvsu__onp.args
            [0], arg_types, typemap, updated_containers),
            get_const_value_inner(func_ir, jmvsu__onp.args[1], arg_types,
            typemap, updated_containers), get_const_value_inner(func_ir,
            jmvsu__onp.args[2], arg_types, typemap, updated_containers))
    if fded__mbtd == ('len', 'builtins') and typemap and isinstance(typemap
        .get(jmvsu__onp.args[0].name, None), types.BaseTuple):
        return len(typemap[jmvsu__onp.args[0].name])
    if fded__mbtd == ('len', 'builtins'):
        vku__maen = guard(get_definition, func_ir, jmvsu__onp.args[0])
        if isinstance(vku__maen, ir.Expr) and vku__maen.op in ('build_tuple',
            'build_list', 'build_set', 'build_map'):
            return len(vku__maen.items)
        return len(get_const_value_inner(func_ir, jmvsu__onp.args[0],
            arg_types, typemap, updated_containers))
    if fded__mbtd == ('CategoricalDtype', 'pandas'):
        kws = dict(jmvsu__onp.kws)
        vgbe__ylj = get_call_expr_arg('CategoricalDtype', jmvsu__onp.args,
            kws, 0, 'categories', '')
        jqqcj__bmr = get_call_expr_arg('CategoricalDtype', jmvsu__onp.args,
            kws, 1, 'ordered', False)
        if jqqcj__bmr is not False:
            jqqcj__bmr = get_const_value_inner(func_ir, jqqcj__bmr,
                arg_types, typemap, updated_containers)
        if vgbe__ylj == '':
            vgbe__ylj = None
        else:
            vgbe__ylj = get_const_value_inner(func_ir, vgbe__ylj, arg_types,
                typemap, updated_containers)
        return pd.CategoricalDtype(vgbe__ylj, jqqcj__bmr)
    if fded__mbtd == ('dtype', 'numpy'):
        return np.dtype(get_const_value_inner(func_ir, jmvsu__onp.args[0],
            arg_types, typemap, updated_containers))
    if fded__mbtd is not None and len(fded__mbtd) == 2 and fded__mbtd[1
        ] == 'pandas' and fded__mbtd[0] in ('Int8Dtype', 'Int16Dtype',
        'Int32Dtype', 'Int64Dtype', 'UInt8Dtype', 'UInt16Dtype',
        'UInt32Dtype', 'UInt64Dtype'):
        return getattr(pd, fded__mbtd[0])()
    if fded__mbtd is not None and len(fded__mbtd) == 2 and isinstance(
        fded__mbtd[1], ir.Var):
        yybiw__hak = get_const_value_inner(func_ir, fded__mbtd[1],
            arg_types, typemap, updated_containers)
        args = [get_const_value_inner(func_ir, ywrfj__tmpp, arg_types,
            typemap, updated_containers) for ywrfj__tmpp in jmvsu__onp.args]
        kws = {lug__uksqd[0]: get_const_value_inner(func_ir, lug__uksqd[1],
            arg_types, typemap, updated_containers) for lug__uksqd in
            jmvsu__onp.kws}
        return getattr(yybiw__hak, fded__mbtd[0])(*args, **kws)
    if fded__mbtd is not None and len(fded__mbtd) == 2 and fded__mbtd[1
        ] == 'bodo' and fded__mbtd[0] in bodo_types_with_params:
        args = tuple(get_const_value_inner(func_ir, ywrfj__tmpp, arg_types,
            typemap, updated_containers) for ywrfj__tmpp in jmvsu__onp.args)
        kwargs = {hayf__owizk: get_const_value_inner(func_ir, ywrfj__tmpp,
            arg_types, typemap, updated_containers) for hayf__owizk,
            ywrfj__tmpp in dict(jmvsu__onp.kws).items()}
        return getattr(bodo, fded__mbtd[0])(*args, **kwargs)
    if is_call(jmvsu__onp) and typemap and isinstance(typemap.get(
        jmvsu__onp.func.name, None), types.Dispatcher):
        py_func = typemap[jmvsu__onp.func.name].dispatcher.py_func
        require(jmvsu__onp.vararg is None)
        args = tuple(get_const_value_inner(func_ir, ywrfj__tmpp, arg_types,
            typemap, updated_containers) for ywrfj__tmpp in jmvsu__onp.args)
        kwargs = {hayf__owizk: get_const_value_inner(func_ir, ywrfj__tmpp,
            arg_types, typemap, updated_containers) for hayf__owizk,
            ywrfj__tmpp in dict(jmvsu__onp.kws).items()}
        arg_types = tuple(bodo.typeof(ywrfj__tmpp) for ywrfj__tmpp in args)
        kw_types = {mukjg__ien: bodo.typeof(ywrfj__tmpp) for mukjg__ien,
            ywrfj__tmpp in kwargs.items()}
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
    f_ir, typemap, ghb__iezkr, ghb__iezkr = bodo.compiler.get_func_type_info(
        py_func, arg_types, kw_types)
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
                    zfrg__ggbgq = guard(get_definition, f_ir, rhs.func)
                    if isinstance(zfrg__ggbgq, ir.Const) and isinstance(
                        zfrg__ggbgq.value, numba.core.dispatcher.
                        ObjModeLiftedWith):
                        return False
                    fvgug__drhs = guard(find_callname, f_ir, rhs)
                    if fvgug__drhs is None:
                        return False
                    func_name, uci__eplw = fvgug__drhs
                    if uci__eplw == 'pandas' and func_name.startswith('read_'):
                        return False
                    if fvgug__drhs in (('fromfile', 'numpy'), ('file_read',
                        'bodo.io.np_io')):
                        return False
                    if fvgug__drhs == ('File', 'h5py'):
                        return False
                    if isinstance(uci__eplw, ir.Var):
                        qknax__cyho = typemap[uci__eplw.name]
                        if isinstance(qknax__cyho, (DataFrameType, SeriesType)
                            ) and func_name in ('to_csv', 'to_excel',
                            'to_json', 'to_sql', 'to_pickle', 'to_parquet',
                            'info'):
                            return False
                        if isinstance(qknax__cyho, types.Array
                            ) and func_name == 'tofile':
                            return False
                        if isinstance(qknax__cyho, bodo.LoggingLoggerType):
                            return False
                        if str(qknax__cyho).startswith('Mpl'):
                            return False
                        if (func_name in container_update_method_names and
                            isinstance(guard(get_definition, f_ir,
                            uci__eplw), ir.Arg)):
                            return False
                    if uci__eplw in ('numpy.random', 'time', 'logging',
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
        swf__idfa = func.literal_value.code
        gzryk__qklhe = {'np': np, 'pd': pd, 'numba': numba, 'bodo': bodo}
        if hasattr(func.literal_value, 'globals'):
            gzryk__qklhe = func.literal_value.globals
        f_ir = numba.core.ir_utils.get_ir_of_code(gzryk__qklhe, swf__idfa)
        fix_struct_return(f_ir)
        typemap, zhwp__bwldy, rimy__vjb, ghb__iezkr = (numba.core.
            typed_passes.type_inference_stage(typing_context,
            target_context, f_ir, arg_types, None))
    elif isinstance(func, bodo.utils.typing.FunctionLiteral):
        py_func = func.literal_value
        f_ir, typemap, rimy__vjb, zhwp__bwldy = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    elif isinstance(func, CPUDispatcher):
        py_func = func.py_func
        f_ir, typemap, rimy__vjb, zhwp__bwldy = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    else:
        if not isinstance(func, types.Dispatcher):
            if isinstance(func, types.Function):
                raise BodoError(
                    f'Bodo does not support built-in functions yet, {func}')
            else:
                raise BodoError(f'Function type expected, not {func}')
        py_func = func.dispatcher.py_func
        f_ir, typemap, rimy__vjb, zhwp__bwldy = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    if is_udf and isinstance(zhwp__bwldy, types.DictType):
        dykg__mlza = guard(get_struct_keynames, f_ir, typemap)
        if dykg__mlza is not None:
            zhwp__bwldy = StructType((zhwp__bwldy.value_type,) * len(
                dykg__mlza), dykg__mlza)
    if is_udf and isinstance(zhwp__bwldy, (SeriesType, HeterogeneousSeriesType)
        ):
        rpt__ueo = numba.core.registry.cpu_target.typing_context
        iylzf__lbqcz = numba.core.registry.cpu_target.target_context
        cqnf__mbx = bodo.transforms.series_pass.SeriesPass(f_ir, rpt__ueo,
            iylzf__lbqcz, typemap, rimy__vjb, {})
        cqnf__mbx.run()
        cqnf__mbx.run()
        cqnf__mbx.run()
        hoayq__kxl = compute_cfg_from_blocks(f_ir.blocks)
        oag__sdjq = [guard(_get_const_series_info, f_ir.blocks[tzi__jrp],
            f_ir, typemap) for tzi__jrp in hoayq__kxl.exit_points() if
            isinstance(f_ir.blocks[tzi__jrp].body[-1], ir.Return)]
        if None in oag__sdjq or len(pd.Series(oag__sdjq).unique()) != 1:
            zhwp__bwldy.const_info = None
        else:
            zhwp__bwldy.const_info = oag__sdjq[0]
    return zhwp__bwldy


def _get_const_series_info(block, f_ir, typemap):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType
    assert isinstance(block.body[-1], ir.Return)
    hnw__hlmzf = block.body[-1].value
    dpdo__csw = get_definition(f_ir, hnw__hlmzf)
    require(is_expr(dpdo__csw, 'cast'))
    dpdo__csw = get_definition(f_ir, dpdo__csw.value)
    require(is_call(dpdo__csw) and find_callname(f_ir, dpdo__csw) == (
        'init_series', 'bodo.hiframes.pd_series_ext'))
    xvrz__lvh = dpdo__csw.args[1]
    gyir__lasbb = tuple(get_const_value_inner(f_ir, xvrz__lvh, typemap=typemap)
        )
    if isinstance(typemap[hnw__hlmzf.name], HeterogeneousSeriesType):
        return len(typemap[hnw__hlmzf.name].data), gyir__lasbb
    vtt__eekct = dpdo__csw.args[0]
    cgcib__ngcz = get_definition(f_ir, vtt__eekct)
    func_name, ctt__heqp = find_callname(f_ir, cgcib__ngcz)
    if is_call(cgcib__ngcz) and bodo.utils.utils.is_alloc_callname(func_name,
        ctt__heqp):
        oui__ymlzt = cgcib__ngcz.args[0]
        qpgm__pde = get_const_value_inner(f_ir, oui__ymlzt, typemap=typemap)
        return qpgm__pde, gyir__lasbb
    if is_call(cgcib__ngcz) and find_callname(f_ir, cgcib__ngcz) in [(
        'asarray', 'numpy'), ('str_arr_from_sequence',
        'bodo.libs.str_arr_ext'), ('build_nullable_tuple',
        'bodo.libs.nullable_tuple_ext')]:
        vtt__eekct = cgcib__ngcz.args[0]
        cgcib__ngcz = get_definition(f_ir, vtt__eekct)
    require(is_expr(cgcib__ngcz, 'build_tuple') or is_expr(cgcib__ngcz,
        'build_list'))
    return len(cgcib__ngcz.items), gyir__lasbb


def extract_keyvals_from_struct_map(f_ir, build_map, loc, scope, typemap=None):
    uel__tcba = []
    lgsk__ayf = []
    values = []
    for mukjg__ien, ywrfj__tmpp in build_map.items:
        suzyh__kgj = find_const(f_ir, mukjg__ien)
        require(isinstance(suzyh__kgj, str))
        lgsk__ayf.append(suzyh__kgj)
        uel__tcba.append(mukjg__ien)
        values.append(ywrfj__tmpp)
    qzimd__oxgw = ir.Var(scope, mk_unique_var('val_tup'), loc)
    ssp__sfx = ir.Assign(ir.Expr.build_tuple(values, loc), qzimd__oxgw, loc)
    f_ir._definitions[qzimd__oxgw.name] = [ssp__sfx.value]
    woxx__hbkij = ir.Var(scope, mk_unique_var('key_tup'), loc)
    fektm__xmmv = ir.Assign(ir.Expr.build_tuple(uel__tcba, loc),
        woxx__hbkij, loc)
    f_ir._definitions[woxx__hbkij.name] = [fektm__xmmv.value]
    if typemap is not None:
        typemap[qzimd__oxgw.name] = types.Tuple([typemap[ywrfj__tmpp.name] for
            ywrfj__tmpp in values])
        typemap[woxx__hbkij.name] = types.Tuple([typemap[ywrfj__tmpp.name] for
            ywrfj__tmpp in uel__tcba])
    return lgsk__ayf, qzimd__oxgw, ssp__sfx, woxx__hbkij, fektm__xmmv


def _replace_const_map_return(f_ir, block, label):
    require(isinstance(block.body[-1], ir.Return))
    gexq__mfdj = block.body[-1].value
    obi__frlh = guard(get_definition, f_ir, gexq__mfdj)
    require(is_expr(obi__frlh, 'cast'))
    dpdo__csw = guard(get_definition, f_ir, obi__frlh.value)
    require(is_expr(dpdo__csw, 'build_map'))
    require(len(dpdo__csw.items) > 0)
    loc = block.loc
    scope = block.scope
    lgsk__ayf, qzimd__oxgw, ssp__sfx, woxx__hbkij, fektm__xmmv = (
        extract_keyvals_from_struct_map(f_ir, dpdo__csw, loc, scope))
    bvpzt__xqf = ir.Var(scope, mk_unique_var('conv_call'), loc)
    txht__odms = ir.Assign(ir.Global('struct_if_heter_dict', bodo.utils.
        conversion.struct_if_heter_dict, loc), bvpzt__xqf, loc)
    f_ir._definitions[bvpzt__xqf.name] = [txht__odms.value]
    rzeh__abty = ir.Var(scope, mk_unique_var('struct_val'), loc)
    kdpb__qsbn = ir.Assign(ir.Expr.call(bvpzt__xqf, [qzimd__oxgw,
        woxx__hbkij], {}, loc), rzeh__abty, loc)
    f_ir._definitions[rzeh__abty.name] = [kdpb__qsbn.value]
    obi__frlh.value = rzeh__abty
    dpdo__csw.items = [(mukjg__ien, mukjg__ien) for mukjg__ien, ghb__iezkr in
        dpdo__csw.items]
    block.body = block.body[:-2] + [ssp__sfx, fektm__xmmv, txht__odms,
        kdpb__qsbn] + block.body[-2:]
    return tuple(lgsk__ayf)


def get_struct_keynames(f_ir, typemap):
    hoayq__kxl = compute_cfg_from_blocks(f_ir.blocks)
    wxm__zhhzj = list(hoayq__kxl.exit_points())[0]
    block = f_ir.blocks[wxm__zhhzj]
    require(isinstance(block.body[-1], ir.Return))
    gexq__mfdj = block.body[-1].value
    obi__frlh = guard(get_definition, f_ir, gexq__mfdj)
    require(is_expr(obi__frlh, 'cast'))
    dpdo__csw = guard(get_definition, f_ir, obi__frlh.value)
    require(is_call(dpdo__csw) and find_callname(f_ir, dpdo__csw) == (
        'struct_if_heter_dict', 'bodo.utils.conversion'))
    return get_overload_const_list(typemap[dpdo__csw.args[1].name])


def fix_struct_return(f_ir):
    ibi__rdevu = None
    hoayq__kxl = compute_cfg_from_blocks(f_ir.blocks)
    for wxm__zhhzj in hoayq__kxl.exit_points():
        ibi__rdevu = guard(_replace_const_map_return, f_ir, f_ir.blocks[
            wxm__zhhzj], wxm__zhhzj)
    return ibi__rdevu


def update_node_list_definitions(node_list, func_ir):
    loc = ir.Loc('', 0)
    ypda__gsucu = ir.Block(ir.Scope(None, loc), loc)
    ypda__gsucu.body = node_list
    build_definitions({(0): ypda__gsucu}, func_ir._definitions)
    return


NESTED_TUP_SENTINEL = '$BODO_NESTED_TUP'


def gen_const_val_str(c):
    if isinstance(c, tuple):
        return "'{}{}', ".format(NESTED_TUP_SENTINEL, len(c)) + ', '.join(
            gen_const_val_str(ywrfj__tmpp) for ywrfj__tmpp in c)
    if isinstance(c, str):
        return "'{}'".format(c)
    if isinstance(c, (pd.Timestamp, pd.Timedelta, float)):
        return "'{}'".format(c)
    return str(c)


def gen_const_tup(vals):
    ddkr__elnur = ', '.join(gen_const_val_str(c) for c in vals)
    return '({}{})'.format(ddkr__elnur, ',' if len(vals) == 1 else '')


def get_const_tup_vals(c_typ):
    vals = get_overload_const_list(c_typ)
    return _get_original_nested_tups(vals)


def _get_original_nested_tups(vals):
    for fafyf__exq in range(len(vals) - 1, -1, -1):
        ywrfj__tmpp = vals[fafyf__exq]
        if isinstance(ywrfj__tmpp, str) and ywrfj__tmpp.startswith(
            NESTED_TUP_SENTINEL):
            mhnx__kne = int(ywrfj__tmpp[len(NESTED_TUP_SENTINEL):])
            return _get_original_nested_tups(tuple(vals[:fafyf__exq]) + (
                tuple(vals[fafyf__exq + 1:fafyf__exq + mhnx__kne + 1]),) +
                tuple(vals[fafyf__exq + mhnx__kne + 1:]))
    return tuple(vals)


def get_call_expr_arg(f_name, args, kws, arg_no, arg_name, default=None,
    err_msg=None, use_default=False):
    egnsv__uopy = None
    if len(args) > arg_no and arg_no >= 0:
        egnsv__uopy = args[arg_no]
        if arg_name in kws:
            err_msg = (
                f"{f_name}() got multiple values for argument '{arg_name}'")
            raise BodoError(err_msg)
    elif arg_name in kws:
        egnsv__uopy = kws[arg_name]
    if egnsv__uopy is None:
        if use_default or default is not None:
            return default
        if err_msg is None:
            err_msg = "{} requires '{}' argument".format(f_name, arg_name)
        raise BodoError(err_msg)
    return egnsv__uopy


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
    okbx__oyy = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd}
    if extra_globals is not None:
        okbx__oyy.update(extra_globals)
    func.__globals__.update(okbx__oyy)
    if pysig is not None:
        pre_nodes = [] if pre_nodes is None else pre_nodes
        scope = next(iter(pass_info.func_ir.blocks.values())).scope
        loc = scope.loc

        def normal_handler(index, param, default):
            return default

        def default_handler(index, param, default):
            gbqfr__cbwe = ir.Var(scope, mk_unique_var('defaults'), loc)
            try:
                pass_info.typemap[gbqfr__cbwe.name] = types.literal(default)
            except:
                pass_info.typemap[gbqfr__cbwe.name] = numba.typeof(default)
            ljwk__kzgmh = ir.Assign(ir.Const(default, loc), gbqfr__cbwe, loc)
            pre_nodes.append(ljwk__kzgmh)
            return gbqfr__cbwe
        args = numba.core.typing.fold_arguments(pysig, args, kws,
            normal_handler, default_handler, normal_handler)
    ejnbb__sqlx = tuple(pass_info.typemap[ywrfj__tmpp.name] for ywrfj__tmpp in
        args)
    if const:
        nham__wtk = []
        for fafyf__exq, egnsv__uopy in enumerate(args):
            yybiw__hak = guard(find_const, pass_info.func_ir, egnsv__uopy)
            if yybiw__hak:
                nham__wtk.append(types.literal(yybiw__hak))
            else:
                nham__wtk.append(ejnbb__sqlx[fafyf__exq])
        ejnbb__sqlx = tuple(nham__wtk)
    return ReplaceFunc(func, ejnbb__sqlx, args, okbx__oyy,
        inline_bodo_calls, run_full_pipeline, pre_nodes)


def is_var_size_item_array_type(t):
    assert is_array_typ(t, False)
    return t == string_array_type or isinstance(t, ArrayItemArrayType
        ) or isinstance(t, StructArrayType) and any(
        is_var_size_item_array_type(novkn__bfm) for novkn__bfm in t.data)


def gen_init_varsize_alloc_sizes(t):
    if t == string_array_type:
        lukx__mlzww = 'num_chars_{}'.format(ir_utils.next_label())
        return f'  {lukx__mlzww} = 0\n', (lukx__mlzww,)
    if isinstance(t, ArrayItemArrayType):
        nuu__gup, sfu__prvma = gen_init_varsize_alloc_sizes(t.dtype)
        lukx__mlzww = 'num_items_{}'.format(ir_utils.next_label())
        return f'  {lukx__mlzww} = 0\n' + nuu__gup, (lukx__mlzww,) + sfu__prvma
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
        return 1 + sum(get_type_alloc_counts(novkn__bfm.dtype) for
            novkn__bfm in t.data)
    if isinstance(t, ArrayItemArrayType) or t == string_array_type:
        return 1 + get_type_alloc_counts(t.dtype)
    if isinstance(t, MapArrayType):
        return get_type_alloc_counts(t.key_arr_type) + get_type_alloc_counts(t
            .value_arr_type)
    if bodo.utils.utils.is_array_typ(t, False) or t == bodo.string_type:
        return 1
    if isinstance(t, StructType):
        return sum(get_type_alloc_counts(novkn__bfm) for novkn__bfm in t.data)
    if isinstance(t, types.BaseTuple):
        return sum(get_type_alloc_counts(novkn__bfm) for novkn__bfm in t.types)
    return 0


def find_udf_str_name(obj_dtype, func_name, typing_context, caller_name):
    lkglx__ihuow = typing_context.resolve_getattr(obj_dtype, func_name)
    if lkglx__ihuow is None:
        jzbu__qcgy = types.misc.Module(np)
        try:
            lkglx__ihuow = typing_context.resolve_getattr(jzbu__qcgy, func_name
                )
        except AttributeError as dlywq__ntqe:
            lkglx__ihuow = None
        if lkglx__ihuow is None:
            raise BodoError(
                f"{caller_name}(): No Pandas method or Numpy function found with the name '{func_name}'."
                )
    return lkglx__ihuow


def get_udf_str_return_type(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    lkglx__ihuow = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(lkglx__ihuow, types.BoundFunction):
        if axis is not None:
            gytr__ynjd = lkglx__ihuow.get_call_type(typing_context, (), {
                'axis': axis})
        else:
            gytr__ynjd = lkglx__ihuow.get_call_type(typing_context, (), {})
        return gytr__ynjd.return_type
    else:
        if bodo.utils.typing.is_numpy_ufunc(lkglx__ihuow):
            gytr__ynjd = lkglx__ihuow.get_call_type(typing_context, (
                obj_dtype,), {})
            return gytr__ynjd.return_type
        raise BodoError(
            f"{caller_name}(): Only Pandas methods and np.ufunc are supported as string literals. '{func_name}' not supported."
            )


def get_pandas_method_str_impl(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    lkglx__ihuow = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(lkglx__ihuow, types.BoundFunction):
        fryan__ezq = lkglx__ihuow.template
        if axis is not None:
            return fryan__ezq._overload_func(obj_dtype, axis=axis)
        else:
            return fryan__ezq._overload_func(obj_dtype)
    return None


def dict_to_const_keys_var_values_lists(dict_var, func_ir, arg_types,
    typemap, updated_containers, require_const_map, label):
    require(isinstance(dict_var, ir.Var))
    wgo__tkvt = get_definition(func_ir, dict_var)
    require(isinstance(wgo__tkvt, ir.Expr))
    require(wgo__tkvt.op == 'build_map')
    yrwb__ejreq = wgo__tkvt.items
    uel__tcba = []
    values = []
    vlufm__tuvz = False
    for fafyf__exq in range(len(yrwb__ejreq)):
        aso__ozx, value = yrwb__ejreq[fafyf__exq]
        try:
            gan__zsut = get_const_value_inner(func_ir, aso__ozx, arg_types,
                typemap, updated_containers)
            uel__tcba.append(gan__zsut)
            values.append(value)
        except GuardException as dlywq__ntqe:
            require_const_map[aso__ozx] = label
            vlufm__tuvz = True
    if vlufm__tuvz:
        raise GuardException
    return uel__tcba, values


def _get_const_keys_from_dict(args, func_ir, build_map, err_msg, loc):
    try:
        uel__tcba = tuple(get_const_value_inner(func_ir, t[0], args) for t in
            build_map.items)
    except GuardException as dlywq__ntqe:
        raise BodoError(err_msg, loc)
    if not all(isinstance(c, (str, int)) for c in uel__tcba):
        raise BodoError(err_msg, loc)
    return uel__tcba


def _convert_const_key_dict(args, func_ir, build_map, err_msg, scope, loc,
    output_sentinel_tuple=False):
    uel__tcba = _get_const_keys_from_dict(args, func_ir, build_map, err_msg,
        loc)
    ndo__kyk = []
    bhr__zvg = [bodo.transforms.typing_pass._create_const_var(mukjg__ien,
        'dict_key', scope, loc, ndo__kyk) for mukjg__ien in uel__tcba]
    hhq__tftix = [t[1] for t in build_map.items]
    if output_sentinel_tuple:
        ugstz__wwuj = ir.Var(scope, mk_unique_var('sentinel'), loc)
        swz__emi = ir.Var(scope, mk_unique_var('dict_tup'), loc)
        ndo__kyk.append(ir.Assign(ir.Const('__bodo_tup', loc), ugstz__wwuj,
            loc))
        erxun__lmsc = [ugstz__wwuj] + bhr__zvg + hhq__tftix
        ndo__kyk.append(ir.Assign(ir.Expr.build_tuple(erxun__lmsc, loc),
            swz__emi, loc))
        return (swz__emi,), ndo__kyk
    else:
        jjzrn__jpqda = ir.Var(scope, mk_unique_var('values_tup'), loc)
        plr__yrg = ir.Var(scope, mk_unique_var('idx_tup'), loc)
        ndo__kyk.append(ir.Assign(ir.Expr.build_tuple(hhq__tftix, loc),
            jjzrn__jpqda, loc))
        ndo__kyk.append(ir.Assign(ir.Expr.build_tuple(bhr__zvg, loc),
            plr__yrg, loc))
        return (jjzrn__jpqda, plr__yrg), ndo__kyk
