"""File containing utility functions for supporting DataFrame operations with Table Format."""
import numba
import numpy as np
from numba.core import types
import bodo
from bodo.hiframes.table import TableType
from bodo.utils.typing import get_overload_const_bool, get_overload_const_str, is_overload_constant_bool, is_overload_constant_str, is_overload_none, raise_bodo_error


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def generate_mappable_table_func(table, func_name, out_arr_typ, is_method,
    used_cols=None):
    if not is_overload_constant_str(func_name) and not is_overload_none(
        func_name):
        raise_bodo_error(
            'generate_mappable_table_func(): func_name must be a constant string'
            )
    if not is_overload_constant_bool(is_method):
        raise_bodo_error(
            'generate_mappable_table_func(): is_method must be a constant boolean'
            )
    ubdz__yajn = not is_overload_none(func_name)
    if ubdz__yajn:
        func_name = get_overload_const_str(func_name)
        tpmz__jcx = get_overload_const_bool(is_method)
    ovcz__lmlou = out_arr_typ.instance_type if isinstance(out_arr_typ,
        types.TypeRef) else out_arr_typ
    xfee__zfi = ovcz__lmlou == types.none
    ydwqg__zsm = len(table.arr_types)
    if xfee__zfi:
        uvarl__tks = table
    else:
        uwnj__rseh = tuple([ovcz__lmlou] * ydwqg__zsm)
        uvarl__tks = TableType(uwnj__rseh)
    ngbcb__nmlmo = {'bodo': bodo, 'lst_dtype': ovcz__lmlou, 'table_typ':
        uvarl__tks}
    dqfdm__wmijv = (
        'def impl(table, func_name, out_arr_typ, is_method, used_cols=None):\n'
        )
    if xfee__zfi:
        dqfdm__wmijv += (
            f'  out_table = bodo.hiframes.table.init_table(table, False)\n')
        dqfdm__wmijv += f'  l = len(table)\n'
    else:
        dqfdm__wmijv += f"""  out_list = bodo.hiframes.table.alloc_empty_list_type({ydwqg__zsm}, lst_dtype)
"""
    if not is_overload_none(used_cols):
        dqfdm__wmijv += f'  used_cols_set = set(used_cols)\n'
    else:
        dqfdm__wmijv += f'  used_cols_set = used_cols\n'
    dqfdm__wmijv += (
        f'  bodo.hiframes.table.ensure_table_unboxed(table, used_cols_set)\n')
    for lgrz__tsxrt in table.type_to_blk.values():
        dqfdm__wmijv += f"""  blk_{lgrz__tsxrt} = bodo.hiframes.table.get_table_block(table, {lgrz__tsxrt})
"""
        ngbcb__nmlmo[f'col_indices_{lgrz__tsxrt}'] = np.array(table.
            block_to_arr_ind[lgrz__tsxrt], dtype=np.int64)
        if xfee__zfi:
            dqfdm__wmijv += f"""  out_list_{lgrz__tsxrt} = bodo.hiframes.table.alloc_list_like(blk_{lgrz__tsxrt}, False)
"""
        dqfdm__wmijv += f'  for i in range(len(blk_{lgrz__tsxrt})):\n'
        dqfdm__wmijv += f'    col_loc = col_indices_{lgrz__tsxrt}[i]\n'
        if not is_overload_none(used_cols):
            dqfdm__wmijv += f'    if col_loc not in used_cols_set:\n'
            dqfdm__wmijv += f'        continue\n'
        if xfee__zfi:
            sjprf__nnvdj = 'i'
            nlkc__dzby = f'out_list_{lgrz__tsxrt}'
        else:
            sjprf__nnvdj = 'col_loc'
            nlkc__dzby = 'out_list'
        if not ubdz__yajn:
            dqfdm__wmijv += (
                f'    {nlkc__dzby}[{sjprf__nnvdj}] = blk_{lgrz__tsxrt}[i]\n')
        elif tpmz__jcx:
            dqfdm__wmijv += f"""    {nlkc__dzby}[{sjprf__nnvdj}] = blk_{lgrz__tsxrt}[i].{func_name}()
"""
        else:
            dqfdm__wmijv += f"""    {nlkc__dzby}[{sjprf__nnvdj}] = {func_name}(blk_{lgrz__tsxrt}[i])
"""
        if xfee__zfi:
            dqfdm__wmijv += f"""  out_table = bodo.hiframes.table.set_table_block(out_table, {nlkc__dzby}, {lgrz__tsxrt})
"""
    if xfee__zfi:
        dqfdm__wmijv += (
            f'  out_table = bodo.hiframes.table.set_table_len(out_table, l)\n')
        dqfdm__wmijv += '  return out_table'
    else:
        dqfdm__wmijv += (
            '  return bodo.hiframes.table.init_table_from_lists((out_list,), table_typ)'
            )
    cwg__rea = {}
    exec(dqfdm__wmijv, ngbcb__nmlmo, cwg__rea)
    return cwg__rea['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def generate_table_nbytes(table, out_arr, start_offset, parallel=False):
    ngbcb__nmlmo = {'bodo': bodo, 'sum_op': np.int32(bodo.libs.
        distributed_api.Reduce_Type.Sum.value)}
    dqfdm__wmijv = 'def impl(table, out_arr, start_offset, parallel=False):\n'
    dqfdm__wmijv += '  bodo.hiframes.table.ensure_table_unboxed(table, None)\n'
    for lgrz__tsxrt in table.type_to_blk.values():
        dqfdm__wmijv += (
            f'  blk = bodo.hiframes.table.get_table_block(table, {lgrz__tsxrt})\n'
            )
        ngbcb__nmlmo[f'col_indices_{lgrz__tsxrt}'] = np.array(table.
            block_to_arr_ind[lgrz__tsxrt], dtype=np.int64)
        dqfdm__wmijv += '  for i in range(len(blk)):\n'
        dqfdm__wmijv += f'    col_loc = col_indices_{lgrz__tsxrt}[i]\n'
        dqfdm__wmijv += '    out_arr[col_loc + start_offset] = blk[i].nbytes\n'
    dqfdm__wmijv += '  if parallel:\n'
    dqfdm__wmijv += '    for i in range(start_offset, len(out_arr)):\n'
    dqfdm__wmijv += """      out_arr[i] = bodo.libs.distributed_api.dist_reduce(out_arr[i], sum_op)
"""
    cwg__rea = {}
    exec(dqfdm__wmijv, ngbcb__nmlmo, cwg__rea)
    return cwg__rea['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_concat(table, col_nums, arr_type):
    arr_type = arr_type.instance_type if isinstance(arr_type, types.TypeRef
        ) else arr_type
    dygj__dfb = table.type_to_blk[arr_type]
    ngbcb__nmlmo = {'bodo': bodo}
    ngbcb__nmlmo['col_indices'] = np.array(table.block_to_arr_ind[dygj__dfb
        ], dtype=np.int64)
    dqfdm__wmijv = 'def impl(table, col_nums, arr_type):\n'
    dqfdm__wmijv += (
        f'  blk = bodo.hiframes.table.get_table_block(table, {dygj__dfb})\n')
    dqfdm__wmijv += (
        '  col_num_to_ind_in_blk = {c : i for i, c in enumerate(col_indices)}\n'
        )
    dqfdm__wmijv += '  n = len(table)\n'
    ntw__vnak = bodo.utils.typing.is_str_arr_type(arr_type)
    if ntw__vnak:
        dqfdm__wmijv += '  total_chars = 0\n'
        dqfdm__wmijv += '  for c in col_nums:\n'
        dqfdm__wmijv += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
        dqfdm__wmijv += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
        dqfdm__wmijv += (
            '    total_chars += bodo.libs.str_arr_ext.num_total_chars(arr)\n')
        dqfdm__wmijv += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n * len(col_nums), total_chars)
"""
    else:
        dqfdm__wmijv += """  out_arr = bodo.utils.utils.alloc_type(n * len(col_nums), arr_type, (-1,))
"""
    dqfdm__wmijv += '  for i in range(len(col_nums)):\n'
    dqfdm__wmijv += '    c = col_nums[i]\n'
    if not ntw__vnak:
        dqfdm__wmijv += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
    dqfdm__wmijv += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
    dqfdm__wmijv += '    off = i * n\n'
    dqfdm__wmijv += '    for j in range(len(arr)):\n'
    dqfdm__wmijv += '      if bodo.libs.array_kernels.isna(arr, j):\n'
    dqfdm__wmijv += '        bodo.libs.array_kernels.setna(out_arr, off+j)\n'
    dqfdm__wmijv += '      else:\n'
    dqfdm__wmijv += '        out_arr[off+j] = arr[j]\n'
    dqfdm__wmijv += '  return out_arr\n'
    emxw__xvqnn = {}
    exec(dqfdm__wmijv, ngbcb__nmlmo, emxw__xvqnn)
    tbumu__bssn = emxw__xvqnn['impl']
    return tbumu__bssn
