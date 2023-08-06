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
    mmqq__qnq = []
    ybm__vnqe = []
    cjibn__dir = []
    for snv__duibp, qugy__mgw in enumerate(json_node.out_vars):
        if qugy__mgw.name in lives:
            mmqq__qnq.append(json_node.df_colnames[snv__duibp])
            ybm__vnqe.append(json_node.out_vars[snv__duibp])
            cjibn__dir.append(json_node.out_types[snv__duibp])
    json_node.df_colnames = mmqq__qnq
    json_node.out_vars = ybm__vnqe
    json_node.out_types = cjibn__dir
    if len(json_node.out_vars) == 0:
        return None
    return json_node


def json_distributed_run(json_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 1:
        pdwo__clud = (
            'Finish column pruning on read_json node:\n%s\nColumns loaded %s\n'
            )
        zaby__uvni = json_node.loc.strformat()
        amlx__ojkw = json_node.df_colnames
        bodo.user_logging.log_message('Column Pruning', pdwo__clud,
            zaby__uvni, amlx__ojkw)
        xbdx__dhc = [aes__pbik for snv__duibp, aes__pbik in enumerate(
            json_node.df_colnames) if isinstance(json_node.out_types[
            snv__duibp], bodo.libs.dict_arr_ext.DictionaryArrayType)]
        if xbdx__dhc:
            ifao__umfvx = """Finished optimized encoding on read_json node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                ifao__umfvx, zaby__uvni, xbdx__dhc)
    parallel = False
    if array_dists is not None:
        parallel = True
        for irjg__vjjol in json_node.out_vars:
            if array_dists[irjg__vjjol.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                irjg__vjjol.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    brx__owovx = len(json_node.out_vars)
    zoph__xnaj = ', '.join('arr' + str(snv__duibp) for snv__duibp in range(
        brx__owovx))
    jwzfe__eysy = 'def json_impl(fname):\n'
    jwzfe__eysy += '    ({},) = _json_reader_py(fname)\n'.format(zoph__xnaj)
    ttylz__axgg = {}
    exec(jwzfe__eysy, {}, ttylz__axgg)
    dha__zhhj = ttylz__axgg['json_impl']
    uivux__ftf = _gen_json_reader_py(json_node.df_colnames, json_node.
        out_types, typingctx, targetctx, parallel, json_node.orient,
        json_node.convert_dates, json_node.precise_float, json_node.lines,
        json_node.compression, json_node.storage_options)
    rtrpi__jol = compile_to_numba_ir(dha__zhhj, {'_json_reader_py':
        uivux__ftf}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type,), typemap=typemap, calltypes=calltypes).blocks.popitem()[1
        ]
    replace_arg_nodes(rtrpi__jol, [json_node.file_name])
    gaz__kym = rtrpi__jol.body[:-3]
    for snv__duibp in range(len(json_node.out_vars)):
        gaz__kym[-len(json_node.out_vars) + snv__duibp
            ].target = json_node.out_vars[snv__duibp]
    return gaz__kym


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
    xkbzj__crcz = [sanitize_varname(aes__pbik) for aes__pbik in col_names]
    ohrcq__rmbu = ', '.join(str(snv__duibp) for snv__duibp, andf__xsg in
        enumerate(col_typs) if andf__xsg.dtype == types.NPDatetime('ns'))
    nht__eym = ', '.join(["{}='{}'".format(mqjen__qztp, bodo.ir.csv_ext.
        _get_dtype_str(andf__xsg)) for mqjen__qztp, andf__xsg in zip(
        xkbzj__crcz, col_typs)])
    rwex__wxr = ', '.join(["'{}':{}".format(vuj__hzd, bodo.ir.csv_ext.
        _get_pd_dtype_str(andf__xsg)) for vuj__hzd, andf__xsg in zip(
        col_names, col_typs)])
    if compression is None:
        compression = 'uncompressed'
    jwzfe__eysy = 'def json_reader_py(fname):\n'
    jwzfe__eysy += '  df_typeref_2 = df_typeref\n'
    jwzfe__eysy += '  check_java_installation(fname)\n'
    jwzfe__eysy += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    jwzfe__eysy += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    jwzfe__eysy += (
        '  f_reader = bodo.ir.json_ext.json_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    jwzfe__eysy += (
        """    {}, {}, -1, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py )
"""
        .format(lines, parallel, compression))
    jwzfe__eysy += '  bodo.utils.utils.check_and_propagate_cpp_exception()\n'
    jwzfe__eysy += '  if bodo.utils.utils.is_null_pointer(f_reader):\n'
    jwzfe__eysy += "      raise FileNotFoundError('File does not exist')\n"
    jwzfe__eysy += f'  with objmode({nht__eym}):\n'
    jwzfe__eysy += f"    df = pd.read_json(f_reader, orient='{orient}',\n"
    jwzfe__eysy += f'       convert_dates = {convert_dates}, \n'
    jwzfe__eysy += f'       precise_float={precise_float}, \n'
    jwzfe__eysy += f'       lines={lines}, \n'
    jwzfe__eysy += '       dtype={{{}}},\n'.format(rwex__wxr)
    jwzfe__eysy += '       )\n'
    jwzfe__eysy += (
        '    bodo.ir.connector.cast_float_to_nullable(df, df_typeref_2)\n')
    for mqjen__qztp, vuj__hzd in zip(xkbzj__crcz, col_names):
        jwzfe__eysy += '    if len(df) > 0:\n'
        jwzfe__eysy += "        {} = df['{}'].values\n".format(mqjen__qztp,
            vuj__hzd)
        jwzfe__eysy += '    else:\n'
        jwzfe__eysy += '        {} = np.array([])\n'.format(mqjen__qztp)
    jwzfe__eysy += '  return ({},)\n'.format(', '.join(eojmw__sumh for
        eojmw__sumh in xkbzj__crcz))
    wszlc__axf = globals()
    wszlc__axf.update({'bodo': bodo, 'pd': pd, 'np': np, 'objmode': objmode,
        'check_java_installation': check_java_installation, 'df_typeref':
        bodo.DataFrameType(tuple(col_typs), bodo.RangeIndexType(None),
        tuple(col_names)), 'get_storage_options_pyobject':
        get_storage_options_pyobject})
    ttylz__axgg = {}
    exec(jwzfe__eysy, wszlc__axf, ttylz__axgg)
    uivux__ftf = ttylz__axgg['json_reader_py']
    fvh__dqw = numba.njit(uivux__ftf)
    compiled_funcs.append(fvh__dqw)
    return fvh__dqw
