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
            dmom__obp = 0
            iov__pue = []
            for i in range(usecols[-1] + 1):
                if i == usecols[dmom__obp]:
                    iov__pue.append(arrs[dmom__obp])
                    dmom__obp += 1
                else:
                    iov__pue.append(None)
            for ret__wjhnk in range(usecols[-1] + 1, num_arrs):
                iov__pue.append(None)
            self.arrays = iov__pue
        else:
            self.arrays = arrs
        self.block_0 = arrs

    def __eq__(self, other):
        return isinstance(other, Table) and len(self.arrays) == len(other.
            arrays) and all((jmr__ibbu == jcpok__cvyyj).all() for jmr__ibbu,
            jcpok__cvyyj in zip(self.arrays, other.arrays))

    def __str__(self) ->str:
        return str(self.arrays)

    def to_pandas(self, index=None):
        rgbq__fhumm = len(self.arrays)
        wpxn__ffwac = dict(zip(range(rgbq__fhumm), self.arrays))
        df = pd.DataFrame(wpxn__ffwac, index)
        return df


class TableType(types.ArrayCompatible):

    def __init__(self, arr_types, has_runtime_cols=False):
        self.arr_types = arr_types
        self.has_runtime_cols = has_runtime_cols
        vekuk__unvxr = []
        vvo__zbo = []
        wsl__ofbov = {}
        sap__bgkpq = defaultdict(int)
        emj__hwc = defaultdict(list)
        if not has_runtime_cols:
            for i, ouw__rpzs in enumerate(arr_types):
                if ouw__rpzs not in wsl__ofbov:
                    wsl__ofbov[ouw__rpzs] = len(wsl__ofbov)
                wvfc__cwn = wsl__ofbov[ouw__rpzs]
                vekuk__unvxr.append(wvfc__cwn)
                vvo__zbo.append(sap__bgkpq[wvfc__cwn])
                sap__bgkpq[wvfc__cwn] += 1
                emj__hwc[wvfc__cwn].append(i)
        self.block_nums = vekuk__unvxr
        self.block_offsets = vvo__zbo
        self.type_to_blk = wsl__ofbov
        self.block_to_arr_ind = emj__hwc
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
    return TableType(tuple(numba.typeof(yvf__hjg) for yvf__hjg in val.arrays))


@register_model(TableType)
class TableTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        if fe_type.has_runtime_cols:
            zeq__mruq = [(f'block_{i}', types.List(ouw__rpzs)) for i,
                ouw__rpzs in enumerate(fe_type.arr_types)]
        else:
            zeq__mruq = [(f'block_{wvfc__cwn}', types.List(ouw__rpzs)) for 
                ouw__rpzs, wvfc__cwn in fe_type.type_to_blk.items()]
        zeq__mruq.append(('parent', types.pyobject))
        zeq__mruq.append(('len', types.int64))
        super(TableTypeModel, self).__init__(dmm, fe_type, zeq__mruq)


make_attribute_wrapper(TableType, 'block_0', 'block_0')
make_attribute_wrapper(TableType, 'len', '_len')


@infer_getattr
class TableTypeAttribute(OverloadedKeyAttributeTemplate):
    key = TableType

    def resolve_shape(self, df):
        return types.Tuple([types.int64, types.int64])


@unbox(TableType)
def unbox_table(typ, val, c):
    mzrgy__unge = c.pyapi.object_getattr_string(val, 'arrays')
    zuruu__hgyah = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    zuruu__hgyah.parent = cgutils.get_null_value(zuruu__hgyah.parent.type)
    nav__ajop = c.pyapi.make_none()
    ycklz__eowj = c.context.get_constant(types.int64, 0)
    ihm__etgk = cgutils.alloca_once_value(c.builder, ycklz__eowj)
    for ouw__rpzs, wvfc__cwn in typ.type_to_blk.items():
        jvn__tfqkb = c.context.get_constant(types.int64, len(typ.
            block_to_arr_ind[wvfc__cwn]))
        ret__wjhnk, qmbci__vyret = ListInstance.allocate_ex(c.context, c.
            builder, types.List(ouw__rpzs), jvn__tfqkb)
        qmbci__vyret.size = jvn__tfqkb
        zubt__jwti = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[wvfc__cwn],
            dtype=np.int64))
        hau__lkc = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, zubt__jwti)
        with cgutils.for_range(c.builder, jvn__tfqkb) as rxlwg__crkpf:
            i = rxlwg__crkpf.index
            dhqq__hzbyv = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), hau__lkc, i)
            vrdrr__qyn = c.pyapi.long_from_longlong(dhqq__hzbyv)
            brhy__uuub = c.pyapi.object_getitem(mzrgy__unge, vrdrr__qyn)
            etx__lxqpr = c.builder.icmp_unsigned('==', brhy__uuub, nav__ajop)
            with c.builder.if_else(etx__lxqpr) as (qfmsh__jfe, hjf__ckfqg):
                with qfmsh__jfe:
                    catu__qkk = c.context.get_constant_null(ouw__rpzs)
                    qmbci__vyret.inititem(i, catu__qkk, incref=False)
                with hjf__ckfqg:
                    mhubd__rygpz = c.pyapi.call_method(brhy__uuub,
                        '__len__', ())
                    lsmup__qdav = c.pyapi.long_as_longlong(mhubd__rygpz)
                    c.builder.store(lsmup__qdav, ihm__etgk)
                    c.pyapi.decref(mhubd__rygpz)
                    yvf__hjg = c.pyapi.to_native_value(ouw__rpzs, brhy__uuub
                        ).value
                    qmbci__vyret.inititem(i, yvf__hjg, incref=False)
            c.pyapi.decref(brhy__uuub)
            c.pyapi.decref(vrdrr__qyn)
        setattr(zuruu__hgyah, f'block_{wvfc__cwn}', qmbci__vyret.value)
    zuruu__hgyah.len = c.builder.load(ihm__etgk)
    c.pyapi.decref(mzrgy__unge)
    c.pyapi.decref(nav__ajop)
    axf__lvr = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(zuruu__hgyah._getvalue(), is_error=axf__lvr)


@box(TableType)
def box_table(typ, val, c, ensure_unboxed=None):
    from bodo.hiframes.boxing import get_df_obj_column_codegen
    zuruu__hgyah = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ.has_runtime_cols:
        rmd__ucxy = c.context.get_constant(types.int64, 0)
        for i, ouw__rpzs in enumerate(typ.arr_types):
            iov__pue = getattr(zuruu__hgyah, f'block_{i}')
            linc__keb = ListInstance(c.context, c.builder, types.List(
                ouw__rpzs), iov__pue)
            rmd__ucxy = c.builder.add(rmd__ucxy, linc__keb.size)
        atom__mgc = c.pyapi.list_new(rmd__ucxy)
        acrcv__yitym = c.context.get_constant(types.int64, 0)
        for i, ouw__rpzs in enumerate(typ.arr_types):
            iov__pue = getattr(zuruu__hgyah, f'block_{i}')
            linc__keb = ListInstance(c.context, c.builder, types.List(
                ouw__rpzs), iov__pue)
            with cgutils.for_range(c.builder, linc__keb.size) as rxlwg__crkpf:
                i = rxlwg__crkpf.index
                yvf__hjg = linc__keb.getitem(i)
                c.context.nrt.incref(c.builder, ouw__rpzs, yvf__hjg)
                idx = c.builder.add(acrcv__yitym, i)
                c.pyapi.list_setitem(atom__mgc, idx, c.pyapi.
                    from_native_value(ouw__rpzs, yvf__hjg, c.env_manager))
            acrcv__yitym = c.builder.add(acrcv__yitym, linc__keb.size)
        qqulf__xpzj = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
        hvl__jjihh = c.pyapi.call_function_objargs(qqulf__xpzj, (atom__mgc,))
        c.pyapi.decref(qqulf__xpzj)
        c.pyapi.decref(atom__mgc)
        c.context.nrt.decref(c.builder, typ, val)
        return hvl__jjihh
    atom__mgc = c.pyapi.list_new(c.context.get_constant(types.int64, len(
        typ.arr_types)))
    vujzh__gcj = cgutils.is_not_null(c.builder, zuruu__hgyah.parent)
    if ensure_unboxed is None:
        ensure_unboxed = c.context.get_constant(types.bool_, False)
    for ouw__rpzs, wvfc__cwn in typ.type_to_blk.items():
        iov__pue = getattr(zuruu__hgyah, f'block_{wvfc__cwn}')
        linc__keb = ListInstance(c.context, c.builder, types.List(ouw__rpzs
            ), iov__pue)
        zubt__jwti = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[wvfc__cwn],
            dtype=np.int64))
        hau__lkc = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, zubt__jwti)
        with cgutils.for_range(c.builder, linc__keb.size) as rxlwg__crkpf:
            i = rxlwg__crkpf.index
            dhqq__hzbyv = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), hau__lkc, i)
            yvf__hjg = linc__keb.getitem(i)
            ppmvg__zth = cgutils.alloca_once_value(c.builder, yvf__hjg)
            lknn__cvswb = cgutils.alloca_once_value(c.builder, c.context.
                get_constant_null(ouw__rpzs))
            fhuj__mhijr = is_ll_eq(c.builder, ppmvg__zth, lknn__cvswb)
            with c.builder.if_else(c.builder.and_(fhuj__mhijr, c.builder.
                not_(ensure_unboxed))) as (qfmsh__jfe, hjf__ckfqg):
                with qfmsh__jfe:
                    nav__ajop = c.pyapi.make_none()
                    c.pyapi.list_setitem(atom__mgc, dhqq__hzbyv, nav__ajop)
                with hjf__ckfqg:
                    brhy__uuub = cgutils.alloca_once(c.builder, c.context.
                        get_value_type(types.pyobject))
                    with c.builder.if_else(c.builder.and_(fhuj__mhijr,
                        vujzh__gcj)) as (gne__mbxmk, hhib__rgjg):
                        with gne__mbxmk:
                            pip__mroq = get_df_obj_column_codegen(c.context,
                                c.builder, c.pyapi, zuruu__hgyah.parent,
                                dhqq__hzbyv, ouw__rpzs)
                            c.builder.store(pip__mroq, brhy__uuub)
                        with hhib__rgjg:
                            c.context.nrt.incref(c.builder, ouw__rpzs, yvf__hjg
                                )
                            c.builder.store(c.pyapi.from_native_value(
                                ouw__rpzs, yvf__hjg, c.env_manager), brhy__uuub
                                )
                    c.pyapi.list_setitem(atom__mgc, dhqq__hzbyv, c.builder.
                        load(brhy__uuub))
    qqulf__xpzj = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
    hvl__jjihh = c.pyapi.call_function_objargs(qqulf__xpzj, (atom__mgc,))
    c.pyapi.decref(qqulf__xpzj)
    c.pyapi.decref(atom__mgc)
    c.context.nrt.decref(c.builder, typ, val)
    return hvl__jjihh


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
        zuruu__hgyah = cgutils.create_struct_proxy(table_type)(context,
            builder, table_arg)
        qfhk__jrvr = context.get_constant(types.int64, 0)
        for i, ouw__rpzs in enumerate(table_type.arr_types):
            iov__pue = getattr(zuruu__hgyah, f'block_{i}')
            linc__keb = ListInstance(context, builder, types.List(ouw__rpzs
                ), iov__pue)
            qfhk__jrvr = builder.add(qfhk__jrvr, linc__keb.size)
        return qfhk__jrvr
    sig = types.int64(table_type)
    return sig, codegen


def get_table_data_codegen(context, builder, table_arg, col_ind, table_type):
    arr_type = table_type.arr_types[col_ind]
    zuruu__hgyah = cgutils.create_struct_proxy(table_type)(context, builder,
        table_arg)
    wvfc__cwn = table_type.block_nums[col_ind]
    lgvh__ehlo = table_type.block_offsets[col_ind]
    iov__pue = getattr(zuruu__hgyah, f'block_{wvfc__cwn}')
    linc__keb = ListInstance(context, builder, types.List(arr_type), iov__pue)
    yvf__hjg = linc__keb.getitem(lgvh__ehlo)
    return yvf__hjg


@intrinsic
def get_table_data(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, ret__wjhnk = args
        yvf__hjg = get_table_data_codegen(context, builder, table_arg,
            col_ind, table_type)
        return impl_ret_borrowed(context, builder, arr_type, yvf__hjg)
    sig = arr_type(table_type, ind_typ)
    return sig, codegen


@intrinsic
def del_column(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, ret__wjhnk = args
        zuruu__hgyah = cgutils.create_struct_proxy(table_type)(context,
            builder, table_arg)
        wvfc__cwn = table_type.block_nums[col_ind]
        lgvh__ehlo = table_type.block_offsets[col_ind]
        iov__pue = getattr(zuruu__hgyah, f'block_{wvfc__cwn}')
        linc__keb = ListInstance(context, builder, types.List(arr_type),
            iov__pue)
        yvf__hjg = linc__keb.getitem(lgvh__ehlo)
        context.nrt.decref(builder, arr_type, yvf__hjg)
        catu__qkk = context.get_constant_null(arr_type)
        linc__keb.inititem(lgvh__ehlo, catu__qkk, incref=False)
    sig = types.void(table_type, ind_typ)
    return sig, codegen


def set_table_data_codegen(context, builder, in_table_type, in_table,
    out_table_type, arr_type, arr_arg, col_ind, is_new_col):
    in_table = cgutils.create_struct_proxy(in_table_type)(context, builder,
        in_table)
    out_table = cgutils.create_struct_proxy(out_table_type)(context, builder)
    out_table.len = in_table.len
    out_table.parent = in_table.parent
    ycklz__eowj = context.get_constant(types.int64, 0)
    ydd__wpro = context.get_constant(types.int64, 1)
    mfug__emrjy = arr_type not in in_table_type.type_to_blk
    for ouw__rpzs, wvfc__cwn in out_table_type.type_to_blk.items():
        if ouw__rpzs in in_table_type.type_to_blk:
            fowp__fcle = in_table_type.type_to_blk[ouw__rpzs]
            qmbci__vyret = ListInstance(context, builder, types.List(
                ouw__rpzs), getattr(in_table, f'block_{fowp__fcle}'))
            context.nrt.incref(builder, types.List(ouw__rpzs), qmbci__vyret
                .value)
            setattr(out_table, f'block_{wvfc__cwn}', qmbci__vyret.value)
    if mfug__emrjy:
        ret__wjhnk, qmbci__vyret = ListInstance.allocate_ex(context,
            builder, types.List(arr_type), ydd__wpro)
        qmbci__vyret.size = ydd__wpro
        qmbci__vyret.inititem(ycklz__eowj, arr_arg, incref=True)
        wvfc__cwn = out_table_type.type_to_blk[arr_type]
        setattr(out_table, f'block_{wvfc__cwn}', qmbci__vyret.value)
        if not is_new_col:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
    else:
        wvfc__cwn = out_table_type.type_to_blk[arr_type]
        qmbci__vyret = ListInstance(context, builder, types.List(arr_type),
            getattr(out_table, f'block_{wvfc__cwn}'))
        if is_new_col:
            n = qmbci__vyret.size
            hkgll__ozq = builder.add(n, ydd__wpro)
            qmbci__vyret.resize(hkgll__ozq)
            qmbci__vyret.inititem(n, arr_arg, incref=True)
        elif arr_type == in_table_type.arr_types[col_ind]:
            iesq__cibq = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            qmbci__vyret.setitem(iesq__cibq, arr_arg, True)
        else:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
            iesq__cibq = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            n = qmbci__vyret.size
            hkgll__ozq = builder.add(n, ydd__wpro)
            qmbci__vyret.resize(hkgll__ozq)
            context.nrt.incref(builder, arr_type, qmbci__vyret.getitem(
                iesq__cibq))
            qmbci__vyret.move(builder.add(iesq__cibq, ydd__wpro),
                iesq__cibq, builder.sub(n, iesq__cibq))
            qmbci__vyret.setitem(iesq__cibq, arr_arg, incref=True)
    return out_table._getvalue()


def _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
    context, builder):
    wfjec__ivc = in_table_type.arr_types[col_ind]
    if wfjec__ivc in out_table_type.type_to_blk:
        wvfc__cwn = out_table_type.type_to_blk[wfjec__ivc]
        vpbz__qzro = getattr(out_table, f'block_{wvfc__cwn}')
        umird__dnyd = types.List(wfjec__ivc)
        iesq__cibq = context.get_constant(types.int64, in_table_type.
            block_offsets[col_ind])
        txzzf__kyrw = umird__dnyd.dtype(umird__dnyd, types.intp)
        rdfo__faef = context.compile_internal(builder, lambda lst, i: lst.
            pop(i), txzzf__kyrw, (vpbz__qzro, iesq__cibq))
        context.nrt.decref(builder, wfjec__ivc, rdfo__faef)


@intrinsic
def set_table_data(typingctx, table_type, ind_type, arr_type):
    assert isinstance(table_type, TableType), 'invalid input to set_table_data'
    assert is_overload_constant_int(ind_type
        ), 'set_table_data expects const index'
    col_ind = get_overload_const_int(ind_type)
    is_new_col = col_ind == len(table_type.arr_types)
    troid__nqhx = list(table_type.arr_types)
    if is_new_col:
        troid__nqhx.append(arr_type)
    else:
        troid__nqhx[col_ind] = arr_type
    out_table_type = TableType(tuple(troid__nqhx))

    def codegen(context, builder, sig, args):
        table_arg, ret__wjhnk, qgow__vcqv = args
        out_table = set_table_data_codegen(context, builder, table_type,
            table_arg, out_table_type, arr_type, qgow__vcqv, col_ind,
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
    yjg__sro = args[0]
    if equiv_set.has_shape(yjg__sro):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            yjg__sro)[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_get_table_data = (
    get_table_data_equiv)


@lower_constant(TableType)
def lower_constant_table(context, builder, table_type, pyval):
    zfy__nkxj = []
    for ouw__rpzs, wvfc__cwn in table_type.type_to_blk.items():
        aokyl__kulrv = len(table_type.block_to_arr_ind[wvfc__cwn])
        vwe__ithm = []
        for i in range(aokyl__kulrv):
            dhqq__hzbyv = table_type.block_to_arr_ind[wvfc__cwn][i]
            vwe__ithm.append(pyval.arrays[dhqq__hzbyv])
        zfy__nkxj.append(context.get_constant_generic(builder, types.List(
            ouw__rpzs), vwe__ithm))
    iho__dvi = context.get_constant_null(types.pyobject)
    cogw__sufi = context.get_constant(types.int64, 0 if len(pyval.arrays) ==
        0 else len(pyval.arrays[0]))
    return lir.Constant.literal_struct(zfy__nkxj + [iho__dvi, cogw__sufi])


@intrinsic
def init_table(typingctx, table_type, to_str_if_dict_t):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    out_table_type = table_type
    if is_overload_true(to_str_if_dict_t):
        out_table_type = to_str_arr_if_dict_array(table_type)

    def codegen(context, builder, sig, args):
        zuruu__hgyah = cgutils.create_struct_proxy(out_table_type)(context,
            builder)
        for ouw__rpzs, wvfc__cwn in out_table_type.type_to_blk.items():
            kzrfy__zhh = context.get_constant_null(types.List(ouw__rpzs))
            setattr(zuruu__hgyah, f'block_{wvfc__cwn}', kzrfy__zhh)
        return zuruu__hgyah._getvalue()
    sig = out_table_type(table_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def init_table_from_lists(typingctx, tuple_of_lists_type, table_type):
    assert isinstance(tuple_of_lists_type, types.BaseTuple
        ), 'Tuple of data expected'
    mgocq__mzps = {}
    for i, typ in enumerate(tuple_of_lists_type):
        assert isinstance(typ, types.List), 'Each tuple element must be a list'
        mgocq__mzps[typ.dtype] = i
    vbalz__uzvwt = table_type.instance_type if isinstance(table_type, types
        .TypeRef) else table_type
    assert isinstance(vbalz__uzvwt, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        zgm__ahami, ret__wjhnk = args
        zuruu__hgyah = cgutils.create_struct_proxy(vbalz__uzvwt)(context,
            builder)
        for ouw__rpzs, wvfc__cwn in vbalz__uzvwt.type_to_blk.items():
            idx = mgocq__mzps[ouw__rpzs]
            aacb__bruyj = signature(types.List(ouw__rpzs),
                tuple_of_lists_type, types.literal(idx))
            rbvn__wea = zgm__ahami, idx
            yvgsm__pntu = numba.cpython.tupleobj.static_getitem_tuple(context,
                builder, aacb__bruyj, rbvn__wea)
            setattr(zuruu__hgyah, f'block_{wvfc__cwn}', yvgsm__pntu)
        return zuruu__hgyah._getvalue()
    sig = vbalz__uzvwt(tuple_of_lists_type, table_type)
    return sig, codegen


@intrinsic
def get_table_block(typingctx, table_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_int(blk_type)
    wvfc__cwn = get_overload_const_int(blk_type)
    arr_type = None
    for ouw__rpzs, jcpok__cvyyj in table_type.type_to_blk.items():
        if jcpok__cvyyj == wvfc__cwn:
            arr_type = ouw__rpzs
            break
    assert arr_type is not None, 'invalid table type block'
    haa__ezwk = types.List(arr_type)

    def codegen(context, builder, sig, args):
        zuruu__hgyah = cgutils.create_struct_proxy(table_type)(context,
            builder, args[0])
        iov__pue = getattr(zuruu__hgyah, f'block_{wvfc__cwn}')
        return impl_ret_borrowed(context, builder, haa__ezwk, iov__pue)
    sig = haa__ezwk(table_type, blk_type)
    return sig, codegen


@intrinsic
def ensure_table_unboxed(typingctx, table_type, used_cols_typ):

    def codegen(context, builder, sig, args):
        table_arg, wlqna__srnf = args
        gne__ibyuy = context.get_python_api(builder)
        tvcp__aezj = used_cols_typ == types.none
        if not tvcp__aezj:
            ijfdh__umtv = numba.cpython.setobj.SetInstance(context, builder,
                types.Set(types.int64), wlqna__srnf)
        zuruu__hgyah = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, table_arg)
        vujzh__gcj = cgutils.is_not_null(builder, zuruu__hgyah.parent)
        for ouw__rpzs, wvfc__cwn in table_type.type_to_blk.items():
            jvn__tfqkb = context.get_constant(types.int64, len(table_type.
                block_to_arr_ind[wvfc__cwn]))
            zubt__jwti = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(table_type.block_to_arr_ind[
                wvfc__cwn], dtype=np.int64))
            hau__lkc = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, zubt__jwti)
            iov__pue = getattr(zuruu__hgyah, f'block_{wvfc__cwn}')
            with cgutils.for_range(builder, jvn__tfqkb) as rxlwg__crkpf:
                i = rxlwg__crkpf.index
                dhqq__hzbyv = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'), hau__lkc, i)
                svbh__mfhu = types.none(table_type, types.List(ouw__rpzs),
                    types.int64, types.int64)
                ekf__jpb = table_arg, iov__pue, i, dhqq__hzbyv
                if tvcp__aezj:
                    ensure_column_unboxed_codegen(context, builder,
                        svbh__mfhu, ekf__jpb)
                else:
                    tehq__xxow = ijfdh__umtv.contains(dhqq__hzbyv)
                    with builder.if_then(tehq__xxow):
                        ensure_column_unboxed_codegen(context, builder,
                            svbh__mfhu, ekf__jpb)
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
    table_arg, duk__pbbc, kcq__ywvph, asadb__mcpj = args
    gne__ibyuy = context.get_python_api(builder)
    zuruu__hgyah = cgutils.create_struct_proxy(sig.args[0])(context,
        builder, table_arg)
    vujzh__gcj = cgutils.is_not_null(builder, zuruu__hgyah.parent)
    linc__keb = ListInstance(context, builder, sig.args[1], duk__pbbc)
    jxt__rpmq = linc__keb.getitem(kcq__ywvph)
    ppmvg__zth = cgutils.alloca_once_value(builder, jxt__rpmq)
    lknn__cvswb = cgutils.alloca_once_value(builder, context.
        get_constant_null(sig.args[1].dtype))
    fhuj__mhijr = is_ll_eq(builder, ppmvg__zth, lknn__cvswb)
    with builder.if_then(fhuj__mhijr):
        with builder.if_else(vujzh__gcj) as (qfmsh__jfe, hjf__ckfqg):
            with qfmsh__jfe:
                brhy__uuub = get_df_obj_column_codegen(context, builder,
                    gne__ibyuy, zuruu__hgyah.parent, asadb__mcpj, sig.args[
                    1].dtype)
                yvf__hjg = gne__ibyuy.to_native_value(sig.args[1].dtype,
                    brhy__uuub).value
                linc__keb.inititem(kcq__ywvph, yvf__hjg, incref=False)
                gne__ibyuy.decref(brhy__uuub)
            with hjf__ckfqg:
                context.call_conv.return_user_exc(builder, BodoError, (
                    'unexpected null table column',))


@intrinsic
def set_table_block(typingctx, table_type, arr_list_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert isinstance(arr_list_type, types.List), 'list type expected'
    assert is_overload_constant_int(blk_type), 'blk should be const int'
    wvfc__cwn = get_overload_const_int(blk_type)

    def codegen(context, builder, sig, args):
        table_arg, enzkg__ayco, ret__wjhnk = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        setattr(in_table, f'block_{wvfc__cwn}', enzkg__ayco)
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, arr_list_type, blk_type)
    return sig, codegen


@intrinsic
def set_table_len(typingctx, table_type, l_type):
    assert isinstance(table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        table_arg, fto__tzr = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        in_table.len = fto__tzr
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, l_type)
    return sig, codegen


@intrinsic
def alloc_list_like(typingctx, list_type, to_str_if_dict_t):
    assert isinstance(list_type, types.List), 'list type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    haa__ezwk = list_type
    if is_overload_true(to_str_if_dict_t):
        haa__ezwk = types.List(to_str_arr_if_dict_array(list_type.dtype))

    def codegen(context, builder, sig, args):
        dvm__cbtao = ListInstance(context, builder, list_type, args[0])
        uvvwi__rkx = dvm__cbtao.size
        ret__wjhnk, qmbci__vyret = ListInstance.allocate_ex(context,
            builder, haa__ezwk, uvvwi__rkx)
        qmbci__vyret.size = uvvwi__rkx
        return qmbci__vyret.value
    sig = haa__ezwk(list_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def alloc_empty_list_type(typingctx, size_typ, data_typ=None):
    assert isinstance(size_typ, types.Integer), 'Size must be an integer'
    uqk__bnsya = data_typ.instance_type if isinstance(data_typ, types.TypeRef
        ) else data_typ
    list_type = types.List(uqk__bnsya)

    def codegen(context, builder, sig, args):
        uvvwi__rkx, ret__wjhnk = args
        ret__wjhnk, qmbci__vyret = ListInstance.allocate_ex(context,
            builder, list_type, uvvwi__rkx)
        qmbci__vyret.size = uvvwi__rkx
        return qmbci__vyret.value
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
        vgocy__ftdg = numba.cpython.unicode._normalize_slice(idx, n)
        return numba.cpython.unicode._slice_span(vgocy__ftdg)
    return impl


def gen_table_filter(T, used_cols=None):
    from bodo.utils.conversion import ensure_contig_if_np
    ovnv__foj = {'init_table': init_table, 'get_table_block':
        get_table_block, 'ensure_column_unboxed': ensure_column_unboxed,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'alloc_list_like': alloc_list_like, '_get_idx_length':
        _get_idx_length, 'ensure_contig_if_np': ensure_contig_if_np}
    if used_cols is not None:
        ovnv__foj['used_cols'] = used_cols
    hux__wxx = 'def impl(T, idx):\n'
    hux__wxx += f'  T2 = init_table(T, False)\n'
    hux__wxx += f'  l = 0\n'
    if used_cols is not None and len(used_cols) == 0:
        hux__wxx += f'  l = _get_idx_length(idx, len(T))\n'
        hux__wxx += f'  T2 = set_table_len(T2, l)\n'
        hux__wxx += f'  return T2\n'
        xinyg__domhp = {}
        exec(hux__wxx, ovnv__foj, xinyg__domhp)
        return xinyg__domhp['impl']
    if used_cols is not None:
        hux__wxx += f'  used_set = set(used_cols)\n'
    for wvfc__cwn in T.type_to_blk.values():
        ovnv__foj[f'arr_inds_{wvfc__cwn}'] = np.array(T.block_to_arr_ind[
            wvfc__cwn], dtype=np.int64)
        hux__wxx += (
            f'  arr_list_{wvfc__cwn} = get_table_block(T, {wvfc__cwn})\n')
        hux__wxx += (
            f'  out_arr_list_{wvfc__cwn} = alloc_list_like(arr_list_{wvfc__cwn}, False)\n'
            )
        hux__wxx += f'  for i in range(len(arr_list_{wvfc__cwn})):\n'
        hux__wxx += f'    arr_ind_{wvfc__cwn} = arr_inds_{wvfc__cwn}[i]\n'
        if used_cols is not None:
            hux__wxx += (
                f'    if arr_ind_{wvfc__cwn} not in used_set: continue\n')
        hux__wxx += (
            f'    ensure_column_unboxed(T, arr_list_{wvfc__cwn}, i, arr_ind_{wvfc__cwn})\n'
            )
        hux__wxx += (
            f'    out_arr_{wvfc__cwn} = ensure_contig_if_np(arr_list_{wvfc__cwn}[i][idx])\n'
            )
        hux__wxx += f'    l = len(out_arr_{wvfc__cwn})\n'
        hux__wxx += f'    out_arr_list_{wvfc__cwn}[i] = out_arr_{wvfc__cwn}\n'
        hux__wxx += (
            f'  T2 = set_table_block(T2, out_arr_list_{wvfc__cwn}, {wvfc__cwn})\n'
            )
    hux__wxx += f'  T2 = set_table_len(T2, l)\n'
    hux__wxx += f'  return T2\n'
    xinyg__domhp = {}
    exec(hux__wxx, ovnv__foj, xinyg__domhp)
    return xinyg__domhp['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def decode_if_dict_table(T):
    hux__wxx = 'def impl(T):\n'
    hux__wxx += f'  T2 = init_table(T, True)\n'
    hux__wxx += f'  l = len(T)\n'
    ovnv__foj = {'init_table': init_table, 'get_table_block':
        get_table_block, 'ensure_column_unboxed': ensure_column_unboxed,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'alloc_list_like': alloc_list_like, 'decode_if_dict_array':
        decode_if_dict_array}
    for wvfc__cwn in T.type_to_blk.values():
        ovnv__foj[f'arr_inds_{wvfc__cwn}'] = np.array(T.block_to_arr_ind[
            wvfc__cwn], dtype=np.int64)
        hux__wxx += (
            f'  arr_list_{wvfc__cwn} = get_table_block(T, {wvfc__cwn})\n')
        hux__wxx += (
            f'  out_arr_list_{wvfc__cwn} = alloc_list_like(arr_list_{wvfc__cwn}, True)\n'
            )
        hux__wxx += f'  for i in range(len(arr_list_{wvfc__cwn})):\n'
        hux__wxx += f'    arr_ind_{wvfc__cwn} = arr_inds_{wvfc__cwn}[i]\n'
        hux__wxx += (
            f'    ensure_column_unboxed(T, arr_list_{wvfc__cwn}, i, arr_ind_{wvfc__cwn})\n'
            )
        hux__wxx += (
            f'    out_arr_{wvfc__cwn} = decode_if_dict_array(arr_list_{wvfc__cwn}[i])\n'
            )
        hux__wxx += f'    out_arr_list_{wvfc__cwn}[i] = out_arr_{wvfc__cwn}\n'
        hux__wxx += (
            f'  T2 = set_table_block(T2, out_arr_list_{wvfc__cwn}, {wvfc__cwn})\n'
            )
    hux__wxx += f'  T2 = set_table_len(T2, l)\n'
    hux__wxx += f'  return T2\n'
    xinyg__domhp = {}
    exec(hux__wxx, ovnv__foj, xinyg__domhp)
    return xinyg__domhp['impl']


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
        ymuyk__jme = [arr_list_tup_typ.dtype.dtype] * len(arr_list_tup_typ)
    else:
        ymuyk__jme = []
        for typ in arr_list_tup_typ:
            if typ.dtype == types.undefined:
                return
            ymuyk__jme.append(typ.dtype)
    assert isinstance(nrows_typ, types.Integer
        ), 'init_runtime_table_from_lists requires an integer length'

    def codegen(context, builder, sig, args):
        romt__ijpy, sbt__mix = args
        zuruu__hgyah = cgutils.create_struct_proxy(table_type)(context, builder
            )
        zuruu__hgyah.len = sbt__mix
        zfy__nkxj = cgutils.unpack_tuple(builder, romt__ijpy)
        for i, iov__pue in enumerate(zfy__nkxj):
            setattr(zuruu__hgyah, f'block_{i}', iov__pue)
            context.nrt.incref(builder, types.List(ymuyk__jme[i]), iov__pue)
        return zuruu__hgyah._getvalue()
    table_type = TableType(tuple(ymuyk__jme), True)
    sig = table_type(arr_list_tup_typ, nrows_typ)
    return sig, codegen
