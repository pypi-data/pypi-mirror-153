"""
Class information for DataFrame iterators returned by pd.read_csv. This is used
to handle situations in which pd.read_csv is used to return chunks with separate
read calls instead of just a single read.
"""
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, ir_utils, types
from numba.core.imputils import RefType, impl_ret_borrowed, iternext_impl
from numba.core.typing.templates import signature
from numba.extending import intrinsic, lower_builtin, models, register_model
import bodo
import bodo.ir.connector
import bodo.ir.csv_ext
from bodo import objmode
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.table import Table, TableType
from bodo.io import csv_cpp
from bodo.ir.csv_ext import _gen_read_csv_objmode, astype
from bodo.utils.utils import check_java_installation
from bodo.utils.utils import sanitize_varname
ll.add_symbol('update_csv_reader', csv_cpp.update_csv_reader)
ll.add_symbol('initialize_csv_reader', csv_cpp.initialize_csv_reader)


class CSVIteratorType(types.SimpleIteratorType):

    def __init__(self, df_type, out_colnames, out_types, usecols, sep,
        index_ind, index_arr_typ, index_name, escapechar, storage_options):
        assert isinstance(df_type, DataFrameType
            ), 'CSVIterator must return a DataFrame'
        unj__yhi = (
            f'CSVIteratorType({df_type}, {out_colnames}, {out_types}, {usecols}, {sep}, {index_ind}, {index_arr_typ}, {index_name}, {escapechar})'
            )
        super(types.SimpleIteratorType, self).__init__(unj__yhi)
        self._yield_type = df_type
        self._out_colnames = out_colnames
        self._out_types = out_types
        self._usecols = usecols
        self._sep = sep
        self._index_ind = index_ind
        self._index_arr_typ = index_arr_typ
        self._index_name = index_name
        self._escapechar = escapechar
        self._storage_options = storage_options

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(CSVIteratorType)
class CSVIteratorModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        eafur__dbra = [('csv_reader', bodo.ir.connector.stream_reader_type),
            ('index', types.EphemeralPointer(types.uintp))]
        super(CSVIteratorModel, self).__init__(dmm, fe_type, eafur__dbra)


@lower_builtin('getiter', CSVIteratorType)
def getiter_csv_iterator(context, builder, sig, args):
    wihew__red = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    wwhwa__eob = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer()]
        )
    lzoi__zccfl = cgutils.get_or_insert_function(builder.module, wwhwa__eob,
        name='initialize_csv_reader')
    builder.call(lzoi__zccfl, [wihew__red.csv_reader])
    builder.store(context.get_constant(types.uint64, 0), wihew__red.index)
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', CSVIteratorType)
@iternext_impl(RefType.NEW)
def iternext_csv_iterator(context, builder, sig, args, result):
    [fojl__dfur] = sig.args
    [rqskp__rio] = args
    wihew__red = cgutils.create_struct_proxy(fojl__dfur)(context, builder,
        value=rqskp__rio)
    wwhwa__eob = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer()]
        )
    lzoi__zccfl = cgutils.get_or_insert_function(builder.module, wwhwa__eob,
        name='update_csv_reader')
    ofcw__jteng = builder.call(lzoi__zccfl, [wihew__red.csv_reader])
    result.set_valid(ofcw__jteng)
    with builder.if_then(ofcw__jteng):
        vew__ooygo = builder.load(wihew__red.index)
        oxzyr__mawcf = types.Tuple([sig.return_type.first_type, types.int64])
        cfwrk__gnap = gen_read_csv_objmode(sig.args[0])
        cvaiv__xlaor = signature(oxzyr__mawcf, bodo.ir.connector.
            stream_reader_type, types.int64)
        hdap__lwdpu = context.compile_internal(builder, cfwrk__gnap,
            cvaiv__xlaor, [wihew__red.csv_reader, vew__ooygo])
        mqvrh__spc, adh__hzxys = cgutils.unpack_tuple(builder, hdap__lwdpu)
        qip__ynt = builder.add(vew__ooygo, adh__hzxys, flags=['nsw'])
        builder.store(qip__ynt, wihew__red.index)
        result.yield_(mqvrh__spc)


@intrinsic
def init_csv_iterator(typingctx, csv_reader, csv_iterator_typeref):

    def codegen(context, builder, signature, args):
        iww__mov = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        iww__mov.csv_reader = args[0]
        mmhj__trz = context.get_constant(types.uintp, 0)
        iww__mov.index = cgutils.alloca_once_value(builder, mmhj__trz)
        return iww__mov._getvalue()
    assert isinstance(csv_iterator_typeref, types.TypeRef
        ), 'Initializing a csv iterator requires a typeref'
    nzvlj__kgna = csv_iterator_typeref.instance_type
    sig = signature(nzvlj__kgna, csv_reader, csv_iterator_typeref)
    return sig, codegen


def gen_read_csv_objmode(csv_iterator_type):
    zzxew__dxcvp = 'def read_csv_objmode(f_reader):\n'
    cnqp__spyin = [sanitize_varname(detoi__qqfxl) for detoi__qqfxl in
        csv_iterator_type._out_colnames]
    bqnr__dvwy = ir_utils.next_label()
    wbtu__bfta = globals()
    out_types = csv_iterator_type._out_types
    wbtu__bfta[f'table_type_{bqnr__dvwy}'] = TableType(tuple(out_types))
    wbtu__bfta[f'idx_array_typ'] = csv_iterator_type._index_arr_typ
    wrvtn__san = list(range(len(csv_iterator_type._usecols)))
    zzxew__dxcvp += _gen_read_csv_objmode(csv_iterator_type._out_colnames,
        cnqp__spyin, out_types, csv_iterator_type._usecols, wrvtn__san,
        csv_iterator_type._sep, csv_iterator_type._escapechar,
        csv_iterator_type._storage_options, bqnr__dvwy, wbtu__bfta,
        parallel=False, check_parallel_runtime=True, idx_col_index=
        csv_iterator_type._index_ind, idx_col_typ=csv_iterator_type.
        _index_arr_typ)
    aqtnf__yfvo = bodo.ir.csv_ext._gen_parallel_flag_name(cnqp__spyin)
    eghx__pbhd = ['T'] + (['idx_arr'] if csv_iterator_type._index_ind is not
        None else []) + [aqtnf__yfvo]
    zzxew__dxcvp += f"  return {', '.join(eghx__pbhd)}"
    wbtu__bfta = globals()
    ari__oqb = {}
    exec(zzxew__dxcvp, wbtu__bfta, ari__oqb)
    uyv__rpejl = ari__oqb['read_csv_objmode']
    yii__cggw = numba.njit(uyv__rpejl)
    bodo.ir.csv_ext.compiled_funcs.append(yii__cggw)
    nyesr__njtgd = 'def read_func(reader, local_start):\n'
    nyesr__njtgd += f"  {', '.join(eghx__pbhd)} = objmode_func(reader)\n"
    index_ind = csv_iterator_type._index_ind
    if index_ind is None:
        nyesr__njtgd += f'  local_len = len(T)\n'
        nyesr__njtgd += '  total_size = local_len\n'
        nyesr__njtgd += f'  if ({aqtnf__yfvo}):\n'
        nyesr__njtgd += """    local_start = local_start + bodo.libs.distributed_api.dist_exscan(local_len, _op)
"""
        nyesr__njtgd += (
            '    total_size = bodo.libs.distributed_api.dist_reduce(local_len, _op)\n'
            )
        xiz__ikozt = (
            f'bodo.hiframes.pd_index_ext.init_range_index(local_start, local_start + local_len, 1, None)'
            )
    else:
        nyesr__njtgd += '  total_size = 0\n'
        xiz__ikozt = (
            f'bodo.utils.conversion.convert_to_index({eghx__pbhd[1]}, {csv_iterator_type._index_name!r})'
            )
    nyesr__njtgd += f"""  return (bodo.hiframes.pd_dataframe_ext.init_dataframe(({eghx__pbhd[0]},), {xiz__ikozt}, out_df_typ), total_size)
"""
    exec(nyesr__njtgd, {'bodo': bodo, 'objmode_func': yii__cggw, '_op': np.
        int32(bodo.libs.distributed_api.Reduce_Type.Sum.value),
        'out_df_typ': csv_iterator_type.yield_type}, ari__oqb)
    return ari__oqb['read_func']
