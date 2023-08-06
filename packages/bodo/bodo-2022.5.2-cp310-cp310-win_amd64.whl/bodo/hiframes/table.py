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
            xiir__kbb = 0
            rbveq__whi = []
            for i in range(usecols[-1] + 1):
                if i == usecols[xiir__kbb]:
                    rbveq__whi.append(arrs[xiir__kbb])
                    xiir__kbb += 1
                else:
                    rbveq__whi.append(None)
            for itnpf__zjbyg in range(usecols[-1] + 1, num_arrs):
                rbveq__whi.append(None)
            self.arrays = rbveq__whi
        else:
            self.arrays = arrs
        self.block_0 = arrs

    def __eq__(self, other):
        return isinstance(other, Table) and len(self.arrays) == len(other.
            arrays) and all((suuh__hbj == bjy__vksjk).all() for suuh__hbj,
            bjy__vksjk in zip(self.arrays, other.arrays))

    def __str__(self) ->str:
        return str(self.arrays)

    def to_pandas(self, index=None):
        kblts__xnsr = len(self.arrays)
        yom__dusub = dict(zip(range(kblts__xnsr), self.arrays))
        df = pd.DataFrame(yom__dusub, index)
        return df


class TableType(types.ArrayCompatible):

    def __init__(self, arr_types, has_runtime_cols=False):
        self.arr_types = arr_types
        self.has_runtime_cols = has_runtime_cols
        krr__mokf = []
        huxah__onlj = []
        gdzm__pgm = {}
        wkhsz__oqjr = defaultdict(int)
        xnpj__ipjo = defaultdict(list)
        if not has_runtime_cols:
            for i, nus__jsn in enumerate(arr_types):
                if nus__jsn not in gdzm__pgm:
                    gdzm__pgm[nus__jsn] = len(gdzm__pgm)
                caxl__lqsfm = gdzm__pgm[nus__jsn]
                krr__mokf.append(caxl__lqsfm)
                huxah__onlj.append(wkhsz__oqjr[caxl__lqsfm])
                wkhsz__oqjr[caxl__lqsfm] += 1
                xnpj__ipjo[caxl__lqsfm].append(i)
        self.block_nums = krr__mokf
        self.block_offsets = huxah__onlj
        self.type_to_blk = gdzm__pgm
        self.block_to_arr_ind = xnpj__ipjo
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
    return TableType(tuple(numba.typeof(qqfu__jzfbw) for qqfu__jzfbw in val
        .arrays))


@register_model(TableType)
class TableTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        if fe_type.has_runtime_cols:
            qnfy__wwqwf = [(f'block_{i}', types.List(nus__jsn)) for i,
                nus__jsn in enumerate(fe_type.arr_types)]
        else:
            qnfy__wwqwf = [(f'block_{caxl__lqsfm}', types.List(nus__jsn)) for
                nus__jsn, caxl__lqsfm in fe_type.type_to_blk.items()]
        qnfy__wwqwf.append(('parent', types.pyobject))
        qnfy__wwqwf.append(('len', types.int64))
        super(TableTypeModel, self).__init__(dmm, fe_type, qnfy__wwqwf)


make_attribute_wrapper(TableType, 'block_0', 'block_0')
make_attribute_wrapper(TableType, 'len', '_len')


@infer_getattr
class TableTypeAttribute(OverloadedKeyAttributeTemplate):
    key = TableType

    def resolve_shape(self, df):
        return types.Tuple([types.int64, types.int64])


@unbox(TableType)
def unbox_table(typ, val, c):
    wqmvf__zmo = c.pyapi.object_getattr_string(val, 'arrays')
    yga__fnaur = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    yga__fnaur.parent = cgutils.get_null_value(yga__fnaur.parent.type)
    dazvo__ood = c.pyapi.make_none()
    kszi__grvhs = c.context.get_constant(types.int64, 0)
    ovyq__vaofr = cgutils.alloca_once_value(c.builder, kszi__grvhs)
    for nus__jsn, caxl__lqsfm in typ.type_to_blk.items():
        rrxn__ymu = c.context.get_constant(types.int64, len(typ.
            block_to_arr_ind[caxl__lqsfm]))
        itnpf__zjbyg, fmoc__hxbd = ListInstance.allocate_ex(c.context, c.
            builder, types.List(nus__jsn), rrxn__ymu)
        fmoc__hxbd.size = rrxn__ymu
        sol__vqu = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[caxl__lqsfm
            ], dtype=np.int64))
        oic__ojh = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, sol__vqu)
        with cgutils.for_range(c.builder, rrxn__ymu) as sjubt__wmv:
            i = sjubt__wmv.index
            cojeb__wipy = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), oic__ojh, i)
            btsvf__lyvt = c.pyapi.long_from_longlong(cojeb__wipy)
            nej__xcgpo = c.pyapi.object_getitem(wqmvf__zmo, btsvf__lyvt)
            yihxk__lihl = c.builder.icmp_unsigned('==', nej__xcgpo, dazvo__ood)
            with c.builder.if_else(yihxk__lihl) as (sbwyy__vohq, alw__oggfv):
                with sbwyy__vohq:
                    vsd__qketa = c.context.get_constant_null(nus__jsn)
                    fmoc__hxbd.inititem(i, vsd__qketa, incref=False)
                with alw__oggfv:
                    gdqrh__moo = c.pyapi.call_method(nej__xcgpo, '__len__', ())
                    rnuoh__yyaf = c.pyapi.long_as_longlong(gdqrh__moo)
                    c.builder.store(rnuoh__yyaf, ovyq__vaofr)
                    c.pyapi.decref(gdqrh__moo)
                    qqfu__jzfbw = c.pyapi.to_native_value(nus__jsn, nej__xcgpo
                        ).value
                    fmoc__hxbd.inititem(i, qqfu__jzfbw, incref=False)
            c.pyapi.decref(nej__xcgpo)
            c.pyapi.decref(btsvf__lyvt)
        setattr(yga__fnaur, f'block_{caxl__lqsfm}', fmoc__hxbd.value)
    yga__fnaur.len = c.builder.load(ovyq__vaofr)
    c.pyapi.decref(wqmvf__zmo)
    c.pyapi.decref(dazvo__ood)
    ufly__mtty = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(yga__fnaur._getvalue(), is_error=ufly__mtty)


@box(TableType)
def box_table(typ, val, c, ensure_unboxed=None):
    from bodo.hiframes.boxing import get_df_obj_column_codegen
    yga__fnaur = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ.has_runtime_cols:
        yvvsd__pic = c.context.get_constant(types.int64, 0)
        for i, nus__jsn in enumerate(typ.arr_types):
            rbveq__whi = getattr(yga__fnaur, f'block_{i}')
            upih__hmho = ListInstance(c.context, c.builder, types.List(
                nus__jsn), rbveq__whi)
            yvvsd__pic = c.builder.add(yvvsd__pic, upih__hmho.size)
        piybe__hpve = c.pyapi.list_new(yvvsd__pic)
        jmu__odh = c.context.get_constant(types.int64, 0)
        for i, nus__jsn in enumerate(typ.arr_types):
            rbveq__whi = getattr(yga__fnaur, f'block_{i}')
            upih__hmho = ListInstance(c.context, c.builder, types.List(
                nus__jsn), rbveq__whi)
            with cgutils.for_range(c.builder, upih__hmho.size) as sjubt__wmv:
                i = sjubt__wmv.index
                qqfu__jzfbw = upih__hmho.getitem(i)
                c.context.nrt.incref(c.builder, nus__jsn, qqfu__jzfbw)
                idx = c.builder.add(jmu__odh, i)
                c.pyapi.list_setitem(piybe__hpve, idx, c.pyapi.
                    from_native_value(nus__jsn, qqfu__jzfbw, c.env_manager))
            jmu__odh = c.builder.add(jmu__odh, upih__hmho.size)
        pwprp__oned = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
        ptr__zscmu = c.pyapi.call_function_objargs(pwprp__oned, (piybe__hpve,))
        c.pyapi.decref(pwprp__oned)
        c.pyapi.decref(piybe__hpve)
        c.context.nrt.decref(c.builder, typ, val)
        return ptr__zscmu
    piybe__hpve = c.pyapi.list_new(c.context.get_constant(types.int64, len(
        typ.arr_types)))
    eder__knvoi = cgutils.is_not_null(c.builder, yga__fnaur.parent)
    if ensure_unboxed is None:
        ensure_unboxed = c.context.get_constant(types.bool_, False)
    for nus__jsn, caxl__lqsfm in typ.type_to_blk.items():
        rbveq__whi = getattr(yga__fnaur, f'block_{caxl__lqsfm}')
        upih__hmho = ListInstance(c.context, c.builder, types.List(nus__jsn
            ), rbveq__whi)
        sol__vqu = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[caxl__lqsfm
            ], dtype=np.int64))
        oic__ojh = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, sol__vqu)
        with cgutils.for_range(c.builder, upih__hmho.size) as sjubt__wmv:
            i = sjubt__wmv.index
            cojeb__wipy = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), oic__ojh, i)
            qqfu__jzfbw = upih__hmho.getitem(i)
            oiv__rrghs = cgutils.alloca_once_value(c.builder, qqfu__jzfbw)
            vtsxf__ruk = cgutils.alloca_once_value(c.builder, c.context.
                get_constant_null(nus__jsn))
            lfxkw__sqzza = is_ll_eq(c.builder, oiv__rrghs, vtsxf__ruk)
            with c.builder.if_else(c.builder.and_(lfxkw__sqzza, c.builder.
                not_(ensure_unboxed))) as (sbwyy__vohq, alw__oggfv):
                with sbwyy__vohq:
                    dazvo__ood = c.pyapi.make_none()
                    c.pyapi.list_setitem(piybe__hpve, cojeb__wipy, dazvo__ood)
                with alw__oggfv:
                    nej__xcgpo = cgutils.alloca_once(c.builder, c.context.
                        get_value_type(types.pyobject))
                    with c.builder.if_else(c.builder.and_(lfxkw__sqzza,
                        eder__knvoi)) as (ocv__hdz, uqp__wxt):
                        with ocv__hdz:
                            mfrku__ate = get_df_obj_column_codegen(c.
                                context, c.builder, c.pyapi, yga__fnaur.
                                parent, cojeb__wipy, nus__jsn)
                            c.builder.store(mfrku__ate, nej__xcgpo)
                        with uqp__wxt:
                            c.context.nrt.incref(c.builder, nus__jsn,
                                qqfu__jzfbw)
                            c.builder.store(c.pyapi.from_native_value(
                                nus__jsn, qqfu__jzfbw, c.env_manager),
                                nej__xcgpo)
                    c.pyapi.list_setitem(piybe__hpve, cojeb__wipy, c.
                        builder.load(nej__xcgpo))
    pwprp__oned = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
    ptr__zscmu = c.pyapi.call_function_objargs(pwprp__oned, (piybe__hpve,))
    c.pyapi.decref(pwprp__oned)
    c.pyapi.decref(piybe__hpve)
    c.context.nrt.decref(c.builder, typ, val)
    return ptr__zscmu


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
        yga__fnaur = cgutils.create_struct_proxy(table_type)(context,
            builder, table_arg)
        rrn__lrqmc = context.get_constant(types.int64, 0)
        for i, nus__jsn in enumerate(table_type.arr_types):
            rbveq__whi = getattr(yga__fnaur, f'block_{i}')
            upih__hmho = ListInstance(context, builder, types.List(nus__jsn
                ), rbveq__whi)
            rrn__lrqmc = builder.add(rrn__lrqmc, upih__hmho.size)
        return rrn__lrqmc
    sig = types.int64(table_type)
    return sig, codegen


def get_table_data_codegen(context, builder, table_arg, col_ind, table_type):
    arr_type = table_type.arr_types[col_ind]
    yga__fnaur = cgutils.create_struct_proxy(table_type)(context, builder,
        table_arg)
    caxl__lqsfm = table_type.block_nums[col_ind]
    nrf__dlc = table_type.block_offsets[col_ind]
    rbveq__whi = getattr(yga__fnaur, f'block_{caxl__lqsfm}')
    upih__hmho = ListInstance(context, builder, types.List(arr_type),
        rbveq__whi)
    qqfu__jzfbw = upih__hmho.getitem(nrf__dlc)
    return qqfu__jzfbw


@intrinsic
def get_table_data(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, itnpf__zjbyg = args
        qqfu__jzfbw = get_table_data_codegen(context, builder, table_arg,
            col_ind, table_type)
        return impl_ret_borrowed(context, builder, arr_type, qqfu__jzfbw)
    sig = arr_type(table_type, ind_typ)
    return sig, codegen


@intrinsic
def del_column(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, itnpf__zjbyg = args
        yga__fnaur = cgutils.create_struct_proxy(table_type)(context,
            builder, table_arg)
        caxl__lqsfm = table_type.block_nums[col_ind]
        nrf__dlc = table_type.block_offsets[col_ind]
        rbveq__whi = getattr(yga__fnaur, f'block_{caxl__lqsfm}')
        upih__hmho = ListInstance(context, builder, types.List(arr_type),
            rbveq__whi)
        qqfu__jzfbw = upih__hmho.getitem(nrf__dlc)
        context.nrt.decref(builder, arr_type, qqfu__jzfbw)
        vsd__qketa = context.get_constant_null(arr_type)
        upih__hmho.inititem(nrf__dlc, vsd__qketa, incref=False)
    sig = types.void(table_type, ind_typ)
    return sig, codegen


def set_table_data_codegen(context, builder, in_table_type, in_table,
    out_table_type, arr_type, arr_arg, col_ind, is_new_col):
    in_table = cgutils.create_struct_proxy(in_table_type)(context, builder,
        in_table)
    out_table = cgutils.create_struct_proxy(out_table_type)(context, builder)
    out_table.len = in_table.len
    out_table.parent = in_table.parent
    kszi__grvhs = context.get_constant(types.int64, 0)
    zoxw__ssx = context.get_constant(types.int64, 1)
    mwqta__bbr = arr_type not in in_table_type.type_to_blk
    for nus__jsn, caxl__lqsfm in out_table_type.type_to_blk.items():
        if nus__jsn in in_table_type.type_to_blk:
            anmzw__hoq = in_table_type.type_to_blk[nus__jsn]
            fmoc__hxbd = ListInstance(context, builder, types.List(nus__jsn
                ), getattr(in_table, f'block_{anmzw__hoq}'))
            context.nrt.incref(builder, types.List(nus__jsn), fmoc__hxbd.value)
            setattr(out_table, f'block_{caxl__lqsfm}', fmoc__hxbd.value)
    if mwqta__bbr:
        itnpf__zjbyg, fmoc__hxbd = ListInstance.allocate_ex(context,
            builder, types.List(arr_type), zoxw__ssx)
        fmoc__hxbd.size = zoxw__ssx
        fmoc__hxbd.inititem(kszi__grvhs, arr_arg, incref=True)
        caxl__lqsfm = out_table_type.type_to_blk[arr_type]
        setattr(out_table, f'block_{caxl__lqsfm}', fmoc__hxbd.value)
        if not is_new_col:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
    else:
        caxl__lqsfm = out_table_type.type_to_blk[arr_type]
        fmoc__hxbd = ListInstance(context, builder, types.List(arr_type),
            getattr(out_table, f'block_{caxl__lqsfm}'))
        if is_new_col:
            n = fmoc__hxbd.size
            npjp__yiya = builder.add(n, zoxw__ssx)
            fmoc__hxbd.resize(npjp__yiya)
            fmoc__hxbd.inititem(n, arr_arg, incref=True)
        elif arr_type == in_table_type.arr_types[col_ind]:
            kiki__jfu = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            fmoc__hxbd.setitem(kiki__jfu, arr_arg, True)
        else:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
            kiki__jfu = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            n = fmoc__hxbd.size
            npjp__yiya = builder.add(n, zoxw__ssx)
            fmoc__hxbd.resize(npjp__yiya)
            context.nrt.incref(builder, arr_type, fmoc__hxbd.getitem(kiki__jfu)
                )
            fmoc__hxbd.move(builder.add(kiki__jfu, zoxw__ssx), kiki__jfu,
                builder.sub(n, kiki__jfu))
            fmoc__hxbd.setitem(kiki__jfu, arr_arg, incref=True)
    return out_table._getvalue()


def _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
    context, builder):
    moy__wwql = in_table_type.arr_types[col_ind]
    if moy__wwql in out_table_type.type_to_blk:
        caxl__lqsfm = out_table_type.type_to_blk[moy__wwql]
        xqlig__pgqzx = getattr(out_table, f'block_{caxl__lqsfm}')
        gvr__yvxt = types.List(moy__wwql)
        kiki__jfu = context.get_constant(types.int64, in_table_type.
            block_offsets[col_ind])
        dnnd__ibhl = gvr__yvxt.dtype(gvr__yvxt, types.intp)
        tdg__gabq = context.compile_internal(builder, lambda lst, i: lst.
            pop(i), dnnd__ibhl, (xqlig__pgqzx, kiki__jfu))
        context.nrt.decref(builder, moy__wwql, tdg__gabq)


@intrinsic
def set_table_data(typingctx, table_type, ind_type, arr_type):
    assert isinstance(table_type, TableType), 'invalid input to set_table_data'
    assert is_overload_constant_int(ind_type
        ), 'set_table_data expects const index'
    col_ind = get_overload_const_int(ind_type)
    is_new_col = col_ind == len(table_type.arr_types)
    esnsf__wokl = list(table_type.arr_types)
    if is_new_col:
        esnsf__wokl.append(arr_type)
    else:
        esnsf__wokl[col_ind] = arr_type
    out_table_type = TableType(tuple(esnsf__wokl))

    def codegen(context, builder, sig, args):
        table_arg, itnpf__zjbyg, rwszw__hhomg = args
        out_table = set_table_data_codegen(context, builder, table_type,
            table_arg, out_table_type, arr_type, rwszw__hhomg, col_ind,
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
    quh__xjjd = args[0]
    if equiv_set.has_shape(quh__xjjd):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            quh__xjjd)[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_get_table_data = (
    get_table_data_equiv)


@lower_constant(TableType)
def lower_constant_table(context, builder, table_type, pyval):
    foud__pakx = []
    for nus__jsn, caxl__lqsfm in table_type.type_to_blk.items():
        zodu__buxss = len(table_type.block_to_arr_ind[caxl__lqsfm])
        yqayv__xefk = []
        for i in range(zodu__buxss):
            cojeb__wipy = table_type.block_to_arr_ind[caxl__lqsfm][i]
            yqayv__xefk.append(pyval.arrays[cojeb__wipy])
        foud__pakx.append(context.get_constant_generic(builder, types.List(
            nus__jsn), yqayv__xefk))
    qbgat__inteh = context.get_constant_null(types.pyobject)
    xxjip__bst = context.get_constant(types.int64, 0 if len(pyval.arrays) ==
        0 else len(pyval.arrays[0]))
    return lir.Constant.literal_struct(foud__pakx + [qbgat__inteh, xxjip__bst])


@intrinsic
def init_table(typingctx, table_type, to_str_if_dict_t):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    out_table_type = table_type
    if is_overload_true(to_str_if_dict_t):
        out_table_type = to_str_arr_if_dict_array(table_type)

    def codegen(context, builder, sig, args):
        yga__fnaur = cgutils.create_struct_proxy(out_table_type)(context,
            builder)
        for nus__jsn, caxl__lqsfm in out_table_type.type_to_blk.items():
            wmaz__znnhl = context.get_constant_null(types.List(nus__jsn))
            setattr(yga__fnaur, f'block_{caxl__lqsfm}', wmaz__znnhl)
        return yga__fnaur._getvalue()
    sig = out_table_type(table_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def init_table_from_lists(typingctx, tuple_of_lists_type, table_type):
    assert isinstance(tuple_of_lists_type, types.BaseTuple
        ), 'Tuple of data expected'
    ivqxm__htgd = {}
    for i, typ in enumerate(tuple_of_lists_type):
        assert isinstance(typ, types.List), 'Each tuple element must be a list'
        ivqxm__htgd[typ.dtype] = i
    zjfm__eaopd = table_type.instance_type if isinstance(table_type, types.
        TypeRef) else table_type
    assert isinstance(zjfm__eaopd, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        uaco__yolk, itnpf__zjbyg = args
        yga__fnaur = cgutils.create_struct_proxy(zjfm__eaopd)(context, builder)
        for nus__jsn, caxl__lqsfm in zjfm__eaopd.type_to_blk.items():
            idx = ivqxm__htgd[nus__jsn]
            qjw__sjwj = signature(types.List(nus__jsn), tuple_of_lists_type,
                types.literal(idx))
            nqgma__zuhq = uaco__yolk, idx
            kiat__lbb = numba.cpython.tupleobj.static_getitem_tuple(context,
                builder, qjw__sjwj, nqgma__zuhq)
            setattr(yga__fnaur, f'block_{caxl__lqsfm}', kiat__lbb)
        return yga__fnaur._getvalue()
    sig = zjfm__eaopd(tuple_of_lists_type, table_type)
    return sig, codegen


@intrinsic
def get_table_block(typingctx, table_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_int(blk_type)
    caxl__lqsfm = get_overload_const_int(blk_type)
    arr_type = None
    for nus__jsn, bjy__vksjk in table_type.type_to_blk.items():
        if bjy__vksjk == caxl__lqsfm:
            arr_type = nus__jsn
            break
    assert arr_type is not None, 'invalid table type block'
    tja__qxyk = types.List(arr_type)

    def codegen(context, builder, sig, args):
        yga__fnaur = cgutils.create_struct_proxy(table_type)(context,
            builder, args[0])
        rbveq__whi = getattr(yga__fnaur, f'block_{caxl__lqsfm}')
        return impl_ret_borrowed(context, builder, tja__qxyk, rbveq__whi)
    sig = tja__qxyk(table_type, blk_type)
    return sig, codegen


@intrinsic
def ensure_table_unboxed(typingctx, table_type, used_cols_typ):

    def codegen(context, builder, sig, args):
        table_arg, fewnw__iwudb = args
        pzgsi__owsm = context.get_python_api(builder)
        rvcd__syqg = used_cols_typ == types.none
        if not rvcd__syqg:
            litmb__vjz = numba.cpython.setobj.SetInstance(context, builder,
                types.Set(types.int64), fewnw__iwudb)
        yga__fnaur = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, table_arg)
        eder__knvoi = cgutils.is_not_null(builder, yga__fnaur.parent)
        for nus__jsn, caxl__lqsfm in table_type.type_to_blk.items():
            rrxn__ymu = context.get_constant(types.int64, len(table_type.
                block_to_arr_ind[caxl__lqsfm]))
            sol__vqu = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(table_type.block_to_arr_ind[
                caxl__lqsfm], dtype=np.int64))
            oic__ojh = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, sol__vqu)
            rbveq__whi = getattr(yga__fnaur, f'block_{caxl__lqsfm}')
            with cgutils.for_range(builder, rrxn__ymu) as sjubt__wmv:
                i = sjubt__wmv.index
                cojeb__wipy = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'), oic__ojh, i)
                ffsya__mwff = types.none(table_type, types.List(nus__jsn),
                    types.int64, types.int64)
                ywci__kzz = table_arg, rbveq__whi, i, cojeb__wipy
                if rvcd__syqg:
                    ensure_column_unboxed_codegen(context, builder,
                        ffsya__mwff, ywci__kzz)
                else:
                    hdo__zoj = litmb__vjz.contains(cojeb__wipy)
                    with builder.if_then(hdo__zoj):
                        ensure_column_unboxed_codegen(context, builder,
                            ffsya__mwff, ywci__kzz)
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
    table_arg, apqg__hmajr, ezktl__ggpk, zbe__dadx = args
    pzgsi__owsm = context.get_python_api(builder)
    yga__fnaur = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        table_arg)
    eder__knvoi = cgutils.is_not_null(builder, yga__fnaur.parent)
    upih__hmho = ListInstance(context, builder, sig.args[1], apqg__hmajr)
    dsysv__uzf = upih__hmho.getitem(ezktl__ggpk)
    oiv__rrghs = cgutils.alloca_once_value(builder, dsysv__uzf)
    vtsxf__ruk = cgutils.alloca_once_value(builder, context.
        get_constant_null(sig.args[1].dtype))
    lfxkw__sqzza = is_ll_eq(builder, oiv__rrghs, vtsxf__ruk)
    with builder.if_then(lfxkw__sqzza):
        with builder.if_else(eder__knvoi) as (sbwyy__vohq, alw__oggfv):
            with sbwyy__vohq:
                nej__xcgpo = get_df_obj_column_codegen(context, builder,
                    pzgsi__owsm, yga__fnaur.parent, zbe__dadx, sig.args[1].
                    dtype)
                qqfu__jzfbw = pzgsi__owsm.to_native_value(sig.args[1].dtype,
                    nej__xcgpo).value
                upih__hmho.inititem(ezktl__ggpk, qqfu__jzfbw, incref=False)
                pzgsi__owsm.decref(nej__xcgpo)
            with alw__oggfv:
                context.call_conv.return_user_exc(builder, BodoError, (
                    'unexpected null table column',))


@intrinsic
def set_table_block(typingctx, table_type, arr_list_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert isinstance(arr_list_type, types.List), 'list type expected'
    assert is_overload_constant_int(blk_type), 'blk should be const int'
    caxl__lqsfm = get_overload_const_int(blk_type)

    def codegen(context, builder, sig, args):
        table_arg, lemny__yapfi, itnpf__zjbyg = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        setattr(in_table, f'block_{caxl__lqsfm}', lemny__yapfi)
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, arr_list_type, blk_type)
    return sig, codegen


@intrinsic
def set_table_len(typingctx, table_type, l_type):
    assert isinstance(table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        table_arg, ezqo__copg = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        in_table.len = ezqo__copg
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, l_type)
    return sig, codegen


@intrinsic
def alloc_list_like(typingctx, list_type, to_str_if_dict_t):
    assert isinstance(list_type, types.List), 'list type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    tja__qxyk = list_type
    if is_overload_true(to_str_if_dict_t):
        tja__qxyk = types.List(to_str_arr_if_dict_array(list_type.dtype))

    def codegen(context, builder, sig, args):
        pnyly__xozd = ListInstance(context, builder, list_type, args[0])
        mqd__olew = pnyly__xozd.size
        itnpf__zjbyg, fmoc__hxbd = ListInstance.allocate_ex(context,
            builder, tja__qxyk, mqd__olew)
        fmoc__hxbd.size = mqd__olew
        return fmoc__hxbd.value
    sig = tja__qxyk(list_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def alloc_empty_list_type(typingctx, size_typ, data_typ=None):
    assert isinstance(size_typ, types.Integer), 'Size must be an integer'
    fdey__xgq = data_typ.instance_type if isinstance(data_typ, types.TypeRef
        ) else data_typ
    list_type = types.List(fdey__xgq)

    def codegen(context, builder, sig, args):
        mqd__olew, itnpf__zjbyg = args
        itnpf__zjbyg, fmoc__hxbd = ListInstance.allocate_ex(context,
            builder, list_type, mqd__olew)
        fmoc__hxbd.size = mqd__olew
        return fmoc__hxbd.value
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
        nlcwj__cbl = numba.cpython.unicode._normalize_slice(idx, n)
        return numba.cpython.unicode._slice_span(nlcwj__cbl)
    return impl


def gen_table_filter(T, used_cols=None):
    from bodo.utils.conversion import ensure_contig_if_np
    dnsue__mxhuz = {'init_table': init_table, 'get_table_block':
        get_table_block, 'ensure_column_unboxed': ensure_column_unboxed,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'alloc_list_like': alloc_list_like, '_get_idx_length':
        _get_idx_length, 'ensure_contig_if_np': ensure_contig_if_np}
    if used_cols is not None:
        dnsue__mxhuz['used_cols'] = used_cols
    hxayx__qduum = 'def impl(T, idx):\n'
    hxayx__qduum += f'  T2 = init_table(T, False)\n'
    hxayx__qduum += f'  l = 0\n'
    if used_cols is not None and len(used_cols) == 0:
        hxayx__qduum += f'  l = _get_idx_length(idx, len(T))\n'
        hxayx__qduum += f'  T2 = set_table_len(T2, l)\n'
        hxayx__qduum += f'  return T2\n'
        ievws__ekh = {}
        exec(hxayx__qduum, dnsue__mxhuz, ievws__ekh)
        return ievws__ekh['impl']
    if used_cols is not None:
        hxayx__qduum += f'  used_set = set(used_cols)\n'
    for caxl__lqsfm in T.type_to_blk.values():
        dnsue__mxhuz[f'arr_inds_{caxl__lqsfm}'] = np.array(T.
            block_to_arr_ind[caxl__lqsfm], dtype=np.int64)
        hxayx__qduum += (
            f'  arr_list_{caxl__lqsfm} = get_table_block(T, {caxl__lqsfm})\n')
        hxayx__qduum += f"""  out_arr_list_{caxl__lqsfm} = alloc_list_like(arr_list_{caxl__lqsfm}, False)
"""
        hxayx__qduum += f'  for i in range(len(arr_list_{caxl__lqsfm})):\n'
        hxayx__qduum += (
            f'    arr_ind_{caxl__lqsfm} = arr_inds_{caxl__lqsfm}[i]\n')
        if used_cols is not None:
            hxayx__qduum += (
                f'    if arr_ind_{caxl__lqsfm} not in used_set: continue\n')
        hxayx__qduum += f"""    ensure_column_unboxed(T, arr_list_{caxl__lqsfm}, i, arr_ind_{caxl__lqsfm})
"""
        hxayx__qduum += f"""    out_arr_{caxl__lqsfm} = ensure_contig_if_np(arr_list_{caxl__lqsfm}[i][idx])
"""
        hxayx__qduum += f'    l = len(out_arr_{caxl__lqsfm})\n'
        hxayx__qduum += (
            f'    out_arr_list_{caxl__lqsfm}[i] = out_arr_{caxl__lqsfm}\n')
        hxayx__qduum += (
            f'  T2 = set_table_block(T2, out_arr_list_{caxl__lqsfm}, {caxl__lqsfm})\n'
            )
    hxayx__qduum += f'  T2 = set_table_len(T2, l)\n'
    hxayx__qduum += f'  return T2\n'
    ievws__ekh = {}
    exec(hxayx__qduum, dnsue__mxhuz, ievws__ekh)
    return ievws__ekh['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def decode_if_dict_table(T):
    hxayx__qduum = 'def impl(T):\n'
    hxayx__qduum += f'  T2 = init_table(T, True)\n'
    hxayx__qduum += f'  l = len(T)\n'
    dnsue__mxhuz = {'init_table': init_table, 'get_table_block':
        get_table_block, 'ensure_column_unboxed': ensure_column_unboxed,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'alloc_list_like': alloc_list_like, 'decode_if_dict_array':
        decode_if_dict_array}
    for caxl__lqsfm in T.type_to_blk.values():
        dnsue__mxhuz[f'arr_inds_{caxl__lqsfm}'] = np.array(T.
            block_to_arr_ind[caxl__lqsfm], dtype=np.int64)
        hxayx__qduum += (
            f'  arr_list_{caxl__lqsfm} = get_table_block(T, {caxl__lqsfm})\n')
        hxayx__qduum += f"""  out_arr_list_{caxl__lqsfm} = alloc_list_like(arr_list_{caxl__lqsfm}, True)
"""
        hxayx__qduum += f'  for i in range(len(arr_list_{caxl__lqsfm})):\n'
        hxayx__qduum += (
            f'    arr_ind_{caxl__lqsfm} = arr_inds_{caxl__lqsfm}[i]\n')
        hxayx__qduum += f"""    ensure_column_unboxed(T, arr_list_{caxl__lqsfm}, i, arr_ind_{caxl__lqsfm})
"""
        hxayx__qduum += f"""    out_arr_{caxl__lqsfm} = decode_if_dict_array(arr_list_{caxl__lqsfm}[i])
"""
        hxayx__qduum += (
            f'    out_arr_list_{caxl__lqsfm}[i] = out_arr_{caxl__lqsfm}\n')
        hxayx__qduum += (
            f'  T2 = set_table_block(T2, out_arr_list_{caxl__lqsfm}, {caxl__lqsfm})\n'
            )
    hxayx__qduum += f'  T2 = set_table_len(T2, l)\n'
    hxayx__qduum += f'  return T2\n'
    ievws__ekh = {}
    exec(hxayx__qduum, dnsue__mxhuz, ievws__ekh)
    return ievws__ekh['impl']


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
        mfae__kdn = [arr_list_tup_typ.dtype.dtype] * len(arr_list_tup_typ)
    else:
        mfae__kdn = []
        for typ in arr_list_tup_typ:
            if typ.dtype == types.undefined:
                return
            mfae__kdn.append(typ.dtype)
    assert isinstance(nrows_typ, types.Integer
        ), 'init_runtime_table_from_lists requires an integer length'

    def codegen(context, builder, sig, args):
        lgcf__valdq, urr__mfvb = args
        yga__fnaur = cgutils.create_struct_proxy(table_type)(context, builder)
        yga__fnaur.len = urr__mfvb
        foud__pakx = cgutils.unpack_tuple(builder, lgcf__valdq)
        for i, rbveq__whi in enumerate(foud__pakx):
            setattr(yga__fnaur, f'block_{i}', rbveq__whi)
            context.nrt.incref(builder, types.List(mfae__kdn[i]), rbveq__whi)
        return yga__fnaur._getvalue()
    table_type = TableType(tuple(mfae__kdn), True)
    sig = table_type(arr_list_tup_typ, nrows_typ)
    return sig, codegen
