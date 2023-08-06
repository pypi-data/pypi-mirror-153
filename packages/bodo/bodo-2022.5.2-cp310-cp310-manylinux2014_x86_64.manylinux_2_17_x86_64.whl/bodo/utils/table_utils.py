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
    nqz__svemt = not is_overload_none(func_name)
    if nqz__svemt:
        func_name = get_overload_const_str(func_name)
        ckp__styzh = get_overload_const_bool(is_method)
    xjyzh__xeno = out_arr_typ.instance_type if isinstance(out_arr_typ,
        types.TypeRef) else out_arr_typ
    thn__hghm = xjyzh__xeno == types.none
    sgr__xtdh = len(table.arr_types)
    if thn__hghm:
        dychq__hbih = table
    else:
        rpe__bgu = tuple([xjyzh__xeno] * sgr__xtdh)
        dychq__hbih = TableType(rpe__bgu)
    ova__htiln = {'bodo': bodo, 'lst_dtype': xjyzh__xeno, 'table_typ':
        dychq__hbih}
    fys__pjbqt = (
        'def impl(table, func_name, out_arr_typ, is_method, used_cols=None):\n'
        )
    if thn__hghm:
        fys__pjbqt += (
            f'  out_table = bodo.hiframes.table.init_table(table, False)\n')
        fys__pjbqt += f'  l = len(table)\n'
    else:
        fys__pjbqt += f"""  out_list = bodo.hiframes.table.alloc_empty_list_type({sgr__xtdh}, lst_dtype)
"""
    if not is_overload_none(used_cols):
        fys__pjbqt += f'  used_cols_set = set(used_cols)\n'
    else:
        fys__pjbqt += f'  used_cols_set = used_cols\n'
    fys__pjbqt += (
        f'  bodo.hiframes.table.ensure_table_unboxed(table, used_cols_set)\n')
    for ppq__encoz in table.type_to_blk.values():
        fys__pjbqt += f"""  blk_{ppq__encoz} = bodo.hiframes.table.get_table_block(table, {ppq__encoz})
"""
        ova__htiln[f'col_indices_{ppq__encoz}'] = np.array(table.
            block_to_arr_ind[ppq__encoz], dtype=np.int64)
        if thn__hghm:
            fys__pjbqt += f"""  out_list_{ppq__encoz} = bodo.hiframes.table.alloc_list_like(blk_{ppq__encoz}, False)
"""
        fys__pjbqt += f'  for i in range(len(blk_{ppq__encoz})):\n'
        fys__pjbqt += f'    col_loc = col_indices_{ppq__encoz}[i]\n'
        if not is_overload_none(used_cols):
            fys__pjbqt += f'    if col_loc not in used_cols_set:\n'
            fys__pjbqt += f'        continue\n'
        if thn__hghm:
            qgi__vxwj = 'i'
            fxyfr__ufv = f'out_list_{ppq__encoz}'
        else:
            qgi__vxwj = 'col_loc'
            fxyfr__ufv = 'out_list'
        if not nqz__svemt:
            fys__pjbqt += (
                f'    {fxyfr__ufv}[{qgi__vxwj}] = blk_{ppq__encoz}[i]\n')
        elif ckp__styzh:
            fys__pjbqt += (
                f'    {fxyfr__ufv}[{qgi__vxwj}] = blk_{ppq__encoz}[i].{func_name}()\n'
                )
        else:
            fys__pjbqt += (
                f'    {fxyfr__ufv}[{qgi__vxwj}] = {func_name}(blk_{ppq__encoz}[i])\n'
                )
        if thn__hghm:
            fys__pjbqt += f"""  out_table = bodo.hiframes.table.set_table_block(out_table, {fxyfr__ufv}, {ppq__encoz})
"""
    if thn__hghm:
        fys__pjbqt += (
            f'  out_table = bodo.hiframes.table.set_table_len(out_table, l)\n')
        fys__pjbqt += '  return out_table'
    else:
        fys__pjbqt += (
            '  return bodo.hiframes.table.init_table_from_lists((out_list,), table_typ)'
            )
    ncspm__dbose = {}
    exec(fys__pjbqt, ova__htiln, ncspm__dbose)
    return ncspm__dbose['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def generate_table_nbytes(table, out_arr, start_offset, parallel=False):
    ova__htiln = {'bodo': bodo, 'sum_op': np.int32(bodo.libs.
        distributed_api.Reduce_Type.Sum.value)}
    fys__pjbqt = 'def impl(table, out_arr, start_offset, parallel=False):\n'
    fys__pjbqt += '  bodo.hiframes.table.ensure_table_unboxed(table, None)\n'
    for ppq__encoz in table.type_to_blk.values():
        fys__pjbqt += (
            f'  blk = bodo.hiframes.table.get_table_block(table, {ppq__encoz})\n'
            )
        ova__htiln[f'col_indices_{ppq__encoz}'] = np.array(table.
            block_to_arr_ind[ppq__encoz], dtype=np.int64)
        fys__pjbqt += '  for i in range(len(blk)):\n'
        fys__pjbqt += f'    col_loc = col_indices_{ppq__encoz}[i]\n'
        fys__pjbqt += '    out_arr[col_loc + start_offset] = blk[i].nbytes\n'
    fys__pjbqt += '  if parallel:\n'
    fys__pjbqt += '    for i in range(start_offset, len(out_arr)):\n'
    fys__pjbqt += (
        '      out_arr[i] = bodo.libs.distributed_api.dist_reduce(out_arr[i], sum_op)\n'
        )
    ncspm__dbose = {}
    exec(fys__pjbqt, ova__htiln, ncspm__dbose)
    return ncspm__dbose['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_concat(table, col_nums, arr_type):
    arr_type = arr_type.instance_type if isinstance(arr_type, types.TypeRef
        ) else arr_type
    angqd__njaxw = table.type_to_blk[arr_type]
    ova__htiln = {'bodo': bodo}
    ova__htiln['col_indices'] = np.array(table.block_to_arr_ind[
        angqd__njaxw], dtype=np.int64)
    fys__pjbqt = 'def impl(table, col_nums, arr_type):\n'
    fys__pjbqt += (
        f'  blk = bodo.hiframes.table.get_table_block(table, {angqd__njaxw})\n'
        )
    fys__pjbqt += (
        '  col_num_to_ind_in_blk = {c : i for i, c in enumerate(col_indices)}\n'
        )
    fys__pjbqt += '  n = len(table)\n'
    pmosj__sfk = bodo.utils.typing.is_str_arr_type(arr_type)
    if pmosj__sfk:
        fys__pjbqt += '  total_chars = 0\n'
        fys__pjbqt += '  for c in col_nums:\n'
        fys__pjbqt += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
        fys__pjbqt += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
        fys__pjbqt += (
            '    total_chars += bodo.libs.str_arr_ext.num_total_chars(arr)\n')
        fys__pjbqt += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n * len(col_nums), total_chars)
"""
    else:
        fys__pjbqt += """  out_arr = bodo.utils.utils.alloc_type(n * len(col_nums), arr_type, (-1,))
"""
    fys__pjbqt += '  for i in range(len(col_nums)):\n'
    fys__pjbqt += '    c = col_nums[i]\n'
    if not pmosj__sfk:
        fys__pjbqt += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
    fys__pjbqt += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
    fys__pjbqt += '    off = i * n\n'
    fys__pjbqt += '    for j in range(len(arr)):\n'
    fys__pjbqt += '      if bodo.libs.array_kernels.isna(arr, j):\n'
    fys__pjbqt += '        bodo.libs.array_kernels.setna(out_arr, off+j)\n'
    fys__pjbqt += '      else:\n'
    fys__pjbqt += '        out_arr[off+j] = arr[j]\n'
    fys__pjbqt += '  return out_arr\n'
    mihz__enl = {}
    exec(fys__pjbqt, ova__htiln, mihz__enl)
    ccc__zpllh = mihz__enl['impl']
    return ccc__zpllh
