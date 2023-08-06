"""Table data type for storing dataframe column arrays. Supports storing many columns
(e.g. >10k) efficiently.
"""
import operator
from collections import defaultdict
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.typing.templates import signature
from numba.cpython.listobj import ListInstance
from numba.extending import NativeValue, box, infer_getattr, intrinsic, lower_builtin, lower_getattr, make_attribute_wrapper, models, overload, register_model, typeof_impl, unbox
from numba.np.arrayobj import _getitem_array_single_int
from numba.parfors.array_analysis import ArrayAnalysis
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.templates import OverloadedKeyAttributeTemplate
from bodo.utils.typing import BodoError, decode_if_dict_array, get_overload_const_int, is_list_like_index_type, is_overload_constant_bool, is_overload_constant_int, is_overload_true, to_str_arr_if_dict_array


class Table:

    def __init__(self, arrs, usecols=None, num_arrs=-1):
        if usecols is not None:
            assert num_arrs != -1, 'num_arrs must be provided if usecols is not None'
            lbg__obhma = 0
            xlma__axddp = []
            for i in range(usecols[-1] + 1):
                if i == usecols[lbg__obhma]:
                    xlma__axddp.append(arrs[lbg__obhma])
                    lbg__obhma += 1
                else:
                    xlma__axddp.append(None)
            for iib__ecpo in range(usecols[-1] + 1, num_arrs):
                xlma__axddp.append(None)
            self.arrays = xlma__axddp
        else:
            self.arrays = arrs
        self.block_0 = arrs

    def __eq__(self, other):
        return isinstance(other, Table) and len(self.arrays) == len(other.
            arrays) and all((dwxu__vbq == kia__tijf).all() for dwxu__vbq,
            kia__tijf in zip(self.arrays, other.arrays))

    def __str__(self) ->str:
        return str(self.arrays)

    def to_pandas(self, index=None):
        hnrw__hupo = len(self.arrays)
        qsax__bxwzq = dict(zip(range(hnrw__hupo), self.arrays))
        df = pd.DataFrame(qsax__bxwzq, index)
        return df


class TableType(types.ArrayCompatible):

    def __init__(self, arr_types, has_runtime_cols=False):
        self.arr_types = arr_types
        self.has_runtime_cols = has_runtime_cols
        fvdff__vug = []
        bzhv__cegd = []
        zpt__tmu = {}
        lmbi__nfqb = defaultdict(int)
        ufker__hqjup = defaultdict(list)
        if not has_runtime_cols:
            for i, dry__sqi in enumerate(arr_types):
                if dry__sqi not in zpt__tmu:
                    zpt__tmu[dry__sqi] = len(zpt__tmu)
                onnzr__vxdy = zpt__tmu[dry__sqi]
                fvdff__vug.append(onnzr__vxdy)
                bzhv__cegd.append(lmbi__nfqb[onnzr__vxdy])
                lmbi__nfqb[onnzr__vxdy] += 1
                ufker__hqjup[onnzr__vxdy].append(i)
        self.block_nums = fvdff__vug
        self.block_offsets = bzhv__cegd
        self.type_to_blk = zpt__tmu
        self.block_to_arr_ind = ufker__hqjup
        super(TableType, self).__init__(name=
            f'TableType({arr_types}, {has_runtime_cols})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 2, 'C')

    @property
    def key(self):
        return self.arr_types, self.has_runtime_cols

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(Table)
def typeof_table(val, c):
    return TableType(tuple(numba.typeof(wii__qmz) for wii__qmz in val.arrays))


@register_model(TableType)
class TableTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        if fe_type.has_runtime_cols:
            fdz__tcst = [(f'block_{i}', types.List(dry__sqi)) for i,
                dry__sqi in enumerate(fe_type.arr_types)]
        else:
            fdz__tcst = [(f'block_{onnzr__vxdy}', types.List(dry__sqi)) for
                dry__sqi, onnzr__vxdy in fe_type.type_to_blk.items()]
        fdz__tcst.append(('parent', types.pyobject))
        fdz__tcst.append(('len', types.int64))
        super(TableTypeModel, self).__init__(dmm, fe_type, fdz__tcst)


make_attribute_wrapper(TableType, 'block_0', 'block_0')
make_attribute_wrapper(TableType, 'len', '_len')


@infer_getattr
class TableTypeAttribute(OverloadedKeyAttributeTemplate):
    key = TableType

    def resolve_shape(self, df):
        return types.Tuple([types.int64, types.int64])


@unbox(TableType)
def unbox_table(typ, val, c):
    rlrtn__szlee = c.pyapi.object_getattr_string(val, 'arrays')
    hiq__wvrqn = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    hiq__wvrqn.parent = cgutils.get_null_value(hiq__wvrqn.parent.type)
    gmee__hwlvl = c.pyapi.make_none()
    lyez__brzv = c.context.get_constant(types.int64, 0)
    tlzo__lwh = cgutils.alloca_once_value(c.builder, lyez__brzv)
    for dry__sqi, onnzr__vxdy in typ.type_to_blk.items():
        fbzxn__jrqce = c.context.get_constant(types.int64, len(typ.
            block_to_arr_ind[onnzr__vxdy]))
        iib__ecpo, mztld__pdlkr = ListInstance.allocate_ex(c.context, c.
            builder, types.List(dry__sqi), fbzxn__jrqce)
        mztld__pdlkr.size = fbzxn__jrqce
        xmyc__puvgj = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[onnzr__vxdy
            ], dtype=np.int64))
        elj__xuufb = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, xmyc__puvgj)
        with cgutils.for_range(c.builder, fbzxn__jrqce) as ydw__zyifr:
            i = ydw__zyifr.index
            jxbh__gbru = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), elj__xuufb, i)
            vdni__hwt = c.pyapi.long_from_longlong(jxbh__gbru)
            amfi__oohfa = c.pyapi.object_getitem(rlrtn__szlee, vdni__hwt)
            vwfv__gkfyo = c.builder.icmp_unsigned('==', amfi__oohfa,
                gmee__hwlvl)
            with c.builder.if_else(vwfv__gkfyo) as (nuxbq__vtdq, iqwk__peyih):
                with nuxbq__vtdq:
                    cpr__axvg = c.context.get_constant_null(dry__sqi)
                    mztld__pdlkr.inititem(i, cpr__axvg, incref=False)
                with iqwk__peyih:
                    gjpi__ztnps = c.pyapi.call_method(amfi__oohfa,
                        '__len__', ())
                    cui__tmeof = c.pyapi.long_as_longlong(gjpi__ztnps)
                    c.builder.store(cui__tmeof, tlzo__lwh)
                    c.pyapi.decref(gjpi__ztnps)
                    wii__qmz = c.pyapi.to_native_value(dry__sqi, amfi__oohfa
                        ).value
                    mztld__pdlkr.inititem(i, wii__qmz, incref=False)
            c.pyapi.decref(amfi__oohfa)
            c.pyapi.decref(vdni__hwt)
        setattr(hiq__wvrqn, f'block_{onnzr__vxdy}', mztld__pdlkr.value)
    hiq__wvrqn.len = c.builder.load(tlzo__lwh)
    c.pyapi.decref(rlrtn__szlee)
    c.pyapi.decref(gmee__hwlvl)
    umy__tbh = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(hiq__wvrqn._getvalue(), is_error=umy__tbh)


@box(TableType)
def box_table(typ, val, c, ensure_unboxed=None):
    from bodo.hiframes.boxing import get_df_obj_column_codegen
    hiq__wvrqn = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ.has_runtime_cols:
        vntiq__alb = c.context.get_constant(types.int64, 0)
        for i, dry__sqi in enumerate(typ.arr_types):
            xlma__axddp = getattr(hiq__wvrqn, f'block_{i}')
            dgao__ylnr = ListInstance(c.context, c.builder, types.List(
                dry__sqi), xlma__axddp)
            vntiq__alb = c.builder.add(vntiq__alb, dgao__ylnr.size)
        lovqc__aoc = c.pyapi.list_new(vntiq__alb)
        qlkh__mdian = c.context.get_constant(types.int64, 0)
        for i, dry__sqi in enumerate(typ.arr_types):
            xlma__axddp = getattr(hiq__wvrqn, f'block_{i}')
            dgao__ylnr = ListInstance(c.context, c.builder, types.List(
                dry__sqi), xlma__axddp)
            with cgutils.for_range(c.builder, dgao__ylnr.size) as ydw__zyifr:
                i = ydw__zyifr.index
                wii__qmz = dgao__ylnr.getitem(i)
                c.context.nrt.incref(c.builder, dry__sqi, wii__qmz)
                idx = c.builder.add(qlkh__mdian, i)
                c.pyapi.list_setitem(lovqc__aoc, idx, c.pyapi.
                    from_native_value(dry__sqi, wii__qmz, c.env_manager))
            qlkh__mdian = c.builder.add(qlkh__mdian, dgao__ylnr.size)
        axvu__owxqz = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
        rsxs__smd = c.pyapi.call_function_objargs(axvu__owxqz, (lovqc__aoc,))
        c.pyapi.decref(axvu__owxqz)
        c.pyapi.decref(lovqc__aoc)
        c.context.nrt.decref(c.builder, typ, val)
        return rsxs__smd
    lovqc__aoc = c.pyapi.list_new(c.context.get_constant(types.int64, len(
        typ.arr_types)))
    jgq__bnum = cgutils.is_not_null(c.builder, hiq__wvrqn.parent)
    if ensure_unboxed is None:
        ensure_unboxed = c.context.get_constant(types.bool_, False)
    for dry__sqi, onnzr__vxdy in typ.type_to_blk.items():
        xlma__axddp = getattr(hiq__wvrqn, f'block_{onnzr__vxdy}')
        dgao__ylnr = ListInstance(c.context, c.builder, types.List(dry__sqi
            ), xlma__axddp)
        xmyc__puvgj = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[onnzr__vxdy
            ], dtype=np.int64))
        elj__xuufb = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, xmyc__puvgj)
        with cgutils.for_range(c.builder, dgao__ylnr.size) as ydw__zyifr:
            i = ydw__zyifr.index
            jxbh__gbru = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), elj__xuufb, i)
            wii__qmz = dgao__ylnr.getitem(i)
            ddfot__zypyj = cgutils.alloca_once_value(c.builder, wii__qmz)
            jzcpr__qevn = cgutils.alloca_once_value(c.builder, c.context.
                get_constant_null(dry__sqi))
            mbvu__icwk = is_ll_eq(c.builder, ddfot__zypyj, jzcpr__qevn)
            with c.builder.if_else(c.builder.and_(mbvu__icwk, c.builder.
                not_(ensure_unboxed))) as (nuxbq__vtdq, iqwk__peyih):
                with nuxbq__vtdq:
                    gmee__hwlvl = c.pyapi.make_none()
                    c.pyapi.list_setitem(lovqc__aoc, jxbh__gbru, gmee__hwlvl)
                with iqwk__peyih:
                    amfi__oohfa = cgutils.alloca_once(c.builder, c.context.
                        get_value_type(types.pyobject))
                    with c.builder.if_else(c.builder.and_(mbvu__icwk,
                        jgq__bnum)) as (zfug__hwrd, ixysp__haf):
                        with zfug__hwrd:
                            vie__pvbjf = get_df_obj_column_codegen(c.
                                context, c.builder, c.pyapi, hiq__wvrqn.
                                parent, jxbh__gbru, dry__sqi)
                            c.builder.store(vie__pvbjf, amfi__oohfa)
                        with ixysp__haf:
                            c.context.nrt.incref(c.builder, dry__sqi, wii__qmz)
                            c.builder.store(c.pyapi.from_native_value(
                                dry__sqi, wii__qmz, c.env_manager), amfi__oohfa
                                )
                    c.pyapi.list_setitem(lovqc__aoc, jxbh__gbru, c.builder.
                        load(amfi__oohfa))
    axvu__owxqz = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
    rsxs__smd = c.pyapi.call_function_objargs(axvu__owxqz, (lovqc__aoc,))
    c.pyapi.decref(axvu__owxqz)
    c.pyapi.decref(lovqc__aoc)
    c.context.nrt.decref(c.builder, typ, val)
    return rsxs__smd


@lower_builtin(len, TableType)
def table_len_lower(context, builder, sig, args):
    impl = table_len_overload(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def table_len_overload(T):
    if not isinstance(T, TableType):
        return

    def impl(T):
        return T._len
    return impl


@lower_getattr(TableType, 'shape')
def lower_table_shape(context, builder, typ, val):
    impl = table_shape_overload(typ)
    return context.compile_internal(builder, impl, types.Tuple([types.int64,
        types.int64])(typ), (val,))


def table_shape_overload(T):
    if T.has_runtime_cols:

        def impl(T):
            return T._len, compute_num_runtime_columns(T)
        return impl
    ncols = len(T.arr_types)
    return lambda T: (T._len, types.int64(ncols))


@intrinsic
def compute_num_runtime_columns(typingctx, table_type):
    assert isinstance(table_type, TableType)

    def codegen(context, builder, sig, args):
        table_arg, = args
        hiq__wvrqn = cgutils.create_struct_proxy(table_type)(context,
            builder, table_arg)
        wsd__uqllx = context.get_constant(types.int64, 0)
        for i, dry__sqi in enumerate(table_type.arr_types):
            xlma__axddp = getattr(hiq__wvrqn, f'block_{i}')
            dgao__ylnr = ListInstance(context, builder, types.List(dry__sqi
                ), xlma__axddp)
            wsd__uqllx = builder.add(wsd__uqllx, dgao__ylnr.size)
        return wsd__uqllx
    sig = types.int64(table_type)
    return sig, codegen


def get_table_data_codegen(context, builder, table_arg, col_ind, table_type):
    arr_type = table_type.arr_types[col_ind]
    hiq__wvrqn = cgutils.create_struct_proxy(table_type)(context, builder,
        table_arg)
    onnzr__vxdy = table_type.block_nums[col_ind]
    ocnx__tke = table_type.block_offsets[col_ind]
    xlma__axddp = getattr(hiq__wvrqn, f'block_{onnzr__vxdy}')
    dgao__ylnr = ListInstance(context, builder, types.List(arr_type),
        xlma__axddp)
    wii__qmz = dgao__ylnr.getitem(ocnx__tke)
    return wii__qmz


@intrinsic
def get_table_data(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, iib__ecpo = args
        wii__qmz = get_table_data_codegen(context, builder, table_arg,
            col_ind, table_type)
        return impl_ret_borrowed(context, builder, arr_type, wii__qmz)
    sig = arr_type(table_type, ind_typ)
    return sig, codegen


@intrinsic
def del_column(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, iib__ecpo = args
        hiq__wvrqn = cgutils.create_struct_proxy(table_type)(context,
            builder, table_arg)
        onnzr__vxdy = table_type.block_nums[col_ind]
        ocnx__tke = table_type.block_offsets[col_ind]
        xlma__axddp = getattr(hiq__wvrqn, f'block_{onnzr__vxdy}')
        dgao__ylnr = ListInstance(context, builder, types.List(arr_type),
            xlma__axddp)
        wii__qmz = dgao__ylnr.getitem(ocnx__tke)
        context.nrt.decref(builder, arr_type, wii__qmz)
        cpr__axvg = context.get_constant_null(arr_type)
        dgao__ylnr.inititem(ocnx__tke, cpr__axvg, incref=False)
    sig = types.void(table_type, ind_typ)
    return sig, codegen


def set_table_data_codegen(context, builder, in_table_type, in_table,
    out_table_type, arr_type, arr_arg, col_ind, is_new_col):
    in_table = cgutils.create_struct_proxy(in_table_type)(context, builder,
        in_table)
    out_table = cgutils.create_struct_proxy(out_table_type)(context, builder)
    out_table.len = in_table.len
    out_table.parent = in_table.parent
    lyez__brzv = context.get_constant(types.int64, 0)
    diy__qbrfr = context.get_constant(types.int64, 1)
    dcz__hoqsx = arr_type not in in_table_type.type_to_blk
    for dry__sqi, onnzr__vxdy in out_table_type.type_to_blk.items():
        if dry__sqi in in_table_type.type_to_blk:
            ipuo__bhmou = in_table_type.type_to_blk[dry__sqi]
            mztld__pdlkr = ListInstance(context, builder, types.List(
                dry__sqi), getattr(in_table, f'block_{ipuo__bhmou}'))
            context.nrt.incref(builder, types.List(dry__sqi), mztld__pdlkr.
                value)
            setattr(out_table, f'block_{onnzr__vxdy}', mztld__pdlkr.value)
    if dcz__hoqsx:
        iib__ecpo, mztld__pdlkr = ListInstance.allocate_ex(context, builder,
            types.List(arr_type), diy__qbrfr)
        mztld__pdlkr.size = diy__qbrfr
        mztld__pdlkr.inititem(lyez__brzv, arr_arg, incref=True)
        onnzr__vxdy = out_table_type.type_to_blk[arr_type]
        setattr(out_table, f'block_{onnzr__vxdy}', mztld__pdlkr.value)
        if not is_new_col:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
    else:
        onnzr__vxdy = out_table_type.type_to_blk[arr_type]
        mztld__pdlkr = ListInstance(context, builder, types.List(arr_type),
            getattr(out_table, f'block_{onnzr__vxdy}'))
        if is_new_col:
            n = mztld__pdlkr.size
            fitok__svldn = builder.add(n, diy__qbrfr)
            mztld__pdlkr.resize(fitok__svldn)
            mztld__pdlkr.inititem(n, arr_arg, incref=True)
        elif arr_type == in_table_type.arr_types[col_ind]:
            cakv__eaxh = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            mztld__pdlkr.setitem(cakv__eaxh, arr_arg, True)
        else:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
            cakv__eaxh = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            n = mztld__pdlkr.size
            fitok__svldn = builder.add(n, diy__qbrfr)
            mztld__pdlkr.resize(fitok__svldn)
            context.nrt.incref(builder, arr_type, mztld__pdlkr.getitem(
                cakv__eaxh))
            mztld__pdlkr.move(builder.add(cakv__eaxh, diy__qbrfr),
                cakv__eaxh, builder.sub(n, cakv__eaxh))
            mztld__pdlkr.setitem(cakv__eaxh, arr_arg, incref=True)
    return out_table._getvalue()


def _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
    context, builder):
    ynmpz__tbki = in_table_type.arr_types[col_ind]
    if ynmpz__tbki in out_table_type.type_to_blk:
        onnzr__vxdy = out_table_type.type_to_blk[ynmpz__tbki]
        lkas__qwra = getattr(out_table, f'block_{onnzr__vxdy}')
        tjypb__qnt = types.List(ynmpz__tbki)
        cakv__eaxh = context.get_constant(types.int64, in_table_type.
            block_offsets[col_ind])
        pny__uzax = tjypb__qnt.dtype(tjypb__qnt, types.intp)
        ute__qpew = context.compile_internal(builder, lambda lst, i: lst.
            pop(i), pny__uzax, (lkas__qwra, cakv__eaxh))
        context.nrt.decref(builder, ynmpz__tbki, ute__qpew)


@intrinsic
def set_table_data(typingctx, table_type, ind_type, arr_type):
    assert isinstance(table_type, TableType), 'invalid input to set_table_data'
    assert is_overload_constant_int(ind_type
        ), 'set_table_data expects const index'
    col_ind = get_overload_const_int(ind_type)
    is_new_col = col_ind == len(table_type.arr_types)
    fuggl__stw = list(table_type.arr_types)
    if is_new_col:
        fuggl__stw.append(arr_type)
    else:
        fuggl__stw[col_ind] = arr_type
    out_table_type = TableType(tuple(fuggl__stw))

    def codegen(context, builder, sig, args):
        table_arg, iib__ecpo, bjkeq__bfumo = args
        out_table = set_table_data_codegen(context, builder, table_type,
            table_arg, out_table_type, arr_type, bjkeq__bfumo, col_ind,
            is_new_col)
        return out_table
    return out_table_type(table_type, ind_type, arr_type), codegen


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_table_data',
    'bodo.hiframes.table'] = alias_ext_dummy_func


def get_table_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    niy__rha = args[0]
    if equiv_set.has_shape(niy__rha):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            niy__rha)[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_get_table_data = (
    get_table_data_equiv)


@lower_constant(TableType)
def lower_constant_table(context, builder, table_type, pyval):
    jgj__dvh = []
    for dry__sqi, onnzr__vxdy in table_type.type_to_blk.items():
        shat__kux = len(table_type.block_to_arr_ind[onnzr__vxdy])
        fyq__hqp = []
        for i in range(shat__kux):
            jxbh__gbru = table_type.block_to_arr_ind[onnzr__vxdy][i]
            fyq__hqp.append(pyval.arrays[jxbh__gbru])
        jgj__dvh.append(context.get_constant_generic(builder, types.List(
            dry__sqi), fyq__hqp))
    nuevt__dqdli = context.get_constant_null(types.pyobject)
    boug__yss = context.get_constant(types.int64, 0 if len(pyval.arrays) ==
        0 else len(pyval.arrays[0]))
    return lir.Constant.literal_struct(jgj__dvh + [nuevt__dqdli, boug__yss])


@intrinsic
def init_table(typingctx, table_type, to_str_if_dict_t):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    out_table_type = table_type
    if is_overload_true(to_str_if_dict_t):
        out_table_type = to_str_arr_if_dict_array(table_type)

    def codegen(context, builder, sig, args):
        hiq__wvrqn = cgutils.create_struct_proxy(out_table_type)(context,
            builder)
        for dry__sqi, onnzr__vxdy in out_table_type.type_to_blk.items():
            bjcvu__wreh = context.get_constant_null(types.List(dry__sqi))
            setattr(hiq__wvrqn, f'block_{onnzr__vxdy}', bjcvu__wreh)
        return hiq__wvrqn._getvalue()
    sig = out_table_type(table_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def init_table_from_lists(typingctx, tuple_of_lists_type, table_type):
    assert isinstance(tuple_of_lists_type, types.BaseTuple
        ), 'Tuple of data expected'
    oct__lzcu = {}
    for i, typ in enumerate(tuple_of_lists_type):
        assert isinstance(typ, types.List), 'Each tuple element must be a list'
        oct__lzcu[typ.dtype] = i
    obuf__jpn = table_type.instance_type if isinstance(table_type, types.
        TypeRef) else table_type
    assert isinstance(obuf__jpn, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        bwc__tmho, iib__ecpo = args
        hiq__wvrqn = cgutils.create_struct_proxy(obuf__jpn)(context, builder)
        for dry__sqi, onnzr__vxdy in obuf__jpn.type_to_blk.items():
            idx = oct__lzcu[dry__sqi]
            lbp__ifjc = signature(types.List(dry__sqi), tuple_of_lists_type,
                types.literal(idx))
            oev__cff = bwc__tmho, idx
            lruqq__sofl = numba.cpython.tupleobj.static_getitem_tuple(context,
                builder, lbp__ifjc, oev__cff)
            setattr(hiq__wvrqn, f'block_{onnzr__vxdy}', lruqq__sofl)
        return hiq__wvrqn._getvalue()
    sig = obuf__jpn(tuple_of_lists_type, table_type)
    return sig, codegen


@intrinsic
def get_table_block(typingctx, table_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_int(blk_type)
    onnzr__vxdy = get_overload_const_int(blk_type)
    arr_type = None
    for dry__sqi, kia__tijf in table_type.type_to_blk.items():
        if kia__tijf == onnzr__vxdy:
            arr_type = dry__sqi
            break
    assert arr_type is not None, 'invalid table type block'
    fvc__mws = types.List(arr_type)

    def codegen(context, builder, sig, args):
        hiq__wvrqn = cgutils.create_struct_proxy(table_type)(context,
            builder, args[0])
        xlma__axddp = getattr(hiq__wvrqn, f'block_{onnzr__vxdy}')
        return impl_ret_borrowed(context, builder, fvc__mws, xlma__axddp)
    sig = fvc__mws(table_type, blk_type)
    return sig, codegen


@intrinsic
def ensure_table_unboxed(typingctx, table_type, used_cols_typ):

    def codegen(context, builder, sig, args):
        table_arg, vadro__dyf = args
        xdmvw__ozqr = context.get_python_api(builder)
        nivs__kmjxm = used_cols_typ == types.none
        if not nivs__kmjxm:
            itxvo__elxlg = numba.cpython.setobj.SetInstance(context,
                builder, types.Set(types.int64), vadro__dyf)
        hiq__wvrqn = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, table_arg)
        jgq__bnum = cgutils.is_not_null(builder, hiq__wvrqn.parent)
        for dry__sqi, onnzr__vxdy in table_type.type_to_blk.items():
            fbzxn__jrqce = context.get_constant(types.int64, len(table_type
                .block_to_arr_ind[onnzr__vxdy]))
            xmyc__puvgj = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(table_type.block_to_arr_ind[
                onnzr__vxdy], dtype=np.int64))
            elj__xuufb = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, xmyc__puvgj)
            xlma__axddp = getattr(hiq__wvrqn, f'block_{onnzr__vxdy}')
            with cgutils.for_range(builder, fbzxn__jrqce) as ydw__zyifr:
                i = ydw__zyifr.index
                jxbh__gbru = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    elj__xuufb, i)
                lov__unzde = types.none(table_type, types.List(dry__sqi),
                    types.int64, types.int64)
                yxz__onxlt = table_arg, xlma__axddp, i, jxbh__gbru
                if nivs__kmjxm:
                    ensure_column_unboxed_codegen(context, builder,
                        lov__unzde, yxz__onxlt)
                else:
                    wrdlt__fcow = itxvo__elxlg.contains(jxbh__gbru)
                    with builder.if_then(wrdlt__fcow):
                        ensure_column_unboxed_codegen(context, builder,
                            lov__unzde, yxz__onxlt)
    assert isinstance(table_type, TableType), 'table type expected'
    sig = types.none(table_type, used_cols_typ)
    return sig, codegen


@intrinsic
def ensure_column_unboxed(typingctx, table_type, arr_list_t, ind_t, arr_ind_t):
    assert isinstance(table_type, TableType), 'table type expected'
    sig = types.none(table_type, arr_list_t, ind_t, arr_ind_t)
    return sig, ensure_column_unboxed_codegen


def ensure_column_unboxed_codegen(context, builder, sig, args):
    from bodo.hiframes.boxing import get_df_obj_column_codegen
    table_arg, uvri__wqvz, dty__kuotn, ybtj__mrya = args
    xdmvw__ozqr = context.get_python_api(builder)
    hiq__wvrqn = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        table_arg)
    jgq__bnum = cgutils.is_not_null(builder, hiq__wvrqn.parent)
    dgao__ylnr = ListInstance(context, builder, sig.args[1], uvri__wqvz)
    ckqrg__zed = dgao__ylnr.getitem(dty__kuotn)
    ddfot__zypyj = cgutils.alloca_once_value(builder, ckqrg__zed)
    jzcpr__qevn = cgutils.alloca_once_value(builder, context.
        get_constant_null(sig.args[1].dtype))
    mbvu__icwk = is_ll_eq(builder, ddfot__zypyj, jzcpr__qevn)
    with builder.if_then(mbvu__icwk):
        with builder.if_else(jgq__bnum) as (nuxbq__vtdq, iqwk__peyih):
            with nuxbq__vtdq:
                amfi__oohfa = get_df_obj_column_codegen(context, builder,
                    xdmvw__ozqr, hiq__wvrqn.parent, ybtj__mrya, sig.args[1]
                    .dtype)
                wii__qmz = xdmvw__ozqr.to_native_value(sig.args[1].dtype,
                    amfi__oohfa).value
                dgao__ylnr.inititem(dty__kuotn, wii__qmz, incref=False)
                xdmvw__ozqr.decref(amfi__oohfa)
            with iqwk__peyih:
                context.call_conv.return_user_exc(builder, BodoError, (
                    'unexpected null table column',))


@intrinsic
def set_table_block(typingctx, table_type, arr_list_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert isinstance(arr_list_type, types.List), 'list type expected'
    assert is_overload_constant_int(blk_type), 'blk should be const int'
    onnzr__vxdy = get_overload_const_int(blk_type)

    def codegen(context, builder, sig, args):
        table_arg, vjqmt__pwqeq, iib__ecpo = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        setattr(in_table, f'block_{onnzr__vxdy}', vjqmt__pwqeq)
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, arr_list_type, blk_type)
    return sig, codegen


@intrinsic
def set_table_len(typingctx, table_type, l_type):
    assert isinstance(table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        table_arg, hkb__rhjk = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        in_table.len = hkb__rhjk
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, l_type)
    return sig, codegen


@intrinsic
def alloc_list_like(typingctx, list_type, to_str_if_dict_t):
    assert isinstance(list_type, types.List), 'list type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    fvc__mws = list_type
    if is_overload_true(to_str_if_dict_t):
        fvc__mws = types.List(to_str_arr_if_dict_array(list_type.dtype))

    def codegen(context, builder, sig, args):
        ghac__ciod = ListInstance(context, builder, list_type, args[0])
        dhax__grp = ghac__ciod.size
        iib__ecpo, mztld__pdlkr = ListInstance.allocate_ex(context, builder,
            fvc__mws, dhax__grp)
        mztld__pdlkr.size = dhax__grp
        return mztld__pdlkr.value
    sig = fvc__mws(list_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def alloc_empty_list_type(typingctx, size_typ, data_typ=None):
    assert isinstance(size_typ, types.Integer), 'Size must be an integer'
    ggxy__xtqt = data_typ.instance_type if isinstance(data_typ, types.TypeRef
        ) else data_typ
    list_type = types.List(ggxy__xtqt)

    def codegen(context, builder, sig, args):
        dhax__grp, iib__ecpo = args
        iib__ecpo, mztld__pdlkr = ListInstance.allocate_ex(context, builder,
            list_type, dhax__grp)
        mztld__pdlkr.size = dhax__grp
        return mztld__pdlkr.value
    sig = list_type(size_typ, data_typ)
    return sig, codegen


def _get_idx_length(idx):
    pass


@overload(_get_idx_length)
def overload_get_idx_length(idx, n):
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        return lambda idx, n: idx.sum()
    assert isinstance(idx, types.SliceType), 'slice index expected'

    def impl(idx, n):
        sfs__aanb = numba.cpython.unicode._normalize_slice(idx, n)
        return numba.cpython.unicode._slice_span(sfs__aanb)
    return impl


def gen_table_filter(T, used_cols=None):
    from bodo.utils.conversion import ensure_contig_if_np
    vbb__zmizu = {'init_table': init_table, 'get_table_block':
        get_table_block, 'ensure_column_unboxed': ensure_column_unboxed,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'alloc_list_like': alloc_list_like, '_get_idx_length':
        _get_idx_length, 'ensure_contig_if_np': ensure_contig_if_np}
    if used_cols is not None:
        vbb__zmizu['used_cols'] = used_cols
    sfse__kbfdf = 'def impl(T, idx):\n'
    sfse__kbfdf += f'  T2 = init_table(T, False)\n'
    sfse__kbfdf += f'  l = 0\n'
    if used_cols is not None and len(used_cols) == 0:
        sfse__kbfdf += f'  l = _get_idx_length(idx, len(T))\n'
        sfse__kbfdf += f'  T2 = set_table_len(T2, l)\n'
        sfse__kbfdf += f'  return T2\n'
        jlg__texb = {}
        exec(sfse__kbfdf, vbb__zmizu, jlg__texb)
        return jlg__texb['impl']
    if used_cols is not None:
        sfse__kbfdf += f'  used_set = set(used_cols)\n'
    for onnzr__vxdy in T.type_to_blk.values():
        vbb__zmizu[f'arr_inds_{onnzr__vxdy}'] = np.array(T.block_to_arr_ind
            [onnzr__vxdy], dtype=np.int64)
        sfse__kbfdf += (
            f'  arr_list_{onnzr__vxdy} = get_table_block(T, {onnzr__vxdy})\n')
        sfse__kbfdf += f"""  out_arr_list_{onnzr__vxdy} = alloc_list_like(arr_list_{onnzr__vxdy}, False)
"""
        sfse__kbfdf += f'  for i in range(len(arr_list_{onnzr__vxdy})):\n'
        sfse__kbfdf += (
            f'    arr_ind_{onnzr__vxdy} = arr_inds_{onnzr__vxdy}[i]\n')
        if used_cols is not None:
            sfse__kbfdf += (
                f'    if arr_ind_{onnzr__vxdy} not in used_set: continue\n')
        sfse__kbfdf += f"""    ensure_column_unboxed(T, arr_list_{onnzr__vxdy}, i, arr_ind_{onnzr__vxdy})
"""
        sfse__kbfdf += f"""    out_arr_{onnzr__vxdy} = ensure_contig_if_np(arr_list_{onnzr__vxdy}[i][idx])
"""
        sfse__kbfdf += f'    l = len(out_arr_{onnzr__vxdy})\n'
        sfse__kbfdf += (
            f'    out_arr_list_{onnzr__vxdy}[i] = out_arr_{onnzr__vxdy}\n')
        sfse__kbfdf += (
            f'  T2 = set_table_block(T2, out_arr_list_{onnzr__vxdy}, {onnzr__vxdy})\n'
            )
    sfse__kbfdf += f'  T2 = set_table_len(T2, l)\n'
    sfse__kbfdf += f'  return T2\n'
    jlg__texb = {}
    exec(sfse__kbfdf, vbb__zmizu, jlg__texb)
    return jlg__texb['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def decode_if_dict_table(T):
    sfse__kbfdf = 'def impl(T):\n'
    sfse__kbfdf += f'  T2 = init_table(T, True)\n'
    sfse__kbfdf += f'  l = len(T)\n'
    vbb__zmizu = {'init_table': init_table, 'get_table_block':
        get_table_block, 'ensure_column_unboxed': ensure_column_unboxed,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'alloc_list_like': alloc_list_like, 'decode_if_dict_array':
        decode_if_dict_array}
    for onnzr__vxdy in T.type_to_blk.values():
        vbb__zmizu[f'arr_inds_{onnzr__vxdy}'] = np.array(T.block_to_arr_ind
            [onnzr__vxdy], dtype=np.int64)
        sfse__kbfdf += (
            f'  arr_list_{onnzr__vxdy} = get_table_block(T, {onnzr__vxdy})\n')
        sfse__kbfdf += f"""  out_arr_list_{onnzr__vxdy} = alloc_list_like(arr_list_{onnzr__vxdy}, True)
"""
        sfse__kbfdf += f'  for i in range(len(arr_list_{onnzr__vxdy})):\n'
        sfse__kbfdf += (
            f'    arr_ind_{onnzr__vxdy} = arr_inds_{onnzr__vxdy}[i]\n')
        sfse__kbfdf += f"""    ensure_column_unboxed(T, arr_list_{onnzr__vxdy}, i, arr_ind_{onnzr__vxdy})
"""
        sfse__kbfdf += f"""    out_arr_{onnzr__vxdy} = decode_if_dict_array(arr_list_{onnzr__vxdy}[i])
"""
        sfse__kbfdf += (
            f'    out_arr_list_{onnzr__vxdy}[i] = out_arr_{onnzr__vxdy}\n')
        sfse__kbfdf += (
            f'  T2 = set_table_block(T2, out_arr_list_{onnzr__vxdy}, {onnzr__vxdy})\n'
            )
    sfse__kbfdf += f'  T2 = set_table_len(T2, l)\n'
    sfse__kbfdf += f'  return T2\n'
    jlg__texb = {}
    exec(sfse__kbfdf, vbb__zmizu, jlg__texb)
    return jlg__texb['impl']


@overload(operator.getitem, no_unliteral=True)
def table_getitem(T, idx):
    if not isinstance(T, TableType):
        return
    return gen_table_filter(T)


@intrinsic
def init_runtime_table_from_lists(typingctx, arr_list_tup_typ, nrows_typ=None):
    assert isinstance(arr_list_tup_typ, types.BaseTuple
        ), 'init_runtime_table_from_lists requires a tuple of list of arrays'
    if isinstance(arr_list_tup_typ, types.UniTuple):
        if arr_list_tup_typ.dtype.dtype == types.undefined:
            return
        wfvtq__fqu = [arr_list_tup_typ.dtype.dtype] * len(arr_list_tup_typ)
    else:
        wfvtq__fqu = []
        for typ in arr_list_tup_typ:
            if typ.dtype == types.undefined:
                return
            wfvtq__fqu.append(typ.dtype)
    assert isinstance(nrows_typ, types.Integer
        ), 'init_runtime_table_from_lists requires an integer length'

    def codegen(context, builder, sig, args):
        ztgk__lxo, yzai__jhd = args
        hiq__wvrqn = cgutils.create_struct_proxy(table_type)(context, builder)
        hiq__wvrqn.len = yzai__jhd
        jgj__dvh = cgutils.unpack_tuple(builder, ztgk__lxo)
        for i, xlma__axddp in enumerate(jgj__dvh):
            setattr(hiq__wvrqn, f'block_{i}', xlma__axddp)
            context.nrt.incref(builder, types.List(wfvtq__fqu[i]), xlma__axddp)
        return hiq__wvrqn._getvalue()
    table_type = TableType(tuple(wfvtq__fqu), True)
    sig = table_type(arr_list_tup_typ, nrows_typ)
    return sig, codegen
