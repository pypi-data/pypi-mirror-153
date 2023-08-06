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
    ollyj__job = []
    qtur__uwg = []
    twlsx__dsq = []
    for rceds__aybh, artpi__nbyh in enumerate(json_node.out_vars):
        if artpi__nbyh.name in lives:
            ollyj__job.append(json_node.df_colnames[rceds__aybh])
            qtur__uwg.append(json_node.out_vars[rceds__aybh])
            twlsx__dsq.append(json_node.out_types[rceds__aybh])
    json_node.df_colnames = ollyj__job
    json_node.out_vars = qtur__uwg
    json_node.out_types = twlsx__dsq
    if len(json_node.out_vars) == 0:
        return None
    return json_node


def json_distributed_run(json_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 1:
        vcoe__ptk = (
            'Finish column pruning on read_json node:\n%s\nColumns loaded %s\n'
            )
        djy__rnl = json_node.loc.strformat()
        evwxp__itgx = json_node.df_colnames
        bodo.user_logging.log_message('Column Pruning', vcoe__ptk, djy__rnl,
            evwxp__itgx)
        uwzv__thwbu = [kffo__xzqc for rceds__aybh, kffo__xzqc in enumerate(
            json_node.df_colnames) if isinstance(json_node.out_types[
            rceds__aybh], bodo.libs.dict_arr_ext.DictionaryArrayType)]
        if uwzv__thwbu:
            vorgt__ugbpv = """Finished optimized encoding on read_json node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                vorgt__ugbpv, djy__rnl, uwzv__thwbu)
    parallel = False
    if array_dists is not None:
        parallel = True
        for mdxvr__eegm in json_node.out_vars:
            if array_dists[mdxvr__eegm.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                mdxvr__eegm.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    nvpa__svkc = len(json_node.out_vars)
    tqtkk__vthdi = ', '.join('arr' + str(rceds__aybh) for rceds__aybh in
        range(nvpa__svkc))
    vgxo__dvhg = 'def json_impl(fname):\n'
    vgxo__dvhg += '    ({},) = _json_reader_py(fname)\n'.format(tqtkk__vthdi)
    skhau__npue = {}
    exec(vgxo__dvhg, {}, skhau__npue)
    qgbyx__jkdmr = skhau__npue['json_impl']
    zbjdf__trkob = _gen_json_reader_py(json_node.df_colnames, json_node.
        out_types, typingctx, targetctx, parallel, json_node.orient,
        json_node.convert_dates, json_node.precise_float, json_node.lines,
        json_node.compression, json_node.storage_options)
    dqgki__zrkem = compile_to_numba_ir(qgbyx__jkdmr, {'_json_reader_py':
        zbjdf__trkob}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type,), typemap=typemap, calltypes=calltypes).blocks.popitem()[1
        ]
    replace_arg_nodes(dqgki__zrkem, [json_node.file_name])
    aez__ithks = dqgki__zrkem.body[:-3]
    for rceds__aybh in range(len(json_node.out_vars)):
        aez__ithks[-len(json_node.out_vars) + rceds__aybh
            ].target = json_node.out_vars[rceds__aybh]
    return aez__ithks


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
    aczm__sywij = [sanitize_varname(kffo__xzqc) for kffo__xzqc in col_names]
    fgs__iolw = ', '.join(str(rceds__aybh) for rceds__aybh, mzaa__maf in
        enumerate(col_typs) if mzaa__maf.dtype == types.NPDatetime('ns'))
    wlb__yjphr = ', '.join(["{}='{}'".format(deiy__kqypa, bodo.ir.csv_ext.
        _get_dtype_str(mzaa__maf)) for deiy__kqypa, mzaa__maf in zip(
        aczm__sywij, col_typs)])
    qmps__vtvyn = ', '.join(["'{}':{}".format(nynl__ljza, bodo.ir.csv_ext.
        _get_pd_dtype_str(mzaa__maf)) for nynl__ljza, mzaa__maf in zip(
        col_names, col_typs)])
    if compression is None:
        compression = 'uncompressed'
    vgxo__dvhg = 'def json_reader_py(fname):\n'
    vgxo__dvhg += '  df_typeref_2 = df_typeref\n'
    vgxo__dvhg += '  check_java_installation(fname)\n'
    vgxo__dvhg += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    vgxo__dvhg += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    vgxo__dvhg += (
        '  f_reader = bodo.ir.json_ext.json_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    vgxo__dvhg += (
        """    {}, {}, -1, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py )
"""
        .format(lines, parallel, compression))
    vgxo__dvhg += '  bodo.utils.utils.check_and_propagate_cpp_exception()\n'
    vgxo__dvhg += '  if bodo.utils.utils.is_null_pointer(f_reader):\n'
    vgxo__dvhg += "      raise FileNotFoundError('File does not exist')\n"
    vgxo__dvhg += f'  with objmode({wlb__yjphr}):\n'
    vgxo__dvhg += f"    df = pd.read_json(f_reader, orient='{orient}',\n"
    vgxo__dvhg += f'       convert_dates = {convert_dates}, \n'
    vgxo__dvhg += f'       precise_float={precise_float}, \n'
    vgxo__dvhg += f'       lines={lines}, \n'
    vgxo__dvhg += '       dtype={{{}}},\n'.format(qmps__vtvyn)
    vgxo__dvhg += '       )\n'
    vgxo__dvhg += (
        '    bodo.ir.connector.cast_float_to_nullable(df, df_typeref_2)\n')
    for deiy__kqypa, nynl__ljza in zip(aczm__sywij, col_names):
        vgxo__dvhg += '    if len(df) > 0:\n'
        vgxo__dvhg += "        {} = df['{}'].values\n".format(deiy__kqypa,
            nynl__ljza)
        vgxo__dvhg += '    else:\n'
        vgxo__dvhg += '        {} = np.array([])\n'.format(deiy__kqypa)
    vgxo__dvhg += '  return ({},)\n'.format(', '.join(tftq__txifl for
        tftq__txifl in aczm__sywij))
    vkip__nqfk = globals()
    vkip__nqfk.update({'bodo': bodo, 'pd': pd, 'np': np, 'objmode': objmode,
        'check_java_installation': check_java_installation, 'df_typeref':
        bodo.DataFrameType(tuple(col_typs), bodo.RangeIndexType(None),
        tuple(col_names)), 'get_storage_options_pyobject':
        get_storage_options_pyobject})
    skhau__npue = {}
    exec(vgxo__dvhg, vkip__nqfk, skhau__npue)
    zbjdf__trkob = skhau__npue['json_reader_py']
    kml__amupf = numba.njit(zbjdf__trkob)
    compiled_funcs.append(kml__amupf)
    return kml__amupf
