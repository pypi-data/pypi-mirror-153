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
    uzk__akdh = not is_overload_none(func_name)
    if uzk__akdh:
        func_name = get_overload_const_str(func_name)
        zckn__ejh = get_overload_const_bool(is_method)
    xsoqc__xooif = out_arr_typ.instance_type if isinstance(out_arr_typ,
        types.TypeRef) else out_arr_typ
    opz__ahd = xsoqc__xooif == types.none
    vgvzh__tctb = len(table.arr_types)
    if opz__ahd:
        gsb__rhks = table
    else:
        oby__fsk = tuple([xsoqc__xooif] * vgvzh__tctb)
        gsb__rhks = TableType(oby__fsk)
    xyim__wlfnf = {'bodo': bodo, 'lst_dtype': xsoqc__xooif, 'table_typ':
        gsb__rhks}
    gme__gluqb = (
        'def impl(table, func_name, out_arr_typ, is_method, used_cols=None):\n'
        )
    if opz__ahd:
        gme__gluqb += (
            f'  out_table = bodo.hiframes.table.init_table(table, False)\n')
        gme__gluqb += f'  l = len(table)\n'
    else:
        gme__gluqb += f"""  out_list = bodo.hiframes.table.alloc_empty_list_type({vgvzh__tctb}, lst_dtype)
"""
    if not is_overload_none(used_cols):
        gme__gluqb += f'  used_cols_set = set(used_cols)\n'
    else:
        gme__gluqb += f'  used_cols_set = used_cols\n'
    gme__gluqb += (
        f'  bodo.hiframes.table.ensure_table_unboxed(table, used_cols_set)\n')
    for kxax__qae in table.type_to_blk.values():
        gme__gluqb += f"""  blk_{kxax__qae} = bodo.hiframes.table.get_table_block(table, {kxax__qae})
"""
        xyim__wlfnf[f'col_indices_{kxax__qae}'] = np.array(table.
            block_to_arr_ind[kxax__qae], dtype=np.int64)
        if opz__ahd:
            gme__gluqb += f"""  out_list_{kxax__qae} = bodo.hiframes.table.alloc_list_like(blk_{kxax__qae}, False)
"""
        gme__gluqb += f'  for i in range(len(blk_{kxax__qae})):\n'
        gme__gluqb += f'    col_loc = col_indices_{kxax__qae}[i]\n'
        if not is_overload_none(used_cols):
            gme__gluqb += f'    if col_loc not in used_cols_set:\n'
            gme__gluqb += f'        continue\n'
        if opz__ahd:
            wgwm__bmf = 'i'
            moa__ldfo = f'out_list_{kxax__qae}'
        else:
            wgwm__bmf = 'col_loc'
            moa__ldfo = 'out_list'
        if not uzk__akdh:
            gme__gluqb += (
                f'    {moa__ldfo}[{wgwm__bmf}] = blk_{kxax__qae}[i]\n')
        elif zckn__ejh:
            gme__gluqb += (
                f'    {moa__ldfo}[{wgwm__bmf}] = blk_{kxax__qae}[i].{func_name}()\n'
                )
        else:
            gme__gluqb += (
                f'    {moa__ldfo}[{wgwm__bmf}] = {func_name}(blk_{kxax__qae}[i])\n'
                )
        if opz__ahd:
            gme__gluqb += f"""  out_table = bodo.hiframes.table.set_table_block(out_table, {moa__ldfo}, {kxax__qae})
"""
    if opz__ahd:
        gme__gluqb += (
            f'  out_table = bodo.hiframes.table.set_table_len(out_table, l)\n')
        gme__gluqb += '  return out_table'
    else:
        gme__gluqb += (
            '  return bodo.hiframes.table.init_table_from_lists((out_list,), table_typ)'
            )
    vikrx__bmkvt = {}
    exec(gme__gluqb, xyim__wlfnf, vikrx__bmkvt)
    return vikrx__bmkvt['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def generate_table_nbytes(table, out_arr, start_offset, parallel=False):
    xyim__wlfnf = {'bodo': bodo, 'sum_op': np.int32(bodo.libs.
        distributed_api.Reduce_Type.Sum.value)}
    gme__gluqb = 'def impl(table, out_arr, start_offset, parallel=False):\n'
    gme__gluqb += '  bodo.hiframes.table.ensure_table_unboxed(table, None)\n'
    for kxax__qae in table.type_to_blk.values():
        gme__gluqb += (
            f'  blk = bodo.hiframes.table.get_table_block(table, {kxax__qae})\n'
            )
        xyim__wlfnf[f'col_indices_{kxax__qae}'] = np.array(table.
            block_to_arr_ind[kxax__qae], dtype=np.int64)
        gme__gluqb += '  for i in range(len(blk)):\n'
        gme__gluqb += f'    col_loc = col_indices_{kxax__qae}[i]\n'
        gme__gluqb += '    out_arr[col_loc + start_offset] = blk[i].nbytes\n'
    gme__gluqb += '  if parallel:\n'
    gme__gluqb += '    for i in range(start_offset, len(out_arr)):\n'
    gme__gluqb += (
        '      out_arr[i] = bodo.libs.distributed_api.dist_reduce(out_arr[i], sum_op)\n'
        )
    vikrx__bmkvt = {}
    exec(gme__gluqb, xyim__wlfnf, vikrx__bmkvt)
    return vikrx__bmkvt['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_concat(table, col_nums, arr_type):
    arr_type = arr_type.instance_type if isinstance(arr_type, types.TypeRef
        ) else arr_type
    ogly__ljmtp = table.type_to_blk[arr_type]
    xyim__wlfnf = {'bodo': bodo}
    xyim__wlfnf['col_indices'] = np.array(table.block_to_arr_ind[
        ogly__ljmtp], dtype=np.int64)
    gme__gluqb = 'def impl(table, col_nums, arr_type):\n'
    gme__gluqb += (
        f'  blk = bodo.hiframes.table.get_table_block(table, {ogly__ljmtp})\n')
    gme__gluqb += (
        '  col_num_to_ind_in_blk = {c : i for i, c in enumerate(col_indices)}\n'
        )
    gme__gluqb += '  n = len(table)\n'
    buos__whfh = bodo.utils.typing.is_str_arr_type(arr_type)
    if buos__whfh:
        gme__gluqb += '  total_chars = 0\n'
        gme__gluqb += '  for c in col_nums:\n'
        gme__gluqb += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
        gme__gluqb += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
        gme__gluqb += (
            '    total_chars += bodo.libs.str_arr_ext.num_total_chars(arr)\n')
        gme__gluqb += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n * len(col_nums), total_chars)
"""
    else:
        gme__gluqb += """  out_arr = bodo.utils.utils.alloc_type(n * len(col_nums), arr_type, (-1,))
"""
    gme__gluqb += '  for i in range(len(col_nums)):\n'
    gme__gluqb += '    c = col_nums[i]\n'
    if not buos__whfh:
        gme__gluqb += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
    gme__gluqb += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
    gme__gluqb += '    off = i * n\n'
    gme__gluqb += '    for j in range(len(arr)):\n'
    gme__gluqb += '      if bodo.libs.array_kernels.isna(arr, j):\n'
    gme__gluqb += '        bodo.libs.array_kernels.setna(out_arr, off+j)\n'
    gme__gluqb += '      else:\n'
    gme__gluqb += '        out_arr[off+j] = arr[j]\n'
    gme__gluqb += '  return out_arr\n'
    kprx__vey = {}
    exec(gme__gluqb, xyim__wlfnf, kprx__vey)
    rjth__ybyjp = kprx__vey['impl']
    return rjth__ybyjp
