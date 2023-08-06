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
    rct__noh = typemap[node.file_name.name]
    if types.unliteral(rct__noh) != types.unicode_type:
        raise BodoError(
            f"pd.read_csv(): 'filepath_or_buffer' must be a string. Found type: {rct__noh}."
            , node.file_name.loc)
    if not isinstance(node.skiprows, ir.Const):
        rwkb__jre = typemap[node.skiprows.name]
        if isinstance(rwkb__jre, types.Dispatcher):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' callable not supported yet.",
                node.file_name.loc)
        elif not isinstance(rwkb__jre, types.Integer) and not (isinstance(
            rwkb__jre, (types.List, types.Tuple)) and isinstance(rwkb__jre.
            dtype, types.Integer)) and not isinstance(rwkb__jre, (types.
            LiteralList, bodo.utils.typing.ListLiteral)):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' must be an integer or list of integers. Found type {rwkb__jre}."
                , loc=node.skiprows.loc)
        elif isinstance(rwkb__jre, (types.List, types.Tuple)):
            node.is_skiprows_list = True
    if not isinstance(node.nrows, ir.Const):
        bruxr__lsfb = typemap[node.nrows.name]
        if not isinstance(bruxr__lsfb, types.Integer):
            raise BodoError(
                f"pd.read_csv(): 'nrows' must be an integer. Found type {bruxr__lsfb}."
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
        bmz__tip = csv_node.out_vars[0]
        if bmz__tip.name not in lives:
            return None
    else:
        jqb__pwyao = csv_node.out_vars[0]
        oqblw__tak = csv_node.out_vars[1]
        if jqb__pwyao.name not in lives and oqblw__tak.name not in lives:
            return None
        elif oqblw__tak.name not in lives:
            csv_node.index_column_index = None
            csv_node.index_column_typ = types.none
        elif jqb__pwyao.name not in lives:
            csv_node.usecols = []
            csv_node.out_types = []
            csv_node.type_usecol_offset = []
    return csv_node


def csv_distributed_run(csv_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    rwkb__jre = types.int64 if isinstance(csv_node.skiprows, ir.Const
        ) else types.unliteral(typemap[csv_node.skiprows.name])
    if csv_node.chunksize is not None:
        parallel = False
        if bodo.user_logging.get_verbose_level() >= 1:
            aua__ndpu = (
                'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n'
                )
            phl__rcuk = csv_node.loc.strformat()
            qqn__okcwg = csv_node.df_colnames
            bodo.user_logging.log_message('Column Pruning', aua__ndpu,
                phl__rcuk, qqn__okcwg)
            ajib__mjdbu = csv_node.out_types[0].yield_type.data
            hsbsz__urk = [dmm__bliz for xmgtq__nfs, dmm__bliz in enumerate(
                csv_node.df_colnames) if isinstance(ajib__mjdbu[xmgtq__nfs],
                bodo.libs.dict_arr_ext.DictionaryArrayType)]
            if hsbsz__urk:
                cqv__mgn = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
                bodo.user_logging.log_message('Dictionary Encoding',
                    cqv__mgn, phl__rcuk, hsbsz__urk)
        if array_dists is not None:
            qbaut__tofgs = csv_node.out_vars[0].name
            parallel = array_dists[qbaut__tofgs] in (distributed_pass.
                Distribution.OneD, distributed_pass.Distribution.OneD_Var)
        vrbi__wgj = 'def csv_iterator_impl(fname, nrows, skiprows):\n'
        vrbi__wgj += f'    reader = _csv_reader_init(fname, nrows, skiprows)\n'
        vrbi__wgj += (
            f'    iterator = init_csv_iterator(reader, csv_iterator_type)\n')
        lkgam__iphcf = {}
        from bodo.io.csv_iterator_ext import init_csv_iterator
        exec(vrbi__wgj, {}, lkgam__iphcf)
        gbgfm__tcosg = lkgam__iphcf['csv_iterator_impl']
        nwex__kvyy = 'def csv_reader_init(fname, nrows, skiprows):\n'
        nwex__kvyy += _gen_csv_file_reader_init(parallel, csv_node.header,
            csv_node.compression, csv_node.chunksize, csv_node.
            is_skiprows_list, csv_node.pd_low_memory, csv_node.storage_options)
        nwex__kvyy += '  return f_reader\n'
        exec(nwex__kvyy, globals(), lkgam__iphcf)
        hjhry__zmlrw = lkgam__iphcf['csv_reader_init']
        ikrgm__gfyn = numba.njit(hjhry__zmlrw)
        compiled_funcs.append(ikrgm__gfyn)
        mhmt__wwbt = compile_to_numba_ir(gbgfm__tcosg, {'_csv_reader_init':
            ikrgm__gfyn, 'init_csv_iterator': init_csv_iterator,
            'csv_iterator_type': typemap[csv_node.out_vars[0].name]},
            typingctx=typingctx, targetctx=targetctx, arg_typs=(string_type,
            types.int64, rwkb__jre), typemap=typemap, calltypes=calltypes
            ).blocks.popitem()[1]
        replace_arg_nodes(mhmt__wwbt, [csv_node.file_name, csv_node.nrows,
            csv_node.skiprows])
        cfj__cotp = mhmt__wwbt.body[:-3]
        cfj__cotp[-1].target = csv_node.out_vars[0]
        return cfj__cotp
    parallel = bodo.ir.connector.is_connector_table_parallel(csv_node,
        array_dists, typemap, 'CSVReader')
    vrbi__wgj = 'def csv_impl(fname, nrows, skiprows):\n'
    vrbi__wgj += (
        f'    (table_val, idx_col) = _csv_reader_py(fname, nrows, skiprows)\n')
    lkgam__iphcf = {}
    exec(vrbi__wgj, {}, lkgam__iphcf)
    exsy__zmaat = lkgam__iphcf['csv_impl']
    bezst__ttfv = csv_node.usecols
    if bezst__ttfv:
        bezst__ttfv = [csv_node.usecols[xmgtq__nfs] for xmgtq__nfs in
            csv_node.type_usecol_offset]
    if bodo.user_logging.get_verbose_level() >= 1:
        aua__ndpu = (
            'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n')
        phl__rcuk = csv_node.loc.strformat()
        qqn__okcwg = []
        hsbsz__urk = []
        if bezst__ttfv:
            for xmgtq__nfs in bezst__ttfv:
                ejj__qtq = csv_node.df_colnames[xmgtq__nfs]
                qqn__okcwg.append(ejj__qtq)
                if isinstance(csv_node.out_types[xmgtq__nfs], bodo.libs.
                    dict_arr_ext.DictionaryArrayType):
                    hsbsz__urk.append(ejj__qtq)
        bodo.user_logging.log_message('Column Pruning', aua__ndpu,
            phl__rcuk, qqn__okcwg)
        if hsbsz__urk:
            cqv__mgn = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', cqv__mgn,
                phl__rcuk, hsbsz__urk)
    xqu__jme = _gen_csv_reader_py(csv_node.df_colnames, csv_node.out_types,
        bezst__ttfv, csv_node.type_usecol_offset, csv_node.sep, parallel,
        csv_node.header, csv_node.compression, csv_node.is_skiprows_list,
        csv_node.pd_low_memory, csv_node.escapechar, csv_node.
        storage_options, idx_col_index=csv_node.index_column_index,
        idx_col_typ=csv_node.index_column_typ)
    mhmt__wwbt = compile_to_numba_ir(exsy__zmaat, {'_csv_reader_py':
        xqu__jme}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type, types.int64, rwkb__jre), typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(mhmt__wwbt, [csv_node.file_name, csv_node.nrows,
        csv_node.skiprows, csv_node.is_skiprows_list])
    cfj__cotp = mhmt__wwbt.body[:-3]
    cfj__cotp[-1].target = csv_node.out_vars[1]
    cfj__cotp[-2].target = csv_node.out_vars[0]
    assert not (csv_node.index_column_index is None and not bezst__ttfv
        ), 'At most one of table and index should be dead if the CSV IR node is live'
    if csv_node.index_column_index is None:
        cfj__cotp.pop(-1)
    elif not bezst__ttfv:
        cfj__cotp.pop(-2)
    return cfj__cotp


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
    gyahi__ghnc = t.dtype
    if isinstance(gyahi__ghnc, PDCategoricalDtype):
        bzu__rdj = CategoricalArrayType(gyahi__ghnc)
        qxk__kpek = 'CategoricalArrayType' + str(ir_utils.next_label())
        setattr(types, qxk__kpek, bzu__rdj)
        return qxk__kpek
    if gyahi__ghnc == types.NPDatetime('ns'):
        gyahi__ghnc = 'NPDatetime("ns")'
    if t == string_array_type:
        types.string_array_type = string_array_type
        return 'string_array_type'
    if isinstance(t, IntegerArrayType):
        gsyg__hhcjc = 'int_arr_{}'.format(gyahi__ghnc)
        setattr(types, gsyg__hhcjc, t)
        return gsyg__hhcjc
    if t == boolean_array:
        types.boolean_array = boolean_array
        return 'boolean_array'
    if gyahi__ghnc == types.bool_:
        gyahi__ghnc = 'bool_'
    if gyahi__ghnc == datetime_date_type:
        return 'datetime_date_array_type'
    if isinstance(t, ArrayItemArrayType) and isinstance(gyahi__ghnc, (
        StringArrayType, ArrayItemArrayType)):
        xhs__odbbj = f'ArrayItemArrayType{str(ir_utils.next_label())}'
        setattr(types, xhs__odbbj, t)
        return xhs__odbbj
    return '{}[::1]'.format(gyahi__ghnc)


def _get_pd_dtype_str(t):
    gyahi__ghnc = t.dtype
    if isinstance(gyahi__ghnc, PDCategoricalDtype):
        return 'pd.CategoricalDtype({})'.format(gyahi__ghnc.categories)
    if gyahi__ghnc == types.NPDatetime('ns'):
        return 'str'
    if t == string_array_type:
        return 'str'
    if isinstance(t, IntegerArrayType):
        return '"{}Int{}"'.format('' if gyahi__ghnc.signed else 'U',
            gyahi__ghnc.bitwidth)
    if t == boolean_array:
        return 'np.bool_'
    if isinstance(t, ArrayItemArrayType) and isinstance(gyahi__ghnc, (
        StringArrayType, ArrayItemArrayType)):
        return 'object'
    return 'np.{}'.format(gyahi__ghnc)


compiled_funcs = []


@numba.njit
def check_nrows_skiprows_value(nrows, skiprows):
    if nrows < -1:
        raise ValueError('pd.read_csv: nrows must be integer >= 0.')
    if skiprows[0] < 0:
        raise ValueError('pd.read_csv: skiprows must be integer >= 0.')


def astype(df, typemap, parallel):
    nxgy__xfiio = ''
    from collections import defaultdict
    ucnzt__lreox = defaultdict(list)
    for sfjsd__vik, zvqsh__pjobw in typemap.items():
        ucnzt__lreox[zvqsh__pjobw].append(sfjsd__vik)
    edijx__knkz = df.columns.to_list()
    bepu__fqmv = []
    for zvqsh__pjobw, qdwxf__pnwdx in ucnzt__lreox.items():
        try:
            bepu__fqmv.append(df.loc[:, qdwxf__pnwdx].astype(zvqsh__pjobw,
                copy=False))
            df = df.drop(qdwxf__pnwdx, axis=1)
        except (ValueError, TypeError) as fwyp__vmxg:
            nxgy__xfiio = (
                f"Caught the runtime error '{fwyp__vmxg}' on columns {qdwxf__pnwdx}. Consider setting the 'dtype' argument in 'read_csv' or investigate if the data is corrupted."
                )
            break
    bjptl__yeamx = bool(nxgy__xfiio)
    if parallel:
        ibmym__hroum = MPI.COMM_WORLD
        bjptl__yeamx = ibmym__hroum.allreduce(bjptl__yeamx, op=MPI.LOR)
    if bjptl__yeamx:
        flyuj__srrl = 'pd.read_csv(): Bodo could not infer dtypes correctly.'
        if nxgy__xfiio:
            raise TypeError(f'{flyuj__srrl}\n{nxgy__xfiio}')
        else:
            raise TypeError(
                f'{flyuj__srrl}\nPlease refer to errors on other ranks.')
    df = pd.concat(bepu__fqmv + [df], axis=1)
    yxq__eink = df.loc[:, edijx__knkz]
    return yxq__eink


def _gen_csv_file_reader_init(parallel, header, compression, chunksize,
    is_skiprows_list, pd_low_memory, storage_options):
    jaz__wpunf = header == 0
    if compression is None:
        compression = 'uncompressed'
    if is_skiprows_list:
        vrbi__wgj = '  skiprows = sorted(set(skiprows))\n'
    else:
        vrbi__wgj = '  skiprows = [skiprows]\n'
    vrbi__wgj += '  skiprows_list_len = len(skiprows)\n'
    vrbi__wgj += '  check_nrows_skiprows_value(nrows, skiprows)\n'
    vrbi__wgj += '  check_java_installation(fname)\n'
    vrbi__wgj += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    vrbi__wgj += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    vrbi__wgj += (
        '  f_reader = bodo.ir.csv_ext.csv_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    vrbi__wgj += (
        """    {}, bodo.utils.conversion.coerce_to_ndarray(skiprows, scalar_to_arr_len=1).ctypes, nrows, {}, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py, {}, {}, skiprows_list_len, {})
"""
        .format(parallel, jaz__wpunf, compression, chunksize,
        is_skiprows_list, pd_low_memory))
    vrbi__wgj += '  bodo.utils.utils.check_and_propagate_cpp_exception()\n'
    vrbi__wgj += '  if bodo.utils.utils.is_null_pointer(f_reader):\n'
    vrbi__wgj += "      raise FileNotFoundError('File does not exist')\n"
    return vrbi__wgj


def _gen_read_csv_objmode(col_names, sanitized_cnames, col_typs, usecols,
    type_usecol_offset, sep, escapechar, storage_options, call_id, glbs,
    parallel, check_parallel_runtime, idx_col_index, idx_col_typ):
    bskd__eyl = [str(xmgtq__nfs) for xmgtq__nfs, vgen__qtxl in enumerate(
        usecols) if col_typs[type_usecol_offset[xmgtq__nfs]].dtype == types
        .NPDatetime('ns')]
    if idx_col_typ == types.NPDatetime('ns'):
        assert not idx_col_index is None
        bskd__eyl.append(str(idx_col_index))
    kkht__gnbpf = ', '.join(bskd__eyl)
    fjpq__judla = _gen_parallel_flag_name(sanitized_cnames)
    itcyl__crlt = f"{fjpq__judla}='bool_'" if check_parallel_runtime else ''
    wcpqt__jzyz = [_get_pd_dtype_str(col_typs[type_usecol_offset[xmgtq__nfs
        ]]) for xmgtq__nfs in range(len(usecols))]
    onhk__thxc = None if idx_col_index is None else _get_pd_dtype_str(
        idx_col_typ)
    xydb__ial = [vgen__qtxl for xmgtq__nfs, vgen__qtxl in enumerate(usecols
        ) if wcpqt__jzyz[xmgtq__nfs] == 'str']
    if idx_col_index is not None and onhk__thxc == 'str':
        xydb__ial.append(idx_col_index)
    enb__ntp = np.array(xydb__ial, dtype=np.int64)
    glbs[f'str_col_nums_{call_id}'] = enb__ntp
    vrbi__wgj = f'  str_col_nums_{call_id}_2 = str_col_nums_{call_id}\n'
    xuc__uldq = np.array(usecols + ([idx_col_index] if idx_col_index is not
        None else []), dtype=np.int64)
    glbs[f'usecols_arr_{call_id}'] = xuc__uldq
    vrbi__wgj += f'  usecols_arr_{call_id}_2 = usecols_arr_{call_id}\n'
    qsc__heujl = np.array(type_usecol_offset, dtype=np.int64)
    if usecols:
        glbs[f'type_usecols_offsets_arr_{call_id}'] = qsc__heujl
        vrbi__wgj += f"""  type_usecols_offsets_arr_{call_id}_2 = type_usecols_offsets_arr_{call_id}
"""
    jck__hzr = defaultdict(list)
    for xmgtq__nfs, vgen__qtxl in enumerate(usecols):
        if wcpqt__jzyz[xmgtq__nfs] == 'str':
            continue
        jck__hzr[wcpqt__jzyz[xmgtq__nfs]].append(vgen__qtxl)
    if idx_col_index is not None and onhk__thxc != 'str':
        jck__hzr[onhk__thxc].append(idx_col_index)
    for xmgtq__nfs, kpjdo__rhvxl in enumerate(jck__hzr.values()):
        glbs[f't_arr_{xmgtq__nfs}_{call_id}'] = np.asarray(kpjdo__rhvxl)
        vrbi__wgj += (
            f'  t_arr_{xmgtq__nfs}_{call_id}_2 = t_arr_{xmgtq__nfs}_{call_id}\n'
            )
    if idx_col_index != None:
        vrbi__wgj += f"""  with objmode(T=table_type_{call_id}, idx_arr=idx_array_typ, {itcyl__crlt}):
"""
    else:
        vrbi__wgj += (
            f'  with objmode(T=table_type_{call_id}, {itcyl__crlt}):\n')
    vrbi__wgj += f'    typemap = {{}}\n'
    for xmgtq__nfs, tjftg__vtk in enumerate(jck__hzr.keys()):
        vrbi__wgj += f"""    typemap.update({{i:{tjftg__vtk} for i in t_arr_{xmgtq__nfs}_{call_id}_2}})
"""
    vrbi__wgj += '    if f_reader.get_chunk_size() == 0:\n'
    vrbi__wgj += (
        f'      df = pd.DataFrame(columns=usecols_arr_{call_id}_2, dtype=str)\n'
        )
    vrbi__wgj += '    else:\n'
    vrbi__wgj += '      df = pd.read_csv(f_reader,\n'
    vrbi__wgj += '        header=None,\n'
    vrbi__wgj += '        parse_dates=[{}],\n'.format(kkht__gnbpf)
    vrbi__wgj += (
        f'        dtype={{i:str for i in str_col_nums_{call_id}_2}},\n')
    vrbi__wgj += f"""        usecols=usecols_arr_{call_id}_2, sep={sep!r}, low_memory=False, escapechar={escapechar!r})
"""
    if check_parallel_runtime:
        vrbi__wgj += f'    {fjpq__judla} = f_reader.is_parallel()\n'
    else:
        vrbi__wgj += f'    {fjpq__judla} = {parallel}\n'
    vrbi__wgj += f'    df = astype(df, typemap, {fjpq__judla})\n'
    if idx_col_index != None:
        psj__icucw = sorted(xuc__uldq).index(idx_col_index)
        vrbi__wgj += f'    idx_arr = df.iloc[:, {psj__icucw}].values\n'
        vrbi__wgj += (
            f'    df.drop(columns=df.columns[{psj__icucw}], inplace=True)\n')
    if len(usecols) == 0:
        vrbi__wgj += f'    T = None\n'
    else:
        vrbi__wgj += f'    arrs = []\n'
        vrbi__wgj += f'    for i in range(df.shape[1]):\n'
        vrbi__wgj += f'      arrs.append(df.iloc[:, i].values)\n'
        vrbi__wgj += f"""    T = Table(arrs, type_usecols_offsets_arr_{call_id}_2, {len(col_names)})
"""
    return vrbi__wgj


def _gen_parallel_flag_name(sanitized_cnames):
    fjpq__judla = '_parallel_value'
    while fjpq__judla in sanitized_cnames:
        fjpq__judla = '_' + fjpq__judla
    return fjpq__judla


def _gen_csv_reader_py(col_names, col_typs, usecols, type_usecol_offset,
    sep, parallel, header, compression, is_skiprows_list, pd_low_memory,
    escapechar, storage_options, idx_col_index=None, idx_col_typ=types.none):
    sanitized_cnames = [sanitize_varname(dmm__bliz) for dmm__bliz in col_names]
    vrbi__wgj = 'def csv_reader_py(fname, nrows, skiprows):\n'
    vrbi__wgj += _gen_csv_file_reader_init(parallel, header, compression, -
        1, is_skiprows_list, pd_low_memory, storage_options)
    call_id = ir_utils.next_label()
    fzu__ysb = globals()
    if idx_col_typ != types.none:
        fzu__ysb[f'idx_array_typ'] = idx_col_typ
    if len(usecols) == 0:
        fzu__ysb[f'table_type_{call_id}'] = types.none
    else:
        fzu__ysb[f'table_type_{call_id}'] = TableType(tuple(col_typs))
    vrbi__wgj += _gen_read_csv_objmode(col_names, sanitized_cnames,
        col_typs, usecols, type_usecol_offset, sep, escapechar,
        storage_options, call_id, fzu__ysb, parallel=parallel,
        check_parallel_runtime=False, idx_col_index=idx_col_index,
        idx_col_typ=idx_col_typ)
    if idx_col_index != None:
        vrbi__wgj += '  return (T, idx_arr)\n'
    else:
        vrbi__wgj += '  return (T, None)\n'
    lkgam__iphcf = {}
    fzu__ysb['get_storage_options_pyobject'] = get_storage_options_pyobject
    exec(vrbi__wgj, fzu__ysb, lkgam__iphcf)
    xqu__jme = lkgam__iphcf['csv_reader_py']
    ikrgm__gfyn = numba.njit(xqu__jme)
    compiled_funcs.append(ikrgm__gfyn)
    return ikrgm__gfyn
