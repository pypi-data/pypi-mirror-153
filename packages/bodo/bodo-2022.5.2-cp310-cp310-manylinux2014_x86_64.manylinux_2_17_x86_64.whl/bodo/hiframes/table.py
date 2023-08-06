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
            kuxf__fos = 0
            teyzw__hwin = []
            for i in range(usecols[-1] + 1):
                if i == usecols[kuxf__fos]:
                    teyzw__hwin.append(arrs[kuxf__fos])
                    kuxf__fos += 1
                else:
                    teyzw__hwin.append(None)
            for qloqc__zld in range(usecols[-1] + 1, num_arrs):
                teyzw__hwin.append(None)
            self.arrays = teyzw__hwin
        else:
            self.arrays = arrs
        self.block_0 = arrs

    def __eq__(self, other):
        return isinstance(other, Table) and len(self.arrays) == len(other.
            arrays) and all((soqpe__pni == rzfjq__zwa).all() for soqpe__pni,
            rzfjq__zwa in zip(self.arrays, other.arrays))

    def __str__(self) ->str:
        return str(self.arrays)

    def to_pandas(self, index=None):
        gvhgq__rkino = len(self.arrays)
        bxdt__oob = dict(zip(range(gvhgq__rkino), self.arrays))
        df = pd.DataFrame(bxdt__oob, index)
        return df


class TableType(types.ArrayCompatible):

    def __init__(self, arr_types, has_runtime_cols=False):
        self.arr_types = arr_types
        self.has_runtime_cols = has_runtime_cols
        esox__zmzkb = []
        rndw__zemh = []
        anxe__brg = {}
        zefc__stjwm = defaultdict(int)
        yylo__hgr = defaultdict(list)
        if not has_runtime_cols:
            for i, blpir__nqxto in enumerate(arr_types):
                if blpir__nqxto not in anxe__brg:
                    anxe__brg[blpir__nqxto] = len(anxe__brg)
                hvv__oia = anxe__brg[blpir__nqxto]
                esox__zmzkb.append(hvv__oia)
                rndw__zemh.append(zefc__stjwm[hvv__oia])
                zefc__stjwm[hvv__oia] += 1
                yylo__hgr[hvv__oia].append(i)
        self.block_nums = esox__zmzkb
        self.block_offsets = rndw__zemh
        self.type_to_blk = anxe__brg
        self.block_to_arr_ind = yylo__hgr
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
    return TableType(tuple(numba.typeof(lpqp__rxwp) for lpqp__rxwp in val.
        arrays))


@register_model(TableType)
class TableTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        if fe_type.has_runtime_cols:
            whd__omghf = [(f'block_{i}', types.List(blpir__nqxto)) for i,
                blpir__nqxto in enumerate(fe_type.arr_types)]
        else:
            whd__omghf = [(f'block_{hvv__oia}', types.List(blpir__nqxto)) for
                blpir__nqxto, hvv__oia in fe_type.type_to_blk.items()]
        whd__omghf.append(('parent', types.pyobject))
        whd__omghf.append(('len', types.int64))
        super(TableTypeModel, self).__init__(dmm, fe_type, whd__omghf)


make_attribute_wrapper(TableType, 'block_0', 'block_0')
make_attribute_wrapper(TableType, 'len', '_len')


@infer_getattr
class TableTypeAttribute(OverloadedKeyAttributeTemplate):
    key = TableType

    def resolve_shape(self, df):
        return types.Tuple([types.int64, types.int64])


@unbox(TableType)
def unbox_table(typ, val, c):
    qej__nilo = c.pyapi.object_getattr_string(val, 'arrays')
    uynz__nlfet = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    uynz__nlfet.parent = cgutils.get_null_value(uynz__nlfet.parent.type)
    vjfdd__ckt = c.pyapi.make_none()
    orw__ndjox = c.context.get_constant(types.int64, 0)
    xgkgq__pie = cgutils.alloca_once_value(c.builder, orw__ndjox)
    for blpir__nqxto, hvv__oia in typ.type_to_blk.items():
        epkc__tatb = c.context.get_constant(types.int64, len(typ.
            block_to_arr_ind[hvv__oia]))
        qloqc__zld, oso__uijx = ListInstance.allocate_ex(c.context, c.
            builder, types.List(blpir__nqxto), epkc__tatb)
        oso__uijx.size = epkc__tatb
        vsam__idkrw = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[hvv__oia],
            dtype=np.int64))
        efhu__phhr = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, vsam__idkrw)
        with cgutils.for_range(c.builder, epkc__tatb) as illr__aqq:
            i = illr__aqq.index
            nzcp__jckfk = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), efhu__phhr, i)
            osmg__pafh = c.pyapi.long_from_longlong(nzcp__jckfk)
            clf__zpuqo = c.pyapi.object_getitem(qej__nilo, osmg__pafh)
            bgl__hgvo = c.builder.icmp_unsigned('==', clf__zpuqo, vjfdd__ckt)
            with c.builder.if_else(bgl__hgvo) as (oqm__ugo, ysnp__gui):
                with oqm__ugo:
                    vhp__ycbd = c.context.get_constant_null(blpir__nqxto)
                    oso__uijx.inititem(i, vhp__ycbd, incref=False)
                with ysnp__gui:
                    thbo__zlk = c.pyapi.call_method(clf__zpuqo, '__len__', ())
                    odrxz__jttyd = c.pyapi.long_as_longlong(thbo__zlk)
                    c.builder.store(odrxz__jttyd, xgkgq__pie)
                    c.pyapi.decref(thbo__zlk)
                    lpqp__rxwp = c.pyapi.to_native_value(blpir__nqxto,
                        clf__zpuqo).value
                    oso__uijx.inititem(i, lpqp__rxwp, incref=False)
            c.pyapi.decref(clf__zpuqo)
            c.pyapi.decref(osmg__pafh)
        setattr(uynz__nlfet, f'block_{hvv__oia}', oso__uijx.value)
    uynz__nlfet.len = c.builder.load(xgkgq__pie)
    c.pyapi.decref(qej__nilo)
    c.pyapi.decref(vjfdd__ckt)
    fxman__swh = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(uynz__nlfet._getvalue(), is_error=fxman__swh)


@box(TableType)
def box_table(typ, val, c, ensure_unboxed=None):
    from bodo.hiframes.boxing import get_df_obj_column_codegen
    uynz__nlfet = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ.has_runtime_cols:
        bhzsc__wlf = c.context.get_constant(types.int64, 0)
        for i, blpir__nqxto in enumerate(typ.arr_types):
            teyzw__hwin = getattr(uynz__nlfet, f'block_{i}')
            ebxgq__lgfr = ListInstance(c.context, c.builder, types.List(
                blpir__nqxto), teyzw__hwin)
            bhzsc__wlf = c.builder.add(bhzsc__wlf, ebxgq__lgfr.size)
        ncky__tfek = c.pyapi.list_new(bhzsc__wlf)
        sfn__hqgdb = c.context.get_constant(types.int64, 0)
        for i, blpir__nqxto in enumerate(typ.arr_types):
            teyzw__hwin = getattr(uynz__nlfet, f'block_{i}')
            ebxgq__lgfr = ListInstance(c.context, c.builder, types.List(
                blpir__nqxto), teyzw__hwin)
            with cgutils.for_range(c.builder, ebxgq__lgfr.size) as illr__aqq:
                i = illr__aqq.index
                lpqp__rxwp = ebxgq__lgfr.getitem(i)
                c.context.nrt.incref(c.builder, blpir__nqxto, lpqp__rxwp)
                idx = c.builder.add(sfn__hqgdb, i)
                c.pyapi.list_setitem(ncky__tfek, idx, c.pyapi.
                    from_native_value(blpir__nqxto, lpqp__rxwp, c.env_manager))
            sfn__hqgdb = c.builder.add(sfn__hqgdb, ebxgq__lgfr.size)
        taobq__wsk = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
        xpf__rirci = c.pyapi.call_function_objargs(taobq__wsk, (ncky__tfek,))
        c.pyapi.decref(taobq__wsk)
        c.pyapi.decref(ncky__tfek)
        c.context.nrt.decref(c.builder, typ, val)
        return xpf__rirci
    ncky__tfek = c.pyapi.list_new(c.context.get_constant(types.int64, len(
        typ.arr_types)))
    goiws__usr = cgutils.is_not_null(c.builder, uynz__nlfet.parent)
    if ensure_unboxed is None:
        ensure_unboxed = c.context.get_constant(types.bool_, False)
    for blpir__nqxto, hvv__oia in typ.type_to_blk.items():
        teyzw__hwin = getattr(uynz__nlfet, f'block_{hvv__oia}')
        ebxgq__lgfr = ListInstance(c.context, c.builder, types.List(
            blpir__nqxto), teyzw__hwin)
        vsam__idkrw = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[hvv__oia],
            dtype=np.int64))
        efhu__phhr = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, vsam__idkrw)
        with cgutils.for_range(c.builder, ebxgq__lgfr.size) as illr__aqq:
            i = illr__aqq.index
            nzcp__jckfk = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), efhu__phhr, i)
            lpqp__rxwp = ebxgq__lgfr.getitem(i)
            fvjp__fdufu = cgutils.alloca_once_value(c.builder, lpqp__rxwp)
            xqhy__yjqke = cgutils.alloca_once_value(c.builder, c.context.
                get_constant_null(blpir__nqxto))
            pmkku__sducp = is_ll_eq(c.builder, fvjp__fdufu, xqhy__yjqke)
            with c.builder.if_else(c.builder.and_(pmkku__sducp, c.builder.
                not_(ensure_unboxed))) as (oqm__ugo, ysnp__gui):
                with oqm__ugo:
                    vjfdd__ckt = c.pyapi.make_none()
                    c.pyapi.list_setitem(ncky__tfek, nzcp__jckfk, vjfdd__ckt)
                with ysnp__gui:
                    clf__zpuqo = cgutils.alloca_once(c.builder, c.context.
                        get_value_type(types.pyobject))
                    with c.builder.if_else(c.builder.and_(pmkku__sducp,
                        goiws__usr)) as (ttl__hmh, isyma__hmmoz):
                        with ttl__hmh:
                            xuz__purfn = get_df_obj_column_codegen(c.
                                context, c.builder, c.pyapi, uynz__nlfet.
                                parent, nzcp__jckfk, blpir__nqxto)
                            c.builder.store(xuz__purfn, clf__zpuqo)
                        with isyma__hmmoz:
                            c.context.nrt.incref(c.builder, blpir__nqxto,
                                lpqp__rxwp)
                            c.builder.store(c.pyapi.from_native_value(
                                blpir__nqxto, lpqp__rxwp, c.env_manager),
                                clf__zpuqo)
                    c.pyapi.list_setitem(ncky__tfek, nzcp__jckfk, c.builder
                        .load(clf__zpuqo))
    taobq__wsk = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
    xpf__rirci = c.pyapi.call_function_objargs(taobq__wsk, (ncky__tfek,))
    c.pyapi.decref(taobq__wsk)
    c.pyapi.decref(ncky__tfek)
    c.context.nrt.decref(c.builder, typ, val)
    return xpf__rirci


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
        uynz__nlfet = cgutils.create_struct_proxy(table_type)(context,
            builder, table_arg)
        nsk__rzcr = context.get_constant(types.int64, 0)
        for i, blpir__nqxto in enumerate(table_type.arr_types):
            teyzw__hwin = getattr(uynz__nlfet, f'block_{i}')
            ebxgq__lgfr = ListInstance(context, builder, types.List(
                blpir__nqxto), teyzw__hwin)
            nsk__rzcr = builder.add(nsk__rzcr, ebxgq__lgfr.size)
        return nsk__rzcr
    sig = types.int64(table_type)
    return sig, codegen


def get_table_data_codegen(context, builder, table_arg, col_ind, table_type):
    arr_type = table_type.arr_types[col_ind]
    uynz__nlfet = cgutils.create_struct_proxy(table_type)(context, builder,
        table_arg)
    hvv__oia = table_type.block_nums[col_ind]
    absx__tqfiq = table_type.block_offsets[col_ind]
    teyzw__hwin = getattr(uynz__nlfet, f'block_{hvv__oia}')
    ebxgq__lgfr = ListInstance(context, builder, types.List(arr_type),
        teyzw__hwin)
    lpqp__rxwp = ebxgq__lgfr.getitem(absx__tqfiq)
    return lpqp__rxwp


@intrinsic
def get_table_data(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, qloqc__zld = args
        lpqp__rxwp = get_table_data_codegen(context, builder, table_arg,
            col_ind, table_type)
        return impl_ret_borrowed(context, builder, arr_type, lpqp__rxwp)
    sig = arr_type(table_type, ind_typ)
    return sig, codegen


@intrinsic
def del_column(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, qloqc__zld = args
        uynz__nlfet = cgutils.create_struct_proxy(table_type)(context,
            builder, table_arg)
        hvv__oia = table_type.block_nums[col_ind]
        absx__tqfiq = table_type.block_offsets[col_ind]
        teyzw__hwin = getattr(uynz__nlfet, f'block_{hvv__oia}')
        ebxgq__lgfr = ListInstance(context, builder, types.List(arr_type),
            teyzw__hwin)
        lpqp__rxwp = ebxgq__lgfr.getitem(absx__tqfiq)
        context.nrt.decref(builder, arr_type, lpqp__rxwp)
        vhp__ycbd = context.get_constant_null(arr_type)
        ebxgq__lgfr.inititem(absx__tqfiq, vhp__ycbd, incref=False)
    sig = types.void(table_type, ind_typ)
    return sig, codegen


def set_table_data_codegen(context, builder, in_table_type, in_table,
    out_table_type, arr_type, arr_arg, col_ind, is_new_col):
    in_table = cgutils.create_struct_proxy(in_table_type)(context, builder,
        in_table)
    out_table = cgutils.create_struct_proxy(out_table_type)(context, builder)
    out_table.len = in_table.len
    out_table.parent = in_table.parent
    orw__ndjox = context.get_constant(types.int64, 0)
    nvwg__hql = context.get_constant(types.int64, 1)
    jexl__delqa = arr_type not in in_table_type.type_to_blk
    for blpir__nqxto, hvv__oia in out_table_type.type_to_blk.items():
        if blpir__nqxto in in_table_type.type_to_blk:
            bvcg__dwu = in_table_type.type_to_blk[blpir__nqxto]
            oso__uijx = ListInstance(context, builder, types.List(
                blpir__nqxto), getattr(in_table, f'block_{bvcg__dwu}'))
            context.nrt.incref(builder, types.List(blpir__nqxto), oso__uijx
                .value)
            setattr(out_table, f'block_{hvv__oia}', oso__uijx.value)
    if jexl__delqa:
        qloqc__zld, oso__uijx = ListInstance.allocate_ex(context, builder,
            types.List(arr_type), nvwg__hql)
        oso__uijx.size = nvwg__hql
        oso__uijx.inititem(orw__ndjox, arr_arg, incref=True)
        hvv__oia = out_table_type.type_to_blk[arr_type]
        setattr(out_table, f'block_{hvv__oia}', oso__uijx.value)
        if not is_new_col:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
    else:
        hvv__oia = out_table_type.type_to_blk[arr_type]
        oso__uijx = ListInstance(context, builder, types.List(arr_type),
            getattr(out_table, f'block_{hvv__oia}'))
        if is_new_col:
            n = oso__uijx.size
            buz__zshzh = builder.add(n, nvwg__hql)
            oso__uijx.resize(buz__zshzh)
            oso__uijx.inititem(n, arr_arg, incref=True)
        elif arr_type == in_table_type.arr_types[col_ind]:
            iixzl__ese = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            oso__uijx.setitem(iixzl__ese, arr_arg, True)
        else:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
            iixzl__ese = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            n = oso__uijx.size
            buz__zshzh = builder.add(n, nvwg__hql)
            oso__uijx.resize(buz__zshzh)
            context.nrt.incref(builder, arr_type, oso__uijx.getitem(iixzl__ese)
                )
            oso__uijx.move(builder.add(iixzl__ese, nvwg__hql), iixzl__ese,
                builder.sub(n, iixzl__ese))
            oso__uijx.setitem(iixzl__ese, arr_arg, incref=True)
    return out_table._getvalue()


def _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
    context, builder):
    kfzp__wrfvl = in_table_type.arr_types[col_ind]
    if kfzp__wrfvl in out_table_type.type_to_blk:
        hvv__oia = out_table_type.type_to_blk[kfzp__wrfvl]
        lbu__bha = getattr(out_table, f'block_{hvv__oia}')
        yfeqp__meeok = types.List(kfzp__wrfvl)
        iixzl__ese = context.get_constant(types.int64, in_table_type.
            block_offsets[col_ind])
        ajh__vvt = yfeqp__meeok.dtype(yfeqp__meeok, types.intp)
        rhna__fwg = context.compile_internal(builder, lambda lst, i: lst.
            pop(i), ajh__vvt, (lbu__bha, iixzl__ese))
        context.nrt.decref(builder, kfzp__wrfvl, rhna__fwg)


@intrinsic
def set_table_data(typingctx, table_type, ind_type, arr_type):
    assert isinstance(table_type, TableType), 'invalid input to set_table_data'
    assert is_overload_constant_int(ind_type
        ), 'set_table_data expects const index'
    col_ind = get_overload_const_int(ind_type)
    is_new_col = col_ind == len(table_type.arr_types)
    xey__gxwma = list(table_type.arr_types)
    if is_new_col:
        xey__gxwma.append(arr_type)
    else:
        xey__gxwma[col_ind] = arr_type
    out_table_type = TableType(tuple(xey__gxwma))

    def codegen(context, builder, sig, args):
        table_arg, qloqc__zld, swiu__oczrs = args
        out_table = set_table_data_codegen(context, builder, table_type,
            table_arg, out_table_type, arr_type, swiu__oczrs, col_ind,
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
    oarx__utuv = args[0]
    if equiv_set.has_shape(oarx__utuv):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            oarx__utuv)[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_get_table_data = (
    get_table_data_equiv)


@lower_constant(TableType)
def lower_constant_table(context, builder, table_type, pyval):
    nnfj__tem = []
    for blpir__nqxto, hvv__oia in table_type.type_to_blk.items():
        jdmmx__arzek = len(table_type.block_to_arr_ind[hvv__oia])
        ebvz__ykatl = []
        for i in range(jdmmx__arzek):
            nzcp__jckfk = table_type.block_to_arr_ind[hvv__oia][i]
            ebvz__ykatl.append(pyval.arrays[nzcp__jckfk])
        nnfj__tem.append(context.get_constant_generic(builder, types.List(
            blpir__nqxto), ebvz__ykatl))
    fyoqk__xkat = context.get_constant_null(types.pyobject)
    olmm__dsns = context.get_constant(types.int64, 0 if len(pyval.arrays) ==
        0 else len(pyval.arrays[0]))
    return lir.Constant.literal_struct(nnfj__tem + [fyoqk__xkat, olmm__dsns])


@intrinsic
def init_table(typingctx, table_type, to_str_if_dict_t):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    out_table_type = table_type
    if is_overload_true(to_str_if_dict_t):
        out_table_type = to_str_arr_if_dict_array(table_type)

    def codegen(context, builder, sig, args):
        uynz__nlfet = cgutils.create_struct_proxy(out_table_type)(context,
            builder)
        for blpir__nqxto, hvv__oia in out_table_type.type_to_blk.items():
            fwz__uzd = context.get_constant_null(types.List(blpir__nqxto))
            setattr(uynz__nlfet, f'block_{hvv__oia}', fwz__uzd)
        return uynz__nlfet._getvalue()
    sig = out_table_type(table_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def init_table_from_lists(typingctx, tuple_of_lists_type, table_type):
    assert isinstance(tuple_of_lists_type, types.BaseTuple
        ), 'Tuple of data expected'
    jqkpo__bbfvz = {}
    for i, typ in enumerate(tuple_of_lists_type):
        assert isinstance(typ, types.List), 'Each tuple element must be a list'
        jqkpo__bbfvz[typ.dtype] = i
    xptpt__oaf = table_type.instance_type if isinstance(table_type, types.
        TypeRef) else table_type
    assert isinstance(xptpt__oaf, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        rtp__oyddr, qloqc__zld = args
        uynz__nlfet = cgutils.create_struct_proxy(xptpt__oaf)(context, builder)
        for blpir__nqxto, hvv__oia in xptpt__oaf.type_to_blk.items():
            idx = jqkpo__bbfvz[blpir__nqxto]
            cwoxn__hnrb = signature(types.List(blpir__nqxto),
                tuple_of_lists_type, types.literal(idx))
            grg__ams = rtp__oyddr, idx
            yfok__mckh = numba.cpython.tupleobj.static_getitem_tuple(context,
                builder, cwoxn__hnrb, grg__ams)
            setattr(uynz__nlfet, f'block_{hvv__oia}', yfok__mckh)
        return uynz__nlfet._getvalue()
    sig = xptpt__oaf(tuple_of_lists_type, table_type)
    return sig, codegen


@intrinsic
def get_table_block(typingctx, table_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_int(blk_type)
    hvv__oia = get_overload_const_int(blk_type)
    arr_type = None
    for blpir__nqxto, rzfjq__zwa in table_type.type_to_blk.items():
        if rzfjq__zwa == hvv__oia:
            arr_type = blpir__nqxto
            break
    assert arr_type is not None, 'invalid table type block'
    fta__mlyw = types.List(arr_type)

    def codegen(context, builder, sig, args):
        uynz__nlfet = cgutils.create_struct_proxy(table_type)(context,
            builder, args[0])
        teyzw__hwin = getattr(uynz__nlfet, f'block_{hvv__oia}')
        return impl_ret_borrowed(context, builder, fta__mlyw, teyzw__hwin)
    sig = fta__mlyw(table_type, blk_type)
    return sig, codegen


@intrinsic
def ensure_table_unboxed(typingctx, table_type, used_cols_typ):

    def codegen(context, builder, sig, args):
        table_arg, nwkp__gtmxk = args
        vvfd__yys = context.get_python_api(builder)
        lgjhs__ecazq = used_cols_typ == types.none
        if not lgjhs__ecazq:
            pzju__iqz = numba.cpython.setobj.SetInstance(context, builder,
                types.Set(types.int64), nwkp__gtmxk)
        uynz__nlfet = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, table_arg)
        goiws__usr = cgutils.is_not_null(builder, uynz__nlfet.parent)
        for blpir__nqxto, hvv__oia in table_type.type_to_blk.items():
            epkc__tatb = context.get_constant(types.int64, len(table_type.
                block_to_arr_ind[hvv__oia]))
            vsam__idkrw = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(table_type.block_to_arr_ind[
                hvv__oia], dtype=np.int64))
            efhu__phhr = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, vsam__idkrw)
            teyzw__hwin = getattr(uynz__nlfet, f'block_{hvv__oia}')
            with cgutils.for_range(builder, epkc__tatb) as illr__aqq:
                i = illr__aqq.index
                nzcp__jckfk = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    efhu__phhr, i)
                agl__utx = types.none(table_type, types.List(blpir__nqxto),
                    types.int64, types.int64)
                qctf__hdsqt = table_arg, teyzw__hwin, i, nzcp__jckfk
                if lgjhs__ecazq:
                    ensure_column_unboxed_codegen(context, builder,
                        agl__utx, qctf__hdsqt)
                else:
                    mbkci__oiia = pzju__iqz.contains(nzcp__jckfk)
                    with builder.if_then(mbkci__oiia):
                        ensure_column_unboxed_codegen(context, builder,
                            agl__utx, qctf__hdsqt)
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
    table_arg, bpcn__pyf, xxjhx__coqs, ogv__dunq = args
    vvfd__yys = context.get_python_api(builder)
    uynz__nlfet = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        table_arg)
    goiws__usr = cgutils.is_not_null(builder, uynz__nlfet.parent)
    ebxgq__lgfr = ListInstance(context, builder, sig.args[1], bpcn__pyf)
    tlr__uxk = ebxgq__lgfr.getitem(xxjhx__coqs)
    fvjp__fdufu = cgutils.alloca_once_value(builder, tlr__uxk)
    xqhy__yjqke = cgutils.alloca_once_value(builder, context.
        get_constant_null(sig.args[1].dtype))
    pmkku__sducp = is_ll_eq(builder, fvjp__fdufu, xqhy__yjqke)
    with builder.if_then(pmkku__sducp):
        with builder.if_else(goiws__usr) as (oqm__ugo, ysnp__gui):
            with oqm__ugo:
                clf__zpuqo = get_df_obj_column_codegen(context, builder,
                    vvfd__yys, uynz__nlfet.parent, ogv__dunq, sig.args[1].dtype
                    )
                lpqp__rxwp = vvfd__yys.to_native_value(sig.args[1].dtype,
                    clf__zpuqo).value
                ebxgq__lgfr.inititem(xxjhx__coqs, lpqp__rxwp, incref=False)
                vvfd__yys.decref(clf__zpuqo)
            with ysnp__gui:
                context.call_conv.return_user_exc(builder, BodoError, (
                    'unexpected null table column',))


@intrinsic
def set_table_block(typingctx, table_type, arr_list_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert isinstance(arr_list_type, types.List), 'list type expected'
    assert is_overload_constant_int(blk_type), 'blk should be const int'
    hvv__oia = get_overload_const_int(blk_type)

    def codegen(context, builder, sig, args):
        table_arg, ukhn__mvru, qloqc__zld = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        setattr(in_table, f'block_{hvv__oia}', ukhn__mvru)
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, arr_list_type, blk_type)
    return sig, codegen


@intrinsic
def set_table_len(typingctx, table_type, l_type):
    assert isinstance(table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        table_arg, vzrms__pwcjm = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        in_table.len = vzrms__pwcjm
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, l_type)
    return sig, codegen


@intrinsic
def alloc_list_like(typingctx, list_type, to_str_if_dict_t):
    assert isinstance(list_type, types.List), 'list type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    fta__mlyw = list_type
    if is_overload_true(to_str_if_dict_t):
        fta__mlyw = types.List(to_str_arr_if_dict_array(list_type.dtype))

    def codegen(context, builder, sig, args):
        aci__gfp = ListInstance(context, builder, list_type, args[0])
        jokih__eongb = aci__gfp.size
        qloqc__zld, oso__uijx = ListInstance.allocate_ex(context, builder,
            fta__mlyw, jokih__eongb)
        oso__uijx.size = jokih__eongb
        return oso__uijx.value
    sig = fta__mlyw(list_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def alloc_empty_list_type(typingctx, size_typ, data_typ=None):
    assert isinstance(size_typ, types.Integer), 'Size must be an integer'
    kvun__rouv = data_typ.instance_type if isinstance(data_typ, types.TypeRef
        ) else data_typ
    list_type = types.List(kvun__rouv)

    def codegen(context, builder, sig, args):
        jokih__eongb, qloqc__zld = args
        qloqc__zld, oso__uijx = ListInstance.allocate_ex(context, builder,
            list_type, jokih__eongb)
        oso__uijx.size = jokih__eongb
        return oso__uijx.value
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
        uwci__hkeb = numba.cpython.unicode._normalize_slice(idx, n)
        return numba.cpython.unicode._slice_span(uwci__hkeb)
    return impl


def gen_table_filter(T, used_cols=None):
    from bodo.utils.conversion import ensure_contig_if_np
    tqkwo__mnmd = {'init_table': init_table, 'get_table_block':
        get_table_block, 'ensure_column_unboxed': ensure_column_unboxed,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'alloc_list_like': alloc_list_like, '_get_idx_length':
        _get_idx_length, 'ensure_contig_if_np': ensure_contig_if_np}
    if used_cols is not None:
        tqkwo__mnmd['used_cols'] = used_cols
    mhhk__sdeq = 'def impl(T, idx):\n'
    mhhk__sdeq += f'  T2 = init_table(T, False)\n'
    mhhk__sdeq += f'  l = 0\n'
    if used_cols is not None and len(used_cols) == 0:
        mhhk__sdeq += f'  l = _get_idx_length(idx, len(T))\n'
        mhhk__sdeq += f'  T2 = set_table_len(T2, l)\n'
        mhhk__sdeq += f'  return T2\n'
        sorwk__odx = {}
        exec(mhhk__sdeq, tqkwo__mnmd, sorwk__odx)
        return sorwk__odx['impl']
    if used_cols is not None:
        mhhk__sdeq += f'  used_set = set(used_cols)\n'
    for hvv__oia in T.type_to_blk.values():
        tqkwo__mnmd[f'arr_inds_{hvv__oia}'] = np.array(T.block_to_arr_ind[
            hvv__oia], dtype=np.int64)
        mhhk__sdeq += (
            f'  arr_list_{hvv__oia} = get_table_block(T, {hvv__oia})\n')
        mhhk__sdeq += (
            f'  out_arr_list_{hvv__oia} = alloc_list_like(arr_list_{hvv__oia}, False)\n'
            )
        mhhk__sdeq += f'  for i in range(len(arr_list_{hvv__oia})):\n'
        mhhk__sdeq += f'    arr_ind_{hvv__oia} = arr_inds_{hvv__oia}[i]\n'
        if used_cols is not None:
            mhhk__sdeq += (
                f'    if arr_ind_{hvv__oia} not in used_set: continue\n')
        mhhk__sdeq += (
            f'    ensure_column_unboxed(T, arr_list_{hvv__oia}, i, arr_ind_{hvv__oia})\n'
            )
        mhhk__sdeq += (
            f'    out_arr_{hvv__oia} = ensure_contig_if_np(arr_list_{hvv__oia}[i][idx])\n'
            )
        mhhk__sdeq += f'    l = len(out_arr_{hvv__oia})\n'
        mhhk__sdeq += f'    out_arr_list_{hvv__oia}[i] = out_arr_{hvv__oia}\n'
        mhhk__sdeq += (
            f'  T2 = set_table_block(T2, out_arr_list_{hvv__oia}, {hvv__oia})\n'
            )
    mhhk__sdeq += f'  T2 = set_table_len(T2, l)\n'
    mhhk__sdeq += f'  return T2\n'
    sorwk__odx = {}
    exec(mhhk__sdeq, tqkwo__mnmd, sorwk__odx)
    return sorwk__odx['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def decode_if_dict_table(T):
    mhhk__sdeq = 'def impl(T):\n'
    mhhk__sdeq += f'  T2 = init_table(T, True)\n'
    mhhk__sdeq += f'  l = len(T)\n'
    tqkwo__mnmd = {'init_table': init_table, 'get_table_block':
        get_table_block, 'ensure_column_unboxed': ensure_column_unboxed,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'alloc_list_like': alloc_list_like, 'decode_if_dict_array':
        decode_if_dict_array}
    for hvv__oia in T.type_to_blk.values():
        tqkwo__mnmd[f'arr_inds_{hvv__oia}'] = np.array(T.block_to_arr_ind[
            hvv__oia], dtype=np.int64)
        mhhk__sdeq += (
            f'  arr_list_{hvv__oia} = get_table_block(T, {hvv__oia})\n')
        mhhk__sdeq += (
            f'  out_arr_list_{hvv__oia} = alloc_list_like(arr_list_{hvv__oia}, True)\n'
            )
        mhhk__sdeq += f'  for i in range(len(arr_list_{hvv__oia})):\n'
        mhhk__sdeq += f'    arr_ind_{hvv__oia} = arr_inds_{hvv__oia}[i]\n'
        mhhk__sdeq += (
            f'    ensure_column_unboxed(T, arr_list_{hvv__oia}, i, arr_ind_{hvv__oia})\n'
            )
        mhhk__sdeq += (
            f'    out_arr_{hvv__oia} = decode_if_dict_array(arr_list_{hvv__oia}[i])\n'
            )
        mhhk__sdeq += f'    out_arr_list_{hvv__oia}[i] = out_arr_{hvv__oia}\n'
        mhhk__sdeq += (
            f'  T2 = set_table_block(T2, out_arr_list_{hvv__oia}, {hvv__oia})\n'
            )
    mhhk__sdeq += f'  T2 = set_table_len(T2, l)\n'
    mhhk__sdeq += f'  return T2\n'
    sorwk__odx = {}
    exec(mhhk__sdeq, tqkwo__mnmd, sorwk__odx)
    return sorwk__odx['impl']


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
        hkva__kzdry = [arr_list_tup_typ.dtype.dtype] * len(arr_list_tup_typ)
    else:
        hkva__kzdry = []
        for typ in arr_list_tup_typ:
            if typ.dtype == types.undefined:
                return
            hkva__kzdry.append(typ.dtype)
    assert isinstance(nrows_typ, types.Integer
        ), 'init_runtime_table_from_lists requires an integer length'

    def codegen(context, builder, sig, args):
        hay__hfhr, exp__isrt = args
        uynz__nlfet = cgutils.create_struct_proxy(table_type)(context, builder)
        uynz__nlfet.len = exp__isrt
        nnfj__tem = cgutils.unpack_tuple(builder, hay__hfhr)
        for i, teyzw__hwin in enumerate(nnfj__tem):
            setattr(uynz__nlfet, f'block_{i}', teyzw__hwin)
            context.nrt.incref(builder, types.List(hkva__kzdry[i]), teyzw__hwin
                )
        return uynz__nlfet._getvalue()
    table_type = TableType(tuple(hkva__kzdry), True)
    sig = table_type(arr_list_tup_typ, nrows_typ)
    return sig, codegen
