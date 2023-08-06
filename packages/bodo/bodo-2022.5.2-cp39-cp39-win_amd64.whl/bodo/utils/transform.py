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
    rmhgt__dizhf = tuple(call_list)
    if rmhgt__dizhf in no_side_effect_call_tuples:
        return True
    if rmhgt__dizhf == (bodo.hiframes.pd_index_ext.init_range_index,):
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
    if len(rmhgt__dizhf) == 1 and tuple in getattr(rmhgt__dizhf[0],
        '__mro__', ()):
        return True
    return False


numba.core.ir_utils.remove_call_handlers.append(remove_hiframes)


def compile_func_single_block(func, args, ret_var, typing_info=None,
    extra_globals=None, infer_types=True, run_untyped_pass=False, flags=
    None, replace_globals=True):
    wim__flb = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd, 'math': math}
    if extra_globals is not None:
        wim__flb.update(extra_globals)
    if not replace_globals:
        wim__flb = func.__globals__
    loc = ir.Loc('', 0)
    if ret_var:
        loc = ret_var.loc
    if typing_info and infer_types:
        loc = typing_info.curr_loc
        f_ir = compile_to_numba_ir(func, wim__flb, typingctx=typing_info.
            typingctx, targetctx=typing_info.targetctx, arg_typs=tuple(
            typing_info.typemap[zst__oowze.name] for zst__oowze in args),
            typemap=typing_info.typemap, calltypes=typing_info.calltypes)
    else:
        f_ir = compile_to_numba_ir(func, wim__flb)
    assert len(f_ir.blocks
        ) == 1, 'only single block functions supported in compile_func_single_block()'
    if run_untyped_pass:
        vbrin__fqbqd = tuple(typing_info.typemap[zst__oowze.name] for
            zst__oowze in args)
        gah__lwskr = bodo.transforms.untyped_pass.UntypedPass(f_ir,
            typing_info.typingctx, vbrin__fqbqd, {}, {}, flags)
        gah__lwskr.run()
    tvkba__ryz = f_ir.blocks.popitem()[1]
    replace_arg_nodes(tvkba__ryz, args)
    uya__ktv = tvkba__ryz.body[:-2]
    update_locs(uya__ktv[len(args):], loc)
    for stmt in uya__ktv[:len(args)]:
        stmt.target.loc = loc
    if ret_var is not None:
        sild__wls = tvkba__ryz.body[-2]
        assert is_assign(sild__wls) and is_expr(sild__wls.value, 'cast')
        gem__bwdr = sild__wls.value.value
        uya__ktv.append(ir.Assign(gem__bwdr, ret_var, loc))
    return uya__ktv


def update_locs(node_list, loc):
    for stmt in node_list:
        stmt.loc = loc
        for eirs__yrej in stmt.list_vars():
            eirs__yrej.loc = loc
        if is_assign(stmt):
            stmt.value.loc = loc


def get_stmt_defs(stmt):
    if is_assign(stmt):
        return set([stmt.target.name])
    if type(stmt) in numba.core.analysis.ir_extension_usedefs:
        grpg__gajj = numba.core.analysis.ir_extension_usedefs[type(stmt)]
        hcnth__mxlu, axkeo__vmio = grpg__gajj(stmt)
        return axkeo__vmio
    return set()


def get_const_value(var, func_ir, err_msg, typemap=None, arg_types=None,
    file_info=None):
    if hasattr(var, 'loc'):
        loc = var.loc
    else:
        loc = None
    try:
        babu__cygk = get_const_value_inner(func_ir, var, arg_types, typemap,
            file_info=file_info)
        if isinstance(babu__cygk, ir.UndefinedType):
            irrds__qna = func_ir.get_definition(var.name).name
            raise BodoError(f"name '{irrds__qna}' is not defined", loc=loc)
    except GuardException as clr__hlccn:
        raise BodoError(err_msg, loc=loc)
    return babu__cygk


def get_const_value_inner(func_ir, var, arg_types=None, typemap=None,
    updated_containers=None, file_info=None, pyobject_to_literal=False,
    literalize_args=True):
    require(isinstance(var, ir.Var))
    xskd__kos = get_definition(func_ir, var)
    bmprh__ayehs = None
    if typemap is not None:
        bmprh__ayehs = typemap.get(var.name, None)
    if isinstance(xskd__kos, ir.Arg) and arg_types is not None:
        bmprh__ayehs = arg_types[xskd__kos.index]
    if updated_containers and var.name in updated_containers:
        raise BodoConstUpdatedError(
            f"variable '{var.name}' is updated inplace using '{updated_containers[var.name]}'"
            )
    if is_literal_type(bmprh__ayehs):
        return get_literal_value(bmprh__ayehs)
    if isinstance(xskd__kos, (ir.Const, ir.Global, ir.FreeVar)):
        babu__cygk = xskd__kos.value
        return babu__cygk
    if literalize_args and isinstance(xskd__kos, ir.Arg
        ) and can_literalize_type(bmprh__ayehs, pyobject_to_literal):
        raise numba.core.errors.ForceLiteralArg({xskd__kos.index}, loc=var.
            loc, file_infos={xskd__kos.index: file_info} if file_info is not
            None else None)
    if is_expr(xskd__kos, 'binop'):
        if file_info and xskd__kos.fn == operator.add:
            try:
                kxj__dezzv = get_const_value_inner(func_ir, xskd__kos.lhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(kxj__dezzv, True)
                plvb__uifo = get_const_value_inner(func_ir, xskd__kos.rhs,
                    arg_types, typemap, updated_containers, file_info)
                return xskd__kos.fn(kxj__dezzv, plvb__uifo)
            except (GuardException, BodoConstUpdatedError) as clr__hlccn:
                pass
            try:
                plvb__uifo = get_const_value_inner(func_ir, xskd__kos.rhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(plvb__uifo, False)
                kxj__dezzv = get_const_value_inner(func_ir, xskd__kos.lhs,
                    arg_types, typemap, updated_containers, file_info)
                return xskd__kos.fn(kxj__dezzv, plvb__uifo)
            except (GuardException, BodoConstUpdatedError) as clr__hlccn:
                pass
        kxj__dezzv = get_const_value_inner(func_ir, xskd__kos.lhs,
            arg_types, typemap, updated_containers)
        plvb__uifo = get_const_value_inner(func_ir, xskd__kos.rhs,
            arg_types, typemap, updated_containers)
        return xskd__kos.fn(kxj__dezzv, plvb__uifo)
    if is_expr(xskd__kos, 'unary'):
        babu__cygk = get_const_value_inner(func_ir, xskd__kos.value,
            arg_types, typemap, updated_containers)
        return xskd__kos.fn(babu__cygk)
    if is_expr(xskd__kos, 'getattr') and typemap:
        vdkn__sdh = typemap.get(xskd__kos.value.name, None)
        if isinstance(vdkn__sdh, bodo.hiframes.pd_dataframe_ext.DataFrameType
            ) and xskd__kos.attr == 'columns':
            return pd.Index(vdkn__sdh.columns)
        if isinstance(vdkn__sdh, types.SliceType):
            tbf__xkpkk = get_definition(func_ir, xskd__kos.value)
            require(is_call(tbf__xkpkk))
            tcz__azmmj = find_callname(func_ir, tbf__xkpkk)
            wipq__thq = False
            if tcz__azmmj == ('_normalize_slice', 'numba.cpython.unicode'):
                require(xskd__kos.attr in ('start', 'step'))
                tbf__xkpkk = get_definition(func_ir, tbf__xkpkk.args[0])
                wipq__thq = True
            require(find_callname(func_ir, tbf__xkpkk) == ('slice', 'builtins')
                )
            if len(tbf__xkpkk.args) == 1:
                if xskd__kos.attr == 'start':
                    return 0
                if xskd__kos.attr == 'step':
                    return 1
                require(xskd__kos.attr == 'stop')
                return get_const_value_inner(func_ir, tbf__xkpkk.args[0],
                    arg_types, typemap, updated_containers)
            if xskd__kos.attr == 'start':
                babu__cygk = get_const_value_inner(func_ir, tbf__xkpkk.args
                    [0], arg_types, typemap, updated_containers)
                if babu__cygk is None:
                    babu__cygk = 0
                if wipq__thq:
                    require(babu__cygk == 0)
                return babu__cygk
            if xskd__kos.attr == 'stop':
                assert not wipq__thq
                return get_const_value_inner(func_ir, tbf__xkpkk.args[1],
                    arg_types, typemap, updated_containers)
            require(xskd__kos.attr == 'step')
            if len(tbf__xkpkk.args) == 2:
                return 1
            else:
                babu__cygk = get_const_value_inner(func_ir, tbf__xkpkk.args
                    [2], arg_types, typemap, updated_containers)
                if babu__cygk is None:
                    babu__cygk = 1
                if wipq__thq:
                    require(babu__cygk == 1)
                return babu__cygk
    if is_expr(xskd__kos, 'getattr'):
        return getattr(get_const_value_inner(func_ir, xskd__kos.value,
            arg_types, typemap, updated_containers), xskd__kos.attr)
    if is_expr(xskd__kos, 'getitem'):
        value = get_const_value_inner(func_ir, xskd__kos.value, arg_types,
            typemap, updated_containers)
        index = get_const_value_inner(func_ir, xskd__kos.index, arg_types,
            typemap, updated_containers)
        return value[index]
    hxoa__xkozr = guard(find_callname, func_ir, xskd__kos, typemap)
    if hxoa__xkozr is not None and len(hxoa__xkozr) == 2 and hxoa__xkozr[0
        ] == 'keys' and isinstance(hxoa__xkozr[1], ir.Var):
        nmo__role = xskd__kos.func
        xskd__kos = get_definition(func_ir, hxoa__xkozr[1])
        cvnz__por = hxoa__xkozr[1].name
        if updated_containers and cvnz__por in updated_containers:
            raise BodoConstUpdatedError(
                "variable '{}' is updated inplace using '{}'".format(
                cvnz__por, updated_containers[cvnz__por]))
        require(is_expr(xskd__kos, 'build_map'))
        vals = [eirs__yrej[0] for eirs__yrej in xskd__kos.items]
        cfl__maqtc = guard(get_definition, func_ir, nmo__role)
        assert isinstance(cfl__maqtc, ir.Expr) and cfl__maqtc.attr == 'keys'
        cfl__maqtc.attr = 'copy'
        return [get_const_value_inner(func_ir, eirs__yrej, arg_types,
            typemap, updated_containers) for eirs__yrej in vals]
    if is_expr(xskd__kos, 'build_map'):
        return {get_const_value_inner(func_ir, eirs__yrej[0], arg_types,
            typemap, updated_containers): get_const_value_inner(func_ir,
            eirs__yrej[1], arg_types, typemap, updated_containers) for
            eirs__yrej in xskd__kos.items}
    if is_expr(xskd__kos, 'build_tuple'):
        return tuple(get_const_value_inner(func_ir, eirs__yrej, arg_types,
            typemap, updated_containers) for eirs__yrej in xskd__kos.items)
    if is_expr(xskd__kos, 'build_list'):
        return [get_const_value_inner(func_ir, eirs__yrej, arg_types,
            typemap, updated_containers) for eirs__yrej in xskd__kos.items]
    if is_expr(xskd__kos, 'build_set'):
        return {get_const_value_inner(func_ir, eirs__yrej, arg_types,
            typemap, updated_containers) for eirs__yrej in xskd__kos.items}
    if hxoa__xkozr == ('list', 'builtins'):
        values = get_const_value_inner(func_ir, xskd__kos.args[0],
            arg_types, typemap, updated_containers)
        if isinstance(values, set):
            values = sorted(values)
        return list(values)
    if hxoa__xkozr == ('set', 'builtins'):
        return set(get_const_value_inner(func_ir, xskd__kos.args[0],
            arg_types, typemap, updated_containers))
    if hxoa__xkozr == ('range', 'builtins') and len(xskd__kos.args) == 1:
        return range(get_const_value_inner(func_ir, xskd__kos.args[0],
            arg_types, typemap, updated_containers))
    if hxoa__xkozr == ('slice', 'builtins'):
        return slice(*tuple(get_const_value_inner(func_ir, eirs__yrej,
            arg_types, typemap, updated_containers) for eirs__yrej in
            xskd__kos.args))
    if hxoa__xkozr == ('str', 'builtins'):
        return str(get_const_value_inner(func_ir, xskd__kos.args[0],
            arg_types, typemap, updated_containers))
    if hxoa__xkozr == ('bool', 'builtins'):
        return bool(get_const_value_inner(func_ir, xskd__kos.args[0],
            arg_types, typemap, updated_containers))
    if hxoa__xkozr == ('format', 'builtins'):
        zst__oowze = get_const_value_inner(func_ir, xskd__kos.args[0],
            arg_types, typemap, updated_containers)
        kiedg__egg = get_const_value_inner(func_ir, xskd__kos.args[1],
            arg_types, typemap, updated_containers) if len(xskd__kos.args
            ) > 1 else ''
        return format(zst__oowze, kiedg__egg)
    if hxoa__xkozr in (('init_binary_str_index',
        'bodo.hiframes.pd_index_ext'), ('init_numeric_index',
        'bodo.hiframes.pd_index_ext'), ('init_categorical_index',
        'bodo.hiframes.pd_index_ext'), ('init_datetime_index',
        'bodo.hiframes.pd_index_ext'), ('init_timedelta_index',
        'bodo.hiframes.pd_index_ext'), ('init_heter_index',
        'bodo.hiframes.pd_index_ext')):
        return pd.Index(get_const_value_inner(func_ir, xskd__kos.args[0],
            arg_types, typemap, updated_containers))
    if hxoa__xkozr == ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'):
        return np.array(get_const_value_inner(func_ir, xskd__kos.args[0],
            arg_types, typemap, updated_containers))
    if hxoa__xkozr == ('init_range_index', 'bodo.hiframes.pd_index_ext'):
        return pd.RangeIndex(get_const_value_inner(func_ir, xskd__kos.args[
            0], arg_types, typemap, updated_containers),
            get_const_value_inner(func_ir, xskd__kos.args[1], arg_types,
            typemap, updated_containers), get_const_value_inner(func_ir,
            xskd__kos.args[2], arg_types, typemap, updated_containers))
    if hxoa__xkozr == ('len', 'builtins') and typemap and isinstance(typemap
        .get(xskd__kos.args[0].name, None), types.BaseTuple):
        return len(typemap[xskd__kos.args[0].name])
    if hxoa__xkozr == ('len', 'builtins'):
        hvoc__kdj = guard(get_definition, func_ir, xskd__kos.args[0])
        if isinstance(hvoc__kdj, ir.Expr) and hvoc__kdj.op in ('build_tuple',
            'build_list', 'build_set', 'build_map'):
            return len(hvoc__kdj.items)
        return len(get_const_value_inner(func_ir, xskd__kos.args[0],
            arg_types, typemap, updated_containers))
    if hxoa__xkozr == ('CategoricalDtype', 'pandas'):
        kws = dict(xskd__kos.kws)
        iaoi__ugvo = get_call_expr_arg('CategoricalDtype', xskd__kos.args,
            kws, 0, 'categories', '')
        nwufd__lpke = get_call_expr_arg('CategoricalDtype', xskd__kos.args,
            kws, 1, 'ordered', False)
        if nwufd__lpke is not False:
            nwufd__lpke = get_const_value_inner(func_ir, nwufd__lpke,
                arg_types, typemap, updated_containers)
        if iaoi__ugvo == '':
            iaoi__ugvo = None
        else:
            iaoi__ugvo = get_const_value_inner(func_ir, iaoi__ugvo,
                arg_types, typemap, updated_containers)
        return pd.CategoricalDtype(iaoi__ugvo, nwufd__lpke)
    if hxoa__xkozr == ('dtype', 'numpy'):
        return np.dtype(get_const_value_inner(func_ir, xskd__kos.args[0],
            arg_types, typemap, updated_containers))
    if hxoa__xkozr is not None and len(hxoa__xkozr) == 2 and hxoa__xkozr[1
        ] == 'pandas' and hxoa__xkozr[0] in ('Int8Dtype', 'Int16Dtype',
        'Int32Dtype', 'Int64Dtype', 'UInt8Dtype', 'UInt16Dtype',
        'UInt32Dtype', 'UInt64Dtype'):
        return getattr(pd, hxoa__xkozr[0])()
    if hxoa__xkozr is not None and len(hxoa__xkozr) == 2 and isinstance(
        hxoa__xkozr[1], ir.Var):
        babu__cygk = get_const_value_inner(func_ir, hxoa__xkozr[1],
            arg_types, typemap, updated_containers)
        args = [get_const_value_inner(func_ir, eirs__yrej, arg_types,
            typemap, updated_containers) for eirs__yrej in xskd__kos.args]
        kws = {sbm__gquz[0]: get_const_value_inner(func_ir, sbm__gquz[1],
            arg_types, typemap, updated_containers) for sbm__gquz in
            xskd__kos.kws}
        return getattr(babu__cygk, hxoa__xkozr[0])(*args, **kws)
    if hxoa__xkozr is not None and len(hxoa__xkozr) == 2 and hxoa__xkozr[1
        ] == 'bodo' and hxoa__xkozr[0] in bodo_types_with_params:
        args = tuple(get_const_value_inner(func_ir, eirs__yrej, arg_types,
            typemap, updated_containers) for eirs__yrej in xskd__kos.args)
        kwargs = {irrds__qna: get_const_value_inner(func_ir, eirs__yrej,
            arg_types, typemap, updated_containers) for irrds__qna,
            eirs__yrej in dict(xskd__kos.kws).items()}
        return getattr(bodo, hxoa__xkozr[0])(*args, **kwargs)
    if is_call(xskd__kos) and typemap and isinstance(typemap.get(xskd__kos.
        func.name, None), types.Dispatcher):
        py_func = typemap[xskd__kos.func.name].dispatcher.py_func
        require(xskd__kos.vararg is None)
        args = tuple(get_const_value_inner(func_ir, eirs__yrej, arg_types,
            typemap, updated_containers) for eirs__yrej in xskd__kos.args)
        kwargs = {irrds__qna: get_const_value_inner(func_ir, eirs__yrej,
            arg_types, typemap, updated_containers) for irrds__qna,
            eirs__yrej in dict(xskd__kos.kws).items()}
        arg_types = tuple(bodo.typeof(eirs__yrej) for eirs__yrej in args)
        kw_types = {qvpk__rek: bodo.typeof(eirs__yrej) for qvpk__rek,
            eirs__yrej in kwargs.items()}
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
    f_ir, typemap, qkq__jrubm, qkq__jrubm = bodo.compiler.get_func_type_info(
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
                    mfjlz__srx = guard(get_definition, f_ir, rhs.func)
                    if isinstance(mfjlz__srx, ir.Const) and isinstance(
                        mfjlz__srx.value, numba.core.dispatcher.
                        ObjModeLiftedWith):
                        return False
                    wliac__jbg = guard(find_callname, f_ir, rhs)
                    if wliac__jbg is None:
                        return False
                    func_name, wtmxa__vpuda = wliac__jbg
                    if wtmxa__vpuda == 'pandas' and func_name.startswith(
                        'read_'):
                        return False
                    if wliac__jbg in (('fromfile', 'numpy'), ('file_read',
                        'bodo.io.np_io')):
                        return False
                    if wliac__jbg == ('File', 'h5py'):
                        return False
                    if isinstance(wtmxa__vpuda, ir.Var):
                        bmprh__ayehs = typemap[wtmxa__vpuda.name]
                        if isinstance(bmprh__ayehs, (DataFrameType, SeriesType)
                            ) and func_name in ('to_csv', 'to_excel',
                            'to_json', 'to_sql', 'to_pickle', 'to_parquet',
                            'info'):
                            return False
                        if isinstance(bmprh__ayehs, types.Array
                            ) and func_name == 'tofile':
                            return False
                        if isinstance(bmprh__ayehs, bodo.LoggingLoggerType):
                            return False
                        if str(bmprh__ayehs).startswith('Mpl'):
                            return False
                        if (func_name in container_update_method_names and
                            isinstance(guard(get_definition, f_ir,
                            wtmxa__vpuda), ir.Arg)):
                            return False
                    if wtmxa__vpuda in ('numpy.random', 'time', 'logging',
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
        ylclw__fww = func.literal_value.code
        ijtql__lzxt = {'np': np, 'pd': pd, 'numba': numba, 'bodo': bodo}
        if hasattr(func.literal_value, 'globals'):
            ijtql__lzxt = func.literal_value.globals
        f_ir = numba.core.ir_utils.get_ir_of_code(ijtql__lzxt, ylclw__fww)
        fix_struct_return(f_ir)
        typemap, zyqi__tpa, jgc__kgxtm, qkq__jrubm = (numba.core.
            typed_passes.type_inference_stage(typing_context,
            target_context, f_ir, arg_types, None))
    elif isinstance(func, bodo.utils.typing.FunctionLiteral):
        py_func = func.literal_value
        f_ir, typemap, jgc__kgxtm, zyqi__tpa = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    elif isinstance(func, CPUDispatcher):
        py_func = func.py_func
        f_ir, typemap, jgc__kgxtm, zyqi__tpa = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    else:
        if not isinstance(func, types.Dispatcher):
            if isinstance(func, types.Function):
                raise BodoError(
                    f'Bodo does not support built-in functions yet, {func}')
            else:
                raise BodoError(f'Function type expected, not {func}')
        py_func = func.dispatcher.py_func
        f_ir, typemap, jgc__kgxtm, zyqi__tpa = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    if is_udf and isinstance(zyqi__tpa, types.DictType):
        pss__jpm = guard(get_struct_keynames, f_ir, typemap)
        if pss__jpm is not None:
            zyqi__tpa = StructType((zyqi__tpa.value_type,) * len(pss__jpm),
                pss__jpm)
    if is_udf and isinstance(zyqi__tpa, (SeriesType, HeterogeneousSeriesType)):
        oitpu__aczp = numba.core.registry.cpu_target.typing_context
        tvn__zlgba = numba.core.registry.cpu_target.target_context
        zjaoy__nlb = bodo.transforms.series_pass.SeriesPass(f_ir,
            oitpu__aczp, tvn__zlgba, typemap, jgc__kgxtm, {})
        zjaoy__nlb.run()
        zjaoy__nlb.run()
        zjaoy__nlb.run()
        fad__gema = compute_cfg_from_blocks(f_ir.blocks)
        uacov__voqge = [guard(_get_const_series_info, f_ir.blocks[
            pgy__okocd], f_ir, typemap) for pgy__okocd in fad__gema.
            exit_points() if isinstance(f_ir.blocks[pgy__okocd].body[-1],
            ir.Return)]
        if None in uacov__voqge or len(pd.Series(uacov__voqge).unique()) != 1:
            zyqi__tpa.const_info = None
        else:
            zyqi__tpa.const_info = uacov__voqge[0]
    return zyqi__tpa


def _get_const_series_info(block, f_ir, typemap):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType
    assert isinstance(block.body[-1], ir.Return)
    pfc__zzjh = block.body[-1].value
    dpp__lszc = get_definition(f_ir, pfc__zzjh)
    require(is_expr(dpp__lszc, 'cast'))
    dpp__lszc = get_definition(f_ir, dpp__lszc.value)
    require(is_call(dpp__lszc) and find_callname(f_ir, dpp__lszc) == (
        'init_series', 'bodo.hiframes.pd_series_ext'))
    wmxha__qkac = dpp__lszc.args[1]
    zxqpl__ftj = tuple(get_const_value_inner(f_ir, wmxha__qkac, typemap=
        typemap))
    if isinstance(typemap[pfc__zzjh.name], HeterogeneousSeriesType):
        return len(typemap[pfc__zzjh.name].data), zxqpl__ftj
    hwew__fxee = dpp__lszc.args[0]
    ouf__nsml = get_definition(f_ir, hwew__fxee)
    func_name, cil__vvurn = find_callname(f_ir, ouf__nsml)
    if is_call(ouf__nsml) and bodo.utils.utils.is_alloc_callname(func_name,
        cil__vvurn):
        gujeq__rmsi = ouf__nsml.args[0]
        bxm__tfoj = get_const_value_inner(f_ir, gujeq__rmsi, typemap=typemap)
        return bxm__tfoj, zxqpl__ftj
    if is_call(ouf__nsml) and find_callname(f_ir, ouf__nsml) in [('asarray',
        'numpy'), ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'), (
        'build_nullable_tuple', 'bodo.libs.nullable_tuple_ext')]:
        hwew__fxee = ouf__nsml.args[0]
        ouf__nsml = get_definition(f_ir, hwew__fxee)
    require(is_expr(ouf__nsml, 'build_tuple') or is_expr(ouf__nsml,
        'build_list'))
    return len(ouf__nsml.items), zxqpl__ftj


def extract_keyvals_from_struct_map(f_ir, build_map, loc, scope, typemap=None):
    yotl__vwvi = []
    cpq__hscd = []
    values = []
    for qvpk__rek, eirs__yrej in build_map.items:
        kjlxn__gbv = find_const(f_ir, qvpk__rek)
        require(isinstance(kjlxn__gbv, str))
        cpq__hscd.append(kjlxn__gbv)
        yotl__vwvi.append(qvpk__rek)
        values.append(eirs__yrej)
    yzb__mas = ir.Var(scope, mk_unique_var('val_tup'), loc)
    qry__kem = ir.Assign(ir.Expr.build_tuple(values, loc), yzb__mas, loc)
    f_ir._definitions[yzb__mas.name] = [qry__kem.value]
    hvd__iyy = ir.Var(scope, mk_unique_var('key_tup'), loc)
    hows__squk = ir.Assign(ir.Expr.build_tuple(yotl__vwvi, loc), hvd__iyy, loc)
    f_ir._definitions[hvd__iyy.name] = [hows__squk.value]
    if typemap is not None:
        typemap[yzb__mas.name] = types.Tuple([typemap[eirs__yrej.name] for
            eirs__yrej in values])
        typemap[hvd__iyy.name] = types.Tuple([typemap[eirs__yrej.name] for
            eirs__yrej in yotl__vwvi])
    return cpq__hscd, yzb__mas, qry__kem, hvd__iyy, hows__squk


def _replace_const_map_return(f_ir, block, label):
    require(isinstance(block.body[-1], ir.Return))
    pxr__jwxu = block.body[-1].value
    zss__xyoh = guard(get_definition, f_ir, pxr__jwxu)
    require(is_expr(zss__xyoh, 'cast'))
    dpp__lszc = guard(get_definition, f_ir, zss__xyoh.value)
    require(is_expr(dpp__lszc, 'build_map'))
    require(len(dpp__lszc.items) > 0)
    loc = block.loc
    scope = block.scope
    cpq__hscd, yzb__mas, qry__kem, hvd__iyy, hows__squk = (
        extract_keyvals_from_struct_map(f_ir, dpp__lszc, loc, scope))
    ejhip__rgev = ir.Var(scope, mk_unique_var('conv_call'), loc)
    gkwn__fhmt = ir.Assign(ir.Global('struct_if_heter_dict', bodo.utils.
        conversion.struct_if_heter_dict, loc), ejhip__rgev, loc)
    f_ir._definitions[ejhip__rgev.name] = [gkwn__fhmt.value]
    zak__awj = ir.Var(scope, mk_unique_var('struct_val'), loc)
    ouzz__fwzty = ir.Assign(ir.Expr.call(ejhip__rgev, [yzb__mas, hvd__iyy],
        {}, loc), zak__awj, loc)
    f_ir._definitions[zak__awj.name] = [ouzz__fwzty.value]
    zss__xyoh.value = zak__awj
    dpp__lszc.items = [(qvpk__rek, qvpk__rek) for qvpk__rek, qkq__jrubm in
        dpp__lszc.items]
    block.body = block.body[:-2] + [qry__kem, hows__squk, gkwn__fhmt,
        ouzz__fwzty] + block.body[-2:]
    return tuple(cpq__hscd)


def get_struct_keynames(f_ir, typemap):
    fad__gema = compute_cfg_from_blocks(f_ir.blocks)
    atyo__gsx = list(fad__gema.exit_points())[0]
    block = f_ir.blocks[atyo__gsx]
    require(isinstance(block.body[-1], ir.Return))
    pxr__jwxu = block.body[-1].value
    zss__xyoh = guard(get_definition, f_ir, pxr__jwxu)
    require(is_expr(zss__xyoh, 'cast'))
    dpp__lszc = guard(get_definition, f_ir, zss__xyoh.value)
    require(is_call(dpp__lszc) and find_callname(f_ir, dpp__lszc) == (
        'struct_if_heter_dict', 'bodo.utils.conversion'))
    return get_overload_const_list(typemap[dpp__lszc.args[1].name])


def fix_struct_return(f_ir):
    qykkt__hnwd = None
    fad__gema = compute_cfg_from_blocks(f_ir.blocks)
    for atyo__gsx in fad__gema.exit_points():
        qykkt__hnwd = guard(_replace_const_map_return, f_ir, f_ir.blocks[
            atyo__gsx], atyo__gsx)
    return qykkt__hnwd


def update_node_list_definitions(node_list, func_ir):
    loc = ir.Loc('', 0)
    deww__xsbc = ir.Block(ir.Scope(None, loc), loc)
    deww__xsbc.body = node_list
    build_definitions({(0): deww__xsbc}, func_ir._definitions)
    return


NESTED_TUP_SENTINEL = '$BODO_NESTED_TUP'


def gen_const_val_str(c):
    if isinstance(c, tuple):
        return "'{}{}', ".format(NESTED_TUP_SENTINEL, len(c)) + ', '.join(
            gen_const_val_str(eirs__yrej) for eirs__yrej in c)
    if isinstance(c, str):
        return "'{}'".format(c)
    if isinstance(c, (pd.Timestamp, pd.Timedelta, float)):
        return "'{}'".format(c)
    return str(c)


def gen_const_tup(vals):
    olf__psdsw = ', '.join(gen_const_val_str(c) for c in vals)
    return '({}{})'.format(olf__psdsw, ',' if len(vals) == 1 else '')


def get_const_tup_vals(c_typ):
    vals = get_overload_const_list(c_typ)
    return _get_original_nested_tups(vals)


def _get_original_nested_tups(vals):
    for noanf__xqwys in range(len(vals) - 1, -1, -1):
        eirs__yrej = vals[noanf__xqwys]
        if isinstance(eirs__yrej, str) and eirs__yrej.startswith(
            NESTED_TUP_SENTINEL):
            wprza__vxac = int(eirs__yrej[len(NESTED_TUP_SENTINEL):])
            return _get_original_nested_tups(tuple(vals[:noanf__xqwys]) + (
                tuple(vals[noanf__xqwys + 1:noanf__xqwys + wprza__vxac + 1]
                ),) + tuple(vals[noanf__xqwys + wprza__vxac + 1:]))
    return tuple(vals)


def get_call_expr_arg(f_name, args, kws, arg_no, arg_name, default=None,
    err_msg=None, use_default=False):
    zst__oowze = None
    if len(args) > arg_no and arg_no >= 0:
        zst__oowze = args[arg_no]
        if arg_name in kws:
            err_msg = (
                f"{f_name}() got multiple values for argument '{arg_name}'")
            raise BodoError(err_msg)
    elif arg_name in kws:
        zst__oowze = kws[arg_name]
    if zst__oowze is None:
        if use_default or default is not None:
            return default
        if err_msg is None:
            err_msg = "{} requires '{}' argument".format(f_name, arg_name)
        raise BodoError(err_msg)
    return zst__oowze


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
    wim__flb = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd}
    if extra_globals is not None:
        wim__flb.update(extra_globals)
    func.__globals__.update(wim__flb)
    if pysig is not None:
        pre_nodes = [] if pre_nodes is None else pre_nodes
        scope = next(iter(pass_info.func_ir.blocks.values())).scope
        loc = scope.loc

        def normal_handler(index, param, default):
            return default

        def default_handler(index, param, default):
            jxzc__qrgd = ir.Var(scope, mk_unique_var('defaults'), loc)
            try:
                pass_info.typemap[jxzc__qrgd.name] = types.literal(default)
            except:
                pass_info.typemap[jxzc__qrgd.name] = numba.typeof(default)
            clqo__mflzu = ir.Assign(ir.Const(default, loc), jxzc__qrgd, loc)
            pre_nodes.append(clqo__mflzu)
            return jxzc__qrgd
        args = numba.core.typing.fold_arguments(pysig, args, kws,
            normal_handler, default_handler, normal_handler)
    vbrin__fqbqd = tuple(pass_info.typemap[eirs__yrej.name] for eirs__yrej in
        args)
    if const:
        bfhhy__tkidi = []
        for noanf__xqwys, zst__oowze in enumerate(args):
            babu__cygk = guard(find_const, pass_info.func_ir, zst__oowze)
            if babu__cygk:
                bfhhy__tkidi.append(types.literal(babu__cygk))
            else:
                bfhhy__tkidi.append(vbrin__fqbqd[noanf__xqwys])
        vbrin__fqbqd = tuple(bfhhy__tkidi)
    return ReplaceFunc(func, vbrin__fqbqd, args, wim__flb,
        inline_bodo_calls, run_full_pipeline, pre_nodes)


def is_var_size_item_array_type(t):
    assert is_array_typ(t, False)
    return t == string_array_type or isinstance(t, ArrayItemArrayType
        ) or isinstance(t, StructArrayType) and any(
        is_var_size_item_array_type(wwo__pmx) for wwo__pmx in t.data)


def gen_init_varsize_alloc_sizes(t):
    if t == string_array_type:
        evh__wufo = 'num_chars_{}'.format(ir_utils.next_label())
        return f'  {evh__wufo} = 0\n', (evh__wufo,)
    if isinstance(t, ArrayItemArrayType):
        ykky__xyns, wpse__sykwz = gen_init_varsize_alloc_sizes(t.dtype)
        evh__wufo = 'num_items_{}'.format(ir_utils.next_label())
        return f'  {evh__wufo} = 0\n' + ykky__xyns, (evh__wufo,) + wpse__sykwz
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
        return 1 + sum(get_type_alloc_counts(wwo__pmx.dtype) for wwo__pmx in
            t.data)
    if isinstance(t, ArrayItemArrayType) or t == string_array_type:
        return 1 + get_type_alloc_counts(t.dtype)
    if isinstance(t, MapArrayType):
        return get_type_alloc_counts(t.key_arr_type) + get_type_alloc_counts(t
            .value_arr_type)
    if bodo.utils.utils.is_array_typ(t, False) or t == bodo.string_type:
        return 1
    if isinstance(t, StructType):
        return sum(get_type_alloc_counts(wwo__pmx) for wwo__pmx in t.data)
    if isinstance(t, types.BaseTuple):
        return sum(get_type_alloc_counts(wwo__pmx) for wwo__pmx in t.types)
    return 0


def find_udf_str_name(obj_dtype, func_name, typing_context, caller_name):
    mtoc__xcgqz = typing_context.resolve_getattr(obj_dtype, func_name)
    if mtoc__xcgqz is None:
        zegn__szrfu = types.misc.Module(np)
        try:
            mtoc__xcgqz = typing_context.resolve_getattr(zegn__szrfu, func_name
                )
        except AttributeError as clr__hlccn:
            mtoc__xcgqz = None
        if mtoc__xcgqz is None:
            raise BodoError(
                f"{caller_name}(): No Pandas method or Numpy function found with the name '{func_name}'."
                )
    return mtoc__xcgqz


def get_udf_str_return_type(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    mtoc__xcgqz = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(mtoc__xcgqz, types.BoundFunction):
        if axis is not None:
            lidyt__tbas = mtoc__xcgqz.get_call_type(typing_context, (), {
                'axis': axis})
        else:
            lidyt__tbas = mtoc__xcgqz.get_call_type(typing_context, (), {})
        return lidyt__tbas.return_type
    else:
        if bodo.utils.typing.is_numpy_ufunc(mtoc__xcgqz):
            lidyt__tbas = mtoc__xcgqz.get_call_type(typing_context, (
                obj_dtype,), {})
            return lidyt__tbas.return_type
        raise BodoError(
            f"{caller_name}(): Only Pandas methods and np.ufunc are supported as string literals. '{func_name}' not supported."
            )


def get_pandas_method_str_impl(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    mtoc__xcgqz = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(mtoc__xcgqz, types.BoundFunction):
        cxzju__nslvt = mtoc__xcgqz.template
        if axis is not None:
            return cxzju__nslvt._overload_func(obj_dtype, axis=axis)
        else:
            return cxzju__nslvt._overload_func(obj_dtype)
    return None


def dict_to_const_keys_var_values_lists(dict_var, func_ir, arg_types,
    typemap, updated_containers, require_const_map, label):
    require(isinstance(dict_var, ir.Var))
    tftba__sdpjl = get_definition(func_ir, dict_var)
    require(isinstance(tftba__sdpjl, ir.Expr))
    require(tftba__sdpjl.op == 'build_map')
    ffzqz__ztw = tftba__sdpjl.items
    yotl__vwvi = []
    values = []
    xtc__hrop = False
    for noanf__xqwys in range(len(ffzqz__ztw)):
        alkrx__towx, value = ffzqz__ztw[noanf__xqwys]
        try:
            yppw__otuuu = get_const_value_inner(func_ir, alkrx__towx,
                arg_types, typemap, updated_containers)
            yotl__vwvi.append(yppw__otuuu)
            values.append(value)
        except GuardException as clr__hlccn:
            require_const_map[alkrx__towx] = label
            xtc__hrop = True
    if xtc__hrop:
        raise GuardException
    return yotl__vwvi, values


def _get_const_keys_from_dict(args, func_ir, build_map, err_msg, loc):
    try:
        yotl__vwvi = tuple(get_const_value_inner(func_ir, t[0], args) for t in
            build_map.items)
    except GuardException as clr__hlccn:
        raise BodoError(err_msg, loc)
    if not all(isinstance(c, (str, int)) for c in yotl__vwvi):
        raise BodoError(err_msg, loc)
    return yotl__vwvi


def _convert_const_key_dict(args, func_ir, build_map, err_msg, scope, loc,
    output_sentinel_tuple=False):
    yotl__vwvi = _get_const_keys_from_dict(args, func_ir, build_map,
        err_msg, loc)
    bdrvz__htf = []
    atp__bps = [bodo.transforms.typing_pass._create_const_var(qvpk__rek,
        'dict_key', scope, loc, bdrvz__htf) for qvpk__rek in yotl__vwvi]
    ncqv__vzsz = [t[1] for t in build_map.items]
    if output_sentinel_tuple:
        tukzq__ngr = ir.Var(scope, mk_unique_var('sentinel'), loc)
        nvk__xlr = ir.Var(scope, mk_unique_var('dict_tup'), loc)
        bdrvz__htf.append(ir.Assign(ir.Const('__bodo_tup', loc), tukzq__ngr,
            loc))
        pndjc__wdlyd = [tukzq__ngr] + atp__bps + ncqv__vzsz
        bdrvz__htf.append(ir.Assign(ir.Expr.build_tuple(pndjc__wdlyd, loc),
            nvk__xlr, loc))
        return (nvk__xlr,), bdrvz__htf
    else:
        ekniy__ogdqo = ir.Var(scope, mk_unique_var('values_tup'), loc)
        xbh__mtalb = ir.Var(scope, mk_unique_var('idx_tup'), loc)
        bdrvz__htf.append(ir.Assign(ir.Expr.build_tuple(ncqv__vzsz, loc),
            ekniy__ogdqo, loc))
        bdrvz__htf.append(ir.Assign(ir.Expr.build_tuple(atp__bps, loc),
            xbh__mtalb, loc))
        return (ekniy__ogdqo, xbh__mtalb), bdrvz__htf
