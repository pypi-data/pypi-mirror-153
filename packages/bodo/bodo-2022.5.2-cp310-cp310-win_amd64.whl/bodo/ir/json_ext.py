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
    qzkoy__sgm = []
    zenhi__jmegd = []
    ngjhi__cvr = []
    for ijste__qstuc, xdfar__cdhzv in enumerate(json_node.out_vars):
        if xdfar__cdhzv.name in lives:
            qzkoy__sgm.append(json_node.df_colnames[ijste__qstuc])
            zenhi__jmegd.append(json_node.out_vars[ijste__qstuc])
            ngjhi__cvr.append(json_node.out_types[ijste__qstuc])
    json_node.df_colnames = qzkoy__sgm
    json_node.out_vars = zenhi__jmegd
    json_node.out_types = ngjhi__cvr
    if len(json_node.out_vars) == 0:
        return None
    return json_node


def json_distributed_run(json_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 1:
        uvx__fgk = (
            'Finish column pruning on read_json node:\n%s\nColumns loaded %s\n'
            )
        iijs__bki = json_node.loc.strformat()
        jptp__dyk = json_node.df_colnames
        bodo.user_logging.log_message('Column Pruning', uvx__fgk, iijs__bki,
            jptp__dyk)
        brrg__cim = [eahm__zukm for ijste__qstuc, eahm__zukm in enumerate(
            json_node.df_colnames) if isinstance(json_node.out_types[
            ijste__qstuc], bodo.libs.dict_arr_ext.DictionaryArrayType)]
        if brrg__cim:
            ckpo__xxwxl = """Finished optimized encoding on read_json node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                ckpo__xxwxl, iijs__bki, brrg__cim)
    parallel = False
    if array_dists is not None:
        parallel = True
        for gxkx__aana in json_node.out_vars:
            if array_dists[gxkx__aana.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                gxkx__aana.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    zlavo__pki = len(json_node.out_vars)
    apwz__gijfz = ', '.join('arr' + str(ijste__qstuc) for ijste__qstuc in
        range(zlavo__pki))
    xqkia__xyj = 'def json_impl(fname):\n'
    xqkia__xyj += '    ({},) = _json_reader_py(fname)\n'.format(apwz__gijfz)
    oxlb__bodb = {}
    exec(xqkia__xyj, {}, oxlb__bodb)
    kez__aytt = oxlb__bodb['json_impl']
    ctnk__jhim = _gen_json_reader_py(json_node.df_colnames, json_node.
        out_types, typingctx, targetctx, parallel, json_node.orient,
        json_node.convert_dates, json_node.precise_float, json_node.lines,
        json_node.compression, json_node.storage_options)
    kwvgs__uebp = compile_to_numba_ir(kez__aytt, {'_json_reader_py':
        ctnk__jhim}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type,), typemap=typemap, calltypes=calltypes).blocks.popitem()[1
        ]
    replace_arg_nodes(kwvgs__uebp, [json_node.file_name])
    pzk__filf = kwvgs__uebp.body[:-3]
    for ijste__qstuc in range(len(json_node.out_vars)):
        pzk__filf[-len(json_node.out_vars) + ijste__qstuc
            ].target = json_node.out_vars[ijste__qstuc]
    return pzk__filf


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
    hgj__smbgc = [sanitize_varname(eahm__zukm) for eahm__zukm in col_names]
    ijkxp__ths = ', '.join(str(ijste__qstuc) for ijste__qstuc, evif__kurd in
        enumerate(col_typs) if evif__kurd.dtype == types.NPDatetime('ns'))
    sviq__aulu = ', '.join(["{}='{}'".format(yspxz__kqle, bodo.ir.csv_ext.
        _get_dtype_str(evif__kurd)) for yspxz__kqle, evif__kurd in zip(
        hgj__smbgc, col_typs)])
    nnldw__jua = ', '.join(["'{}':{}".format(mdi__tca, bodo.ir.csv_ext.
        _get_pd_dtype_str(evif__kurd)) for mdi__tca, evif__kurd in zip(
        col_names, col_typs)])
    if compression is None:
        compression = 'uncompressed'
    xqkia__xyj = 'def json_reader_py(fname):\n'
    xqkia__xyj += '  df_typeref_2 = df_typeref\n'
    xqkia__xyj += '  check_java_installation(fname)\n'
    xqkia__xyj += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    xqkia__xyj += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    xqkia__xyj += (
        '  f_reader = bodo.ir.json_ext.json_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    xqkia__xyj += (
        """    {}, {}, -1, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py )
"""
        .format(lines, parallel, compression))
    xqkia__xyj += '  bodo.utils.utils.check_and_propagate_cpp_exception()\n'
    xqkia__xyj += '  if bodo.utils.utils.is_null_pointer(f_reader):\n'
    xqkia__xyj += "      raise FileNotFoundError('File does not exist')\n"
    xqkia__xyj += f'  with objmode({sviq__aulu}):\n'
    xqkia__xyj += f"    df = pd.read_json(f_reader, orient='{orient}',\n"
    xqkia__xyj += f'       convert_dates = {convert_dates}, \n'
    xqkia__xyj += f'       precise_float={precise_float}, \n'
    xqkia__xyj += f'       lines={lines}, \n'
    xqkia__xyj += '       dtype={{{}}},\n'.format(nnldw__jua)
    xqkia__xyj += '       )\n'
    xqkia__xyj += (
        '    bodo.ir.connector.cast_float_to_nullable(df, df_typeref_2)\n')
    for yspxz__kqle, mdi__tca in zip(hgj__smbgc, col_names):
        xqkia__xyj += '    if len(df) > 0:\n'
        xqkia__xyj += "        {} = df['{}'].values\n".format(yspxz__kqle,
            mdi__tca)
        xqkia__xyj += '    else:\n'
        xqkia__xyj += '        {} = np.array([])\n'.format(yspxz__kqle)
    xqkia__xyj += '  return ({},)\n'.format(', '.join(lyxnw__mheda for
        lyxnw__mheda in hgj__smbgc))
    nurt__hgw = globals()
    nurt__hgw.update({'bodo': bodo, 'pd': pd, 'np': np, 'objmode': objmode,
        'check_java_installation': check_java_installation, 'df_typeref':
        bodo.DataFrameType(tuple(col_typs), bodo.RangeIndexType(None),
        tuple(col_names)), 'get_storage_options_pyobject':
        get_storage_options_pyobject})
    oxlb__bodb = {}
    exec(xqkia__xyj, nurt__hgw, oxlb__bodb)
    ctnk__jhim = oxlb__bodb['json_reader_py']
    hfd__hpo = numba.njit(ctnk__jhim)
    compiled_funcs.append(hfd__hpo)
    return hfd__hpo
