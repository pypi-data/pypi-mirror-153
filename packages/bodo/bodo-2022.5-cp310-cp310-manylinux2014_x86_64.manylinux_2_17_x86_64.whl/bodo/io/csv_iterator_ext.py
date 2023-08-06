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
        dfd__fqeb = (
            f'CSVIteratorType({df_type}, {out_colnames}, {out_types}, {usecols}, {sep}, {index_ind}, {index_arr_typ}, {index_name}, {escapechar})'
            )
        super(types.SimpleIteratorType, self).__init__(dfd__fqeb)
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
        afodf__pqa = [('csv_reader', bodo.ir.connector.stream_reader_type),
            ('index', types.EphemeralPointer(types.uintp))]
        super(CSVIteratorModel, self).__init__(dmm, fe_type, afodf__pqa)


@lower_builtin('getiter', CSVIteratorType)
def getiter_csv_iterator(context, builder, sig, args):
    ypxxa__ckou = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    zqu__ayjb = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer()])
    juz__gzqpx = cgutils.get_or_insert_function(builder.module, zqu__ayjb,
        name='initialize_csv_reader')
    builder.call(juz__gzqpx, [ypxxa__ckou.csv_reader])
    builder.store(context.get_constant(types.uint64, 0), ypxxa__ckou.index)
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', CSVIteratorType)
@iternext_impl(RefType.NEW)
def iternext_csv_iterator(context, builder, sig, args, result):
    [nmyrp__zhpk] = sig.args
    [jpob__ikqwe] = args
    ypxxa__ckou = cgutils.create_struct_proxy(nmyrp__zhpk)(context, builder,
        value=jpob__ikqwe)
    zqu__ayjb = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer()])
    juz__gzqpx = cgutils.get_or_insert_function(builder.module, zqu__ayjb,
        name='update_csv_reader')
    lpl__xwwkf = builder.call(juz__gzqpx, [ypxxa__ckou.csv_reader])
    result.set_valid(lpl__xwwkf)
    with builder.if_then(lpl__xwwkf):
        nrvo__psw = builder.load(ypxxa__ckou.index)
        ykpe__zbxcj = types.Tuple([sig.return_type.first_type, types.int64])
        riqg__bdjl = gen_read_csv_objmode(sig.args[0])
        ynr__ptaia = signature(ykpe__zbxcj, bodo.ir.connector.
            stream_reader_type, types.int64)
        lcysl__gvjju = context.compile_internal(builder, riqg__bdjl,
            ynr__ptaia, [ypxxa__ckou.csv_reader, nrvo__psw])
        jic__yres, ajgvm__tezov = cgutils.unpack_tuple(builder, lcysl__gvjju)
        fcbe__xhv = builder.add(nrvo__psw, ajgvm__tezov, flags=['nsw'])
        builder.store(fcbe__xhv, ypxxa__ckou.index)
        result.yield_(jic__yres)


@intrinsic
def init_csv_iterator(typingctx, csv_reader, csv_iterator_typeref):

    def codegen(context, builder, signature, args):
        xsg__riknr = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        xsg__riknr.csv_reader = args[0]
        uiff__hfjd = context.get_constant(types.uintp, 0)
        xsg__riknr.index = cgutils.alloca_once_value(builder, uiff__hfjd)
        return xsg__riknr._getvalue()
    assert isinstance(csv_iterator_typeref, types.TypeRef
        ), 'Initializing a csv iterator requires a typeref'
    dcvi__jfm = csv_iterator_typeref.instance_type
    sig = signature(dcvi__jfm, csv_reader, csv_iterator_typeref)
    return sig, codegen


def gen_read_csv_objmode(csv_iterator_type):
    qmp__twy = 'def read_csv_objmode(f_reader):\n'
    vlx__bdk = [sanitize_varname(iny__pjlg) for iny__pjlg in
        csv_iterator_type._out_colnames]
    hhypp__ptlf = ir_utils.next_label()
    qszx__nzrt = globals()
    out_types = csv_iterator_type._out_types
    qszx__nzrt[f'table_type_{hhypp__ptlf}'] = TableType(tuple(out_types))
    qszx__nzrt[f'idx_array_typ'] = csv_iterator_type._index_arr_typ
    pzvig__mwz = list(range(len(csv_iterator_type._usecols)))
    qmp__twy += _gen_read_csv_objmode(csv_iterator_type._out_colnames,
        vlx__bdk, out_types, csv_iterator_type._usecols, pzvig__mwz,
        csv_iterator_type._sep, csv_iterator_type._escapechar,
        csv_iterator_type._storage_options, hhypp__ptlf, qszx__nzrt,
        parallel=False, check_parallel_runtime=True, idx_col_index=
        csv_iterator_type._index_ind, idx_col_typ=csv_iterator_type.
        _index_arr_typ)
    xxuu__rgj = bodo.ir.csv_ext._gen_parallel_flag_name(vlx__bdk)
    aymq__kyfd = ['T'] + (['idx_arr'] if csv_iterator_type._index_ind is not
        None else []) + [xxuu__rgj]
    qmp__twy += f"  return {', '.join(aymq__kyfd)}"
    qszx__nzrt = globals()
    qgcpc__gavw = {}
    exec(qmp__twy, qszx__nzrt, qgcpc__gavw)
    neoms__fust = qgcpc__gavw['read_csv_objmode']
    xeke__jfpt = numba.njit(neoms__fust)
    bodo.ir.csv_ext.compiled_funcs.append(xeke__jfpt)
    panm__eodd = 'def read_func(reader, local_start):\n'
    panm__eodd += f"  {', '.join(aymq__kyfd)} = objmode_func(reader)\n"
    index_ind = csv_iterator_type._index_ind
    if index_ind is None:
        panm__eodd += f'  local_len = len(T)\n'
        panm__eodd += '  total_size = local_len\n'
        panm__eodd += f'  if ({xxuu__rgj}):\n'
        panm__eodd += """    local_start = local_start + bodo.libs.distributed_api.dist_exscan(local_len, _op)
"""
        panm__eodd += (
            '    total_size = bodo.libs.distributed_api.dist_reduce(local_len, _op)\n'
            )
        lmn__nebi = (
            f'bodo.hiframes.pd_index_ext.init_range_index(local_start, local_start + local_len, 1, None)'
            )
    else:
        panm__eodd += '  total_size = 0\n'
        lmn__nebi = (
            f'bodo.utils.conversion.convert_to_index({aymq__kyfd[1]}, {csv_iterator_type._index_name!r})'
            )
    panm__eodd += f"""  return (bodo.hiframes.pd_dataframe_ext.init_dataframe(({aymq__kyfd[0]},), {lmn__nebi}, out_df_typ), total_size)
"""
    exec(panm__eodd, {'bodo': bodo, 'objmode_func': xeke__jfpt, '_op': np.
        int32(bodo.libs.distributed_api.Reduce_Type.Sum.value),
        'out_df_typ': csv_iterator_type.yield_type}, qgcpc__gavw)
    return qgcpc__gavw['read_func']
