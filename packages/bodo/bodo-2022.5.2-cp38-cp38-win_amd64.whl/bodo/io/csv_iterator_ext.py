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
        dfty__lpxnj = (
            f'CSVIteratorType({df_type}, {out_colnames}, {out_types}, {usecols}, {sep}, {index_ind}, {index_arr_typ}, {index_name}, {escapechar})'
            )
        super(types.SimpleIteratorType, self).__init__(dfty__lpxnj)
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
        enpa__ytqbo = [('csv_reader', bodo.ir.connector.stream_reader_type),
            ('index', types.EphemeralPointer(types.uintp))]
        super(CSVIteratorModel, self).__init__(dmm, fe_type, enpa__ytqbo)


@lower_builtin('getiter', CSVIteratorType)
def getiter_csv_iterator(context, builder, sig, args):
    zkjx__qsxc = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    shq__xsypf = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer()]
        )
    puvle__nuv = cgutils.get_or_insert_function(builder.module, shq__xsypf,
        name='initialize_csv_reader')
    builder.call(puvle__nuv, [zkjx__qsxc.csv_reader])
    builder.store(context.get_constant(types.uint64, 0), zkjx__qsxc.index)
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', CSVIteratorType)
@iternext_impl(RefType.NEW)
def iternext_csv_iterator(context, builder, sig, args, result):
    [bdf__nmym] = sig.args
    [aof__dchix] = args
    zkjx__qsxc = cgutils.create_struct_proxy(bdf__nmym)(context, builder,
        value=aof__dchix)
    shq__xsypf = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer()]
        )
    puvle__nuv = cgutils.get_or_insert_function(builder.module, shq__xsypf,
        name='update_csv_reader')
    xiwko__vyau = builder.call(puvle__nuv, [zkjx__qsxc.csv_reader])
    result.set_valid(xiwko__vyau)
    with builder.if_then(xiwko__vyau):
        umf__fbp = builder.load(zkjx__qsxc.index)
        plb__vakla = types.Tuple([sig.return_type.first_type, types.int64])
        doj__cggm = gen_read_csv_objmode(sig.args[0])
        qvlld__hscpz = signature(plb__vakla, bodo.ir.connector.
            stream_reader_type, types.int64)
        yfa__ivlmb = context.compile_internal(builder, doj__cggm,
            qvlld__hscpz, [zkjx__qsxc.csv_reader, umf__fbp])
        jlx__pxis, ecx__gjfc = cgutils.unpack_tuple(builder, yfa__ivlmb)
        fgr__kjg = builder.add(umf__fbp, ecx__gjfc, flags=['nsw'])
        builder.store(fgr__kjg, zkjx__qsxc.index)
        result.yield_(jlx__pxis)


@intrinsic
def init_csv_iterator(typingctx, csv_reader, csv_iterator_typeref):

    def codegen(context, builder, signature, args):
        xwgi__tby = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        xwgi__tby.csv_reader = args[0]
        lqeo__ton = context.get_constant(types.uintp, 0)
        xwgi__tby.index = cgutils.alloca_once_value(builder, lqeo__ton)
        return xwgi__tby._getvalue()
    assert isinstance(csv_iterator_typeref, types.TypeRef
        ), 'Initializing a csv iterator requires a typeref'
    ycy__cxje = csv_iterator_typeref.instance_type
    sig = signature(ycy__cxje, csv_reader, csv_iterator_typeref)
    return sig, codegen


def gen_read_csv_objmode(csv_iterator_type):
    aajz__zcd = 'def read_csv_objmode(f_reader):\n'
    iosj__ylvqt = [sanitize_varname(rzyn__hwxx) for rzyn__hwxx in
        csv_iterator_type._out_colnames]
    bwlaz__srsqf = ir_utils.next_label()
    curks__purq = globals()
    out_types = csv_iterator_type._out_types
    curks__purq[f'table_type_{bwlaz__srsqf}'] = TableType(tuple(out_types))
    curks__purq[f'idx_array_typ'] = csv_iterator_type._index_arr_typ
    aph__nja = list(range(len(csv_iterator_type._usecols)))
    aajz__zcd += _gen_read_csv_objmode(csv_iterator_type._out_colnames,
        iosj__ylvqt, out_types, csv_iterator_type._usecols, aph__nja,
        csv_iterator_type._sep, csv_iterator_type._escapechar,
        csv_iterator_type._storage_options, bwlaz__srsqf, curks__purq,
        parallel=False, check_parallel_runtime=True, idx_col_index=
        csv_iterator_type._index_ind, idx_col_typ=csv_iterator_type.
        _index_arr_typ)
    pan__vlitw = bodo.ir.csv_ext._gen_parallel_flag_name(iosj__ylvqt)
    avjv__squpw = ['T'] + (['idx_arr'] if csv_iterator_type._index_ind is not
        None else []) + [pan__vlitw]
    aajz__zcd += f"  return {', '.join(avjv__squpw)}"
    curks__purq = globals()
    kikg__gbi = {}
    exec(aajz__zcd, curks__purq, kikg__gbi)
    oah__qpgh = kikg__gbi['read_csv_objmode']
    qtnc__fyq = numba.njit(oah__qpgh)
    bodo.ir.csv_ext.compiled_funcs.append(qtnc__fyq)
    rxfw__sacv = 'def read_func(reader, local_start):\n'
    rxfw__sacv += f"  {', '.join(avjv__squpw)} = objmode_func(reader)\n"
    index_ind = csv_iterator_type._index_ind
    if index_ind is None:
        rxfw__sacv += f'  local_len = len(T)\n'
        rxfw__sacv += '  total_size = local_len\n'
        rxfw__sacv += f'  if ({pan__vlitw}):\n'
        rxfw__sacv += """    local_start = local_start + bodo.libs.distributed_api.dist_exscan(local_len, _op)
"""
        rxfw__sacv += (
            '    total_size = bodo.libs.distributed_api.dist_reduce(local_len, _op)\n'
            )
        yudva__xul = (
            f'bodo.hiframes.pd_index_ext.init_range_index(local_start, local_start + local_len, 1, None)'
            )
    else:
        rxfw__sacv += '  total_size = 0\n'
        yudva__xul = (
            f'bodo.utils.conversion.convert_to_index({avjv__squpw[1]}, {csv_iterator_type._index_name!r})'
            )
    rxfw__sacv += f"""  return (bodo.hiframes.pd_dataframe_ext.init_dataframe(({avjv__squpw[0]},), {yudva__xul}, out_df_typ), total_size)
"""
    exec(rxfw__sacv, {'bodo': bodo, 'objmode_func': qtnc__fyq, '_op': np.
        int32(bodo.libs.distributed_api.Reduce_Type.Sum.value),
        'out_df_typ': csv_iterator_type.yield_type}, kikg__gbi)
    return kikg__gbi['read_func']
