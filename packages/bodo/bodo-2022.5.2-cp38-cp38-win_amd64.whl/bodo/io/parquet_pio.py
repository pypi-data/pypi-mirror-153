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
        except OSError as lidvv__kna:
            if 'non-file path' in str(lidvv__kna):
                raise FileNotFoundError(str(lidvv__kna))
            raise


class ParquetHandler:

    def __init__(self, func_ir, typingctx, args, _locals):
        self.func_ir = func_ir
        self.typingctx = typingctx
        self.args = args
        self.locals = _locals

    def gen_parquet_read(self, file_name, lhs, columns, storage_options=
        None, input_file_name_col=None, read_as_dict_cols=None):
        lcsq__wof = lhs.scope
        ttolm__rihzx = lhs.loc
        bnbs__wcqmg = None
        if lhs.name in self.locals:
            bnbs__wcqmg = self.locals[lhs.name]
            self.locals.pop(lhs.name)
        tumlj__rjv = {}
        if lhs.name + ':convert' in self.locals:
            tumlj__rjv = self.locals[lhs.name + ':convert']
            self.locals.pop(lhs.name + ':convert')
        if bnbs__wcqmg is None:
            emcd__fpq = (
                'Parquet schema not available. Either path argument should be constant for Bodo to look at the file at compile time or schema should be provided. For more information, see: https://docs.bodo.ai/latest/file_io/#parquet-section.'
                )
            lfxax__nyisz = get_const_value(file_name, self.func_ir,
                emcd__fpq, arg_types=self.args, file_info=ParquetFileInfo(
                columns, storage_options=storage_options,
                input_file_name_col=input_file_name_col, read_as_dict_cols=
                read_as_dict_cols))
            gjkq__ytf = False
            nxlzm__gyhfp = guard(get_definition, self.func_ir, file_name)
            if isinstance(nxlzm__gyhfp, ir.Arg):
                typ = self.args[nxlzm__gyhfp.index]
                if isinstance(typ, types.FilenameType):
                    (col_names, jlv__ewct, agx__zmjuf, col_indices,
                        partition_names, djnr__nlovd, baqg__fxeh) = typ.schema
                    gjkq__ytf = True
            if not gjkq__ytf:
                (col_names, jlv__ewct, agx__zmjuf, col_indices,
                    partition_names, djnr__nlovd, baqg__fxeh) = (
                    parquet_file_schema(lfxax__nyisz, columns,
                    storage_options=storage_options, input_file_name_col=
                    input_file_name_col, read_as_dict_cols=read_as_dict_cols))
        else:
            qlagf__keut = list(bnbs__wcqmg.keys())
            irj__fohmg = {c: chbt__opa for chbt__opa, c in enumerate(
                qlagf__keut)}
            nbph__mxd = [lylcp__qdls for lylcp__qdls in bnbs__wcqmg.values()]
            agx__zmjuf = 'index' if 'index' in irj__fohmg else None
            if columns is None:
                selected_columns = qlagf__keut
            else:
                selected_columns = columns
            col_indices = [irj__fohmg[c] for c in selected_columns]
            jlv__ewct = [nbph__mxd[irj__fohmg[c]] for c in selected_columns]
            col_names = selected_columns
            agx__zmjuf = agx__zmjuf if agx__zmjuf in col_names else None
            partition_names = []
            djnr__nlovd = []
            baqg__fxeh = []
        cahm__agyl = None if isinstance(agx__zmjuf, dict
            ) or agx__zmjuf is None else agx__zmjuf
        index_column_index = None
        index_column_type = types.none
        if cahm__agyl:
            nvjpz__rpym = col_names.index(cahm__agyl)
            index_column_index = col_indices.pop(nvjpz__rpym)
            index_column_type = jlv__ewct.pop(nvjpz__rpym)
            col_names.pop(nvjpz__rpym)
        for chbt__opa, c in enumerate(col_names):
            if c in tumlj__rjv:
                jlv__ewct[chbt__opa] = tumlj__rjv[c]
        hmfq__blgi = [ir.Var(lcsq__wof, mk_unique_var('pq_table'),
            ttolm__rihzx), ir.Var(lcsq__wof, mk_unique_var('pq_index'),
            ttolm__rihzx)]
        yfl__oirsd = [bodo.ir.parquet_ext.ParquetReader(file_name, lhs.name,
            col_names, col_indices, jlv__ewct, hmfq__blgi, ttolm__rihzx,
            partition_names, storage_options, index_column_index,
            index_column_type, input_file_name_col, djnr__nlovd, baqg__fxeh)]
        return (col_names, hmfq__blgi, agx__zmjuf, yfl__oirsd, jlv__ewct,
            index_column_type)


def pq_distributed_run(pq_node, array_dists, typemap, calltypes, typingctx,
    targetctx, meta_head_only_info=None):
    gzkn__syj = len(pq_node.out_vars)
    dnf_filter_str = 'None'
    expr_filter_str = 'None'
    iyk__mvh, hck__ril = bodo.ir.connector.generate_filter_map(pq_node.filters)
    extra_args = ', '.join(iyk__mvh.values())
    dnf_filter_str, expr_filter_str = bodo.ir.connector.generate_arrow_filters(
        pq_node.filters, iyk__mvh, hck__ril, pq_node.original_df_colnames,
        pq_node.partition_names, pq_node.original_out_types, typemap, 'parquet'
        )
    lxfqb__ogohd = ', '.join(f'out{chbt__opa}' for chbt__opa in range(
        gzkn__syj))
    vsuj__iwh = f'def pq_impl(fname, {extra_args}):\n'
    vsuj__iwh += (
        f'    (total_rows, {lxfqb__ogohd},) = _pq_reader_py(fname, {extra_args})\n'
        )
    qnd__hvkon = {}
    exec(vsuj__iwh, {}, qnd__hvkon)
    pnjw__fub = qnd__hvkon['pq_impl']
    if bodo.user_logging.get_verbose_level() >= 1:
        hod__ooo = pq_node.loc.strformat()
        ipzqi__idef = []
        rih__ivan = []
        for chbt__opa in pq_node.type_usecol_offset:
            clml__dkfs = pq_node.df_colnames[chbt__opa]
            ipzqi__idef.append(clml__dkfs)
            if isinstance(pq_node.out_types[chbt__opa], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                rih__ivan.append(clml__dkfs)
        hszjk__mxmj = (
            'Finish column pruning on read_parquet node:\n%s\nColumns loaded %s\n'
            )
        bodo.user_logging.log_message('Column Pruning', hszjk__mxmj,
            hod__ooo, ipzqi__idef)
        if rih__ivan:
            csrb__pyfus = """Finished optimized encoding on read_parquet node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                csrb__pyfus, hod__ooo, rih__ivan)
    parallel = bodo.ir.connector.is_connector_table_parallel(pq_node,
        array_dists, typemap, 'ParquetReader')
    if pq_node.unsupported_columns:
        winet__uwb = set(pq_node.type_usecol_offset)
        yup__edgln = set(pq_node.unsupported_columns)
        nbj__ufpq = winet__uwb & yup__edgln
        if nbj__ufpq:
            hjcuo__zcln = sorted(nbj__ufpq)
            dgb__ujm = [
                f'pandas.read_parquet(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                "Please manually remove these columns from your read_parquet with the 'columns' argument. If these "
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            fybi__dalq = 0
            for ctb__fiyxp in hjcuo__zcln:
                while pq_node.unsupported_columns[fybi__dalq] != ctb__fiyxp:
                    fybi__dalq += 1
                dgb__ujm.append(
                    f"Column '{pq_node.df_colnames[ctb__fiyxp]}' with unsupported arrow type {pq_node.unsupported_arrow_types[fybi__dalq]}"
                    )
                fybi__dalq += 1
            cyogo__sls = '\n'.join(dgb__ujm)
            raise BodoError(cyogo__sls, loc=pq_node.loc)
    afgn__tgl = _gen_pq_reader_py(pq_node.df_colnames, pq_node.col_indices,
        pq_node.type_usecol_offset, pq_node.out_types, pq_node.
        storage_options, pq_node.partition_names, dnf_filter_str,
        expr_filter_str, extra_args, parallel, meta_head_only_info, pq_node
        .index_column_index, pq_node.index_column_type, pq_node.
        input_file_name_col)
    kpz__pog = typemap[pq_node.file_name.name]
    etj__ekrn = (kpz__pog,) + tuple(typemap[bjjp__xrp.name] for bjjp__xrp in
        hck__ril)
    xrsj__mqjnz = compile_to_numba_ir(pnjw__fub, {'_pq_reader_py':
        afgn__tgl}, typingctx=typingctx, targetctx=targetctx, arg_typs=
        etj__ekrn, typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(xrsj__mqjnz, [pq_node.file_name] + hck__ril)
    yfl__oirsd = xrsj__mqjnz.body[:-3]
    if meta_head_only_info:
        yfl__oirsd[-1 - gzkn__syj].target = meta_head_only_info[1]
    yfl__oirsd[-2].target = pq_node.out_vars[0]
    yfl__oirsd[-1].target = pq_node.out_vars[1]
    assert not (pq_node.index_column_index is None and not pq_node.
        type_usecol_offset
        ), 'At most one of table and index should be dead if the Parquet IR node is live'
    if pq_node.index_column_index is None:
        yfl__oirsd.pop(-1)
    elif not pq_node.type_usecol_offset:
        yfl__oirsd.pop(-2)
    return yfl__oirsd


distributed_pass.distributed_run_extensions[bodo.ir.parquet_ext.ParquetReader
    ] = pq_distributed_run


def get_filters_pyobject(dnf_filter_str, expr_filter_str, vars):
    pass


@overload(get_filters_pyobject, no_unliteral=True)
def overload_get_filters_pyobject(dnf_filter_str, expr_filter_str, var_tup):
    gziv__fxut = get_overload_const_str(dnf_filter_str)
    xmqe__dir = get_overload_const_str(expr_filter_str)
    zezw__lyaeu = ', '.join(f'f{chbt__opa}' for chbt__opa in range(len(
        var_tup)))
    vsuj__iwh = 'def impl(dnf_filter_str, expr_filter_str, var_tup):\n'
    if len(var_tup):
        vsuj__iwh += f'  {zezw__lyaeu}, = var_tup\n'
    vsuj__iwh += """  with numba.objmode(dnf_filters_py='parquet_predicate_type', expr_filters_py='parquet_predicate_type'):
"""
    vsuj__iwh += f'    dnf_filters_py = {gziv__fxut}\n'
    vsuj__iwh += f'    expr_filters_py = {xmqe__dir}\n'
    vsuj__iwh += '  return (dnf_filters_py, expr_filters_py)\n'
    qnd__hvkon = {}
    exec(vsuj__iwh, globals(), qnd__hvkon)
    return qnd__hvkon['impl']


@numba.njit
def get_fname_pyobject(fname):
    with numba.objmode(fname_py='read_parquet_fpath_type'):
        fname_py = fname
    return fname_py


def _gen_pq_reader_py(col_names, col_indices, type_usecol_offset, out_types,
    storage_options, partition_names, dnf_filter_str, expr_filter_str,
    extra_args, is_parallel, meta_head_only_info, index_column_index,
    index_column_type, input_file_name_col):
    stkd__sgcte = next_label()
    xml__gkrh = ',' if extra_args else ''
    vsuj__iwh = f'def pq_reader_py(fname,{extra_args}):\n'
    vsuj__iwh += (
        f"    ev = bodo.utils.tracing.Event('read_parquet', {is_parallel})\n")
    vsuj__iwh += f"    ev.add_attribute('g_fname', fname)\n"
    vsuj__iwh += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={is_parallel})
"""
    vsuj__iwh += f"""    dnf_filters, expr_filters = get_filters_pyobject("{dnf_filter_str}", "{expr_filter_str}", ({extra_args}{xml__gkrh}))
"""
    vsuj__iwh += '    fname_py = get_fname_pyobject(fname)\n'
    storage_options['bodo_dummy'] = 'dummy'
    vsuj__iwh += (
        f'    storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    tot_rows_to_read = -1
    if meta_head_only_info and meta_head_only_info[0] is not None:
        tot_rows_to_read = meta_head_only_info[0]
    oqyhk__lmag = not type_usecol_offset
    mvktm__spz = [sanitize_varname(c) for c in col_names]
    partition_names = [sanitize_varname(c) for c in partition_names]
    input_file_name_col = sanitize_varname(input_file_name_col
        ) if input_file_name_col is not None and col_names.index(
        input_file_name_col) in type_usecol_offset else None
    erwn__qzsg = {c: chbt__opa for chbt__opa, c in enumerate(col_indices)}
    buyxo__dew = {c: chbt__opa for chbt__opa, c in enumerate(mvktm__spz)}
    fanqs__lfjq = []
    mrm__qmvk = set()
    edbq__dll = partition_names + [input_file_name_col]
    for chbt__opa in type_usecol_offset:
        if mvktm__spz[chbt__opa] not in edbq__dll:
            fanqs__lfjq.append(col_indices[chbt__opa])
        elif not input_file_name_col or mvktm__spz[chbt__opa
            ] != input_file_name_col:
            mrm__qmvk.add(col_indices[chbt__opa])
    if index_column_index is not None:
        fanqs__lfjq.append(index_column_index)
    fanqs__lfjq = sorted(fanqs__lfjq)
    xlboi__fvbmz = {c: chbt__opa for chbt__opa, c in enumerate(fanqs__lfjq)}
    bokx__mxp = [(int(is_nullable(out_types[erwn__qzsg[bmk__avuk]])) if 
        bmk__avuk != index_column_index else int(is_nullable(
        index_column_type))) for bmk__avuk in fanqs__lfjq]
    str_as_dict_cols = []
    for bmk__avuk in fanqs__lfjq:
        if bmk__avuk == index_column_index:
            lylcp__qdls = index_column_type
        else:
            lylcp__qdls = out_types[erwn__qzsg[bmk__avuk]]
        if lylcp__qdls == dict_str_arr_type:
            str_as_dict_cols.append(bmk__avuk)
    rpffl__ozcfn = []
    evos__xqzyf = {}
    zgm__vqr = []
    qylon__ziqsk = []
    for chbt__opa, lncah__rkz in enumerate(partition_names):
        try:
            ccgu__ieeb = buyxo__dew[lncah__rkz]
            if col_indices[ccgu__ieeb] not in mrm__qmvk:
                continue
        except (KeyError, ValueError) as fhbsw__beiee:
            continue
        evos__xqzyf[lncah__rkz] = len(rpffl__ozcfn)
        rpffl__ozcfn.append(lncah__rkz)
        zgm__vqr.append(chbt__opa)
        arz__mzv = out_types[ccgu__ieeb].dtype
        htkwd__jjv = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arz__mzv)
        qylon__ziqsk.append(numba_to_c_type(htkwd__jjv))
    vsuj__iwh += f'    total_rows_np = np.array([0], dtype=np.int64)\n'
    vsuj__iwh += f'    out_table = pq_read(\n'
    vsuj__iwh += f'        fname_py, {is_parallel},\n'
    vsuj__iwh += f'        unicode_to_utf8(bucket_region),\n'
    vsuj__iwh += f'        dnf_filters, expr_filters,\n'
    vsuj__iwh += f"""        storage_options_py, {tot_rows_to_read}, selected_cols_arr_{stkd__sgcte}.ctypes,
"""
    vsuj__iwh += f'        {len(fanqs__lfjq)},\n'
    vsuj__iwh += f'        nullable_cols_arr_{stkd__sgcte}.ctypes,\n'
    if len(zgm__vqr) > 0:
        vsuj__iwh += f'        np.array({zgm__vqr}, dtype=np.int32).ctypes,\n'
        vsuj__iwh += (
            f'        np.array({qylon__ziqsk}, dtype=np.int32).ctypes,\n')
        vsuj__iwh += f'        {len(zgm__vqr)},\n'
    else:
        vsuj__iwh += f'        0, 0, 0,\n'
    if len(str_as_dict_cols) > 0:
        vsuj__iwh += f"""        np.array({str_as_dict_cols}, dtype=np.int32).ctypes, {len(str_as_dict_cols)},
"""
    else:
        vsuj__iwh += f'        0, 0,\n'
    vsuj__iwh += f'        total_rows_np.ctypes,\n'
    vsuj__iwh += f'        {input_file_name_col is not None},\n'
    vsuj__iwh += f'    )\n'
    vsuj__iwh += f'    check_and_propagate_cpp_exception()\n'
    eyhnc__nld = 'None'
    pil__ras = index_column_type
    nnhdg__ooz = TableType(tuple(out_types))
    if oqyhk__lmag:
        nnhdg__ooz = types.none
    if index_column_index is not None:
        qgbu__lwnzy = xlboi__fvbmz[index_column_index]
        eyhnc__nld = (
            f'info_to_array(info_from_table(out_table, {qgbu__lwnzy}), index_arr_type)'
            )
    vsuj__iwh += f'    index_arr = {eyhnc__nld}\n'
    if oqyhk__lmag:
        kiq__tzwx = None
    else:
        kiq__tzwx = []
        eule__nfj = 0
        hjj__hnlgt = col_indices[col_names.index(input_file_name_col)
            ] if input_file_name_col is not None else None
        for chbt__opa, ctb__fiyxp in enumerate(col_indices):
            if eule__nfj < len(type_usecol_offset
                ) and chbt__opa == type_usecol_offset[eule__nfj]:
                rrvv__fei = col_indices[chbt__opa]
                if hjj__hnlgt and rrvv__fei == hjj__hnlgt:
                    kiq__tzwx.append(len(fanqs__lfjq) + len(rpffl__ozcfn))
                elif rrvv__fei in mrm__qmvk:
                    ftskf__cdn = mvktm__spz[chbt__opa]
                    kiq__tzwx.append(len(fanqs__lfjq) + evos__xqzyf[ftskf__cdn]
                        )
                else:
                    kiq__tzwx.append(xlboi__fvbmz[ctb__fiyxp])
                eule__nfj += 1
            else:
                kiq__tzwx.append(-1)
        kiq__tzwx = np.array(kiq__tzwx, dtype=np.int64)
    if oqyhk__lmag:
        vsuj__iwh += '    T = None\n'
    else:
        vsuj__iwh += f"""    T = cpp_table_to_py_table(out_table, table_idx_{stkd__sgcte}, py_table_type_{stkd__sgcte})
"""
    vsuj__iwh += f'    delete_table(out_table)\n'
    vsuj__iwh += f'    total_rows = total_rows_np[0]\n'
    vsuj__iwh += f'    ev.finalize()\n'
    vsuj__iwh += f'    return (total_rows, T, index_arr)\n'
    qnd__hvkon = {}
    sfo__nuxv = {f'py_table_type_{stkd__sgcte}': nnhdg__ooz,
        f'table_idx_{stkd__sgcte}': kiq__tzwx,
        f'selected_cols_arr_{stkd__sgcte}': np.array(fanqs__lfjq, np.int32),
        f'nullable_cols_arr_{stkd__sgcte}': np.array(bokx__mxp, np.int32),
        'index_arr_type': pil__ras, 'cpp_table_to_py_table':
        cpp_table_to_py_table, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'delete_table': delete_table,
        'check_and_propagate_cpp_exception':
        check_and_propagate_cpp_exception, 'pq_read': _pq_read,
        'unicode_to_utf8': unicode_to_utf8, 'get_filters_pyobject':
        get_filters_pyobject, 'get_storage_options_pyobject':
        get_storage_options_pyobject, 'get_fname_pyobject':
        get_fname_pyobject, 'np': np, 'pd': pd, 'bodo': bodo}
    exec(vsuj__iwh, sfo__nuxv, qnd__hvkon)
    afgn__tgl = qnd__hvkon['pq_reader_py']
    cjed__owsii = numba.njit(afgn__tgl, no_cpython_wrapper=True)
    return cjed__owsii


import pyarrow as pa
_pa_numba_typ_map = {pa.bool_(): types.bool_, pa.int8(): types.int8, pa.
    int16(): types.int16, pa.int32(): types.int32, pa.int64(): types.int64,
    pa.uint8(): types.uint8, pa.uint16(): types.uint16, pa.uint32(): types.
    uint32, pa.uint64(): types.uint64, pa.float32(): types.float32, pa.
    float64(): types.float64, pa.string(): string_type, pa.binary():
    bytes_type, pa.date32(): datetime_date_type, pa.date64(): types.
    NPDatetime('ns'), null(): string_type}


def get_arrow_timestamp_type(pa_ts_typ):
    jqv__mkkw = 'ns', 'us', 'ms', 's'
    if pa_ts_typ.unit not in jqv__mkkw:
        return types.Array(bodo.datetime64ns, 1, 'C'), False
    elif pa_ts_typ.tz is not None:
        mrt__ixqab = pa_ts_typ.to_pandas_dtype().tz
        tnqoj__cxw = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(
            mrt__ixqab)
        return bodo.DatetimeArrayType(tnqoj__cxw), True
    else:
        return types.Array(bodo.datetime64ns, 1, 'C'), True


def _get_numba_typ_from_pa_typ(pa_typ, is_index, nullable_from_metadata,
    category_info, str_as_dict=False):
    if isinstance(pa_typ.type, pa.ListType):
        ogon__aoi, oanzq__aaic = _get_numba_typ_from_pa_typ(pa_typ.type.
            value_field, is_index, nullable_from_metadata, category_info)
        return ArrayItemArrayType(ogon__aoi), oanzq__aaic
    if isinstance(pa_typ.type, pa.StructType):
        mke__aqgf = []
        zhb__ynggt = []
        oanzq__aaic = True
        for jaqd__xiaaj in pa_typ.flatten():
            zhb__ynggt.append(jaqd__xiaaj.name.split('.')[-1])
            auc__hdn, ujjjg__hzi = _get_numba_typ_from_pa_typ(jaqd__xiaaj,
                is_index, nullable_from_metadata, category_info)
            mke__aqgf.append(auc__hdn)
            oanzq__aaic = oanzq__aaic and ujjjg__hzi
        return StructArrayType(tuple(mke__aqgf), tuple(zhb__ynggt)
            ), oanzq__aaic
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
        zbdg__znxvk = _pa_numba_typ_map[pa_typ.type.index_type]
        tnbv__rum = PDCategoricalDtype(category_info[pa_typ.name], bodo.
            string_type, pa_typ.type.ordered, int_type=zbdg__znxvk)
        return CategoricalArrayType(tnbv__rum), True
    if isinstance(pa_typ.type, pa.lib.TimestampType):
        return get_arrow_timestamp_type(pa_typ.type)
    elif pa_typ.type in _pa_numba_typ_map:
        tzx__yjd = _pa_numba_typ_map[pa_typ.type]
        oanzq__aaic = True
    else:
        raise BodoError('Arrow data type {} not supported yet'.format(
            pa_typ.type))
    if tzx__yjd == datetime_date_type:
        return datetime_date_array_type, oanzq__aaic
    if tzx__yjd == bytes_type:
        return binary_array_type, oanzq__aaic
    ogon__aoi = string_array_type if tzx__yjd == string_type else types.Array(
        tzx__yjd, 1, 'C')
    if tzx__yjd == types.bool_:
        ogon__aoi = boolean_array
    if nullable_from_metadata is not None:
        rdoh__kznr = nullable_from_metadata
    else:
        rdoh__kznr = use_nullable_int_arr
    if rdoh__kznr and not is_index and isinstance(tzx__yjd, types.Integer
        ) and pa_typ.nullable:
        ogon__aoi = IntegerArrayType(tzx__yjd)
    return ogon__aoi, oanzq__aaic


def get_parquet_dataset(fpath, get_row_counts=True, dnf_filters=None,
    expr_filters=None, storage_options=None, read_categories=False,
    is_parallel=False, tot_rows_to_read=None, typing_pa_schema=None):
    if get_row_counts:
        ngwfk__umduz = tracing.Event('get_parquet_dataset')
    import time
    import pyarrow as pa
    import pyarrow.parquet as pq
    from mpi4py import MPI
    ychee__unepf = MPI.COMM_WORLD
    if isinstance(fpath, list):
        srx__alwm = urlparse(fpath[0])
        protocol = srx__alwm.scheme
        ucfhu__gjm = srx__alwm.netloc
        for chbt__opa in range(len(fpath)):
            toutp__tky = fpath[chbt__opa]
            nadcp__cqsq = urlparse(toutp__tky)
            if nadcp__cqsq.scheme != protocol:
                raise BodoError(
                    'All parquet files must use the same filesystem protocol')
            if nadcp__cqsq.netloc != ucfhu__gjm:
                raise BodoError(
                    'All parquet files must be in the same S3 bucket')
            fpath[chbt__opa] = toutp__tky.rstrip('/')
    else:
        srx__alwm = urlparse(fpath)
        protocol = srx__alwm.scheme
        fpath = fpath.rstrip('/')
    if protocol in {'gcs', 'gs'}:
        try:
            import gcsfs
        except ImportError as fhbsw__beiee:
            waojf__pdtm = """Couldn't import gcsfs, which is required for Google cloud access. gcsfs can be installed by calling 'conda install -c conda-forge gcsfs'.
"""
            raise BodoError(waojf__pdtm)
    if protocol == 'http':
        try:
            import fsspec
        except ImportError as fhbsw__beiee:
            waojf__pdtm = """Couldn't import fsspec, which is required for http access. fsspec can be installed by calling 'conda install -c conda-forge fsspec'.
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
            ebvm__lya = gcsfs.GCSFileSystem(token=None)
            fs.append(ebvm__lya)
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
                prefix = f'{protocol}://{srx__alwm.netloc}'
                path = path[len(prefix):]
            xubiu__tfj = fs.glob(path)
            if protocol == 's3':
                xubiu__tfj = [('s3://' + toutp__tky) for toutp__tky in
                    xubiu__tfj if not toutp__tky.startswith('s3://')]
            elif protocol in {'hdfs', 'abfs', 'abfss'}:
                xubiu__tfj = [(prefix + toutp__tky) for toutp__tky in
                    xubiu__tfj]
        except:
            raise BodoError(
                f'glob pattern expansion not supported for {protocol}')
        if len(xubiu__tfj) == 0:
            raise BodoError('No files found matching glob pattern')
        return xubiu__tfj
    ggrh__wlq = False
    if get_row_counts:
        ssfr__myo = getfs(parallel=True)
        ggrh__wlq = bodo.parquet_validate_schema
    if bodo.get_rank() == 0:
        jdk__vvn = 1
        nxb__oof = os.cpu_count()
        if nxb__oof is not None and nxb__oof > 1:
            jdk__vvn = nxb__oof // 2
        try:
            if get_row_counts:
                dxkj__tps = tracing.Event('pq.ParquetDataset', is_parallel=
                    False)
                if tracing.is_tracing():
                    dxkj__tps.add_attribute('g_dnf_filter', str(dnf_filters))
            hmb__lhiwa = pa.io_thread_count()
            pa.set_io_thread_count(jdk__vvn)
            if isinstance(fpath, list):
                vgecr__njr = []
                for wbak__xkhvd in fpath:
                    if has_magic(wbak__xkhvd):
                        vgecr__njr += glob(protocol, getfs(), wbak__xkhvd)
                    else:
                        vgecr__njr.append(wbak__xkhvd)
                fpath = vgecr__njr
            elif has_magic(fpath):
                fpath = glob(protocol, getfs(), fpath)
            if protocol == 's3':
                if isinstance(fpath, list):
                    get_legacy_fs().info(fpath[0])
                else:
                    get_legacy_fs().info(fpath)
            if protocol in {'hdfs', 'abfs', 'abfss'}:
                prefix = f'{protocol}://{srx__alwm.netloc}'
                if isinstance(fpath, list):
                    mub__gbmi = [toutp__tky[len(prefix):] for toutp__tky in
                        fpath]
                else:
                    mub__gbmi = fpath[len(prefix):]
            else:
                mub__gbmi = fpath
            gye__byz = pq.ParquetDataset(mub__gbmi, filesystem=
                get_legacy_fs(), filters=None, use_legacy_dataset=True,
                validate_schema=False, metadata_nthreads=jdk__vvn)
            pa.set_io_thread_count(hmb__lhiwa)
            if typing_pa_schema:
                yswol__meymd = typing_pa_schema
            else:
                yswol__meymd = bodo.io.pa_parquet.get_dataset_schema(gye__byz)
            if dnf_filters:
                if get_row_counts:
                    dxkj__tps.add_attribute('num_pieces_before_filter', len
                        (gye__byz.pieces))
                jwpg__tlgab = time.time()
                gye__byz._filter(dnf_filters)
                if get_row_counts:
                    dxkj__tps.add_attribute('dnf_filter_time', time.time() -
                        jwpg__tlgab)
                    dxkj__tps.add_attribute('num_pieces_after_filter', len(
                        gye__byz.pieces))
            if get_row_counts:
                dxkj__tps.finalize()
            gye__byz._metadata.fs = None
        except Exception as lidvv__kna:
            if isinstance(fpath, list) and isinstance(lidvv__kna, (OSError,
                FileNotFoundError)):
                lidvv__kna = BodoError(str(lidvv__kna) +
                    list_of_files_error_msg)
            else:
                lidvv__kna = BodoError(
                    f"""error from pyarrow: {type(lidvv__kna).__name__}: {str(lidvv__kna)}
"""
                    )
            ychee__unepf.bcast(lidvv__kna)
            raise lidvv__kna
        if get_row_counts:
            cly__cnzlh = tracing.Event('bcast dataset')
        ychee__unepf.bcast(gye__byz)
        ychee__unepf.bcast(yswol__meymd)
    else:
        if get_row_counts:
            cly__cnzlh = tracing.Event('bcast dataset')
        gye__byz = ychee__unepf.bcast(None)
        if isinstance(gye__byz, Exception):
            juvfe__mvx = gye__byz
            raise juvfe__mvx
        yswol__meymd = ychee__unepf.bcast(None)
    uis__lmi = set(yswol__meymd.names)
    if get_row_counts:
        mwevw__lfx = getfs()
    else:
        mwevw__lfx = get_legacy_fs()
    gye__byz._metadata.fs = mwevw__lfx
    if get_row_counts:
        cly__cnzlh.finalize()
    gye__byz._bodo_total_rows = 0
    if get_row_counts and tot_rows_to_read == 0:
        get_row_counts = ggrh__wlq = False
        for wbak__xkhvd in gye__byz.pieces:
            wbak__xkhvd._bodo_num_rows = 0
    if get_row_counts or ggrh__wlq:
        if get_row_counts and tracing.is_tracing():
            hil__umtuu = tracing.Event('get_row_counts')
            hil__umtuu.add_attribute('g_num_pieces', len(gye__byz.pieces))
            hil__umtuu.add_attribute('g_expr_filters', str(expr_filters))
        yli__sncbm = 0.0
        num_pieces = len(gye__byz.pieces)
        start = get_start(num_pieces, bodo.get_size(), bodo.get_rank())
        dwaoq__xzq = get_end(num_pieces, bodo.get_size(), bodo.get_rank())
        mau__wbd = 0
        goryw__sfwx = 0
        glxx__slx = 0
        bzk__bxjl = True
        if expr_filters is not None:
            import random
            random.seed(37)
            ibu__tku = random.sample(gye__byz.pieces, k=len(gye__byz.pieces))
        else:
            ibu__tku = gye__byz.pieces
        for wbak__xkhvd in ibu__tku:
            wbak__xkhvd._bodo_num_rows = 0
        fpaths = [wbak__xkhvd.path for wbak__xkhvd in ibu__tku[start:
            dwaoq__xzq]]
        if protocol == 's3':
            ucfhu__gjm = srx__alwm.netloc
            prefix = 's3://' + ucfhu__gjm + '/'
            fpaths = [toutp__tky[len(prefix):] for toutp__tky in fpaths]
            mwevw__lfx = get_s3_subtree_fs(ucfhu__gjm, region=getfs().
                region, storage_options=storage_options)
        else:
            mwevw__lfx = getfs()
        jdk__vvn = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), 4)
        pa.set_io_thread_count(jdk__vvn)
        pa.set_cpu_count(jdk__vvn)
        juvfe__mvx = None
        try:
            wge__tnkp = ds.dataset(fpaths, filesystem=mwevw__lfx,
                partitioning=ds.partitioning(flavor='hive') if gye__byz.
                partitions else None)
            for voa__rlso, tfsbk__rdot in zip(ibu__tku[start:dwaoq__xzq],
                wge__tnkp.get_fragments()):
                if ggrh__wlq:
                    npa__xadz = tfsbk__rdot.metadata.schema.to_arrow_schema()
                    gaf__iqzo = set(npa__xadz.names)
                    if uis__lmi != gaf__iqzo:
                        yek__swakc = gaf__iqzo - uis__lmi
                        zisz__mqxk = uis__lmi - gaf__iqzo
                        emcd__fpq = f'Schema in {voa__rlso} was different.\n'
                        if yek__swakc:
                            emcd__fpq += f"""File contains column(s) {yek__swakc} not found in other files in the dataset.
"""
                        if zisz__mqxk:
                            emcd__fpq += f"""File missing column(s) {zisz__mqxk} found in other files in the dataset.
"""
                        raise BodoError(emcd__fpq)
                    try:
                        yswol__meymd = pa.unify_schemas([yswol__meymd,
                            npa__xadz])
                    except Exception as lidvv__kna:
                        emcd__fpq = (
                            f'Schema in {voa__rlso} was different.\n' + str
                            (lidvv__kna))
                        raise BodoError(emcd__fpq)
                jwpg__tlgab = time.time()
                ryqhh__ocq = tfsbk__rdot.scanner(schema=wge__tnkp.schema,
                    filter=expr_filters, use_threads=True).count_rows()
                yli__sncbm += time.time() - jwpg__tlgab
                voa__rlso._bodo_num_rows = ryqhh__ocq
                mau__wbd += ryqhh__ocq
                goryw__sfwx += tfsbk__rdot.num_row_groups
                glxx__slx += sum(jdxk__gcili.total_byte_size for
                    jdxk__gcili in tfsbk__rdot.row_groups)
        except Exception as lidvv__kna:
            juvfe__mvx = lidvv__kna
        if ychee__unepf.allreduce(juvfe__mvx is not None, op=MPI.LOR):
            for juvfe__mvx in ychee__unepf.allgather(juvfe__mvx):
                if juvfe__mvx:
                    if isinstance(fpath, list) and isinstance(juvfe__mvx, (
                        OSError, FileNotFoundError)):
                        raise BodoError(str(juvfe__mvx) +
                            list_of_files_error_msg)
                    raise juvfe__mvx
        if ggrh__wlq:
            bzk__bxjl = ychee__unepf.allreduce(bzk__bxjl, op=MPI.LAND)
            if not bzk__bxjl:
                raise BodoError("Schema in parquet files don't match")
        if get_row_counts:
            gye__byz._bodo_total_rows = ychee__unepf.allreduce(mau__wbd, op
                =MPI.SUM)
            keo__agrp = ychee__unepf.allreduce(goryw__sfwx, op=MPI.SUM)
            fnm__zlqm = ychee__unepf.allreduce(glxx__slx, op=MPI.SUM)
            zqoth__rtf = np.array([wbak__xkhvd._bodo_num_rows for
                wbak__xkhvd in gye__byz.pieces])
            zqoth__rtf = ychee__unepf.allreduce(zqoth__rtf, op=MPI.SUM)
            for wbak__xkhvd, utnp__mbw in zip(gye__byz.pieces, zqoth__rtf):
                wbak__xkhvd._bodo_num_rows = utnp__mbw
            if is_parallel and bodo.get_rank(
                ) == 0 and keo__agrp < bodo.get_size() and keo__agrp != 0:
                warnings.warn(BodoWarning(
                    f"""Total number of row groups in parquet dataset {fpath} ({keo__agrp}) is too small for effective IO parallelization.
For best performance the number of row groups should be greater than the number of workers ({bodo.get_size()}). For more details, refer to
https://docs.bodo.ai/latest/file_io/#parquet-section.
"""
                    ))
            if keo__agrp == 0:
                bxct__noa = 0
            else:
                bxct__noa = fnm__zlqm // keo__agrp
            if (bodo.get_rank() == 0 and fnm__zlqm >= 20 * 1048576 and 
                bxct__noa < 1048576 and protocol in REMOTE_FILESYSTEMS):
                warnings.warn(BodoWarning(
                    f'Parquet average row group size is small ({bxct__noa} bytes) and can have negative impact on performance when reading from remote sources'
                    ))
            if tracing.is_tracing():
                hil__umtuu.add_attribute('g_total_num_row_groups', keo__agrp)
                hil__umtuu.add_attribute('total_scan_time', yli__sncbm)
                qte__jiowo = np.array([wbak__xkhvd._bodo_num_rows for
                    wbak__xkhvd in gye__byz.pieces])
                tcv__yhz = np.percentile(qte__jiowo, [25, 50, 75])
                hil__umtuu.add_attribute('g_row_counts_min', qte__jiowo.min())
                hil__umtuu.add_attribute('g_row_counts_Q1', tcv__yhz[0])
                hil__umtuu.add_attribute('g_row_counts_median', tcv__yhz[1])
                hil__umtuu.add_attribute('g_row_counts_Q3', tcv__yhz[2])
                hil__umtuu.add_attribute('g_row_counts_max', qte__jiowo.max())
                hil__umtuu.add_attribute('g_row_counts_mean', qte__jiowo.mean()
                    )
                hil__umtuu.add_attribute('g_row_counts_std', qte__jiowo.std())
                hil__umtuu.add_attribute('g_row_counts_sum', qte__jiowo.sum())
                hil__umtuu.finalize()
    gye__byz._prefix = ''
    if protocol in {'hdfs', 'abfs', 'abfss'}:
        prefix = f'{protocol}://{srx__alwm.netloc}'
        if len(gye__byz.pieces) > 0:
            voa__rlso = gye__byz.pieces[0]
            if not voa__rlso.path.startswith(prefix):
                gye__byz._prefix = prefix
    if read_categories:
        _add_categories_to_pq_dataset(gye__byz)
    if get_row_counts:
        ngwfk__umduz.finalize()
    if ggrh__wlq and is_parallel:
        if tracing.is_tracing():
            yzw__ddjbf = tracing.Event('unify_schemas_across_ranks')
        juvfe__mvx = None
        try:
            yswol__meymd = ychee__unepf.allreduce(yswol__meymd, bodo.io.
                helpers.pa_schema_unify_mpi_op)
        except Exception as lidvv__kna:
            juvfe__mvx = lidvv__kna
        if tracing.is_tracing():
            yzw__ddjbf.finalize()
        if ychee__unepf.allreduce(juvfe__mvx is not None, op=MPI.LOR):
            for juvfe__mvx in ychee__unepf.allgather(juvfe__mvx):
                if juvfe__mvx:
                    emcd__fpq = (f'Schema in some files were different.\n' +
                        str(juvfe__mvx))
                    raise BodoError(emcd__fpq)
    gye__byz._bodo_arrow_schema = yswol__meymd
    return gye__byz


def get_scanner_batches(fpaths, expr_filters, selected_fields,
    avg_num_pieces, is_parallel, storage_options, region, prefix,
    str_as_dict_cols, start_offset, rows_to_read, has_partitions, schema):
    import pyarrow as pa
    nxb__oof = os.cpu_count()
    if nxb__oof is None or nxb__oof == 0:
        nxb__oof = 2
    dpmeq__ofxl = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), nxb__oof)
    fjv__lerd = min(int(os.environ.get('BODO_MAX_IO_THREADS', 16)), nxb__oof)
    if is_parallel and len(fpaths) > fjv__lerd and len(fpaths
        ) / avg_num_pieces >= 2.0:
        pa.set_io_thread_count(fjv__lerd)
        pa.set_cpu_count(fjv__lerd)
    else:
        pa.set_io_thread_count(dpmeq__ofxl)
        pa.set_cpu_count(dpmeq__ofxl)
    if fpaths[0].startswith('s3://'):
        ucfhu__gjm = urlparse(fpaths[0]).netloc
        prefix = 's3://' + ucfhu__gjm + '/'
        fpaths = [toutp__tky[len(prefix):] for toutp__tky in fpaths]
        if region == '':
            region = get_s3_bucket_region_njit(fpaths[0], parallel=False)
        mwevw__lfx = get_s3_subtree_fs(ucfhu__gjm, region=region,
            storage_options=storage_options)
    elif prefix and prefix.startswith(('hdfs', 'abfs', 'abfss')):
        mwevw__lfx = get_hdfs_fs(prefix + fpaths[0])
    elif fpaths[0].startswith(('gcs', 'gs')):
        import gcsfs
        mwevw__lfx = gcsfs.GCSFileSystem(token=None)
    else:
        mwevw__lfx = None
    asj__erkzv = ds.ParquetFileFormat(dictionary_columns=str_as_dict_cols)
    gye__byz = ds.dataset(fpaths, filesystem=mwevw__lfx, partitioning=ds.
        partitioning(flavor='hive') if has_partitions else None, format=
        asj__erkzv)
    wvqr__igvh = set(str_as_dict_cols)
    ektla__aunnv = schema.names
    for chbt__opa, name in enumerate(ektla__aunnv):
        if name in wvqr__igvh:
            mdvdm__gtdb = schema.field(chbt__opa)
            zdm__obb = pa.field(name, pa.dictionary(pa.int32(), mdvdm__gtdb
                .type), mdvdm__gtdb.nullable)
            schema = schema.remove(chbt__opa).insert(chbt__opa, zdm__obb)
    gye__byz = gye__byz.replace_schema(pa.unify_schemas([gye__byz.schema,
        schema]))
    col_names = gye__byz.schema.names
    jggyz__gov = [col_names[ljy__ibc] for ljy__ibc in selected_fields]
    bwam__piv = len(fpaths) <= 3 or start_offset > 0 and len(fpaths) <= 10
    if bwam__piv and expr_filters is None:
        arhx__rgonn = []
        juibn__vgv = 0
        uvd__bxa = 0
        for tfsbk__rdot in gye__byz.get_fragments():
            eprxx__blg = []
            for jdxk__gcili in tfsbk__rdot.row_groups:
                iggvf__cwi = jdxk__gcili.num_rows
                if start_offset < juibn__vgv + iggvf__cwi:
                    if uvd__bxa == 0:
                        ncjcg__aqm = start_offset - juibn__vgv
                        ucbho__hif = min(iggvf__cwi - ncjcg__aqm, rows_to_read)
                    else:
                        ucbho__hif = min(iggvf__cwi, rows_to_read - uvd__bxa)
                    uvd__bxa += ucbho__hif
                    eprxx__blg.append(jdxk__gcili.id)
                juibn__vgv += iggvf__cwi
                if uvd__bxa == rows_to_read:
                    break
            arhx__rgonn.append(tfsbk__rdot.subset(row_group_ids=eprxx__blg))
            if uvd__bxa == rows_to_read:
                break
        gye__byz = ds.FileSystemDataset(arhx__rgonn, gye__byz.schema,
            asj__erkzv, filesystem=gye__byz.filesystem)
        start_offset = ncjcg__aqm
    rsbp__htx = gye__byz.scanner(columns=jggyz__gov, filter=expr_filters,
        use_threads=True).to_reader()
    return gye__byz, rsbp__htx, start_offset


def _add_categories_to_pq_dataset(pq_dataset):
    import pyarrow as pa
    from mpi4py import MPI
    if len(pq_dataset.pieces) < 1:
        raise BodoError(
            'No pieces found in Parquet dataset. Cannot get read categorical values'
            )
    pa_schema = pq_dataset.schema.to_arrow_schema()
    qawqd__xkx = [c for c in pa_schema.names if isinstance(pa_schema.field(
        c).type, pa.DictionaryType)]
    if len(qawqd__xkx) == 0:
        pq_dataset._category_info = {}
        return
    ychee__unepf = MPI.COMM_WORLD
    if bodo.get_rank() == 0:
        try:
            gcvay__avpjt = pq_dataset.pieces[0].open()
            jdxk__gcili = gcvay__avpjt.read_row_group(0, qawqd__xkx)
            category_info = {c: tuple(jdxk__gcili.column(c).chunk(0).
                dictionary.to_pylist()) for c in qawqd__xkx}
            del gcvay__avpjt, jdxk__gcili
        except Exception as lidvv__kna:
            ychee__unepf.bcast(lidvv__kna)
            raise lidvv__kna
        ychee__unepf.bcast(category_info)
    else:
        category_info = ychee__unepf.bcast(None)
        if isinstance(category_info, Exception):
            juvfe__mvx = category_info
            raise juvfe__mvx
    pq_dataset._category_info = category_info


def get_pandas_metadata(schema, num_pieces):
    agx__zmjuf = None
    nullable_from_metadata = defaultdict(lambda : None)
    supfr__jbqj = b'pandas'
    if schema.metadata is not None and supfr__jbqj in schema.metadata:
        import json
        luna__ducz = json.loads(schema.metadata[supfr__jbqj].decode('utf8'))
        tmzou__hegfi = len(luna__ducz['index_columns'])
        if tmzou__hegfi > 1:
            raise BodoError('read_parquet: MultiIndex not supported yet')
        agx__zmjuf = luna__ducz['index_columns'][0] if tmzou__hegfi else None
        if not isinstance(agx__zmjuf, str) and not isinstance(agx__zmjuf, dict
            ):
            agx__zmjuf = None
        for dxnwf__rdr in luna__ducz['columns']:
            tieli__npsdh = dxnwf__rdr['name']
            if dxnwf__rdr['pandas_type'].startswith('int'
                ) and tieli__npsdh is not None:
                if dxnwf__rdr['numpy_type'].startswith('Int'):
                    nullable_from_metadata[tieli__npsdh] = True
                else:
                    nullable_from_metadata[tieli__npsdh] = False
    return agx__zmjuf, nullable_from_metadata


def get_str_columns_from_pa_schema(pa_schema):
    str_columns = []
    for tieli__npsdh in pa_schema.names:
        jaqd__xiaaj = pa_schema.field(tieli__npsdh)
        if jaqd__xiaaj.type == pa.string():
            str_columns.append(tieli__npsdh)
    return str_columns


def determine_str_as_dict_columns(pq_dataset, pa_schema, str_columns):
    from mpi4py import MPI
    ychee__unepf = MPI.COMM_WORLD
    if len(str_columns) == 0:
        return set()
    if len(pq_dataset.pieces) > bodo.get_size():
        import random
        random.seed(37)
        ibu__tku = random.sample(pq_dataset.pieces, bodo.get_size())
    else:
        ibu__tku = pq_dataset.pieces
    mbg__lrl = np.zeros(len(str_columns), dtype=np.int64)
    gsrgg__lid = np.zeros(len(str_columns), dtype=np.int64)
    if bodo.get_rank() < len(ibu__tku):
        voa__rlso = ibu__tku[bodo.get_rank()]
        try:
            lwbnr__gje = voa__rlso.get_metadata()
            for chbt__opa in range(lwbnr__gje.num_row_groups):
                for eule__nfj, tieli__npsdh in enumerate(str_columns):
                    fybi__dalq = pa_schema.get_field_index(tieli__npsdh)
                    mbg__lrl[eule__nfj] += lwbnr__gje.row_group(chbt__opa
                        ).column(fybi__dalq).total_uncompressed_size
            crybr__gwzgc = lwbnr__gje.num_rows
        except Exception as lidvv__kna:
            if isinstance(lidvv__kna, (OSError, FileNotFoundError)):
                crybr__gwzgc = 0
            else:
                raise
    else:
        crybr__gwzgc = 0
    uazus__uzidp = ychee__unepf.allreduce(crybr__gwzgc, op=MPI.SUM)
    if uazus__uzidp == 0:
        return set()
    ychee__unepf.Allreduce(mbg__lrl, gsrgg__lid, op=MPI.SUM)
    tnc__gejz = gsrgg__lid / uazus__uzidp
    str_as_dict = set()
    for chbt__opa, hwdu__oxt in enumerate(tnc__gejz):
        if hwdu__oxt < READ_STR_AS_DICT_THRESHOLD:
            tieli__npsdh = str_columns[chbt__opa][0]
            str_as_dict.add(tieli__npsdh)
    return str_as_dict


def parquet_file_schema(file_name, selected_columns, storage_options=None,
    input_file_name_col=None, read_as_dict_cols=None):
    col_names = []
    jlv__ewct = []
    pq_dataset = get_parquet_dataset(file_name, get_row_counts=False,
        storage_options=storage_options, read_categories=True)
    if hasattr(pq_dataset, '_bodo_arrow_schema'):
        pa_schema = pq_dataset._bodo_arrow_schema
    else:
        pa_schema = pq_dataset.schema.to_arrow_schema()
    partition_names = [] if pq_dataset.partitions is None else [pq_dataset.
        partitions.levels[chbt__opa].name for chbt__opa in range(len(
        pq_dataset.partitions.partition_names))]
    num_pieces = len(pq_dataset.pieces)
    str_columns = get_str_columns_from_pa_schema(pa_schema)
    yme__tewdv = set(str_columns)
    if read_as_dict_cols is None:
        read_as_dict_cols = []
    read_as_dict_cols = set(read_as_dict_cols)
    khu__dnfhr = read_as_dict_cols - yme__tewdv
    if len(khu__dnfhr) > 0:
        if bodo.get_rank() == 0:
            warnings.warn(
                f'The following columns are not of datatype string and hence cannot be read with dictionary encoding: {khu__dnfhr}'
                , bodo.utils.typing.BodoWarning)
    read_as_dict_cols.intersection_update(yme__tewdv)
    yme__tewdv = yme__tewdv - read_as_dict_cols
    str_columns = [tmfuh__xldi for tmfuh__xldi in str_columns if 
        tmfuh__xldi in yme__tewdv]
    str_as_dict: set = determine_str_as_dict_columns(pq_dataset, pa_schema,
        str_columns)
    str_as_dict.update(read_as_dict_cols)
    col_names = pa_schema.names
    agx__zmjuf, nullable_from_metadata = get_pandas_metadata(pa_schema,
        num_pieces)
    nbph__mxd = []
    ofx__lwu = []
    fhht__xzeyt = []
    for chbt__opa, c in enumerate(col_names):
        jaqd__xiaaj = pa_schema.field(c)
        tzx__yjd, oanzq__aaic = _get_numba_typ_from_pa_typ(jaqd__xiaaj, c ==
            agx__zmjuf, nullable_from_metadata[c], pq_dataset.
            _category_info, str_as_dict=c in str_as_dict)
        nbph__mxd.append(tzx__yjd)
        ofx__lwu.append(oanzq__aaic)
        fhht__xzeyt.append(jaqd__xiaaj.type)
    if partition_names:
        col_names += partition_names
        nbph__mxd += [_get_partition_cat_dtype(pq_dataset.partitions.levels
            [chbt__opa]) for chbt__opa in range(len(partition_names))]
        ofx__lwu.extend([True] * len(partition_names))
        fhht__xzeyt.extend([None] * len(partition_names))
    if input_file_name_col is not None:
        col_names += [input_file_name_col]
        nbph__mxd += [dict_str_arr_type]
        ofx__lwu.append(True)
        fhht__xzeyt.append(None)
    dqwfj__phkvz = {c: chbt__opa for chbt__opa, c in enumerate(col_names)}
    if selected_columns is None:
        selected_columns = col_names
    for c in selected_columns:
        if c not in dqwfj__phkvz:
            raise BodoError(f'Selected column {c} not in Parquet file schema')
    if agx__zmjuf and not isinstance(agx__zmjuf, dict
        ) and agx__zmjuf not in selected_columns:
        selected_columns.append(agx__zmjuf)
    col_names = selected_columns
    col_indices = []
    jlv__ewct = []
    djnr__nlovd = []
    baqg__fxeh = []
    for chbt__opa, c in enumerate(col_names):
        rrvv__fei = dqwfj__phkvz[c]
        col_indices.append(rrvv__fei)
        jlv__ewct.append(nbph__mxd[rrvv__fei])
        if not ofx__lwu[rrvv__fei]:
            djnr__nlovd.append(chbt__opa)
            baqg__fxeh.append(fhht__xzeyt[rrvv__fei])
    return (col_names, jlv__ewct, agx__zmjuf, col_indices, partition_names,
        djnr__nlovd, baqg__fxeh)


def _get_partition_cat_dtype(part_set):
    ysj__uuzq = part_set.dictionary.to_pandas()
    xdpcx__onzt = bodo.typeof(ysj__uuzq).dtype
    tnbv__rum = PDCategoricalDtype(tuple(ysj__uuzq), xdpcx__onzt, False)
    return CategoricalArrayType(tnbv__rum)


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
        roamj__wnski = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(32), lir.IntType(32),
            lir.IntType(32), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        jtvx__due = cgutils.get_or_insert_function(builder.module,
            roamj__wnski, name='pq_write')
        builder.call(jtvx__due, args)
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
        roamj__wnski = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        jtvx__due = cgutils.get_or_insert_function(builder.module,
            roamj__wnski, name='pq_write_partitioned')
        builder.call(jtvx__due, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
    return types.void(types.voidptr, data_table_t, col_names_t,
        col_names_no_partitions_t, cat_table_t, types.voidptr, types.int32,
        types.voidptr, types.boolean, types.voidptr, types.int64), codegen
