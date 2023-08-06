from collections import defaultdict
import numba
import numpy as np
import pandas as pd
from mpi4py import MPI
from numba.core import ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, replace_arg_nodes
import bodo
import bodo.ir.connector
from bodo import objmode
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.hiframes.table import Table, TableType
from bodo.io.fs_io import get_storage_options_pyobject, storage_options_dict_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType, string_array_type
from bodo.libs.str_ext import string_type
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.table_column_del_pass import ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.typing import BodoError
from bodo.utils.utils import check_java_installation
from bodo.utils.utils import sanitize_varname


class CsvReader(ir.Stmt):

    def __init__(self, file_name, df_out, sep, df_colnames, out_vars,
        out_types, usecols, loc, header, compression, nrows, skiprows,
        chunksize, is_skiprows_list, low_memory, escapechar,
        storage_options=None, index_column_index=None, index_column_typ=
        types.none):
        self.connector_typ = 'csv'
        self.file_name = file_name
        self.df_out = df_out
        self.sep = sep
        self.df_colnames = df_colnames
        self.out_vars = out_vars
        self.out_types = out_types
        self.usecols = usecols
        self.loc = loc
        self.skiprows = skiprows
        self.nrows = nrows
        self.header = header
        self.compression = compression
        self.chunksize = chunksize
        self.is_skiprows_list = is_skiprows_list
        self.pd_low_memory = low_memory
        self.escapechar = escapechar
        self.storage_options = storage_options
        self.index_column_index = index_column_index
        self.index_column_typ = index_column_typ
        self.type_usecol_offset = list(range(len(usecols)))

    def __repr__(self):
        return (
            '{} = ReadCsv(file={}, col_names={}, types={}, vars={}, nrows={}, skiprows={}, chunksize={}, is_skiprows_list={}, pd_low_memory={}, escapechar={}, storage_options={}, index_column_index={}, index_colum_typ = {}, type_usecol_offsets={})'
            .format(self.df_out, self.file_name, self.df_colnames, self.
            out_types, self.out_vars, self.nrows, self.skiprows, self.
            chunksize, self.is_skiprows_list, self.pd_low_memory, self.
            escapechar, self.storage_options, self.index_column_index, self
            .index_column_typ, self.type_usecol_offset))


def check_node_typing(node, typemap):
    izfk__pzig = typemap[node.file_name.name]
    if types.unliteral(izfk__pzig) != types.unicode_type:
        raise BodoError(
            f"pd.read_csv(): 'filepath_or_buffer' must be a string. Found type: {izfk__pzig}."
            , node.file_name.loc)
    if not isinstance(node.skiprows, ir.Const):
        uca__gje = typemap[node.skiprows.name]
        if isinstance(uca__gje, types.Dispatcher):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' callable not supported yet.",
                node.file_name.loc)
        elif not isinstance(uca__gje, types.Integer) and not (isinstance(
            uca__gje, (types.List, types.Tuple)) and isinstance(uca__gje.
            dtype, types.Integer)) and not isinstance(uca__gje, (types.
            LiteralList, bodo.utils.typing.ListLiteral)):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' must be an integer or list of integers. Found type {uca__gje}."
                , loc=node.skiprows.loc)
        elif isinstance(uca__gje, (types.List, types.Tuple)):
            node.is_skiprows_list = True
    if not isinstance(node.nrows, ir.Const):
        hchmi__nrr = typemap[node.nrows.name]
        if not isinstance(hchmi__nrr, types.Integer):
            raise BodoError(
                f"pd.read_csv(): 'nrows' must be an integer. Found type {hchmi__nrr}."
                , loc=node.nrows.loc)


import llvmlite.binding as ll
from bodo.io import csv_cpp
ll.add_symbol('csv_file_chunk_reader', csv_cpp.csv_file_chunk_reader)
csv_file_chunk_reader = types.ExternalFunction('csv_file_chunk_reader',
    bodo.ir.connector.stream_reader_type(types.voidptr, types.bool_, types.
    voidptr, types.int64, types.bool_, types.voidptr, types.voidptr,
    storage_options_dict_type, types.int64, types.bool_, types.int64, types
    .bool_))


def remove_dead_csv(csv_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    if csv_node.chunksize is not None:
        tdh__froip = csv_node.out_vars[0]
        if tdh__froip.name not in lives:
            return None
    else:
        bsg__wtyq = csv_node.out_vars[0]
        mkd__ysg = csv_node.out_vars[1]
        if bsg__wtyq.name not in lives and mkd__ysg.name not in lives:
            return None
        elif mkd__ysg.name not in lives:
            csv_node.index_column_index = None
            csv_node.index_column_typ = types.none
        elif bsg__wtyq.name not in lives:
            csv_node.usecols = []
            csv_node.out_types = []
            csv_node.type_usecol_offset = []
    return csv_node


def csv_distributed_run(csv_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    uca__gje = types.int64 if isinstance(csv_node.skiprows, ir.Const
        ) else types.unliteral(typemap[csv_node.skiprows.name])
    if csv_node.chunksize is not None:
        parallel = False
        if bodo.user_logging.get_verbose_level() >= 1:
            rbw__ruzq = (
                'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n'
                )
            iapc__hgf = csv_node.loc.strformat()
            lqbzc__csb = csv_node.df_colnames
            bodo.user_logging.log_message('Column Pruning', rbw__ruzq,
                iapc__hgf, lqbzc__csb)
            zsk__wbpmg = csv_node.out_types[0].yield_type.data
            hvljl__ftk = [ohl__pxmrf for padrb__awb, ohl__pxmrf in
                enumerate(csv_node.df_colnames) if isinstance(zsk__wbpmg[
                padrb__awb], bodo.libs.dict_arr_ext.DictionaryArrayType)]
            if hvljl__ftk:
                kpxo__bnorn = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
                bodo.user_logging.log_message('Dictionary Encoding',
                    kpxo__bnorn, iapc__hgf, hvljl__ftk)
        if array_dists is not None:
            zdhj__fshk = csv_node.out_vars[0].name
            parallel = array_dists[zdhj__fshk] in (distributed_pass.
                Distribution.OneD, distributed_pass.Distribution.OneD_Var)
        esbu__elul = 'def csv_iterator_impl(fname, nrows, skiprows):\n'
        esbu__elul += (
            f'    reader = _csv_reader_init(fname, nrows, skiprows)\n')
        esbu__elul += (
            f'    iterator = init_csv_iterator(reader, csv_iterator_type)\n')
        qxy__ertj = {}
        from bodo.io.csv_iterator_ext import init_csv_iterator
        exec(esbu__elul, {}, qxy__ertj)
        fvddk__pslw = qxy__ertj['csv_iterator_impl']
        mwyz__godc = 'def csv_reader_init(fname, nrows, skiprows):\n'
        mwyz__godc += _gen_csv_file_reader_init(parallel, csv_node.header,
            csv_node.compression, csv_node.chunksize, csv_node.
            is_skiprows_list, csv_node.pd_low_memory, csv_node.storage_options)
        mwyz__godc += '  return f_reader\n'
        exec(mwyz__godc, globals(), qxy__ertj)
        zgxvn__weioa = qxy__ertj['csv_reader_init']
        hehv__dycd = numba.njit(zgxvn__weioa)
        compiled_funcs.append(hehv__dycd)
        hemb__mclay = compile_to_numba_ir(fvddk__pslw, {'_csv_reader_init':
            hehv__dycd, 'init_csv_iterator': init_csv_iterator,
            'csv_iterator_type': typemap[csv_node.out_vars[0].name]},
            typingctx=typingctx, targetctx=targetctx, arg_typs=(string_type,
            types.int64, uca__gje), typemap=typemap, calltypes=calltypes
            ).blocks.popitem()[1]
        replace_arg_nodes(hemb__mclay, [csv_node.file_name, csv_node.nrows,
            csv_node.skiprows])
        gwdq__dbgjp = hemb__mclay.body[:-3]
        gwdq__dbgjp[-1].target = csv_node.out_vars[0]
        return gwdq__dbgjp
    parallel = bodo.ir.connector.is_connector_table_parallel(csv_node,
        array_dists, typemap, 'CSVReader')
    esbu__elul = 'def csv_impl(fname, nrows, skiprows):\n'
    esbu__elul += (
        f'    (table_val, idx_col) = _csv_reader_py(fname, nrows, skiprows)\n')
    qxy__ertj = {}
    exec(esbu__elul, {}, qxy__ertj)
    rnxw__dayyu = qxy__ertj['csv_impl']
    orr__lcc = csv_node.usecols
    if orr__lcc:
        orr__lcc = [csv_node.usecols[padrb__awb] for padrb__awb in csv_node
            .type_usecol_offset]
    if bodo.user_logging.get_verbose_level() >= 1:
        rbw__ruzq = (
            'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n')
        iapc__hgf = csv_node.loc.strformat()
        lqbzc__csb = []
        hvljl__ftk = []
        if orr__lcc:
            for padrb__awb in orr__lcc:
                fii__axx = csv_node.df_colnames[padrb__awb]
                lqbzc__csb.append(fii__axx)
                if isinstance(csv_node.out_types[padrb__awb], bodo.libs.
                    dict_arr_ext.DictionaryArrayType):
                    hvljl__ftk.append(fii__axx)
        bodo.user_logging.log_message('Column Pruning', rbw__ruzq,
            iapc__hgf, lqbzc__csb)
        if hvljl__ftk:
            kpxo__bnorn = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                kpxo__bnorn, iapc__hgf, hvljl__ftk)
    ajvk__fega = _gen_csv_reader_py(csv_node.df_colnames, csv_node.
        out_types, orr__lcc, csv_node.type_usecol_offset, csv_node.sep,
        parallel, csv_node.header, csv_node.compression, csv_node.
        is_skiprows_list, csv_node.pd_low_memory, csv_node.escapechar,
        csv_node.storage_options, idx_col_index=csv_node.index_column_index,
        idx_col_typ=csv_node.index_column_typ)
    hemb__mclay = compile_to_numba_ir(rnxw__dayyu, {'_csv_reader_py':
        ajvk__fega}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type, types.int64, uca__gje), typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(hemb__mclay, [csv_node.file_name, csv_node.nrows,
        csv_node.skiprows, csv_node.is_skiprows_list])
    gwdq__dbgjp = hemb__mclay.body[:-3]
    gwdq__dbgjp[-1].target = csv_node.out_vars[1]
    gwdq__dbgjp[-2].target = csv_node.out_vars[0]
    assert not (csv_node.index_column_index is None and not orr__lcc
        ), 'At most one of table and index should be dead if the CSV IR node is live'
    if csv_node.index_column_index is None:
        gwdq__dbgjp.pop(-1)
    elif not orr__lcc:
        gwdq__dbgjp.pop(-2)
    return gwdq__dbgjp


def csv_remove_dead_column(csv_node, column_live_map, equiv_vars, typemap):
    if csv_node.chunksize is not None:
        return False
    return bodo.ir.connector.base_connector_remove_dead_columns(csv_node,
        column_live_map, equiv_vars, typemap, 'CSVReader', csv_node.usecols)


numba.parfors.array_analysis.array_analysis_extensions[CsvReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[CsvReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[CsvReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[CsvReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[CsvReader] = remove_dead_csv
numba.core.analysis.ir_extension_usedefs[CsvReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[CsvReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[CsvReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[CsvReader
    ] = bodo.ir.connector.build_connector_definitions
distributed_pass.distributed_run_extensions[CsvReader] = csv_distributed_run
remove_dead_column_extensions[CsvReader] = csv_remove_dead_column
ir_extension_table_column_use[CsvReader
    ] = bodo.ir.connector.connector_table_column_use


def _get_dtype_str(t):
    tup__nhih = t.dtype
    if isinstance(tup__nhih, PDCategoricalDtype):
        badjb__qpgi = CategoricalArrayType(tup__nhih)
        eypy__wlaum = 'CategoricalArrayType' + str(ir_utils.next_label())
        setattr(types, eypy__wlaum, badjb__qpgi)
        return eypy__wlaum
    if tup__nhih == types.NPDatetime('ns'):
        tup__nhih = 'NPDatetime("ns")'
    if t == string_array_type:
        types.string_array_type = string_array_type
        return 'string_array_type'
    if isinstance(t, IntegerArrayType):
        ylpiy__mkk = 'int_arr_{}'.format(tup__nhih)
        setattr(types, ylpiy__mkk, t)
        return ylpiy__mkk
    if t == boolean_array:
        types.boolean_array = boolean_array
        return 'boolean_array'
    if tup__nhih == types.bool_:
        tup__nhih = 'bool_'
    if tup__nhih == datetime_date_type:
        return 'datetime_date_array_type'
    if isinstance(t, ArrayItemArrayType) and isinstance(tup__nhih, (
        StringArrayType, ArrayItemArrayType)):
        lcnjr__yea = f'ArrayItemArrayType{str(ir_utils.next_label())}'
        setattr(types, lcnjr__yea, t)
        return lcnjr__yea
    return '{}[::1]'.format(tup__nhih)


def _get_pd_dtype_str(t):
    tup__nhih = t.dtype
    if isinstance(tup__nhih, PDCategoricalDtype):
        return 'pd.CategoricalDtype({})'.format(tup__nhih.categories)
    if tup__nhih == types.NPDatetime('ns'):
        return 'str'
    if t == string_array_type:
        return 'str'
    if isinstance(t, IntegerArrayType):
        return '"{}Int{}"'.format('' if tup__nhih.signed else 'U',
            tup__nhih.bitwidth)
    if t == boolean_array:
        return 'np.bool_'
    if isinstance(t, ArrayItemArrayType) and isinstance(tup__nhih, (
        StringArrayType, ArrayItemArrayType)):
        return 'object'
    return 'np.{}'.format(tup__nhih)


compiled_funcs = []


@numba.njit
def check_nrows_skiprows_value(nrows, skiprows):
    if nrows < -1:
        raise ValueError('pd.read_csv: nrows must be integer >= 0.')
    if skiprows[0] < 0:
        raise ValueError('pd.read_csv: skiprows must be integer >= 0.')


def astype(df, typemap, parallel):
    plo__jkmwj = ''
    from collections import defaultdict
    utqz__glr = defaultdict(list)
    for nvsx__qzgn, dhiaw__pjhzt in typemap.items():
        utqz__glr[dhiaw__pjhzt].append(nvsx__qzgn)
    zglm__glq = df.columns.to_list()
    lvg__juicj = []
    for dhiaw__pjhzt, tbkxj__rwtw in utqz__glr.items():
        try:
            lvg__juicj.append(df.loc[:, tbkxj__rwtw].astype(dhiaw__pjhzt,
                copy=False))
            df = df.drop(tbkxj__rwtw, axis=1)
        except (ValueError, TypeError) as ypzsz__jvfl:
            plo__jkmwj = (
                f"Caught the runtime error '{ypzsz__jvfl}' on columns {tbkxj__rwtw}. Consider setting the 'dtype' argument in 'read_csv' or investigate if the data is corrupted."
                )
            break
    drrp__hgfp = bool(plo__jkmwj)
    if parallel:
        ejfsf__ext = MPI.COMM_WORLD
        drrp__hgfp = ejfsf__ext.allreduce(drrp__hgfp, op=MPI.LOR)
    if drrp__hgfp:
        czox__opwa = 'pd.read_csv(): Bodo could not infer dtypes correctly.'
        if plo__jkmwj:
            raise TypeError(f'{czox__opwa}\n{plo__jkmwj}')
        else:
            raise TypeError(
                f'{czox__opwa}\nPlease refer to errors on other ranks.')
    df = pd.concat(lvg__juicj + [df], axis=1)
    omuhw__xksqg = df.loc[:, zglm__glq]
    return omuhw__xksqg


def _gen_csv_file_reader_init(parallel, header, compression, chunksize,
    is_skiprows_list, pd_low_memory, storage_options):
    cnsf__oxzvc = header == 0
    if compression is None:
        compression = 'uncompressed'
    if is_skiprows_list:
        esbu__elul = '  skiprows = sorted(set(skiprows))\n'
    else:
        esbu__elul = '  skiprows = [skiprows]\n'
    esbu__elul += '  skiprows_list_len = len(skiprows)\n'
    esbu__elul += '  check_nrows_skiprows_value(nrows, skiprows)\n'
    esbu__elul += '  check_java_installation(fname)\n'
    esbu__elul += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    esbu__elul += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    esbu__elul += (
        '  f_reader = bodo.ir.csv_ext.csv_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    esbu__elul += (
        """    {}, bodo.utils.conversion.coerce_to_ndarray(skiprows, scalar_to_arr_len=1).ctypes, nrows, {}, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py, {}, {}, skiprows_list_len, {})
"""
        .format(parallel, cnsf__oxzvc, compression, chunksize,
        is_skiprows_list, pd_low_memory))
    esbu__elul += '  bodo.utils.utils.check_and_propagate_cpp_exception()\n'
    esbu__elul += '  if bodo.utils.utils.is_null_pointer(f_reader):\n'
    esbu__elul += "      raise FileNotFoundError('File does not exist')\n"
    return esbu__elul


def _gen_read_csv_objmode(col_names, sanitized_cnames, col_typs, usecols,
    type_usecol_offset, sep, escapechar, storage_options, call_id, glbs,
    parallel, check_parallel_runtime, idx_col_index, idx_col_typ):
    mayd__qyzme = [str(padrb__awb) for padrb__awb, ynzw__kjf in enumerate(
        usecols) if col_typs[type_usecol_offset[padrb__awb]].dtype == types
        .NPDatetime('ns')]
    if idx_col_typ == types.NPDatetime('ns'):
        assert not idx_col_index is None
        mayd__qyzme.append(str(idx_col_index))
    trj__eopj = ', '.join(mayd__qyzme)
    jyjq__heabl = _gen_parallel_flag_name(sanitized_cnames)
    lyy__dok = f"{jyjq__heabl}='bool_'" if check_parallel_runtime else ''
    uljl__sww = [_get_pd_dtype_str(col_typs[type_usecol_offset[padrb__awb]]
        ) for padrb__awb in range(len(usecols))]
    rve__klmul = None if idx_col_index is None else _get_pd_dtype_str(
        idx_col_typ)
    iuhnu__btrm = [ynzw__kjf for padrb__awb, ynzw__kjf in enumerate(usecols
        ) if uljl__sww[padrb__awb] == 'str']
    if idx_col_index is not None and rve__klmul == 'str':
        iuhnu__btrm.append(idx_col_index)
    lyi__jwwo = np.array(iuhnu__btrm, dtype=np.int64)
    glbs[f'str_col_nums_{call_id}'] = lyi__jwwo
    esbu__elul = f'  str_col_nums_{call_id}_2 = str_col_nums_{call_id}\n'
    hkyeg__tdrx = np.array(usecols + ([idx_col_index] if idx_col_index is not
        None else []), dtype=np.int64)
    glbs[f'usecols_arr_{call_id}'] = hkyeg__tdrx
    esbu__elul += f'  usecols_arr_{call_id}_2 = usecols_arr_{call_id}\n'
    wzh__rzafb = np.array(type_usecol_offset, dtype=np.int64)
    if usecols:
        glbs[f'type_usecols_offsets_arr_{call_id}'] = wzh__rzafb
        esbu__elul += f"""  type_usecols_offsets_arr_{call_id}_2 = type_usecols_offsets_arr_{call_id}
"""
    ztrzl__dhc = defaultdict(list)
    for padrb__awb, ynzw__kjf in enumerate(usecols):
        if uljl__sww[padrb__awb] == 'str':
            continue
        ztrzl__dhc[uljl__sww[padrb__awb]].append(ynzw__kjf)
    if idx_col_index is not None and rve__klmul != 'str':
        ztrzl__dhc[rve__klmul].append(idx_col_index)
    for padrb__awb, qripa__eidpr in enumerate(ztrzl__dhc.values()):
        glbs[f't_arr_{padrb__awb}_{call_id}'] = np.asarray(qripa__eidpr)
        esbu__elul += (
            f'  t_arr_{padrb__awb}_{call_id}_2 = t_arr_{padrb__awb}_{call_id}\n'
            )
    if idx_col_index != None:
        esbu__elul += f"""  with objmode(T=table_type_{call_id}, idx_arr=idx_array_typ, {lyy__dok}):
"""
    else:
        esbu__elul += f'  with objmode(T=table_type_{call_id}, {lyy__dok}):\n'
    esbu__elul += f'    typemap = {{}}\n'
    for padrb__awb, ldld__osnv in enumerate(ztrzl__dhc.keys()):
        esbu__elul += f"""    typemap.update({{i:{ldld__osnv} for i in t_arr_{padrb__awb}_{call_id}_2}})
"""
    esbu__elul += '    if f_reader.get_chunk_size() == 0:\n'
    esbu__elul += (
        f'      df = pd.DataFrame(columns=usecols_arr_{call_id}_2, dtype=str)\n'
        )
    esbu__elul += '    else:\n'
    esbu__elul += '      df = pd.read_csv(f_reader,\n'
    esbu__elul += '        header=None,\n'
    esbu__elul += '        parse_dates=[{}],\n'.format(trj__eopj)
    esbu__elul += (
        f'        dtype={{i:str for i in str_col_nums_{call_id}_2}},\n')
    esbu__elul += f"""        usecols=usecols_arr_{call_id}_2, sep={sep!r}, low_memory=False, escapechar={escapechar!r})
"""
    if check_parallel_runtime:
        esbu__elul += f'    {jyjq__heabl} = f_reader.is_parallel()\n'
    else:
        esbu__elul += f'    {jyjq__heabl} = {parallel}\n'
    esbu__elul += f'    df = astype(df, typemap, {jyjq__heabl})\n'
    if idx_col_index != None:
        hwbai__xpjou = sorted(hkyeg__tdrx).index(idx_col_index)
        esbu__elul += f'    idx_arr = df.iloc[:, {hwbai__xpjou}].values\n'
        esbu__elul += (
            f'    df.drop(columns=df.columns[{hwbai__xpjou}], inplace=True)\n')
    if len(usecols) == 0:
        esbu__elul += f'    T = None\n'
    else:
        esbu__elul += f'    arrs = []\n'
        esbu__elul += f'    for i in range(df.shape[1]):\n'
        esbu__elul += f'      arrs.append(df.iloc[:, i].values)\n'
        esbu__elul += f"""    T = Table(arrs, type_usecols_offsets_arr_{call_id}_2, {len(col_names)})
"""
    return esbu__elul


def _gen_parallel_flag_name(sanitized_cnames):
    jyjq__heabl = '_parallel_value'
    while jyjq__heabl in sanitized_cnames:
        jyjq__heabl = '_' + jyjq__heabl
    return jyjq__heabl


def _gen_csv_reader_py(col_names, col_typs, usecols, type_usecol_offset,
    sep, parallel, header, compression, is_skiprows_list, pd_low_memory,
    escapechar, storage_options, idx_col_index=None, idx_col_typ=types.none):
    sanitized_cnames = [sanitize_varname(ohl__pxmrf) for ohl__pxmrf in
        col_names]
    esbu__elul = 'def csv_reader_py(fname, nrows, skiprows):\n'
    esbu__elul += _gen_csv_file_reader_init(parallel, header, compression, 
        -1, is_skiprows_list, pd_low_memory, storage_options)
    call_id = ir_utils.next_label()
    lps__apd = globals()
    if idx_col_typ != types.none:
        lps__apd[f'idx_array_typ'] = idx_col_typ
    if len(usecols) == 0:
        lps__apd[f'table_type_{call_id}'] = types.none
    else:
        lps__apd[f'table_type_{call_id}'] = TableType(tuple(col_typs))
    esbu__elul += _gen_read_csv_objmode(col_names, sanitized_cnames,
        col_typs, usecols, type_usecol_offset, sep, escapechar,
        storage_options, call_id, lps__apd, parallel=parallel,
        check_parallel_runtime=False, idx_col_index=idx_col_index,
        idx_col_typ=idx_col_typ)
    if idx_col_index != None:
        esbu__elul += '  return (T, idx_arr)\n'
    else:
        esbu__elul += '  return (T, None)\n'
    qxy__ertj = {}
    lps__apd['get_storage_options_pyobject'] = get_storage_options_pyobject
    exec(esbu__elul, lps__apd, qxy__ertj)
    ajvk__fega = qxy__ertj['csv_reader_py']
    hehv__dycd = numba.njit(ajvk__fega)
    compiled_funcs.append(hehv__dycd)
    return hehv__dycd
