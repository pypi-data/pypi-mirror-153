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
        hxc__dsefy = (
            f'CSVIteratorType({df_type}, {out_colnames}, {out_types}, {usecols}, {sep}, {index_ind}, {index_arr_typ}, {index_name}, {escapechar})'
            )
        super(types.SimpleIteratorType, self).__init__(hxc__dsefy)
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
        gaqy__cbwq = [('csv_reader', bodo.ir.connector.stream_reader_type),
            ('index', types.EphemeralPointer(types.uintp))]
        super(CSVIteratorModel, self).__init__(dmm, fe_type, gaqy__cbwq)


@lower_builtin('getiter', CSVIteratorType)
def getiter_csv_iterator(context, builder, sig, args):
    ymra__ctn = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    gtml__hbe = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer()])
    dafoy__ick = cgutils.get_or_insert_function(builder.module, gtml__hbe,
        name='initialize_csv_reader')
    builder.call(dafoy__ick, [ymra__ctn.csv_reader])
    builder.store(context.get_constant(types.uint64, 0), ymra__ctn.index)
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', CSVIteratorType)
@iternext_impl(RefType.NEW)
def iternext_csv_iterator(context, builder, sig, args, result):
    [chqkb__kkcbs] = sig.args
    [forjp__jgbhq] = args
    ymra__ctn = cgutils.create_struct_proxy(chqkb__kkcbs)(context, builder,
        value=forjp__jgbhq)
    gtml__hbe = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer()])
    dafoy__ick = cgutils.get_or_insert_function(builder.module, gtml__hbe,
        name='update_csv_reader')
    djg__vhb = builder.call(dafoy__ick, [ymra__ctn.csv_reader])
    result.set_valid(djg__vhb)
    with builder.if_then(djg__vhb):
        gbofw__tviws = builder.load(ymra__ctn.index)
        mser__kmzh = types.Tuple([sig.return_type.first_type, types.int64])
        arcfb__hwd = gen_read_csv_objmode(sig.args[0])
        gqnl__fotog = signature(mser__kmzh, bodo.ir.connector.
            stream_reader_type, types.int64)
        jhdo__kdg = context.compile_internal(builder, arcfb__hwd,
            gqnl__fotog, [ymra__ctn.csv_reader, gbofw__tviws])
        sza__udfb, eqqhm__sexvr = cgutils.unpack_tuple(builder, jhdo__kdg)
        kpx__pxuo = builder.add(gbofw__tviws, eqqhm__sexvr, flags=['nsw'])
        builder.store(kpx__pxuo, ymra__ctn.index)
        result.yield_(sza__udfb)


@intrinsic
def init_csv_iterator(typingctx, csv_reader, csv_iterator_typeref):

    def codegen(context, builder, signature, args):
        zfkny__bqwhf = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        zfkny__bqwhf.csv_reader = args[0]
        jdwqz__lnz = context.get_constant(types.uintp, 0)
        zfkny__bqwhf.index = cgutils.alloca_once_value(builder, jdwqz__lnz)
        return zfkny__bqwhf._getvalue()
    assert isinstance(csv_iterator_typeref, types.TypeRef
        ), 'Initializing a csv iterator requires a typeref'
    fgaam__ptr = csv_iterator_typeref.instance_type
    sig = signature(fgaam__ptr, csv_reader, csv_iterator_typeref)
    return sig, codegen


def gen_read_csv_objmode(csv_iterator_type):
    gpkjl__qcbu = 'def read_csv_objmode(f_reader):\n'
    auo__zhwdv = [sanitize_varname(jhi__tlg) for jhi__tlg in
        csv_iterator_type._out_colnames]
    ggkg__xdfaa = ir_utils.next_label()
    yvcv__owyqh = globals()
    out_types = csv_iterator_type._out_types
    yvcv__owyqh[f'table_type_{ggkg__xdfaa}'] = TableType(tuple(out_types))
    yvcv__owyqh[f'idx_array_typ'] = csv_iterator_type._index_arr_typ
    upck__ygamh = list(range(len(csv_iterator_type._usecols)))
    gpkjl__qcbu += _gen_read_csv_objmode(csv_iterator_type._out_colnames,
        auo__zhwdv, out_types, csv_iterator_type._usecols, upck__ygamh,
        csv_iterator_type._sep, csv_iterator_type._escapechar,
        csv_iterator_type._storage_options, ggkg__xdfaa, yvcv__owyqh,
        parallel=False, check_parallel_runtime=True, idx_col_index=
        csv_iterator_type._index_ind, idx_col_typ=csv_iterator_type.
        _index_arr_typ)
    swott__vyf = bodo.ir.csv_ext._gen_parallel_flag_name(auo__zhwdv)
    qdacz__ewm = ['T'] + (['idx_arr'] if csv_iterator_type._index_ind is not
        None else []) + [swott__vyf]
    gpkjl__qcbu += f"  return {', '.join(qdacz__ewm)}"
    yvcv__owyqh = globals()
    lvsn__xnu = {}
    exec(gpkjl__qcbu, yvcv__owyqh, lvsn__xnu)
    eupwf__vlojf = lvsn__xnu['read_csv_objmode']
    uoi__yibn = numba.njit(eupwf__vlojf)
    bodo.ir.csv_ext.compiled_funcs.append(uoi__yibn)
    ehzg__drzy = 'def read_func(reader, local_start):\n'
    ehzg__drzy += f"  {', '.join(qdacz__ewm)} = objmode_func(reader)\n"
    index_ind = csv_iterator_type._index_ind
    if index_ind is None:
        ehzg__drzy += f'  local_len = len(T)\n'
        ehzg__drzy += '  total_size = local_len\n'
        ehzg__drzy += f'  if ({swott__vyf}):\n'
        ehzg__drzy += """    local_start = local_start + bodo.libs.distributed_api.dist_exscan(local_len, _op)
"""
        ehzg__drzy += (
            '    total_size = bodo.libs.distributed_api.dist_reduce(local_len, _op)\n'
            )
        chh__bcix = (
            f'bodo.hiframes.pd_index_ext.init_range_index(local_start, local_start + local_len, 1, None)'
            )
    else:
        ehzg__drzy += '  total_size = 0\n'
        chh__bcix = (
            f'bodo.utils.conversion.convert_to_index({qdacz__ewm[1]}, {csv_iterator_type._index_name!r})'
            )
    ehzg__drzy += f"""  return (bodo.hiframes.pd_dataframe_ext.init_dataframe(({qdacz__ewm[0]},), {chh__bcix}, out_df_typ), total_size)
"""
    exec(ehzg__drzy, {'bodo': bodo, 'objmode_func': uoi__yibn, '_op': np.
        int32(bodo.libs.distributed_api.Reduce_Type.Sum.value),
        'out_df_typ': csv_iterator_type.yield_type}, lvsn__xnu)
    return lvsn__xnu['read_func']
