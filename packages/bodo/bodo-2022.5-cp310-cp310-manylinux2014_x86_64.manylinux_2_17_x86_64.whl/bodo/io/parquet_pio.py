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
        except OSError as clr__dfw:
            if 'non-file path' in str(clr__dfw):
                raise FileNotFoundError(str(clr__dfw))
            raise


class ParquetHandler:

    def __init__(self, func_ir, typingctx, args, _locals):
        self.func_ir = func_ir
        self.typingctx = typingctx
        self.args = args
        self.locals = _locals

    def gen_parquet_read(self, file_name, lhs, columns, storage_options=
        None, input_file_name_col=None, read_as_dict_cols=None):
        dtw__snvpn = lhs.scope
        qfdaq__ybhgf = lhs.loc
        ivdz__nywt = None
        if lhs.name in self.locals:
            ivdz__nywt = self.locals[lhs.name]
            self.locals.pop(lhs.name)
        qwil__baaa = {}
        if lhs.name + ':convert' in self.locals:
            qwil__baaa = self.locals[lhs.name + ':convert']
            self.locals.pop(lhs.name + ':convert')
        if ivdz__nywt is None:
            ujh__lre = (
                'Parquet schema not available. Either path argument should be constant for Bodo to look at the file at compile time or schema should be provided. For more information, see: https://docs.bodo.ai/latest/file_io/#parquet-section.'
                )
            dmc__vvbjt = get_const_value(file_name, self.func_ir, ujh__lre,
                arg_types=self.args, file_info=ParquetFileInfo(columns,
                storage_options=storage_options, input_file_name_col=
                input_file_name_col, read_as_dict_cols=read_as_dict_cols))
            qlccx__uob = False
            haym__hocz = guard(get_definition, self.func_ir, file_name)
            if isinstance(haym__hocz, ir.Arg):
                typ = self.args[haym__hocz.index]
                if isinstance(typ, types.FilenameType):
                    (col_names, bujpe__dehju, dbl__jhon, col_indices,
                        partition_names, rqf__vkuw, pbax__lsjpg) = typ.schema
                    qlccx__uob = True
            if not qlccx__uob:
                (col_names, bujpe__dehju, dbl__jhon, col_indices,
                    partition_names, rqf__vkuw, pbax__lsjpg) = (
                    parquet_file_schema(dmc__vvbjt, columns,
                    storage_options=storage_options, input_file_name_col=
                    input_file_name_col, read_as_dict_cols=read_as_dict_cols))
        else:
            xygj__swika = list(ivdz__nywt.keys())
            eenk__awp = {c: mifb__wph for mifb__wph, c in enumerate(
                xygj__swika)}
            wfp__pipfk = [hguuj__gnktv for hguuj__gnktv in ivdz__nywt.values()]
            dbl__jhon = 'index' if 'index' in eenk__awp else None
            if columns is None:
                selected_columns = xygj__swika
            else:
                selected_columns = columns
            col_indices = [eenk__awp[c] for c in selected_columns]
            bujpe__dehju = [wfp__pipfk[eenk__awp[c]] for c in selected_columns]
            col_names = selected_columns
            dbl__jhon = dbl__jhon if dbl__jhon in col_names else None
            partition_names = []
            rqf__vkuw = []
            pbax__lsjpg = []
        rjsro__wmqez = None if isinstance(dbl__jhon, dict
            ) or dbl__jhon is None else dbl__jhon
        index_column_index = None
        index_column_type = types.none
        if rjsro__wmqez:
            lsh__trtw = col_names.index(rjsro__wmqez)
            index_column_index = col_indices.pop(lsh__trtw)
            index_column_type = bujpe__dehju.pop(lsh__trtw)
            col_names.pop(lsh__trtw)
        for mifb__wph, c in enumerate(col_names):
            if c in qwil__baaa:
                bujpe__dehju[mifb__wph] = qwil__baaa[c]
        rzjs__jvp = [ir.Var(dtw__snvpn, mk_unique_var('pq_table'),
            qfdaq__ybhgf), ir.Var(dtw__snvpn, mk_unique_var('pq_index'),
            qfdaq__ybhgf)]
        mbj__zrwve = [bodo.ir.parquet_ext.ParquetReader(file_name, lhs.name,
            col_names, col_indices, bujpe__dehju, rzjs__jvp, qfdaq__ybhgf,
            partition_names, storage_options, index_column_index,
            index_column_type, input_file_name_col, rqf__vkuw, pbax__lsjpg)]
        return (col_names, rzjs__jvp, dbl__jhon, mbj__zrwve, bujpe__dehju,
            index_column_type)


def pq_distributed_run(pq_node, array_dists, typemap, calltypes, typingctx,
    targetctx, meta_head_only_info=None):
    ivvz__chvvv = len(pq_node.out_vars)
    dnf_filter_str = 'None'
    expr_filter_str = 'None'
    oncv__rbsp, kguy__jjpvr = bodo.ir.connector.generate_filter_map(pq_node
        .filters)
    extra_args = ', '.join(oncv__rbsp.values())
    dnf_filter_str, expr_filter_str = bodo.ir.connector.generate_arrow_filters(
        pq_node.filters, oncv__rbsp, kguy__jjpvr, pq_node.
        original_df_colnames, pq_node.partition_names, pq_node.
        original_out_types, typemap, 'parquet')
    lvey__bkypn = ', '.join(f'out{mifb__wph}' for mifb__wph in range(
        ivvz__chvvv))
    wktvl__sjuhv = f'def pq_impl(fname, {extra_args}):\n'
    wktvl__sjuhv += (
        f'    (total_rows, {lvey__bkypn},) = _pq_reader_py(fname, {extra_args})\n'
        )
    mjt__wfbuy = {}
    exec(wktvl__sjuhv, {}, mjt__wfbuy)
    xff__hubfo = mjt__wfbuy['pq_impl']
    if bodo.user_logging.get_verbose_level() >= 1:
        rwt__lin = pq_node.loc.strformat()
        prt__kkznb = []
        kdwz__vkgv = []
        for mifb__wph in pq_node.type_usecol_offset:
            aunnh__kmbde = pq_node.df_colnames[mifb__wph]
            prt__kkznb.append(aunnh__kmbde)
            if isinstance(pq_node.out_types[mifb__wph], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                kdwz__vkgv.append(aunnh__kmbde)
        icmu__njyjy = (
            'Finish column pruning on read_parquet node:\n%s\nColumns loaded %s\n'
            )
        bodo.user_logging.log_message('Column Pruning', icmu__njyjy,
            rwt__lin, prt__kkznb)
        if kdwz__vkgv:
            amgn__ckl = """Finished optimized encoding on read_parquet node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', amgn__ckl,
                rwt__lin, kdwz__vkgv)
    parallel = bodo.ir.connector.is_connector_table_parallel(pq_node,
        array_dists, typemap, 'ParquetReader')
    if pq_node.unsupported_columns:
        ozx__gknxn = set(pq_node.type_usecol_offset)
        rmsk__emm = set(pq_node.unsupported_columns)
        xdq__ibwb = ozx__gknxn & rmsk__emm
        if xdq__ibwb:
            tuu__tilb = sorted(xdq__ibwb)
            ydtzl__tpoi = [
                f'pandas.read_parquet(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                "Please manually remove these columns from your read_parquet with the 'columns' argument. If these "
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            setu__egfo = 0
            for mvtuq__sows in tuu__tilb:
                while pq_node.unsupported_columns[setu__egfo] != mvtuq__sows:
                    setu__egfo += 1
                ydtzl__tpoi.append(
                    f"Column '{pq_node.df_colnames[mvtuq__sows]}' with unsupported arrow type {pq_node.unsupported_arrow_types[setu__egfo]}"
                    )
                setu__egfo += 1
            zst__ncr = '\n'.join(ydtzl__tpoi)
            raise BodoError(zst__ncr, loc=pq_node.loc)
    qtdr__fxrp = _gen_pq_reader_py(pq_node.df_colnames, pq_node.col_indices,
        pq_node.type_usecol_offset, pq_node.out_types, pq_node.
        storage_options, pq_node.partition_names, dnf_filter_str,
        expr_filter_str, extra_args, parallel, meta_head_only_info, pq_node
        .index_column_index, pq_node.index_column_type, pq_node.
        input_file_name_col)
    gml__tec = typemap[pq_node.file_name.name]
    cmnv__fpya = (gml__tec,) + tuple(typemap[plb__rtvx.name] for plb__rtvx in
        kguy__jjpvr)
    unb__yfoc = compile_to_numba_ir(xff__hubfo, {'_pq_reader_py':
        qtdr__fxrp}, typingctx=typingctx, targetctx=targetctx, arg_typs=
        cmnv__fpya, typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(unb__yfoc, [pq_node.file_name] + kguy__jjpvr)
    mbj__zrwve = unb__yfoc.body[:-3]
    if meta_head_only_info:
        mbj__zrwve[-1 - ivvz__chvvv].target = meta_head_only_info[1]
    mbj__zrwve[-2].target = pq_node.out_vars[0]
    mbj__zrwve[-1].target = pq_node.out_vars[1]
    assert not (pq_node.index_column_index is None and not pq_node.
        type_usecol_offset
        ), 'At most one of table and index should be dead if the Parquet IR node is live'
    if pq_node.index_column_index is None:
        mbj__zrwve.pop(-1)
    elif not pq_node.type_usecol_offset:
        mbj__zrwve.pop(-2)
    return mbj__zrwve


distributed_pass.distributed_run_extensions[bodo.ir.parquet_ext.ParquetReader
    ] = pq_distributed_run


def get_filters_pyobject(dnf_filter_str, expr_filter_str, vars):
    pass


@overload(get_filters_pyobject, no_unliteral=True)
def overload_get_filters_pyobject(dnf_filter_str, expr_filter_str, var_tup):
    cdzau__rqx = get_overload_const_str(dnf_filter_str)
    wku__jqk = get_overload_const_str(expr_filter_str)
    kiwpf__krj = ', '.join(f'f{mifb__wph}' for mifb__wph in range(len(var_tup))
        )
    wktvl__sjuhv = 'def impl(dnf_filter_str, expr_filter_str, var_tup):\n'
    if len(var_tup):
        wktvl__sjuhv += f'  {kiwpf__krj}, = var_tup\n'
    wktvl__sjuhv += """  with numba.objmode(dnf_filters_py='parquet_predicate_type', expr_filters_py='parquet_predicate_type'):
"""
    wktvl__sjuhv += f'    dnf_filters_py = {cdzau__rqx}\n'
    wktvl__sjuhv += f'    expr_filters_py = {wku__jqk}\n'
    wktvl__sjuhv += '  return (dnf_filters_py, expr_filters_py)\n'
    mjt__wfbuy = {}
    exec(wktvl__sjuhv, globals(), mjt__wfbuy)
    return mjt__wfbuy['impl']


@numba.njit
def get_fname_pyobject(fname):
    with numba.objmode(fname_py='read_parquet_fpath_type'):
        fname_py = fname
    return fname_py


def _gen_pq_reader_py(col_names, col_indices, type_usecol_offset, out_types,
    storage_options, partition_names, dnf_filter_str, expr_filter_str,
    extra_args, is_parallel, meta_head_only_info, index_column_index,
    index_column_type, input_file_name_col):
    vxa__qxei = next_label()
    ecq__lvj = ',' if extra_args else ''
    wktvl__sjuhv = f'def pq_reader_py(fname,{extra_args}):\n'
    wktvl__sjuhv += (
        f"    ev = bodo.utils.tracing.Event('read_parquet', {is_parallel})\n")
    wktvl__sjuhv += f"    ev.add_attribute('g_fname', fname)\n"
    wktvl__sjuhv += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={is_parallel})
"""
    wktvl__sjuhv += f"""    dnf_filters, expr_filters = get_filters_pyobject("{dnf_filter_str}", "{expr_filter_str}", ({extra_args}{ecq__lvj}))
"""
    wktvl__sjuhv += '    fname_py = get_fname_pyobject(fname)\n'
    storage_options['bodo_dummy'] = 'dummy'
    wktvl__sjuhv += f"""    storage_options_py = get_storage_options_pyobject({str(storage_options)})
"""
    tot_rows_to_read = -1
    if meta_head_only_info and meta_head_only_info[0] is not None:
        tot_rows_to_read = meta_head_only_info[0]
    mnu__ymuzj = not type_usecol_offset
    wcah__mzig = [sanitize_varname(c) for c in col_names]
    partition_names = [sanitize_varname(c) for c in partition_names]
    input_file_name_col = sanitize_varname(input_file_name_col
        ) if input_file_name_col is not None and col_names.index(
        input_file_name_col) in type_usecol_offset else None
    iann__hhaii = {c: mifb__wph for mifb__wph, c in enumerate(col_indices)}
    qitir__ltsye = {c: mifb__wph for mifb__wph, c in enumerate(wcah__mzig)}
    eshl__inxdw = []
    mwbri__mgawb = set()
    adn__qjgob = partition_names + [input_file_name_col]
    for mifb__wph in type_usecol_offset:
        if wcah__mzig[mifb__wph] not in adn__qjgob:
            eshl__inxdw.append(col_indices[mifb__wph])
        elif not input_file_name_col or wcah__mzig[mifb__wph
            ] != input_file_name_col:
            mwbri__mgawb.add(col_indices[mifb__wph])
    if index_column_index is not None:
        eshl__inxdw.append(index_column_index)
    eshl__inxdw = sorted(eshl__inxdw)
    rdlcn__jqi = {c: mifb__wph for mifb__wph, c in enumerate(eshl__inxdw)}
    elkpd__ryac = [(int(is_nullable(out_types[iann__hhaii[kvopn__igpm]])) if
        kvopn__igpm != index_column_index else int(is_nullable(
        index_column_type))) for kvopn__igpm in eshl__inxdw]
    str_as_dict_cols = []
    for kvopn__igpm in eshl__inxdw:
        if kvopn__igpm == index_column_index:
            hguuj__gnktv = index_column_type
        else:
            hguuj__gnktv = out_types[iann__hhaii[kvopn__igpm]]
        if hguuj__gnktv == dict_str_arr_type:
            str_as_dict_cols.append(kvopn__igpm)
    fgsj__bucr = []
    dquzj__gqff = {}
    dvt__agbkn = []
    ian__ylzp = []
    for mifb__wph, olgou__urh in enumerate(partition_names):
        try:
            oucp__hfne = qitir__ltsye[olgou__urh]
            if col_indices[oucp__hfne] not in mwbri__mgawb:
                continue
        except (KeyError, ValueError) as yxa__sgmn:
            continue
        dquzj__gqff[olgou__urh] = len(fgsj__bucr)
        fgsj__bucr.append(olgou__urh)
        dvt__agbkn.append(mifb__wph)
        eouto__kto = out_types[oucp__hfne].dtype
        aci__zhv = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            eouto__kto)
        ian__ylzp.append(numba_to_c_type(aci__zhv))
    wktvl__sjuhv += f'    total_rows_np = np.array([0], dtype=np.int64)\n'
    wktvl__sjuhv += f'    out_table = pq_read(\n'
    wktvl__sjuhv += f'        fname_py, {is_parallel},\n'
    wktvl__sjuhv += f'        unicode_to_utf8(bucket_region),\n'
    wktvl__sjuhv += f'        dnf_filters, expr_filters,\n'
    wktvl__sjuhv += f"""        storage_options_py, {tot_rows_to_read}, selected_cols_arr_{vxa__qxei}.ctypes,
"""
    wktvl__sjuhv += f'        {len(eshl__inxdw)},\n'
    wktvl__sjuhv += f'        nullable_cols_arr_{vxa__qxei}.ctypes,\n'
    if len(dvt__agbkn) > 0:
        wktvl__sjuhv += (
            f'        np.array({dvt__agbkn}, dtype=np.int32).ctypes,\n')
        wktvl__sjuhv += (
            f'        np.array({ian__ylzp}, dtype=np.int32).ctypes,\n')
        wktvl__sjuhv += f'        {len(dvt__agbkn)},\n'
    else:
        wktvl__sjuhv += f'        0, 0, 0,\n'
    if len(str_as_dict_cols) > 0:
        wktvl__sjuhv += f"""        np.array({str_as_dict_cols}, dtype=np.int32).ctypes, {len(str_as_dict_cols)},
"""
    else:
        wktvl__sjuhv += f'        0, 0,\n'
    wktvl__sjuhv += f'        total_rows_np.ctypes,\n'
    wktvl__sjuhv += f'        {input_file_name_col is not None},\n'
    wktvl__sjuhv += f'    )\n'
    wktvl__sjuhv += f'    check_and_propagate_cpp_exception()\n'
    byv__osbvn = 'None'
    iqb__aukk = index_column_type
    pvj__ose = TableType(tuple(out_types))
    if mnu__ymuzj:
        pvj__ose = types.none
    if index_column_index is not None:
        xiy__drntb = rdlcn__jqi[index_column_index]
        byv__osbvn = (
            f'info_to_array(info_from_table(out_table, {xiy__drntb}), index_arr_type)'
            )
    wktvl__sjuhv += f'    index_arr = {byv__osbvn}\n'
    if mnu__ymuzj:
        vhij__sgz = None
    else:
        vhij__sgz = []
        tjwox__ojr = 0
        tkvvs__myq = col_indices[col_names.index(input_file_name_col)
            ] if input_file_name_col is not None else None
        for mifb__wph, mvtuq__sows in enumerate(col_indices):
            if tjwox__ojr < len(type_usecol_offset
                ) and mifb__wph == type_usecol_offset[tjwox__ojr]:
                fjaqy__bnjo = col_indices[mifb__wph]
                if tkvvs__myq and fjaqy__bnjo == tkvvs__myq:
                    vhij__sgz.append(len(eshl__inxdw) + len(fgsj__bucr))
                elif fjaqy__bnjo in mwbri__mgawb:
                    jkfp__fhtuz = wcah__mzig[mifb__wph]
                    vhij__sgz.append(len(eshl__inxdw) + dquzj__gqff[
                        jkfp__fhtuz])
                else:
                    vhij__sgz.append(rdlcn__jqi[mvtuq__sows])
                tjwox__ojr += 1
            else:
                vhij__sgz.append(-1)
        vhij__sgz = np.array(vhij__sgz, dtype=np.int64)
    if mnu__ymuzj:
        wktvl__sjuhv += '    T = None\n'
    else:
        wktvl__sjuhv += f"""    T = cpp_table_to_py_table(out_table, table_idx_{vxa__qxei}, py_table_type_{vxa__qxei})
"""
    wktvl__sjuhv += f'    delete_table(out_table)\n'
    wktvl__sjuhv += f'    total_rows = total_rows_np[0]\n'
    wktvl__sjuhv += f'    ev.finalize()\n'
    wktvl__sjuhv += f'    return (total_rows, T, index_arr)\n'
    mjt__wfbuy = {}
    fpsm__lxnh = {f'py_table_type_{vxa__qxei}': pvj__ose,
        f'table_idx_{vxa__qxei}': vhij__sgz,
        f'selected_cols_arr_{vxa__qxei}': np.array(eshl__inxdw, np.int32),
        f'nullable_cols_arr_{vxa__qxei}': np.array(elkpd__ryac, np.int32),
        'index_arr_type': iqb__aukk, 'cpp_table_to_py_table':
        cpp_table_to_py_table, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'delete_table': delete_table,
        'check_and_propagate_cpp_exception':
        check_and_propagate_cpp_exception, 'pq_read': _pq_read,
        'unicode_to_utf8': unicode_to_utf8, 'get_filters_pyobject':
        get_filters_pyobject, 'get_storage_options_pyobject':
        get_storage_options_pyobject, 'get_fname_pyobject':
        get_fname_pyobject, 'np': np, 'pd': pd, 'bodo': bodo}
    exec(wktvl__sjuhv, fpsm__lxnh, mjt__wfbuy)
    qtdr__fxrp = mjt__wfbuy['pq_reader_py']
    zgivd__eag = numba.njit(qtdr__fxrp, no_cpython_wrapper=True)
    return zgivd__eag


import pyarrow as pa
_pa_numba_typ_map = {pa.bool_(): types.bool_, pa.int8(): types.int8, pa.
    int16(): types.int16, pa.int32(): types.int32, pa.int64(): types.int64,
    pa.uint8(): types.uint8, pa.uint16(): types.uint16, pa.uint32(): types.
    uint32, pa.uint64(): types.uint64, pa.float32(): types.float32, pa.
    float64(): types.float64, pa.string(): string_type, pa.binary():
    bytes_type, pa.date32(): datetime_date_type, pa.date64(): types.
    NPDatetime('ns'), null(): string_type}


def get_arrow_timestamp_type(pa_ts_typ):
    fhc__cipr = 'ns', 'us', 'ms', 's'
    if pa_ts_typ.unit not in fhc__cipr:
        return types.Array(bodo.datetime64ns, 1, 'C'), False
    elif pa_ts_typ.tz is not None:
        soj__cykrg = pa_ts_typ.to_pandas_dtype().tz
        skef__iuji = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(
            soj__cykrg)
        return bodo.DatetimeArrayType(skef__iuji), True
    else:
        return types.Array(bodo.datetime64ns, 1, 'C'), True


def _get_numba_typ_from_pa_typ(pa_typ, is_index, nullable_from_metadata,
    category_info, str_as_dict=False):
    if isinstance(pa_typ.type, pa.ListType):
        zgncw__bjd, try__wss = _get_numba_typ_from_pa_typ(pa_typ.type.
            value_field, is_index, nullable_from_metadata, category_info)
        return ArrayItemArrayType(zgncw__bjd), try__wss
    if isinstance(pa_typ.type, pa.StructType):
        rmkbr__mhjt = []
        vghkf__uvnu = []
        try__wss = True
        for mfdb__mjakn in pa_typ.flatten():
            vghkf__uvnu.append(mfdb__mjakn.name.split('.')[-1])
            ohvu__ffega, iuomq__ejkap = _get_numba_typ_from_pa_typ(mfdb__mjakn,
                is_index, nullable_from_metadata, category_info)
            rmkbr__mhjt.append(ohvu__ffega)
            try__wss = try__wss and iuomq__ejkap
        return StructArrayType(tuple(rmkbr__mhjt), tuple(vghkf__uvnu)
            ), try__wss
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
        mwcv__nun = _pa_numba_typ_map[pa_typ.type.index_type]
        tih__pbh = PDCategoricalDtype(category_info[pa_typ.name], bodo.
            string_type, pa_typ.type.ordered, int_type=mwcv__nun)
        return CategoricalArrayType(tih__pbh), True
    if isinstance(pa_typ.type, pa.lib.TimestampType):
        return get_arrow_timestamp_type(pa_typ.type)
    elif pa_typ.type in _pa_numba_typ_map:
        tqh__obj = _pa_numba_typ_map[pa_typ.type]
        try__wss = True
    else:
        raise BodoError('Arrow data type {} not supported yet'.format(
            pa_typ.type))
    if tqh__obj == datetime_date_type:
        return datetime_date_array_type, try__wss
    if tqh__obj == bytes_type:
        return binary_array_type, try__wss
    zgncw__bjd = string_array_type if tqh__obj == string_type else types.Array(
        tqh__obj, 1, 'C')
    if tqh__obj == types.bool_:
        zgncw__bjd = boolean_array
    if nullable_from_metadata is not None:
        xplr__nudez = nullable_from_metadata
    else:
        xplr__nudez = use_nullable_int_arr
    if xplr__nudez and not is_index and isinstance(tqh__obj, types.Integer
        ) and pa_typ.nullable:
        zgncw__bjd = IntegerArrayType(tqh__obj)
    return zgncw__bjd, try__wss


def get_parquet_dataset(fpath, get_row_counts=True, dnf_filters=None,
    expr_filters=None, storage_options=None, read_categories=False,
    is_parallel=False, tot_rows_to_read=None, typing_pa_schema=None):
    if get_row_counts:
        hzwc__ivlt = tracing.Event('get_parquet_dataset')
    import time
    import pyarrow as pa
    import pyarrow.parquet as pq
    from mpi4py import MPI
    ddge__hzvxq = MPI.COMM_WORLD
    if isinstance(fpath, list):
        crp__hxh = urlparse(fpath[0])
        protocol = crp__hxh.scheme
        queq__ljk = crp__hxh.netloc
        for mifb__wph in range(len(fpath)):
            cyw__tfig = fpath[mifb__wph]
            thi__zap = urlparse(cyw__tfig)
            if thi__zap.scheme != protocol:
                raise BodoError(
                    'All parquet files must use the same filesystem protocol')
            if thi__zap.netloc != queq__ljk:
                raise BodoError(
                    'All parquet files must be in the same S3 bucket')
            fpath[mifb__wph] = cyw__tfig.rstrip('/')
    else:
        crp__hxh = urlparse(fpath)
        protocol = crp__hxh.scheme
        fpath = fpath.rstrip('/')
    if protocol in {'gcs', 'gs'}:
        try:
            import gcsfs
        except ImportError as yxa__sgmn:
            mynlg__gnvmw = """Couldn't import gcsfs, which is required for Google cloud access. gcsfs can be installed by calling 'conda install -c conda-forge gcsfs'.
"""
            raise BodoError(mynlg__gnvmw)
    if protocol == 'http':
        try:
            import fsspec
        except ImportError as yxa__sgmn:
            mynlg__gnvmw = """Couldn't import fsspec, which is required for http access. fsspec can be installed by calling 'conda install -c conda-forge fsspec'.
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
            vkjrm__nrp = gcsfs.GCSFileSystem(token=None)
            fs.append(vkjrm__nrp)
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
                prefix = f'{protocol}://{crp__hxh.netloc}'
                path = path[len(prefix):]
            vvi__hjezn = fs.glob(path)
            if protocol == 's3':
                vvi__hjezn = [('s3://' + cyw__tfig) for cyw__tfig in
                    vvi__hjezn if not cyw__tfig.startswith('s3://')]
            elif protocol in {'hdfs', 'abfs', 'abfss'}:
                vvi__hjezn = [(prefix + cyw__tfig) for cyw__tfig in vvi__hjezn]
        except:
            raise BodoError(
                f'glob pattern expansion not supported for {protocol}')
        if len(vvi__hjezn) == 0:
            raise BodoError('No files found matching glob pattern')
        return vvi__hjezn
    gyt__wdai = False
    if get_row_counts:
        pljnr__cnlrt = getfs(parallel=True)
        gyt__wdai = bodo.parquet_validate_schema
    if bodo.get_rank() == 0:
        pvusr__qluo = 1
        ivszt__leb = os.cpu_count()
        if ivszt__leb is not None and ivszt__leb > 1:
            pvusr__qluo = ivszt__leb // 2
        try:
            if get_row_counts:
                kmr__wht = tracing.Event('pq.ParquetDataset', is_parallel=False
                    )
                if tracing.is_tracing():
                    kmr__wht.add_attribute('g_dnf_filter', str(dnf_filters))
            rlp__iryxn = pa.io_thread_count()
            pa.set_io_thread_count(pvusr__qluo)
            if isinstance(fpath, list):
                eyv__tieq = []
                for dastt__cqu in fpath:
                    if has_magic(dastt__cqu):
                        eyv__tieq += glob(protocol, getfs(), dastt__cqu)
                    else:
                        eyv__tieq.append(dastt__cqu)
                fpath = eyv__tieq
            elif has_magic(fpath):
                fpath = glob(protocol, getfs(), fpath)
            if protocol == 's3':
                if isinstance(fpath, list):
                    get_legacy_fs().info(fpath[0])
                else:
                    get_legacy_fs().info(fpath)
            if protocol in {'hdfs', 'abfs', 'abfss'}:
                prefix = f'{protocol}://{crp__hxh.netloc}'
                if isinstance(fpath, list):
                    sth__mwt = [cyw__tfig[len(prefix):] for cyw__tfig in fpath]
                else:
                    sth__mwt = fpath[len(prefix):]
            else:
                sth__mwt = fpath
            zxcru__hyevg = pq.ParquetDataset(sth__mwt, filesystem=
                get_legacy_fs(), filters=None, use_legacy_dataset=True,
                validate_schema=False, metadata_nthreads=pvusr__qluo)
            pa.set_io_thread_count(rlp__iryxn)
            if typing_pa_schema:
                oyw__grz = typing_pa_schema
            else:
                oyw__grz = bodo.io.pa_parquet.get_dataset_schema(zxcru__hyevg)
            if dnf_filters:
                if get_row_counts:
                    kmr__wht.add_attribute('num_pieces_before_filter', len(
                        zxcru__hyevg.pieces))
                bend__afx = time.time()
                zxcru__hyevg._filter(dnf_filters)
                if get_row_counts:
                    kmr__wht.add_attribute('dnf_filter_time', time.time() -
                        bend__afx)
                    kmr__wht.add_attribute('num_pieces_after_filter', len(
                        zxcru__hyevg.pieces))
            if get_row_counts:
                kmr__wht.finalize()
            zxcru__hyevg._metadata.fs = None
        except Exception as clr__dfw:
            if isinstance(fpath, list) and isinstance(clr__dfw, (OSError,
                FileNotFoundError)):
                clr__dfw = BodoError(str(clr__dfw) + list_of_files_error_msg)
            else:
                clr__dfw = BodoError(
                    f"""error from pyarrow: {type(clr__dfw).__name__}: {str(clr__dfw)}
"""
                    )
            ddge__hzvxq.bcast(clr__dfw)
            raise clr__dfw
        if get_row_counts:
            cpjrk__ehn = tracing.Event('bcast dataset')
        ddge__hzvxq.bcast(zxcru__hyevg)
        ddge__hzvxq.bcast(oyw__grz)
    else:
        if get_row_counts:
            cpjrk__ehn = tracing.Event('bcast dataset')
        zxcru__hyevg = ddge__hzvxq.bcast(None)
        if isinstance(zxcru__hyevg, Exception):
            eqx__aqbvi = zxcru__hyevg
            raise eqx__aqbvi
        oyw__grz = ddge__hzvxq.bcast(None)
    cnp__nctx = set(oyw__grz.names)
    if get_row_counts:
        coru__oyj = getfs()
    else:
        coru__oyj = get_legacy_fs()
    zxcru__hyevg._metadata.fs = coru__oyj
    if get_row_counts:
        cpjrk__ehn.finalize()
    zxcru__hyevg._bodo_total_rows = 0
    if get_row_counts and tot_rows_to_read == 0:
        get_row_counts = gyt__wdai = False
        for dastt__cqu in zxcru__hyevg.pieces:
            dastt__cqu._bodo_num_rows = 0
    if get_row_counts or gyt__wdai:
        if get_row_counts and tracing.is_tracing():
            njzyk__sus = tracing.Event('get_row_counts')
            njzyk__sus.add_attribute('g_num_pieces', len(zxcru__hyevg.pieces))
            njzyk__sus.add_attribute('g_expr_filters', str(expr_filters))
        ktlmt__mfuxb = 0.0
        num_pieces = len(zxcru__hyevg.pieces)
        start = get_start(num_pieces, bodo.get_size(), bodo.get_rank())
        rsgt__kiva = get_end(num_pieces, bodo.get_size(), bodo.get_rank())
        dkdoi__ewf = 0
        bxpka__gqc = 0
        ulc__ntjif = 0
        jqif__cdj = True
        if expr_filters is not None:
            import random
            random.seed(37)
            dbj__znhn = random.sample(zxcru__hyevg.pieces, k=len(
                zxcru__hyevg.pieces))
        else:
            dbj__znhn = zxcru__hyevg.pieces
        for dastt__cqu in dbj__znhn:
            dastt__cqu._bodo_num_rows = 0
        fpaths = [dastt__cqu.path for dastt__cqu in dbj__znhn[start:rsgt__kiva]
            ]
        if protocol == 's3':
            queq__ljk = crp__hxh.netloc
            prefix = 's3://' + queq__ljk + '/'
            fpaths = [cyw__tfig[len(prefix):] for cyw__tfig in fpaths]
            coru__oyj = get_s3_subtree_fs(queq__ljk, region=getfs().region,
                storage_options=storage_options)
        else:
            coru__oyj = getfs()
        pvusr__qluo = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), 4)
        pa.set_io_thread_count(pvusr__qluo)
        pa.set_cpu_count(pvusr__qluo)
        eqx__aqbvi = None
        try:
            jfw__jhqv = ds.dataset(fpaths, filesystem=coru__oyj,
                partitioning=ds.partitioning(flavor='hive') if zxcru__hyevg
                .partitions else None)
            for zxjwk__spggw, led__lvuur in zip(dbj__znhn[start:rsgt__kiva],
                jfw__jhqv.get_fragments()):
                if gyt__wdai:
                    uudq__lkubr = led__lvuur.metadata.schema.to_arrow_schema()
                    zjb__dovoa = set(uudq__lkubr.names)
                    if cnp__nctx != zjb__dovoa:
                        rzem__qcomd = zjb__dovoa - cnp__nctx
                        gvgdv__ekvc = cnp__nctx - zjb__dovoa
                        ujh__lre = f'Schema in {zxjwk__spggw} was different.\n'
                        if rzem__qcomd:
                            ujh__lre += f"""File contains column(s) {rzem__qcomd} not found in other files in the dataset.
"""
                        if gvgdv__ekvc:
                            ujh__lre += f"""File missing column(s) {gvgdv__ekvc} found in other files in the dataset.
"""
                        raise BodoError(ujh__lre)
                    try:
                        oyw__grz = pa.unify_schemas([oyw__grz, uudq__lkubr])
                    except Exception as clr__dfw:
                        ujh__lre = (
                            f'Schema in {zxjwk__spggw} was different.\n' +
                            str(clr__dfw))
                        raise BodoError(ujh__lre)
                bend__afx = time.time()
                gdyf__nkstj = led__lvuur.scanner(schema=jfw__jhqv.schema,
                    filter=expr_filters, use_threads=True).count_rows()
                ktlmt__mfuxb += time.time() - bend__afx
                zxjwk__spggw._bodo_num_rows = gdyf__nkstj
                dkdoi__ewf += gdyf__nkstj
                bxpka__gqc += led__lvuur.num_row_groups
                ulc__ntjif += sum(qwra__tybw.total_byte_size for qwra__tybw in
                    led__lvuur.row_groups)
        except Exception as clr__dfw:
            eqx__aqbvi = clr__dfw
        if ddge__hzvxq.allreduce(eqx__aqbvi is not None, op=MPI.LOR):
            for eqx__aqbvi in ddge__hzvxq.allgather(eqx__aqbvi):
                if eqx__aqbvi:
                    if isinstance(fpath, list) and isinstance(eqx__aqbvi, (
                        OSError, FileNotFoundError)):
                        raise BodoError(str(eqx__aqbvi) +
                            list_of_files_error_msg)
                    raise eqx__aqbvi
        if gyt__wdai:
            jqif__cdj = ddge__hzvxq.allreduce(jqif__cdj, op=MPI.LAND)
            if not jqif__cdj:
                raise BodoError("Schema in parquet files don't match")
        if get_row_counts:
            zxcru__hyevg._bodo_total_rows = ddge__hzvxq.allreduce(dkdoi__ewf,
                op=MPI.SUM)
            dxvss__pigck = ddge__hzvxq.allreduce(bxpka__gqc, op=MPI.SUM)
            djdcy__yzync = ddge__hzvxq.allreduce(ulc__ntjif, op=MPI.SUM)
            thwf__bqcu = np.array([dastt__cqu._bodo_num_rows for dastt__cqu in
                zxcru__hyevg.pieces])
            thwf__bqcu = ddge__hzvxq.allreduce(thwf__bqcu, op=MPI.SUM)
            for dastt__cqu, zqvvb__lxnsn in zip(zxcru__hyevg.pieces, thwf__bqcu
                ):
                dastt__cqu._bodo_num_rows = zqvvb__lxnsn
            if is_parallel and bodo.get_rank(
                ) == 0 and dxvss__pigck < bodo.get_size(
                ) and dxvss__pigck != 0:
                warnings.warn(BodoWarning(
                    f"""Total number of row groups in parquet dataset {fpath} ({dxvss__pigck}) is too small for effective IO parallelization.
For best performance the number of row groups should be greater than the number of workers ({bodo.get_size()}). For more details, refer to
https://docs.bodo.ai/latest/file_io/#parquet-section.
"""
                    ))
            if dxvss__pigck == 0:
                mekz__yde = 0
            else:
                mekz__yde = djdcy__yzync // dxvss__pigck
            if (bodo.get_rank() == 0 and djdcy__yzync >= 20 * 1048576 and 
                mekz__yde < 1048576 and protocol in REMOTE_FILESYSTEMS):
                warnings.warn(BodoWarning(
                    f'Parquet average row group size is small ({mekz__yde} bytes) and can have negative impact on performance when reading from remote sources'
                    ))
            if tracing.is_tracing():
                njzyk__sus.add_attribute('g_total_num_row_groups', dxvss__pigck
                    )
                njzyk__sus.add_attribute('total_scan_time', ktlmt__mfuxb)
                xqk__teuky = np.array([dastt__cqu._bodo_num_rows for
                    dastt__cqu in zxcru__hyevg.pieces])
                sco__ocg = np.percentile(xqk__teuky, [25, 50, 75])
                njzyk__sus.add_attribute('g_row_counts_min', xqk__teuky.min())
                njzyk__sus.add_attribute('g_row_counts_Q1', sco__ocg[0])
                njzyk__sus.add_attribute('g_row_counts_median', sco__ocg[1])
                njzyk__sus.add_attribute('g_row_counts_Q3', sco__ocg[2])
                njzyk__sus.add_attribute('g_row_counts_max', xqk__teuky.max())
                njzyk__sus.add_attribute('g_row_counts_mean', xqk__teuky.mean()
                    )
                njzyk__sus.add_attribute('g_row_counts_std', xqk__teuky.std())
                njzyk__sus.add_attribute('g_row_counts_sum', xqk__teuky.sum())
                njzyk__sus.finalize()
    zxcru__hyevg._prefix = ''
    if protocol in {'hdfs', 'abfs', 'abfss'}:
        prefix = f'{protocol}://{crp__hxh.netloc}'
        if len(zxcru__hyevg.pieces) > 0:
            zxjwk__spggw = zxcru__hyevg.pieces[0]
            if not zxjwk__spggw.path.startswith(prefix):
                zxcru__hyevg._prefix = prefix
    if read_categories:
        _add_categories_to_pq_dataset(zxcru__hyevg)
    if get_row_counts:
        hzwc__ivlt.finalize()
    if gyt__wdai and is_parallel:
        if tracing.is_tracing():
            pkgpl__koyj = tracing.Event('unify_schemas_across_ranks')
        eqx__aqbvi = None
        try:
            oyw__grz = ddge__hzvxq.allreduce(oyw__grz, bodo.io.helpers.
                pa_schema_unify_mpi_op)
        except Exception as clr__dfw:
            eqx__aqbvi = clr__dfw
        if tracing.is_tracing():
            pkgpl__koyj.finalize()
        if ddge__hzvxq.allreduce(eqx__aqbvi is not None, op=MPI.LOR):
            for eqx__aqbvi in ddge__hzvxq.allgather(eqx__aqbvi):
                if eqx__aqbvi:
                    ujh__lre = f'Schema in some files were different.\n' + str(
                        eqx__aqbvi)
                    raise BodoError(ujh__lre)
    zxcru__hyevg._bodo_arrow_schema = oyw__grz
    return zxcru__hyevg


def get_scanner_batches(fpaths, expr_filters, selected_fields,
    avg_num_pieces, is_parallel, storage_options, region, prefix,
    str_as_dict_cols, start_offset, rows_to_read, has_partitions, schema):
    import pyarrow as pa
    ivszt__leb = os.cpu_count()
    if ivszt__leb is None or ivszt__leb == 0:
        ivszt__leb = 2
    uaf__zexxz = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), ivszt__leb)
    dab__qas = min(int(os.environ.get('BODO_MAX_IO_THREADS', 16)), ivszt__leb)
    if is_parallel and len(fpaths) > dab__qas and len(fpaths
        ) / avg_num_pieces >= 2.0:
        pa.set_io_thread_count(dab__qas)
        pa.set_cpu_count(dab__qas)
    else:
        pa.set_io_thread_count(uaf__zexxz)
        pa.set_cpu_count(uaf__zexxz)
    if fpaths[0].startswith('s3://'):
        queq__ljk = urlparse(fpaths[0]).netloc
        prefix = 's3://' + queq__ljk + '/'
        fpaths = [cyw__tfig[len(prefix):] for cyw__tfig in fpaths]
        if region == '':
            region = get_s3_bucket_region_njit(fpaths[0], parallel=False)
        coru__oyj = get_s3_subtree_fs(queq__ljk, region=region,
            storage_options=storage_options)
    elif prefix and prefix.startswith(('hdfs', 'abfs', 'abfss')):
        coru__oyj = get_hdfs_fs(prefix + fpaths[0])
    elif fpaths[0].startswith(('gcs', 'gs')):
        import gcsfs
        coru__oyj = gcsfs.GCSFileSystem(token=None)
    else:
        coru__oyj = None
    jwcmi__lqu = ds.ParquetFileFormat(dictionary_columns=str_as_dict_cols)
    zxcru__hyevg = ds.dataset(fpaths, filesystem=coru__oyj, partitioning=ds
        .partitioning(flavor='hive') if has_partitions else None, format=
        jwcmi__lqu)
    nmqb__dum = set(str_as_dict_cols)
    ntf__qdxav = schema.names
    for mifb__wph, name in enumerate(ntf__qdxav):
        if name in nmqb__dum:
            fgivo__boz = schema.field(mifb__wph)
            lzs__zcm = pa.field(name, pa.dictionary(pa.int32(), fgivo__boz.
                type), fgivo__boz.nullable)
            schema = schema.remove(mifb__wph).insert(mifb__wph, lzs__zcm)
    zxcru__hyevg = zxcru__hyevg.replace_schema(pa.unify_schemas([
        zxcru__hyevg.schema, schema]))
    col_names = zxcru__hyevg.schema.names
    dji__nwci = [col_names[sqokp__vabl] for sqokp__vabl in selected_fields]
    dhx__rudpm = len(fpaths) <= 3 or start_offset > 0 and len(fpaths) <= 10
    if dhx__rudpm and expr_filters is None:
        imppc__rsg = []
        kieh__uzr = 0
        msajl__idz = 0
        for led__lvuur in zxcru__hyevg.get_fragments():
            wuad__mteia = []
            for qwra__tybw in led__lvuur.row_groups:
                bmewe__lvjt = qwra__tybw.num_rows
                if start_offset < kieh__uzr + bmewe__lvjt:
                    if msajl__idz == 0:
                        any__jjtbj = start_offset - kieh__uzr
                        cte__wic = min(bmewe__lvjt - any__jjtbj, rows_to_read)
                    else:
                        cte__wic = min(bmewe__lvjt, rows_to_read - msajl__idz)
                    msajl__idz += cte__wic
                    wuad__mteia.append(qwra__tybw.id)
                kieh__uzr += bmewe__lvjt
                if msajl__idz == rows_to_read:
                    break
            imppc__rsg.append(led__lvuur.subset(row_group_ids=wuad__mteia))
            if msajl__idz == rows_to_read:
                break
        zxcru__hyevg = ds.FileSystemDataset(imppc__rsg, zxcru__hyevg.schema,
            jwcmi__lqu, filesystem=zxcru__hyevg.filesystem)
        start_offset = any__jjtbj
    xnxg__mdq = zxcru__hyevg.scanner(columns=dji__nwci, filter=expr_filters,
        use_threads=True).to_reader()
    return zxcru__hyevg, xnxg__mdq, start_offset


def _add_categories_to_pq_dataset(pq_dataset):
    import pyarrow as pa
    from mpi4py import MPI
    if len(pq_dataset.pieces) < 1:
        raise BodoError(
            'No pieces found in Parquet dataset. Cannot get read categorical values'
            )
    pa_schema = pq_dataset.schema.to_arrow_schema()
    tzyh__ghjw = [c for c in pa_schema.names if isinstance(pa_schema.field(
        c).type, pa.DictionaryType)]
    if len(tzyh__ghjw) == 0:
        pq_dataset._category_info = {}
        return
    ddge__hzvxq = MPI.COMM_WORLD
    if bodo.get_rank() == 0:
        try:
            vttc__ahqp = pq_dataset.pieces[0].open()
            qwra__tybw = vttc__ahqp.read_row_group(0, tzyh__ghjw)
            category_info = {c: tuple(qwra__tybw.column(c).chunk(0).
                dictionary.to_pylist()) for c in tzyh__ghjw}
            del vttc__ahqp, qwra__tybw
        except Exception as clr__dfw:
            ddge__hzvxq.bcast(clr__dfw)
            raise clr__dfw
        ddge__hzvxq.bcast(category_info)
    else:
        category_info = ddge__hzvxq.bcast(None)
        if isinstance(category_info, Exception):
            eqx__aqbvi = category_info
            raise eqx__aqbvi
    pq_dataset._category_info = category_info


def get_pandas_metadata(schema, num_pieces):
    dbl__jhon = None
    nullable_from_metadata = defaultdict(lambda : None)
    mklg__jwq = b'pandas'
    if schema.metadata is not None and mklg__jwq in schema.metadata:
        import json
        manq__zunld = json.loads(schema.metadata[mklg__jwq].decode('utf8'))
        vbuea__bgcn = len(manq__zunld['index_columns'])
        if vbuea__bgcn > 1:
            raise BodoError('read_parquet: MultiIndex not supported yet')
        dbl__jhon = manq__zunld['index_columns'][0] if vbuea__bgcn else None
        if not isinstance(dbl__jhon, str) and not isinstance(dbl__jhon, dict):
            dbl__jhon = None
        for aotxj__vhhkb in manq__zunld['columns']:
            xxrj__qkxk = aotxj__vhhkb['name']
            if aotxj__vhhkb['pandas_type'].startswith('int'
                ) and xxrj__qkxk is not None:
                if aotxj__vhhkb['numpy_type'].startswith('Int'):
                    nullable_from_metadata[xxrj__qkxk] = True
                else:
                    nullable_from_metadata[xxrj__qkxk] = False
    return dbl__jhon, nullable_from_metadata


def get_str_columns_from_pa_schema(pa_schema):
    str_columns = []
    for xxrj__qkxk in pa_schema.names:
        mfdb__mjakn = pa_schema.field(xxrj__qkxk)
        if mfdb__mjakn.type == pa.string():
            str_columns.append(xxrj__qkxk)
    return str_columns


def determine_str_as_dict_columns(pq_dataset, pa_schema, str_columns):
    from mpi4py import MPI
    ddge__hzvxq = MPI.COMM_WORLD
    if len(str_columns) == 0:
        return set()
    if len(pq_dataset.pieces) > bodo.get_size():
        import random
        random.seed(37)
        dbj__znhn = random.sample(pq_dataset.pieces, bodo.get_size())
    else:
        dbj__znhn = pq_dataset.pieces
    gdfm__iti = np.zeros(len(str_columns), dtype=np.int64)
    gicy__tzey = np.zeros(len(str_columns), dtype=np.int64)
    if bodo.get_rank() < len(dbj__znhn):
        zxjwk__spggw = dbj__znhn[bodo.get_rank()]
        try:
            qdzvx__jxk = zxjwk__spggw.get_metadata()
            for mifb__wph in range(qdzvx__jxk.num_row_groups):
                for tjwox__ojr, xxrj__qkxk in enumerate(str_columns):
                    setu__egfo = pa_schema.get_field_index(xxrj__qkxk)
                    gdfm__iti[tjwox__ojr] += qdzvx__jxk.row_group(mifb__wph
                        ).column(setu__egfo).total_uncompressed_size
            ixojw__jubk = qdzvx__jxk.num_rows
        except Exception as clr__dfw:
            if isinstance(clr__dfw, (OSError, FileNotFoundError)):
                ixojw__jubk = 0
            else:
                raise
    else:
        ixojw__jubk = 0
    fao__mswxu = ddge__hzvxq.allreduce(ixojw__jubk, op=MPI.SUM)
    if fao__mswxu == 0:
        return set()
    ddge__hzvxq.Allreduce(gdfm__iti, gicy__tzey, op=MPI.SUM)
    qiyr__irfq = gicy__tzey / fao__mswxu
    str_as_dict = set()
    for mifb__wph, ufq__kyb in enumerate(qiyr__irfq):
        if ufq__kyb < READ_STR_AS_DICT_THRESHOLD:
            xxrj__qkxk = str_columns[mifb__wph][0]
            str_as_dict.add(xxrj__qkxk)
    return str_as_dict


def parquet_file_schema(file_name, selected_columns, storage_options=None,
    input_file_name_col=None, read_as_dict_cols=None):
    col_names = []
    bujpe__dehju = []
    pq_dataset = get_parquet_dataset(file_name, get_row_counts=False,
        storage_options=storage_options, read_categories=True)
    if hasattr(pq_dataset, '_bodo_arrow_schema'):
        pa_schema = pq_dataset._bodo_arrow_schema
    else:
        pa_schema = pq_dataset.schema.to_arrow_schema()
    partition_names = [] if pq_dataset.partitions is None else [pq_dataset.
        partitions.levels[mifb__wph].name for mifb__wph in range(len(
        pq_dataset.partitions.partition_names))]
    num_pieces = len(pq_dataset.pieces)
    str_columns = get_str_columns_from_pa_schema(pa_schema)
    uugei__spzzh = set(str_columns)
    if read_as_dict_cols is None:
        read_as_dict_cols = []
    read_as_dict_cols = set(read_as_dict_cols)
    rgm__desl = read_as_dict_cols - uugei__spzzh
    if len(rgm__desl) > 0:
        if bodo.get_rank() == 0:
            warnings.warn(
                f'The following columns are not of datatype string and hence cannot be read with dictionary encoding: {rgm__desl}'
                , bodo.utils.typing.BodoWarning)
    read_as_dict_cols.intersection_update(uugei__spzzh)
    uugei__spzzh = uugei__spzzh - read_as_dict_cols
    str_columns = [fkb__gmw for fkb__gmw in str_columns if fkb__gmw in
        uugei__spzzh]
    str_as_dict: set = determine_str_as_dict_columns(pq_dataset, pa_schema,
        str_columns)
    str_as_dict.update(read_as_dict_cols)
    col_names = pa_schema.names
    dbl__jhon, nullable_from_metadata = get_pandas_metadata(pa_schema,
        num_pieces)
    wfp__pipfk = []
    olv__pkb = []
    tco__cwxpa = []
    for mifb__wph, c in enumerate(col_names):
        mfdb__mjakn = pa_schema.field(c)
        tqh__obj, try__wss = _get_numba_typ_from_pa_typ(mfdb__mjakn, c ==
            dbl__jhon, nullable_from_metadata[c], pq_dataset._category_info,
            str_as_dict=c in str_as_dict)
        wfp__pipfk.append(tqh__obj)
        olv__pkb.append(try__wss)
        tco__cwxpa.append(mfdb__mjakn.type)
    if partition_names:
        col_names += partition_names
        wfp__pipfk += [_get_partition_cat_dtype(pq_dataset.partitions.
            levels[mifb__wph]) for mifb__wph in range(len(partition_names))]
        olv__pkb.extend([True] * len(partition_names))
        tco__cwxpa.extend([None] * len(partition_names))
    if input_file_name_col is not None:
        col_names += [input_file_name_col]
        wfp__pipfk += [dict_str_arr_type]
        olv__pkb.append(True)
        tco__cwxpa.append(None)
    nei__trt = {c: mifb__wph for mifb__wph, c in enumerate(col_names)}
    if selected_columns is None:
        selected_columns = col_names
    for c in selected_columns:
        if c not in nei__trt:
            raise BodoError(f'Selected column {c} not in Parquet file schema')
    if dbl__jhon and not isinstance(dbl__jhon, dict
        ) and dbl__jhon not in selected_columns:
        selected_columns.append(dbl__jhon)
    col_names = selected_columns
    col_indices = []
    bujpe__dehju = []
    rqf__vkuw = []
    pbax__lsjpg = []
    for mifb__wph, c in enumerate(col_names):
        fjaqy__bnjo = nei__trt[c]
        col_indices.append(fjaqy__bnjo)
        bujpe__dehju.append(wfp__pipfk[fjaqy__bnjo])
        if not olv__pkb[fjaqy__bnjo]:
            rqf__vkuw.append(mifb__wph)
            pbax__lsjpg.append(tco__cwxpa[fjaqy__bnjo])
    return (col_names, bujpe__dehju, dbl__jhon, col_indices,
        partition_names, rqf__vkuw, pbax__lsjpg)


def _get_partition_cat_dtype(part_set):
    rkwn__til = part_set.dictionary.to_pandas()
    rxdnr__fkjk = bodo.typeof(rkwn__til).dtype
    tih__pbh = PDCategoricalDtype(tuple(rkwn__til), rxdnr__fkjk, False)
    return CategoricalArrayType(tih__pbh)


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
        ejw__evkv = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(32), lir.IntType(32),
            lir.IntType(32), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        vize__fofa = cgutils.get_or_insert_function(builder.module,
            ejw__evkv, name='pq_write')
        builder.call(vize__fofa, args)
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
        ejw__evkv = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        vize__fofa = cgutils.get_or_insert_function(builder.module,
            ejw__evkv, name='pq_write_partitioned')
        builder.call(vize__fofa, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
    return types.void(types.voidptr, data_table_t, col_names_t,
        col_names_no_partitions_t, cat_table_t, types.voidptr, types.int32,
        types.voidptr, types.boolean, types.voidptr, types.int64), codegen
