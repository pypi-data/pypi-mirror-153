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
    rxkh__cvo = not is_overload_none(func_name)
    if rxkh__cvo:
        func_name = get_overload_const_str(func_name)
        jql__omdss = get_overload_const_bool(is_method)
    stllv__unzvu = out_arr_typ.instance_type if isinstance(out_arr_typ,
        types.TypeRef) else out_arr_typ
    lfp__ucaq = stllv__unzvu == types.none
    pul__syaw = len(table.arr_types)
    if lfp__ucaq:
        eain__kdnty = table
    else:
        jgyq__xlqrt = tuple([stllv__unzvu] * pul__syaw)
        eain__kdnty = TableType(jgyq__xlqrt)
    npwf__vrrjd = {'bodo': bodo, 'lst_dtype': stllv__unzvu, 'table_typ':
        eain__kdnty}
    hccg__ter = (
        'def impl(table, func_name, out_arr_typ, is_method, used_cols=None):\n'
        )
    if lfp__ucaq:
        hccg__ter += (
            f'  out_table = bodo.hiframes.table.init_table(table, False)\n')
        hccg__ter += f'  l = len(table)\n'
    else:
        hccg__ter += f"""  out_list = bodo.hiframes.table.alloc_empty_list_type({pul__syaw}, lst_dtype)
"""
    if not is_overload_none(used_cols):
        hccg__ter += f'  used_cols_set = set(used_cols)\n'
    else:
        hccg__ter += f'  used_cols_set = used_cols\n'
    hccg__ter += (
        f'  bodo.hiframes.table.ensure_table_unboxed(table, used_cols_set)\n')
    for jgpe__xme in table.type_to_blk.values():
        hccg__ter += f"""  blk_{jgpe__xme} = bodo.hiframes.table.get_table_block(table, {jgpe__xme})
"""
        npwf__vrrjd[f'col_indices_{jgpe__xme}'] = np.array(table.
            block_to_arr_ind[jgpe__xme], dtype=np.int64)
        if lfp__ucaq:
            hccg__ter += f"""  out_list_{jgpe__xme} = bodo.hiframes.table.alloc_list_like(blk_{jgpe__xme}, False)
"""
        hccg__ter += f'  for i in range(len(blk_{jgpe__xme})):\n'
        hccg__ter += f'    col_loc = col_indices_{jgpe__xme}[i]\n'
        if not is_overload_none(used_cols):
            hccg__ter += f'    if col_loc not in used_cols_set:\n'
            hccg__ter += f'        continue\n'
        if lfp__ucaq:
            qxowz__xen = 'i'
            upx__jvdm = f'out_list_{jgpe__xme}'
        else:
            qxowz__xen = 'col_loc'
            upx__jvdm = 'out_list'
        if not rxkh__cvo:
            hccg__ter += (
                f'    {upx__jvdm}[{qxowz__xen}] = blk_{jgpe__xme}[i]\n')
        elif jql__omdss:
            hccg__ter += (
                f'    {upx__jvdm}[{qxowz__xen}] = blk_{jgpe__xme}[i].{func_name}()\n'
                )
        else:
            hccg__ter += (
                f'    {upx__jvdm}[{qxowz__xen}] = {func_name}(blk_{jgpe__xme}[i])\n'
                )
        if lfp__ucaq:
            hccg__ter += f"""  out_table = bodo.hiframes.table.set_table_block(out_table, {upx__jvdm}, {jgpe__xme})
"""
    if lfp__ucaq:
        hccg__ter += (
            f'  out_table = bodo.hiframes.table.set_table_len(out_table, l)\n')
        hccg__ter += '  return out_table'
    else:
        hccg__ter += (
            '  return bodo.hiframes.table.init_table_from_lists((out_list,), table_typ)'
            )
    dyn__wbhfw = {}
    exec(hccg__ter, npwf__vrrjd, dyn__wbhfw)
    return dyn__wbhfw['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def generate_table_nbytes(table, out_arr, start_offset, parallel=False):
    npwf__vrrjd = {'bodo': bodo, 'sum_op': np.int32(bodo.libs.
        distributed_api.Reduce_Type.Sum.value)}
    hccg__ter = 'def impl(table, out_arr, start_offset, parallel=False):\n'
    hccg__ter += '  bodo.hiframes.table.ensure_table_unboxed(table, None)\n'
    for jgpe__xme in table.type_to_blk.values():
        hccg__ter += (
            f'  blk = bodo.hiframes.table.get_table_block(table, {jgpe__xme})\n'
            )
        npwf__vrrjd[f'col_indices_{jgpe__xme}'] = np.array(table.
            block_to_arr_ind[jgpe__xme], dtype=np.int64)
        hccg__ter += '  for i in range(len(blk)):\n'
        hccg__ter += f'    col_loc = col_indices_{jgpe__xme}[i]\n'
        hccg__ter += '    out_arr[col_loc + start_offset] = blk[i].nbytes\n'
    hccg__ter += '  if parallel:\n'
    hccg__ter += '    for i in range(start_offset, len(out_arr)):\n'
    hccg__ter += (
        '      out_arr[i] = bodo.libs.distributed_api.dist_reduce(out_arr[i], sum_op)\n'
        )
    dyn__wbhfw = {}
    exec(hccg__ter, npwf__vrrjd, dyn__wbhfw)
    return dyn__wbhfw['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_concat(table, col_nums, arr_type):
    arr_type = arr_type.instance_type if isinstance(arr_type, types.TypeRef
        ) else arr_type
    gev__fiqhb = table.type_to_blk[arr_type]
    npwf__vrrjd = {'bodo': bodo}
    npwf__vrrjd['col_indices'] = np.array(table.block_to_arr_ind[gev__fiqhb
        ], dtype=np.int64)
    hccg__ter = 'def impl(table, col_nums, arr_type):\n'
    hccg__ter += (
        f'  blk = bodo.hiframes.table.get_table_block(table, {gev__fiqhb})\n')
    hccg__ter += (
        '  col_num_to_ind_in_blk = {c : i for i, c in enumerate(col_indices)}\n'
        )
    hccg__ter += '  n = len(table)\n'
    mki__vvts = bodo.utils.typing.is_str_arr_type(arr_type)
    if mki__vvts:
        hccg__ter += '  total_chars = 0\n'
        hccg__ter += '  for c in col_nums:\n'
        hccg__ter += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
        hccg__ter += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
        hccg__ter += (
            '    total_chars += bodo.libs.str_arr_ext.num_total_chars(arr)\n')
        hccg__ter += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n * len(col_nums), total_chars)
"""
    else:
        hccg__ter += """  out_arr = bodo.utils.utils.alloc_type(n * len(col_nums), arr_type, (-1,))
"""
    hccg__ter += '  for i in range(len(col_nums)):\n'
    hccg__ter += '    c = col_nums[i]\n'
    if not mki__vvts:
        hccg__ter += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
    hccg__ter += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
    hccg__ter += '    off = i * n\n'
    hccg__ter += '    for j in range(len(arr)):\n'
    hccg__ter += '      if bodo.libs.array_kernels.isna(arr, j):\n'
    hccg__ter += '        bodo.libs.array_kernels.setna(out_arr, off+j)\n'
    hccg__ter += '      else:\n'
    hccg__ter += '        out_arr[off+j] = arr[j]\n'
    hccg__ter += '  return out_arr\n'
    uwz__mhj = {}
    exec(hccg__ter, npwf__vrrjd, uwz__mhj)
    qmspd__rfksa = uwz__mhj['impl']
    return qmspd__rfksa
