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
    vbil__uqut = typemap[node.file_name.name]
    if types.unliteral(vbil__uqut) != types.unicode_type:
        raise BodoError(
            f"pd.read_csv(): 'filepath_or_buffer' must be a string. Found type: {vbil__uqut}."
            , node.file_name.loc)
    if not isinstance(node.skiprows, ir.Const):
        egy__nib = typemap[node.skiprows.name]
        if isinstance(egy__nib, types.Dispatcher):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' callable not supported yet.",
                node.file_name.loc)
        elif not isinstance(egy__nib, types.Integer) and not (isinstance(
            egy__nib, (types.List, types.Tuple)) and isinstance(egy__nib.
            dtype, types.Integer)) and not isinstance(egy__nib, (types.
            LiteralList, bodo.utils.typing.ListLiteral)):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' must be an integer or list of integers. Found type {egy__nib}."
                , loc=node.skiprows.loc)
        elif isinstance(egy__nib, (types.List, types.Tuple)):
            node.is_skiprows_list = True
    if not isinstance(node.nrows, ir.Const):
        lqx__vznh = typemap[node.nrows.name]
        if not isinstance(lqx__vznh, types.Integer):
            raise BodoError(
                f"pd.read_csv(): 'nrows' must be an integer. Found type {lqx__vznh}."
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
        rmwz__xgn = csv_node.out_vars[0]
        if rmwz__xgn.name not in lives:
            return None
    else:
        prcp__lav = csv_node.out_vars[0]
        jbzmr__wtsiz = csv_node.out_vars[1]
        if prcp__lav.name not in lives and jbzmr__wtsiz.name not in lives:
            return None
        elif jbzmr__wtsiz.name not in lives:
            csv_node.index_column_index = None
            csv_node.index_column_typ = types.none
        elif prcp__lav.name not in lives:
            csv_node.usecols = []
            csv_node.out_types = []
            csv_node.type_usecol_offset = []
    return csv_node


def csv_distributed_run(csv_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    egy__nib = types.int64 if isinstance(csv_node.skiprows, ir.Const
        ) else types.unliteral(typemap[csv_node.skiprows.name])
    if csv_node.chunksize is not None:
        parallel = False
        if bodo.user_logging.get_verbose_level() >= 1:
            joawg__edrzc = (
                'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n'
                )
            tcwh__rqz = csv_node.loc.strformat()
            srrlr__khr = csv_node.df_colnames
            bodo.user_logging.log_message('Column Pruning', joawg__edrzc,
                tcwh__rqz, srrlr__khr)
            fhuyj__cor = csv_node.out_types[0].yield_type.data
            rvxi__aeg = [qhijr__myrgm for pqbmm__euy, qhijr__myrgm in
                enumerate(csv_node.df_colnames) if isinstance(fhuyj__cor[
                pqbmm__euy], bodo.libs.dict_arr_ext.DictionaryArrayType)]
            if rvxi__aeg:
                plm__mkc = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
                bodo.user_logging.log_message('Dictionary Encoding',
                    plm__mkc, tcwh__rqz, rvxi__aeg)
        if array_dists is not None:
            rpj__uhfi = csv_node.out_vars[0].name
            parallel = array_dists[rpj__uhfi] in (distributed_pass.
                Distribution.OneD, distributed_pass.Distribution.OneD_Var)
        jbyfw__eyn = 'def csv_iterator_impl(fname, nrows, skiprows):\n'
        jbyfw__eyn += (
            f'    reader = _csv_reader_init(fname, nrows, skiprows)\n')
        jbyfw__eyn += (
            f'    iterator = init_csv_iterator(reader, csv_iterator_type)\n')
        weczx__tkhgr = {}
        from bodo.io.csv_iterator_ext import init_csv_iterator
        exec(jbyfw__eyn, {}, weczx__tkhgr)
        ujb__bru = weczx__tkhgr['csv_iterator_impl']
        uvdn__zzcw = 'def csv_reader_init(fname, nrows, skiprows):\n'
        uvdn__zzcw += _gen_csv_file_reader_init(parallel, csv_node.header,
            csv_node.compression, csv_node.chunksize, csv_node.
            is_skiprows_list, csv_node.pd_low_memory, csv_node.storage_options)
        uvdn__zzcw += '  return f_reader\n'
        exec(uvdn__zzcw, globals(), weczx__tkhgr)
        oiqnc__eafd = weczx__tkhgr['csv_reader_init']
        tvlj__lpze = numba.njit(oiqnc__eafd)
        compiled_funcs.append(tvlj__lpze)
        jgn__hbmkl = compile_to_numba_ir(ujb__bru, {'_csv_reader_init':
            tvlj__lpze, 'init_csv_iterator': init_csv_iterator,
            'csv_iterator_type': typemap[csv_node.out_vars[0].name]},
            typingctx=typingctx, targetctx=targetctx, arg_typs=(string_type,
            types.int64, egy__nib), typemap=typemap, calltypes=calltypes
            ).blocks.popitem()[1]
        replace_arg_nodes(jgn__hbmkl, [csv_node.file_name, csv_node.nrows,
            csv_node.skiprows])
        tsn__rbxaf = jgn__hbmkl.body[:-3]
        tsn__rbxaf[-1].target = csv_node.out_vars[0]
        return tsn__rbxaf
    parallel = bodo.ir.connector.is_connector_table_parallel(csv_node,
        array_dists, typemap, 'CSVReader')
    jbyfw__eyn = 'def csv_impl(fname, nrows, skiprows):\n'
    jbyfw__eyn += (
        f'    (table_val, idx_col) = _csv_reader_py(fname, nrows, skiprows)\n')
    weczx__tkhgr = {}
    exec(jbyfw__eyn, {}, weczx__tkhgr)
    mxz__uxgvc = weczx__tkhgr['csv_impl']
    upzg__tlt = csv_node.usecols
    if upzg__tlt:
        upzg__tlt = [csv_node.usecols[pqbmm__euy] for pqbmm__euy in
            csv_node.type_usecol_offset]
    if bodo.user_logging.get_verbose_level() >= 1:
        joawg__edrzc = (
            'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n')
        tcwh__rqz = csv_node.loc.strformat()
        srrlr__khr = []
        rvxi__aeg = []
        if upzg__tlt:
            for pqbmm__euy in upzg__tlt:
                giaw__gvegv = csv_node.df_colnames[pqbmm__euy]
                srrlr__khr.append(giaw__gvegv)
                if isinstance(csv_node.out_types[pqbmm__euy], bodo.libs.
                    dict_arr_ext.DictionaryArrayType):
                    rvxi__aeg.append(giaw__gvegv)
        bodo.user_logging.log_message('Column Pruning', joawg__edrzc,
            tcwh__rqz, srrlr__khr)
        if rvxi__aeg:
            plm__mkc = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', plm__mkc,
                tcwh__rqz, rvxi__aeg)
    opw__ustaf = _gen_csv_reader_py(csv_node.df_colnames, csv_node.
        out_types, upzg__tlt, csv_node.type_usecol_offset, csv_node.sep,
        parallel, csv_node.header, csv_node.compression, csv_node.
        is_skiprows_list, csv_node.pd_low_memory, csv_node.escapechar,
        csv_node.storage_options, idx_col_index=csv_node.index_column_index,
        idx_col_typ=csv_node.index_column_typ)
    jgn__hbmkl = compile_to_numba_ir(mxz__uxgvc, {'_csv_reader_py':
        opw__ustaf}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type, types.int64, egy__nib), typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(jgn__hbmkl, [csv_node.file_name, csv_node.nrows,
        csv_node.skiprows, csv_node.is_skiprows_list])
    tsn__rbxaf = jgn__hbmkl.body[:-3]
    tsn__rbxaf[-1].target = csv_node.out_vars[1]
    tsn__rbxaf[-2].target = csv_node.out_vars[0]
    assert not (csv_node.index_column_index is None and not upzg__tlt
        ), 'At most one of table and index should be dead if the CSV IR node is live'
    if csv_node.index_column_index is None:
        tsn__rbxaf.pop(-1)
    elif not upzg__tlt:
        tsn__rbxaf.pop(-2)
    return tsn__rbxaf


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
    typ__qaal = t.dtype
    if isinstance(typ__qaal, PDCategoricalDtype):
        oxte__dqfpl = CategoricalArrayType(typ__qaal)
        vfg__cfpa = 'CategoricalArrayType' + str(ir_utils.next_label())
        setattr(types, vfg__cfpa, oxte__dqfpl)
        return vfg__cfpa
    if typ__qaal == types.NPDatetime('ns'):
        typ__qaal = 'NPDatetime("ns")'
    if t == string_array_type:
        types.string_array_type = string_array_type
        return 'string_array_type'
    if isinstance(t, IntegerArrayType):
        xtolr__ios = 'int_arr_{}'.format(typ__qaal)
        setattr(types, xtolr__ios, t)
        return xtolr__ios
    if t == boolean_array:
        types.boolean_array = boolean_array
        return 'boolean_array'
    if typ__qaal == types.bool_:
        typ__qaal = 'bool_'
    if typ__qaal == datetime_date_type:
        return 'datetime_date_array_type'
    if isinstance(t, ArrayItemArrayType) and isinstance(typ__qaal, (
        StringArrayType, ArrayItemArrayType)):
        opzyz__zjtp = f'ArrayItemArrayType{str(ir_utils.next_label())}'
        setattr(types, opzyz__zjtp, t)
        return opzyz__zjtp
    return '{}[::1]'.format(typ__qaal)


def _get_pd_dtype_str(t):
    typ__qaal = t.dtype
    if isinstance(typ__qaal, PDCategoricalDtype):
        return 'pd.CategoricalDtype({})'.format(typ__qaal.categories)
    if typ__qaal == types.NPDatetime('ns'):
        return 'str'
    if t == string_array_type:
        return 'str'
    if isinstance(t, IntegerArrayType):
        return '"{}Int{}"'.format('' if typ__qaal.signed else 'U',
            typ__qaal.bitwidth)
    if t == boolean_array:
        return 'np.bool_'
    if isinstance(t, ArrayItemArrayType) and isinstance(typ__qaal, (
        StringArrayType, ArrayItemArrayType)):
        return 'object'
    return 'np.{}'.format(typ__qaal)


compiled_funcs = []


@numba.njit
def check_nrows_skiprows_value(nrows, skiprows):
    if nrows < -1:
        raise ValueError('pd.read_csv: nrows must be integer >= 0.')
    if skiprows[0] < 0:
        raise ValueError('pd.read_csv: skiprows must be integer >= 0.')


def astype(df, typemap, parallel):
    mfmh__awp = ''
    from collections import defaultdict
    bnu__auc = defaultdict(list)
    for yjqn__vfe, hvdki__axhj in typemap.items():
        bnu__auc[hvdki__axhj].append(yjqn__vfe)
    sjuo__gah = df.columns.to_list()
    yqqxu__wxe = []
    for hvdki__axhj, dqj__phc in bnu__auc.items():
        try:
            yqqxu__wxe.append(df.loc[:, dqj__phc].astype(hvdki__axhj, copy=
                False))
            df = df.drop(dqj__phc, axis=1)
        except (ValueError, TypeError) as rrpnc__jyyly:
            mfmh__awp = (
                f"Caught the runtime error '{rrpnc__jyyly}' on columns {dqj__phc}. Consider setting the 'dtype' argument in 'read_csv' or investigate if the data is corrupted."
                )
            break
    heaae__csnn = bool(mfmh__awp)
    if parallel:
        qps__ivjcv = MPI.COMM_WORLD
        heaae__csnn = qps__ivjcv.allreduce(heaae__csnn, op=MPI.LOR)
    if heaae__csnn:
        jfatg__ebc = 'pd.read_csv(): Bodo could not infer dtypes correctly.'
        if mfmh__awp:
            raise TypeError(f'{jfatg__ebc}\n{mfmh__awp}')
        else:
            raise TypeError(
                f'{jfatg__ebc}\nPlease refer to errors on other ranks.')
    df = pd.concat(yqqxu__wxe + [df], axis=1)
    iqi__nzqu = df.loc[:, sjuo__gah]
    return iqi__nzqu


def _gen_csv_file_reader_init(parallel, header, compression, chunksize,
    is_skiprows_list, pd_low_memory, storage_options):
    ptj__xww = header == 0
    if compression is None:
        compression = 'uncompressed'
    if is_skiprows_list:
        jbyfw__eyn = '  skiprows = sorted(set(skiprows))\n'
    else:
        jbyfw__eyn = '  skiprows = [skiprows]\n'
    jbyfw__eyn += '  skiprows_list_len = len(skiprows)\n'
    jbyfw__eyn += '  check_nrows_skiprows_value(nrows, skiprows)\n'
    jbyfw__eyn += '  check_java_installation(fname)\n'
    jbyfw__eyn += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    jbyfw__eyn += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    jbyfw__eyn += (
        '  f_reader = bodo.ir.csv_ext.csv_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    jbyfw__eyn += (
        """    {}, bodo.utils.conversion.coerce_to_ndarray(skiprows, scalar_to_arr_len=1).ctypes, nrows, {}, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py, {}, {}, skiprows_list_len, {})
"""
        .format(parallel, ptj__xww, compression, chunksize,
        is_skiprows_list, pd_low_memory))
    jbyfw__eyn += '  bodo.utils.utils.check_and_propagate_cpp_exception()\n'
    jbyfw__eyn += '  if bodo.utils.utils.is_null_pointer(f_reader):\n'
    jbyfw__eyn += "      raise FileNotFoundError('File does not exist')\n"
    return jbyfw__eyn


def _gen_read_csv_objmode(col_names, sanitized_cnames, col_typs, usecols,
    type_usecol_offset, sep, escapechar, storage_options, call_id, glbs,
    parallel, check_parallel_runtime, idx_col_index, idx_col_typ):
    uhuqg__dzm = [str(pqbmm__euy) for pqbmm__euy, otk__fcumf in enumerate(
        usecols) if col_typs[type_usecol_offset[pqbmm__euy]].dtype == types
        .NPDatetime('ns')]
    if idx_col_typ == types.NPDatetime('ns'):
        assert not idx_col_index is None
        uhuqg__dzm.append(str(idx_col_index))
    ihfkw__fwbhx = ', '.join(uhuqg__dzm)
    ufhh__yrcfw = _gen_parallel_flag_name(sanitized_cnames)
    eeqh__hcvu = f"{ufhh__yrcfw}='bool_'" if check_parallel_runtime else ''
    fgqc__lxqwu = [_get_pd_dtype_str(col_typs[type_usecol_offset[pqbmm__euy
        ]]) for pqbmm__euy in range(len(usecols))]
    eca__jlh = None if idx_col_index is None else _get_pd_dtype_str(idx_col_typ
        )
    eshlj__imnmc = [otk__fcumf for pqbmm__euy, otk__fcumf in enumerate(
        usecols) if fgqc__lxqwu[pqbmm__euy] == 'str']
    if idx_col_index is not None and eca__jlh == 'str':
        eshlj__imnmc.append(idx_col_index)
    jtbf__qwda = np.array(eshlj__imnmc, dtype=np.int64)
    glbs[f'str_col_nums_{call_id}'] = jtbf__qwda
    jbyfw__eyn = f'  str_col_nums_{call_id}_2 = str_col_nums_{call_id}\n'
    vdo__pboq = np.array(usecols + ([idx_col_index] if idx_col_index is not
        None else []), dtype=np.int64)
    glbs[f'usecols_arr_{call_id}'] = vdo__pboq
    jbyfw__eyn += f'  usecols_arr_{call_id}_2 = usecols_arr_{call_id}\n'
    ilgzl__dsq = np.array(type_usecol_offset, dtype=np.int64)
    if usecols:
        glbs[f'type_usecols_offsets_arr_{call_id}'] = ilgzl__dsq
        jbyfw__eyn += f"""  type_usecols_offsets_arr_{call_id}_2 = type_usecols_offsets_arr_{call_id}
"""
    fnvay__qlte = defaultdict(list)
    for pqbmm__euy, otk__fcumf in enumerate(usecols):
        if fgqc__lxqwu[pqbmm__euy] == 'str':
            continue
        fnvay__qlte[fgqc__lxqwu[pqbmm__euy]].append(otk__fcumf)
    if idx_col_index is not None and eca__jlh != 'str':
        fnvay__qlte[eca__jlh].append(idx_col_index)
    for pqbmm__euy, okz__fni in enumerate(fnvay__qlte.values()):
        glbs[f't_arr_{pqbmm__euy}_{call_id}'] = np.asarray(okz__fni)
        jbyfw__eyn += (
            f'  t_arr_{pqbmm__euy}_{call_id}_2 = t_arr_{pqbmm__euy}_{call_id}\n'
            )
    if idx_col_index != None:
        jbyfw__eyn += f"""  with objmode(T=table_type_{call_id}, idx_arr=idx_array_typ, {eeqh__hcvu}):
"""
    else:
        jbyfw__eyn += (
            f'  with objmode(T=table_type_{call_id}, {eeqh__hcvu}):\n')
    jbyfw__eyn += f'    typemap = {{}}\n'
    for pqbmm__euy, mkyf__kwwp in enumerate(fnvay__qlte.keys()):
        jbyfw__eyn += f"""    typemap.update({{i:{mkyf__kwwp} for i in t_arr_{pqbmm__euy}_{call_id}_2}})
"""
    jbyfw__eyn += '    if f_reader.get_chunk_size() == 0:\n'
    jbyfw__eyn += (
        f'      df = pd.DataFrame(columns=usecols_arr_{call_id}_2, dtype=str)\n'
        )
    jbyfw__eyn += '    else:\n'
    jbyfw__eyn += '      df = pd.read_csv(f_reader,\n'
    jbyfw__eyn += '        header=None,\n'
    jbyfw__eyn += '        parse_dates=[{}],\n'.format(ihfkw__fwbhx)
    jbyfw__eyn += (
        f'        dtype={{i:str for i in str_col_nums_{call_id}_2}},\n')
    jbyfw__eyn += f"""        usecols=usecols_arr_{call_id}_2, sep={sep!r}, low_memory=False, escapechar={escapechar!r})
"""
    if check_parallel_runtime:
        jbyfw__eyn += f'    {ufhh__yrcfw} = f_reader.is_parallel()\n'
    else:
        jbyfw__eyn += f'    {ufhh__yrcfw} = {parallel}\n'
    jbyfw__eyn += f'    df = astype(df, typemap, {ufhh__yrcfw})\n'
    if idx_col_index != None:
        iyegt__uexj = sorted(vdo__pboq).index(idx_col_index)
        jbyfw__eyn += f'    idx_arr = df.iloc[:, {iyegt__uexj}].values\n'
        jbyfw__eyn += (
            f'    df.drop(columns=df.columns[{iyegt__uexj}], inplace=True)\n')
    if len(usecols) == 0:
        jbyfw__eyn += f'    T = None\n'
    else:
        jbyfw__eyn += f'    arrs = []\n'
        jbyfw__eyn += f'    for i in range(df.shape[1]):\n'
        jbyfw__eyn += f'      arrs.append(df.iloc[:, i].values)\n'
        jbyfw__eyn += f"""    T = Table(arrs, type_usecols_offsets_arr_{call_id}_2, {len(col_names)})
"""
    return jbyfw__eyn


def _gen_parallel_flag_name(sanitized_cnames):
    ufhh__yrcfw = '_parallel_value'
    while ufhh__yrcfw in sanitized_cnames:
        ufhh__yrcfw = '_' + ufhh__yrcfw
    return ufhh__yrcfw


def _gen_csv_reader_py(col_names, col_typs, usecols, type_usecol_offset,
    sep, parallel, header, compression, is_skiprows_list, pd_low_memory,
    escapechar, storage_options, idx_col_index=None, idx_col_typ=types.none):
    sanitized_cnames = [sanitize_varname(qhijr__myrgm) for qhijr__myrgm in
        col_names]
    jbyfw__eyn = 'def csv_reader_py(fname, nrows, skiprows):\n'
    jbyfw__eyn += _gen_csv_file_reader_init(parallel, header, compression, 
        -1, is_skiprows_list, pd_low_memory, storage_options)
    call_id = ir_utils.next_label()
    wuln__sqdjt = globals()
    if idx_col_typ != types.none:
        wuln__sqdjt[f'idx_array_typ'] = idx_col_typ
    if len(usecols) == 0:
        wuln__sqdjt[f'table_type_{call_id}'] = types.none
    else:
        wuln__sqdjt[f'table_type_{call_id}'] = TableType(tuple(col_typs))
    jbyfw__eyn += _gen_read_csv_objmode(col_names, sanitized_cnames,
        col_typs, usecols, type_usecol_offset, sep, escapechar,
        storage_options, call_id, wuln__sqdjt, parallel=parallel,
        check_parallel_runtime=False, idx_col_index=idx_col_index,
        idx_col_typ=idx_col_typ)
    if idx_col_index != None:
        jbyfw__eyn += '  return (T, idx_arr)\n'
    else:
        jbyfw__eyn += '  return (T, None)\n'
    weczx__tkhgr = {}
    wuln__sqdjt['get_storage_options_pyobject'] = get_storage_options_pyobject
    exec(jbyfw__eyn, wuln__sqdjt, weczx__tkhgr)
    opw__ustaf = weczx__tkhgr['csv_reader_py']
    tvlj__lpze = numba.njit(opw__ustaf)
    compiled_funcs.append(tvlj__lpze)
    return tvlj__lpze
