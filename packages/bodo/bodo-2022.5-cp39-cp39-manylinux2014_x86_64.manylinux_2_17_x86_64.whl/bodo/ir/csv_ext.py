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
    eowjx__awpm = typemap[node.file_name.name]
    if types.unliteral(eowjx__awpm) != types.unicode_type:
        raise BodoError(
            f"pd.read_csv(): 'filepath_or_buffer' must be a string. Found type: {eowjx__awpm}."
            , node.file_name.loc)
    if not isinstance(node.skiprows, ir.Const):
        nae__dvdjx = typemap[node.skiprows.name]
        if isinstance(nae__dvdjx, types.Dispatcher):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' callable not supported yet.",
                node.file_name.loc)
        elif not isinstance(nae__dvdjx, types.Integer) and not (isinstance(
            nae__dvdjx, (types.List, types.Tuple)) and isinstance(
            nae__dvdjx.dtype, types.Integer)) and not isinstance(nae__dvdjx,
            (types.LiteralList, bodo.utils.typing.ListLiteral)):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' must be an integer or list of integers. Found type {nae__dvdjx}."
                , loc=node.skiprows.loc)
        elif isinstance(nae__dvdjx, (types.List, types.Tuple)):
            node.is_skiprows_list = True
    if not isinstance(node.nrows, ir.Const):
        snh__tihwz = typemap[node.nrows.name]
        if not isinstance(snh__tihwz, types.Integer):
            raise BodoError(
                f"pd.read_csv(): 'nrows' must be an integer. Found type {snh__tihwz}."
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
        jrjka__phza = csv_node.out_vars[0]
        if jrjka__phza.name not in lives:
            return None
    else:
        gaue__zseyi = csv_node.out_vars[0]
        zzx__jzb = csv_node.out_vars[1]
        if gaue__zseyi.name not in lives and zzx__jzb.name not in lives:
            return None
        elif zzx__jzb.name not in lives:
            csv_node.index_column_index = None
            csv_node.index_column_typ = types.none
        elif gaue__zseyi.name not in lives:
            csv_node.usecols = []
            csv_node.out_types = []
            csv_node.type_usecol_offset = []
    return csv_node


def csv_distributed_run(csv_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    nae__dvdjx = types.int64 if isinstance(csv_node.skiprows, ir.Const
        ) else types.unliteral(typemap[csv_node.skiprows.name])
    if csv_node.chunksize is not None:
        parallel = False
        if bodo.user_logging.get_verbose_level() >= 1:
            eibd__zzi = (
                'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n'
                )
            brc__spsi = csv_node.loc.strformat()
            rzz__qqmz = csv_node.df_colnames
            bodo.user_logging.log_message('Column Pruning', eibd__zzi,
                brc__spsi, rzz__qqmz)
            azzim__vjwh = csv_node.out_types[0].yield_type.data
            zxcby__njz = [ouvp__kzg for bkbs__mcmk, ouvp__kzg in enumerate(
                csv_node.df_colnames) if isinstance(azzim__vjwh[bkbs__mcmk],
                bodo.libs.dict_arr_ext.DictionaryArrayType)]
            if zxcby__njz:
                bprcz__gms = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
                bodo.user_logging.log_message('Dictionary Encoding',
                    bprcz__gms, brc__spsi, zxcby__njz)
        if array_dists is not None:
            stje__ghno = csv_node.out_vars[0].name
            parallel = array_dists[stje__ghno] in (distributed_pass.
                Distribution.OneD, distributed_pass.Distribution.OneD_Var)
        qakeo__vdps = 'def csv_iterator_impl(fname, nrows, skiprows):\n'
        qakeo__vdps += (
            f'    reader = _csv_reader_init(fname, nrows, skiprows)\n')
        qakeo__vdps += (
            f'    iterator = init_csv_iterator(reader, csv_iterator_type)\n')
        afx__udr = {}
        from bodo.io.csv_iterator_ext import init_csv_iterator
        exec(qakeo__vdps, {}, afx__udr)
        jqhq__lmecq = afx__udr['csv_iterator_impl']
        teuxa__dsz = 'def csv_reader_init(fname, nrows, skiprows):\n'
        teuxa__dsz += _gen_csv_file_reader_init(parallel, csv_node.header,
            csv_node.compression, csv_node.chunksize, csv_node.
            is_skiprows_list, csv_node.pd_low_memory, csv_node.storage_options)
        teuxa__dsz += '  return f_reader\n'
        exec(teuxa__dsz, globals(), afx__udr)
        zzt__zqv = afx__udr['csv_reader_init']
        rkpk__qwxuw = numba.njit(zzt__zqv)
        compiled_funcs.append(rkpk__qwxuw)
        qie__tkcjk = compile_to_numba_ir(jqhq__lmecq, {'_csv_reader_init':
            rkpk__qwxuw, 'init_csv_iterator': init_csv_iterator,
            'csv_iterator_type': typemap[csv_node.out_vars[0].name]},
            typingctx=typingctx, targetctx=targetctx, arg_typs=(string_type,
            types.int64, nae__dvdjx), typemap=typemap, calltypes=calltypes
            ).blocks.popitem()[1]
        replace_arg_nodes(qie__tkcjk, [csv_node.file_name, csv_node.nrows,
            csv_node.skiprows])
        ika__nvdws = qie__tkcjk.body[:-3]
        ika__nvdws[-1].target = csv_node.out_vars[0]
        return ika__nvdws
    parallel = bodo.ir.connector.is_connector_table_parallel(csv_node,
        array_dists, typemap, 'CSVReader')
    qakeo__vdps = 'def csv_impl(fname, nrows, skiprows):\n'
    qakeo__vdps += (
        f'    (table_val, idx_col) = _csv_reader_py(fname, nrows, skiprows)\n')
    afx__udr = {}
    exec(qakeo__vdps, {}, afx__udr)
    ccg__kmzv = afx__udr['csv_impl']
    fatw__gswwq = csv_node.usecols
    if fatw__gswwq:
        fatw__gswwq = [csv_node.usecols[bkbs__mcmk] for bkbs__mcmk in
            csv_node.type_usecol_offset]
    if bodo.user_logging.get_verbose_level() >= 1:
        eibd__zzi = (
            'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n')
        brc__spsi = csv_node.loc.strformat()
        rzz__qqmz = []
        zxcby__njz = []
        if fatw__gswwq:
            for bkbs__mcmk in fatw__gswwq:
                ums__rnx = csv_node.df_colnames[bkbs__mcmk]
                rzz__qqmz.append(ums__rnx)
                if isinstance(csv_node.out_types[bkbs__mcmk], bodo.libs.
                    dict_arr_ext.DictionaryArrayType):
                    zxcby__njz.append(ums__rnx)
        bodo.user_logging.log_message('Column Pruning', eibd__zzi,
            brc__spsi, rzz__qqmz)
        if zxcby__njz:
            bprcz__gms = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', bprcz__gms,
                brc__spsi, zxcby__njz)
    yaki__eta = _gen_csv_reader_py(csv_node.df_colnames, csv_node.out_types,
        fatw__gswwq, csv_node.type_usecol_offset, csv_node.sep, parallel,
        csv_node.header, csv_node.compression, csv_node.is_skiprows_list,
        csv_node.pd_low_memory, csv_node.escapechar, csv_node.
        storage_options, idx_col_index=csv_node.index_column_index,
        idx_col_typ=csv_node.index_column_typ)
    qie__tkcjk = compile_to_numba_ir(ccg__kmzv, {'_csv_reader_py':
        yaki__eta}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type, types.int64, nae__dvdjx), typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(qie__tkcjk, [csv_node.file_name, csv_node.nrows,
        csv_node.skiprows, csv_node.is_skiprows_list])
    ika__nvdws = qie__tkcjk.body[:-3]
    ika__nvdws[-1].target = csv_node.out_vars[1]
    ika__nvdws[-2].target = csv_node.out_vars[0]
    assert not (csv_node.index_column_index is None and not fatw__gswwq
        ), 'At most one of table and index should be dead if the CSV IR node is live'
    if csv_node.index_column_index is None:
        ika__nvdws.pop(-1)
    elif not fatw__gswwq:
        ika__nvdws.pop(-2)
    return ika__nvdws


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
    joxuu__mhn = t.dtype
    if isinstance(joxuu__mhn, PDCategoricalDtype):
        cvi__cqpi = CategoricalArrayType(joxuu__mhn)
        vchp__nez = 'CategoricalArrayType' + str(ir_utils.next_label())
        setattr(types, vchp__nez, cvi__cqpi)
        return vchp__nez
    if joxuu__mhn == types.NPDatetime('ns'):
        joxuu__mhn = 'NPDatetime("ns")'
    if t == string_array_type:
        types.string_array_type = string_array_type
        return 'string_array_type'
    if isinstance(t, IntegerArrayType):
        bdwgd__yfiqc = 'int_arr_{}'.format(joxuu__mhn)
        setattr(types, bdwgd__yfiqc, t)
        return bdwgd__yfiqc
    if t == boolean_array:
        types.boolean_array = boolean_array
        return 'boolean_array'
    if joxuu__mhn == types.bool_:
        joxuu__mhn = 'bool_'
    if joxuu__mhn == datetime_date_type:
        return 'datetime_date_array_type'
    if isinstance(t, ArrayItemArrayType) and isinstance(joxuu__mhn, (
        StringArrayType, ArrayItemArrayType)):
        ffkx__phuy = f'ArrayItemArrayType{str(ir_utils.next_label())}'
        setattr(types, ffkx__phuy, t)
        return ffkx__phuy
    return '{}[::1]'.format(joxuu__mhn)


def _get_pd_dtype_str(t):
    joxuu__mhn = t.dtype
    if isinstance(joxuu__mhn, PDCategoricalDtype):
        return 'pd.CategoricalDtype({})'.format(joxuu__mhn.categories)
    if joxuu__mhn == types.NPDatetime('ns'):
        return 'str'
    if t == string_array_type:
        return 'str'
    if isinstance(t, IntegerArrayType):
        return '"{}Int{}"'.format('' if joxuu__mhn.signed else 'U',
            joxuu__mhn.bitwidth)
    if t == boolean_array:
        return 'np.bool_'
    if isinstance(t, ArrayItemArrayType) and isinstance(joxuu__mhn, (
        StringArrayType, ArrayItemArrayType)):
        return 'object'
    return 'np.{}'.format(joxuu__mhn)


compiled_funcs = []


@numba.njit
def check_nrows_skiprows_value(nrows, skiprows):
    if nrows < -1:
        raise ValueError('pd.read_csv: nrows must be integer >= 0.')
    if skiprows[0] < 0:
        raise ValueError('pd.read_csv: skiprows must be integer >= 0.')


def astype(df, typemap, parallel):
    onj__gkz = ''
    from collections import defaultdict
    sae__fptsr = defaultdict(list)
    for wpasz__fhvjc, tux__ystb in typemap.items():
        sae__fptsr[tux__ystb].append(wpasz__fhvjc)
    soiq__gkfe = df.columns.to_list()
    nfba__ekr = []
    for tux__ystb, yuyp__geyyf in sae__fptsr.items():
        try:
            nfba__ekr.append(df.loc[:, yuyp__geyyf].astype(tux__ystb, copy=
                False))
            df = df.drop(yuyp__geyyf, axis=1)
        except (ValueError, TypeError) as tsz__tmh:
            onj__gkz = (
                f"Caught the runtime error '{tsz__tmh}' on columns {yuyp__geyyf}. Consider setting the 'dtype' argument in 'read_csv' or investigate if the data is corrupted."
                )
            break
    yxjs__vugo = bool(onj__gkz)
    if parallel:
        sbun__zax = MPI.COMM_WORLD
        yxjs__vugo = sbun__zax.allreduce(yxjs__vugo, op=MPI.LOR)
    if yxjs__vugo:
        yoxt__vpfzg = 'pd.read_csv(): Bodo could not infer dtypes correctly.'
        if onj__gkz:
            raise TypeError(f'{yoxt__vpfzg}\n{onj__gkz}')
        else:
            raise TypeError(
                f'{yoxt__vpfzg}\nPlease refer to errors on other ranks.')
    df = pd.concat(nfba__ekr + [df], axis=1)
    zldao__mfs = df.loc[:, soiq__gkfe]
    return zldao__mfs


def _gen_csv_file_reader_init(parallel, header, compression, chunksize,
    is_skiprows_list, pd_low_memory, storage_options):
    ffpj__anfc = header == 0
    if compression is None:
        compression = 'uncompressed'
    if is_skiprows_list:
        qakeo__vdps = '  skiprows = sorted(set(skiprows))\n'
    else:
        qakeo__vdps = '  skiprows = [skiprows]\n'
    qakeo__vdps += '  skiprows_list_len = len(skiprows)\n'
    qakeo__vdps += '  check_nrows_skiprows_value(nrows, skiprows)\n'
    qakeo__vdps += '  check_java_installation(fname)\n'
    qakeo__vdps += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    qakeo__vdps += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    qakeo__vdps += (
        '  f_reader = bodo.ir.csv_ext.csv_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    qakeo__vdps += (
        """    {}, bodo.utils.conversion.coerce_to_ndarray(skiprows, scalar_to_arr_len=1).ctypes, nrows, {}, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py, {}, {}, skiprows_list_len, {})
"""
        .format(parallel, ffpj__anfc, compression, chunksize,
        is_skiprows_list, pd_low_memory))
    qakeo__vdps += '  bodo.utils.utils.check_and_propagate_cpp_exception()\n'
    qakeo__vdps += '  if bodo.utils.utils.is_null_pointer(f_reader):\n'
    qakeo__vdps += "      raise FileNotFoundError('File does not exist')\n"
    return qakeo__vdps


def _gen_read_csv_objmode(col_names, sanitized_cnames, col_typs, usecols,
    type_usecol_offset, sep, escapechar, storage_options, call_id, glbs,
    parallel, check_parallel_runtime, idx_col_index, idx_col_typ):
    ibs__mvj = [str(bkbs__mcmk) for bkbs__mcmk, zqs__juutq in enumerate(
        usecols) if col_typs[type_usecol_offset[bkbs__mcmk]].dtype == types
        .NPDatetime('ns')]
    if idx_col_typ == types.NPDatetime('ns'):
        assert not idx_col_index is None
        ibs__mvj.append(str(idx_col_index))
    gbnmw__vva = ', '.join(ibs__mvj)
    evvlo__mpgpv = _gen_parallel_flag_name(sanitized_cnames)
    nrqve__pdgam = f"{evvlo__mpgpv}='bool_'" if check_parallel_runtime else ''
    nba__cvumc = [_get_pd_dtype_str(col_typs[type_usecol_offset[bkbs__mcmk]
        ]) for bkbs__mcmk in range(len(usecols))]
    rlzfx__qxx = None if idx_col_index is None else _get_pd_dtype_str(
        idx_col_typ)
    ypadt__qvgud = [zqs__juutq for bkbs__mcmk, zqs__juutq in enumerate(
        usecols) if nba__cvumc[bkbs__mcmk] == 'str']
    if idx_col_index is not None and rlzfx__qxx == 'str':
        ypadt__qvgud.append(idx_col_index)
    ovhup__ilw = np.array(ypadt__qvgud, dtype=np.int64)
    glbs[f'str_col_nums_{call_id}'] = ovhup__ilw
    qakeo__vdps = f'  str_col_nums_{call_id}_2 = str_col_nums_{call_id}\n'
    wybx__dverj = np.array(usecols + ([idx_col_index] if idx_col_index is not
        None else []), dtype=np.int64)
    glbs[f'usecols_arr_{call_id}'] = wybx__dverj
    qakeo__vdps += f'  usecols_arr_{call_id}_2 = usecols_arr_{call_id}\n'
    nsjv__oeeyz = np.array(type_usecol_offset, dtype=np.int64)
    if usecols:
        glbs[f'type_usecols_offsets_arr_{call_id}'] = nsjv__oeeyz
        qakeo__vdps += f"""  type_usecols_offsets_arr_{call_id}_2 = type_usecols_offsets_arr_{call_id}
"""
    svdjy__naobu = defaultdict(list)
    for bkbs__mcmk, zqs__juutq in enumerate(usecols):
        if nba__cvumc[bkbs__mcmk] == 'str':
            continue
        svdjy__naobu[nba__cvumc[bkbs__mcmk]].append(zqs__juutq)
    if idx_col_index is not None and rlzfx__qxx != 'str':
        svdjy__naobu[rlzfx__qxx].append(idx_col_index)
    for bkbs__mcmk, zprr__ezqdm in enumerate(svdjy__naobu.values()):
        glbs[f't_arr_{bkbs__mcmk}_{call_id}'] = np.asarray(zprr__ezqdm)
        qakeo__vdps += (
            f'  t_arr_{bkbs__mcmk}_{call_id}_2 = t_arr_{bkbs__mcmk}_{call_id}\n'
            )
    if idx_col_index != None:
        qakeo__vdps += f"""  with objmode(T=table_type_{call_id}, idx_arr=idx_array_typ, {nrqve__pdgam}):
"""
    else:
        qakeo__vdps += (
            f'  with objmode(T=table_type_{call_id}, {nrqve__pdgam}):\n')
    qakeo__vdps += f'    typemap = {{}}\n'
    for bkbs__mcmk, atdnt__edzs in enumerate(svdjy__naobu.keys()):
        qakeo__vdps += f"""    typemap.update({{i:{atdnt__edzs} for i in t_arr_{bkbs__mcmk}_{call_id}_2}})
"""
    qakeo__vdps += '    if f_reader.get_chunk_size() == 0:\n'
    qakeo__vdps += (
        f'      df = pd.DataFrame(columns=usecols_arr_{call_id}_2, dtype=str)\n'
        )
    qakeo__vdps += '    else:\n'
    qakeo__vdps += '      df = pd.read_csv(f_reader,\n'
    qakeo__vdps += '        header=None,\n'
    qakeo__vdps += '        parse_dates=[{}],\n'.format(gbnmw__vva)
    qakeo__vdps += (
        f'        dtype={{i:str for i in str_col_nums_{call_id}_2}},\n')
    qakeo__vdps += f"""        usecols=usecols_arr_{call_id}_2, sep={sep!r}, low_memory=False, escapechar={escapechar!r})
"""
    if check_parallel_runtime:
        qakeo__vdps += f'    {evvlo__mpgpv} = f_reader.is_parallel()\n'
    else:
        qakeo__vdps += f'    {evvlo__mpgpv} = {parallel}\n'
    qakeo__vdps += f'    df = astype(df, typemap, {evvlo__mpgpv})\n'
    if idx_col_index != None:
        gdwnv__eygtx = sorted(wybx__dverj).index(idx_col_index)
        qakeo__vdps += f'    idx_arr = df.iloc[:, {gdwnv__eygtx}].values\n'
        qakeo__vdps += (
            f'    df.drop(columns=df.columns[{gdwnv__eygtx}], inplace=True)\n')
    if len(usecols) == 0:
        qakeo__vdps += f'    T = None\n'
    else:
        qakeo__vdps += f'    arrs = []\n'
        qakeo__vdps += f'    for i in range(df.shape[1]):\n'
        qakeo__vdps += f'      arrs.append(df.iloc[:, i].values)\n'
        qakeo__vdps += f"""    T = Table(arrs, type_usecols_offsets_arr_{call_id}_2, {len(col_names)})
"""
    return qakeo__vdps


def _gen_parallel_flag_name(sanitized_cnames):
    evvlo__mpgpv = '_parallel_value'
    while evvlo__mpgpv in sanitized_cnames:
        evvlo__mpgpv = '_' + evvlo__mpgpv
    return evvlo__mpgpv


def _gen_csv_reader_py(col_names, col_typs, usecols, type_usecol_offset,
    sep, parallel, header, compression, is_skiprows_list, pd_low_memory,
    escapechar, storage_options, idx_col_index=None, idx_col_typ=types.none):
    sanitized_cnames = [sanitize_varname(ouvp__kzg) for ouvp__kzg in col_names]
    qakeo__vdps = 'def csv_reader_py(fname, nrows, skiprows):\n'
    qakeo__vdps += _gen_csv_file_reader_init(parallel, header, compression,
        -1, is_skiprows_list, pd_low_memory, storage_options)
    call_id = ir_utils.next_label()
    mgd__mab = globals()
    if idx_col_typ != types.none:
        mgd__mab[f'idx_array_typ'] = idx_col_typ
    if len(usecols) == 0:
        mgd__mab[f'table_type_{call_id}'] = types.none
    else:
        mgd__mab[f'table_type_{call_id}'] = TableType(tuple(col_typs))
    qakeo__vdps += _gen_read_csv_objmode(col_names, sanitized_cnames,
        col_typs, usecols, type_usecol_offset, sep, escapechar,
        storage_options, call_id, mgd__mab, parallel=parallel,
        check_parallel_runtime=False, idx_col_index=idx_col_index,
        idx_col_typ=idx_col_typ)
    if idx_col_index != None:
        qakeo__vdps += '  return (T, idx_arr)\n'
    else:
        qakeo__vdps += '  return (T, None)\n'
    afx__udr = {}
    mgd__mab['get_storage_options_pyobject'] = get_storage_options_pyobject
    exec(qakeo__vdps, mgd__mab, afx__udr)
    yaki__eta = afx__udr['csv_reader_py']
    rkpk__qwxuw = numba.njit(yaki__eta)
    compiled_funcs.append(rkpk__qwxuw)
    return rkpk__qwxuw
