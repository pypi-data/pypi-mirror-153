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
        except OSError as mrxt__qnvk:
            if 'non-file path' in str(mrxt__qnvk):
                raise FileNotFoundError(str(mrxt__qnvk))
            raise


class ParquetHandler:

    def __init__(self, func_ir, typingctx, args, _locals):
        self.func_ir = func_ir
        self.typingctx = typingctx
        self.args = args
        self.locals = _locals

    def gen_parquet_read(self, file_name, lhs, columns, storage_options=
        None, input_file_name_col=None, read_as_dict_cols=None):
        dej__addx = lhs.scope
        lupa__odwkw = lhs.loc
        bxpth__omqtm = None
        if lhs.name in self.locals:
            bxpth__omqtm = self.locals[lhs.name]
            self.locals.pop(lhs.name)
        kdb__nsvl = {}
        if lhs.name + ':convert' in self.locals:
            kdb__nsvl = self.locals[lhs.name + ':convert']
            self.locals.pop(lhs.name + ':convert')
        if bxpth__omqtm is None:
            qbdu__jiovi = (
                'Parquet schema not available. Either path argument should be constant for Bodo to look at the file at compile time or schema should be provided. For more information, see: https://docs.bodo.ai/latest/file_io/#parquet-section.'
                )
            vyxen__dom = get_const_value(file_name, self.func_ir,
                qbdu__jiovi, arg_types=self.args, file_info=ParquetFileInfo
                (columns, storage_options=storage_options,
                input_file_name_col=input_file_name_col, read_as_dict_cols=
                read_as_dict_cols))
            tguw__tsxj = False
            sbxlu__utbc = guard(get_definition, self.func_ir, file_name)
            if isinstance(sbxlu__utbc, ir.Arg):
                typ = self.args[sbxlu__utbc.index]
                if isinstance(typ, types.FilenameType):
                    (col_names, lnurp__qkqio, lstgg__qpm, col_indices,
                        partition_names, fwyp__uvwdj, ngt__zgr) = typ.schema
                    tguw__tsxj = True
            if not tguw__tsxj:
                (col_names, lnurp__qkqio, lstgg__qpm, col_indices,
                    partition_names, fwyp__uvwdj, ngt__zgr) = (
                    parquet_file_schema(vyxen__dom, columns,
                    storage_options=storage_options, input_file_name_col=
                    input_file_name_col, read_as_dict_cols=read_as_dict_cols))
        else:
            szm__pszyl = list(bxpth__omqtm.keys())
            djmjc__mqiw = {c: ofjfd__lekgh for ofjfd__lekgh, c in enumerate
                (szm__pszyl)}
            zjekn__chj = [tdgn__ybz for tdgn__ybz in bxpth__omqtm.values()]
            lstgg__qpm = 'index' if 'index' in djmjc__mqiw else None
            if columns is None:
                selected_columns = szm__pszyl
            else:
                selected_columns = columns
            col_indices = [djmjc__mqiw[c] for c in selected_columns]
            lnurp__qkqio = [zjekn__chj[djmjc__mqiw[c]] for c in
                selected_columns]
            col_names = selected_columns
            lstgg__qpm = lstgg__qpm if lstgg__qpm in col_names else None
            partition_names = []
            fwyp__uvwdj = []
            ngt__zgr = []
        nsry__ygg = None if isinstance(lstgg__qpm, dict
            ) or lstgg__qpm is None else lstgg__qpm
        index_column_index = None
        index_column_type = types.none
        if nsry__ygg:
            twidn__yxrcj = col_names.index(nsry__ygg)
            index_column_index = col_indices.pop(twidn__yxrcj)
            index_column_type = lnurp__qkqio.pop(twidn__yxrcj)
            col_names.pop(twidn__yxrcj)
        for ofjfd__lekgh, c in enumerate(col_names):
            if c in kdb__nsvl:
                lnurp__qkqio[ofjfd__lekgh] = kdb__nsvl[c]
        hky__tlgql = [ir.Var(dej__addx, mk_unique_var('pq_table'),
            lupa__odwkw), ir.Var(dej__addx, mk_unique_var('pq_index'),
            lupa__odwkw)]
        ahz__yvmst = [bodo.ir.parquet_ext.ParquetReader(file_name, lhs.name,
            col_names, col_indices, lnurp__qkqio, hky__tlgql, lupa__odwkw,
            partition_names, storage_options, index_column_index,
            index_column_type, input_file_name_col, fwyp__uvwdj, ngt__zgr)]
        return (col_names, hky__tlgql, lstgg__qpm, ahz__yvmst, lnurp__qkqio,
            index_column_type)


def pq_distributed_run(pq_node, array_dists, typemap, calltypes, typingctx,
    targetctx, meta_head_only_info=None):
    urdf__xdhs = len(pq_node.out_vars)
    dnf_filter_str = 'None'
    expr_filter_str = 'None'
    ter__gnoy, pshlm__pzeso = bodo.ir.connector.generate_filter_map(pq_node
        .filters)
    extra_args = ', '.join(ter__gnoy.values())
    dnf_filter_str, expr_filter_str = bodo.ir.connector.generate_arrow_filters(
        pq_node.filters, ter__gnoy, pshlm__pzeso, pq_node.
        original_df_colnames, pq_node.partition_names, pq_node.
        original_out_types, typemap, 'parquet')
    wqubu__uxbq = ', '.join(f'out{ofjfd__lekgh}' for ofjfd__lekgh in range(
        urdf__xdhs))
    zywfh__qzk = f'def pq_impl(fname, {extra_args}):\n'
    zywfh__qzk += (
        f'    (total_rows, {wqubu__uxbq},) = _pq_reader_py(fname, {extra_args})\n'
        )
    udcua__znx = {}
    exec(zywfh__qzk, {}, udcua__znx)
    ujme__rtlq = udcua__znx['pq_impl']
    if bodo.user_logging.get_verbose_level() >= 1:
        ifuv__txcg = pq_node.loc.strformat()
        etw__pda = []
        yjy__tum = []
        for ofjfd__lekgh in pq_node.type_usecol_offset:
            nka__pqnph = pq_node.df_colnames[ofjfd__lekgh]
            etw__pda.append(nka__pqnph)
            if isinstance(pq_node.out_types[ofjfd__lekgh], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                yjy__tum.append(nka__pqnph)
        jhbqw__guyho = (
            'Finish column pruning on read_parquet node:\n%s\nColumns loaded %s\n'
            )
        bodo.user_logging.log_message('Column Pruning', jhbqw__guyho,
            ifuv__txcg, etw__pda)
        if yjy__tum:
            wcth__qey = """Finished optimized encoding on read_parquet node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', wcth__qey,
                ifuv__txcg, yjy__tum)
    parallel = bodo.ir.connector.is_connector_table_parallel(pq_node,
        array_dists, typemap, 'ParquetReader')
    if pq_node.unsupported_columns:
        vtexx__zupf = set(pq_node.type_usecol_offset)
        ngsql__cspq = set(pq_node.unsupported_columns)
        pvluv__utv = vtexx__zupf & ngsql__cspq
        if pvluv__utv:
            qiexf__xmiz = sorted(pvluv__utv)
            dbny__dfw = [
                f'pandas.read_parquet(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                "Please manually remove these columns from your read_parquet with the 'columns' argument. If these "
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            zbglo__hgswe = 0
            for vpbxd__jch in qiexf__xmiz:
                while pq_node.unsupported_columns[zbglo__hgswe] != vpbxd__jch:
                    zbglo__hgswe += 1
                dbny__dfw.append(
                    f"Column '{pq_node.df_colnames[vpbxd__jch]}' with unsupported arrow type {pq_node.unsupported_arrow_types[zbglo__hgswe]}"
                    )
                zbglo__hgswe += 1
            fxenl__uhz = '\n'.join(dbny__dfw)
            raise BodoError(fxenl__uhz, loc=pq_node.loc)
    pias__onw = _gen_pq_reader_py(pq_node.df_colnames, pq_node.col_indices,
        pq_node.type_usecol_offset, pq_node.out_types, pq_node.
        storage_options, pq_node.partition_names, dnf_filter_str,
        expr_filter_str, extra_args, parallel, meta_head_only_info, pq_node
        .index_column_index, pq_node.index_column_type, pq_node.
        input_file_name_col)
    xbt__omg = typemap[pq_node.file_name.name]
    pmcg__xfozf = (xbt__omg,) + tuple(typemap[hox__tei.name] for hox__tei in
        pshlm__pzeso)
    pyp__tce = compile_to_numba_ir(ujme__rtlq, {'_pq_reader_py': pias__onw},
        typingctx=typingctx, targetctx=targetctx, arg_typs=pmcg__xfozf,
        typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(pyp__tce, [pq_node.file_name] + pshlm__pzeso)
    ahz__yvmst = pyp__tce.body[:-3]
    if meta_head_only_info:
        ahz__yvmst[-1 - urdf__xdhs].target = meta_head_only_info[1]
    ahz__yvmst[-2].target = pq_node.out_vars[0]
    ahz__yvmst[-1].target = pq_node.out_vars[1]
    assert not (pq_node.index_column_index is None and not pq_node.
        type_usecol_offset
        ), 'At most one of table and index should be dead if the Parquet IR node is live'
    if pq_node.index_column_index is None:
        ahz__yvmst.pop(-1)
    elif not pq_node.type_usecol_offset:
        ahz__yvmst.pop(-2)
    return ahz__yvmst


distributed_pass.distributed_run_extensions[bodo.ir.parquet_ext.ParquetReader
    ] = pq_distributed_run


def get_filters_pyobject(dnf_filter_str, expr_filter_str, vars):
    pass


@overload(get_filters_pyobject, no_unliteral=True)
def overload_get_filters_pyobject(dnf_filter_str, expr_filter_str, var_tup):
    pumu__otcs = get_overload_const_str(dnf_filter_str)
    ypw__jjt = get_overload_const_str(expr_filter_str)
    ewi__ummnx = ', '.join(f'f{ofjfd__lekgh}' for ofjfd__lekgh in range(len
        (var_tup)))
    zywfh__qzk = 'def impl(dnf_filter_str, expr_filter_str, var_tup):\n'
    if len(var_tup):
        zywfh__qzk += f'  {ewi__ummnx}, = var_tup\n'
    zywfh__qzk += """  with numba.objmode(dnf_filters_py='parquet_predicate_type', expr_filters_py='parquet_predicate_type'):
"""
    zywfh__qzk += f'    dnf_filters_py = {pumu__otcs}\n'
    zywfh__qzk += f'    expr_filters_py = {ypw__jjt}\n'
    zywfh__qzk += '  return (dnf_filters_py, expr_filters_py)\n'
    udcua__znx = {}
    exec(zywfh__qzk, globals(), udcua__znx)
    return udcua__znx['impl']


@numba.njit
def get_fname_pyobject(fname):
    with numba.objmode(fname_py='read_parquet_fpath_type'):
        fname_py = fname
    return fname_py


def _gen_pq_reader_py(col_names, col_indices, type_usecol_offset, out_types,
    storage_options, partition_names, dnf_filter_str, expr_filter_str,
    extra_args, is_parallel, meta_head_only_info, index_column_index,
    index_column_type, input_file_name_col):
    suet__ugxs = next_label()
    dpkve__fpj = ',' if extra_args else ''
    zywfh__qzk = f'def pq_reader_py(fname,{extra_args}):\n'
    zywfh__qzk += (
        f"    ev = bodo.utils.tracing.Event('read_parquet', {is_parallel})\n")
    zywfh__qzk += f"    ev.add_attribute('g_fname', fname)\n"
    zywfh__qzk += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={is_parallel})
"""
    zywfh__qzk += f"""    dnf_filters, expr_filters = get_filters_pyobject("{dnf_filter_str}", "{expr_filter_str}", ({extra_args}{dpkve__fpj}))
"""
    zywfh__qzk += '    fname_py = get_fname_pyobject(fname)\n'
    storage_options['bodo_dummy'] = 'dummy'
    zywfh__qzk += (
        f'    storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    tot_rows_to_read = -1
    if meta_head_only_info and meta_head_only_info[0] is not None:
        tot_rows_to_read = meta_head_only_info[0]
    syjou__pqs = not type_usecol_offset
    wbfi__yru = [sanitize_varname(c) for c in col_names]
    partition_names = [sanitize_varname(c) for c in partition_names]
    input_file_name_col = sanitize_varname(input_file_name_col
        ) if input_file_name_col is not None and col_names.index(
        input_file_name_col) in type_usecol_offset else None
    efhk__cfev = {c: ofjfd__lekgh for ofjfd__lekgh, c in enumerate(col_indices)
        }
    cgial__tvz = {c: ofjfd__lekgh for ofjfd__lekgh, c in enumerate(wbfi__yru)}
    ywph__pbku = []
    fds__ttb = set()
    rzw__pzfur = partition_names + [input_file_name_col]
    for ofjfd__lekgh in type_usecol_offset:
        if wbfi__yru[ofjfd__lekgh] not in rzw__pzfur:
            ywph__pbku.append(col_indices[ofjfd__lekgh])
        elif not input_file_name_col or wbfi__yru[ofjfd__lekgh
            ] != input_file_name_col:
            fds__ttb.add(col_indices[ofjfd__lekgh])
    if index_column_index is not None:
        ywph__pbku.append(index_column_index)
    ywph__pbku = sorted(ywph__pbku)
    iaver__obg = {c: ofjfd__lekgh for ofjfd__lekgh, c in enumerate(ywph__pbku)}
    eiklt__bfi = [(int(is_nullable(out_types[efhk__cfev[lxmy__gmc]])) if 
        lxmy__gmc != index_column_index else int(is_nullable(
        index_column_type))) for lxmy__gmc in ywph__pbku]
    str_as_dict_cols = []
    for lxmy__gmc in ywph__pbku:
        if lxmy__gmc == index_column_index:
            tdgn__ybz = index_column_type
        else:
            tdgn__ybz = out_types[efhk__cfev[lxmy__gmc]]
        if tdgn__ybz == dict_str_arr_type:
            str_as_dict_cols.append(lxmy__gmc)
    fjq__drev = []
    erpvq__ynyya = {}
    jjecg__ordm = []
    epth__ymz = []
    for ofjfd__lekgh, fxvu__btnlf in enumerate(partition_names):
        try:
            xzqb__jvtjj = cgial__tvz[fxvu__btnlf]
            if col_indices[xzqb__jvtjj] not in fds__ttb:
                continue
        except (KeyError, ValueError) as usn__syuz:
            continue
        erpvq__ynyya[fxvu__btnlf] = len(fjq__drev)
        fjq__drev.append(fxvu__btnlf)
        jjecg__ordm.append(ofjfd__lekgh)
        ixczm__bvu = out_types[xzqb__jvtjj].dtype
        faivs__dezbz = (bodo.hiframes.pd_categorical_ext.
            get_categories_int_type(ixczm__bvu))
        epth__ymz.append(numba_to_c_type(faivs__dezbz))
    zywfh__qzk += f'    total_rows_np = np.array([0], dtype=np.int64)\n'
    zywfh__qzk += f'    out_table = pq_read(\n'
    zywfh__qzk += f'        fname_py, {is_parallel},\n'
    zywfh__qzk += f'        unicode_to_utf8(bucket_region),\n'
    zywfh__qzk += f'        dnf_filters, expr_filters,\n'
    zywfh__qzk += f"""        storage_options_py, {tot_rows_to_read}, selected_cols_arr_{suet__ugxs}.ctypes,
"""
    zywfh__qzk += f'        {len(ywph__pbku)},\n'
    zywfh__qzk += f'        nullable_cols_arr_{suet__ugxs}.ctypes,\n'
    if len(jjecg__ordm) > 0:
        zywfh__qzk += (
            f'        np.array({jjecg__ordm}, dtype=np.int32).ctypes,\n')
        zywfh__qzk += (
            f'        np.array({epth__ymz}, dtype=np.int32).ctypes,\n')
        zywfh__qzk += f'        {len(jjecg__ordm)},\n'
    else:
        zywfh__qzk += f'        0, 0, 0,\n'
    if len(str_as_dict_cols) > 0:
        zywfh__qzk += f"""        np.array({str_as_dict_cols}, dtype=np.int32).ctypes, {len(str_as_dict_cols)},
"""
    else:
        zywfh__qzk += f'        0, 0,\n'
    zywfh__qzk += f'        total_rows_np.ctypes,\n'
    zywfh__qzk += f'        {input_file_name_col is not None},\n'
    zywfh__qzk += f'    )\n'
    zywfh__qzk += f'    check_and_propagate_cpp_exception()\n'
    zosvo__kvbx = 'None'
    ahy__eyah = index_column_type
    sjpx__sjmki = TableType(tuple(out_types))
    if syjou__pqs:
        sjpx__sjmki = types.none
    if index_column_index is not None:
        qwkt__mcseg = iaver__obg[index_column_index]
        zosvo__kvbx = (
            f'info_to_array(info_from_table(out_table, {qwkt__mcseg}), index_arr_type)'
            )
    zywfh__qzk += f'    index_arr = {zosvo__kvbx}\n'
    if syjou__pqs:
        qljoc__oxl = None
    else:
        qljoc__oxl = []
        uqgl__lnyyp = 0
        pxm__noxmr = col_indices[col_names.index(input_file_name_col)
            ] if input_file_name_col is not None else None
        for ofjfd__lekgh, vpbxd__jch in enumerate(col_indices):
            if uqgl__lnyyp < len(type_usecol_offset
                ) and ofjfd__lekgh == type_usecol_offset[uqgl__lnyyp]:
                qtpo__vxk = col_indices[ofjfd__lekgh]
                if pxm__noxmr and qtpo__vxk == pxm__noxmr:
                    qljoc__oxl.append(len(ywph__pbku) + len(fjq__drev))
                elif qtpo__vxk in fds__ttb:
                    epj__njmmo = wbfi__yru[ofjfd__lekgh]
                    qljoc__oxl.append(len(ywph__pbku) + erpvq__ynyya[
                        epj__njmmo])
                else:
                    qljoc__oxl.append(iaver__obg[vpbxd__jch])
                uqgl__lnyyp += 1
            else:
                qljoc__oxl.append(-1)
        qljoc__oxl = np.array(qljoc__oxl, dtype=np.int64)
    if syjou__pqs:
        zywfh__qzk += '    T = None\n'
    else:
        zywfh__qzk += f"""    T = cpp_table_to_py_table(out_table, table_idx_{suet__ugxs}, py_table_type_{suet__ugxs})
"""
    zywfh__qzk += f'    delete_table(out_table)\n'
    zywfh__qzk += f'    total_rows = total_rows_np[0]\n'
    zywfh__qzk += f'    ev.finalize()\n'
    zywfh__qzk += f'    return (total_rows, T, index_arr)\n'
    udcua__znx = {}
    fojh__gobbc = {f'py_table_type_{suet__ugxs}': sjpx__sjmki,
        f'table_idx_{suet__ugxs}': qljoc__oxl,
        f'selected_cols_arr_{suet__ugxs}': np.array(ywph__pbku, np.int32),
        f'nullable_cols_arr_{suet__ugxs}': np.array(eiklt__bfi, np.int32),
        'index_arr_type': ahy__eyah, 'cpp_table_to_py_table':
        cpp_table_to_py_table, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'delete_table': delete_table,
        'check_and_propagate_cpp_exception':
        check_and_propagate_cpp_exception, 'pq_read': _pq_read,
        'unicode_to_utf8': unicode_to_utf8, 'get_filters_pyobject':
        get_filters_pyobject, 'get_storage_options_pyobject':
        get_storage_options_pyobject, 'get_fname_pyobject':
        get_fname_pyobject, 'np': np, 'pd': pd, 'bodo': bodo}
    exec(zywfh__qzk, fojh__gobbc, udcua__znx)
    pias__onw = udcua__znx['pq_reader_py']
    uone__zotzl = numba.njit(pias__onw, no_cpython_wrapper=True)
    return uone__zotzl


import pyarrow as pa
_pa_numba_typ_map = {pa.bool_(): types.bool_, pa.int8(): types.int8, pa.
    int16(): types.int16, pa.int32(): types.int32, pa.int64(): types.int64,
    pa.uint8(): types.uint8, pa.uint16(): types.uint16, pa.uint32(): types.
    uint32, pa.uint64(): types.uint64, pa.float32(): types.float32, pa.
    float64(): types.float64, pa.string(): string_type, pa.binary():
    bytes_type, pa.date32(): datetime_date_type, pa.date64(): types.
    NPDatetime('ns'), null(): string_type}


def get_arrow_timestamp_type(pa_ts_typ):
    oshp__noubn = 'ns', 'us', 'ms', 's'
    if pa_ts_typ.unit not in oshp__noubn:
        return types.Array(bodo.datetime64ns, 1, 'C'), False
    elif pa_ts_typ.tz is not None:
        vdwl__xyvqs = pa_ts_typ.to_pandas_dtype().tz
        pny__fsjot = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(
            vdwl__xyvqs)
        return bodo.DatetimeArrayType(pny__fsjot), True
    else:
        return types.Array(bodo.datetime64ns, 1, 'C'), True


def _get_numba_typ_from_pa_typ(pa_typ, is_index, nullable_from_metadata,
    category_info, str_as_dict=False):
    if isinstance(pa_typ.type, pa.ListType):
        czps__awb, tmbbi__iqe = _get_numba_typ_from_pa_typ(pa_typ.type.
            value_field, is_index, nullable_from_metadata, category_info)
        return ArrayItemArrayType(czps__awb), tmbbi__iqe
    if isinstance(pa_typ.type, pa.StructType):
        xily__noc = []
        hic__zcvvw = []
        tmbbi__iqe = True
        for gbqs__fmpt in pa_typ.flatten():
            hic__zcvvw.append(gbqs__fmpt.name.split('.')[-1])
            cua__vtm, acv__joqv = _get_numba_typ_from_pa_typ(gbqs__fmpt,
                is_index, nullable_from_metadata, category_info)
            xily__noc.append(cua__vtm)
            tmbbi__iqe = tmbbi__iqe and acv__joqv
        return StructArrayType(tuple(xily__noc), tuple(hic__zcvvw)), tmbbi__iqe
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
        etleb__wtbvl = _pa_numba_typ_map[pa_typ.type.index_type]
        zqshf__jmk = PDCategoricalDtype(category_info[pa_typ.name], bodo.
            string_type, pa_typ.type.ordered, int_type=etleb__wtbvl)
        return CategoricalArrayType(zqshf__jmk), True
    if isinstance(pa_typ.type, pa.lib.TimestampType):
        return get_arrow_timestamp_type(pa_typ.type)
    elif pa_typ.type in _pa_numba_typ_map:
        tgr__rwde = _pa_numba_typ_map[pa_typ.type]
        tmbbi__iqe = True
    else:
        raise BodoError('Arrow data type {} not supported yet'.format(
            pa_typ.type))
    if tgr__rwde == datetime_date_type:
        return datetime_date_array_type, tmbbi__iqe
    if tgr__rwde == bytes_type:
        return binary_array_type, tmbbi__iqe
    czps__awb = string_array_type if tgr__rwde == string_type else types.Array(
        tgr__rwde, 1, 'C')
    if tgr__rwde == types.bool_:
        czps__awb = boolean_array
    if nullable_from_metadata is not None:
        fitjx__fvf = nullable_from_metadata
    else:
        fitjx__fvf = use_nullable_int_arr
    if fitjx__fvf and not is_index and isinstance(tgr__rwde, types.Integer
        ) and pa_typ.nullable:
        czps__awb = IntegerArrayType(tgr__rwde)
    return czps__awb, tmbbi__iqe


def get_parquet_dataset(fpath, get_row_counts=True, dnf_filters=None,
    expr_filters=None, storage_options=None, read_categories=False,
    is_parallel=False, tot_rows_to_read=None, typing_pa_schema=None):
    if get_row_counts:
        mddo__wxej = tracing.Event('get_parquet_dataset')
    import time
    import pyarrow as pa
    import pyarrow.parquet as pq
    from mpi4py import MPI
    ahxq__dzcvc = MPI.COMM_WORLD
    if isinstance(fpath, list):
        tejxq__vcg = urlparse(fpath[0])
        protocol = tejxq__vcg.scheme
        rxyrg__oejyi = tejxq__vcg.netloc
        for ofjfd__lekgh in range(len(fpath)):
            ojhkg__nepz = fpath[ofjfd__lekgh]
            ldfxm__cins = urlparse(ojhkg__nepz)
            if ldfxm__cins.scheme != protocol:
                raise BodoError(
                    'All parquet files must use the same filesystem protocol')
            if ldfxm__cins.netloc != rxyrg__oejyi:
                raise BodoError(
                    'All parquet files must be in the same S3 bucket')
            fpath[ofjfd__lekgh] = ojhkg__nepz.rstrip('/')
    else:
        tejxq__vcg = urlparse(fpath)
        protocol = tejxq__vcg.scheme
        fpath = fpath.rstrip('/')
    if protocol in {'gcs', 'gs'}:
        try:
            import gcsfs
        except ImportError as usn__syuz:
            hsv__cfatv = """Couldn't import gcsfs, which is required for Google cloud access. gcsfs can be installed by calling 'conda install -c conda-forge gcsfs'.
"""
            raise BodoError(hsv__cfatv)
    if protocol == 'http':
        try:
            import fsspec
        except ImportError as usn__syuz:
            hsv__cfatv = """Couldn't import fsspec, which is required for http access. fsspec can be installed by calling 'conda install -c conda-forge fsspec'.
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
            aaikj__zie = gcsfs.GCSFileSystem(token=None)
            fs.append(aaikj__zie)
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
                prefix = f'{protocol}://{tejxq__vcg.netloc}'
                path = path[len(prefix):]
            prxud__pky = fs.glob(path)
            if protocol == 's3':
                prxud__pky = [('s3://' + ojhkg__nepz) for ojhkg__nepz in
                    prxud__pky if not ojhkg__nepz.startswith('s3://')]
            elif protocol in {'hdfs', 'abfs', 'abfss'}:
                prxud__pky = [(prefix + ojhkg__nepz) for ojhkg__nepz in
                    prxud__pky]
        except:
            raise BodoError(
                f'glob pattern expansion not supported for {protocol}')
        if len(prxud__pky) == 0:
            raise BodoError('No files found matching glob pattern')
        return prxud__pky
    grdca__mstvm = False
    if get_row_counts:
        fht__jts = getfs(parallel=True)
        grdca__mstvm = bodo.parquet_validate_schema
    if bodo.get_rank() == 0:
        uvgli__fwo = 1
        iqak__iiu = os.cpu_count()
        if iqak__iiu is not None and iqak__iiu > 1:
            uvgli__fwo = iqak__iiu // 2
        try:
            if get_row_counts:
                svo__wvrpx = tracing.Event('pq.ParquetDataset', is_parallel
                    =False)
                if tracing.is_tracing():
                    svo__wvrpx.add_attribute('g_dnf_filter', str(dnf_filters))
            kps__yafjf = pa.io_thread_count()
            pa.set_io_thread_count(uvgli__fwo)
            if isinstance(fpath, list):
                rzib__ala = []
                for voa__toh in fpath:
                    if has_magic(voa__toh):
                        rzib__ala += glob(protocol, getfs(), voa__toh)
                    else:
                        rzib__ala.append(voa__toh)
                fpath = rzib__ala
            elif has_magic(fpath):
                fpath = glob(protocol, getfs(), fpath)
            if protocol == 's3':
                if isinstance(fpath, list):
                    get_legacy_fs().info(fpath[0])
                else:
                    get_legacy_fs().info(fpath)
            if protocol in {'hdfs', 'abfs', 'abfss'}:
                prefix = f'{protocol}://{tejxq__vcg.netloc}'
                if isinstance(fpath, list):
                    llz__gqjp = [ojhkg__nepz[len(prefix):] for ojhkg__nepz in
                        fpath]
                else:
                    llz__gqjp = fpath[len(prefix):]
            else:
                llz__gqjp = fpath
            nfl__mejat = pq.ParquetDataset(llz__gqjp, filesystem=
                get_legacy_fs(), filters=None, use_legacy_dataset=True,
                validate_schema=False, metadata_nthreads=uvgli__fwo)
            pa.set_io_thread_count(kps__yafjf)
            if typing_pa_schema:
                titiw__wgndm = typing_pa_schema
            else:
                titiw__wgndm = bodo.io.pa_parquet.get_dataset_schema(nfl__mejat
                    )
            if dnf_filters:
                if get_row_counts:
                    svo__wvrpx.add_attribute('num_pieces_before_filter',
                        len(nfl__mejat.pieces))
                chu__zji = time.time()
                nfl__mejat._filter(dnf_filters)
                if get_row_counts:
                    svo__wvrpx.add_attribute('dnf_filter_time', time.time() -
                        chu__zji)
                    svo__wvrpx.add_attribute('num_pieces_after_filter', len
                        (nfl__mejat.pieces))
            if get_row_counts:
                svo__wvrpx.finalize()
            nfl__mejat._metadata.fs = None
        except Exception as mrxt__qnvk:
            if isinstance(fpath, list) and isinstance(mrxt__qnvk, (OSError,
                FileNotFoundError)):
                mrxt__qnvk = BodoError(str(mrxt__qnvk) +
                    list_of_files_error_msg)
            else:
                mrxt__qnvk = BodoError(
                    f"""error from pyarrow: {type(mrxt__qnvk).__name__}: {str(mrxt__qnvk)}
"""
                    )
            ahxq__dzcvc.bcast(mrxt__qnvk)
            raise mrxt__qnvk
        if get_row_counts:
            fidpp__cwxb = tracing.Event('bcast dataset')
        ahxq__dzcvc.bcast(nfl__mejat)
        ahxq__dzcvc.bcast(titiw__wgndm)
    else:
        if get_row_counts:
            fidpp__cwxb = tracing.Event('bcast dataset')
        nfl__mejat = ahxq__dzcvc.bcast(None)
        if isinstance(nfl__mejat, Exception):
            jktb__nyftv = nfl__mejat
            raise jktb__nyftv
        titiw__wgndm = ahxq__dzcvc.bcast(None)
    tskae__rntoq = set(titiw__wgndm.names)
    if get_row_counts:
        gylvj__ntu = getfs()
    else:
        gylvj__ntu = get_legacy_fs()
    nfl__mejat._metadata.fs = gylvj__ntu
    if get_row_counts:
        fidpp__cwxb.finalize()
    nfl__mejat._bodo_total_rows = 0
    if get_row_counts and tot_rows_to_read == 0:
        get_row_counts = grdca__mstvm = False
        for voa__toh in nfl__mejat.pieces:
            voa__toh._bodo_num_rows = 0
    if get_row_counts or grdca__mstvm:
        if get_row_counts and tracing.is_tracing():
            llf__oft = tracing.Event('get_row_counts')
            llf__oft.add_attribute('g_num_pieces', len(nfl__mejat.pieces))
            llf__oft.add_attribute('g_expr_filters', str(expr_filters))
        mhoe__retkw = 0.0
        num_pieces = len(nfl__mejat.pieces)
        start = get_start(num_pieces, bodo.get_size(), bodo.get_rank())
        mcjkd__irmy = get_end(num_pieces, bodo.get_size(), bodo.get_rank())
        gax__kqbf = 0
        mom__jqole = 0
        rvp__bbv = 0
        abxfz__ngj = True
        if expr_filters is not None:
            import random
            random.seed(37)
            ktz__ojfr = random.sample(nfl__mejat.pieces, k=len(nfl__mejat.
                pieces))
        else:
            ktz__ojfr = nfl__mejat.pieces
        for voa__toh in ktz__ojfr:
            voa__toh._bodo_num_rows = 0
        fpaths = [voa__toh.path for voa__toh in ktz__ojfr[start:mcjkd__irmy]]
        if protocol == 's3':
            rxyrg__oejyi = tejxq__vcg.netloc
            prefix = 's3://' + rxyrg__oejyi + '/'
            fpaths = [ojhkg__nepz[len(prefix):] for ojhkg__nepz in fpaths]
            gylvj__ntu = get_s3_subtree_fs(rxyrg__oejyi, region=getfs().
                region, storage_options=storage_options)
        else:
            gylvj__ntu = getfs()
        uvgli__fwo = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), 4)
        pa.set_io_thread_count(uvgli__fwo)
        pa.set_cpu_count(uvgli__fwo)
        jktb__nyftv = None
        try:
            ivqig__uevon = ds.dataset(fpaths, filesystem=gylvj__ntu,
                partitioning=ds.partitioning(flavor='hive') if nfl__mejat.
                partitions else None)
            for oodc__ehia, tfi__yevb in zip(ktz__ojfr[start:mcjkd__irmy],
                ivqig__uevon.get_fragments()):
                if grdca__mstvm:
                    rmea__kgwta = tfi__yevb.metadata.schema.to_arrow_schema()
                    kdg__alco = set(rmea__kgwta.names)
                    if tskae__rntoq != kdg__alco:
                        hiqp__uesg = kdg__alco - tskae__rntoq
                        mlfmy__przh = tskae__rntoq - kdg__alco
                        qbdu__jiovi = (
                            f'Schema in {oodc__ehia} was different.\n')
                        if hiqp__uesg:
                            qbdu__jiovi += f"""File contains column(s) {hiqp__uesg} not found in other files in the dataset.
"""
                        if mlfmy__przh:
                            qbdu__jiovi += f"""File missing column(s) {mlfmy__przh} found in other files in the dataset.
"""
                        raise BodoError(qbdu__jiovi)
                    try:
                        titiw__wgndm = pa.unify_schemas([titiw__wgndm,
                            rmea__kgwta])
                    except Exception as mrxt__qnvk:
                        qbdu__jiovi = (
                            f'Schema in {oodc__ehia} was different.\n' +
                            str(mrxt__qnvk))
                        raise BodoError(qbdu__jiovi)
                chu__zji = time.time()
                ylr__qigg = tfi__yevb.scanner(schema=ivqig__uevon.schema,
                    filter=expr_filters, use_threads=True).count_rows()
                mhoe__retkw += time.time() - chu__zji
                oodc__ehia._bodo_num_rows = ylr__qigg
                gax__kqbf += ylr__qigg
                mom__jqole += tfi__yevb.num_row_groups
                rvp__bbv += sum(iscd__txemw.total_byte_size for iscd__txemw in
                    tfi__yevb.row_groups)
        except Exception as mrxt__qnvk:
            jktb__nyftv = mrxt__qnvk
        if ahxq__dzcvc.allreduce(jktb__nyftv is not None, op=MPI.LOR):
            for jktb__nyftv in ahxq__dzcvc.allgather(jktb__nyftv):
                if jktb__nyftv:
                    if isinstance(fpath, list) and isinstance(jktb__nyftv,
                        (OSError, FileNotFoundError)):
                        raise BodoError(str(jktb__nyftv) +
                            list_of_files_error_msg)
                    raise jktb__nyftv
        if grdca__mstvm:
            abxfz__ngj = ahxq__dzcvc.allreduce(abxfz__ngj, op=MPI.LAND)
            if not abxfz__ngj:
                raise BodoError("Schema in parquet files don't match")
        if get_row_counts:
            nfl__mejat._bodo_total_rows = ahxq__dzcvc.allreduce(gax__kqbf,
                op=MPI.SUM)
            xsqhy__ngs = ahxq__dzcvc.allreduce(mom__jqole, op=MPI.SUM)
            lvyde__iiyt = ahxq__dzcvc.allreduce(rvp__bbv, op=MPI.SUM)
            ztm__pwih = np.array([voa__toh._bodo_num_rows for voa__toh in
                nfl__mejat.pieces])
            ztm__pwih = ahxq__dzcvc.allreduce(ztm__pwih, op=MPI.SUM)
            for voa__toh, dji__vgvq in zip(nfl__mejat.pieces, ztm__pwih):
                voa__toh._bodo_num_rows = dji__vgvq
            if is_parallel and bodo.get_rank(
                ) == 0 and xsqhy__ngs < bodo.get_size() and xsqhy__ngs != 0:
                warnings.warn(BodoWarning(
                    f"""Total number of row groups in parquet dataset {fpath} ({xsqhy__ngs}) is too small for effective IO parallelization.
For best performance the number of row groups should be greater than the number of workers ({bodo.get_size()}). For more details, refer to
https://docs.bodo.ai/latest/file_io/#parquet-section.
"""
                    ))
            if xsqhy__ngs == 0:
                whr__fcxkp = 0
            else:
                whr__fcxkp = lvyde__iiyt // xsqhy__ngs
            if (bodo.get_rank() == 0 and lvyde__iiyt >= 20 * 1048576 and 
                whr__fcxkp < 1048576 and protocol in REMOTE_FILESYSTEMS):
                warnings.warn(BodoWarning(
                    f'Parquet average row group size is small ({whr__fcxkp} bytes) and can have negative impact on performance when reading from remote sources'
                    ))
            if tracing.is_tracing():
                llf__oft.add_attribute('g_total_num_row_groups', xsqhy__ngs)
                llf__oft.add_attribute('total_scan_time', mhoe__retkw)
                dhv__akj = np.array([voa__toh._bodo_num_rows for voa__toh in
                    nfl__mejat.pieces])
                dfkp__uci = np.percentile(dhv__akj, [25, 50, 75])
                llf__oft.add_attribute('g_row_counts_min', dhv__akj.min())
                llf__oft.add_attribute('g_row_counts_Q1', dfkp__uci[0])
                llf__oft.add_attribute('g_row_counts_median', dfkp__uci[1])
                llf__oft.add_attribute('g_row_counts_Q3', dfkp__uci[2])
                llf__oft.add_attribute('g_row_counts_max', dhv__akj.max())
                llf__oft.add_attribute('g_row_counts_mean', dhv__akj.mean())
                llf__oft.add_attribute('g_row_counts_std', dhv__akj.std())
                llf__oft.add_attribute('g_row_counts_sum', dhv__akj.sum())
                llf__oft.finalize()
    nfl__mejat._prefix = ''
    if protocol in {'hdfs', 'abfs', 'abfss'}:
        prefix = f'{protocol}://{tejxq__vcg.netloc}'
        if len(nfl__mejat.pieces) > 0:
            oodc__ehia = nfl__mejat.pieces[0]
            if not oodc__ehia.path.startswith(prefix):
                nfl__mejat._prefix = prefix
    if read_categories:
        _add_categories_to_pq_dataset(nfl__mejat)
    if get_row_counts:
        mddo__wxej.finalize()
    if grdca__mstvm and is_parallel:
        if tracing.is_tracing():
            oknf__cfxbj = tracing.Event('unify_schemas_across_ranks')
        jktb__nyftv = None
        try:
            titiw__wgndm = ahxq__dzcvc.allreduce(titiw__wgndm, bodo.io.
                helpers.pa_schema_unify_mpi_op)
        except Exception as mrxt__qnvk:
            jktb__nyftv = mrxt__qnvk
        if tracing.is_tracing():
            oknf__cfxbj.finalize()
        if ahxq__dzcvc.allreduce(jktb__nyftv is not None, op=MPI.LOR):
            for jktb__nyftv in ahxq__dzcvc.allgather(jktb__nyftv):
                if jktb__nyftv:
                    qbdu__jiovi = (
                        f'Schema in some files were different.\n' + str(
                        jktb__nyftv))
                    raise BodoError(qbdu__jiovi)
    nfl__mejat._bodo_arrow_schema = titiw__wgndm
    return nfl__mejat


def get_scanner_batches(fpaths, expr_filters, selected_fields,
    avg_num_pieces, is_parallel, storage_options, region, prefix,
    str_as_dict_cols, start_offset, rows_to_read, has_partitions, schema):
    import pyarrow as pa
    iqak__iiu = os.cpu_count()
    if iqak__iiu is None or iqak__iiu == 0:
        iqak__iiu = 2
    kdje__ajb = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), iqak__iiu)
    ejzi__infpn = min(int(os.environ.get('BODO_MAX_IO_THREADS', 16)), iqak__iiu
        )
    if is_parallel and len(fpaths) > ejzi__infpn and len(fpaths
        ) / avg_num_pieces >= 2.0:
        pa.set_io_thread_count(ejzi__infpn)
        pa.set_cpu_count(ejzi__infpn)
    else:
        pa.set_io_thread_count(kdje__ajb)
        pa.set_cpu_count(kdje__ajb)
    if fpaths[0].startswith('s3://'):
        rxyrg__oejyi = urlparse(fpaths[0]).netloc
        prefix = 's3://' + rxyrg__oejyi + '/'
        fpaths = [ojhkg__nepz[len(prefix):] for ojhkg__nepz in fpaths]
        if region == '':
            region = get_s3_bucket_region_njit(fpaths[0], parallel=False)
        gylvj__ntu = get_s3_subtree_fs(rxyrg__oejyi, region=region,
            storage_options=storage_options)
    elif prefix and prefix.startswith(('hdfs', 'abfs', 'abfss')):
        gylvj__ntu = get_hdfs_fs(prefix + fpaths[0])
    elif fpaths[0].startswith(('gcs', 'gs')):
        import gcsfs
        gylvj__ntu = gcsfs.GCSFileSystem(token=None)
    else:
        gylvj__ntu = None
    szkw__oval = ds.ParquetFileFormat(dictionary_columns=str_as_dict_cols)
    nfl__mejat = ds.dataset(fpaths, filesystem=gylvj__ntu, partitioning=ds.
        partitioning(flavor='hive') if has_partitions else None, format=
        szkw__oval)
    yupzc__wzuja = set(str_as_dict_cols)
    iznma__lbd = schema.names
    for ofjfd__lekgh, name in enumerate(iznma__lbd):
        if name in yupzc__wzuja:
            zxhh__qeem = schema.field(ofjfd__lekgh)
            xqqu__ckvr = pa.field(name, pa.dictionary(pa.int32(),
                zxhh__qeem.type), zxhh__qeem.nullable)
            schema = schema.remove(ofjfd__lekgh).insert(ofjfd__lekgh,
                xqqu__ckvr)
    nfl__mejat = nfl__mejat.replace_schema(pa.unify_schemas([nfl__mejat.
        schema, schema]))
    col_names = nfl__mejat.schema.names
    zmd__bul = [col_names[ijon__fzqoo] for ijon__fzqoo in selected_fields]
    atklz__mjqu = len(fpaths) <= 3 or start_offset > 0 and len(fpaths) <= 10
    if atklz__mjqu and expr_filters is None:
        rfd__esje = []
        mqm__wepfm = 0
        ujvtm__pctal = 0
        for tfi__yevb in nfl__mejat.get_fragments():
            fxplc__fvby = []
            for iscd__txemw in tfi__yevb.row_groups:
                dux__quk = iscd__txemw.num_rows
                if start_offset < mqm__wepfm + dux__quk:
                    if ujvtm__pctal == 0:
                        rxm__crvi = start_offset - mqm__wepfm
                        jvn__jcy = min(dux__quk - rxm__crvi, rows_to_read)
                    else:
                        jvn__jcy = min(dux__quk, rows_to_read - ujvtm__pctal)
                    ujvtm__pctal += jvn__jcy
                    fxplc__fvby.append(iscd__txemw.id)
                mqm__wepfm += dux__quk
                if ujvtm__pctal == rows_to_read:
                    break
            rfd__esje.append(tfi__yevb.subset(row_group_ids=fxplc__fvby))
            if ujvtm__pctal == rows_to_read:
                break
        nfl__mejat = ds.FileSystemDataset(rfd__esje, nfl__mejat.schema,
            szkw__oval, filesystem=nfl__mejat.filesystem)
        start_offset = rxm__crvi
    iggoq__yii = nfl__mejat.scanner(columns=zmd__bul, filter=expr_filters,
        use_threads=True).to_reader()
    return nfl__mejat, iggoq__yii, start_offset


def _add_categories_to_pq_dataset(pq_dataset):
    import pyarrow as pa
    from mpi4py import MPI
    if len(pq_dataset.pieces) < 1:
        raise BodoError(
            'No pieces found in Parquet dataset. Cannot get read categorical values'
            )
    pa_schema = pq_dataset.schema.to_arrow_schema()
    zvrmu__hpyji = [c for c in pa_schema.names if isinstance(pa_schema.
        field(c).type, pa.DictionaryType)]
    if len(zvrmu__hpyji) == 0:
        pq_dataset._category_info = {}
        return
    ahxq__dzcvc = MPI.COMM_WORLD
    if bodo.get_rank() == 0:
        try:
            wwtzn__neziv = pq_dataset.pieces[0].open()
            iscd__txemw = wwtzn__neziv.read_row_group(0, zvrmu__hpyji)
            category_info = {c: tuple(iscd__txemw.column(c).chunk(0).
                dictionary.to_pylist()) for c in zvrmu__hpyji}
            del wwtzn__neziv, iscd__txemw
        except Exception as mrxt__qnvk:
            ahxq__dzcvc.bcast(mrxt__qnvk)
            raise mrxt__qnvk
        ahxq__dzcvc.bcast(category_info)
    else:
        category_info = ahxq__dzcvc.bcast(None)
        if isinstance(category_info, Exception):
            jktb__nyftv = category_info
            raise jktb__nyftv
    pq_dataset._category_info = category_info


def get_pandas_metadata(schema, num_pieces):
    lstgg__qpm = None
    nullable_from_metadata = defaultdict(lambda : None)
    sfy__edjoi = b'pandas'
    if schema.metadata is not None and sfy__edjoi in schema.metadata:
        import json
        ptfgc__vdg = json.loads(schema.metadata[sfy__edjoi].decode('utf8'))
        dtjoh__fjy = len(ptfgc__vdg['index_columns'])
        if dtjoh__fjy > 1:
            raise BodoError('read_parquet: MultiIndex not supported yet')
        lstgg__qpm = ptfgc__vdg['index_columns'][0] if dtjoh__fjy else None
        if not isinstance(lstgg__qpm, str) and not isinstance(lstgg__qpm, dict
            ):
            lstgg__qpm = None
        for swbw__kpq in ptfgc__vdg['columns']:
            xif__tbw = swbw__kpq['name']
            if swbw__kpq['pandas_type'].startswith('int'
                ) and xif__tbw is not None:
                if swbw__kpq['numpy_type'].startswith('Int'):
                    nullable_from_metadata[xif__tbw] = True
                else:
                    nullable_from_metadata[xif__tbw] = False
    return lstgg__qpm, nullable_from_metadata


def get_str_columns_from_pa_schema(pa_schema):
    str_columns = []
    for xif__tbw in pa_schema.names:
        gbqs__fmpt = pa_schema.field(xif__tbw)
        if gbqs__fmpt.type == pa.string():
            str_columns.append(xif__tbw)
    return str_columns


def determine_str_as_dict_columns(pq_dataset, pa_schema, str_columns):
    from mpi4py import MPI
    ahxq__dzcvc = MPI.COMM_WORLD
    if len(str_columns) == 0:
        return set()
    if len(pq_dataset.pieces) > bodo.get_size():
        import random
        random.seed(37)
        ktz__ojfr = random.sample(pq_dataset.pieces, bodo.get_size())
    else:
        ktz__ojfr = pq_dataset.pieces
    ihie__dwxnh = np.zeros(len(str_columns), dtype=np.int64)
    byw__mtekg = np.zeros(len(str_columns), dtype=np.int64)
    if bodo.get_rank() < len(ktz__ojfr):
        oodc__ehia = ktz__ojfr[bodo.get_rank()]
        try:
            oeb__xwoo = oodc__ehia.get_metadata()
            for ofjfd__lekgh in range(oeb__xwoo.num_row_groups):
                for uqgl__lnyyp, xif__tbw in enumerate(str_columns):
                    zbglo__hgswe = pa_schema.get_field_index(xif__tbw)
                    ihie__dwxnh[uqgl__lnyyp] += oeb__xwoo.row_group(
                        ofjfd__lekgh).column(zbglo__hgswe
                        ).total_uncompressed_size
            kdy__rvrn = oeb__xwoo.num_rows
        except Exception as mrxt__qnvk:
            if isinstance(mrxt__qnvk, (OSError, FileNotFoundError)):
                kdy__rvrn = 0
            else:
                raise
    else:
        kdy__rvrn = 0
    ivjxi__nays = ahxq__dzcvc.allreduce(kdy__rvrn, op=MPI.SUM)
    if ivjxi__nays == 0:
        return set()
    ahxq__dzcvc.Allreduce(ihie__dwxnh, byw__mtekg, op=MPI.SUM)
    bvcgg__jye = byw__mtekg / ivjxi__nays
    str_as_dict = set()
    for ofjfd__lekgh, nuflx__fpnum in enumerate(bvcgg__jye):
        if nuflx__fpnum < READ_STR_AS_DICT_THRESHOLD:
            xif__tbw = str_columns[ofjfd__lekgh][0]
            str_as_dict.add(xif__tbw)
    return str_as_dict


def parquet_file_schema(file_name, selected_columns, storage_options=None,
    input_file_name_col=None, read_as_dict_cols=None):
    col_names = []
    lnurp__qkqio = []
    pq_dataset = get_parquet_dataset(file_name, get_row_counts=False,
        storage_options=storage_options, read_categories=True)
    if hasattr(pq_dataset, '_bodo_arrow_schema'):
        pa_schema = pq_dataset._bodo_arrow_schema
    else:
        pa_schema = pq_dataset.schema.to_arrow_schema()
    partition_names = [] if pq_dataset.partitions is None else [pq_dataset.
        partitions.levels[ofjfd__lekgh].name for ofjfd__lekgh in range(len(
        pq_dataset.partitions.partition_names))]
    num_pieces = len(pq_dataset.pieces)
    str_columns = get_str_columns_from_pa_schema(pa_schema)
    brtuk__ino = set(str_columns)
    if read_as_dict_cols is None:
        read_as_dict_cols = []
    read_as_dict_cols = set(read_as_dict_cols)
    cvvba__ezs = read_as_dict_cols - brtuk__ino
    if len(cvvba__ezs) > 0:
        if bodo.get_rank() == 0:
            warnings.warn(
                f'The following columns are not of datatype string and hence cannot be read with dictionary encoding: {cvvba__ezs}'
                , bodo.utils.typing.BodoWarning)
    read_as_dict_cols.intersection_update(brtuk__ino)
    brtuk__ino = brtuk__ino - read_as_dict_cols
    str_columns = [sxr__oadrl for sxr__oadrl in str_columns if sxr__oadrl in
        brtuk__ino]
    str_as_dict: set = determine_str_as_dict_columns(pq_dataset, pa_schema,
        str_columns)
    str_as_dict.update(read_as_dict_cols)
    col_names = pa_schema.names
    lstgg__qpm, nullable_from_metadata = get_pandas_metadata(pa_schema,
        num_pieces)
    zjekn__chj = []
    hbmf__xfs = []
    knckz__yjeqc = []
    for ofjfd__lekgh, c in enumerate(col_names):
        gbqs__fmpt = pa_schema.field(c)
        tgr__rwde, tmbbi__iqe = _get_numba_typ_from_pa_typ(gbqs__fmpt, c ==
            lstgg__qpm, nullable_from_metadata[c], pq_dataset.
            _category_info, str_as_dict=c in str_as_dict)
        zjekn__chj.append(tgr__rwde)
        hbmf__xfs.append(tmbbi__iqe)
        knckz__yjeqc.append(gbqs__fmpt.type)
    if partition_names:
        col_names += partition_names
        zjekn__chj += [_get_partition_cat_dtype(pq_dataset.partitions.
            levels[ofjfd__lekgh]) for ofjfd__lekgh in range(len(
            partition_names))]
        hbmf__xfs.extend([True] * len(partition_names))
        knckz__yjeqc.extend([None] * len(partition_names))
    if input_file_name_col is not None:
        col_names += [input_file_name_col]
        zjekn__chj += [dict_str_arr_type]
        hbmf__xfs.append(True)
        knckz__yjeqc.append(None)
    rvf__uff = {c: ofjfd__lekgh for ofjfd__lekgh, c in enumerate(col_names)}
    if selected_columns is None:
        selected_columns = col_names
    for c in selected_columns:
        if c not in rvf__uff:
            raise BodoError(f'Selected column {c} not in Parquet file schema')
    if lstgg__qpm and not isinstance(lstgg__qpm, dict
        ) and lstgg__qpm not in selected_columns:
        selected_columns.append(lstgg__qpm)
    col_names = selected_columns
    col_indices = []
    lnurp__qkqio = []
    fwyp__uvwdj = []
    ngt__zgr = []
    for ofjfd__lekgh, c in enumerate(col_names):
        qtpo__vxk = rvf__uff[c]
        col_indices.append(qtpo__vxk)
        lnurp__qkqio.append(zjekn__chj[qtpo__vxk])
        if not hbmf__xfs[qtpo__vxk]:
            fwyp__uvwdj.append(ofjfd__lekgh)
            ngt__zgr.append(knckz__yjeqc[qtpo__vxk])
    return (col_names, lnurp__qkqio, lstgg__qpm, col_indices,
        partition_names, fwyp__uvwdj, ngt__zgr)


def _get_partition_cat_dtype(part_set):
    pds__sro = part_set.dictionary.to_pandas()
    jli__nxvx = bodo.typeof(pds__sro).dtype
    zqshf__jmk = PDCategoricalDtype(tuple(pds__sro), jli__nxvx, False)
    return CategoricalArrayType(zqshf__jmk)


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
        wuud__ussys = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(32), lir.IntType(32),
            lir.IntType(32), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        tpt__vccp = cgutils.get_or_insert_function(builder.module,
            wuud__ussys, name='pq_write')
        builder.call(tpt__vccp, args)
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
        wuud__ussys = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        tpt__vccp = cgutils.get_or_insert_function(builder.module,
            wuud__ussys, name='pq_write_partitioned')
        builder.call(tpt__vccp, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
    return types.void(types.voidptr, data_table_t, col_names_t,
        col_names_no_partitions_t, cat_table_t, types.voidptr, types.int32,
        types.voidptr, types.boolean, types.voidptr, types.int64), codegen
