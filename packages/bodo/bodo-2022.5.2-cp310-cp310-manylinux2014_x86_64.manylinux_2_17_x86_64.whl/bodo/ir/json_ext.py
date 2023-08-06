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
    wtsmx__mqyae = []
    idvul__dykg = []
    pkf__qgppq = []
    for yaos__tcmxc, tglwy__ypt in enumerate(json_node.out_vars):
        if tglwy__ypt.name in lives:
            wtsmx__mqyae.append(json_node.df_colnames[yaos__tcmxc])
            idvul__dykg.append(json_node.out_vars[yaos__tcmxc])
            pkf__qgppq.append(json_node.out_types[yaos__tcmxc])
    json_node.df_colnames = wtsmx__mqyae
    json_node.out_vars = idvul__dykg
    json_node.out_types = pkf__qgppq
    if len(json_node.out_vars) == 0:
        return None
    return json_node


def json_distributed_run(json_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 1:
        rsuy__kaios = (
            'Finish column pruning on read_json node:\n%s\nColumns loaded %s\n'
            )
        osqw__gkipp = json_node.loc.strformat()
        dagk__sgrgi = json_node.df_colnames
        bodo.user_logging.log_message('Column Pruning', rsuy__kaios,
            osqw__gkipp, dagk__sgrgi)
        isqd__riiwu = [uvroy__kiuda for yaos__tcmxc, uvroy__kiuda in
            enumerate(json_node.df_colnames) if isinstance(json_node.
            out_types[yaos__tcmxc], bodo.libs.dict_arr_ext.DictionaryArrayType)
            ]
        if isqd__riiwu:
            qvdjb__bpwnb = """Finished optimized encoding on read_json node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                qvdjb__bpwnb, osqw__gkipp, isqd__riiwu)
    parallel = False
    if array_dists is not None:
        parallel = True
        for cpulq__hkbin in json_node.out_vars:
            if array_dists[cpulq__hkbin.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                cpulq__hkbin.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    woni__gudxx = len(json_node.out_vars)
    dvuu__gslla = ', '.join('arr' + str(yaos__tcmxc) for yaos__tcmxc in
        range(woni__gudxx))
    kjf__ord = 'def json_impl(fname):\n'
    kjf__ord += '    ({},) = _json_reader_py(fname)\n'.format(dvuu__gslla)
    ogn__mktbd = {}
    exec(kjf__ord, {}, ogn__mktbd)
    sqxfm__uee = ogn__mktbd['json_impl']
    reyn__qoqn = _gen_json_reader_py(json_node.df_colnames, json_node.
        out_types, typingctx, targetctx, parallel, json_node.orient,
        json_node.convert_dates, json_node.precise_float, json_node.lines,
        json_node.compression, json_node.storage_options)
    kql__gxwt = compile_to_numba_ir(sqxfm__uee, {'_json_reader_py':
        reyn__qoqn}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type,), typemap=typemap, calltypes=calltypes).blocks.popitem()[1
        ]
    replace_arg_nodes(kql__gxwt, [json_node.file_name])
    vjvt__qyr = kql__gxwt.body[:-3]
    for yaos__tcmxc in range(len(json_node.out_vars)):
        vjvt__qyr[-len(json_node.out_vars) + yaos__tcmxc
            ].target = json_node.out_vars[yaos__tcmxc]
    return vjvt__qyr


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
    jrlkb__bzw = [sanitize_varname(uvroy__kiuda) for uvroy__kiuda in col_names]
    zytm__bsgam = ', '.join(str(yaos__tcmxc) for yaos__tcmxc, bfsi__sjl in
        enumerate(col_typs) if bfsi__sjl.dtype == types.NPDatetime('ns'))
    hvkfx__ggn = ', '.join(["{}='{}'".format(vecov__kpx, bodo.ir.csv_ext.
        _get_dtype_str(bfsi__sjl)) for vecov__kpx, bfsi__sjl in zip(
        jrlkb__bzw, col_typs)])
    fxy__svcr = ', '.join(["'{}':{}".format(poi__ihmz, bodo.ir.csv_ext.
        _get_pd_dtype_str(bfsi__sjl)) for poi__ihmz, bfsi__sjl in zip(
        col_names, col_typs)])
    if compression is None:
        compression = 'uncompressed'
    kjf__ord = 'def json_reader_py(fname):\n'
    kjf__ord += '  df_typeref_2 = df_typeref\n'
    kjf__ord += '  check_java_installation(fname)\n'
    kjf__ord += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    kjf__ord += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    kjf__ord += (
        '  f_reader = bodo.ir.json_ext.json_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    kjf__ord += (
        """    {}, {}, -1, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py )
"""
        .format(lines, parallel, compression))
    kjf__ord += '  bodo.utils.utils.check_and_propagate_cpp_exception()\n'
    kjf__ord += '  if bodo.utils.utils.is_null_pointer(f_reader):\n'
    kjf__ord += "      raise FileNotFoundError('File does not exist')\n"
    kjf__ord += f'  with objmode({hvkfx__ggn}):\n'
    kjf__ord += f"    df = pd.read_json(f_reader, orient='{orient}',\n"
    kjf__ord += f'       convert_dates = {convert_dates}, \n'
    kjf__ord += f'       precise_float={precise_float}, \n'
    kjf__ord += f'       lines={lines}, \n'
    kjf__ord += '       dtype={{{}}},\n'.format(fxy__svcr)
    kjf__ord += '       )\n'
    kjf__ord += (
        '    bodo.ir.connector.cast_float_to_nullable(df, df_typeref_2)\n')
    for vecov__kpx, poi__ihmz in zip(jrlkb__bzw, col_names):
        kjf__ord += '    if len(df) > 0:\n'
        kjf__ord += "        {} = df['{}'].values\n".format(vecov__kpx,
            poi__ihmz)
        kjf__ord += '    else:\n'
        kjf__ord += '        {} = np.array([])\n'.format(vecov__kpx)
    kjf__ord += '  return ({},)\n'.format(', '.join(bkt__kqy for bkt__kqy in
        jrlkb__bzw))
    bggkr__gsmxl = globals()
    bggkr__gsmxl.update({'bodo': bodo, 'pd': pd, 'np': np, 'objmode':
        objmode, 'check_java_installation': check_java_installation,
        'df_typeref': bodo.DataFrameType(tuple(col_typs), bodo.
        RangeIndexType(None), tuple(col_names)),
        'get_storage_options_pyobject': get_storage_options_pyobject})
    ogn__mktbd = {}
    exec(kjf__ord, bggkr__gsmxl, ogn__mktbd)
    reyn__qoqn = ogn__mktbd['json_reader_py']
    csrty__iidg = numba.njit(reyn__qoqn)
    compiled_funcs.append(csrty__iidg)
    return csrty__iidg
