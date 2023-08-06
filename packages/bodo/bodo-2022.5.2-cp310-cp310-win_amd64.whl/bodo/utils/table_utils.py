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
    udi__zgee = not is_overload_none(func_name)
    if udi__zgee:
        func_name = get_overload_const_str(func_name)
        xvkn__edt = get_overload_const_bool(is_method)
    wpz__zss = out_arr_typ.instance_type if isinstance(out_arr_typ, types.
        TypeRef) else out_arr_typ
    ydqmw__ualbg = wpz__zss == types.none
    ejf__zfgrc = len(table.arr_types)
    if ydqmw__ualbg:
        soud__oxcbw = table
    else:
        glno__gek = tuple([wpz__zss] * ejf__zfgrc)
        soud__oxcbw = TableType(glno__gek)
    yzi__qnke = {'bodo': bodo, 'lst_dtype': wpz__zss, 'table_typ': soud__oxcbw}
    duk__pyfdm = (
        'def impl(table, func_name, out_arr_typ, is_method, used_cols=None):\n'
        )
    if ydqmw__ualbg:
        duk__pyfdm += (
            f'  out_table = bodo.hiframes.table.init_table(table, False)\n')
        duk__pyfdm += f'  l = len(table)\n'
    else:
        duk__pyfdm += f"""  out_list = bodo.hiframes.table.alloc_empty_list_type({ejf__zfgrc}, lst_dtype)
"""
    if not is_overload_none(used_cols):
        duk__pyfdm += f'  used_cols_set = set(used_cols)\n'
    else:
        duk__pyfdm += f'  used_cols_set = used_cols\n'
    duk__pyfdm += (
        f'  bodo.hiframes.table.ensure_table_unboxed(table, used_cols_set)\n')
    for vwe__tfqqg in table.type_to_blk.values():
        duk__pyfdm += f"""  blk_{vwe__tfqqg} = bodo.hiframes.table.get_table_block(table, {vwe__tfqqg})
"""
        yzi__qnke[f'col_indices_{vwe__tfqqg}'] = np.array(table.
            block_to_arr_ind[vwe__tfqqg], dtype=np.int64)
        if ydqmw__ualbg:
            duk__pyfdm += f"""  out_list_{vwe__tfqqg} = bodo.hiframes.table.alloc_list_like(blk_{vwe__tfqqg}, False)
"""
        duk__pyfdm += f'  for i in range(len(blk_{vwe__tfqqg})):\n'
        duk__pyfdm += f'    col_loc = col_indices_{vwe__tfqqg}[i]\n'
        if not is_overload_none(used_cols):
            duk__pyfdm += f'    if col_loc not in used_cols_set:\n'
            duk__pyfdm += f'        continue\n'
        if ydqmw__ualbg:
            lrsw__frav = 'i'
            xtwe__cejdt = f'out_list_{vwe__tfqqg}'
        else:
            lrsw__frav = 'col_loc'
            xtwe__cejdt = 'out_list'
        if not udi__zgee:
            duk__pyfdm += (
                f'    {xtwe__cejdt}[{lrsw__frav}] = blk_{vwe__tfqqg}[i]\n')
        elif xvkn__edt:
            duk__pyfdm += (
                f'    {xtwe__cejdt}[{lrsw__frav}] = blk_{vwe__tfqqg}[i].{func_name}()\n'
                )
        else:
            duk__pyfdm += (
                f'    {xtwe__cejdt}[{lrsw__frav}] = {func_name}(blk_{vwe__tfqqg}[i])\n'
                )
        if ydqmw__ualbg:
            duk__pyfdm += f"""  out_table = bodo.hiframes.table.set_table_block(out_table, {xtwe__cejdt}, {vwe__tfqqg})
"""
    if ydqmw__ualbg:
        duk__pyfdm += (
            f'  out_table = bodo.hiframes.table.set_table_len(out_table, l)\n')
        duk__pyfdm += '  return out_table'
    else:
        duk__pyfdm += (
            '  return bodo.hiframes.table.init_table_from_lists((out_list,), table_typ)'
            )
    hxjk__azs = {}
    exec(duk__pyfdm, yzi__qnke, hxjk__azs)
    return hxjk__azs['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def generate_table_nbytes(table, out_arr, start_offset, parallel=False):
    yzi__qnke = {'bodo': bodo, 'sum_op': np.int32(bodo.libs.distributed_api
        .Reduce_Type.Sum.value)}
    duk__pyfdm = 'def impl(table, out_arr, start_offset, parallel=False):\n'
    duk__pyfdm += '  bodo.hiframes.table.ensure_table_unboxed(table, None)\n'
    for vwe__tfqqg in table.type_to_blk.values():
        duk__pyfdm += (
            f'  blk = bodo.hiframes.table.get_table_block(table, {vwe__tfqqg})\n'
            )
        yzi__qnke[f'col_indices_{vwe__tfqqg}'] = np.array(table.
            block_to_arr_ind[vwe__tfqqg], dtype=np.int64)
        duk__pyfdm += '  for i in range(len(blk)):\n'
        duk__pyfdm += f'    col_loc = col_indices_{vwe__tfqqg}[i]\n'
        duk__pyfdm += '    out_arr[col_loc + start_offset] = blk[i].nbytes\n'
    duk__pyfdm += '  if parallel:\n'
    duk__pyfdm += '    for i in range(start_offset, len(out_arr)):\n'
    duk__pyfdm += (
        '      out_arr[i] = bodo.libs.distributed_api.dist_reduce(out_arr[i], sum_op)\n'
        )
    hxjk__azs = {}
    exec(duk__pyfdm, yzi__qnke, hxjk__azs)
    return hxjk__azs['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_concat(table, col_nums, arr_type):
    arr_type = arr_type.instance_type if isinstance(arr_type, types.TypeRef
        ) else arr_type
    eoum__gxrsy = table.type_to_blk[arr_type]
    yzi__qnke = {'bodo': bodo}
    yzi__qnke['col_indices'] = np.array(table.block_to_arr_ind[eoum__gxrsy],
        dtype=np.int64)
    duk__pyfdm = 'def impl(table, col_nums, arr_type):\n'
    duk__pyfdm += (
        f'  blk = bodo.hiframes.table.get_table_block(table, {eoum__gxrsy})\n')
    duk__pyfdm += (
        '  col_num_to_ind_in_blk = {c : i for i, c in enumerate(col_indices)}\n'
        )
    duk__pyfdm += '  n = len(table)\n'
    crsi__dxta = bodo.utils.typing.is_str_arr_type(arr_type)
    if crsi__dxta:
        duk__pyfdm += '  total_chars = 0\n'
        duk__pyfdm += '  for c in col_nums:\n'
        duk__pyfdm += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
        duk__pyfdm += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
        duk__pyfdm += (
            '    total_chars += bodo.libs.str_arr_ext.num_total_chars(arr)\n')
        duk__pyfdm += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n * len(col_nums), total_chars)
"""
    else:
        duk__pyfdm += """  out_arr = bodo.utils.utils.alloc_type(n * len(col_nums), arr_type, (-1,))
"""
    duk__pyfdm += '  for i in range(len(col_nums)):\n'
    duk__pyfdm += '    c = col_nums[i]\n'
    if not crsi__dxta:
        duk__pyfdm += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
    duk__pyfdm += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
    duk__pyfdm += '    off = i * n\n'
    duk__pyfdm += '    for j in range(len(arr)):\n'
    duk__pyfdm += '      if bodo.libs.array_kernels.isna(arr, j):\n'
    duk__pyfdm += '        bodo.libs.array_kernels.setna(out_arr, off+j)\n'
    duk__pyfdm += '      else:\n'
    duk__pyfdm += '        out_arr[off+j] = arr[j]\n'
    duk__pyfdm += '  return out_arr\n'
    tjle__qwe = {}
    exec(duk__pyfdm, yzi__qnke, tjle__qwe)
    ogpk__uile = tjle__qwe['impl']
    return ogpk__uile
