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
        except OSError as cjsma__sluoo:
            if 'non-file path' in str(cjsma__sluoo):
                raise FileNotFoundError(str(cjsma__sluoo))
            raise


class ParquetHandler:

    def __init__(self, func_ir, typingctx, args, _locals):
        self.func_ir = func_ir
        self.typingctx = typingctx
        self.args = args
        self.locals = _locals

    def gen_parquet_read(self, file_name, lhs, columns, storage_options=
        None, input_file_name_col=None, read_as_dict_cols=None):
        lbjgw__fmmv = lhs.scope
        aaf__wzr = lhs.loc
        jgvta__bwl = None
        if lhs.name in self.locals:
            jgvta__bwl = self.locals[lhs.name]
            self.locals.pop(lhs.name)
        umvi__fnlch = {}
        if lhs.name + ':convert' in self.locals:
            umvi__fnlch = self.locals[lhs.name + ':convert']
            self.locals.pop(lhs.name + ':convert')
        if jgvta__bwl is None:
            hmbck__ser = (
                'Parquet schema not available. Either path argument should be constant for Bodo to look at the file at compile time or schema should be provided. For more information, see: https://docs.bodo.ai/latest/file_io/#parquet-section.'
                )
            fojt__yyg = get_const_value(file_name, self.func_ir, hmbck__ser,
                arg_types=self.args, file_info=ParquetFileInfo(columns,
                storage_options=storage_options, input_file_name_col=
                input_file_name_col, read_as_dict_cols=read_as_dict_cols))
            oenba__fdaxb = False
            hxjl__smvca = guard(get_definition, self.func_ir, file_name)
            if isinstance(hxjl__smvca, ir.Arg):
                typ = self.args[hxjl__smvca.index]
                if isinstance(typ, types.FilenameType):
                    (col_names, fnasq__kcqxf, qocxb__lkmu, col_indices,
                        partition_names, toc__lgqc, pkq__pabk) = typ.schema
                    oenba__fdaxb = True
            if not oenba__fdaxb:
                (col_names, fnasq__kcqxf, qocxb__lkmu, col_indices,
                    partition_names, toc__lgqc, pkq__pabk) = (
                    parquet_file_schema(fojt__yyg, columns, storage_options
                    =storage_options, input_file_name_col=
                    input_file_name_col, read_as_dict_cols=read_as_dict_cols))
        else:
            kdj__bvn = list(jgvta__bwl.keys())
            mhqk__hfpm = {c: bcy__pxo for bcy__pxo, c in enumerate(kdj__bvn)}
            touyl__xdara = [lur__qnjo for lur__qnjo in jgvta__bwl.values()]
            qocxb__lkmu = 'index' if 'index' in mhqk__hfpm else None
            if columns is None:
                selected_columns = kdj__bvn
            else:
                selected_columns = columns
            col_indices = [mhqk__hfpm[c] for c in selected_columns]
            fnasq__kcqxf = [touyl__xdara[mhqk__hfpm[c]] for c in
                selected_columns]
            col_names = selected_columns
            qocxb__lkmu = qocxb__lkmu if qocxb__lkmu in col_names else None
            partition_names = []
            toc__lgqc = []
            pkq__pabk = []
        bwuxy__sct = None if isinstance(qocxb__lkmu, dict
            ) or qocxb__lkmu is None else qocxb__lkmu
        index_column_index = None
        index_column_type = types.none
        if bwuxy__sct:
            fsn__ghgm = col_names.index(bwuxy__sct)
            index_column_index = col_indices.pop(fsn__ghgm)
            index_column_type = fnasq__kcqxf.pop(fsn__ghgm)
            col_names.pop(fsn__ghgm)
        for bcy__pxo, c in enumerate(col_names):
            if c in umvi__fnlch:
                fnasq__kcqxf[bcy__pxo] = umvi__fnlch[c]
        xki__eryvv = [ir.Var(lbjgw__fmmv, mk_unique_var('pq_table'),
            aaf__wzr), ir.Var(lbjgw__fmmv, mk_unique_var('pq_index'), aaf__wzr)
            ]
        lrwaa__qtc = [bodo.ir.parquet_ext.ParquetReader(file_name, lhs.name,
            col_names, col_indices, fnasq__kcqxf, xki__eryvv, aaf__wzr,
            partition_names, storage_options, index_column_index,
            index_column_type, input_file_name_col, toc__lgqc, pkq__pabk)]
        return (col_names, xki__eryvv, qocxb__lkmu, lrwaa__qtc,
            fnasq__kcqxf, index_column_type)


def pq_distributed_run(pq_node, array_dists, typemap, calltypes, typingctx,
    targetctx, meta_head_only_info=None):
    cvvq__fwccf = len(pq_node.out_vars)
    dnf_filter_str = 'None'
    expr_filter_str = 'None'
    illi__dbxqo, lxqog__xase = bodo.ir.connector.generate_filter_map(pq_node
        .filters)
    extra_args = ', '.join(illi__dbxqo.values())
    dnf_filter_str, expr_filter_str = bodo.ir.connector.generate_arrow_filters(
        pq_node.filters, illi__dbxqo, lxqog__xase, pq_node.
        original_df_colnames, pq_node.partition_names, pq_node.
        original_out_types, typemap, 'parquet')
    ssj__hjffl = ', '.join(f'out{bcy__pxo}' for bcy__pxo in range(cvvq__fwccf))
    cnd__cmww = f'def pq_impl(fname, {extra_args}):\n'
    cnd__cmww += (
        f'    (total_rows, {ssj__hjffl},) = _pq_reader_py(fname, {extra_args})\n'
        )
    igm__rdebd = {}
    exec(cnd__cmww, {}, igm__rdebd)
    hqowf__drg = igm__rdebd['pq_impl']
    if bodo.user_logging.get_verbose_level() >= 1:
        irz__xtfex = pq_node.loc.strformat()
        vcxta__keqp = []
        fmynt__avwvo = []
        for bcy__pxo in pq_node.type_usecol_offset:
            jost__ddmy = pq_node.df_colnames[bcy__pxo]
            vcxta__keqp.append(jost__ddmy)
            if isinstance(pq_node.out_types[bcy__pxo], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                fmynt__avwvo.append(jost__ddmy)
        znyc__jihx = (
            'Finish column pruning on read_parquet node:\n%s\nColumns loaded %s\n'
            )
        bodo.user_logging.log_message('Column Pruning', znyc__jihx,
            irz__xtfex, vcxta__keqp)
        if fmynt__avwvo:
            iif__ymjpi = """Finished optimized encoding on read_parquet node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', iif__ymjpi,
                irz__xtfex, fmynt__avwvo)
    parallel = bodo.ir.connector.is_connector_table_parallel(pq_node,
        array_dists, typemap, 'ParquetReader')
    if pq_node.unsupported_columns:
        pjfv__uxgfy = set(pq_node.type_usecol_offset)
        nef__dwn = set(pq_node.unsupported_columns)
        wqizr__xspvi = pjfv__uxgfy & nef__dwn
        if wqizr__xspvi:
            tduc__clbd = sorted(wqizr__xspvi)
            zytqh__ltmin = [
                f'pandas.read_parquet(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                "Please manually remove these columns from your read_parquet with the 'columns' argument. If these "
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            zmh__sqaf = 0
            for rbav__cpucy in tduc__clbd:
                while pq_node.unsupported_columns[zmh__sqaf] != rbav__cpucy:
                    zmh__sqaf += 1
                zytqh__ltmin.append(
                    f"Column '{pq_node.df_colnames[rbav__cpucy]}' with unsupported arrow type {pq_node.unsupported_arrow_types[zmh__sqaf]}"
                    )
                zmh__sqaf += 1
            rpjf__ofjeb = '\n'.join(zytqh__ltmin)
            raise BodoError(rpjf__ofjeb, loc=pq_node.loc)
    jwwe__mfw = _gen_pq_reader_py(pq_node.df_colnames, pq_node.col_indices,
        pq_node.type_usecol_offset, pq_node.out_types, pq_node.
        storage_options, pq_node.partition_names, dnf_filter_str,
        expr_filter_str, extra_args, parallel, meta_head_only_info, pq_node
        .index_column_index, pq_node.index_column_type, pq_node.
        input_file_name_col)
    cds__czz = typemap[pq_node.file_name.name]
    xxn__xzi = (cds__czz,) + tuple(typemap[eor__dzz.name] for eor__dzz in
        lxqog__xase)
    yhjce__ifntz = compile_to_numba_ir(hqowf__drg, {'_pq_reader_py':
        jwwe__mfw}, typingctx=typingctx, targetctx=targetctx, arg_typs=
        xxn__xzi, typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(yhjce__ifntz, [pq_node.file_name] + lxqog__xase)
    lrwaa__qtc = yhjce__ifntz.body[:-3]
    if meta_head_only_info:
        lrwaa__qtc[-1 - cvvq__fwccf].target = meta_head_only_info[1]
    lrwaa__qtc[-2].target = pq_node.out_vars[0]
    lrwaa__qtc[-1].target = pq_node.out_vars[1]
    assert not (pq_node.index_column_index is None and not pq_node.
        type_usecol_offset
        ), 'At most one of table and index should be dead if the Parquet IR node is live'
    if pq_node.index_column_index is None:
        lrwaa__qtc.pop(-1)
    elif not pq_node.type_usecol_offset:
        lrwaa__qtc.pop(-2)
    return lrwaa__qtc


distributed_pass.distributed_run_extensions[bodo.ir.parquet_ext.ParquetReader
    ] = pq_distributed_run


def get_filters_pyobject(dnf_filter_str, expr_filter_str, vars):
    pass


@overload(get_filters_pyobject, no_unliteral=True)
def overload_get_filters_pyobject(dnf_filter_str, expr_filter_str, var_tup):
    qtfmj__ycb = get_overload_const_str(dnf_filter_str)
    wor__tiicj = get_overload_const_str(expr_filter_str)
    xjfn__jty = ', '.join(f'f{bcy__pxo}' for bcy__pxo in range(len(var_tup)))
    cnd__cmww = 'def impl(dnf_filter_str, expr_filter_str, var_tup):\n'
    if len(var_tup):
        cnd__cmww += f'  {xjfn__jty}, = var_tup\n'
    cnd__cmww += """  with numba.objmode(dnf_filters_py='parquet_predicate_type', expr_filters_py='parquet_predicate_type'):
"""
    cnd__cmww += f'    dnf_filters_py = {qtfmj__ycb}\n'
    cnd__cmww += f'    expr_filters_py = {wor__tiicj}\n'
    cnd__cmww += '  return (dnf_filters_py, expr_filters_py)\n'
    igm__rdebd = {}
    exec(cnd__cmww, globals(), igm__rdebd)
    return igm__rdebd['impl']


@numba.njit
def get_fname_pyobject(fname):
    with numba.objmode(fname_py='read_parquet_fpath_type'):
        fname_py = fname
    return fname_py


def _gen_pq_reader_py(col_names, col_indices, type_usecol_offset, out_types,
    storage_options, partition_names, dnf_filter_str, expr_filter_str,
    extra_args, is_parallel, meta_head_only_info, index_column_index,
    index_column_type, input_file_name_col):
    jxqzf__mcmm = next_label()
    pvhkb__rzynq = ',' if extra_args else ''
    cnd__cmww = f'def pq_reader_py(fname,{extra_args}):\n'
    cnd__cmww += (
        f"    ev = bodo.utils.tracing.Event('read_parquet', {is_parallel})\n")
    cnd__cmww += f"    ev.add_attribute('g_fname', fname)\n"
    cnd__cmww += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={is_parallel})
"""
    cnd__cmww += f"""    dnf_filters, expr_filters = get_filters_pyobject("{dnf_filter_str}", "{expr_filter_str}", ({extra_args}{pvhkb__rzynq}))
"""
    cnd__cmww += '    fname_py = get_fname_pyobject(fname)\n'
    storage_options['bodo_dummy'] = 'dummy'
    cnd__cmww += (
        f'    storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    tot_rows_to_read = -1
    if meta_head_only_info and meta_head_only_info[0] is not None:
        tot_rows_to_read = meta_head_only_info[0]
    aml__rgr = not type_usecol_offset
    kgda__wtrz = [sanitize_varname(c) for c in col_names]
    partition_names = [sanitize_varname(c) for c in partition_names]
    input_file_name_col = sanitize_varname(input_file_name_col
        ) if input_file_name_col is not None and col_names.index(
        input_file_name_col) in type_usecol_offset else None
    efns__syf = {c: bcy__pxo for bcy__pxo, c in enumerate(col_indices)}
    suz__rubvq = {c: bcy__pxo for bcy__pxo, c in enumerate(kgda__wtrz)}
    ssge__qmik = []
    lkrvu__uuqq = set()
    zlnkw__rfyh = partition_names + [input_file_name_col]
    for bcy__pxo in type_usecol_offset:
        if kgda__wtrz[bcy__pxo] not in zlnkw__rfyh:
            ssge__qmik.append(col_indices[bcy__pxo])
        elif not input_file_name_col or kgda__wtrz[bcy__pxo
            ] != input_file_name_col:
            lkrvu__uuqq.add(col_indices[bcy__pxo])
    if index_column_index is not None:
        ssge__qmik.append(index_column_index)
    ssge__qmik = sorted(ssge__qmik)
    fhs__rckzg = {c: bcy__pxo for bcy__pxo, c in enumerate(ssge__qmik)}
    wbyby__ijl = [(int(is_nullable(out_types[efns__syf[eap__urqqy]])) if 
        eap__urqqy != index_column_index else int(is_nullable(
        index_column_type))) for eap__urqqy in ssge__qmik]
    str_as_dict_cols = []
    for eap__urqqy in ssge__qmik:
        if eap__urqqy == index_column_index:
            lur__qnjo = index_column_type
        else:
            lur__qnjo = out_types[efns__syf[eap__urqqy]]
        if lur__qnjo == dict_str_arr_type:
            str_as_dict_cols.append(eap__urqqy)
    xxa__nip = []
    dclj__ypafr = {}
    dttpr__xepbb = []
    gftsj__ywjur = []
    for bcy__pxo, asoml__nojhb in enumerate(partition_names):
        try:
            utp__jfsne = suz__rubvq[asoml__nojhb]
            if col_indices[utp__jfsne] not in lkrvu__uuqq:
                continue
        except (KeyError, ValueError) as vcy__qbedr:
            continue
        dclj__ypafr[asoml__nojhb] = len(xxa__nip)
        xxa__nip.append(asoml__nojhb)
        dttpr__xepbb.append(bcy__pxo)
        cgks__ujg = out_types[utp__jfsne].dtype
        lkj__ctd = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            cgks__ujg)
        gftsj__ywjur.append(numba_to_c_type(lkj__ctd))
    cnd__cmww += f'    total_rows_np = np.array([0], dtype=np.int64)\n'
    cnd__cmww += f'    out_table = pq_read(\n'
    cnd__cmww += f'        fname_py, {is_parallel},\n'
    cnd__cmww += f'        unicode_to_utf8(bucket_region),\n'
    cnd__cmww += f'        dnf_filters, expr_filters,\n'
    cnd__cmww += f"""        storage_options_py, {tot_rows_to_read}, selected_cols_arr_{jxqzf__mcmm}.ctypes,
"""
    cnd__cmww += f'        {len(ssge__qmik)},\n'
    cnd__cmww += f'        nullable_cols_arr_{jxqzf__mcmm}.ctypes,\n'
    if len(dttpr__xepbb) > 0:
        cnd__cmww += (
            f'        np.array({dttpr__xepbb}, dtype=np.int32).ctypes,\n')
        cnd__cmww += (
            f'        np.array({gftsj__ywjur}, dtype=np.int32).ctypes,\n')
        cnd__cmww += f'        {len(dttpr__xepbb)},\n'
    else:
        cnd__cmww += f'        0, 0, 0,\n'
    if len(str_as_dict_cols) > 0:
        cnd__cmww += f"""        np.array({str_as_dict_cols}, dtype=np.int32).ctypes, {len(str_as_dict_cols)},
"""
    else:
        cnd__cmww += f'        0, 0,\n'
    cnd__cmww += f'        total_rows_np.ctypes,\n'
    cnd__cmww += f'        {input_file_name_col is not None},\n'
    cnd__cmww += f'    )\n'
    cnd__cmww += f'    check_and_propagate_cpp_exception()\n'
    cdy__raqs = 'None'
    ocf__cto = index_column_type
    rqnny__owg = TableType(tuple(out_types))
    if aml__rgr:
        rqnny__owg = types.none
    if index_column_index is not None:
        enqtl__klr = fhs__rckzg[index_column_index]
        cdy__raqs = (
            f'info_to_array(info_from_table(out_table, {enqtl__klr}), index_arr_type)'
            )
    cnd__cmww += f'    index_arr = {cdy__raqs}\n'
    if aml__rgr:
        hezcl__kxxh = None
    else:
        hezcl__kxxh = []
        lyqmt__eutkx = 0
        dezfq__veqz = col_indices[col_names.index(input_file_name_col)
            ] if input_file_name_col is not None else None
        for bcy__pxo, rbav__cpucy in enumerate(col_indices):
            if lyqmt__eutkx < len(type_usecol_offset
                ) and bcy__pxo == type_usecol_offset[lyqmt__eutkx]:
                llqyr__bpjk = col_indices[bcy__pxo]
                if dezfq__veqz and llqyr__bpjk == dezfq__veqz:
                    hezcl__kxxh.append(len(ssge__qmik) + len(xxa__nip))
                elif llqyr__bpjk in lkrvu__uuqq:
                    iighi__mniza = kgda__wtrz[bcy__pxo]
                    hezcl__kxxh.append(len(ssge__qmik) + dclj__ypafr[
                        iighi__mniza])
                else:
                    hezcl__kxxh.append(fhs__rckzg[rbav__cpucy])
                lyqmt__eutkx += 1
            else:
                hezcl__kxxh.append(-1)
        hezcl__kxxh = np.array(hezcl__kxxh, dtype=np.int64)
    if aml__rgr:
        cnd__cmww += '    T = None\n'
    else:
        cnd__cmww += f"""    T = cpp_table_to_py_table(out_table, table_idx_{jxqzf__mcmm}, py_table_type_{jxqzf__mcmm})
"""
    cnd__cmww += f'    delete_table(out_table)\n'
    cnd__cmww += f'    total_rows = total_rows_np[0]\n'
    cnd__cmww += f'    ev.finalize()\n'
    cnd__cmww += f'    return (total_rows, T, index_arr)\n'
    igm__rdebd = {}
    wisdv__uczj = {f'py_table_type_{jxqzf__mcmm}': rqnny__owg,
        f'table_idx_{jxqzf__mcmm}': hezcl__kxxh,
        f'selected_cols_arr_{jxqzf__mcmm}': np.array(ssge__qmik, np.int32),
        f'nullable_cols_arr_{jxqzf__mcmm}': np.array(wbyby__ijl, np.int32),
        'index_arr_type': ocf__cto, 'cpp_table_to_py_table':
        cpp_table_to_py_table, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'delete_table': delete_table,
        'check_and_propagate_cpp_exception':
        check_and_propagate_cpp_exception, 'pq_read': _pq_read,
        'unicode_to_utf8': unicode_to_utf8, 'get_filters_pyobject':
        get_filters_pyobject, 'get_storage_options_pyobject':
        get_storage_options_pyobject, 'get_fname_pyobject':
        get_fname_pyobject, 'np': np, 'pd': pd, 'bodo': bodo}
    exec(cnd__cmww, wisdv__uczj, igm__rdebd)
    jwwe__mfw = igm__rdebd['pq_reader_py']
    pwcix__ctlws = numba.njit(jwwe__mfw, no_cpython_wrapper=True)
    return pwcix__ctlws


import pyarrow as pa
_pa_numba_typ_map = {pa.bool_(): types.bool_, pa.int8(): types.int8, pa.
    int16(): types.int16, pa.int32(): types.int32, pa.int64(): types.int64,
    pa.uint8(): types.uint8, pa.uint16(): types.uint16, pa.uint32(): types.
    uint32, pa.uint64(): types.uint64, pa.float32(): types.float32, pa.
    float64(): types.float64, pa.string(): string_type, pa.binary():
    bytes_type, pa.date32(): datetime_date_type, pa.date64(): types.
    NPDatetime('ns'), null(): string_type}


def get_arrow_timestamp_type(pa_ts_typ):
    tovtg__chld = 'ns', 'us', 'ms', 's'
    if pa_ts_typ.unit not in tovtg__chld:
        return types.Array(bodo.datetime64ns, 1, 'C'), False
    elif pa_ts_typ.tz is not None:
        ikf__cxb = pa_ts_typ.to_pandas_dtype().tz
        gyea__hmmq = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(ikf__cxb)
        return bodo.DatetimeArrayType(gyea__hmmq), True
    else:
        return types.Array(bodo.datetime64ns, 1, 'C'), True


def _get_numba_typ_from_pa_typ(pa_typ, is_index, nullable_from_metadata,
    category_info, str_as_dict=False):
    if isinstance(pa_typ.type, pa.ListType):
        ebc__rugip, ndgml__abe = _get_numba_typ_from_pa_typ(pa_typ.type.
            value_field, is_index, nullable_from_metadata, category_info)
        return ArrayItemArrayType(ebc__rugip), ndgml__abe
    if isinstance(pa_typ.type, pa.StructType):
        tgr__zqadb = []
        tyruh__vhxm = []
        ndgml__abe = True
        for pltg__owlwn in pa_typ.flatten():
            tyruh__vhxm.append(pltg__owlwn.name.split('.')[-1])
            tgn__aotot, ugljo__dlm = _get_numba_typ_from_pa_typ(pltg__owlwn,
                is_index, nullable_from_metadata, category_info)
            tgr__zqadb.append(tgn__aotot)
            ndgml__abe = ndgml__abe and ugljo__dlm
        return StructArrayType(tuple(tgr__zqadb), tuple(tyruh__vhxm)
            ), ndgml__abe
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
        lydh__vgz = _pa_numba_typ_map[pa_typ.type.index_type]
        djdvd__fgkex = PDCategoricalDtype(category_info[pa_typ.name], bodo.
            string_type, pa_typ.type.ordered, int_type=lydh__vgz)
        return CategoricalArrayType(djdvd__fgkex), True
    if isinstance(pa_typ.type, pa.lib.TimestampType):
        return get_arrow_timestamp_type(pa_typ.type)
    elif pa_typ.type in _pa_numba_typ_map:
        kzo__vcol = _pa_numba_typ_map[pa_typ.type]
        ndgml__abe = True
    else:
        raise BodoError('Arrow data type {} not supported yet'.format(
            pa_typ.type))
    if kzo__vcol == datetime_date_type:
        return datetime_date_array_type, ndgml__abe
    if kzo__vcol == bytes_type:
        return binary_array_type, ndgml__abe
    ebc__rugip = (string_array_type if kzo__vcol == string_type else types.
        Array(kzo__vcol, 1, 'C'))
    if kzo__vcol == types.bool_:
        ebc__rugip = boolean_array
    if nullable_from_metadata is not None:
        xqg__yvavg = nullable_from_metadata
    else:
        xqg__yvavg = use_nullable_int_arr
    if xqg__yvavg and not is_index and isinstance(kzo__vcol, types.Integer
        ) and pa_typ.nullable:
        ebc__rugip = IntegerArrayType(kzo__vcol)
    return ebc__rugip, ndgml__abe


def get_parquet_dataset(fpath, get_row_counts=True, dnf_filters=None,
    expr_filters=None, storage_options=None, read_categories=False,
    is_parallel=False, tot_rows_to_read=None, typing_pa_schema=None):
    if get_row_counts:
        vjl__wylb = tracing.Event('get_parquet_dataset')
    import time
    import pyarrow as pa
    import pyarrow.parquet as pq
    from mpi4py import MPI
    yzuix__xdify = MPI.COMM_WORLD
    if isinstance(fpath, list):
        ygwt__aek = urlparse(fpath[0])
        protocol = ygwt__aek.scheme
        wlpow__ufutf = ygwt__aek.netloc
        for bcy__pxo in range(len(fpath)):
            fhoqd__ydc = fpath[bcy__pxo]
            qzqq__cyk = urlparse(fhoqd__ydc)
            if qzqq__cyk.scheme != protocol:
                raise BodoError(
                    'All parquet files must use the same filesystem protocol')
            if qzqq__cyk.netloc != wlpow__ufutf:
                raise BodoError(
                    'All parquet files must be in the same S3 bucket')
            fpath[bcy__pxo] = fhoqd__ydc.rstrip('/')
    else:
        ygwt__aek = urlparse(fpath)
        protocol = ygwt__aek.scheme
        fpath = fpath.rstrip('/')
    if protocol in {'gcs', 'gs'}:
        try:
            import gcsfs
        except ImportError as vcy__qbedr:
            wjpul__sajhk = """Couldn't import gcsfs, which is required for Google cloud access. gcsfs can be installed by calling 'conda install -c conda-forge gcsfs'.
"""
            raise BodoError(wjpul__sajhk)
    if protocol == 'http':
        try:
            import fsspec
        except ImportError as vcy__qbedr:
            wjpul__sajhk = """Couldn't import fsspec, which is required for http access. fsspec can be installed by calling 'conda install -c conda-forge fsspec'.
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
            ouwgn__gmqo = gcsfs.GCSFileSystem(token=None)
            fs.append(ouwgn__gmqo)
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
                prefix = f'{protocol}://{ygwt__aek.netloc}'
                path = path[len(prefix):]
            gsja__fzuv = fs.glob(path)
            if protocol == 's3':
                gsja__fzuv = [('s3://' + fhoqd__ydc) for fhoqd__ydc in
                    gsja__fzuv if not fhoqd__ydc.startswith('s3://')]
            elif protocol in {'hdfs', 'abfs', 'abfss'}:
                gsja__fzuv = [(prefix + fhoqd__ydc) for fhoqd__ydc in
                    gsja__fzuv]
        except:
            raise BodoError(
                f'glob pattern expansion not supported for {protocol}')
        if len(gsja__fzuv) == 0:
            raise BodoError('No files found matching glob pattern')
        return gsja__fzuv
    vpt__pshfq = False
    if get_row_counts:
        gwp__zqwxa = getfs(parallel=True)
        vpt__pshfq = bodo.parquet_validate_schema
    if bodo.get_rank() == 0:
        eqz__nhce = 1
        szj__mohe = os.cpu_count()
        if szj__mohe is not None and szj__mohe > 1:
            eqz__nhce = szj__mohe // 2
        try:
            if get_row_counts:
                ztgz__kygn = tracing.Event('pq.ParquetDataset', is_parallel
                    =False)
                if tracing.is_tracing():
                    ztgz__kygn.add_attribute('g_dnf_filter', str(dnf_filters))
            awb__jfs = pa.io_thread_count()
            pa.set_io_thread_count(eqz__nhce)
            if isinstance(fpath, list):
                bkur__fdmg = []
                for cogd__vdg in fpath:
                    if has_magic(cogd__vdg):
                        bkur__fdmg += glob(protocol, getfs(), cogd__vdg)
                    else:
                        bkur__fdmg.append(cogd__vdg)
                fpath = bkur__fdmg
            elif has_magic(fpath):
                fpath = glob(protocol, getfs(), fpath)
            if protocol == 's3':
                if isinstance(fpath, list):
                    get_legacy_fs().info(fpath[0])
                else:
                    get_legacy_fs().info(fpath)
            if protocol in {'hdfs', 'abfs', 'abfss'}:
                prefix = f'{protocol}://{ygwt__aek.netloc}'
                if isinstance(fpath, list):
                    fdyt__diasy = [fhoqd__ydc[len(prefix):] for fhoqd__ydc in
                        fpath]
                else:
                    fdyt__diasy = fpath[len(prefix):]
            else:
                fdyt__diasy = fpath
            gcv__hdf = pq.ParquetDataset(fdyt__diasy, filesystem=
                get_legacy_fs(), filters=None, use_legacy_dataset=True,
                validate_schema=False, metadata_nthreads=eqz__nhce)
            pa.set_io_thread_count(awb__jfs)
            if typing_pa_schema:
                oblx__lkpa = typing_pa_schema
            else:
                oblx__lkpa = bodo.io.pa_parquet.get_dataset_schema(gcv__hdf)
            if dnf_filters:
                if get_row_counts:
                    ztgz__kygn.add_attribute('num_pieces_before_filter',
                        len(gcv__hdf.pieces))
                fod__uhh = time.time()
                gcv__hdf._filter(dnf_filters)
                if get_row_counts:
                    ztgz__kygn.add_attribute('dnf_filter_time', time.time() -
                        fod__uhh)
                    ztgz__kygn.add_attribute('num_pieces_after_filter', len
                        (gcv__hdf.pieces))
            if get_row_counts:
                ztgz__kygn.finalize()
            gcv__hdf._metadata.fs = None
        except Exception as cjsma__sluoo:
            if isinstance(fpath, list) and isinstance(cjsma__sluoo, (
                OSError, FileNotFoundError)):
                cjsma__sluoo = BodoError(str(cjsma__sluoo) +
                    list_of_files_error_msg)
            else:
                cjsma__sluoo = BodoError(
                    f"""error from pyarrow: {type(cjsma__sluoo).__name__}: {str(cjsma__sluoo)}
"""
                    )
            yzuix__xdify.bcast(cjsma__sluoo)
            raise cjsma__sluoo
        if get_row_counts:
            bmd__gzb = tracing.Event('bcast dataset')
        yzuix__xdify.bcast(gcv__hdf)
        yzuix__xdify.bcast(oblx__lkpa)
    else:
        if get_row_counts:
            bmd__gzb = tracing.Event('bcast dataset')
        gcv__hdf = yzuix__xdify.bcast(None)
        if isinstance(gcv__hdf, Exception):
            punen__uzmvs = gcv__hdf
            raise punen__uzmvs
        oblx__lkpa = yzuix__xdify.bcast(None)
    yibj__cnnd = set(oblx__lkpa.names)
    if get_row_counts:
        mxnw__ensvw = getfs()
    else:
        mxnw__ensvw = get_legacy_fs()
    gcv__hdf._metadata.fs = mxnw__ensvw
    if get_row_counts:
        bmd__gzb.finalize()
    gcv__hdf._bodo_total_rows = 0
    if get_row_counts and tot_rows_to_read == 0:
        get_row_counts = vpt__pshfq = False
        for cogd__vdg in gcv__hdf.pieces:
            cogd__vdg._bodo_num_rows = 0
    if get_row_counts or vpt__pshfq:
        if get_row_counts and tracing.is_tracing():
            nsvdr__hku = tracing.Event('get_row_counts')
            nsvdr__hku.add_attribute('g_num_pieces', len(gcv__hdf.pieces))
            nsvdr__hku.add_attribute('g_expr_filters', str(expr_filters))
        ykrjj__trp = 0.0
        num_pieces = len(gcv__hdf.pieces)
        start = get_start(num_pieces, bodo.get_size(), bodo.get_rank())
        bhr__rja = get_end(num_pieces, bodo.get_size(), bodo.get_rank())
        yuxd__gehut = 0
        rzjuo__wmih = 0
        tgfw__xeacl = 0
        ilbkl__nqme = True
        if expr_filters is not None:
            import random
            random.seed(37)
            pfidn__lyt = random.sample(gcv__hdf.pieces, k=len(gcv__hdf.pieces))
        else:
            pfidn__lyt = gcv__hdf.pieces
        for cogd__vdg in pfidn__lyt:
            cogd__vdg._bodo_num_rows = 0
        fpaths = [cogd__vdg.path for cogd__vdg in pfidn__lyt[start:bhr__rja]]
        if protocol == 's3':
            wlpow__ufutf = ygwt__aek.netloc
            prefix = 's3://' + wlpow__ufutf + '/'
            fpaths = [fhoqd__ydc[len(prefix):] for fhoqd__ydc in fpaths]
            mxnw__ensvw = get_s3_subtree_fs(wlpow__ufutf, region=getfs().
                region, storage_options=storage_options)
        else:
            mxnw__ensvw = getfs()
        eqz__nhce = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), 4)
        pa.set_io_thread_count(eqz__nhce)
        pa.set_cpu_count(eqz__nhce)
        punen__uzmvs = None
        try:
            csiw__rgtz = ds.dataset(fpaths, filesystem=mxnw__ensvw,
                partitioning=ds.partitioning(flavor='hive') if gcv__hdf.
                partitions else None)
            for jvdau__vuu, qmg__mhnh in zip(pfidn__lyt[start:bhr__rja],
                csiw__rgtz.get_fragments()):
                if vpt__pshfq:
                    vmoe__dcfa = qmg__mhnh.metadata.schema.to_arrow_schema()
                    kcs__yjw = set(vmoe__dcfa.names)
                    if yibj__cnnd != kcs__yjw:
                        wdo__lsdga = kcs__yjw - yibj__cnnd
                        mei__ydm = yibj__cnnd - kcs__yjw
                        hmbck__ser = f'Schema in {jvdau__vuu} was different.\n'
                        if wdo__lsdga:
                            hmbck__ser += f"""File contains column(s) {wdo__lsdga} not found in other files in the dataset.
"""
                        if mei__ydm:
                            hmbck__ser += f"""File missing column(s) {mei__ydm} found in other files in the dataset.
"""
                        raise BodoError(hmbck__ser)
                    try:
                        oblx__lkpa = pa.unify_schemas([oblx__lkpa, vmoe__dcfa])
                    except Exception as cjsma__sluoo:
                        hmbck__ser = (
                            f'Schema in {jvdau__vuu} was different.\n' +
                            str(cjsma__sluoo))
                        raise BodoError(hmbck__ser)
                fod__uhh = time.time()
                kqejb__dqm = qmg__mhnh.scanner(schema=csiw__rgtz.schema,
                    filter=expr_filters, use_threads=True).count_rows()
                ykrjj__trp += time.time() - fod__uhh
                jvdau__vuu._bodo_num_rows = kqejb__dqm
                yuxd__gehut += kqejb__dqm
                rzjuo__wmih += qmg__mhnh.num_row_groups
                tgfw__xeacl += sum(kqda__csnhb.total_byte_size for
                    kqda__csnhb in qmg__mhnh.row_groups)
        except Exception as cjsma__sluoo:
            punen__uzmvs = cjsma__sluoo
        if yzuix__xdify.allreduce(punen__uzmvs is not None, op=MPI.LOR):
            for punen__uzmvs in yzuix__xdify.allgather(punen__uzmvs):
                if punen__uzmvs:
                    if isinstance(fpath, list) and isinstance(punen__uzmvs,
                        (OSError, FileNotFoundError)):
                        raise BodoError(str(punen__uzmvs) +
                            list_of_files_error_msg)
                    raise punen__uzmvs
        if vpt__pshfq:
            ilbkl__nqme = yzuix__xdify.allreduce(ilbkl__nqme, op=MPI.LAND)
            if not ilbkl__nqme:
                raise BodoError("Schema in parquet files don't match")
        if get_row_counts:
            gcv__hdf._bodo_total_rows = yzuix__xdify.allreduce(yuxd__gehut,
                op=MPI.SUM)
            yoy__bwkvw = yzuix__xdify.allreduce(rzjuo__wmih, op=MPI.SUM)
            hbws__aktih = yzuix__xdify.allreduce(tgfw__xeacl, op=MPI.SUM)
            kkcj__mneh = np.array([cogd__vdg._bodo_num_rows for cogd__vdg in
                gcv__hdf.pieces])
            kkcj__mneh = yzuix__xdify.allreduce(kkcj__mneh, op=MPI.SUM)
            for cogd__vdg, oucld__oim in zip(gcv__hdf.pieces, kkcj__mneh):
                cogd__vdg._bodo_num_rows = oucld__oim
            if is_parallel and bodo.get_rank(
                ) == 0 and yoy__bwkvw < bodo.get_size() and yoy__bwkvw != 0:
                warnings.warn(BodoWarning(
                    f"""Total number of row groups in parquet dataset {fpath} ({yoy__bwkvw}) is too small for effective IO parallelization.
For best performance the number of row groups should be greater than the number of workers ({bodo.get_size()}). For more details, refer to
https://docs.bodo.ai/latest/file_io/#parquet-section.
"""
                    ))
            if yoy__bwkvw == 0:
                qfckl__jrql = 0
            else:
                qfckl__jrql = hbws__aktih // yoy__bwkvw
            if (bodo.get_rank() == 0 and hbws__aktih >= 20 * 1048576 and 
                qfckl__jrql < 1048576 and protocol in REMOTE_FILESYSTEMS):
                warnings.warn(BodoWarning(
                    f'Parquet average row group size is small ({qfckl__jrql} bytes) and can have negative impact on performance when reading from remote sources'
                    ))
            if tracing.is_tracing():
                nsvdr__hku.add_attribute('g_total_num_row_groups', yoy__bwkvw)
                nsvdr__hku.add_attribute('total_scan_time', ykrjj__trp)
                mgad__mxf = np.array([cogd__vdg._bodo_num_rows for
                    cogd__vdg in gcv__hdf.pieces])
                eult__zaq = np.percentile(mgad__mxf, [25, 50, 75])
                nsvdr__hku.add_attribute('g_row_counts_min', mgad__mxf.min())
                nsvdr__hku.add_attribute('g_row_counts_Q1', eult__zaq[0])
                nsvdr__hku.add_attribute('g_row_counts_median', eult__zaq[1])
                nsvdr__hku.add_attribute('g_row_counts_Q3', eult__zaq[2])
                nsvdr__hku.add_attribute('g_row_counts_max', mgad__mxf.max())
                nsvdr__hku.add_attribute('g_row_counts_mean', mgad__mxf.mean())
                nsvdr__hku.add_attribute('g_row_counts_std', mgad__mxf.std())
                nsvdr__hku.add_attribute('g_row_counts_sum', mgad__mxf.sum())
                nsvdr__hku.finalize()
    gcv__hdf._prefix = ''
    if protocol in {'hdfs', 'abfs', 'abfss'}:
        prefix = f'{protocol}://{ygwt__aek.netloc}'
        if len(gcv__hdf.pieces) > 0:
            jvdau__vuu = gcv__hdf.pieces[0]
            if not jvdau__vuu.path.startswith(prefix):
                gcv__hdf._prefix = prefix
    if read_categories:
        _add_categories_to_pq_dataset(gcv__hdf)
    if get_row_counts:
        vjl__wylb.finalize()
    if vpt__pshfq and is_parallel:
        if tracing.is_tracing():
            nke__svqy = tracing.Event('unify_schemas_across_ranks')
        punen__uzmvs = None
        try:
            oblx__lkpa = yzuix__xdify.allreduce(oblx__lkpa, bodo.io.helpers
                .pa_schema_unify_mpi_op)
        except Exception as cjsma__sluoo:
            punen__uzmvs = cjsma__sluoo
        if tracing.is_tracing():
            nke__svqy.finalize()
        if yzuix__xdify.allreduce(punen__uzmvs is not None, op=MPI.LOR):
            for punen__uzmvs in yzuix__xdify.allgather(punen__uzmvs):
                if punen__uzmvs:
                    hmbck__ser = (f'Schema in some files were different.\n' +
                        str(punen__uzmvs))
                    raise BodoError(hmbck__ser)
    gcv__hdf._bodo_arrow_schema = oblx__lkpa
    return gcv__hdf


def get_scanner_batches(fpaths, expr_filters, selected_fields,
    avg_num_pieces, is_parallel, storage_options, region, prefix,
    str_as_dict_cols, start_offset, rows_to_read, has_partitions, schema):
    import pyarrow as pa
    szj__mohe = os.cpu_count()
    if szj__mohe is None or szj__mohe == 0:
        szj__mohe = 2
    dnc__xkbbt = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), szj__mohe)
    lvcj__nrhr = min(int(os.environ.get('BODO_MAX_IO_THREADS', 16)), szj__mohe)
    if is_parallel and len(fpaths) > lvcj__nrhr and len(fpaths
        ) / avg_num_pieces >= 2.0:
        pa.set_io_thread_count(lvcj__nrhr)
        pa.set_cpu_count(lvcj__nrhr)
    else:
        pa.set_io_thread_count(dnc__xkbbt)
        pa.set_cpu_count(dnc__xkbbt)
    if fpaths[0].startswith('s3://'):
        wlpow__ufutf = urlparse(fpaths[0]).netloc
        prefix = 's3://' + wlpow__ufutf + '/'
        fpaths = [fhoqd__ydc[len(prefix):] for fhoqd__ydc in fpaths]
        if region == '':
            region = get_s3_bucket_region_njit(fpaths[0], parallel=False)
        mxnw__ensvw = get_s3_subtree_fs(wlpow__ufutf, region=region,
            storage_options=storage_options)
    elif prefix and prefix.startswith(('hdfs', 'abfs', 'abfss')):
        mxnw__ensvw = get_hdfs_fs(prefix + fpaths[0])
    elif fpaths[0].startswith(('gcs', 'gs')):
        import gcsfs
        mxnw__ensvw = gcsfs.GCSFileSystem(token=None)
    else:
        mxnw__ensvw = None
    aspi__luksl = ds.ParquetFileFormat(dictionary_columns=str_as_dict_cols)
    gcv__hdf = ds.dataset(fpaths, filesystem=mxnw__ensvw, partitioning=ds.
        partitioning(flavor='hive') if has_partitions else None, format=
        aspi__luksl)
    ljti__eplg = set(str_as_dict_cols)
    yao__jgbck = schema.names
    for bcy__pxo, name in enumerate(yao__jgbck):
        if name in ljti__eplg:
            pkf__fuj = schema.field(bcy__pxo)
            vmtr__ulrjw = pa.field(name, pa.dictionary(pa.int32(), pkf__fuj
                .type), pkf__fuj.nullable)
            schema = schema.remove(bcy__pxo).insert(bcy__pxo, vmtr__ulrjw)
    gcv__hdf = gcv__hdf.replace_schema(pa.unify_schemas([gcv__hdf.schema,
        schema]))
    col_names = gcv__hdf.schema.names
    ezgl__hmee = [col_names[hhsjn__ntq] for hhsjn__ntq in selected_fields]
    oboph__sejt = len(fpaths) <= 3 or start_offset > 0 and len(fpaths) <= 10
    if oboph__sejt and expr_filters is None:
        tlyzo__oocso = []
        fvhid__zzvs = 0
        hwiro__ymbq = 0
        for qmg__mhnh in gcv__hdf.get_fragments():
            qsme__awk = []
            for kqda__csnhb in qmg__mhnh.row_groups:
                mhoo__fuhf = kqda__csnhb.num_rows
                if start_offset < fvhid__zzvs + mhoo__fuhf:
                    if hwiro__ymbq == 0:
                        absz__wll = start_offset - fvhid__zzvs
                        keuui__qyhi = min(mhoo__fuhf - absz__wll, rows_to_read)
                    else:
                        keuui__qyhi = min(mhoo__fuhf, rows_to_read -
                            hwiro__ymbq)
                    hwiro__ymbq += keuui__qyhi
                    qsme__awk.append(kqda__csnhb.id)
                fvhid__zzvs += mhoo__fuhf
                if hwiro__ymbq == rows_to_read:
                    break
            tlyzo__oocso.append(qmg__mhnh.subset(row_group_ids=qsme__awk))
            if hwiro__ymbq == rows_to_read:
                break
        gcv__hdf = ds.FileSystemDataset(tlyzo__oocso, gcv__hdf.schema,
            aspi__luksl, filesystem=gcv__hdf.filesystem)
        start_offset = absz__wll
    nuvcw__knp = gcv__hdf.scanner(columns=ezgl__hmee, filter=expr_filters,
        use_threads=True).to_reader()
    return gcv__hdf, nuvcw__knp, start_offset


def _add_categories_to_pq_dataset(pq_dataset):
    import pyarrow as pa
    from mpi4py import MPI
    if len(pq_dataset.pieces) < 1:
        raise BodoError(
            'No pieces found in Parquet dataset. Cannot get read categorical values'
            )
    pa_schema = pq_dataset.schema.to_arrow_schema()
    khyw__uzctw = [c for c in pa_schema.names if isinstance(pa_schema.field
        (c).type, pa.DictionaryType)]
    if len(khyw__uzctw) == 0:
        pq_dataset._category_info = {}
        return
    yzuix__xdify = MPI.COMM_WORLD
    if bodo.get_rank() == 0:
        try:
            fosf__ixhn = pq_dataset.pieces[0].open()
            kqda__csnhb = fosf__ixhn.read_row_group(0, khyw__uzctw)
            category_info = {c: tuple(kqda__csnhb.column(c).chunk(0).
                dictionary.to_pylist()) for c in khyw__uzctw}
            del fosf__ixhn, kqda__csnhb
        except Exception as cjsma__sluoo:
            yzuix__xdify.bcast(cjsma__sluoo)
            raise cjsma__sluoo
        yzuix__xdify.bcast(category_info)
    else:
        category_info = yzuix__xdify.bcast(None)
        if isinstance(category_info, Exception):
            punen__uzmvs = category_info
            raise punen__uzmvs
    pq_dataset._category_info = category_info


def get_pandas_metadata(schema, num_pieces):
    qocxb__lkmu = None
    nullable_from_metadata = defaultdict(lambda : None)
    bwnqv__ned = b'pandas'
    if schema.metadata is not None and bwnqv__ned in schema.metadata:
        import json
        uoiw__uidrp = json.loads(schema.metadata[bwnqv__ned].decode('utf8'))
        xxs__hwkc = len(uoiw__uidrp['index_columns'])
        if xxs__hwkc > 1:
            raise BodoError('read_parquet: MultiIndex not supported yet')
        qocxb__lkmu = uoiw__uidrp['index_columns'][0] if xxs__hwkc else None
        if not isinstance(qocxb__lkmu, str) and not isinstance(qocxb__lkmu,
            dict):
            qocxb__lkmu = None
        for reg__nmpqs in uoiw__uidrp['columns']:
            lfkaa__pkdi = reg__nmpqs['name']
            if reg__nmpqs['pandas_type'].startswith('int'
                ) and lfkaa__pkdi is not None:
                if reg__nmpqs['numpy_type'].startswith('Int'):
                    nullable_from_metadata[lfkaa__pkdi] = True
                else:
                    nullable_from_metadata[lfkaa__pkdi] = False
    return qocxb__lkmu, nullable_from_metadata


def get_str_columns_from_pa_schema(pa_schema):
    str_columns = []
    for lfkaa__pkdi in pa_schema.names:
        pltg__owlwn = pa_schema.field(lfkaa__pkdi)
        if pltg__owlwn.type == pa.string():
            str_columns.append(lfkaa__pkdi)
    return str_columns


def determine_str_as_dict_columns(pq_dataset, pa_schema, str_columns):
    from mpi4py import MPI
    yzuix__xdify = MPI.COMM_WORLD
    if len(str_columns) == 0:
        return set()
    if len(pq_dataset.pieces) > bodo.get_size():
        import random
        random.seed(37)
        pfidn__lyt = random.sample(pq_dataset.pieces, bodo.get_size())
    else:
        pfidn__lyt = pq_dataset.pieces
    rov__wwg = np.zeros(len(str_columns), dtype=np.int64)
    xggmh__ifvow = np.zeros(len(str_columns), dtype=np.int64)
    if bodo.get_rank() < len(pfidn__lyt):
        jvdau__vuu = pfidn__lyt[bodo.get_rank()]
        try:
            tvxqt__bkc = jvdau__vuu.get_metadata()
            for bcy__pxo in range(tvxqt__bkc.num_row_groups):
                for lyqmt__eutkx, lfkaa__pkdi in enumerate(str_columns):
                    zmh__sqaf = pa_schema.get_field_index(lfkaa__pkdi)
                    rov__wwg[lyqmt__eutkx] += tvxqt__bkc.row_group(bcy__pxo
                        ).column(zmh__sqaf).total_uncompressed_size
            lfzit__bhfe = tvxqt__bkc.num_rows
        except Exception as cjsma__sluoo:
            if isinstance(cjsma__sluoo, (OSError, FileNotFoundError)):
                lfzit__bhfe = 0
            else:
                raise
    else:
        lfzit__bhfe = 0
    buys__pqrlq = yzuix__xdify.allreduce(lfzit__bhfe, op=MPI.SUM)
    if buys__pqrlq == 0:
        return set()
    yzuix__xdify.Allreduce(rov__wwg, xggmh__ifvow, op=MPI.SUM)
    fjsto__ivo = xggmh__ifvow / buys__pqrlq
    str_as_dict = set()
    for bcy__pxo, dunml__lfql in enumerate(fjsto__ivo):
        if dunml__lfql < READ_STR_AS_DICT_THRESHOLD:
            lfkaa__pkdi = str_columns[bcy__pxo][0]
            str_as_dict.add(lfkaa__pkdi)
    return str_as_dict


def parquet_file_schema(file_name, selected_columns, storage_options=None,
    input_file_name_col=None, read_as_dict_cols=None):
    col_names = []
    fnasq__kcqxf = []
    pq_dataset = get_parquet_dataset(file_name, get_row_counts=False,
        storage_options=storage_options, read_categories=True)
    if hasattr(pq_dataset, '_bodo_arrow_schema'):
        pa_schema = pq_dataset._bodo_arrow_schema
    else:
        pa_schema = pq_dataset.schema.to_arrow_schema()
    partition_names = [] if pq_dataset.partitions is None else [pq_dataset.
        partitions.levels[bcy__pxo].name for bcy__pxo in range(len(
        pq_dataset.partitions.partition_names))]
    num_pieces = len(pq_dataset.pieces)
    str_columns = get_str_columns_from_pa_schema(pa_schema)
    atp__jej = set(str_columns)
    if read_as_dict_cols is None:
        read_as_dict_cols = []
    read_as_dict_cols = set(read_as_dict_cols)
    ldx__xlbfx = read_as_dict_cols - atp__jej
    if len(ldx__xlbfx) > 0:
        if bodo.get_rank() == 0:
            warnings.warn(
                f'The following columns are not of datatype string and hence cannot be read with dictionary encoding: {ldx__xlbfx}'
                , bodo.utils.typing.BodoWarning)
    read_as_dict_cols.intersection_update(atp__jej)
    atp__jej = atp__jej - read_as_dict_cols
    str_columns = [vyz__tlvl for vyz__tlvl in str_columns if vyz__tlvl in
        atp__jej]
    str_as_dict: set = determine_str_as_dict_columns(pq_dataset, pa_schema,
        str_columns)
    str_as_dict.update(read_as_dict_cols)
    col_names = pa_schema.names
    qocxb__lkmu, nullable_from_metadata = get_pandas_metadata(pa_schema,
        num_pieces)
    touyl__xdara = []
    cngq__seqn = []
    dhkn__upybq = []
    for bcy__pxo, c in enumerate(col_names):
        pltg__owlwn = pa_schema.field(c)
        kzo__vcol, ndgml__abe = _get_numba_typ_from_pa_typ(pltg__owlwn, c ==
            qocxb__lkmu, nullable_from_metadata[c], pq_dataset.
            _category_info, str_as_dict=c in str_as_dict)
        touyl__xdara.append(kzo__vcol)
        cngq__seqn.append(ndgml__abe)
        dhkn__upybq.append(pltg__owlwn.type)
    if partition_names:
        col_names += partition_names
        touyl__xdara += [_get_partition_cat_dtype(pq_dataset.partitions.
            levels[bcy__pxo]) for bcy__pxo in range(len(partition_names))]
        cngq__seqn.extend([True] * len(partition_names))
        dhkn__upybq.extend([None] * len(partition_names))
    if input_file_name_col is not None:
        col_names += [input_file_name_col]
        touyl__xdara += [dict_str_arr_type]
        cngq__seqn.append(True)
        dhkn__upybq.append(None)
    zjsfq__roaa = {c: bcy__pxo for bcy__pxo, c in enumerate(col_names)}
    if selected_columns is None:
        selected_columns = col_names
    for c in selected_columns:
        if c not in zjsfq__roaa:
            raise BodoError(f'Selected column {c} not in Parquet file schema')
    if qocxb__lkmu and not isinstance(qocxb__lkmu, dict
        ) and qocxb__lkmu not in selected_columns:
        selected_columns.append(qocxb__lkmu)
    col_names = selected_columns
    col_indices = []
    fnasq__kcqxf = []
    toc__lgqc = []
    pkq__pabk = []
    for bcy__pxo, c in enumerate(col_names):
        llqyr__bpjk = zjsfq__roaa[c]
        col_indices.append(llqyr__bpjk)
        fnasq__kcqxf.append(touyl__xdara[llqyr__bpjk])
        if not cngq__seqn[llqyr__bpjk]:
            toc__lgqc.append(bcy__pxo)
            pkq__pabk.append(dhkn__upybq[llqyr__bpjk])
    return (col_names, fnasq__kcqxf, qocxb__lkmu, col_indices,
        partition_names, toc__lgqc, pkq__pabk)


def _get_partition_cat_dtype(part_set):
    kjiue__pmo = part_set.dictionary.to_pandas()
    hvnhb__zdhq = bodo.typeof(kjiue__pmo).dtype
    djdvd__fgkex = PDCategoricalDtype(tuple(kjiue__pmo), hvnhb__zdhq, False)
    return CategoricalArrayType(djdvd__fgkex)


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
        anzw__lpcfr = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(32), lir.IntType(32),
            lir.IntType(32), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        lfq__mziq = cgutils.get_or_insert_function(builder.module,
            anzw__lpcfr, name='pq_write')
        builder.call(lfq__mziq, args)
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
        anzw__lpcfr = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        lfq__mziq = cgutils.get_or_insert_function(builder.module,
            anzw__lpcfr, name='pq_write_partitioned')
        builder.call(lfq__mziq, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
    return types.void(types.voidptr, data_table_t, col_names_t,
        col_names_no_partitions_t, cat_table_t, types.voidptr, types.int32,
        types.voidptr, types.boolean, types.voidptr, types.int64), codegen
