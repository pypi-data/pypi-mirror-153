import numba
import numpy as np
import pandas as pd
from numba.core import ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, replace_arg_nodes
import bodo
import bodo.ir.connector
from bodo import objmode
from bodo.io.fs_io import get_storage_options_pyobject, storage_options_dict_type
from bodo.libs.str_ext import string_type
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.utils.utils import check_java_installation, sanitize_varname


class JsonReader(ir.Stmt):

    def __init__(self, df_out, loc, out_vars, out_types, file_name,
        df_colnames, orient, convert_dates, precise_float, lines,
        compression, storage_options):
        self.connector_typ = 'json'
        self.df_out = df_out
        self.loc = loc
        self.out_vars = out_vars
        self.out_types = out_types
        self.file_name = file_name
        self.df_colnames = df_colnames
        self.orient = orient
        self.convert_dates = convert_dates
        self.precise_float = precise_float
        self.lines = lines
        self.compression = compression
        self.storage_options = storage_options

    def __repr__(self):
        return ('{} = ReadJson(file={}, col_names={}, types={}, vars={})'.
            format(self.df_out, self.file_name, self.df_colnames, self.
            out_types, self.out_vars))


import llvmlite.binding as ll
from bodo.io import json_cpp
ll.add_symbol('json_file_chunk_reader', json_cpp.json_file_chunk_reader)
json_file_chunk_reader = types.ExternalFunction('json_file_chunk_reader',
    bodo.ir.connector.stream_reader_type(types.voidptr, types.bool_, types.
    bool_, types.int64, types.voidptr, types.voidptr,
    storage_options_dict_type))


def remove_dead_json(json_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    blxee__cupdb = []
    mpmji__bye = []
    hssmo__dky = []
    for iwyb__nkib, xmq__jdn in enumerate(json_node.out_vars):
        if xmq__jdn.name in lives:
            blxee__cupdb.append(json_node.df_colnames[iwyb__nkib])
            mpmji__bye.append(json_node.out_vars[iwyb__nkib])
            hssmo__dky.append(json_node.out_types[iwyb__nkib])
    json_node.df_colnames = blxee__cupdb
    json_node.out_vars = mpmji__bye
    json_node.out_types = hssmo__dky
    if len(json_node.out_vars) == 0:
        return None
    return json_node


def json_distributed_run(json_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 1:
        jrvhy__kci = (
            'Finish column pruning on read_json node:\n%s\nColumns loaded %s\n'
            )
        loj__gukhj = json_node.loc.strformat()
        zyb__uwp = json_node.df_colnames
        bodo.user_logging.log_message('Column Pruning', jrvhy__kci,
            loj__gukhj, zyb__uwp)
        nxyml__ukpf = [rsx__mddh for iwyb__nkib, rsx__mddh in enumerate(
            json_node.df_colnames) if isinstance(json_node.out_types[
            iwyb__nkib], bodo.libs.dict_arr_ext.DictionaryArrayType)]
        if nxyml__ukpf:
            tvgu__ptvrl = """Finished optimized encoding on read_json node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                tvgu__ptvrl, loj__gukhj, nxyml__ukpf)
    parallel = False
    if array_dists is not None:
        parallel = True
        for jsjq__wcnl in json_node.out_vars:
            if array_dists[jsjq__wcnl.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                jsjq__wcnl.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    tata__vpav = len(json_node.out_vars)
    uemx__heeoj = ', '.join('arr' + str(iwyb__nkib) for iwyb__nkib in range
        (tata__vpav))
    mkb__mayxr = 'def json_impl(fname):\n'
    mkb__mayxr += '    ({},) = _json_reader_py(fname)\n'.format(uemx__heeoj)
    zuxia__atzo = {}
    exec(mkb__mayxr, {}, zuxia__atzo)
    mduj__jalaj = zuxia__atzo['json_impl']
    gjr__fnv = _gen_json_reader_py(json_node.df_colnames, json_node.
        out_types, typingctx, targetctx, parallel, json_node.orient,
        json_node.convert_dates, json_node.precise_float, json_node.lines,
        json_node.compression, json_node.storage_options)
    jis__gtq = compile_to_numba_ir(mduj__jalaj, {'_json_reader_py':
        gjr__fnv}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type,), typemap=typemap, calltypes=calltypes).blocks.popitem()[1
        ]
    replace_arg_nodes(jis__gtq, [json_node.file_name])
    rculo__inro = jis__gtq.body[:-3]
    for iwyb__nkib in range(len(json_node.out_vars)):
        rculo__inro[-len(json_node.out_vars) + iwyb__nkib
            ].target = json_node.out_vars[iwyb__nkib]
    return rculo__inro


numba.parfors.array_analysis.array_analysis_extensions[JsonReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[JsonReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[JsonReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[JsonReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[JsonReader] = remove_dead_json
numba.core.analysis.ir_extension_usedefs[JsonReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[JsonReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[JsonReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[JsonReader
    ] = bodo.ir.connector.build_connector_definitions
distributed_pass.distributed_run_extensions[JsonReader] = json_distributed_run
compiled_funcs = []


def _gen_json_reader_py(col_names, col_typs, typingctx, targetctx, parallel,
    orient, convert_dates, precise_float, lines, compression, storage_options):
    diupg__nytqo = [sanitize_varname(rsx__mddh) for rsx__mddh in col_names]
    xcpyr__uirez = ', '.join(str(iwyb__nkib) for iwyb__nkib, wivqr__ioo in
        enumerate(col_typs) if wivqr__ioo.dtype == types.NPDatetime('ns'))
    ptnv__owc = ', '.join(["{}='{}'".format(ruq__wfna, bodo.ir.csv_ext.
        _get_dtype_str(wivqr__ioo)) for ruq__wfna, wivqr__ioo in zip(
        diupg__nytqo, col_typs)])
    omp__amrr = ', '.join(["'{}':{}".format(ytya__vysn, bodo.ir.csv_ext.
        _get_pd_dtype_str(wivqr__ioo)) for ytya__vysn, wivqr__ioo in zip(
        col_names, col_typs)])
    if compression is None:
        compression = 'uncompressed'
    mkb__mayxr = 'def json_reader_py(fname):\n'
    mkb__mayxr += '  df_typeref_2 = df_typeref\n'
    mkb__mayxr += '  check_java_installation(fname)\n'
    mkb__mayxr += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    mkb__mayxr += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    mkb__mayxr += (
        '  f_reader = bodo.ir.json_ext.json_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    mkb__mayxr += (
        """    {}, {}, -1, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py )
"""
        .format(lines, parallel, compression))
    mkb__mayxr += '  bodo.utils.utils.check_and_propagate_cpp_exception()\n'
    mkb__mayxr += '  if bodo.utils.utils.is_null_pointer(f_reader):\n'
    mkb__mayxr += "      raise FileNotFoundError('File does not exist')\n"
    mkb__mayxr += f'  with objmode({ptnv__owc}):\n'
    mkb__mayxr += f"    df = pd.read_json(f_reader, orient='{orient}',\n"
    mkb__mayxr += f'       convert_dates = {convert_dates}, \n'
    mkb__mayxr += f'       precise_float={precise_float}, \n'
    mkb__mayxr += f'       lines={lines}, \n'
    mkb__mayxr += '       dtype={{{}}},\n'.format(omp__amrr)
    mkb__mayxr += '       )\n'
    mkb__mayxr += (
        '    bodo.ir.connector.cast_float_to_nullable(df, df_typeref_2)\n')
    for ruq__wfna, ytya__vysn in zip(diupg__nytqo, col_names):
        mkb__mayxr += '    if len(df) > 0:\n'
        mkb__mayxr += "        {} = df['{}'].values\n".format(ruq__wfna,
            ytya__vysn)
        mkb__mayxr += '    else:\n'
        mkb__mayxr += '        {} = np.array([])\n'.format(ruq__wfna)
    mkb__mayxr += '  return ({},)\n'.format(', '.join(bojz__gats for
        bojz__gats in diupg__nytqo))
    cbl__cnim = globals()
    cbl__cnim.update({'bodo': bodo, 'pd': pd, 'np': np, 'objmode': objmode,
        'check_java_installation': check_java_installation, 'df_typeref':
        bodo.DataFrameType(tuple(col_typs), bodo.RangeIndexType(None),
        tuple(col_names)), 'get_storage_options_pyobject':
        get_storage_options_pyobject})
    zuxia__atzo = {}
    exec(mkb__mayxr, cbl__cnim, zuxia__atzo)
    gjr__fnv = zuxia__atzo['json_reader_py']
    yzj__vfa = numba.njit(gjr__fnv)
    compiled_funcs.append(yzj__vfa)
    return yzj__vfa
