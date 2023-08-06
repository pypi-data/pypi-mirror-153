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
    odup__fqszn = tuple(call_list)
    if odup__fqszn in no_side_effect_call_tuples:
        return True
    if odup__fqszn == (bodo.hiframes.pd_index_ext.init_range_index,):
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
    if len(odup__fqszn) == 1 and tuple in getattr(odup__fqszn[0], '__mro__', ()
        ):
        return True
    return False


numba.core.ir_utils.remove_call_handlers.append(remove_hiframes)


def compile_func_single_block(func, args, ret_var, typing_info=None,
    extra_globals=None, infer_types=True, run_untyped_pass=False, flags=
    None, replace_globals=True):
    nsn__ibpqu = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd, 'math':
        math}
    if extra_globals is not None:
        nsn__ibpqu.update(extra_globals)
    if not replace_globals:
        nsn__ibpqu = func.__globals__
    loc = ir.Loc('', 0)
    if ret_var:
        loc = ret_var.loc
    if typing_info and infer_types:
        loc = typing_info.curr_loc
        f_ir = compile_to_numba_ir(func, nsn__ibpqu, typingctx=typing_info.
            typingctx, targetctx=typing_info.targetctx, arg_typs=tuple(
            typing_info.typemap[xare__qzb.name] for xare__qzb in args),
            typemap=typing_info.typemap, calltypes=typing_info.calltypes)
    else:
        f_ir = compile_to_numba_ir(func, nsn__ibpqu)
    assert len(f_ir.blocks
        ) == 1, 'only single block functions supported in compile_func_single_block()'
    if run_untyped_pass:
        xtf__xrqlg = tuple(typing_info.typemap[xare__qzb.name] for
            xare__qzb in args)
        gpkpt__agtj = bodo.transforms.untyped_pass.UntypedPass(f_ir,
            typing_info.typingctx, xtf__xrqlg, {}, {}, flags)
        gpkpt__agtj.run()
    pxt__aovs = f_ir.blocks.popitem()[1]
    replace_arg_nodes(pxt__aovs, args)
    ptttd__qjpvs = pxt__aovs.body[:-2]
    update_locs(ptttd__qjpvs[len(args):], loc)
    for stmt in ptttd__qjpvs[:len(args)]:
        stmt.target.loc = loc
    if ret_var is not None:
        bunil__mmr = pxt__aovs.body[-2]
        assert is_assign(bunil__mmr) and is_expr(bunil__mmr.value, 'cast')
        djdlb__gls = bunil__mmr.value.value
        ptttd__qjpvs.append(ir.Assign(djdlb__gls, ret_var, loc))
    return ptttd__qjpvs


def update_locs(node_list, loc):
    for stmt in node_list:
        stmt.loc = loc
        for duby__bgaod in stmt.list_vars():
            duby__bgaod.loc = loc
        if is_assign(stmt):
            stmt.value.loc = loc


def get_stmt_defs(stmt):
    if is_assign(stmt):
        return set([stmt.target.name])
    if type(stmt) in numba.core.analysis.ir_extension_usedefs:
        sybf__oasm = numba.core.analysis.ir_extension_usedefs[type(stmt)]
        lomzd__hff, omkw__rhnob = sybf__oasm(stmt)
        return omkw__rhnob
    return set()


def get_const_value(var, func_ir, err_msg, typemap=None, arg_types=None,
    file_info=None):
    if hasattr(var, 'loc'):
        loc = var.loc
    else:
        loc = None
    try:
        exmp__idcw = get_const_value_inner(func_ir, var, arg_types, typemap,
            file_info=file_info)
        if isinstance(exmp__idcw, ir.UndefinedType):
            yrka__epphx = func_ir.get_definition(var.name).name
            raise BodoError(f"name '{yrka__epphx}' is not defined", loc=loc)
    except GuardException as zrici__wsrm:
        raise BodoError(err_msg, loc=loc)
    return exmp__idcw


def get_const_value_inner(func_ir, var, arg_types=None, typemap=None,
    updated_containers=None, file_info=None, pyobject_to_literal=False,
    literalize_args=True):
    require(isinstance(var, ir.Var))
    ovs__mgiwy = get_definition(func_ir, var)
    ymxw__ablre = None
    if typemap is not None:
        ymxw__ablre = typemap.get(var.name, None)
    if isinstance(ovs__mgiwy, ir.Arg) and arg_types is not None:
        ymxw__ablre = arg_types[ovs__mgiwy.index]
    if updated_containers and var.name in updated_containers:
        raise BodoConstUpdatedError(
            f"variable '{var.name}' is updated inplace using '{updated_containers[var.name]}'"
            )
    if is_literal_type(ymxw__ablre):
        return get_literal_value(ymxw__ablre)
    if isinstance(ovs__mgiwy, (ir.Const, ir.Global, ir.FreeVar)):
        exmp__idcw = ovs__mgiwy.value
        return exmp__idcw
    if literalize_args and isinstance(ovs__mgiwy, ir.Arg
        ) and can_literalize_type(ymxw__ablre, pyobject_to_literal):
        raise numba.core.errors.ForceLiteralArg({ovs__mgiwy.index}, loc=var
            .loc, file_infos={ovs__mgiwy.index: file_info} if file_info is not
            None else None)
    if is_expr(ovs__mgiwy, 'binop'):
        if file_info and ovs__mgiwy.fn == operator.add:
            try:
                kmdpf__aetf = get_const_value_inner(func_ir, ovs__mgiwy.lhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(kmdpf__aetf, True)
                ybmtm__zrv = get_const_value_inner(func_ir, ovs__mgiwy.rhs,
                    arg_types, typemap, updated_containers, file_info)
                return ovs__mgiwy.fn(kmdpf__aetf, ybmtm__zrv)
            except (GuardException, BodoConstUpdatedError) as zrici__wsrm:
                pass
            try:
                ybmtm__zrv = get_const_value_inner(func_ir, ovs__mgiwy.rhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(ybmtm__zrv, False)
                kmdpf__aetf = get_const_value_inner(func_ir, ovs__mgiwy.lhs,
                    arg_types, typemap, updated_containers, file_info)
                return ovs__mgiwy.fn(kmdpf__aetf, ybmtm__zrv)
            except (GuardException, BodoConstUpdatedError) as zrici__wsrm:
                pass
        kmdpf__aetf = get_const_value_inner(func_ir, ovs__mgiwy.lhs,
            arg_types, typemap, updated_containers)
        ybmtm__zrv = get_const_value_inner(func_ir, ovs__mgiwy.rhs,
            arg_types, typemap, updated_containers)
        return ovs__mgiwy.fn(kmdpf__aetf, ybmtm__zrv)
    if is_expr(ovs__mgiwy, 'unary'):
        exmp__idcw = get_const_value_inner(func_ir, ovs__mgiwy.value,
            arg_types, typemap, updated_containers)
        return ovs__mgiwy.fn(exmp__idcw)
    if is_expr(ovs__mgiwy, 'getattr') and typemap:
        tnlwg__yiv = typemap.get(ovs__mgiwy.value.name, None)
        if isinstance(tnlwg__yiv, bodo.hiframes.pd_dataframe_ext.DataFrameType
            ) and ovs__mgiwy.attr == 'columns':
            return pd.Index(tnlwg__yiv.columns)
        if isinstance(tnlwg__yiv, types.SliceType):
            iluz__aem = get_definition(func_ir, ovs__mgiwy.value)
            require(is_call(iluz__aem))
            bpu__hmkz = find_callname(func_ir, iluz__aem)
            dzfnp__wlm = False
            if bpu__hmkz == ('_normalize_slice', 'numba.cpython.unicode'):
                require(ovs__mgiwy.attr in ('start', 'step'))
                iluz__aem = get_definition(func_ir, iluz__aem.args[0])
                dzfnp__wlm = True
            require(find_callname(func_ir, iluz__aem) == ('slice', 'builtins'))
            if len(iluz__aem.args) == 1:
                if ovs__mgiwy.attr == 'start':
                    return 0
                if ovs__mgiwy.attr == 'step':
                    return 1
                require(ovs__mgiwy.attr == 'stop')
                return get_const_value_inner(func_ir, iluz__aem.args[0],
                    arg_types, typemap, updated_containers)
            if ovs__mgiwy.attr == 'start':
                exmp__idcw = get_const_value_inner(func_ir, iluz__aem.args[
                    0], arg_types, typemap, updated_containers)
                if exmp__idcw is None:
                    exmp__idcw = 0
                if dzfnp__wlm:
                    require(exmp__idcw == 0)
                return exmp__idcw
            if ovs__mgiwy.attr == 'stop':
                assert not dzfnp__wlm
                return get_const_value_inner(func_ir, iluz__aem.args[1],
                    arg_types, typemap, updated_containers)
            require(ovs__mgiwy.attr == 'step')
            if len(iluz__aem.args) == 2:
                return 1
            else:
                exmp__idcw = get_const_value_inner(func_ir, iluz__aem.args[
                    2], arg_types, typemap, updated_containers)
                if exmp__idcw is None:
                    exmp__idcw = 1
                if dzfnp__wlm:
                    require(exmp__idcw == 1)
                return exmp__idcw
    if is_expr(ovs__mgiwy, 'getattr'):
        return getattr(get_const_value_inner(func_ir, ovs__mgiwy.value,
            arg_types, typemap, updated_containers), ovs__mgiwy.attr)
    if is_expr(ovs__mgiwy, 'getitem'):
        value = get_const_value_inner(func_ir, ovs__mgiwy.value, arg_types,
            typemap, updated_containers)
        index = get_const_value_inner(func_ir, ovs__mgiwy.index, arg_types,
            typemap, updated_containers)
        return value[index]
    vinoa__fgg = guard(find_callname, func_ir, ovs__mgiwy, typemap)
    if vinoa__fgg is not None and len(vinoa__fgg) == 2 and vinoa__fgg[0
        ] == 'keys' and isinstance(vinoa__fgg[1], ir.Var):
        mud__zxxj = ovs__mgiwy.func
        ovs__mgiwy = get_definition(func_ir, vinoa__fgg[1])
        gidi__oawh = vinoa__fgg[1].name
        if updated_containers and gidi__oawh in updated_containers:
            raise BodoConstUpdatedError(
                "variable '{}' is updated inplace using '{}'".format(
                gidi__oawh, updated_containers[gidi__oawh]))
        require(is_expr(ovs__mgiwy, 'build_map'))
        vals = [duby__bgaod[0] for duby__bgaod in ovs__mgiwy.items]
        iasc__olk = guard(get_definition, func_ir, mud__zxxj)
        assert isinstance(iasc__olk, ir.Expr) and iasc__olk.attr == 'keys'
        iasc__olk.attr = 'copy'
        return [get_const_value_inner(func_ir, duby__bgaod, arg_types,
            typemap, updated_containers) for duby__bgaod in vals]
    if is_expr(ovs__mgiwy, 'build_map'):
        return {get_const_value_inner(func_ir, duby__bgaod[0], arg_types,
            typemap, updated_containers): get_const_value_inner(func_ir,
            duby__bgaod[1], arg_types, typemap, updated_containers) for
            duby__bgaod in ovs__mgiwy.items}
    if is_expr(ovs__mgiwy, 'build_tuple'):
        return tuple(get_const_value_inner(func_ir, duby__bgaod, arg_types,
            typemap, updated_containers) for duby__bgaod in ovs__mgiwy.items)
    if is_expr(ovs__mgiwy, 'build_list'):
        return [get_const_value_inner(func_ir, duby__bgaod, arg_types,
            typemap, updated_containers) for duby__bgaod in ovs__mgiwy.items]
    if is_expr(ovs__mgiwy, 'build_set'):
        return {get_const_value_inner(func_ir, duby__bgaod, arg_types,
            typemap, updated_containers) for duby__bgaod in ovs__mgiwy.items}
    if vinoa__fgg == ('list', 'builtins'):
        values = get_const_value_inner(func_ir, ovs__mgiwy.args[0],
            arg_types, typemap, updated_containers)
        if isinstance(values, set):
            values = sorted(values)
        return list(values)
    if vinoa__fgg == ('set', 'builtins'):
        return set(get_const_value_inner(func_ir, ovs__mgiwy.args[0],
            arg_types, typemap, updated_containers))
    if vinoa__fgg == ('range', 'builtins') and len(ovs__mgiwy.args) == 1:
        return range(get_const_value_inner(func_ir, ovs__mgiwy.args[0],
            arg_types, typemap, updated_containers))
    if vinoa__fgg == ('slice', 'builtins'):
        return slice(*tuple(get_const_value_inner(func_ir, duby__bgaod,
            arg_types, typemap, updated_containers) for duby__bgaod in
            ovs__mgiwy.args))
    if vinoa__fgg == ('str', 'builtins'):
        return str(get_const_value_inner(func_ir, ovs__mgiwy.args[0],
            arg_types, typemap, updated_containers))
    if vinoa__fgg == ('bool', 'builtins'):
        return bool(get_const_value_inner(func_ir, ovs__mgiwy.args[0],
            arg_types, typemap, updated_containers))
    if vinoa__fgg == ('format', 'builtins'):
        xare__qzb = get_const_value_inner(func_ir, ovs__mgiwy.args[0],
            arg_types, typemap, updated_containers)
        nhpg__aut = get_const_value_inner(func_ir, ovs__mgiwy.args[1],
            arg_types, typemap, updated_containers) if len(ovs__mgiwy.args
            ) > 1 else ''
        return format(xare__qzb, nhpg__aut)
    if vinoa__fgg in (('init_binary_str_index',
        'bodo.hiframes.pd_index_ext'), ('init_numeric_index',
        'bodo.hiframes.pd_index_ext'), ('init_categorical_index',
        'bodo.hiframes.pd_index_ext'), ('init_datetime_index',
        'bodo.hiframes.pd_index_ext'), ('init_timedelta_index',
        'bodo.hiframes.pd_index_ext'), ('init_heter_index',
        'bodo.hiframes.pd_index_ext')):
        return pd.Index(get_const_value_inner(func_ir, ovs__mgiwy.args[0],
            arg_types, typemap, updated_containers))
    if vinoa__fgg == ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'):
        return np.array(get_const_value_inner(func_ir, ovs__mgiwy.args[0],
            arg_types, typemap, updated_containers))
    if vinoa__fgg == ('init_range_index', 'bodo.hiframes.pd_index_ext'):
        return pd.RangeIndex(get_const_value_inner(func_ir, ovs__mgiwy.args
            [0], arg_types, typemap, updated_containers),
            get_const_value_inner(func_ir, ovs__mgiwy.args[1], arg_types,
            typemap, updated_containers), get_const_value_inner(func_ir,
            ovs__mgiwy.args[2], arg_types, typemap, updated_containers))
    if vinoa__fgg == ('len', 'builtins') and typemap and isinstance(typemap
        .get(ovs__mgiwy.args[0].name, None), types.BaseTuple):
        return len(typemap[ovs__mgiwy.args[0].name])
    if vinoa__fgg == ('len', 'builtins'):
        mewk__kaxq = guard(get_definition, func_ir, ovs__mgiwy.args[0])
        if isinstance(mewk__kaxq, ir.Expr) and mewk__kaxq.op in ('build_tuple',
            'build_list', 'build_set', 'build_map'):
            return len(mewk__kaxq.items)
        return len(get_const_value_inner(func_ir, ovs__mgiwy.args[0],
            arg_types, typemap, updated_containers))
    if vinoa__fgg == ('CategoricalDtype', 'pandas'):
        kws = dict(ovs__mgiwy.kws)
        zcz__mqe = get_call_expr_arg('CategoricalDtype', ovs__mgiwy.args,
            kws, 0, 'categories', '')
        sakp__wbkp = get_call_expr_arg('CategoricalDtype', ovs__mgiwy.args,
            kws, 1, 'ordered', False)
        if sakp__wbkp is not False:
            sakp__wbkp = get_const_value_inner(func_ir, sakp__wbkp,
                arg_types, typemap, updated_containers)
        if zcz__mqe == '':
            zcz__mqe = None
        else:
            zcz__mqe = get_const_value_inner(func_ir, zcz__mqe, arg_types,
                typemap, updated_containers)
        return pd.CategoricalDtype(zcz__mqe, sakp__wbkp)
    if vinoa__fgg == ('dtype', 'numpy'):
        return np.dtype(get_const_value_inner(func_ir, ovs__mgiwy.args[0],
            arg_types, typemap, updated_containers))
    if vinoa__fgg is not None and len(vinoa__fgg) == 2 and vinoa__fgg[1
        ] == 'pandas' and vinoa__fgg[0] in ('Int8Dtype', 'Int16Dtype',
        'Int32Dtype', 'Int64Dtype', 'UInt8Dtype', 'UInt16Dtype',
        'UInt32Dtype', 'UInt64Dtype'):
        return getattr(pd, vinoa__fgg[0])()
    if vinoa__fgg is not None and len(vinoa__fgg) == 2 and isinstance(
        vinoa__fgg[1], ir.Var):
        exmp__idcw = get_const_value_inner(func_ir, vinoa__fgg[1],
            arg_types, typemap, updated_containers)
        args = [get_const_value_inner(func_ir, duby__bgaod, arg_types,
            typemap, updated_containers) for duby__bgaod in ovs__mgiwy.args]
        kws = {jfbyu__venp[0]: get_const_value_inner(func_ir, jfbyu__venp[1
            ], arg_types, typemap, updated_containers) for jfbyu__venp in
            ovs__mgiwy.kws}
        return getattr(exmp__idcw, vinoa__fgg[0])(*args, **kws)
    if vinoa__fgg is not None and len(vinoa__fgg) == 2 and vinoa__fgg[1
        ] == 'bodo' and vinoa__fgg[0] in bodo_types_with_params:
        args = tuple(get_const_value_inner(func_ir, duby__bgaod, arg_types,
            typemap, updated_containers) for duby__bgaod in ovs__mgiwy.args)
        kwargs = {yrka__epphx: get_const_value_inner(func_ir, duby__bgaod,
            arg_types, typemap, updated_containers) for yrka__epphx,
            duby__bgaod in dict(ovs__mgiwy.kws).items()}
        return getattr(bodo, vinoa__fgg[0])(*args, **kwargs)
    if is_call(ovs__mgiwy) and typemap and isinstance(typemap.get(
        ovs__mgiwy.func.name, None), types.Dispatcher):
        py_func = typemap[ovs__mgiwy.func.name].dispatcher.py_func
        require(ovs__mgiwy.vararg is None)
        args = tuple(get_const_value_inner(func_ir, duby__bgaod, arg_types,
            typemap, updated_containers) for duby__bgaod in ovs__mgiwy.args)
        kwargs = {yrka__epphx: get_const_value_inner(func_ir, duby__bgaod,
            arg_types, typemap, updated_containers) for yrka__epphx,
            duby__bgaod in dict(ovs__mgiwy.kws).items()}
        arg_types = tuple(bodo.typeof(duby__bgaod) for duby__bgaod in args)
        kw_types = {uesn__txtz: bodo.typeof(duby__bgaod) for uesn__txtz,
            duby__bgaod in kwargs.items()}
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
    f_ir, typemap, suatz__yaqhb, suatz__yaqhb = (bodo.compiler.
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
                    min__dva = guard(get_definition, f_ir, rhs.func)
                    if isinstance(min__dva, ir.Const) and isinstance(min__dva
                        .value, numba.core.dispatcher.ObjModeLiftedWith):
                        return False
                    secr__mbhx = guard(find_callname, f_ir, rhs)
                    if secr__mbhx is None:
                        return False
                    func_name, ekyzz__ibbzj = secr__mbhx
                    if ekyzz__ibbzj == 'pandas' and func_name.startswith(
                        'read_'):
                        return False
                    if secr__mbhx in (('fromfile', 'numpy'), ('file_read',
                        'bodo.io.np_io')):
                        return False
                    if secr__mbhx == ('File', 'h5py'):
                        return False
                    if isinstance(ekyzz__ibbzj, ir.Var):
                        ymxw__ablre = typemap[ekyzz__ibbzj.name]
                        if isinstance(ymxw__ablre, (DataFrameType, SeriesType)
                            ) and func_name in ('to_csv', 'to_excel',
                            'to_json', 'to_sql', 'to_pickle', 'to_parquet',
                            'info'):
                            return False
                        if isinstance(ymxw__ablre, types.Array
                            ) and func_name == 'tofile':
                            return False
                        if isinstance(ymxw__ablre, bodo.LoggingLoggerType):
                            return False
                        if str(ymxw__ablre).startswith('Mpl'):
                            return False
                        if (func_name in container_update_method_names and
                            isinstance(guard(get_definition, f_ir,
                            ekyzz__ibbzj), ir.Arg)):
                            return False
                    if ekyzz__ibbzj in ('numpy.random', 'time', 'logging',
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
        vrt__zthjp = func.literal_value.code
        typae__jhyzs = {'np': np, 'pd': pd, 'numba': numba, 'bodo': bodo}
        if hasattr(func.literal_value, 'globals'):
            typae__jhyzs = func.literal_value.globals
        f_ir = numba.core.ir_utils.get_ir_of_code(typae__jhyzs, vrt__zthjp)
        fix_struct_return(f_ir)
        typemap, ohqib__hsbnr, kbal__turnw, suatz__yaqhb = (numba.core.
            typed_passes.type_inference_stage(typing_context,
            target_context, f_ir, arg_types, None))
    elif isinstance(func, bodo.utils.typing.FunctionLiteral):
        py_func = func.literal_value
        f_ir, typemap, kbal__turnw, ohqib__hsbnr = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    elif isinstance(func, CPUDispatcher):
        py_func = func.py_func
        f_ir, typemap, kbal__turnw, ohqib__hsbnr = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    else:
        if not isinstance(func, types.Dispatcher):
            if isinstance(func, types.Function):
                raise BodoError(
                    f'Bodo does not support built-in functions yet, {func}')
            else:
                raise BodoError(f'Function type expected, not {func}')
        py_func = func.dispatcher.py_func
        f_ir, typemap, kbal__turnw, ohqib__hsbnr = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    if is_udf and isinstance(ohqib__hsbnr, types.DictType):
        vcq__ppe = guard(get_struct_keynames, f_ir, typemap)
        if vcq__ppe is not None:
            ohqib__hsbnr = StructType((ohqib__hsbnr.value_type,) * len(
                vcq__ppe), vcq__ppe)
    if is_udf and isinstance(ohqib__hsbnr, (SeriesType,
        HeterogeneousSeriesType)):
        byzy__xhj = numba.core.registry.cpu_target.typing_context
        avd__qayw = numba.core.registry.cpu_target.target_context
        rajq__kcexh = bodo.transforms.series_pass.SeriesPass(f_ir,
            byzy__xhj, avd__qayw, typemap, kbal__turnw, {})
        rajq__kcexh.run()
        rajq__kcexh.run()
        rajq__kcexh.run()
        fxphi__dlt = compute_cfg_from_blocks(f_ir.blocks)
        cdwx__dlsxg = [guard(_get_const_series_info, f_ir.blocks[bxlk__upv],
            f_ir, typemap) for bxlk__upv in fxphi__dlt.exit_points() if
            isinstance(f_ir.blocks[bxlk__upv].body[-1], ir.Return)]
        if None in cdwx__dlsxg or len(pd.Series(cdwx__dlsxg).unique()) != 1:
            ohqib__hsbnr.const_info = None
        else:
            ohqib__hsbnr.const_info = cdwx__dlsxg[0]
    return ohqib__hsbnr


def _get_const_series_info(block, f_ir, typemap):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType
    assert isinstance(block.body[-1], ir.Return)
    trdm__xdm = block.body[-1].value
    tchow__hhi = get_definition(f_ir, trdm__xdm)
    require(is_expr(tchow__hhi, 'cast'))
    tchow__hhi = get_definition(f_ir, tchow__hhi.value)
    require(is_call(tchow__hhi) and find_callname(f_ir, tchow__hhi) == (
        'init_series', 'bodo.hiframes.pd_series_ext'))
    qvw__prufn = tchow__hhi.args[1]
    mxhe__yky = tuple(get_const_value_inner(f_ir, qvw__prufn, typemap=typemap))
    if isinstance(typemap[trdm__xdm.name], HeterogeneousSeriesType):
        return len(typemap[trdm__xdm.name].data), mxhe__yky
    mfwc__wcik = tchow__hhi.args[0]
    yxy__wreq = get_definition(f_ir, mfwc__wcik)
    func_name, jhbpx__alndc = find_callname(f_ir, yxy__wreq)
    if is_call(yxy__wreq) and bodo.utils.utils.is_alloc_callname(func_name,
        jhbpx__alndc):
        nml__wiz = yxy__wreq.args[0]
        frw__skquk = get_const_value_inner(f_ir, nml__wiz, typemap=typemap)
        return frw__skquk, mxhe__yky
    if is_call(yxy__wreq) and find_callname(f_ir, yxy__wreq) in [('asarray',
        'numpy'), ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'), (
        'build_nullable_tuple', 'bodo.libs.nullable_tuple_ext')]:
        mfwc__wcik = yxy__wreq.args[0]
        yxy__wreq = get_definition(f_ir, mfwc__wcik)
    require(is_expr(yxy__wreq, 'build_tuple') or is_expr(yxy__wreq,
        'build_list'))
    return len(yxy__wreq.items), mxhe__yky


def extract_keyvals_from_struct_map(f_ir, build_map, loc, scope, typemap=None):
    oqw__onann = []
    jgon__rze = []
    values = []
    for uesn__txtz, duby__bgaod in build_map.items:
        myy__mmlvw = find_const(f_ir, uesn__txtz)
        require(isinstance(myy__mmlvw, str))
        jgon__rze.append(myy__mmlvw)
        oqw__onann.append(uesn__txtz)
        values.append(duby__bgaod)
    imcmm__fzkny = ir.Var(scope, mk_unique_var('val_tup'), loc)
    kqyb__fwa = ir.Assign(ir.Expr.build_tuple(values, loc), imcmm__fzkny, loc)
    f_ir._definitions[imcmm__fzkny.name] = [kqyb__fwa.value]
    gjgha__kofld = ir.Var(scope, mk_unique_var('key_tup'), loc)
    uwv__tntcp = ir.Assign(ir.Expr.build_tuple(oqw__onann, loc),
        gjgha__kofld, loc)
    f_ir._definitions[gjgha__kofld.name] = [uwv__tntcp.value]
    if typemap is not None:
        typemap[imcmm__fzkny.name] = types.Tuple([typemap[duby__bgaod.name] for
            duby__bgaod in values])
        typemap[gjgha__kofld.name] = types.Tuple([typemap[duby__bgaod.name] for
            duby__bgaod in oqw__onann])
    return jgon__rze, imcmm__fzkny, kqyb__fwa, gjgha__kofld, uwv__tntcp


def _replace_const_map_return(f_ir, block, label):
    require(isinstance(block.body[-1], ir.Return))
    cpd__qhwx = block.body[-1].value
    srw__riipg = guard(get_definition, f_ir, cpd__qhwx)
    require(is_expr(srw__riipg, 'cast'))
    tchow__hhi = guard(get_definition, f_ir, srw__riipg.value)
    require(is_expr(tchow__hhi, 'build_map'))
    require(len(tchow__hhi.items) > 0)
    loc = block.loc
    scope = block.scope
    jgon__rze, imcmm__fzkny, kqyb__fwa, gjgha__kofld, uwv__tntcp = (
        extract_keyvals_from_struct_map(f_ir, tchow__hhi, loc, scope))
    usnd__vpq = ir.Var(scope, mk_unique_var('conv_call'), loc)
    qwnmb__mbrzf = ir.Assign(ir.Global('struct_if_heter_dict', bodo.utils.
        conversion.struct_if_heter_dict, loc), usnd__vpq, loc)
    f_ir._definitions[usnd__vpq.name] = [qwnmb__mbrzf.value]
    etq__bdsgh = ir.Var(scope, mk_unique_var('struct_val'), loc)
    fwd__huhvh = ir.Assign(ir.Expr.call(usnd__vpq, [imcmm__fzkny,
        gjgha__kofld], {}, loc), etq__bdsgh, loc)
    f_ir._definitions[etq__bdsgh.name] = [fwd__huhvh.value]
    srw__riipg.value = etq__bdsgh
    tchow__hhi.items = [(uesn__txtz, uesn__txtz) for uesn__txtz,
        suatz__yaqhb in tchow__hhi.items]
    block.body = block.body[:-2] + [kqyb__fwa, uwv__tntcp, qwnmb__mbrzf,
        fwd__huhvh] + block.body[-2:]
    return tuple(jgon__rze)


def get_struct_keynames(f_ir, typemap):
    fxphi__dlt = compute_cfg_from_blocks(f_ir.blocks)
    pmzti__jpson = list(fxphi__dlt.exit_points())[0]
    block = f_ir.blocks[pmzti__jpson]
    require(isinstance(block.body[-1], ir.Return))
    cpd__qhwx = block.body[-1].value
    srw__riipg = guard(get_definition, f_ir, cpd__qhwx)
    require(is_expr(srw__riipg, 'cast'))
    tchow__hhi = guard(get_definition, f_ir, srw__riipg.value)
    require(is_call(tchow__hhi) and find_callname(f_ir, tchow__hhi) == (
        'struct_if_heter_dict', 'bodo.utils.conversion'))
    return get_overload_const_list(typemap[tchow__hhi.args[1].name])


def fix_struct_return(f_ir):
    gell__rqkxx = None
    fxphi__dlt = compute_cfg_from_blocks(f_ir.blocks)
    for pmzti__jpson in fxphi__dlt.exit_points():
        gell__rqkxx = guard(_replace_const_map_return, f_ir, f_ir.blocks[
            pmzti__jpson], pmzti__jpson)
    return gell__rqkxx


def update_node_list_definitions(node_list, func_ir):
    loc = ir.Loc('', 0)
    uemyo__omyy = ir.Block(ir.Scope(None, loc), loc)
    uemyo__omyy.body = node_list
    build_definitions({(0): uemyo__omyy}, func_ir._definitions)
    return


NESTED_TUP_SENTINEL = '$BODO_NESTED_TUP'


def gen_const_val_str(c):
    if isinstance(c, tuple):
        return "'{}{}', ".format(NESTED_TUP_SENTINEL, len(c)) + ', '.join(
            gen_const_val_str(duby__bgaod) for duby__bgaod in c)
    if isinstance(c, str):
        return "'{}'".format(c)
    if isinstance(c, (pd.Timestamp, pd.Timedelta, float)):
        return "'{}'".format(c)
    return str(c)


def gen_const_tup(vals):
    ktgts__hbxp = ', '.join(gen_const_val_str(c) for c in vals)
    return '({}{})'.format(ktgts__hbxp, ',' if len(vals) == 1 else '')


def get_const_tup_vals(c_typ):
    vals = get_overload_const_list(c_typ)
    return _get_original_nested_tups(vals)


def _get_original_nested_tups(vals):
    for yfwn__wuvyi in range(len(vals) - 1, -1, -1):
        duby__bgaod = vals[yfwn__wuvyi]
        if isinstance(duby__bgaod, str) and duby__bgaod.startswith(
            NESTED_TUP_SENTINEL):
            yckvb__myoj = int(duby__bgaod[len(NESTED_TUP_SENTINEL):])
            return _get_original_nested_tups(tuple(vals[:yfwn__wuvyi]) + (
                tuple(vals[yfwn__wuvyi + 1:yfwn__wuvyi + yckvb__myoj + 1]),
                ) + tuple(vals[yfwn__wuvyi + yckvb__myoj + 1:]))
    return tuple(vals)


def get_call_expr_arg(f_name, args, kws, arg_no, arg_name, default=None,
    err_msg=None, use_default=False):
    xare__qzb = None
    if len(args) > arg_no and arg_no >= 0:
        xare__qzb = args[arg_no]
        if arg_name in kws:
            err_msg = (
                f"{f_name}() got multiple values for argument '{arg_name}'")
            raise BodoError(err_msg)
    elif arg_name in kws:
        xare__qzb = kws[arg_name]
    if xare__qzb is None:
        if use_default or default is not None:
            return default
        if err_msg is None:
            err_msg = "{} requires '{}' argument".format(f_name, arg_name)
        raise BodoError(err_msg)
    return xare__qzb


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
    nsn__ibpqu = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd}
    if extra_globals is not None:
        nsn__ibpqu.update(extra_globals)
    func.__globals__.update(nsn__ibpqu)
    if pysig is not None:
        pre_nodes = [] if pre_nodes is None else pre_nodes
        scope = next(iter(pass_info.func_ir.blocks.values())).scope
        loc = scope.loc

        def normal_handler(index, param, default):
            return default

        def default_handler(index, param, default):
            ydoi__rrl = ir.Var(scope, mk_unique_var('defaults'), loc)
            try:
                pass_info.typemap[ydoi__rrl.name] = types.literal(default)
            except:
                pass_info.typemap[ydoi__rrl.name] = numba.typeof(default)
            cfqzw__ypj = ir.Assign(ir.Const(default, loc), ydoi__rrl, loc)
            pre_nodes.append(cfqzw__ypj)
            return ydoi__rrl
        args = numba.core.typing.fold_arguments(pysig, args, kws,
            normal_handler, default_handler, normal_handler)
    xtf__xrqlg = tuple(pass_info.typemap[duby__bgaod.name] for duby__bgaod in
        args)
    if const:
        sdrlz__hppgd = []
        for yfwn__wuvyi, xare__qzb in enumerate(args):
            exmp__idcw = guard(find_const, pass_info.func_ir, xare__qzb)
            if exmp__idcw:
                sdrlz__hppgd.append(types.literal(exmp__idcw))
            else:
                sdrlz__hppgd.append(xtf__xrqlg[yfwn__wuvyi])
        xtf__xrqlg = tuple(sdrlz__hppgd)
    return ReplaceFunc(func, xtf__xrqlg, args, nsn__ibpqu,
        inline_bodo_calls, run_full_pipeline, pre_nodes)


def is_var_size_item_array_type(t):
    assert is_array_typ(t, False)
    return t == string_array_type or isinstance(t, ArrayItemArrayType
        ) or isinstance(t, StructArrayType) and any(
        is_var_size_item_array_type(hymq__suplg) for hymq__suplg in t.data)


def gen_init_varsize_alloc_sizes(t):
    if t == string_array_type:
        kbid__jlpdk = 'num_chars_{}'.format(ir_utils.next_label())
        return f'  {kbid__jlpdk} = 0\n', (kbid__jlpdk,)
    if isinstance(t, ArrayItemArrayType):
        qgw__xbhft, qip__akq = gen_init_varsize_alloc_sizes(t.dtype)
        kbid__jlpdk = 'num_items_{}'.format(ir_utils.next_label())
        return f'  {kbid__jlpdk} = 0\n' + qgw__xbhft, (kbid__jlpdk,) + qip__akq
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
        return 1 + sum(get_type_alloc_counts(hymq__suplg.dtype) for
            hymq__suplg in t.data)
    if isinstance(t, ArrayItemArrayType) or t == string_array_type:
        return 1 + get_type_alloc_counts(t.dtype)
    if isinstance(t, MapArrayType):
        return get_type_alloc_counts(t.key_arr_type) + get_type_alloc_counts(t
            .value_arr_type)
    if bodo.utils.utils.is_array_typ(t, False) or t == bodo.string_type:
        return 1
    if isinstance(t, StructType):
        return sum(get_type_alloc_counts(hymq__suplg) for hymq__suplg in t.data
            )
    if isinstance(t, types.BaseTuple):
        return sum(get_type_alloc_counts(hymq__suplg) for hymq__suplg in t.
            types)
    return 0


def find_udf_str_name(obj_dtype, func_name, typing_context, caller_name):
    mdput__qek = typing_context.resolve_getattr(obj_dtype, func_name)
    if mdput__qek is None:
        kwdq__ahari = types.misc.Module(np)
        try:
            mdput__qek = typing_context.resolve_getattr(kwdq__ahari, func_name)
        except AttributeError as zrici__wsrm:
            mdput__qek = None
        if mdput__qek is None:
            raise BodoError(
                f"{caller_name}(): No Pandas method or Numpy function found with the name '{func_name}'."
                )
    return mdput__qek


def get_udf_str_return_type(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    mdput__qek = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(mdput__qek, types.BoundFunction):
        if axis is not None:
            flxuo__oaeck = mdput__qek.get_call_type(typing_context, (), {
                'axis': axis})
        else:
            flxuo__oaeck = mdput__qek.get_call_type(typing_context, (), {})
        return flxuo__oaeck.return_type
    else:
        if bodo.utils.typing.is_numpy_ufunc(mdput__qek):
            flxuo__oaeck = mdput__qek.get_call_type(typing_context, (
                obj_dtype,), {})
            return flxuo__oaeck.return_type
        raise BodoError(
            f"{caller_name}(): Only Pandas methods and np.ufunc are supported as string literals. '{func_name}' not supported."
            )


def get_pandas_method_str_impl(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    mdput__qek = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(mdput__qek, types.BoundFunction):
        duklb__iqef = mdput__qek.template
        if axis is not None:
            return duklb__iqef._overload_func(obj_dtype, axis=axis)
        else:
            return duklb__iqef._overload_func(obj_dtype)
    return None


def dict_to_const_keys_var_values_lists(dict_var, func_ir, arg_types,
    typemap, updated_containers, require_const_map, label):
    require(isinstance(dict_var, ir.Var))
    kqm__iuk = get_definition(func_ir, dict_var)
    require(isinstance(kqm__iuk, ir.Expr))
    require(kqm__iuk.op == 'build_map')
    pglp__qgcox = kqm__iuk.items
    oqw__onann = []
    values = []
    kprwb__ybp = False
    for yfwn__wuvyi in range(len(pglp__qgcox)):
        tuuqv__oyem, value = pglp__qgcox[yfwn__wuvyi]
        try:
            ikdh__fcobm = get_const_value_inner(func_ir, tuuqv__oyem,
                arg_types, typemap, updated_containers)
            oqw__onann.append(ikdh__fcobm)
            values.append(value)
        except GuardException as zrici__wsrm:
            require_const_map[tuuqv__oyem] = label
            kprwb__ybp = True
    if kprwb__ybp:
        raise GuardException
    return oqw__onann, values


def _get_const_keys_from_dict(args, func_ir, build_map, err_msg, loc):
    try:
        oqw__onann = tuple(get_const_value_inner(func_ir, t[0], args) for t in
            build_map.items)
    except GuardException as zrici__wsrm:
        raise BodoError(err_msg, loc)
    if not all(isinstance(c, (str, int)) for c in oqw__onann):
        raise BodoError(err_msg, loc)
    return oqw__onann


def _convert_const_key_dict(args, func_ir, build_map, err_msg, scope, loc,
    output_sentinel_tuple=False):
    oqw__onann = _get_const_keys_from_dict(args, func_ir, build_map,
        err_msg, loc)
    zzo__rcnr = []
    prm__yrlod = [bodo.transforms.typing_pass._create_const_var(uesn__txtz,
        'dict_key', scope, loc, zzo__rcnr) for uesn__txtz in oqw__onann]
    owm__wmhd = [t[1] for t in build_map.items]
    if output_sentinel_tuple:
        ynv__ydudg = ir.Var(scope, mk_unique_var('sentinel'), loc)
        iqdfh__icepz = ir.Var(scope, mk_unique_var('dict_tup'), loc)
        zzo__rcnr.append(ir.Assign(ir.Const('__bodo_tup', loc), ynv__ydudg,
            loc))
        ouzu__zdwtm = [ynv__ydudg] + prm__yrlod + owm__wmhd
        zzo__rcnr.append(ir.Assign(ir.Expr.build_tuple(ouzu__zdwtm, loc),
            iqdfh__icepz, loc))
        return (iqdfh__icepz,), zzo__rcnr
    else:
        mtapo__vqefo = ir.Var(scope, mk_unique_var('values_tup'), loc)
        ijg__bddrj = ir.Var(scope, mk_unique_var('idx_tup'), loc)
        zzo__rcnr.append(ir.Assign(ir.Expr.build_tuple(owm__wmhd, loc),
            mtapo__vqefo, loc))
        zzo__rcnr.append(ir.Assign(ir.Expr.build_tuple(prm__yrlod, loc),
            ijg__bddrj, loc))
        return (mtapo__vqefo, ijg__bddrj), zzo__rcnr
