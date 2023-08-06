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
    didsu__yvmqt = tuple(call_list)
    if didsu__yvmqt in no_side_effect_call_tuples:
        return True
    if didsu__yvmqt == (bodo.hiframes.pd_index_ext.init_range_index,):
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
    if len(didsu__yvmqt) == 1 and tuple in getattr(didsu__yvmqt[0],
        '__mro__', ()):
        return True
    return False


numba.core.ir_utils.remove_call_handlers.append(remove_hiframes)


def compile_func_single_block(func, args, ret_var, typing_info=None,
    extra_globals=None, infer_types=True, run_untyped_pass=False, flags=
    None, replace_globals=True):
    loelr__day = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd, 'math':
        math}
    if extra_globals is not None:
        loelr__day.update(extra_globals)
    if not replace_globals:
        loelr__day = func.__globals__
    loc = ir.Loc('', 0)
    if ret_var:
        loc = ret_var.loc
    if typing_info and infer_types:
        loc = typing_info.curr_loc
        f_ir = compile_to_numba_ir(func, loelr__day, typingctx=typing_info.
            typingctx, targetctx=typing_info.targetctx, arg_typs=tuple(
            typing_info.typemap[tkm__yond.name] for tkm__yond in args),
            typemap=typing_info.typemap, calltypes=typing_info.calltypes)
    else:
        f_ir = compile_to_numba_ir(func, loelr__day)
    assert len(f_ir.blocks
        ) == 1, 'only single block functions supported in compile_func_single_block()'
    if run_untyped_pass:
        iln__qimyo = tuple(typing_info.typemap[tkm__yond.name] for
            tkm__yond in args)
        scy__huyqc = bodo.transforms.untyped_pass.UntypedPass(f_ir,
            typing_info.typingctx, iln__qimyo, {}, {}, flags)
        scy__huyqc.run()
    btxq__vlic = f_ir.blocks.popitem()[1]
    replace_arg_nodes(btxq__vlic, args)
    zdnr__exz = btxq__vlic.body[:-2]
    update_locs(zdnr__exz[len(args):], loc)
    for stmt in zdnr__exz[:len(args)]:
        stmt.target.loc = loc
    if ret_var is not None:
        wbll__szqyx = btxq__vlic.body[-2]
        assert is_assign(wbll__szqyx) and is_expr(wbll__szqyx.value, 'cast')
        beee__lqktm = wbll__szqyx.value.value
        zdnr__exz.append(ir.Assign(beee__lqktm, ret_var, loc))
    return zdnr__exz


def update_locs(node_list, loc):
    for stmt in node_list:
        stmt.loc = loc
        for yfc__mfzyw in stmt.list_vars():
            yfc__mfzyw.loc = loc
        if is_assign(stmt):
            stmt.value.loc = loc


def get_stmt_defs(stmt):
    if is_assign(stmt):
        return set([stmt.target.name])
    if type(stmt) in numba.core.analysis.ir_extension_usedefs:
        fluj__qfm = numba.core.analysis.ir_extension_usedefs[type(stmt)]
        xyh__hdlmv, zptt__btkxx = fluj__qfm(stmt)
        return zptt__btkxx
    return set()


def get_const_value(var, func_ir, err_msg, typemap=None, arg_types=None,
    file_info=None):
    if hasattr(var, 'loc'):
        loc = var.loc
    else:
        loc = None
    try:
        czww__bzebm = get_const_value_inner(func_ir, var, arg_types,
            typemap, file_info=file_info)
        if isinstance(czww__bzebm, ir.UndefinedType):
            dbbr__fxpag = func_ir.get_definition(var.name).name
            raise BodoError(f"name '{dbbr__fxpag}' is not defined", loc=loc)
    except GuardException as qrn__lup:
        raise BodoError(err_msg, loc=loc)
    return czww__bzebm


def get_const_value_inner(func_ir, var, arg_types=None, typemap=None,
    updated_containers=None, file_info=None, pyobject_to_literal=False,
    literalize_args=True):
    require(isinstance(var, ir.Var))
    kvc__aei = get_definition(func_ir, var)
    daw__uaywl = None
    if typemap is not None:
        daw__uaywl = typemap.get(var.name, None)
    if isinstance(kvc__aei, ir.Arg) and arg_types is not None:
        daw__uaywl = arg_types[kvc__aei.index]
    if updated_containers and var.name in updated_containers:
        raise BodoConstUpdatedError(
            f"variable '{var.name}' is updated inplace using '{updated_containers[var.name]}'"
            )
    if is_literal_type(daw__uaywl):
        return get_literal_value(daw__uaywl)
    if isinstance(kvc__aei, (ir.Const, ir.Global, ir.FreeVar)):
        czww__bzebm = kvc__aei.value
        return czww__bzebm
    if literalize_args and isinstance(kvc__aei, ir.Arg
        ) and can_literalize_type(daw__uaywl, pyobject_to_literal):
        raise numba.core.errors.ForceLiteralArg({kvc__aei.index}, loc=var.
            loc, file_infos={kvc__aei.index: file_info} if file_info is not
            None else None)
    if is_expr(kvc__aei, 'binop'):
        if file_info and kvc__aei.fn == operator.add:
            try:
                dnacc__yxyt = get_const_value_inner(func_ir, kvc__aei.lhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(dnacc__yxyt, True)
                amr__ljru = get_const_value_inner(func_ir, kvc__aei.rhs,
                    arg_types, typemap, updated_containers, file_info)
                return kvc__aei.fn(dnacc__yxyt, amr__ljru)
            except (GuardException, BodoConstUpdatedError) as qrn__lup:
                pass
            try:
                amr__ljru = get_const_value_inner(func_ir, kvc__aei.rhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(amr__ljru, False)
                dnacc__yxyt = get_const_value_inner(func_ir, kvc__aei.lhs,
                    arg_types, typemap, updated_containers, file_info)
                return kvc__aei.fn(dnacc__yxyt, amr__ljru)
            except (GuardException, BodoConstUpdatedError) as qrn__lup:
                pass
        dnacc__yxyt = get_const_value_inner(func_ir, kvc__aei.lhs,
            arg_types, typemap, updated_containers)
        amr__ljru = get_const_value_inner(func_ir, kvc__aei.rhs, arg_types,
            typemap, updated_containers)
        return kvc__aei.fn(dnacc__yxyt, amr__ljru)
    if is_expr(kvc__aei, 'unary'):
        czww__bzebm = get_const_value_inner(func_ir, kvc__aei.value,
            arg_types, typemap, updated_containers)
        return kvc__aei.fn(czww__bzebm)
    if is_expr(kvc__aei, 'getattr') and typemap:
        kcl__ntzf = typemap.get(kvc__aei.value.name, None)
        if isinstance(kcl__ntzf, bodo.hiframes.pd_dataframe_ext.DataFrameType
            ) and kvc__aei.attr == 'columns':
            return pd.Index(kcl__ntzf.columns)
        if isinstance(kcl__ntzf, types.SliceType):
            ycnfw__ywii = get_definition(func_ir, kvc__aei.value)
            require(is_call(ycnfw__ywii))
            oyuur__idx = find_callname(func_ir, ycnfw__ywii)
            dycy__eyvs = False
            if oyuur__idx == ('_normalize_slice', 'numba.cpython.unicode'):
                require(kvc__aei.attr in ('start', 'step'))
                ycnfw__ywii = get_definition(func_ir, ycnfw__ywii.args[0])
                dycy__eyvs = True
            require(find_callname(func_ir, ycnfw__ywii) == ('slice',
                'builtins'))
            if len(ycnfw__ywii.args) == 1:
                if kvc__aei.attr == 'start':
                    return 0
                if kvc__aei.attr == 'step':
                    return 1
                require(kvc__aei.attr == 'stop')
                return get_const_value_inner(func_ir, ycnfw__ywii.args[0],
                    arg_types, typemap, updated_containers)
            if kvc__aei.attr == 'start':
                czww__bzebm = get_const_value_inner(func_ir, ycnfw__ywii.
                    args[0], arg_types, typemap, updated_containers)
                if czww__bzebm is None:
                    czww__bzebm = 0
                if dycy__eyvs:
                    require(czww__bzebm == 0)
                return czww__bzebm
            if kvc__aei.attr == 'stop':
                assert not dycy__eyvs
                return get_const_value_inner(func_ir, ycnfw__ywii.args[1],
                    arg_types, typemap, updated_containers)
            require(kvc__aei.attr == 'step')
            if len(ycnfw__ywii.args) == 2:
                return 1
            else:
                czww__bzebm = get_const_value_inner(func_ir, ycnfw__ywii.
                    args[2], arg_types, typemap, updated_containers)
                if czww__bzebm is None:
                    czww__bzebm = 1
                if dycy__eyvs:
                    require(czww__bzebm == 1)
                return czww__bzebm
    if is_expr(kvc__aei, 'getattr'):
        return getattr(get_const_value_inner(func_ir, kvc__aei.value,
            arg_types, typemap, updated_containers), kvc__aei.attr)
    if is_expr(kvc__aei, 'getitem'):
        value = get_const_value_inner(func_ir, kvc__aei.value, arg_types,
            typemap, updated_containers)
        index = get_const_value_inner(func_ir, kvc__aei.index, arg_types,
            typemap, updated_containers)
        return value[index]
    oev__zrgxg = guard(find_callname, func_ir, kvc__aei, typemap)
    if oev__zrgxg is not None and len(oev__zrgxg) == 2 and oev__zrgxg[0
        ] == 'keys' and isinstance(oev__zrgxg[1], ir.Var):
        ezmgz__pctqh = kvc__aei.func
        kvc__aei = get_definition(func_ir, oev__zrgxg[1])
        gdsx__bmjza = oev__zrgxg[1].name
        if updated_containers and gdsx__bmjza in updated_containers:
            raise BodoConstUpdatedError(
                "variable '{}' is updated inplace using '{}'".format(
                gdsx__bmjza, updated_containers[gdsx__bmjza]))
        require(is_expr(kvc__aei, 'build_map'))
        vals = [yfc__mfzyw[0] for yfc__mfzyw in kvc__aei.items]
        dqoa__tjql = guard(get_definition, func_ir, ezmgz__pctqh)
        assert isinstance(dqoa__tjql, ir.Expr) and dqoa__tjql.attr == 'keys'
        dqoa__tjql.attr = 'copy'
        return [get_const_value_inner(func_ir, yfc__mfzyw, arg_types,
            typemap, updated_containers) for yfc__mfzyw in vals]
    if is_expr(kvc__aei, 'build_map'):
        return {get_const_value_inner(func_ir, yfc__mfzyw[0], arg_types,
            typemap, updated_containers): get_const_value_inner(func_ir,
            yfc__mfzyw[1], arg_types, typemap, updated_containers) for
            yfc__mfzyw in kvc__aei.items}
    if is_expr(kvc__aei, 'build_tuple'):
        return tuple(get_const_value_inner(func_ir, yfc__mfzyw, arg_types,
            typemap, updated_containers) for yfc__mfzyw in kvc__aei.items)
    if is_expr(kvc__aei, 'build_list'):
        return [get_const_value_inner(func_ir, yfc__mfzyw, arg_types,
            typemap, updated_containers) for yfc__mfzyw in kvc__aei.items]
    if is_expr(kvc__aei, 'build_set'):
        return {get_const_value_inner(func_ir, yfc__mfzyw, arg_types,
            typemap, updated_containers) for yfc__mfzyw in kvc__aei.items}
    if oev__zrgxg == ('list', 'builtins'):
        values = get_const_value_inner(func_ir, kvc__aei.args[0], arg_types,
            typemap, updated_containers)
        if isinstance(values, set):
            values = sorted(values)
        return list(values)
    if oev__zrgxg == ('set', 'builtins'):
        return set(get_const_value_inner(func_ir, kvc__aei.args[0],
            arg_types, typemap, updated_containers))
    if oev__zrgxg == ('range', 'builtins') and len(kvc__aei.args) == 1:
        return range(get_const_value_inner(func_ir, kvc__aei.args[0],
            arg_types, typemap, updated_containers))
    if oev__zrgxg == ('slice', 'builtins'):
        return slice(*tuple(get_const_value_inner(func_ir, yfc__mfzyw,
            arg_types, typemap, updated_containers) for yfc__mfzyw in
            kvc__aei.args))
    if oev__zrgxg == ('str', 'builtins'):
        return str(get_const_value_inner(func_ir, kvc__aei.args[0],
            arg_types, typemap, updated_containers))
    if oev__zrgxg == ('bool', 'builtins'):
        return bool(get_const_value_inner(func_ir, kvc__aei.args[0],
            arg_types, typemap, updated_containers))
    if oev__zrgxg == ('format', 'builtins'):
        tkm__yond = get_const_value_inner(func_ir, kvc__aei.args[0],
            arg_types, typemap, updated_containers)
        jfp__smton = get_const_value_inner(func_ir, kvc__aei.args[1],
            arg_types, typemap, updated_containers) if len(kvc__aei.args
            ) > 1 else ''
        return format(tkm__yond, jfp__smton)
    if oev__zrgxg in (('init_binary_str_index',
        'bodo.hiframes.pd_index_ext'), ('init_numeric_index',
        'bodo.hiframes.pd_index_ext'), ('init_categorical_index',
        'bodo.hiframes.pd_index_ext'), ('init_datetime_index',
        'bodo.hiframes.pd_index_ext'), ('init_timedelta_index',
        'bodo.hiframes.pd_index_ext'), ('init_heter_index',
        'bodo.hiframes.pd_index_ext')):
        return pd.Index(get_const_value_inner(func_ir, kvc__aei.args[0],
            arg_types, typemap, updated_containers))
    if oev__zrgxg == ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'):
        return np.array(get_const_value_inner(func_ir, kvc__aei.args[0],
            arg_types, typemap, updated_containers))
    if oev__zrgxg == ('init_range_index', 'bodo.hiframes.pd_index_ext'):
        return pd.RangeIndex(get_const_value_inner(func_ir, kvc__aei.args[0
            ], arg_types, typemap, updated_containers),
            get_const_value_inner(func_ir, kvc__aei.args[1], arg_types,
            typemap, updated_containers), get_const_value_inner(func_ir,
            kvc__aei.args[2], arg_types, typemap, updated_containers))
    if oev__zrgxg == ('len', 'builtins') and typemap and isinstance(typemap
        .get(kvc__aei.args[0].name, None), types.BaseTuple):
        return len(typemap[kvc__aei.args[0].name])
    if oev__zrgxg == ('len', 'builtins'):
        wju__qhvir = guard(get_definition, func_ir, kvc__aei.args[0])
        if isinstance(wju__qhvir, ir.Expr) and wju__qhvir.op in ('build_tuple',
            'build_list', 'build_set', 'build_map'):
            return len(wju__qhvir.items)
        return len(get_const_value_inner(func_ir, kvc__aei.args[0],
            arg_types, typemap, updated_containers))
    if oev__zrgxg == ('CategoricalDtype', 'pandas'):
        kws = dict(kvc__aei.kws)
        snyq__xvqd = get_call_expr_arg('CategoricalDtype', kvc__aei.args,
            kws, 0, 'categories', '')
        nofeo__ayr = get_call_expr_arg('CategoricalDtype', kvc__aei.args,
            kws, 1, 'ordered', False)
        if nofeo__ayr is not False:
            nofeo__ayr = get_const_value_inner(func_ir, nofeo__ayr,
                arg_types, typemap, updated_containers)
        if snyq__xvqd == '':
            snyq__xvqd = None
        else:
            snyq__xvqd = get_const_value_inner(func_ir, snyq__xvqd,
                arg_types, typemap, updated_containers)
        return pd.CategoricalDtype(snyq__xvqd, nofeo__ayr)
    if oev__zrgxg == ('dtype', 'numpy'):
        return np.dtype(get_const_value_inner(func_ir, kvc__aei.args[0],
            arg_types, typemap, updated_containers))
    if oev__zrgxg is not None and len(oev__zrgxg) == 2 and oev__zrgxg[1
        ] == 'pandas' and oev__zrgxg[0] in ('Int8Dtype', 'Int16Dtype',
        'Int32Dtype', 'Int64Dtype', 'UInt8Dtype', 'UInt16Dtype',
        'UInt32Dtype', 'UInt64Dtype'):
        return getattr(pd, oev__zrgxg[0])()
    if oev__zrgxg is not None and len(oev__zrgxg) == 2 and isinstance(
        oev__zrgxg[1], ir.Var):
        czww__bzebm = get_const_value_inner(func_ir, oev__zrgxg[1],
            arg_types, typemap, updated_containers)
        args = [get_const_value_inner(func_ir, yfc__mfzyw, arg_types,
            typemap, updated_containers) for yfc__mfzyw in kvc__aei.args]
        kws = {uvjhq__crmx[0]: get_const_value_inner(func_ir, uvjhq__crmx[1
            ], arg_types, typemap, updated_containers) for uvjhq__crmx in
            kvc__aei.kws}
        return getattr(czww__bzebm, oev__zrgxg[0])(*args, **kws)
    if oev__zrgxg is not None and len(oev__zrgxg) == 2 and oev__zrgxg[1
        ] == 'bodo' and oev__zrgxg[0] in bodo_types_with_params:
        args = tuple(get_const_value_inner(func_ir, yfc__mfzyw, arg_types,
            typemap, updated_containers) for yfc__mfzyw in kvc__aei.args)
        kwargs = {dbbr__fxpag: get_const_value_inner(func_ir, yfc__mfzyw,
            arg_types, typemap, updated_containers) for dbbr__fxpag,
            yfc__mfzyw in dict(kvc__aei.kws).items()}
        return getattr(bodo, oev__zrgxg[0])(*args, **kwargs)
    if is_call(kvc__aei) and typemap and isinstance(typemap.get(kvc__aei.
        func.name, None), types.Dispatcher):
        py_func = typemap[kvc__aei.func.name].dispatcher.py_func
        require(kvc__aei.vararg is None)
        args = tuple(get_const_value_inner(func_ir, yfc__mfzyw, arg_types,
            typemap, updated_containers) for yfc__mfzyw in kvc__aei.args)
        kwargs = {dbbr__fxpag: get_const_value_inner(func_ir, yfc__mfzyw,
            arg_types, typemap, updated_containers) for dbbr__fxpag,
            yfc__mfzyw in dict(kvc__aei.kws).items()}
        arg_types = tuple(bodo.typeof(yfc__mfzyw) for yfc__mfzyw in args)
        kw_types = {iyb__hqlm: bodo.typeof(yfc__mfzyw) for iyb__hqlm,
            yfc__mfzyw in kwargs.items()}
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
    f_ir, typemap, zqias__wvou, zqias__wvou = bodo.compiler.get_func_type_info(
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
                    obm__ckae = guard(get_definition, f_ir, rhs.func)
                    if isinstance(obm__ckae, ir.Const) and isinstance(obm__ckae
                        .value, numba.core.dispatcher.ObjModeLiftedWith):
                        return False
                    kdxr__xho = guard(find_callname, f_ir, rhs)
                    if kdxr__xho is None:
                        return False
                    func_name, mdzxv__rbk = kdxr__xho
                    if mdzxv__rbk == 'pandas' and func_name.startswith('read_'
                        ):
                        return False
                    if kdxr__xho in (('fromfile', 'numpy'), ('file_read',
                        'bodo.io.np_io')):
                        return False
                    if kdxr__xho == ('File', 'h5py'):
                        return False
                    if isinstance(mdzxv__rbk, ir.Var):
                        daw__uaywl = typemap[mdzxv__rbk.name]
                        if isinstance(daw__uaywl, (DataFrameType, SeriesType)
                            ) and func_name in ('to_csv', 'to_excel',
                            'to_json', 'to_sql', 'to_pickle', 'to_parquet',
                            'info'):
                            return False
                        if isinstance(daw__uaywl, types.Array
                            ) and func_name == 'tofile':
                            return False
                        if isinstance(daw__uaywl, bodo.LoggingLoggerType):
                            return False
                        if str(daw__uaywl).startswith('Mpl'):
                            return False
                        if (func_name in container_update_method_names and
                            isinstance(guard(get_definition, f_ir,
                            mdzxv__rbk), ir.Arg)):
                            return False
                    if mdzxv__rbk in ('numpy.random', 'time', 'logging',
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
        vop__trxj = func.literal_value.code
        jxr__yuicq = {'np': np, 'pd': pd, 'numba': numba, 'bodo': bodo}
        if hasattr(func.literal_value, 'globals'):
            jxr__yuicq = func.literal_value.globals
        f_ir = numba.core.ir_utils.get_ir_of_code(jxr__yuicq, vop__trxj)
        fix_struct_return(f_ir)
        typemap, bafqx__kbb, ich__eps, zqias__wvou = (numba.core.
            typed_passes.type_inference_stage(typing_context,
            target_context, f_ir, arg_types, None))
    elif isinstance(func, bodo.utils.typing.FunctionLiteral):
        py_func = func.literal_value
        f_ir, typemap, ich__eps, bafqx__kbb = bodo.compiler.get_func_type_info(
            py_func, arg_types, kw_types)
    elif isinstance(func, CPUDispatcher):
        py_func = func.py_func
        f_ir, typemap, ich__eps, bafqx__kbb = bodo.compiler.get_func_type_info(
            py_func, arg_types, kw_types)
    else:
        if not isinstance(func, types.Dispatcher):
            if isinstance(func, types.Function):
                raise BodoError(
                    f'Bodo does not support built-in functions yet, {func}')
            else:
                raise BodoError(f'Function type expected, not {func}')
        py_func = func.dispatcher.py_func
        f_ir, typemap, ich__eps, bafqx__kbb = bodo.compiler.get_func_type_info(
            py_func, arg_types, kw_types)
    if is_udf and isinstance(bafqx__kbb, types.DictType):
        jofl__dhcto = guard(get_struct_keynames, f_ir, typemap)
        if jofl__dhcto is not None:
            bafqx__kbb = StructType((bafqx__kbb.value_type,) * len(
                jofl__dhcto), jofl__dhcto)
    if is_udf and isinstance(bafqx__kbb, (SeriesType, HeterogeneousSeriesType)
        ):
        amr__niofv = numba.core.registry.cpu_target.typing_context
        jvpv__mfb = numba.core.registry.cpu_target.target_context
        kifd__vrl = bodo.transforms.series_pass.SeriesPass(f_ir, amr__niofv,
            jvpv__mfb, typemap, ich__eps, {})
        kifd__vrl.run()
        kifd__vrl.run()
        kifd__vrl.run()
        woxja__fbz = compute_cfg_from_blocks(f_ir.blocks)
        awmxo__yddm = [guard(_get_const_series_info, f_ir.blocks[ofs__ukr],
            f_ir, typemap) for ofs__ukr in woxja__fbz.exit_points() if
            isinstance(f_ir.blocks[ofs__ukr].body[-1], ir.Return)]
        if None in awmxo__yddm or len(pd.Series(awmxo__yddm).unique()) != 1:
            bafqx__kbb.const_info = None
        else:
            bafqx__kbb.const_info = awmxo__yddm[0]
    return bafqx__kbb


def _get_const_series_info(block, f_ir, typemap):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType
    assert isinstance(block.body[-1], ir.Return)
    kwugq__gfbd = block.body[-1].value
    egym__hnz = get_definition(f_ir, kwugq__gfbd)
    require(is_expr(egym__hnz, 'cast'))
    egym__hnz = get_definition(f_ir, egym__hnz.value)
    require(is_call(egym__hnz) and find_callname(f_ir, egym__hnz) == (
        'init_series', 'bodo.hiframes.pd_series_ext'))
    dhpl__lkq = egym__hnz.args[1]
    qjxbg__iam = tuple(get_const_value_inner(f_ir, dhpl__lkq, typemap=typemap))
    if isinstance(typemap[kwugq__gfbd.name], HeterogeneousSeriesType):
        return len(typemap[kwugq__gfbd.name].data), qjxbg__iam
    inq__crkp = egym__hnz.args[0]
    vsp__snngq = get_definition(f_ir, inq__crkp)
    func_name, khyeh__xvwn = find_callname(f_ir, vsp__snngq)
    if is_call(vsp__snngq) and bodo.utils.utils.is_alloc_callname(func_name,
        khyeh__xvwn):
        wiac__rgb = vsp__snngq.args[0]
        alu__vyy = get_const_value_inner(f_ir, wiac__rgb, typemap=typemap)
        return alu__vyy, qjxbg__iam
    if is_call(vsp__snngq) and find_callname(f_ir, vsp__snngq) in [(
        'asarray', 'numpy'), ('str_arr_from_sequence',
        'bodo.libs.str_arr_ext'), ('build_nullable_tuple',
        'bodo.libs.nullable_tuple_ext')]:
        inq__crkp = vsp__snngq.args[0]
        vsp__snngq = get_definition(f_ir, inq__crkp)
    require(is_expr(vsp__snngq, 'build_tuple') or is_expr(vsp__snngq,
        'build_list'))
    return len(vsp__snngq.items), qjxbg__iam


def extract_keyvals_from_struct_map(f_ir, build_map, loc, scope, typemap=None):
    vkwg__cmphz = []
    app__uwlu = []
    values = []
    for iyb__hqlm, yfc__mfzyw in build_map.items:
        mez__npwj = find_const(f_ir, iyb__hqlm)
        require(isinstance(mez__npwj, str))
        app__uwlu.append(mez__npwj)
        vkwg__cmphz.append(iyb__hqlm)
        values.append(yfc__mfzyw)
    rjcql__jwvq = ir.Var(scope, mk_unique_var('val_tup'), loc)
    kjll__znceg = ir.Assign(ir.Expr.build_tuple(values, loc), rjcql__jwvq, loc)
    f_ir._definitions[rjcql__jwvq.name] = [kjll__znceg.value]
    dem__fryn = ir.Var(scope, mk_unique_var('key_tup'), loc)
    lnpe__vood = ir.Assign(ir.Expr.build_tuple(vkwg__cmphz, loc), dem__fryn,
        loc)
    f_ir._definitions[dem__fryn.name] = [lnpe__vood.value]
    if typemap is not None:
        typemap[rjcql__jwvq.name] = types.Tuple([typemap[yfc__mfzyw.name] for
            yfc__mfzyw in values])
        typemap[dem__fryn.name] = types.Tuple([typemap[yfc__mfzyw.name] for
            yfc__mfzyw in vkwg__cmphz])
    return app__uwlu, rjcql__jwvq, kjll__znceg, dem__fryn, lnpe__vood


def _replace_const_map_return(f_ir, block, label):
    require(isinstance(block.body[-1], ir.Return))
    ijsm__mabt = block.body[-1].value
    enbji__hjiyq = guard(get_definition, f_ir, ijsm__mabt)
    require(is_expr(enbji__hjiyq, 'cast'))
    egym__hnz = guard(get_definition, f_ir, enbji__hjiyq.value)
    require(is_expr(egym__hnz, 'build_map'))
    require(len(egym__hnz.items) > 0)
    loc = block.loc
    scope = block.scope
    app__uwlu, rjcql__jwvq, kjll__znceg, dem__fryn, lnpe__vood = (
        extract_keyvals_from_struct_map(f_ir, egym__hnz, loc, scope))
    fou__anue = ir.Var(scope, mk_unique_var('conv_call'), loc)
    lwt__krnu = ir.Assign(ir.Global('struct_if_heter_dict', bodo.utils.
        conversion.struct_if_heter_dict, loc), fou__anue, loc)
    f_ir._definitions[fou__anue.name] = [lwt__krnu.value]
    pte__txw = ir.Var(scope, mk_unique_var('struct_val'), loc)
    bdne__zagd = ir.Assign(ir.Expr.call(fou__anue, [rjcql__jwvq, dem__fryn],
        {}, loc), pte__txw, loc)
    f_ir._definitions[pte__txw.name] = [bdne__zagd.value]
    enbji__hjiyq.value = pte__txw
    egym__hnz.items = [(iyb__hqlm, iyb__hqlm) for iyb__hqlm, zqias__wvou in
        egym__hnz.items]
    block.body = block.body[:-2] + [kjll__znceg, lnpe__vood, lwt__krnu,
        bdne__zagd] + block.body[-2:]
    return tuple(app__uwlu)


def get_struct_keynames(f_ir, typemap):
    woxja__fbz = compute_cfg_from_blocks(f_ir.blocks)
    uwgv__uiv = list(woxja__fbz.exit_points())[0]
    block = f_ir.blocks[uwgv__uiv]
    require(isinstance(block.body[-1], ir.Return))
    ijsm__mabt = block.body[-1].value
    enbji__hjiyq = guard(get_definition, f_ir, ijsm__mabt)
    require(is_expr(enbji__hjiyq, 'cast'))
    egym__hnz = guard(get_definition, f_ir, enbji__hjiyq.value)
    require(is_call(egym__hnz) and find_callname(f_ir, egym__hnz) == (
        'struct_if_heter_dict', 'bodo.utils.conversion'))
    return get_overload_const_list(typemap[egym__hnz.args[1].name])


def fix_struct_return(f_ir):
    kzp__mtc = None
    woxja__fbz = compute_cfg_from_blocks(f_ir.blocks)
    for uwgv__uiv in woxja__fbz.exit_points():
        kzp__mtc = guard(_replace_const_map_return, f_ir, f_ir.blocks[
            uwgv__uiv], uwgv__uiv)
    return kzp__mtc


def update_node_list_definitions(node_list, func_ir):
    loc = ir.Loc('', 0)
    gyr__uvlxd = ir.Block(ir.Scope(None, loc), loc)
    gyr__uvlxd.body = node_list
    build_definitions({(0): gyr__uvlxd}, func_ir._definitions)
    return


NESTED_TUP_SENTINEL = '$BODO_NESTED_TUP'


def gen_const_val_str(c):
    if isinstance(c, tuple):
        return "'{}{}', ".format(NESTED_TUP_SENTINEL, len(c)) + ', '.join(
            gen_const_val_str(yfc__mfzyw) for yfc__mfzyw in c)
    if isinstance(c, str):
        return "'{}'".format(c)
    if isinstance(c, (pd.Timestamp, pd.Timedelta, float)):
        return "'{}'".format(c)
    return str(c)


def gen_const_tup(vals):
    qut__lkb = ', '.join(gen_const_val_str(c) for c in vals)
    return '({}{})'.format(qut__lkb, ',' if len(vals) == 1 else '')


def get_const_tup_vals(c_typ):
    vals = get_overload_const_list(c_typ)
    return _get_original_nested_tups(vals)


def _get_original_nested_tups(vals):
    for dxm__vvgv in range(len(vals) - 1, -1, -1):
        yfc__mfzyw = vals[dxm__vvgv]
        if isinstance(yfc__mfzyw, str) and yfc__mfzyw.startswith(
            NESTED_TUP_SENTINEL):
            mejn__nkpqx = int(yfc__mfzyw[len(NESTED_TUP_SENTINEL):])
            return _get_original_nested_tups(tuple(vals[:dxm__vvgv]) + (
                tuple(vals[dxm__vvgv + 1:dxm__vvgv + mejn__nkpqx + 1]),) +
                tuple(vals[dxm__vvgv + mejn__nkpqx + 1:]))
    return tuple(vals)


def get_call_expr_arg(f_name, args, kws, arg_no, arg_name, default=None,
    err_msg=None, use_default=False):
    tkm__yond = None
    if len(args) > arg_no and arg_no >= 0:
        tkm__yond = args[arg_no]
        if arg_name in kws:
            err_msg = (
                f"{f_name}() got multiple values for argument '{arg_name}'")
            raise BodoError(err_msg)
    elif arg_name in kws:
        tkm__yond = kws[arg_name]
    if tkm__yond is None:
        if use_default or default is not None:
            return default
        if err_msg is None:
            err_msg = "{} requires '{}' argument".format(f_name, arg_name)
        raise BodoError(err_msg)
    return tkm__yond


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
    loelr__day = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd}
    if extra_globals is not None:
        loelr__day.update(extra_globals)
    func.__globals__.update(loelr__day)
    if pysig is not None:
        pre_nodes = [] if pre_nodes is None else pre_nodes
        scope = next(iter(pass_info.func_ir.blocks.values())).scope
        loc = scope.loc

        def normal_handler(index, param, default):
            return default

        def default_handler(index, param, default):
            eia__cykv = ir.Var(scope, mk_unique_var('defaults'), loc)
            try:
                pass_info.typemap[eia__cykv.name] = types.literal(default)
            except:
                pass_info.typemap[eia__cykv.name] = numba.typeof(default)
            uwtaz__eace = ir.Assign(ir.Const(default, loc), eia__cykv, loc)
            pre_nodes.append(uwtaz__eace)
            return eia__cykv
        args = numba.core.typing.fold_arguments(pysig, args, kws,
            normal_handler, default_handler, normal_handler)
    iln__qimyo = tuple(pass_info.typemap[yfc__mfzyw.name] for yfc__mfzyw in
        args)
    if const:
        yptg__jrs = []
        for dxm__vvgv, tkm__yond in enumerate(args):
            czww__bzebm = guard(find_const, pass_info.func_ir, tkm__yond)
            if czww__bzebm:
                yptg__jrs.append(types.literal(czww__bzebm))
            else:
                yptg__jrs.append(iln__qimyo[dxm__vvgv])
        iln__qimyo = tuple(yptg__jrs)
    return ReplaceFunc(func, iln__qimyo, args, loelr__day,
        inline_bodo_calls, run_full_pipeline, pre_nodes)


def is_var_size_item_array_type(t):
    assert is_array_typ(t, False)
    return t == string_array_type or isinstance(t, ArrayItemArrayType
        ) or isinstance(t, StructArrayType) and any(
        is_var_size_item_array_type(doga__wks) for doga__wks in t.data)


def gen_init_varsize_alloc_sizes(t):
    if t == string_array_type:
        spo__nbkcd = 'num_chars_{}'.format(ir_utils.next_label())
        return f'  {spo__nbkcd} = 0\n', (spo__nbkcd,)
    if isinstance(t, ArrayItemArrayType):
        sqt__xxk, tke__sktqd = gen_init_varsize_alloc_sizes(t.dtype)
        spo__nbkcd = 'num_items_{}'.format(ir_utils.next_label())
        return f'  {spo__nbkcd} = 0\n' + sqt__xxk, (spo__nbkcd,) + tke__sktqd
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
        return 1 + sum(get_type_alloc_counts(doga__wks.dtype) for doga__wks in
            t.data)
    if isinstance(t, ArrayItemArrayType) or t == string_array_type:
        return 1 + get_type_alloc_counts(t.dtype)
    if isinstance(t, MapArrayType):
        return get_type_alloc_counts(t.key_arr_type) + get_type_alloc_counts(t
            .value_arr_type)
    if bodo.utils.utils.is_array_typ(t, False) or t == bodo.string_type:
        return 1
    if isinstance(t, StructType):
        return sum(get_type_alloc_counts(doga__wks) for doga__wks in t.data)
    if isinstance(t, types.BaseTuple):
        return sum(get_type_alloc_counts(doga__wks) for doga__wks in t.types)
    return 0


def find_udf_str_name(obj_dtype, func_name, typing_context, caller_name):
    qelwq__vklgs = typing_context.resolve_getattr(obj_dtype, func_name)
    if qelwq__vklgs is None:
        dhrlv__ilztb = types.misc.Module(np)
        try:
            qelwq__vklgs = typing_context.resolve_getattr(dhrlv__ilztb,
                func_name)
        except AttributeError as qrn__lup:
            qelwq__vklgs = None
        if qelwq__vklgs is None:
            raise BodoError(
                f"{caller_name}(): No Pandas method or Numpy function found with the name '{func_name}'."
                )
    return qelwq__vklgs


def get_udf_str_return_type(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    qelwq__vklgs = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(qelwq__vklgs, types.BoundFunction):
        if axis is not None:
            hddft__kflip = qelwq__vklgs.get_call_type(typing_context, (), {
                'axis': axis})
        else:
            hddft__kflip = qelwq__vklgs.get_call_type(typing_context, (), {})
        return hddft__kflip.return_type
    else:
        if bodo.utils.typing.is_numpy_ufunc(qelwq__vklgs):
            hddft__kflip = qelwq__vklgs.get_call_type(typing_context, (
                obj_dtype,), {})
            return hddft__kflip.return_type
        raise BodoError(
            f"{caller_name}(): Only Pandas methods and np.ufunc are supported as string literals. '{func_name}' not supported."
            )


def get_pandas_method_str_impl(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    qelwq__vklgs = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(qelwq__vklgs, types.BoundFunction):
        npse__zdt = qelwq__vklgs.template
        if axis is not None:
            return npse__zdt._overload_func(obj_dtype, axis=axis)
        else:
            return npse__zdt._overload_func(obj_dtype)
    return None


def dict_to_const_keys_var_values_lists(dict_var, func_ir, arg_types,
    typemap, updated_containers, require_const_map, label):
    require(isinstance(dict_var, ir.Var))
    bgotg__krtgb = get_definition(func_ir, dict_var)
    require(isinstance(bgotg__krtgb, ir.Expr))
    require(bgotg__krtgb.op == 'build_map')
    nnldw__xmos = bgotg__krtgb.items
    vkwg__cmphz = []
    values = []
    jemvg__kuvds = False
    for dxm__vvgv in range(len(nnldw__xmos)):
        hre__nvvrs, value = nnldw__xmos[dxm__vvgv]
        try:
            nog__xzo = get_const_value_inner(func_ir, hre__nvvrs, arg_types,
                typemap, updated_containers)
            vkwg__cmphz.append(nog__xzo)
            values.append(value)
        except GuardException as qrn__lup:
            require_const_map[hre__nvvrs] = label
            jemvg__kuvds = True
    if jemvg__kuvds:
        raise GuardException
    return vkwg__cmphz, values


def _get_const_keys_from_dict(args, func_ir, build_map, err_msg, loc):
    try:
        vkwg__cmphz = tuple(get_const_value_inner(func_ir, t[0], args) for
            t in build_map.items)
    except GuardException as qrn__lup:
        raise BodoError(err_msg, loc)
    if not all(isinstance(c, (str, int)) for c in vkwg__cmphz):
        raise BodoError(err_msg, loc)
    return vkwg__cmphz


def _convert_const_key_dict(args, func_ir, build_map, err_msg, scope, loc,
    output_sentinel_tuple=False):
    vkwg__cmphz = _get_const_keys_from_dict(args, func_ir, build_map,
        err_msg, loc)
    potm__txun = []
    jedh__orpud = [bodo.transforms.typing_pass._create_const_var(iyb__hqlm,
        'dict_key', scope, loc, potm__txun) for iyb__hqlm in vkwg__cmphz]
    oyryw__eulyl = [t[1] for t in build_map.items]
    if output_sentinel_tuple:
        ddl__cew = ir.Var(scope, mk_unique_var('sentinel'), loc)
        ixici__jdv = ir.Var(scope, mk_unique_var('dict_tup'), loc)
        potm__txun.append(ir.Assign(ir.Const('__bodo_tup', loc), ddl__cew, loc)
            )
        wiqj__slbze = [ddl__cew] + jedh__orpud + oyryw__eulyl
        potm__txun.append(ir.Assign(ir.Expr.build_tuple(wiqj__slbze, loc),
            ixici__jdv, loc))
        return (ixici__jdv,), potm__txun
    else:
        irdd__qzc = ir.Var(scope, mk_unique_var('values_tup'), loc)
        fpgee__bdlz = ir.Var(scope, mk_unique_var('idx_tup'), loc)
        potm__txun.append(ir.Assign(ir.Expr.build_tuple(oyryw__eulyl, loc),
            irdd__qzc, loc))
        potm__txun.append(ir.Assign(ir.Expr.build_tuple(jedh__orpud, loc),
            fpgee__bdlz, loc))
        return (irdd__qzc, fpgee__bdlz), potm__txun
