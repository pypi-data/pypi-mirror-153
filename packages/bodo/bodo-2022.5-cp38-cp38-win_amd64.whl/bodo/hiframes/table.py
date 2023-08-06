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
            lkjj__qgq = 0
            ckx__togjc = []
            for i in range(usecols[-1] + 1):
                if i == usecols[lkjj__qgq]:
                    ckx__togjc.append(arrs[lkjj__qgq])
                    lkjj__qgq += 1
                else:
                    ckx__togjc.append(None)
            for ykpan__bipv in range(usecols[-1] + 1, num_arrs):
                ckx__togjc.append(None)
            self.arrays = ckx__togjc
        else:
            self.arrays = arrs
        self.block_0 = arrs

    def __eq__(self, other):
        return isinstance(other, Table) and len(self.arrays) == len(other.
            arrays) and all((gax__xqoc == swx__tez).all() for gax__xqoc,
            swx__tez in zip(self.arrays, other.arrays))

    def __str__(self) ->str:
        return str(self.arrays)

    def to_pandas(self, index=None):
        sbo__jtbw = len(self.arrays)
        aibny__lzui = dict(zip(range(sbo__jtbw), self.arrays))
        df = pd.DataFrame(aibny__lzui, index)
        return df


class TableType(types.ArrayCompatible):

    def __init__(self, arr_types, has_runtime_cols=False):
        self.arr_types = arr_types
        self.has_runtime_cols = has_runtime_cols
        iaasu__egfx = []
        jcpw__zvqwa = []
        tcsz__ctk = {}
        uqe__oxpuf = defaultdict(int)
        ffjci__jahn = defaultdict(list)
        if not has_runtime_cols:
            for i, lmx__gkgb in enumerate(arr_types):
                if lmx__gkgb not in tcsz__ctk:
                    tcsz__ctk[lmx__gkgb] = len(tcsz__ctk)
                wvtz__fbipk = tcsz__ctk[lmx__gkgb]
                iaasu__egfx.append(wvtz__fbipk)
                jcpw__zvqwa.append(uqe__oxpuf[wvtz__fbipk])
                uqe__oxpuf[wvtz__fbipk] += 1
                ffjci__jahn[wvtz__fbipk].append(i)
        self.block_nums = iaasu__egfx
        self.block_offsets = jcpw__zvqwa
        self.type_to_blk = tcsz__ctk
        self.block_to_arr_ind = ffjci__jahn
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
    return TableType(tuple(numba.typeof(belc__xft) for belc__xft in val.arrays)
        )


@register_model(TableType)
class TableTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        if fe_type.has_runtime_cols:
            tvhi__fqd = [(f'block_{i}', types.List(lmx__gkgb)) for i,
                lmx__gkgb in enumerate(fe_type.arr_types)]
        else:
            tvhi__fqd = [(f'block_{wvtz__fbipk}', types.List(lmx__gkgb)) for
                lmx__gkgb, wvtz__fbipk in fe_type.type_to_blk.items()]
        tvhi__fqd.append(('parent', types.pyobject))
        tvhi__fqd.append(('len', types.int64))
        super(TableTypeModel, self).__init__(dmm, fe_type, tvhi__fqd)


make_attribute_wrapper(TableType, 'block_0', 'block_0')
make_attribute_wrapper(TableType, 'len', '_len')


@infer_getattr
class TableTypeAttribute(OverloadedKeyAttributeTemplate):
    key = TableType

    def resolve_shape(self, df):
        return types.Tuple([types.int64, types.int64])


@unbox(TableType)
def unbox_table(typ, val, c):
    fdtl__gmcx = c.pyapi.object_getattr_string(val, 'arrays')
    psmmr__tfjo = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    psmmr__tfjo.parent = cgutils.get_null_value(psmmr__tfjo.parent.type)
    yojxh__staw = c.pyapi.make_none()
    kthl__kgswu = c.context.get_constant(types.int64, 0)
    tzhfl__jkeu = cgutils.alloca_once_value(c.builder, kthl__kgswu)
    for lmx__gkgb, wvtz__fbipk in typ.type_to_blk.items():
        ikkth__zqe = c.context.get_constant(types.int64, len(typ.
            block_to_arr_ind[wvtz__fbipk]))
        ykpan__bipv, fynw__lxrh = ListInstance.allocate_ex(c.context, c.
            builder, types.List(lmx__gkgb), ikkth__zqe)
        fynw__lxrh.size = ikkth__zqe
        yca__cxx = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[wvtz__fbipk
            ], dtype=np.int64))
        pwwn__roqfc = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, yca__cxx)
        with cgutils.for_range(c.builder, ikkth__zqe) as kyykh__hvqx:
            i = kyykh__hvqx.index
            ohbzp__bxj = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), pwwn__roqfc, i)
            owi__pwdzx = c.pyapi.long_from_longlong(ohbzp__bxj)
            hwls__rvewt = c.pyapi.object_getitem(fdtl__gmcx, owi__pwdzx)
            ejkiy__lsmro = c.builder.icmp_unsigned('==', hwls__rvewt,
                yojxh__staw)
            with c.builder.if_else(ejkiy__lsmro) as (zcggp__kmp, odo__pkb):
                with zcggp__kmp:
                    hmu__jatq = c.context.get_constant_null(lmx__gkgb)
                    fynw__lxrh.inititem(i, hmu__jatq, incref=False)
                with odo__pkb:
                    kih__iam = c.pyapi.call_method(hwls__rvewt, '__len__', ())
                    ipfw__lkf = c.pyapi.long_as_longlong(kih__iam)
                    c.builder.store(ipfw__lkf, tzhfl__jkeu)
                    c.pyapi.decref(kih__iam)
                    belc__xft = c.pyapi.to_native_value(lmx__gkgb, hwls__rvewt
                        ).value
                    fynw__lxrh.inititem(i, belc__xft, incref=False)
            c.pyapi.decref(hwls__rvewt)
            c.pyapi.decref(owi__pwdzx)
        setattr(psmmr__tfjo, f'block_{wvtz__fbipk}', fynw__lxrh.value)
    psmmr__tfjo.len = c.builder.load(tzhfl__jkeu)
    c.pyapi.decref(fdtl__gmcx)
    c.pyapi.decref(yojxh__staw)
    ecew__corj = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(psmmr__tfjo._getvalue(), is_error=ecew__corj)


@box(TableType)
def box_table(typ, val, c, ensure_unboxed=None):
    from bodo.hiframes.boxing import get_df_obj_column_codegen
    psmmr__tfjo = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ.has_runtime_cols:
        bfdm__dvkys = c.context.get_constant(types.int64, 0)
        for i, lmx__gkgb in enumerate(typ.arr_types):
            ckx__togjc = getattr(psmmr__tfjo, f'block_{i}')
            tgakn__pcmkh = ListInstance(c.context, c.builder, types.List(
                lmx__gkgb), ckx__togjc)
            bfdm__dvkys = c.builder.add(bfdm__dvkys, tgakn__pcmkh.size)
        cpep__gqpvj = c.pyapi.list_new(bfdm__dvkys)
        ufy__eyctc = c.context.get_constant(types.int64, 0)
        for i, lmx__gkgb in enumerate(typ.arr_types):
            ckx__togjc = getattr(psmmr__tfjo, f'block_{i}')
            tgakn__pcmkh = ListInstance(c.context, c.builder, types.List(
                lmx__gkgb), ckx__togjc)
            with cgutils.for_range(c.builder, tgakn__pcmkh.size
                ) as kyykh__hvqx:
                i = kyykh__hvqx.index
                belc__xft = tgakn__pcmkh.getitem(i)
                c.context.nrt.incref(c.builder, lmx__gkgb, belc__xft)
                idx = c.builder.add(ufy__eyctc, i)
                c.pyapi.list_setitem(cpep__gqpvj, idx, c.pyapi.
                    from_native_value(lmx__gkgb, belc__xft, c.env_manager))
            ufy__eyctc = c.builder.add(ufy__eyctc, tgakn__pcmkh.size)
        yjox__vjnmv = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
        angqo__gvhrj = c.pyapi.call_function_objargs(yjox__vjnmv, (
            cpep__gqpvj,))
        c.pyapi.decref(yjox__vjnmv)
        c.pyapi.decref(cpep__gqpvj)
        c.context.nrt.decref(c.builder, typ, val)
        return angqo__gvhrj
    cpep__gqpvj = c.pyapi.list_new(c.context.get_constant(types.int64, len(
        typ.arr_types)))
    bna__dlz = cgutils.is_not_null(c.builder, psmmr__tfjo.parent)
    if ensure_unboxed is None:
        ensure_unboxed = c.context.get_constant(types.bool_, False)
    for lmx__gkgb, wvtz__fbipk in typ.type_to_blk.items():
        ckx__togjc = getattr(psmmr__tfjo, f'block_{wvtz__fbipk}')
        tgakn__pcmkh = ListInstance(c.context, c.builder, types.List(
            lmx__gkgb), ckx__togjc)
        yca__cxx = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[wvtz__fbipk
            ], dtype=np.int64))
        pwwn__roqfc = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, yca__cxx)
        with cgutils.for_range(c.builder, tgakn__pcmkh.size) as kyykh__hvqx:
            i = kyykh__hvqx.index
            ohbzp__bxj = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), pwwn__roqfc, i)
            belc__xft = tgakn__pcmkh.getitem(i)
            qza__ccbi = cgutils.alloca_once_value(c.builder, belc__xft)
            aazc__pjpu = cgutils.alloca_once_value(c.builder, c.context.
                get_constant_null(lmx__gkgb))
            fazkd__uikn = is_ll_eq(c.builder, qza__ccbi, aazc__pjpu)
            with c.builder.if_else(c.builder.and_(fazkd__uikn, c.builder.
                not_(ensure_unboxed))) as (zcggp__kmp, odo__pkb):
                with zcggp__kmp:
                    yojxh__staw = c.pyapi.make_none()
                    c.pyapi.list_setitem(cpep__gqpvj, ohbzp__bxj, yojxh__staw)
                with odo__pkb:
                    hwls__rvewt = cgutils.alloca_once(c.builder, c.context.
                        get_value_type(types.pyobject))
                    with c.builder.if_else(c.builder.and_(fazkd__uikn,
                        bna__dlz)) as (wqwse__nekcw, nyn__kndw):
                        with wqwse__nekcw:
                            kaywg__idr = get_df_obj_column_codegen(c.
                                context, c.builder, c.pyapi, psmmr__tfjo.
                                parent, ohbzp__bxj, lmx__gkgb)
                            c.builder.store(kaywg__idr, hwls__rvewt)
                        with nyn__kndw:
                            c.context.nrt.incref(c.builder, lmx__gkgb,
                                belc__xft)
                            c.builder.store(c.pyapi.from_native_value(
                                lmx__gkgb, belc__xft, c.env_manager),
                                hwls__rvewt)
                    c.pyapi.list_setitem(cpep__gqpvj, ohbzp__bxj, c.builder
                        .load(hwls__rvewt))
    yjox__vjnmv = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
    angqo__gvhrj = c.pyapi.call_function_objargs(yjox__vjnmv, (cpep__gqpvj,))
    c.pyapi.decref(yjox__vjnmv)
    c.pyapi.decref(cpep__gqpvj)
    c.context.nrt.decref(c.builder, typ, val)
    return angqo__gvhrj


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
        psmmr__tfjo = cgutils.create_struct_proxy(table_type)(context,
            builder, table_arg)
        ykbag__cgph = context.get_constant(types.int64, 0)
        for i, lmx__gkgb in enumerate(table_type.arr_types):
            ckx__togjc = getattr(psmmr__tfjo, f'block_{i}')
            tgakn__pcmkh = ListInstance(context, builder, types.List(
                lmx__gkgb), ckx__togjc)
            ykbag__cgph = builder.add(ykbag__cgph, tgakn__pcmkh.size)
        return ykbag__cgph
    sig = types.int64(table_type)
    return sig, codegen


def get_table_data_codegen(context, builder, table_arg, col_ind, table_type):
    arr_type = table_type.arr_types[col_ind]
    psmmr__tfjo = cgutils.create_struct_proxy(table_type)(context, builder,
        table_arg)
    wvtz__fbipk = table_type.block_nums[col_ind]
    qauc__lfc = table_type.block_offsets[col_ind]
    ckx__togjc = getattr(psmmr__tfjo, f'block_{wvtz__fbipk}')
    tgakn__pcmkh = ListInstance(context, builder, types.List(arr_type),
        ckx__togjc)
    belc__xft = tgakn__pcmkh.getitem(qauc__lfc)
    return belc__xft


@intrinsic
def get_table_data(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, ykpan__bipv = args
        belc__xft = get_table_data_codegen(context, builder, table_arg,
            col_ind, table_type)
        return impl_ret_borrowed(context, builder, arr_type, belc__xft)
    sig = arr_type(table_type, ind_typ)
    return sig, codegen


@intrinsic
def del_column(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, ykpan__bipv = args
        psmmr__tfjo = cgutils.create_struct_proxy(table_type)(context,
            builder, table_arg)
        wvtz__fbipk = table_type.block_nums[col_ind]
        qauc__lfc = table_type.block_offsets[col_ind]
        ckx__togjc = getattr(psmmr__tfjo, f'block_{wvtz__fbipk}')
        tgakn__pcmkh = ListInstance(context, builder, types.List(arr_type),
            ckx__togjc)
        belc__xft = tgakn__pcmkh.getitem(qauc__lfc)
        context.nrt.decref(builder, arr_type, belc__xft)
        hmu__jatq = context.get_constant_null(arr_type)
        tgakn__pcmkh.inititem(qauc__lfc, hmu__jatq, incref=False)
    sig = types.void(table_type, ind_typ)
    return sig, codegen


def set_table_data_codegen(context, builder, in_table_type, in_table,
    out_table_type, arr_type, arr_arg, col_ind, is_new_col):
    in_table = cgutils.create_struct_proxy(in_table_type)(context, builder,
        in_table)
    out_table = cgutils.create_struct_proxy(out_table_type)(context, builder)
    out_table.len = in_table.len
    out_table.parent = in_table.parent
    kthl__kgswu = context.get_constant(types.int64, 0)
    rvmc__dwwwt = context.get_constant(types.int64, 1)
    ryl__mny = arr_type not in in_table_type.type_to_blk
    for lmx__gkgb, wvtz__fbipk in out_table_type.type_to_blk.items():
        if lmx__gkgb in in_table_type.type_to_blk:
            tiyos__uxgcl = in_table_type.type_to_blk[lmx__gkgb]
            fynw__lxrh = ListInstance(context, builder, types.List(
                lmx__gkgb), getattr(in_table, f'block_{tiyos__uxgcl}'))
            context.nrt.incref(builder, types.List(lmx__gkgb), fynw__lxrh.value
                )
            setattr(out_table, f'block_{wvtz__fbipk}', fynw__lxrh.value)
    if ryl__mny:
        ykpan__bipv, fynw__lxrh = ListInstance.allocate_ex(context, builder,
            types.List(arr_type), rvmc__dwwwt)
        fynw__lxrh.size = rvmc__dwwwt
        fynw__lxrh.inititem(kthl__kgswu, arr_arg, incref=True)
        wvtz__fbipk = out_table_type.type_to_blk[arr_type]
        setattr(out_table, f'block_{wvtz__fbipk}', fynw__lxrh.value)
        if not is_new_col:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
    else:
        wvtz__fbipk = out_table_type.type_to_blk[arr_type]
        fynw__lxrh = ListInstance(context, builder, types.List(arr_type),
            getattr(out_table, f'block_{wvtz__fbipk}'))
        if is_new_col:
            n = fynw__lxrh.size
            vovra__dgy = builder.add(n, rvmc__dwwwt)
            fynw__lxrh.resize(vovra__dgy)
            fynw__lxrh.inititem(n, arr_arg, incref=True)
        elif arr_type == in_table_type.arr_types[col_ind]:
            rbm__mcob = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            fynw__lxrh.setitem(rbm__mcob, arr_arg, True)
        else:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
            rbm__mcob = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            n = fynw__lxrh.size
            vovra__dgy = builder.add(n, rvmc__dwwwt)
            fynw__lxrh.resize(vovra__dgy)
            context.nrt.incref(builder, arr_type, fynw__lxrh.getitem(rbm__mcob)
                )
            fynw__lxrh.move(builder.add(rbm__mcob, rvmc__dwwwt), rbm__mcob,
                builder.sub(n, rbm__mcob))
            fynw__lxrh.setitem(rbm__mcob, arr_arg, incref=True)
    return out_table._getvalue()


def _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
    context, builder):
    ncvth__jpwji = in_table_type.arr_types[col_ind]
    if ncvth__jpwji in out_table_type.type_to_blk:
        wvtz__fbipk = out_table_type.type_to_blk[ncvth__jpwji]
        xyx__fpq = getattr(out_table, f'block_{wvtz__fbipk}')
        zhzsl__tvk = types.List(ncvth__jpwji)
        rbm__mcob = context.get_constant(types.int64, in_table_type.
            block_offsets[col_ind])
        vtob__uqcxz = zhzsl__tvk.dtype(zhzsl__tvk, types.intp)
        jxyzp__ytzjk = context.compile_internal(builder, lambda lst, i: lst
            .pop(i), vtob__uqcxz, (xyx__fpq, rbm__mcob))
        context.nrt.decref(builder, ncvth__jpwji, jxyzp__ytzjk)


@intrinsic
def set_table_data(typingctx, table_type, ind_type, arr_type):
    assert isinstance(table_type, TableType), 'invalid input to set_table_data'
    assert is_overload_constant_int(ind_type
        ), 'set_table_data expects const index'
    col_ind = get_overload_const_int(ind_type)
    is_new_col = col_ind == len(table_type.arr_types)
    guc__yts = list(table_type.arr_types)
    if is_new_col:
        guc__yts.append(arr_type)
    else:
        guc__yts[col_ind] = arr_type
    out_table_type = TableType(tuple(guc__yts))

    def codegen(context, builder, sig, args):
        table_arg, ykpan__bipv, vjx__xpmvo = args
        out_table = set_table_data_codegen(context, builder, table_type,
            table_arg, out_table_type, arr_type, vjx__xpmvo, col_ind,
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
    vuq__akfy = args[0]
    if equiv_set.has_shape(vuq__akfy):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            vuq__akfy)[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_get_table_data = (
    get_table_data_equiv)


@lower_constant(TableType)
def lower_constant_table(context, builder, table_type, pyval):
    nlkcq__kszh = []
    for lmx__gkgb, wvtz__fbipk in table_type.type_to_blk.items():
        pvuow__cjzbw = len(table_type.block_to_arr_ind[wvtz__fbipk])
        gaw__peqch = []
        for i in range(pvuow__cjzbw):
            ohbzp__bxj = table_type.block_to_arr_ind[wvtz__fbipk][i]
            gaw__peqch.append(pyval.arrays[ohbzp__bxj])
        nlkcq__kszh.append(context.get_constant_generic(builder, types.List
            (lmx__gkgb), gaw__peqch))
    jdyy__uuevw = context.get_constant_null(types.pyobject)
    awhd__ypb = context.get_constant(types.int64, 0 if len(pyval.arrays) ==
        0 else len(pyval.arrays[0]))
    return lir.Constant.literal_struct(nlkcq__kszh + [jdyy__uuevw, awhd__ypb])


@intrinsic
def init_table(typingctx, table_type, to_str_if_dict_t):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    out_table_type = table_type
    if is_overload_true(to_str_if_dict_t):
        out_table_type = to_str_arr_if_dict_array(table_type)

    def codegen(context, builder, sig, args):
        psmmr__tfjo = cgutils.create_struct_proxy(out_table_type)(context,
            builder)
        for lmx__gkgb, wvtz__fbipk in out_table_type.type_to_blk.items():
            bmanx__avx = context.get_constant_null(types.List(lmx__gkgb))
            setattr(psmmr__tfjo, f'block_{wvtz__fbipk}', bmanx__avx)
        return psmmr__tfjo._getvalue()
    sig = out_table_type(table_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def init_table_from_lists(typingctx, tuple_of_lists_type, table_type):
    assert isinstance(tuple_of_lists_type, types.BaseTuple
        ), 'Tuple of data expected'
    ulkp__iry = {}
    for i, typ in enumerate(tuple_of_lists_type):
        assert isinstance(typ, types.List), 'Each tuple element must be a list'
        ulkp__iry[typ.dtype] = i
    xbci__iph = table_type.instance_type if isinstance(table_type, types.
        TypeRef) else table_type
    assert isinstance(xbci__iph, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        zofgu__puhav, ykpan__bipv = args
        psmmr__tfjo = cgutils.create_struct_proxy(xbci__iph)(context, builder)
        for lmx__gkgb, wvtz__fbipk in xbci__iph.type_to_blk.items():
            idx = ulkp__iry[lmx__gkgb]
            hrr__srh = signature(types.List(lmx__gkgb), tuple_of_lists_type,
                types.literal(idx))
            pbbqw__weff = zofgu__puhav, idx
            pmo__wzj = numba.cpython.tupleobj.static_getitem_tuple(context,
                builder, hrr__srh, pbbqw__weff)
            setattr(psmmr__tfjo, f'block_{wvtz__fbipk}', pmo__wzj)
        return psmmr__tfjo._getvalue()
    sig = xbci__iph(tuple_of_lists_type, table_type)
    return sig, codegen


@intrinsic
def get_table_block(typingctx, table_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_int(blk_type)
    wvtz__fbipk = get_overload_const_int(blk_type)
    arr_type = None
    for lmx__gkgb, swx__tez in table_type.type_to_blk.items():
        if swx__tez == wvtz__fbipk:
            arr_type = lmx__gkgb
            break
    assert arr_type is not None, 'invalid table type block'
    dcma__wlauw = types.List(arr_type)

    def codegen(context, builder, sig, args):
        psmmr__tfjo = cgutils.create_struct_proxy(table_type)(context,
            builder, args[0])
        ckx__togjc = getattr(psmmr__tfjo, f'block_{wvtz__fbipk}')
        return impl_ret_borrowed(context, builder, dcma__wlauw, ckx__togjc)
    sig = dcma__wlauw(table_type, blk_type)
    return sig, codegen


@intrinsic
def ensure_table_unboxed(typingctx, table_type, used_cols_typ):

    def codegen(context, builder, sig, args):
        table_arg, pmnds__nadij = args
        miuc__ijbg = context.get_python_api(builder)
        fja__uabp = used_cols_typ == types.none
        if not fja__uabp:
            usvvc__kgj = numba.cpython.setobj.SetInstance(context, builder,
                types.Set(types.int64), pmnds__nadij)
        psmmr__tfjo = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, table_arg)
        bna__dlz = cgutils.is_not_null(builder, psmmr__tfjo.parent)
        for lmx__gkgb, wvtz__fbipk in table_type.type_to_blk.items():
            ikkth__zqe = context.get_constant(types.int64, len(table_type.
                block_to_arr_ind[wvtz__fbipk]))
            yca__cxx = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(table_type.block_to_arr_ind[
                wvtz__fbipk], dtype=np.int64))
            pwwn__roqfc = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, yca__cxx)
            ckx__togjc = getattr(psmmr__tfjo, f'block_{wvtz__fbipk}')
            with cgutils.for_range(builder, ikkth__zqe) as kyykh__hvqx:
                i = kyykh__hvqx.index
                ohbzp__bxj = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    pwwn__roqfc, i)
                pjfue__tfalk = types.none(table_type, types.List(lmx__gkgb),
                    types.int64, types.int64)
                dacnq__yeb = table_arg, ckx__togjc, i, ohbzp__bxj
                if fja__uabp:
                    ensure_column_unboxed_codegen(context, builder,
                        pjfue__tfalk, dacnq__yeb)
                else:
                    fcf__fwl = usvvc__kgj.contains(ohbzp__bxj)
                    with builder.if_then(fcf__fwl):
                        ensure_column_unboxed_codegen(context, builder,
                            pjfue__tfalk, dacnq__yeb)
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
    table_arg, vedr__xtfb, ucpky__qpgws, nwwk__plqhj = args
    miuc__ijbg = context.get_python_api(builder)
    psmmr__tfjo = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        table_arg)
    bna__dlz = cgutils.is_not_null(builder, psmmr__tfjo.parent)
    tgakn__pcmkh = ListInstance(context, builder, sig.args[1], vedr__xtfb)
    dnoqh__nckm = tgakn__pcmkh.getitem(ucpky__qpgws)
    qza__ccbi = cgutils.alloca_once_value(builder, dnoqh__nckm)
    aazc__pjpu = cgutils.alloca_once_value(builder, context.
        get_constant_null(sig.args[1].dtype))
    fazkd__uikn = is_ll_eq(builder, qza__ccbi, aazc__pjpu)
    with builder.if_then(fazkd__uikn):
        with builder.if_else(bna__dlz) as (zcggp__kmp, odo__pkb):
            with zcggp__kmp:
                hwls__rvewt = get_df_obj_column_codegen(context, builder,
                    miuc__ijbg, psmmr__tfjo.parent, nwwk__plqhj, sig.args[1
                    ].dtype)
                belc__xft = miuc__ijbg.to_native_value(sig.args[1].dtype,
                    hwls__rvewt).value
                tgakn__pcmkh.inititem(ucpky__qpgws, belc__xft, incref=False)
                miuc__ijbg.decref(hwls__rvewt)
            with odo__pkb:
                context.call_conv.return_user_exc(builder, BodoError, (
                    'unexpected null table column',))


@intrinsic
def set_table_block(typingctx, table_type, arr_list_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert isinstance(arr_list_type, types.List), 'list type expected'
    assert is_overload_constant_int(blk_type), 'blk should be const int'
    wvtz__fbipk = get_overload_const_int(blk_type)

    def codegen(context, builder, sig, args):
        table_arg, plpk__jfhz, ykpan__bipv = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        setattr(in_table, f'block_{wvtz__fbipk}', plpk__jfhz)
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, arr_list_type, blk_type)
    return sig, codegen


@intrinsic
def set_table_len(typingctx, table_type, l_type):
    assert isinstance(table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        table_arg, ceqd__brn = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        in_table.len = ceqd__brn
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, l_type)
    return sig, codegen


@intrinsic
def alloc_list_like(typingctx, list_type, to_str_if_dict_t):
    assert isinstance(list_type, types.List), 'list type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    dcma__wlauw = list_type
    if is_overload_true(to_str_if_dict_t):
        dcma__wlauw = types.List(to_str_arr_if_dict_array(list_type.dtype))

    def codegen(context, builder, sig, args):
        unvi__xdrw = ListInstance(context, builder, list_type, args[0])
        zzon__fpxqh = unvi__xdrw.size
        ykpan__bipv, fynw__lxrh = ListInstance.allocate_ex(context, builder,
            dcma__wlauw, zzon__fpxqh)
        fynw__lxrh.size = zzon__fpxqh
        return fynw__lxrh.value
    sig = dcma__wlauw(list_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def alloc_empty_list_type(typingctx, size_typ, data_typ=None):
    assert isinstance(size_typ, types.Integer), 'Size must be an integer'
    ppiuo__iup = data_typ.instance_type if isinstance(data_typ, types.TypeRef
        ) else data_typ
    list_type = types.List(ppiuo__iup)

    def codegen(context, builder, sig, args):
        zzon__fpxqh, ykpan__bipv = args
        ykpan__bipv, fynw__lxrh = ListInstance.allocate_ex(context, builder,
            list_type, zzon__fpxqh)
        fynw__lxrh.size = zzon__fpxqh
        return fynw__lxrh.value
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
        cekox__nhcj = numba.cpython.unicode._normalize_slice(idx, n)
        return numba.cpython.unicode._slice_span(cekox__nhcj)
    return impl


def gen_table_filter(T, used_cols=None):
    from bodo.utils.conversion import ensure_contig_if_np
    gdn__vea = {'init_table': init_table, 'get_table_block':
        get_table_block, 'ensure_column_unboxed': ensure_column_unboxed,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'alloc_list_like': alloc_list_like, '_get_idx_length':
        _get_idx_length, 'ensure_contig_if_np': ensure_contig_if_np}
    if used_cols is not None:
        gdn__vea['used_cols'] = used_cols
    rinse__imm = 'def impl(T, idx):\n'
    rinse__imm += f'  T2 = init_table(T, False)\n'
    rinse__imm += f'  l = 0\n'
    if used_cols is not None and len(used_cols) == 0:
        rinse__imm += f'  l = _get_idx_length(idx, len(T))\n'
        rinse__imm += f'  T2 = set_table_len(T2, l)\n'
        rinse__imm += f'  return T2\n'
        wdis__igsk = {}
        exec(rinse__imm, gdn__vea, wdis__igsk)
        return wdis__igsk['impl']
    if used_cols is not None:
        rinse__imm += f'  used_set = set(used_cols)\n'
    for wvtz__fbipk in T.type_to_blk.values():
        gdn__vea[f'arr_inds_{wvtz__fbipk}'] = np.array(T.block_to_arr_ind[
            wvtz__fbipk], dtype=np.int64)
        rinse__imm += (
            f'  arr_list_{wvtz__fbipk} = get_table_block(T, {wvtz__fbipk})\n')
        rinse__imm += f"""  out_arr_list_{wvtz__fbipk} = alloc_list_like(arr_list_{wvtz__fbipk}, False)
"""
        rinse__imm += f'  for i in range(len(arr_list_{wvtz__fbipk})):\n'
        rinse__imm += (
            f'    arr_ind_{wvtz__fbipk} = arr_inds_{wvtz__fbipk}[i]\n')
        if used_cols is not None:
            rinse__imm += (
                f'    if arr_ind_{wvtz__fbipk} not in used_set: continue\n')
        rinse__imm += f"""    ensure_column_unboxed(T, arr_list_{wvtz__fbipk}, i, arr_ind_{wvtz__fbipk})
"""
        rinse__imm += f"""    out_arr_{wvtz__fbipk} = ensure_contig_if_np(arr_list_{wvtz__fbipk}[i][idx])
"""
        rinse__imm += f'    l = len(out_arr_{wvtz__fbipk})\n'
        rinse__imm += (
            f'    out_arr_list_{wvtz__fbipk}[i] = out_arr_{wvtz__fbipk}\n')
        rinse__imm += (
            f'  T2 = set_table_block(T2, out_arr_list_{wvtz__fbipk}, {wvtz__fbipk})\n'
            )
    rinse__imm += f'  T2 = set_table_len(T2, l)\n'
    rinse__imm += f'  return T2\n'
    wdis__igsk = {}
    exec(rinse__imm, gdn__vea, wdis__igsk)
    return wdis__igsk['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def decode_if_dict_table(T):
    rinse__imm = 'def impl(T):\n'
    rinse__imm += f'  T2 = init_table(T, True)\n'
    rinse__imm += f'  l = len(T)\n'
    gdn__vea = {'init_table': init_table, 'get_table_block':
        get_table_block, 'ensure_column_unboxed': ensure_column_unboxed,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'alloc_list_like': alloc_list_like, 'decode_if_dict_array':
        decode_if_dict_array}
    for wvtz__fbipk in T.type_to_blk.values():
        gdn__vea[f'arr_inds_{wvtz__fbipk}'] = np.array(T.block_to_arr_ind[
            wvtz__fbipk], dtype=np.int64)
        rinse__imm += (
            f'  arr_list_{wvtz__fbipk} = get_table_block(T, {wvtz__fbipk})\n')
        rinse__imm += f"""  out_arr_list_{wvtz__fbipk} = alloc_list_like(arr_list_{wvtz__fbipk}, True)
"""
        rinse__imm += f'  for i in range(len(arr_list_{wvtz__fbipk})):\n'
        rinse__imm += (
            f'    arr_ind_{wvtz__fbipk} = arr_inds_{wvtz__fbipk}[i]\n')
        rinse__imm += f"""    ensure_column_unboxed(T, arr_list_{wvtz__fbipk}, i, arr_ind_{wvtz__fbipk})
"""
        rinse__imm += f"""    out_arr_{wvtz__fbipk} = decode_if_dict_array(arr_list_{wvtz__fbipk}[i])
"""
        rinse__imm += (
            f'    out_arr_list_{wvtz__fbipk}[i] = out_arr_{wvtz__fbipk}\n')
        rinse__imm += (
            f'  T2 = set_table_block(T2, out_arr_list_{wvtz__fbipk}, {wvtz__fbipk})\n'
            )
    rinse__imm += f'  T2 = set_table_len(T2, l)\n'
    rinse__imm += f'  return T2\n'
    wdis__igsk = {}
    exec(rinse__imm, gdn__vea, wdis__igsk)
    return wdis__igsk['impl']


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
        ccdtc__klon = [arr_list_tup_typ.dtype.dtype] * len(arr_list_tup_typ)
    else:
        ccdtc__klon = []
        for typ in arr_list_tup_typ:
            if typ.dtype == types.undefined:
                return
            ccdtc__klon.append(typ.dtype)
    assert isinstance(nrows_typ, types.Integer
        ), 'init_runtime_table_from_lists requires an integer length'

    def codegen(context, builder, sig, args):
        wwzak__laans, mtow__zwbo = args
        psmmr__tfjo = cgutils.create_struct_proxy(table_type)(context, builder)
        psmmr__tfjo.len = mtow__zwbo
        nlkcq__kszh = cgutils.unpack_tuple(builder, wwzak__laans)
        for i, ckx__togjc in enumerate(nlkcq__kszh):
            setattr(psmmr__tfjo, f'block_{i}', ckx__togjc)
            context.nrt.incref(builder, types.List(ccdtc__klon[i]), ckx__togjc)
        return psmmr__tfjo._getvalue()
    table_type = TableType(tuple(ccdtc__klon), True)
    sig = table_type(arr_list_tup_typ, nrows_typ)
    return sig, codegen
