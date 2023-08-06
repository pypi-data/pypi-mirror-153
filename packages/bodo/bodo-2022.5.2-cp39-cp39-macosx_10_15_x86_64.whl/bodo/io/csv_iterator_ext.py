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
        ogtd__xpf = (
            f'CSVIteratorType({df_type}, {out_colnames}, {out_types}, {usecols}, {sep}, {index_ind}, {index_arr_typ}, {index_name}, {escapechar})'
            )
        super(types.SimpleIteratorType, self).__init__(ogtd__xpf)
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
        krld__dym = [('csv_reader', bodo.ir.connector.stream_reader_type),
            ('index', types.EphemeralPointer(types.uintp))]
        super(CSVIteratorModel, self).__init__(dmm, fe_type, krld__dym)


@lower_builtin('getiter', CSVIteratorType)
def getiter_csv_iterator(context, builder, sig, args):
    zpi__agjjg = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    dsjub__wgk = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer()]
        )
    gvlo__ghi = cgutils.get_or_insert_function(builder.module, dsjub__wgk,
        name='initialize_csv_reader')
    builder.call(gvlo__ghi, [zpi__agjjg.csv_reader])
    builder.store(context.get_constant(types.uint64, 0), zpi__agjjg.index)
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', CSVIteratorType)
@iternext_impl(RefType.NEW)
def iternext_csv_iterator(context, builder, sig, args, result):
    [osxk__vse] = sig.args
    [lmhby__fjfh] = args
    zpi__agjjg = cgutils.create_struct_proxy(osxk__vse)(context, builder,
        value=lmhby__fjfh)
    dsjub__wgk = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer()]
        )
    gvlo__ghi = cgutils.get_or_insert_function(builder.module, dsjub__wgk,
        name='update_csv_reader')
    kdz__wlser = builder.call(gvlo__ghi, [zpi__agjjg.csv_reader])
    result.set_valid(kdz__wlser)
    with builder.if_then(kdz__wlser):
        edci__zmio = builder.load(zpi__agjjg.index)
        jnx__kgjpv = types.Tuple([sig.return_type.first_type, types.int64])
        wja__ylged = gen_read_csv_objmode(sig.args[0])
        lns__tfl = signature(jnx__kgjpv, bodo.ir.connector.
            stream_reader_type, types.int64)
        zjzo__ync = context.compile_internal(builder, wja__ylged, lns__tfl,
            [zpi__agjjg.csv_reader, edci__zmio])
        odx__ayer, yllnp__qof = cgutils.unpack_tuple(builder, zjzo__ync)
        lvu__nzxmn = builder.add(edci__zmio, yllnp__qof, flags=['nsw'])
        builder.store(lvu__nzxmn, zpi__agjjg.index)
        result.yield_(odx__ayer)


@intrinsic
def init_csv_iterator(typingctx, csv_reader, csv_iterator_typeref):

    def codegen(context, builder, signature, args):
        cuux__thbn = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        cuux__thbn.csv_reader = args[0]
        hpz__zauk = context.get_constant(types.uintp, 0)
        cuux__thbn.index = cgutils.alloca_once_value(builder, hpz__zauk)
        return cuux__thbn._getvalue()
    assert isinstance(csv_iterator_typeref, types.TypeRef
        ), 'Initializing a csv iterator requires a typeref'
    rtde__yuncj = csv_iterator_typeref.instance_type
    sig = signature(rtde__yuncj, csv_reader, csv_iterator_typeref)
    return sig, codegen


def gen_read_csv_objmode(csv_iterator_type):
    xbtqj__rpk = 'def read_csv_objmode(f_reader):\n'
    bspjg__qghzo = [sanitize_varname(ikemv__jpvrf) for ikemv__jpvrf in
        csv_iterator_type._out_colnames]
    rxam__qwa = ir_utils.next_label()
    doq__qtb = globals()
    out_types = csv_iterator_type._out_types
    doq__qtb[f'table_type_{rxam__qwa}'] = TableType(tuple(out_types))
    doq__qtb[f'idx_array_typ'] = csv_iterator_type._index_arr_typ
    dfta__mlfh = list(range(len(csv_iterator_type._usecols)))
    xbtqj__rpk += _gen_read_csv_objmode(csv_iterator_type._out_colnames,
        bspjg__qghzo, out_types, csv_iterator_type._usecols, dfta__mlfh,
        csv_iterator_type._sep, csv_iterator_type._escapechar,
        csv_iterator_type._storage_options, rxam__qwa, doq__qtb, parallel=
        False, check_parallel_runtime=True, idx_col_index=csv_iterator_type
        ._index_ind, idx_col_typ=csv_iterator_type._index_arr_typ)
    tnueb__bqdq = bodo.ir.csv_ext._gen_parallel_flag_name(bspjg__qghzo)
    ozu__iqg = ['T'] + (['idx_arr'] if csv_iterator_type._index_ind is not
        None else []) + [tnueb__bqdq]
    xbtqj__rpk += f"  return {', '.join(ozu__iqg)}"
    doq__qtb = globals()
    oxbr__qcmk = {}
    exec(xbtqj__rpk, doq__qtb, oxbr__qcmk)
    hbz__itwa = oxbr__qcmk['read_csv_objmode']
    dewt__yjww = numba.njit(hbz__itwa)
    bodo.ir.csv_ext.compiled_funcs.append(dewt__yjww)
    zic__buf = 'def read_func(reader, local_start):\n'
    zic__buf += f"  {', '.join(ozu__iqg)} = objmode_func(reader)\n"
    index_ind = csv_iterator_type._index_ind
    if index_ind is None:
        zic__buf += f'  local_len = len(T)\n'
        zic__buf += '  total_size = local_len\n'
        zic__buf += f'  if ({tnueb__bqdq}):\n'
        zic__buf += """    local_start = local_start + bodo.libs.distributed_api.dist_exscan(local_len, _op)
"""
        zic__buf += (
            '    total_size = bodo.libs.distributed_api.dist_reduce(local_len, _op)\n'
            )
        sxe__hund = (
            f'bodo.hiframes.pd_index_ext.init_range_index(local_start, local_start + local_len, 1, None)'
            )
    else:
        zic__buf += '  total_size = 0\n'
        sxe__hund = (
            f'bodo.utils.conversion.convert_to_index({ozu__iqg[1]}, {csv_iterator_type._index_name!r})'
            )
    zic__buf += f"""  return (bodo.hiframes.pd_dataframe_ext.init_dataframe(({ozu__iqg[0]},), {sxe__hund}, out_df_typ), total_size)
"""
    exec(zic__buf, {'bodo': bodo, 'objmode_func': dewt__yjww, '_op': np.
        int32(bodo.libs.distributed_api.Reduce_Type.Sum.value),
        'out_df_typ': csv_iterator_type.yield_type}, oxbr__qcmk)
    return oxbr__qcmk['read_func']
