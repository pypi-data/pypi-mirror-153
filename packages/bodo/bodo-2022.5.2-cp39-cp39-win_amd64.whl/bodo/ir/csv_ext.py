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
    jnztc__tlgds = typemap[node.file_name.name]
    if types.unliteral(jnztc__tlgds) != types.unicode_type:
        raise BodoError(
            f"pd.read_csv(): 'filepath_or_buffer' must be a string. Found type: {jnztc__tlgds}."
            , node.file_name.loc)
    if not isinstance(node.skiprows, ir.Const):
        vhq__grmce = typemap[node.skiprows.name]
        if isinstance(vhq__grmce, types.Dispatcher):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' callable not supported yet.",
                node.file_name.loc)
        elif not isinstance(vhq__grmce, types.Integer) and not (isinstance(
            vhq__grmce, (types.List, types.Tuple)) and isinstance(
            vhq__grmce.dtype, types.Integer)) and not isinstance(vhq__grmce,
            (types.LiteralList, bodo.utils.typing.ListLiteral)):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' must be an integer or list of integers. Found type {vhq__grmce}."
                , loc=node.skiprows.loc)
        elif isinstance(vhq__grmce, (types.List, types.Tuple)):
            node.is_skiprows_list = True
    if not isinstance(node.nrows, ir.Const):
        jgssb__thir = typemap[node.nrows.name]
        if not isinstance(jgssb__thir, types.Integer):
            raise BodoError(
                f"pd.read_csv(): 'nrows' must be an integer. Found type {jgssb__thir}."
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
        rki__ejxgn = csv_node.out_vars[0]
        if rki__ejxgn.name not in lives:
            return None
    else:
        pjqud__nimg = csv_node.out_vars[0]
        twr__tvdeb = csv_node.out_vars[1]
        if pjqud__nimg.name not in lives and twr__tvdeb.name not in lives:
            return None
        elif twr__tvdeb.name not in lives:
            csv_node.index_column_index = None
            csv_node.index_column_typ = types.none
        elif pjqud__nimg.name not in lives:
            csv_node.usecols = []
            csv_node.out_types = []
            csv_node.type_usecol_offset = []
    return csv_node


def csv_distributed_run(csv_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    vhq__grmce = types.int64 if isinstance(csv_node.skiprows, ir.Const
        ) else types.unliteral(typemap[csv_node.skiprows.name])
    if csv_node.chunksize is not None:
        parallel = False
        if bodo.user_logging.get_verbose_level() >= 1:
            sqy__fxil = (
                'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n'
                )
            hygru__hsbio = csv_node.loc.strformat()
            uguxt__zidbz = csv_node.df_colnames
            bodo.user_logging.log_message('Column Pruning', sqy__fxil,
                hygru__hsbio, uguxt__zidbz)
            pbpqu__fdjr = csv_node.out_types[0].yield_type.data
            jfw__paow = [xwm__edvet for zpj__qnb, xwm__edvet in enumerate(
                csv_node.df_colnames) if isinstance(pbpqu__fdjr[zpj__qnb],
                bodo.libs.dict_arr_ext.DictionaryArrayType)]
            if jfw__paow:
                yvm__tmz = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
                bodo.user_logging.log_message('Dictionary Encoding',
                    yvm__tmz, hygru__hsbio, jfw__paow)
        if array_dists is not None:
            oebgw__uuru = csv_node.out_vars[0].name
            parallel = array_dists[oebgw__uuru] in (distributed_pass.
                Distribution.OneD, distributed_pass.Distribution.OneD_Var)
        tmx__gdr = 'def csv_iterator_impl(fname, nrows, skiprows):\n'
        tmx__gdr += f'    reader = _csv_reader_init(fname, nrows, skiprows)\n'
        tmx__gdr += (
            f'    iterator = init_csv_iterator(reader, csv_iterator_type)\n')
        cog__bvfp = {}
        from bodo.io.csv_iterator_ext import init_csv_iterator
        exec(tmx__gdr, {}, cog__bvfp)
        iwgi__rbd = cog__bvfp['csv_iterator_impl']
        cibpj__rnjlj = 'def csv_reader_init(fname, nrows, skiprows):\n'
        cibpj__rnjlj += _gen_csv_file_reader_init(parallel, csv_node.header,
            csv_node.compression, csv_node.chunksize, csv_node.
            is_skiprows_list, csv_node.pd_low_memory, csv_node.storage_options)
        cibpj__rnjlj += '  return f_reader\n'
        exec(cibpj__rnjlj, globals(), cog__bvfp)
        nmywg__sujz = cog__bvfp['csv_reader_init']
        mql__wed = numba.njit(nmywg__sujz)
        compiled_funcs.append(mql__wed)
        ceen__fpxg = compile_to_numba_ir(iwgi__rbd, {'_csv_reader_init':
            mql__wed, 'init_csv_iterator': init_csv_iterator,
            'csv_iterator_type': typemap[csv_node.out_vars[0].name]},
            typingctx=typingctx, targetctx=targetctx, arg_typs=(string_type,
            types.int64, vhq__grmce), typemap=typemap, calltypes=calltypes
            ).blocks.popitem()[1]
        replace_arg_nodes(ceen__fpxg, [csv_node.file_name, csv_node.nrows,
            csv_node.skiprows])
        uwpzl__hppo = ceen__fpxg.body[:-3]
        uwpzl__hppo[-1].target = csv_node.out_vars[0]
        return uwpzl__hppo
    parallel = bodo.ir.connector.is_connector_table_parallel(csv_node,
        array_dists, typemap, 'CSVReader')
    tmx__gdr = 'def csv_impl(fname, nrows, skiprows):\n'
    tmx__gdr += (
        f'    (table_val, idx_col) = _csv_reader_py(fname, nrows, skiprows)\n')
    cog__bvfp = {}
    exec(tmx__gdr, {}, cog__bvfp)
    ywj__fpo = cog__bvfp['csv_impl']
    lsqba__ktt = csv_node.usecols
    if lsqba__ktt:
        lsqba__ktt = [csv_node.usecols[zpj__qnb] for zpj__qnb in csv_node.
            type_usecol_offset]
    if bodo.user_logging.get_verbose_level() >= 1:
        sqy__fxil = (
            'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n')
        hygru__hsbio = csv_node.loc.strformat()
        uguxt__zidbz = []
        jfw__paow = []
        if lsqba__ktt:
            for zpj__qnb in lsqba__ktt:
                ygpuq__jax = csv_node.df_colnames[zpj__qnb]
                uguxt__zidbz.append(ygpuq__jax)
                if isinstance(csv_node.out_types[zpj__qnb], bodo.libs.
                    dict_arr_ext.DictionaryArrayType):
                    jfw__paow.append(ygpuq__jax)
        bodo.user_logging.log_message('Column Pruning', sqy__fxil,
            hygru__hsbio, uguxt__zidbz)
        if jfw__paow:
            yvm__tmz = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', yvm__tmz,
                hygru__hsbio, jfw__paow)
    bfr__zorpp = _gen_csv_reader_py(csv_node.df_colnames, csv_node.
        out_types, lsqba__ktt, csv_node.type_usecol_offset, csv_node.sep,
        parallel, csv_node.header, csv_node.compression, csv_node.
        is_skiprows_list, csv_node.pd_low_memory, csv_node.escapechar,
        csv_node.storage_options, idx_col_index=csv_node.index_column_index,
        idx_col_typ=csv_node.index_column_typ)
    ceen__fpxg = compile_to_numba_ir(ywj__fpo, {'_csv_reader_py':
        bfr__zorpp}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type, types.int64, vhq__grmce), typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(ceen__fpxg, [csv_node.file_name, csv_node.nrows,
        csv_node.skiprows, csv_node.is_skiprows_list])
    uwpzl__hppo = ceen__fpxg.body[:-3]
    uwpzl__hppo[-1].target = csv_node.out_vars[1]
    uwpzl__hppo[-2].target = csv_node.out_vars[0]
    assert not (csv_node.index_column_index is None and not lsqba__ktt
        ), 'At most one of table and index should be dead if the CSV IR node is live'
    if csv_node.index_column_index is None:
        uwpzl__hppo.pop(-1)
    elif not lsqba__ktt:
        uwpzl__hppo.pop(-2)
    return uwpzl__hppo


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
    uyul__sjvb = t.dtype
    if isinstance(uyul__sjvb, PDCategoricalDtype):
        xfv__mnz = CategoricalArrayType(uyul__sjvb)
        rdwzy__awp = 'CategoricalArrayType' + str(ir_utils.next_label())
        setattr(types, rdwzy__awp, xfv__mnz)
        return rdwzy__awp
    if uyul__sjvb == types.NPDatetime('ns'):
        uyul__sjvb = 'NPDatetime("ns")'
    if t == string_array_type:
        types.string_array_type = string_array_type
        return 'string_array_type'
    if isinstance(t, IntegerArrayType):
        ubwqf__ocmvp = 'int_arr_{}'.format(uyul__sjvb)
        setattr(types, ubwqf__ocmvp, t)
        return ubwqf__ocmvp
    if t == boolean_array:
        types.boolean_array = boolean_array
        return 'boolean_array'
    if uyul__sjvb == types.bool_:
        uyul__sjvb = 'bool_'
    if uyul__sjvb == datetime_date_type:
        return 'datetime_date_array_type'
    if isinstance(t, ArrayItemArrayType) and isinstance(uyul__sjvb, (
        StringArrayType, ArrayItemArrayType)):
        vbmq__nor = f'ArrayItemArrayType{str(ir_utils.next_label())}'
        setattr(types, vbmq__nor, t)
        return vbmq__nor
    return '{}[::1]'.format(uyul__sjvb)


def _get_pd_dtype_str(t):
    uyul__sjvb = t.dtype
    if isinstance(uyul__sjvb, PDCategoricalDtype):
        return 'pd.CategoricalDtype({})'.format(uyul__sjvb.categories)
    if uyul__sjvb == types.NPDatetime('ns'):
        return 'str'
    if t == string_array_type:
        return 'str'
    if isinstance(t, IntegerArrayType):
        return '"{}Int{}"'.format('' if uyul__sjvb.signed else 'U',
            uyul__sjvb.bitwidth)
    if t == boolean_array:
        return 'np.bool_'
    if isinstance(t, ArrayItemArrayType) and isinstance(uyul__sjvb, (
        StringArrayType, ArrayItemArrayType)):
        return 'object'
    return 'np.{}'.format(uyul__sjvb)


compiled_funcs = []


@numba.njit
def check_nrows_skiprows_value(nrows, skiprows):
    if nrows < -1:
        raise ValueError('pd.read_csv: nrows must be integer >= 0.')
    if skiprows[0] < 0:
        raise ValueError('pd.read_csv: skiprows must be integer >= 0.')


def astype(df, typemap, parallel):
    supbp__wxq = ''
    from collections import defaultdict
    lbxu__olyfe = defaultdict(list)
    for djt__hsku, wnw__ejhb in typemap.items():
        lbxu__olyfe[wnw__ejhb].append(djt__hsku)
    ytm__vvl = df.columns.to_list()
    jaxf__inx = []
    for wnw__ejhb, umws__umy in lbxu__olyfe.items():
        try:
            jaxf__inx.append(df.loc[:, umws__umy].astype(wnw__ejhb, copy=False)
                )
            df = df.drop(umws__umy, axis=1)
        except (ValueError, TypeError) as wblw__pbqz:
            supbp__wxq = (
                f"Caught the runtime error '{wblw__pbqz}' on columns {umws__umy}. Consider setting the 'dtype' argument in 'read_csv' or investigate if the data is corrupted."
                )
            break
    adh__ken = bool(supbp__wxq)
    if parallel:
        ldnq__peelz = MPI.COMM_WORLD
        adh__ken = ldnq__peelz.allreduce(adh__ken, op=MPI.LOR)
    if adh__ken:
        jdn__xump = 'pd.read_csv(): Bodo could not infer dtypes correctly.'
        if supbp__wxq:
            raise TypeError(f'{jdn__xump}\n{supbp__wxq}')
        else:
            raise TypeError(
                f'{jdn__xump}\nPlease refer to errors on other ranks.')
    df = pd.concat(jaxf__inx + [df], axis=1)
    wpdca__bst = df.loc[:, ytm__vvl]
    return wpdca__bst


def _gen_csv_file_reader_init(parallel, header, compression, chunksize,
    is_skiprows_list, pd_low_memory, storage_options):
    hlxls__ilbhp = header == 0
    if compression is None:
        compression = 'uncompressed'
    if is_skiprows_list:
        tmx__gdr = '  skiprows = sorted(set(skiprows))\n'
    else:
        tmx__gdr = '  skiprows = [skiprows]\n'
    tmx__gdr += '  skiprows_list_len = len(skiprows)\n'
    tmx__gdr += '  check_nrows_skiprows_value(nrows, skiprows)\n'
    tmx__gdr += '  check_java_installation(fname)\n'
    tmx__gdr += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    tmx__gdr += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    tmx__gdr += (
        '  f_reader = bodo.ir.csv_ext.csv_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    tmx__gdr += (
        """    {}, bodo.utils.conversion.coerce_to_ndarray(skiprows, scalar_to_arr_len=1).ctypes, nrows, {}, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py, {}, {}, skiprows_list_len, {})
"""
        .format(parallel, hlxls__ilbhp, compression, chunksize,
        is_skiprows_list, pd_low_memory))
    tmx__gdr += '  bodo.utils.utils.check_and_propagate_cpp_exception()\n'
    tmx__gdr += '  if bodo.utils.utils.is_null_pointer(f_reader):\n'
    tmx__gdr += "      raise FileNotFoundError('File does not exist')\n"
    return tmx__gdr


def _gen_read_csv_objmode(col_names, sanitized_cnames, col_typs, usecols,
    type_usecol_offset, sep, escapechar, storage_options, call_id, glbs,
    parallel, check_parallel_runtime, idx_col_index, idx_col_typ):
    yvj__skczw = [str(zpj__qnb) for zpj__qnb, iiwuk__fhd in enumerate(
        usecols) if col_typs[type_usecol_offset[zpj__qnb]].dtype == types.
        NPDatetime('ns')]
    if idx_col_typ == types.NPDatetime('ns'):
        assert not idx_col_index is None
        yvj__skczw.append(str(idx_col_index))
    hxb__ypne = ', '.join(yvj__skczw)
    crjp__siadr = _gen_parallel_flag_name(sanitized_cnames)
    axt__goo = f"{crjp__siadr}='bool_'" if check_parallel_runtime else ''
    vlkc__ohwn = [_get_pd_dtype_str(col_typs[type_usecol_offset[zpj__qnb]]) for
        zpj__qnb in range(len(usecols))]
    txbb__lfrnb = None if idx_col_index is None else _get_pd_dtype_str(
        idx_col_typ)
    unom__rhu = [iiwuk__fhd for zpj__qnb, iiwuk__fhd in enumerate(usecols) if
        vlkc__ohwn[zpj__qnb] == 'str']
    if idx_col_index is not None and txbb__lfrnb == 'str':
        unom__rhu.append(idx_col_index)
    hjn__ahm = np.array(unom__rhu, dtype=np.int64)
    glbs[f'str_col_nums_{call_id}'] = hjn__ahm
    tmx__gdr = f'  str_col_nums_{call_id}_2 = str_col_nums_{call_id}\n'
    pbmom__foyhd = np.array(usecols + ([idx_col_index] if idx_col_index is not
        None else []), dtype=np.int64)
    glbs[f'usecols_arr_{call_id}'] = pbmom__foyhd
    tmx__gdr += f'  usecols_arr_{call_id}_2 = usecols_arr_{call_id}\n'
    aln__qsouj = np.array(type_usecol_offset, dtype=np.int64)
    if usecols:
        glbs[f'type_usecols_offsets_arr_{call_id}'] = aln__qsouj
        tmx__gdr += (
            f'  type_usecols_offsets_arr_{call_id}_2 = type_usecols_offsets_arr_{call_id}\n'
            )
    nxhdy__bna = defaultdict(list)
    for zpj__qnb, iiwuk__fhd in enumerate(usecols):
        if vlkc__ohwn[zpj__qnb] == 'str':
            continue
        nxhdy__bna[vlkc__ohwn[zpj__qnb]].append(iiwuk__fhd)
    if idx_col_index is not None and txbb__lfrnb != 'str':
        nxhdy__bna[txbb__lfrnb].append(idx_col_index)
    for zpj__qnb, rxkj__dunp in enumerate(nxhdy__bna.values()):
        glbs[f't_arr_{zpj__qnb}_{call_id}'] = np.asarray(rxkj__dunp)
        tmx__gdr += (
            f'  t_arr_{zpj__qnb}_{call_id}_2 = t_arr_{zpj__qnb}_{call_id}\n')
    if idx_col_index != None:
        tmx__gdr += (
            f'  with objmode(T=table_type_{call_id}, idx_arr=idx_array_typ, {axt__goo}):\n'
            )
    else:
        tmx__gdr += f'  with objmode(T=table_type_{call_id}, {axt__goo}):\n'
    tmx__gdr += f'    typemap = {{}}\n'
    for zpj__qnb, hqx__jgv in enumerate(nxhdy__bna.keys()):
        tmx__gdr += (
            f'    typemap.update({{i:{hqx__jgv} for i in t_arr_{zpj__qnb}_{call_id}_2}})\n'
            )
    tmx__gdr += '    if f_reader.get_chunk_size() == 0:\n'
    tmx__gdr += (
        f'      df = pd.DataFrame(columns=usecols_arr_{call_id}_2, dtype=str)\n'
        )
    tmx__gdr += '    else:\n'
    tmx__gdr += '      df = pd.read_csv(f_reader,\n'
    tmx__gdr += '        header=None,\n'
    tmx__gdr += '        parse_dates=[{}],\n'.format(hxb__ypne)
    tmx__gdr += f'        dtype={{i:str for i in str_col_nums_{call_id}_2}},\n'
    tmx__gdr += f"""        usecols=usecols_arr_{call_id}_2, sep={sep!r}, low_memory=False, escapechar={escapechar!r})
"""
    if check_parallel_runtime:
        tmx__gdr += f'    {crjp__siadr} = f_reader.is_parallel()\n'
    else:
        tmx__gdr += f'    {crjp__siadr} = {parallel}\n'
    tmx__gdr += f'    df = astype(df, typemap, {crjp__siadr})\n'
    if idx_col_index != None:
        jiz__eoce = sorted(pbmom__foyhd).index(idx_col_index)
        tmx__gdr += f'    idx_arr = df.iloc[:, {jiz__eoce}].values\n'
        tmx__gdr += (
            f'    df.drop(columns=df.columns[{jiz__eoce}], inplace=True)\n')
    if len(usecols) == 0:
        tmx__gdr += f'    T = None\n'
    else:
        tmx__gdr += f'    arrs = []\n'
        tmx__gdr += f'    for i in range(df.shape[1]):\n'
        tmx__gdr += f'      arrs.append(df.iloc[:, i].values)\n'
        tmx__gdr += (
            f'    T = Table(arrs, type_usecols_offsets_arr_{call_id}_2, {len(col_names)})\n'
            )
    return tmx__gdr


def _gen_parallel_flag_name(sanitized_cnames):
    crjp__siadr = '_parallel_value'
    while crjp__siadr in sanitized_cnames:
        crjp__siadr = '_' + crjp__siadr
    return crjp__siadr


def _gen_csv_reader_py(col_names, col_typs, usecols, type_usecol_offset,
    sep, parallel, header, compression, is_skiprows_list, pd_low_memory,
    escapechar, storage_options, idx_col_index=None, idx_col_typ=types.none):
    sanitized_cnames = [sanitize_varname(xwm__edvet) for xwm__edvet in
        col_names]
    tmx__gdr = 'def csv_reader_py(fname, nrows, skiprows):\n'
    tmx__gdr += _gen_csv_file_reader_init(parallel, header, compression, -1,
        is_skiprows_list, pd_low_memory, storage_options)
    call_id = ir_utils.next_label()
    xdex__cvzuk = globals()
    if idx_col_typ != types.none:
        xdex__cvzuk[f'idx_array_typ'] = idx_col_typ
    if len(usecols) == 0:
        xdex__cvzuk[f'table_type_{call_id}'] = types.none
    else:
        xdex__cvzuk[f'table_type_{call_id}'] = TableType(tuple(col_typs))
    tmx__gdr += _gen_read_csv_objmode(col_names, sanitized_cnames, col_typs,
        usecols, type_usecol_offset, sep, escapechar, storage_options,
        call_id, xdex__cvzuk, parallel=parallel, check_parallel_runtime=
        False, idx_col_index=idx_col_index, idx_col_typ=idx_col_typ)
    if idx_col_index != None:
        tmx__gdr += '  return (T, idx_arr)\n'
    else:
        tmx__gdr += '  return (T, None)\n'
    cog__bvfp = {}
    xdex__cvzuk['get_storage_options_pyobject'] = get_storage_options_pyobject
    exec(tmx__gdr, xdex__cvzuk, cog__bvfp)
    bfr__zorpp = cog__bvfp['csv_reader_py']
    mql__wed = numba.njit(bfr__zorpp)
    compiled_funcs.append(mql__wed)
    return mql__wed
