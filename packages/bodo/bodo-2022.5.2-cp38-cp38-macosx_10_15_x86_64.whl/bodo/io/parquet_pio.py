import os
import warnings
from collections import defaultdict
from glob import has_magic
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
import pyarrow
import pyarrow.dataset as ds
from numba.core import ir, types
from numba.core.ir_utils import compile_to_numba_ir, get_definition, guard, mk_unique_var, next_label, replace_arg_nodes
from numba.extending import NativeValue, box, intrinsic, models, overload, register_model, unbox
from pyarrow import null
import bodo
import bodo.ir.parquet_ext
import bodo.utils.tracing as tracing
from bodo.hiframes.datetime_date_ext import datetime_date_array_type, datetime_date_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.hiframes.table import TableType
from bodo.io.fs_io import get_hdfs_fs, get_s3_bucket_region_njit, get_s3_fs_from_path, get_s3_subtree_fs, get_storage_options_pyobject, storage_options_dict_type
from bodo.io.helpers import is_nullable
from bodo.libs.array import cpp_table_to_py_table, delete_table, info_from_table, info_to_array, table_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.distributed_api import get_end, get_start
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type, unicode_to_utf8
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.transforms import distributed_pass
from bodo.utils.transform import get_const_value
from bodo.utils.typing import BodoError, BodoWarning, FileInfo, get_overload_const_str
from bodo.utils.utils import check_and_propagate_cpp_exception, numba_to_c_type, sanitize_varname
use_nullable_int_arr = True
from urllib.parse import urlparse
import bodo.io.pa_parquet
REMOTE_FILESYSTEMS = {'s3', 'gcs', 'gs', 'http', 'hdfs', 'abfs', 'abfss'}
READ_STR_AS_DICT_THRESHOLD = 1.0
list_of_files_error_msg = (
    '. Make sure the list/glob passed to read_parquet() only contains paths to files (no directories)'
    )


class ParquetPredicateType(types.Type):

    def __init__(self):
        super(ParquetPredicateType, self).__init__(name=
            'ParquetPredicateType()')


parquet_predicate_type = ParquetPredicateType()
types.parquet_predicate_type = parquet_predicate_type
register_model(ParquetPredicateType)(models.OpaqueModel)


@unbox(ParquetPredicateType)
def unbox_parquet_predicate_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


@box(ParquetPredicateType)
def box_parquet_predicate_type(typ, val, c):
    c.pyapi.incref(val)
    return val


class ReadParquetFilepathType(types.Opaque):

    def __init__(self):
        super(ReadParquetFilepathType, self).__init__(name=
            'ReadParquetFilepathType')


read_parquet_fpath_type = ReadParquetFilepathType()
types.read_parquet_fpath_type = read_parquet_fpath_type
register_model(ReadParquetFilepathType)(models.OpaqueModel)


@unbox(ReadParquetFilepathType)
def unbox_read_parquet_fpath_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


class ParquetFileInfo(FileInfo):

    def __init__(self, columns, storage_options=None, input_file_name_col=
        None, read_as_dict_cols=None):
        self.columns = columns
        self.storage_options = storage_options
        self.input_file_name_col = input_file_name_col
        self.read_as_dict_cols = read_as_dict_cols
        super().__init__()

    def _get_schema(self, fname):
        try:
            return parquet_file_schema(fname, selected_columns=self.columns,
                storage_options=self.storage_options, input_file_name_col=
                self.input_file_name_col, read_as_dict_cols=self.
                read_as_dict_cols)
        except OSError as ftd__azh:
            if 'non-file path' in str(ftd__azh):
                raise FileNotFoundError(str(ftd__azh))
            raise


class ParquetHandler:

    def __init__(self, func_ir, typingctx, args, _locals):
        self.func_ir = func_ir
        self.typingctx = typingctx
        self.args = args
        self.locals = _locals

    def gen_parquet_read(self, file_name, lhs, columns, storage_options=
        None, input_file_name_col=None, read_as_dict_cols=None):
        ooyg__kmc = lhs.scope
        xarmq__dwu = lhs.loc
        gap__cneae = None
        if lhs.name in self.locals:
            gap__cneae = self.locals[lhs.name]
            self.locals.pop(lhs.name)
        avcz__exf = {}
        if lhs.name + ':convert' in self.locals:
            avcz__exf = self.locals[lhs.name + ':convert']
            self.locals.pop(lhs.name + ':convert')
        if gap__cneae is None:
            tlyiv__pbrc = (
                'Parquet schema not available. Either path argument should be constant for Bodo to look at the file at compile time or schema should be provided. For more information, see: https://docs.bodo.ai/latest/file_io/#parquet-section.'
                )
            gpc__ikvn = get_const_value(file_name, self.func_ir,
                tlyiv__pbrc, arg_types=self.args, file_info=ParquetFileInfo
                (columns, storage_options=storage_options,
                input_file_name_col=input_file_name_col, read_as_dict_cols=
                read_as_dict_cols))
            rugec__tlke = False
            euyj__sidcc = guard(get_definition, self.func_ir, file_name)
            if isinstance(euyj__sidcc, ir.Arg):
                typ = self.args[euyj__sidcc.index]
                if isinstance(typ, types.FilenameType):
                    (col_names, hxmg__hfump, pxkuh__quy, col_indices,
                        partition_names, dzhlt__otgld, leh__ujty) = typ.schema
                    rugec__tlke = True
            if not rugec__tlke:
                (col_names, hxmg__hfump, pxkuh__quy, col_indices,
                    partition_names, dzhlt__otgld, leh__ujty) = (
                    parquet_file_schema(gpc__ikvn, columns, storage_options
                    =storage_options, input_file_name_col=
                    input_file_name_col, read_as_dict_cols=read_as_dict_cols))
        else:
            kobqh__dos = list(gap__cneae.keys())
            age__stmdc = {c: ked__susus for ked__susus, c in enumerate(
                kobqh__dos)}
            becd__unmck = [tdhm__bvxrt for tdhm__bvxrt in gap__cneae.values()]
            pxkuh__quy = 'index' if 'index' in age__stmdc else None
            if columns is None:
                selected_columns = kobqh__dos
            else:
                selected_columns = columns
            col_indices = [age__stmdc[c] for c in selected_columns]
            hxmg__hfump = [becd__unmck[age__stmdc[c]] for c in selected_columns
                ]
            col_names = selected_columns
            pxkuh__quy = pxkuh__quy if pxkuh__quy in col_names else None
            partition_names = []
            dzhlt__otgld = []
            leh__ujty = []
        ogvf__gifte = None if isinstance(pxkuh__quy, dict
            ) or pxkuh__quy is None else pxkuh__quy
        index_column_index = None
        index_column_type = types.none
        if ogvf__gifte:
            jmp__msetd = col_names.index(ogvf__gifte)
            index_column_index = col_indices.pop(jmp__msetd)
            index_column_type = hxmg__hfump.pop(jmp__msetd)
            col_names.pop(jmp__msetd)
        for ked__susus, c in enumerate(col_names):
            if c in avcz__exf:
                hxmg__hfump[ked__susus] = avcz__exf[c]
        jkha__pyrq = [ir.Var(ooyg__kmc, mk_unique_var('pq_table'),
            xarmq__dwu), ir.Var(ooyg__kmc, mk_unique_var('pq_index'),
            xarmq__dwu)]
        ocu__bbng = [bodo.ir.parquet_ext.ParquetReader(file_name, lhs.name,
            col_names, col_indices, hxmg__hfump, jkha__pyrq, xarmq__dwu,
            partition_names, storage_options, index_column_index,
            index_column_type, input_file_name_col, dzhlt__otgld, leh__ujty)]
        return (col_names, jkha__pyrq, pxkuh__quy, ocu__bbng, hxmg__hfump,
            index_column_type)


def pq_distributed_run(pq_node, array_dists, typemap, calltypes, typingctx,
    targetctx, meta_head_only_info=None):
    mwkne__ozb = len(pq_node.out_vars)
    dnf_filter_str = 'None'
    expr_filter_str = 'None'
    lsgu__zxj, pcpra__amh = bodo.ir.connector.generate_filter_map(pq_node.
        filters)
    extra_args = ', '.join(lsgu__zxj.values())
    dnf_filter_str, expr_filter_str = bodo.ir.connector.generate_arrow_filters(
        pq_node.filters, lsgu__zxj, pcpra__amh, pq_node.
        original_df_colnames, pq_node.partition_names, pq_node.
        original_out_types, typemap, 'parquet')
    wnuk__tpu = ', '.join(f'out{ked__susus}' for ked__susus in range(
        mwkne__ozb))
    vcyaz__nlt = f'def pq_impl(fname, {extra_args}):\n'
    vcyaz__nlt += (
        f'    (total_rows, {wnuk__tpu},) = _pq_reader_py(fname, {extra_args})\n'
        )
    jbef__ytl = {}
    exec(vcyaz__nlt, {}, jbef__ytl)
    rpq__vhbr = jbef__ytl['pq_impl']
    if bodo.user_logging.get_verbose_level() >= 1:
        hht__onizm = pq_node.loc.strformat()
        bju__bktt = []
        vhg__jtq = []
        for ked__susus in pq_node.type_usecol_offset:
            eeb__ecvt = pq_node.df_colnames[ked__susus]
            bju__bktt.append(eeb__ecvt)
            if isinstance(pq_node.out_types[ked__susus], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                vhg__jtq.append(eeb__ecvt)
        mryam__tnls = (
            'Finish column pruning on read_parquet node:\n%s\nColumns loaded %s\n'
            )
        bodo.user_logging.log_message('Column Pruning', mryam__tnls,
            hht__onizm, bju__bktt)
        if vhg__jtq:
            dveh__hjq = """Finished optimized encoding on read_parquet node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', dveh__hjq,
                hht__onizm, vhg__jtq)
    parallel = bodo.ir.connector.is_connector_table_parallel(pq_node,
        array_dists, typemap, 'ParquetReader')
    if pq_node.unsupported_columns:
        qikit__salu = set(pq_node.type_usecol_offset)
        pos__wpuob = set(pq_node.unsupported_columns)
        qjnc__euk = qikit__salu & pos__wpuob
        if qjnc__euk:
            bfon__ehvtu = sorted(qjnc__euk)
            vhn__jazed = [
                f'pandas.read_parquet(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                "Please manually remove these columns from your read_parquet with the 'columns' argument. If these "
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            ajn__wblt = 0
            for nymxa__gze in bfon__ehvtu:
                while pq_node.unsupported_columns[ajn__wblt] != nymxa__gze:
                    ajn__wblt += 1
                vhn__jazed.append(
                    f"Column '{pq_node.df_colnames[nymxa__gze]}' with unsupported arrow type {pq_node.unsupported_arrow_types[ajn__wblt]}"
                    )
                ajn__wblt += 1
            alddi__bsrc = '\n'.join(vhn__jazed)
            raise BodoError(alddi__bsrc, loc=pq_node.loc)
    wcix__khny = _gen_pq_reader_py(pq_node.df_colnames, pq_node.col_indices,
        pq_node.type_usecol_offset, pq_node.out_types, pq_node.
        storage_options, pq_node.partition_names, dnf_filter_str,
        expr_filter_str, extra_args, parallel, meta_head_only_info, pq_node
        .index_column_index, pq_node.index_column_type, pq_node.
        input_file_name_col)
    nevok__ppyso = typemap[pq_node.file_name.name]
    uqryx__oeb = (nevok__ppyso,) + tuple(typemap[dhs__gfml.name] for
        dhs__gfml in pcpra__amh)
    tho__dvdj = compile_to_numba_ir(rpq__vhbr, {'_pq_reader_py': wcix__khny
        }, typingctx=typingctx, targetctx=targetctx, arg_typs=uqryx__oeb,
        typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(tho__dvdj, [pq_node.file_name] + pcpra__amh)
    ocu__bbng = tho__dvdj.body[:-3]
    if meta_head_only_info:
        ocu__bbng[-1 - mwkne__ozb].target = meta_head_only_info[1]
    ocu__bbng[-2].target = pq_node.out_vars[0]
    ocu__bbng[-1].target = pq_node.out_vars[1]
    assert not (pq_node.index_column_index is None and not pq_node.
        type_usecol_offset
        ), 'At most one of table and index should be dead if the Parquet IR node is live'
    if pq_node.index_column_index is None:
        ocu__bbng.pop(-1)
    elif not pq_node.type_usecol_offset:
        ocu__bbng.pop(-2)
    return ocu__bbng


distributed_pass.distributed_run_extensions[bodo.ir.parquet_ext.ParquetReader
    ] = pq_distributed_run


def get_filters_pyobject(dnf_filter_str, expr_filter_str, vars):
    pass


@overload(get_filters_pyobject, no_unliteral=True)
def overload_get_filters_pyobject(dnf_filter_str, expr_filter_str, var_tup):
    njmmk__bsj = get_overload_const_str(dnf_filter_str)
    znzr__vzndg = get_overload_const_str(expr_filter_str)
    zsh__djca = ', '.join(f'f{ked__susus}' for ked__susus in range(len(
        var_tup)))
    vcyaz__nlt = 'def impl(dnf_filter_str, expr_filter_str, var_tup):\n'
    if len(var_tup):
        vcyaz__nlt += f'  {zsh__djca}, = var_tup\n'
    vcyaz__nlt += """  with numba.objmode(dnf_filters_py='parquet_predicate_type', expr_filters_py='parquet_predicate_type'):
"""
    vcyaz__nlt += f'    dnf_filters_py = {njmmk__bsj}\n'
    vcyaz__nlt += f'    expr_filters_py = {znzr__vzndg}\n'
    vcyaz__nlt += '  return (dnf_filters_py, expr_filters_py)\n'
    jbef__ytl = {}
    exec(vcyaz__nlt, globals(), jbef__ytl)
    return jbef__ytl['impl']


@numba.njit
def get_fname_pyobject(fname):
    with numba.objmode(fname_py='read_parquet_fpath_type'):
        fname_py = fname
    return fname_py


def _gen_pq_reader_py(col_names, col_indices, type_usecol_offset, out_types,
    storage_options, partition_names, dnf_filter_str, expr_filter_str,
    extra_args, is_parallel, meta_head_only_info, index_column_index,
    index_column_type, input_file_name_col):
    duxkr__mot = next_label()
    nofvf__dgv = ',' if extra_args else ''
    vcyaz__nlt = f'def pq_reader_py(fname,{extra_args}):\n'
    vcyaz__nlt += (
        f"    ev = bodo.utils.tracing.Event('read_parquet', {is_parallel})\n")
    vcyaz__nlt += f"    ev.add_attribute('g_fname', fname)\n"
    vcyaz__nlt += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={is_parallel})
"""
    vcyaz__nlt += f"""    dnf_filters, expr_filters = get_filters_pyobject("{dnf_filter_str}", "{expr_filter_str}", ({extra_args}{nofvf__dgv}))
"""
    vcyaz__nlt += '    fname_py = get_fname_pyobject(fname)\n'
    storage_options['bodo_dummy'] = 'dummy'
    vcyaz__nlt += (
        f'    storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    tot_rows_to_read = -1
    if meta_head_only_info and meta_head_only_info[0] is not None:
        tot_rows_to_read = meta_head_only_info[0]
    zhq__bzvtd = not type_usecol_offset
    yadiu__seswn = [sanitize_varname(c) for c in col_names]
    partition_names = [sanitize_varname(c) for c in partition_names]
    input_file_name_col = sanitize_varname(input_file_name_col
        ) if input_file_name_col is not None and col_names.index(
        input_file_name_col) in type_usecol_offset else None
    mmqd__awi = {c: ked__susus for ked__susus, c in enumerate(col_indices)}
    bevy__xytig = {c: ked__susus for ked__susus, c in enumerate(yadiu__seswn)}
    wibe__vvx = []
    edj__oemkm = set()
    eyo__zllm = partition_names + [input_file_name_col]
    for ked__susus in type_usecol_offset:
        if yadiu__seswn[ked__susus] not in eyo__zllm:
            wibe__vvx.append(col_indices[ked__susus])
        elif not input_file_name_col or yadiu__seswn[ked__susus
            ] != input_file_name_col:
            edj__oemkm.add(col_indices[ked__susus])
    if index_column_index is not None:
        wibe__vvx.append(index_column_index)
    wibe__vvx = sorted(wibe__vvx)
    fhlqh__qgiwt = {c: ked__susus for ked__susus, c in enumerate(wibe__vvx)}
    sluxw__ezbzt = [(int(is_nullable(out_types[mmqd__awi[oonh__lgvb]])) if 
        oonh__lgvb != index_column_index else int(is_nullable(
        index_column_type))) for oonh__lgvb in wibe__vvx]
    str_as_dict_cols = []
    for oonh__lgvb in wibe__vvx:
        if oonh__lgvb == index_column_index:
            tdhm__bvxrt = index_column_type
        else:
            tdhm__bvxrt = out_types[mmqd__awi[oonh__lgvb]]
        if tdhm__bvxrt == dict_str_arr_type:
            str_as_dict_cols.append(oonh__lgvb)
    xzc__kaal = []
    vzua__rdqg = {}
    nfb__yfsvb = []
    utj__aqpk = []
    for ked__susus, mzv__rxp in enumerate(partition_names):
        try:
            ufs__dgchc = bevy__xytig[mzv__rxp]
            if col_indices[ufs__dgchc] not in edj__oemkm:
                continue
        except (KeyError, ValueError) as lmwt__fusd:
            continue
        vzua__rdqg[mzv__rxp] = len(xzc__kaal)
        xzc__kaal.append(mzv__rxp)
        nfb__yfsvb.append(ked__susus)
        oqj__goa = out_types[ufs__dgchc].dtype
        abznt__rdlzv = (bodo.hiframes.pd_categorical_ext.
            get_categories_int_type(oqj__goa))
        utj__aqpk.append(numba_to_c_type(abznt__rdlzv))
    vcyaz__nlt += f'    total_rows_np = np.array([0], dtype=np.int64)\n'
    vcyaz__nlt += f'    out_table = pq_read(\n'
    vcyaz__nlt += f'        fname_py, {is_parallel},\n'
    vcyaz__nlt += f'        unicode_to_utf8(bucket_region),\n'
    vcyaz__nlt += f'        dnf_filters, expr_filters,\n'
    vcyaz__nlt += f"""        storage_options_py, {tot_rows_to_read}, selected_cols_arr_{duxkr__mot}.ctypes,
"""
    vcyaz__nlt += f'        {len(wibe__vvx)},\n'
    vcyaz__nlt += f'        nullable_cols_arr_{duxkr__mot}.ctypes,\n'
    if len(nfb__yfsvb) > 0:
        vcyaz__nlt += (
            f'        np.array({nfb__yfsvb}, dtype=np.int32).ctypes,\n')
        vcyaz__nlt += (
            f'        np.array({utj__aqpk}, dtype=np.int32).ctypes,\n')
        vcyaz__nlt += f'        {len(nfb__yfsvb)},\n'
    else:
        vcyaz__nlt += f'        0, 0, 0,\n'
    if len(str_as_dict_cols) > 0:
        vcyaz__nlt += f"""        np.array({str_as_dict_cols}, dtype=np.int32).ctypes, {len(str_as_dict_cols)},
"""
    else:
        vcyaz__nlt += f'        0, 0,\n'
    vcyaz__nlt += f'        total_rows_np.ctypes,\n'
    vcyaz__nlt += f'        {input_file_name_col is not None},\n'
    vcyaz__nlt += f'    )\n'
    vcyaz__nlt += f'    check_and_propagate_cpp_exception()\n'
    cynbn__rezq = 'None'
    whpgo__ina = index_column_type
    rlpaf__txvbl = TableType(tuple(out_types))
    if zhq__bzvtd:
        rlpaf__txvbl = types.none
    if index_column_index is not None:
        zpfks__yjlpj = fhlqh__qgiwt[index_column_index]
        cynbn__rezq = (
            f'info_to_array(info_from_table(out_table, {zpfks__yjlpj}), index_arr_type)'
            )
    vcyaz__nlt += f'    index_arr = {cynbn__rezq}\n'
    if zhq__bzvtd:
        nmnh__tgb = None
    else:
        nmnh__tgb = []
        srdnl__izaw = 0
        ttxrc__fvalb = col_indices[col_names.index(input_file_name_col)
            ] if input_file_name_col is not None else None
        for ked__susus, nymxa__gze in enumerate(col_indices):
            if srdnl__izaw < len(type_usecol_offset
                ) and ked__susus == type_usecol_offset[srdnl__izaw]:
                mees__ped = col_indices[ked__susus]
                if ttxrc__fvalb and mees__ped == ttxrc__fvalb:
                    nmnh__tgb.append(len(wibe__vvx) + len(xzc__kaal))
                elif mees__ped in edj__oemkm:
                    tfl__hlx = yadiu__seswn[ked__susus]
                    nmnh__tgb.append(len(wibe__vvx) + vzua__rdqg[tfl__hlx])
                else:
                    nmnh__tgb.append(fhlqh__qgiwt[nymxa__gze])
                srdnl__izaw += 1
            else:
                nmnh__tgb.append(-1)
        nmnh__tgb = np.array(nmnh__tgb, dtype=np.int64)
    if zhq__bzvtd:
        vcyaz__nlt += '    T = None\n'
    else:
        vcyaz__nlt += f"""    T = cpp_table_to_py_table(out_table, table_idx_{duxkr__mot}, py_table_type_{duxkr__mot})
"""
    vcyaz__nlt += f'    delete_table(out_table)\n'
    vcyaz__nlt += f'    total_rows = total_rows_np[0]\n'
    vcyaz__nlt += f'    ev.finalize()\n'
    vcyaz__nlt += f'    return (total_rows, T, index_arr)\n'
    jbef__ytl = {}
    xyzc__zdj = {f'py_table_type_{duxkr__mot}': rlpaf__txvbl,
        f'table_idx_{duxkr__mot}': nmnh__tgb,
        f'selected_cols_arr_{duxkr__mot}': np.array(wibe__vvx, np.int32),
        f'nullable_cols_arr_{duxkr__mot}': np.array(sluxw__ezbzt, np.int32),
        'index_arr_type': whpgo__ina, 'cpp_table_to_py_table':
        cpp_table_to_py_table, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'delete_table': delete_table,
        'check_and_propagate_cpp_exception':
        check_and_propagate_cpp_exception, 'pq_read': _pq_read,
        'unicode_to_utf8': unicode_to_utf8, 'get_filters_pyobject':
        get_filters_pyobject, 'get_storage_options_pyobject':
        get_storage_options_pyobject, 'get_fname_pyobject':
        get_fname_pyobject, 'np': np, 'pd': pd, 'bodo': bodo}
    exec(vcyaz__nlt, xyzc__zdj, jbef__ytl)
    wcix__khny = jbef__ytl['pq_reader_py']
    wab__drja = numba.njit(wcix__khny, no_cpython_wrapper=True)
    return wab__drja


import pyarrow as pa
_pa_numba_typ_map = {pa.bool_(): types.bool_, pa.int8(): types.int8, pa.
    int16(): types.int16, pa.int32(): types.int32, pa.int64(): types.int64,
    pa.uint8(): types.uint8, pa.uint16(): types.uint16, pa.uint32(): types.
    uint32, pa.uint64(): types.uint64, pa.float32(): types.float32, pa.
    float64(): types.float64, pa.string(): string_type, pa.binary():
    bytes_type, pa.date32(): datetime_date_type, pa.date64(): types.
    NPDatetime('ns'), null(): string_type}


def get_arrow_timestamp_type(pa_ts_typ):
    vnue__tsuyt = 'ns', 'us', 'ms', 's'
    if pa_ts_typ.unit not in vnue__tsuyt:
        return types.Array(bodo.datetime64ns, 1, 'C'), False
    elif pa_ts_typ.tz is not None:
        hwfi__jniv = pa_ts_typ.to_pandas_dtype().tz
        iwf__byfsp = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(
            hwfi__jniv)
        return bodo.DatetimeArrayType(iwf__byfsp), True
    else:
        return types.Array(bodo.datetime64ns, 1, 'C'), True


def _get_numba_typ_from_pa_typ(pa_typ, is_index, nullable_from_metadata,
    category_info, str_as_dict=False):
    if isinstance(pa_typ.type, pa.ListType):
        hgz__nrw, erres__glw = _get_numba_typ_from_pa_typ(pa_typ.type.
            value_field, is_index, nullable_from_metadata, category_info)
        return ArrayItemArrayType(hgz__nrw), erres__glw
    if isinstance(pa_typ.type, pa.StructType):
        wjvh__ktia = []
        iscev__ugoc = []
        erres__glw = True
        for qqlx__guz in pa_typ.flatten():
            iscev__ugoc.append(qqlx__guz.name.split('.')[-1])
            zync__rihv, fiz__llk = _get_numba_typ_from_pa_typ(qqlx__guz,
                is_index, nullable_from_metadata, category_info)
            wjvh__ktia.append(zync__rihv)
            erres__glw = erres__glw and fiz__llk
        return StructArrayType(tuple(wjvh__ktia), tuple(iscev__ugoc)
            ), erres__glw
    if isinstance(pa_typ.type, pa.Decimal128Type):
        return DecimalArrayType(pa_typ.type.precision, pa_typ.type.scale), True
    if str_as_dict:
        if pa_typ.type != pa.string():
            raise BodoError(
                f'Read as dictionary used for non-string column {pa_typ}')
        return dict_str_arr_type, True
    if isinstance(pa_typ.type, pa.DictionaryType):
        if pa_typ.type.value_type != pa.string():
            raise BodoError(
                f'Parquet Categorical data type should be string, not {pa_typ.type.value_type}'
                )
        cfifc__mum = _pa_numba_typ_map[pa_typ.type.index_type]
        hvsvo__gofdj = PDCategoricalDtype(category_info[pa_typ.name], bodo.
            string_type, pa_typ.type.ordered, int_type=cfifc__mum)
        return CategoricalArrayType(hvsvo__gofdj), True
    if isinstance(pa_typ.type, pa.lib.TimestampType):
        return get_arrow_timestamp_type(pa_typ.type)
    elif pa_typ.type in _pa_numba_typ_map:
        nbpy__exjxs = _pa_numba_typ_map[pa_typ.type]
        erres__glw = True
    else:
        raise BodoError('Arrow data type {} not supported yet'.format(
            pa_typ.type))
    if nbpy__exjxs == datetime_date_type:
        return datetime_date_array_type, erres__glw
    if nbpy__exjxs == bytes_type:
        return binary_array_type, erres__glw
    hgz__nrw = (string_array_type if nbpy__exjxs == string_type else types.
        Array(nbpy__exjxs, 1, 'C'))
    if nbpy__exjxs == types.bool_:
        hgz__nrw = boolean_array
    if nullable_from_metadata is not None:
        npv__amlny = nullable_from_metadata
    else:
        npv__amlny = use_nullable_int_arr
    if npv__amlny and not is_index and isinstance(nbpy__exjxs, types.Integer
        ) and pa_typ.nullable:
        hgz__nrw = IntegerArrayType(nbpy__exjxs)
    return hgz__nrw, erres__glw


def get_parquet_dataset(fpath, get_row_counts=True, dnf_filters=None,
    expr_filters=None, storage_options=None, read_categories=False,
    is_parallel=False, tot_rows_to_read=None, typing_pa_schema=None):
    if get_row_counts:
        zofw__iovxg = tracing.Event('get_parquet_dataset')
    import time
    import pyarrow as pa
    import pyarrow.parquet as pq
    from mpi4py import MPI
    nlkc__rvad = MPI.COMM_WORLD
    if isinstance(fpath, list):
        easky__pok = urlparse(fpath[0])
        protocol = easky__pok.scheme
        wec__oenqc = easky__pok.netloc
        for ked__susus in range(len(fpath)):
            qon__dkzec = fpath[ked__susus]
            kipli__zrwmg = urlparse(qon__dkzec)
            if kipli__zrwmg.scheme != protocol:
                raise BodoError(
                    'All parquet files must use the same filesystem protocol')
            if kipli__zrwmg.netloc != wec__oenqc:
                raise BodoError(
                    'All parquet files must be in the same S3 bucket')
            fpath[ked__susus] = qon__dkzec.rstrip('/')
    else:
        easky__pok = urlparse(fpath)
        protocol = easky__pok.scheme
        fpath = fpath.rstrip('/')
    if protocol in {'gcs', 'gs'}:
        try:
            import gcsfs
        except ImportError as lmwt__fusd:
            mag__bkzc = """Couldn't import gcsfs, which is required for Google cloud access. gcsfs can be installed by calling 'conda install -c conda-forge gcsfs'.
"""
            raise BodoError(mag__bkzc)
    if protocol == 'http':
        try:
            import fsspec
        except ImportError as lmwt__fusd:
            mag__bkzc = """Couldn't import fsspec, which is required for http access. fsspec can be installed by calling 'conda install -c conda-forge fsspec'.
"""
    fs = []

    def getfs(parallel=False):
        if len(fs) == 1:
            return fs[0]
        if protocol == 's3':
            fs.append(get_s3_fs_from_path(fpath, parallel=parallel,
                storage_options=storage_options) if not isinstance(fpath,
                list) else get_s3_fs_from_path(fpath[0], parallel=parallel,
                storage_options=storage_options))
        elif protocol in {'gcs', 'gs'}:
            lxjg__laihh = gcsfs.GCSFileSystem(token=None)
            fs.append(lxjg__laihh)
        elif protocol == 'http':
            fs.append(fsspec.filesystem('http'))
        elif protocol in {'hdfs', 'abfs', 'abfss'}:
            fs.append(get_hdfs_fs(fpath) if not isinstance(fpath, list) else
                get_hdfs_fs(fpath[0]))
        else:
            fs.append(None)
        return fs[0]

    def get_legacy_fs():
        if protocol in {'s3', 'hdfs', 'abfs', 'abfss'}:
            from fsspec.implementations.arrow import ArrowFSWrapper
            return ArrowFSWrapper(getfs())
        else:
            return getfs()

    def glob(protocol, fs, path):
        if not protocol and fs is None:
            from fsspec.implementations.local import LocalFileSystem
            fs = LocalFileSystem()
        if isinstance(fs, pyarrow.fs.FileSystem):
            from fsspec.implementations.arrow import ArrowFSWrapper
            fs = ArrowFSWrapper(fs)
        try:
            if protocol in {'hdfs', 'abfs', 'abfss'}:
                prefix = f'{protocol}://{easky__pok.netloc}'
                path = path[len(prefix):]
            aymz__itpgd = fs.glob(path)
            if protocol == 's3':
                aymz__itpgd = [('s3://' + qon__dkzec) for qon__dkzec in
                    aymz__itpgd if not qon__dkzec.startswith('s3://')]
            elif protocol in {'hdfs', 'abfs', 'abfss'}:
                aymz__itpgd = [(prefix + qon__dkzec) for qon__dkzec in
                    aymz__itpgd]
        except:
            raise BodoError(
                f'glob pattern expansion not supported for {protocol}')
        if len(aymz__itpgd) == 0:
            raise BodoError('No files found matching glob pattern')
        return aymz__itpgd
    pio__mqsfd = False
    if get_row_counts:
        zmx__pqcxn = getfs(parallel=True)
        pio__mqsfd = bodo.parquet_validate_schema
    if bodo.get_rank() == 0:
        zfqgu__prmj = 1
        cgr__ftofe = os.cpu_count()
        if cgr__ftofe is not None and cgr__ftofe > 1:
            zfqgu__prmj = cgr__ftofe // 2
        try:
            if get_row_counts:
                yybu__eif = tracing.Event('pq.ParquetDataset', is_parallel=
                    False)
                if tracing.is_tracing():
                    yybu__eif.add_attribute('g_dnf_filter', str(dnf_filters))
            kzewf__omipy = pa.io_thread_count()
            pa.set_io_thread_count(zfqgu__prmj)
            if isinstance(fpath, list):
                vfz__bsp = []
                for chwl__fxb in fpath:
                    if has_magic(chwl__fxb):
                        vfz__bsp += glob(protocol, getfs(), chwl__fxb)
                    else:
                        vfz__bsp.append(chwl__fxb)
                fpath = vfz__bsp
            elif has_magic(fpath):
                fpath = glob(protocol, getfs(), fpath)
            if protocol == 's3':
                if isinstance(fpath, list):
                    get_legacy_fs().info(fpath[0])
                else:
                    get_legacy_fs().info(fpath)
            if protocol in {'hdfs', 'abfs', 'abfss'}:
                prefix = f'{protocol}://{easky__pok.netloc}'
                if isinstance(fpath, list):
                    cpl__qmi = [qon__dkzec[len(prefix):] for qon__dkzec in
                        fpath]
                else:
                    cpl__qmi = fpath[len(prefix):]
            else:
                cpl__qmi = fpath
            tnpyn__cqls = pq.ParquetDataset(cpl__qmi, filesystem=
                get_legacy_fs(), filters=None, use_legacy_dataset=True,
                validate_schema=False, metadata_nthreads=zfqgu__prmj)
            pa.set_io_thread_count(kzewf__omipy)
            if typing_pa_schema:
                fjw__yjbzk = typing_pa_schema
            else:
                fjw__yjbzk = bodo.io.pa_parquet.get_dataset_schema(tnpyn__cqls)
            if dnf_filters:
                if get_row_counts:
                    yybu__eif.add_attribute('num_pieces_before_filter', len
                        (tnpyn__cqls.pieces))
                novj__rib = time.time()
                tnpyn__cqls._filter(dnf_filters)
                if get_row_counts:
                    yybu__eif.add_attribute('dnf_filter_time', time.time() -
                        novj__rib)
                    yybu__eif.add_attribute('num_pieces_after_filter', len(
                        tnpyn__cqls.pieces))
            if get_row_counts:
                yybu__eif.finalize()
            tnpyn__cqls._metadata.fs = None
        except Exception as ftd__azh:
            if isinstance(fpath, list) and isinstance(ftd__azh, (OSError,
                FileNotFoundError)):
                ftd__azh = BodoError(str(ftd__azh) + list_of_files_error_msg)
            else:
                ftd__azh = BodoError(
                    f"""error from pyarrow: {type(ftd__azh).__name__}: {str(ftd__azh)}
"""
                    )
            nlkc__rvad.bcast(ftd__azh)
            raise ftd__azh
        if get_row_counts:
            iuymc__wwrhg = tracing.Event('bcast dataset')
        nlkc__rvad.bcast(tnpyn__cqls)
        nlkc__rvad.bcast(fjw__yjbzk)
    else:
        if get_row_counts:
            iuymc__wwrhg = tracing.Event('bcast dataset')
        tnpyn__cqls = nlkc__rvad.bcast(None)
        if isinstance(tnpyn__cqls, Exception):
            wijgt__bwdp = tnpyn__cqls
            raise wijgt__bwdp
        fjw__yjbzk = nlkc__rvad.bcast(None)
    bbasy__oydq = set(fjw__yjbzk.names)
    if get_row_counts:
        ueoi__xeti = getfs()
    else:
        ueoi__xeti = get_legacy_fs()
    tnpyn__cqls._metadata.fs = ueoi__xeti
    if get_row_counts:
        iuymc__wwrhg.finalize()
    tnpyn__cqls._bodo_total_rows = 0
    if get_row_counts and tot_rows_to_read == 0:
        get_row_counts = pio__mqsfd = False
        for chwl__fxb in tnpyn__cqls.pieces:
            chwl__fxb._bodo_num_rows = 0
    if get_row_counts or pio__mqsfd:
        if get_row_counts and tracing.is_tracing():
            wwp__apgop = tracing.Event('get_row_counts')
            wwp__apgop.add_attribute('g_num_pieces', len(tnpyn__cqls.pieces))
            wwp__apgop.add_attribute('g_expr_filters', str(expr_filters))
        dqul__kod = 0.0
        num_pieces = len(tnpyn__cqls.pieces)
        start = get_start(num_pieces, bodo.get_size(), bodo.get_rank())
        wua__ilfv = get_end(num_pieces, bodo.get_size(), bodo.get_rank())
        clw__grrtl = 0
        wswj__scqya = 0
        huf__ond = 0
        vdkef__uhp = True
        if expr_filters is not None:
            import random
            random.seed(37)
            hfs__dgf = random.sample(tnpyn__cqls.pieces, k=len(tnpyn__cqls.
                pieces))
        else:
            hfs__dgf = tnpyn__cqls.pieces
        for chwl__fxb in hfs__dgf:
            chwl__fxb._bodo_num_rows = 0
        fpaths = [chwl__fxb.path for chwl__fxb in hfs__dgf[start:wua__ilfv]]
        if protocol == 's3':
            wec__oenqc = easky__pok.netloc
            prefix = 's3://' + wec__oenqc + '/'
            fpaths = [qon__dkzec[len(prefix):] for qon__dkzec in fpaths]
            ueoi__xeti = get_s3_subtree_fs(wec__oenqc, region=getfs().
                region, storage_options=storage_options)
        else:
            ueoi__xeti = getfs()
        zfqgu__prmj = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), 4)
        pa.set_io_thread_count(zfqgu__prmj)
        pa.set_cpu_count(zfqgu__prmj)
        wijgt__bwdp = None
        try:
            xpcsg__quv = ds.dataset(fpaths, filesystem=ueoi__xeti,
                partitioning=ds.partitioning(flavor='hive') if tnpyn__cqls.
                partitions else None)
            for bydif__xhw, qmw__obg in zip(hfs__dgf[start:wua__ilfv],
                xpcsg__quv.get_fragments()):
                if pio__mqsfd:
                    ydv__iso = qmw__obg.metadata.schema.to_arrow_schema()
                    ebdky__kit = set(ydv__iso.names)
                    if bbasy__oydq != ebdky__kit:
                        ssovt__rtk = ebdky__kit - bbasy__oydq
                        ahxjl__zei = bbasy__oydq - ebdky__kit
                        tlyiv__pbrc = (
                            f'Schema in {bydif__xhw} was different.\n')
                        if ssovt__rtk:
                            tlyiv__pbrc += f"""File contains column(s) {ssovt__rtk} not found in other files in the dataset.
"""
                        if ahxjl__zei:
                            tlyiv__pbrc += f"""File missing column(s) {ahxjl__zei} found in other files in the dataset.
"""
                        raise BodoError(tlyiv__pbrc)
                    try:
                        fjw__yjbzk = pa.unify_schemas([fjw__yjbzk, ydv__iso])
                    except Exception as ftd__azh:
                        tlyiv__pbrc = (
                            f'Schema in {bydif__xhw} was different.\n' +
                            str(ftd__azh))
                        raise BodoError(tlyiv__pbrc)
                novj__rib = time.time()
                mtwgb__ijhf = qmw__obg.scanner(schema=xpcsg__quv.schema,
                    filter=expr_filters, use_threads=True).count_rows()
                dqul__kod += time.time() - novj__rib
                bydif__xhw._bodo_num_rows = mtwgb__ijhf
                clw__grrtl += mtwgb__ijhf
                wswj__scqya += qmw__obg.num_row_groups
                huf__ond += sum(scn__czrp.total_byte_size for scn__czrp in
                    qmw__obg.row_groups)
        except Exception as ftd__azh:
            wijgt__bwdp = ftd__azh
        if nlkc__rvad.allreduce(wijgt__bwdp is not None, op=MPI.LOR):
            for wijgt__bwdp in nlkc__rvad.allgather(wijgt__bwdp):
                if wijgt__bwdp:
                    if isinstance(fpath, list) and isinstance(wijgt__bwdp,
                        (OSError, FileNotFoundError)):
                        raise BodoError(str(wijgt__bwdp) +
                            list_of_files_error_msg)
                    raise wijgt__bwdp
        if pio__mqsfd:
            vdkef__uhp = nlkc__rvad.allreduce(vdkef__uhp, op=MPI.LAND)
            if not vdkef__uhp:
                raise BodoError("Schema in parquet files don't match")
        if get_row_counts:
            tnpyn__cqls._bodo_total_rows = nlkc__rvad.allreduce(clw__grrtl,
                op=MPI.SUM)
            mhfo__tkc = nlkc__rvad.allreduce(wswj__scqya, op=MPI.SUM)
            oyw__iltfq = nlkc__rvad.allreduce(huf__ond, op=MPI.SUM)
            ybvnm__dkke = np.array([chwl__fxb._bodo_num_rows for chwl__fxb in
                tnpyn__cqls.pieces])
            ybvnm__dkke = nlkc__rvad.allreduce(ybvnm__dkke, op=MPI.SUM)
            for chwl__fxb, jkg__rgv in zip(tnpyn__cqls.pieces, ybvnm__dkke):
                chwl__fxb._bodo_num_rows = jkg__rgv
            if is_parallel and bodo.get_rank(
                ) == 0 and mhfo__tkc < bodo.get_size() and mhfo__tkc != 0:
                warnings.warn(BodoWarning(
                    f"""Total number of row groups in parquet dataset {fpath} ({mhfo__tkc}) is too small for effective IO parallelization.
For best performance the number of row groups should be greater than the number of workers ({bodo.get_size()}). For more details, refer to
https://docs.bodo.ai/latest/file_io/#parquet-section.
"""
                    ))
            if mhfo__tkc == 0:
                ber__jnrf = 0
            else:
                ber__jnrf = oyw__iltfq // mhfo__tkc
            if (bodo.get_rank() == 0 and oyw__iltfq >= 20 * 1048576 and 
                ber__jnrf < 1048576 and protocol in REMOTE_FILESYSTEMS):
                warnings.warn(BodoWarning(
                    f'Parquet average row group size is small ({ber__jnrf} bytes) and can have negative impact on performance when reading from remote sources'
                    ))
            if tracing.is_tracing():
                wwp__apgop.add_attribute('g_total_num_row_groups', mhfo__tkc)
                wwp__apgop.add_attribute('total_scan_time', dqul__kod)
                ckvks__trak = np.array([chwl__fxb._bodo_num_rows for
                    chwl__fxb in tnpyn__cqls.pieces])
                zuwi__nwi = np.percentile(ckvks__trak, [25, 50, 75])
                wwp__apgop.add_attribute('g_row_counts_min', ckvks__trak.min())
                wwp__apgop.add_attribute('g_row_counts_Q1', zuwi__nwi[0])
                wwp__apgop.add_attribute('g_row_counts_median', zuwi__nwi[1])
                wwp__apgop.add_attribute('g_row_counts_Q3', zuwi__nwi[2])
                wwp__apgop.add_attribute('g_row_counts_max', ckvks__trak.max())
                wwp__apgop.add_attribute('g_row_counts_mean', ckvks__trak.
                    mean())
                wwp__apgop.add_attribute('g_row_counts_std', ckvks__trak.std())
                wwp__apgop.add_attribute('g_row_counts_sum', ckvks__trak.sum())
                wwp__apgop.finalize()
    tnpyn__cqls._prefix = ''
    if protocol in {'hdfs', 'abfs', 'abfss'}:
        prefix = f'{protocol}://{easky__pok.netloc}'
        if len(tnpyn__cqls.pieces) > 0:
            bydif__xhw = tnpyn__cqls.pieces[0]
            if not bydif__xhw.path.startswith(prefix):
                tnpyn__cqls._prefix = prefix
    if read_categories:
        _add_categories_to_pq_dataset(tnpyn__cqls)
    if get_row_counts:
        zofw__iovxg.finalize()
    if pio__mqsfd and is_parallel:
        if tracing.is_tracing():
            iqmm__cgicy = tracing.Event('unify_schemas_across_ranks')
        wijgt__bwdp = None
        try:
            fjw__yjbzk = nlkc__rvad.allreduce(fjw__yjbzk, bodo.io.helpers.
                pa_schema_unify_mpi_op)
        except Exception as ftd__azh:
            wijgt__bwdp = ftd__azh
        if tracing.is_tracing():
            iqmm__cgicy.finalize()
        if nlkc__rvad.allreduce(wijgt__bwdp is not None, op=MPI.LOR):
            for wijgt__bwdp in nlkc__rvad.allgather(wijgt__bwdp):
                if wijgt__bwdp:
                    tlyiv__pbrc = (
                        f'Schema in some files were different.\n' + str(
                        wijgt__bwdp))
                    raise BodoError(tlyiv__pbrc)
    tnpyn__cqls._bodo_arrow_schema = fjw__yjbzk
    return tnpyn__cqls


def get_scanner_batches(fpaths, expr_filters, selected_fields,
    avg_num_pieces, is_parallel, storage_options, region, prefix,
    str_as_dict_cols, start_offset, rows_to_read, has_partitions, schema):
    import pyarrow as pa
    cgr__ftofe = os.cpu_count()
    if cgr__ftofe is None or cgr__ftofe == 0:
        cgr__ftofe = 2
    losgl__brg = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), cgr__ftofe)
    npf__axwi = min(int(os.environ.get('BODO_MAX_IO_THREADS', 16)), cgr__ftofe)
    if is_parallel and len(fpaths) > npf__axwi and len(fpaths
        ) / avg_num_pieces >= 2.0:
        pa.set_io_thread_count(npf__axwi)
        pa.set_cpu_count(npf__axwi)
    else:
        pa.set_io_thread_count(losgl__brg)
        pa.set_cpu_count(losgl__brg)
    if fpaths[0].startswith('s3://'):
        wec__oenqc = urlparse(fpaths[0]).netloc
        prefix = 's3://' + wec__oenqc + '/'
        fpaths = [qon__dkzec[len(prefix):] for qon__dkzec in fpaths]
        if region == '':
            region = get_s3_bucket_region_njit(fpaths[0], parallel=False)
        ueoi__xeti = get_s3_subtree_fs(wec__oenqc, region=region,
            storage_options=storage_options)
    elif prefix and prefix.startswith(('hdfs', 'abfs', 'abfss')):
        ueoi__xeti = get_hdfs_fs(prefix + fpaths[0])
    elif fpaths[0].startswith(('gcs', 'gs')):
        import gcsfs
        ueoi__xeti = gcsfs.GCSFileSystem(token=None)
    else:
        ueoi__xeti = None
    xrb__wrwz = ds.ParquetFileFormat(dictionary_columns=str_as_dict_cols)
    tnpyn__cqls = ds.dataset(fpaths, filesystem=ueoi__xeti, partitioning=ds
        .partitioning(flavor='hive') if has_partitions else None, format=
        xrb__wrwz)
    sghxc__dmw = set(str_as_dict_cols)
    rjna__npvft = schema.names
    for ked__susus, name in enumerate(rjna__npvft):
        if name in sghxc__dmw:
            cfbzo__dik = schema.field(ked__susus)
            azswo__yqri = pa.field(name, pa.dictionary(pa.int32(),
                cfbzo__dik.type), cfbzo__dik.nullable)
            schema = schema.remove(ked__susus).insert(ked__susus, azswo__yqri)
    tnpyn__cqls = tnpyn__cqls.replace_schema(pa.unify_schemas([tnpyn__cqls.
        schema, schema]))
    col_names = tnpyn__cqls.schema.names
    nzu__wzl = [col_names[bek__wfs] for bek__wfs in selected_fields]
    heie__wlr = len(fpaths) <= 3 or start_offset > 0 and len(fpaths) <= 10
    if heie__wlr and expr_filters is None:
        dpzru__jvfbx = []
        zzf__pgcg = 0
        pzda__acgx = 0
        for qmw__obg in tnpyn__cqls.get_fragments():
            vnaa__phadr = []
            for scn__czrp in qmw__obg.row_groups:
                txqhc__ffs = scn__czrp.num_rows
                if start_offset < zzf__pgcg + txqhc__ffs:
                    if pzda__acgx == 0:
                        fnpzx__lfjk = start_offset - zzf__pgcg
                        cmfls__oaura = min(txqhc__ffs - fnpzx__lfjk,
                            rows_to_read)
                    else:
                        cmfls__oaura = min(txqhc__ffs, rows_to_read -
                            pzda__acgx)
                    pzda__acgx += cmfls__oaura
                    vnaa__phadr.append(scn__czrp.id)
                zzf__pgcg += txqhc__ffs
                if pzda__acgx == rows_to_read:
                    break
            dpzru__jvfbx.append(qmw__obg.subset(row_group_ids=vnaa__phadr))
            if pzda__acgx == rows_to_read:
                break
        tnpyn__cqls = ds.FileSystemDataset(dpzru__jvfbx, tnpyn__cqls.schema,
            xrb__wrwz, filesystem=tnpyn__cqls.filesystem)
        start_offset = fnpzx__lfjk
    ywo__hvzvc = tnpyn__cqls.scanner(columns=nzu__wzl, filter=expr_filters,
        use_threads=True).to_reader()
    return tnpyn__cqls, ywo__hvzvc, start_offset


def _add_categories_to_pq_dataset(pq_dataset):
    import pyarrow as pa
    from mpi4py import MPI
    if len(pq_dataset.pieces) < 1:
        raise BodoError(
            'No pieces found in Parquet dataset. Cannot get read categorical values'
            )
    pa_schema = pq_dataset.schema.to_arrow_schema()
    gepe__axlh = [c for c in pa_schema.names if isinstance(pa_schema.field(
        c).type, pa.DictionaryType)]
    if len(gepe__axlh) == 0:
        pq_dataset._category_info = {}
        return
    nlkc__rvad = MPI.COMM_WORLD
    if bodo.get_rank() == 0:
        try:
            sncxr__twhzv = pq_dataset.pieces[0].open()
            scn__czrp = sncxr__twhzv.read_row_group(0, gepe__axlh)
            category_info = {c: tuple(scn__czrp.column(c).chunk(0).
                dictionary.to_pylist()) for c in gepe__axlh}
            del sncxr__twhzv, scn__czrp
        except Exception as ftd__azh:
            nlkc__rvad.bcast(ftd__azh)
            raise ftd__azh
        nlkc__rvad.bcast(category_info)
    else:
        category_info = nlkc__rvad.bcast(None)
        if isinstance(category_info, Exception):
            wijgt__bwdp = category_info
            raise wijgt__bwdp
    pq_dataset._category_info = category_info


def get_pandas_metadata(schema, num_pieces):
    pxkuh__quy = None
    nullable_from_metadata = defaultdict(lambda : None)
    lngj__jua = b'pandas'
    if schema.metadata is not None and lngj__jua in schema.metadata:
        import json
        alekb__hwu = json.loads(schema.metadata[lngj__jua].decode('utf8'))
        gzyb__niud = len(alekb__hwu['index_columns'])
        if gzyb__niud > 1:
            raise BodoError('read_parquet: MultiIndex not supported yet')
        pxkuh__quy = alekb__hwu['index_columns'][0] if gzyb__niud else None
        if not isinstance(pxkuh__quy, str) and not isinstance(pxkuh__quy, dict
            ):
            pxkuh__quy = None
        for ahzpr__jxs in alekb__hwu['columns']:
            xgdwr__kee = ahzpr__jxs['name']
            if ahzpr__jxs['pandas_type'].startswith('int'
                ) and xgdwr__kee is not None:
                if ahzpr__jxs['numpy_type'].startswith('Int'):
                    nullable_from_metadata[xgdwr__kee] = True
                else:
                    nullable_from_metadata[xgdwr__kee] = False
    return pxkuh__quy, nullable_from_metadata


def get_str_columns_from_pa_schema(pa_schema):
    str_columns = []
    for xgdwr__kee in pa_schema.names:
        qqlx__guz = pa_schema.field(xgdwr__kee)
        if qqlx__guz.type == pa.string():
            str_columns.append(xgdwr__kee)
    return str_columns


def determine_str_as_dict_columns(pq_dataset, pa_schema, str_columns):
    from mpi4py import MPI
    nlkc__rvad = MPI.COMM_WORLD
    if len(str_columns) == 0:
        return set()
    if len(pq_dataset.pieces) > bodo.get_size():
        import random
        random.seed(37)
        hfs__dgf = random.sample(pq_dataset.pieces, bodo.get_size())
    else:
        hfs__dgf = pq_dataset.pieces
    ogtln__kmmid = np.zeros(len(str_columns), dtype=np.int64)
    vdm__iaqmy = np.zeros(len(str_columns), dtype=np.int64)
    if bodo.get_rank() < len(hfs__dgf):
        bydif__xhw = hfs__dgf[bodo.get_rank()]
        try:
            rcwk__ovgf = bydif__xhw.get_metadata()
            for ked__susus in range(rcwk__ovgf.num_row_groups):
                for srdnl__izaw, xgdwr__kee in enumerate(str_columns):
                    ajn__wblt = pa_schema.get_field_index(xgdwr__kee)
                    ogtln__kmmid[srdnl__izaw] += rcwk__ovgf.row_group(
                        ked__susus).column(ajn__wblt).total_uncompressed_size
            ngp__ote = rcwk__ovgf.num_rows
        except Exception as ftd__azh:
            if isinstance(ftd__azh, (OSError, FileNotFoundError)):
                ngp__ote = 0
            else:
                raise
    else:
        ngp__ote = 0
    xar__rzm = nlkc__rvad.allreduce(ngp__ote, op=MPI.SUM)
    if xar__rzm == 0:
        return set()
    nlkc__rvad.Allreduce(ogtln__kmmid, vdm__iaqmy, op=MPI.SUM)
    hgag__idw = vdm__iaqmy / xar__rzm
    str_as_dict = set()
    for ked__susus, utiwe__uvgyg in enumerate(hgag__idw):
        if utiwe__uvgyg < READ_STR_AS_DICT_THRESHOLD:
            xgdwr__kee = str_columns[ked__susus][0]
            str_as_dict.add(xgdwr__kee)
    return str_as_dict


def parquet_file_schema(file_name, selected_columns, storage_options=None,
    input_file_name_col=None, read_as_dict_cols=None):
    col_names = []
    hxmg__hfump = []
    pq_dataset = get_parquet_dataset(file_name, get_row_counts=False,
        storage_options=storage_options, read_categories=True)
    if hasattr(pq_dataset, '_bodo_arrow_schema'):
        pa_schema = pq_dataset._bodo_arrow_schema
    else:
        pa_schema = pq_dataset.schema.to_arrow_schema()
    partition_names = [] if pq_dataset.partitions is None else [pq_dataset.
        partitions.levels[ked__susus].name for ked__susus in range(len(
        pq_dataset.partitions.partition_names))]
    num_pieces = len(pq_dataset.pieces)
    str_columns = get_str_columns_from_pa_schema(pa_schema)
    ujogm__sve = set(str_columns)
    if read_as_dict_cols is None:
        read_as_dict_cols = []
    read_as_dict_cols = set(read_as_dict_cols)
    walrq__ejms = read_as_dict_cols - ujogm__sve
    if len(walrq__ejms) > 0:
        if bodo.get_rank() == 0:
            warnings.warn(
                f'The following columns are not of datatype string and hence cannot be read with dictionary encoding: {walrq__ejms}'
                , bodo.utils.typing.BodoWarning)
    read_as_dict_cols.intersection_update(ujogm__sve)
    ujogm__sve = ujogm__sve - read_as_dict_cols
    str_columns = [rxg__qnrse for rxg__qnrse in str_columns if rxg__qnrse in
        ujogm__sve]
    str_as_dict: set = determine_str_as_dict_columns(pq_dataset, pa_schema,
        str_columns)
    str_as_dict.update(read_as_dict_cols)
    col_names = pa_schema.names
    pxkuh__quy, nullable_from_metadata = get_pandas_metadata(pa_schema,
        num_pieces)
    becd__unmck = []
    cju__pnvxu = []
    uxfd__cwqu = []
    for ked__susus, c in enumerate(col_names):
        qqlx__guz = pa_schema.field(c)
        nbpy__exjxs, erres__glw = _get_numba_typ_from_pa_typ(qqlx__guz, c ==
            pxkuh__quy, nullable_from_metadata[c], pq_dataset.
            _category_info, str_as_dict=c in str_as_dict)
        becd__unmck.append(nbpy__exjxs)
        cju__pnvxu.append(erres__glw)
        uxfd__cwqu.append(qqlx__guz.type)
    if partition_names:
        col_names += partition_names
        becd__unmck += [_get_partition_cat_dtype(pq_dataset.partitions.
            levels[ked__susus]) for ked__susus in range(len(partition_names))]
        cju__pnvxu.extend([True] * len(partition_names))
        uxfd__cwqu.extend([None] * len(partition_names))
    if input_file_name_col is not None:
        col_names += [input_file_name_col]
        becd__unmck += [dict_str_arr_type]
        cju__pnvxu.append(True)
        uxfd__cwqu.append(None)
    jsskv__xiazi = {c: ked__susus for ked__susus, c in enumerate(col_names)}
    if selected_columns is None:
        selected_columns = col_names
    for c in selected_columns:
        if c not in jsskv__xiazi:
            raise BodoError(f'Selected column {c} not in Parquet file schema')
    if pxkuh__quy and not isinstance(pxkuh__quy, dict
        ) and pxkuh__quy not in selected_columns:
        selected_columns.append(pxkuh__quy)
    col_names = selected_columns
    col_indices = []
    hxmg__hfump = []
    dzhlt__otgld = []
    leh__ujty = []
    for ked__susus, c in enumerate(col_names):
        mees__ped = jsskv__xiazi[c]
        col_indices.append(mees__ped)
        hxmg__hfump.append(becd__unmck[mees__ped])
        if not cju__pnvxu[mees__ped]:
            dzhlt__otgld.append(ked__susus)
            leh__ujty.append(uxfd__cwqu[mees__ped])
    return (col_names, hxmg__hfump, pxkuh__quy, col_indices,
        partition_names, dzhlt__otgld, leh__ujty)


def _get_partition_cat_dtype(part_set):
    oys__hyae = part_set.dictionary.to_pandas()
    vqvy__ppok = bodo.typeof(oys__hyae).dtype
    hvsvo__gofdj = PDCategoricalDtype(tuple(oys__hyae), vqvy__ppok, False)
    return CategoricalArrayType(hvsvo__gofdj)


_pq_read = types.ExternalFunction('pq_read', table_type(
    read_parquet_fpath_type, types.boolean, types.voidptr,
    parquet_predicate_type, parquet_predicate_type,
    storage_options_dict_type, types.int64, types.voidptr, types.int32,
    types.voidptr, types.voidptr, types.voidptr, types.int32, types.voidptr,
    types.int32, types.voidptr, types.boolean))
from llvmlite import ir as lir
from numba.core import cgutils
if bodo.utils.utils.has_pyarrow():
    from bodo.io import arrow_cpp
    ll.add_symbol('pq_read', arrow_cpp.pq_read)
    ll.add_symbol('pq_write', arrow_cpp.pq_write)
    ll.add_symbol('pq_write_partitioned', arrow_cpp.pq_write_partitioned)


@intrinsic
def parquet_write_table_cpp(typingctx, filename_t, table_t, col_names_t,
    index_t, write_index, metadata_t, compression_t, is_parallel_t,
    write_range_index, start, stop, step, name, bucket_region, row_group_size):

    def codegen(context, builder, sig, args):
        hugen__vqooi = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(32), lir.IntType(32),
            lir.IntType(32), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        fvtwo__uvtm = cgutils.get_or_insert_function(builder.module,
            hugen__vqooi, name='pq_write')
        builder.call(fvtwo__uvtm, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
    return types.void(types.voidptr, table_t, col_names_t, index_t, types.
        boolean, types.voidptr, types.voidptr, types.boolean, types.boolean,
        types.int32, types.int32, types.int32, types.voidptr, types.voidptr,
        types.int64), codegen


@intrinsic
def parquet_write_table_partitioned_cpp(typingctx, filename_t, data_table_t,
    col_names_t, col_names_no_partitions_t, cat_table_t, part_col_idxs_t,
    num_part_col_t, compression_t, is_parallel_t, bucket_region, row_group_size
    ):

    def codegen(context, builder, sig, args):
        hugen__vqooi = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        fvtwo__uvtm = cgutils.get_or_insert_function(builder.module,
            hugen__vqooi, name='pq_write_partitioned')
        builder.call(fvtwo__uvtm, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
    return types.void(types.voidptr, data_table_t, col_names_t,
        col_names_no_partitions_t, cat_table_t, types.voidptr, types.int32,
        types.voidptr, types.boolean, types.voidptr, types.int64), codegen
