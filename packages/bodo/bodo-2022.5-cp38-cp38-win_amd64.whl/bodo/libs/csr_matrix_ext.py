"""CSR Matrix data type implementation for scipy.sparse.csr_matrix
"""
import operator
import numba
import numpy as np
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, typeof_impl, unbox
import bodo
from bodo.utils.typing import BodoError


class CSRMatrixType(types.ArrayCompatible):
    ndim = 2

    def __init__(self, dtype, idx_dtype):
        self.dtype = dtype
        self.idx_dtype = idx_dtype
        super(CSRMatrixType, self).__init__(name=
            f'CSRMatrixType({dtype}, {idx_dtype})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 2, 'C')

    def copy(self):
        return CSRMatrixType(self.dtype, self.idx_dtype)


@register_model(CSRMatrixType)
class CSRMatrixModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        iaf__vbdw = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'indices', types.Array(fe_type.idx_dtype, 1, 'C')), ('indptr',
            types.Array(fe_type.idx_dtype, 1, 'C')), ('shape', types.
            UniTuple(types.int64, 2))]
        models.StructModel.__init__(self, dmm, fe_type, iaf__vbdw)


make_attribute_wrapper(CSRMatrixType, 'data', 'data')
make_attribute_wrapper(CSRMatrixType, 'indices', 'indices')
make_attribute_wrapper(CSRMatrixType, 'indptr', 'indptr')
make_attribute_wrapper(CSRMatrixType, 'shape', 'shape')


@intrinsic
def init_csr_matrix(typingctx, data_t, indices_t, indptr_t, shape_t=None):
    assert isinstance(data_t, types.Array)
    assert isinstance(indices_t, types.Array) and isinstance(indices_t.
        dtype, types.Integer)
    assert indices_t == indptr_t

    def codegen(context, builder, signature, args):
        pjhj__oxo, lrnb__edrny, bqyyv__nbg, bnr__nwcpr = args
        bzuf__uxhsx = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        bzuf__uxhsx.data = pjhj__oxo
        bzuf__uxhsx.indices = lrnb__edrny
        bzuf__uxhsx.indptr = bqyyv__nbg
        bzuf__uxhsx.shape = bnr__nwcpr
        context.nrt.incref(builder, signature.args[0], pjhj__oxo)
        context.nrt.incref(builder, signature.args[1], lrnb__edrny)
        context.nrt.incref(builder, signature.args[2], bqyyv__nbg)
        return bzuf__uxhsx._getvalue()
    lnac__qzma = CSRMatrixType(data_t.dtype, indices_t.dtype)
    fksro__nbl = lnac__qzma(data_t, indices_t, indptr_t, types.UniTuple(
        types.int64, 2))
    return fksro__nbl, codegen


if bodo.utils.utils.has_scipy():
    import scipy.sparse

    @typeof_impl.register(scipy.sparse.csr_matrix)
    def _typeof_csr_matrix(val, c):
        dtype = numba.from_dtype(val.dtype)
        idx_dtype = numba.from_dtype(val.indices.dtype)
        return CSRMatrixType(dtype, idx_dtype)


@unbox(CSRMatrixType)
def unbox_csr_matrix(typ, val, c):
    bzuf__uxhsx = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    cbeba__zkd = c.pyapi.object_getattr_string(val, 'data')
    not__pdcc = c.pyapi.object_getattr_string(val, 'indices')
    lubih__sxryh = c.pyapi.object_getattr_string(val, 'indptr')
    ftem__ljil = c.pyapi.object_getattr_string(val, 'shape')
    bzuf__uxhsx.data = c.pyapi.to_native_value(types.Array(typ.dtype, 1,
        'C'), cbeba__zkd).value
    bzuf__uxhsx.indices = c.pyapi.to_native_value(types.Array(typ.idx_dtype,
        1, 'C'), not__pdcc).value
    bzuf__uxhsx.indptr = c.pyapi.to_native_value(types.Array(typ.idx_dtype,
        1, 'C'), lubih__sxryh).value
    bzuf__uxhsx.shape = c.pyapi.to_native_value(types.UniTuple(types.int64,
        2), ftem__ljil).value
    c.pyapi.decref(cbeba__zkd)
    c.pyapi.decref(not__pdcc)
    c.pyapi.decref(lubih__sxryh)
    c.pyapi.decref(ftem__ljil)
    gdj__xia = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(bzuf__uxhsx._getvalue(), is_error=gdj__xia)


@box(CSRMatrixType)
def box_csr_matrix(typ, val, c):
    ubecx__hsewq = c.context.insert_const_string(c.builder.module,
        'scipy.sparse')
    lqzlj__cgc = c.pyapi.import_module_noblock(ubecx__hsewq)
    bzuf__uxhsx = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Array(typ.dtype, 1, 'C'),
        bzuf__uxhsx.data)
    cbeba__zkd = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        bzuf__uxhsx.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        bzuf__uxhsx.indices)
    not__pdcc = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1, 'C'
        ), bzuf__uxhsx.indices, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        bzuf__uxhsx.indptr)
    lubih__sxryh = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1,
        'C'), bzuf__uxhsx.indptr, c.env_manager)
    ftem__ljil = c.pyapi.from_native_value(types.UniTuple(types.int64, 2),
        bzuf__uxhsx.shape, c.env_manager)
    iepw__wikrz = c.pyapi.tuple_pack([cbeba__zkd, not__pdcc, lubih__sxryh])
    icipq__srihc = c.pyapi.call_method(lqzlj__cgc, 'csr_matrix', (
        iepw__wikrz, ftem__ljil))
    c.pyapi.decref(iepw__wikrz)
    c.pyapi.decref(cbeba__zkd)
    c.pyapi.decref(not__pdcc)
    c.pyapi.decref(lubih__sxryh)
    c.pyapi.decref(ftem__ljil)
    c.pyapi.decref(lqzlj__cgc)
    c.context.nrt.decref(c.builder, typ, val)
    return icipq__srihc


@overload(len, no_unliteral=True)
def overload_csr_matrix_len(A):
    if isinstance(A, CSRMatrixType):
        return lambda A: A.shape[0]


@overload_attribute(CSRMatrixType, 'ndim')
def overload_csr_matrix_ndim(A):
    return lambda A: 2


@overload_method(CSRMatrixType, 'copy', no_unliteral=True)
def overload_csr_matrix_copy(A):

    def copy_impl(A):
        return init_csr_matrix(A.data.copy(), A.indices.copy(), A.indptr.
            copy(), A.shape)
    return copy_impl


@overload(operator.getitem, no_unliteral=True)
def csr_matrix_getitem(A, idx):
    if not isinstance(A, CSRMatrixType):
        return
    fldwx__xcjm = A.dtype
    bzlu__egao = A.idx_dtype
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):

        def impl(A, idx):
            squr__hxuly, hwhc__avfm = A.shape
            uugrq__qkh = numba.cpython.unicode._normalize_slice(idx[0],
                squr__hxuly)
            egfo__vvyrt = numba.cpython.unicode._normalize_slice(idx[1],
                hwhc__avfm)
            if uugrq__qkh.step != 1 or egfo__vvyrt.step != 1:
                raise ValueError(
                    'CSR matrix slice getitem only supports step=1 currently')
            vzry__otfh = uugrq__qkh.start
            ijiwd__ves = uugrq__qkh.stop
            njtza__fgcw = egfo__vvyrt.start
            hglw__klgl = egfo__vvyrt.stop
            oiq__clkln = A.indptr
            twm__jafnw = A.indices
            znpm__xeysy = A.data
            iiyl__gekjl = ijiwd__ves - vzry__otfh
            cdu__uzwhx = hglw__klgl - njtza__fgcw
            prboy__cby = 0
            hvdo__vyvty = 0
            for ubsm__gxpt in range(iiyl__gekjl):
                chy__ncreb = oiq__clkln[vzry__otfh + ubsm__gxpt]
                xboj__jqc = oiq__clkln[vzry__otfh + ubsm__gxpt + 1]
                for acf__vhh in range(chy__ncreb, xboj__jqc):
                    if twm__jafnw[acf__vhh] >= njtza__fgcw and twm__jafnw[
                        acf__vhh] < hglw__klgl:
                        prboy__cby += 1
            ibkao__ngk = np.empty(iiyl__gekjl + 1, bzlu__egao)
            hgcg__qgxi = np.empty(prboy__cby, bzlu__egao)
            jbjq__fop = np.empty(prboy__cby, fldwx__xcjm)
            ibkao__ngk[0] = 0
            for ubsm__gxpt in range(iiyl__gekjl):
                chy__ncreb = oiq__clkln[vzry__otfh + ubsm__gxpt]
                xboj__jqc = oiq__clkln[vzry__otfh + ubsm__gxpt + 1]
                for acf__vhh in range(chy__ncreb, xboj__jqc):
                    if twm__jafnw[acf__vhh] >= njtza__fgcw and twm__jafnw[
                        acf__vhh] < hglw__klgl:
                        hgcg__qgxi[hvdo__vyvty] = twm__jafnw[acf__vhh
                            ] - njtza__fgcw
                        jbjq__fop[hvdo__vyvty] = znpm__xeysy[acf__vhh]
                        hvdo__vyvty += 1
                ibkao__ngk[ubsm__gxpt + 1] = hvdo__vyvty
            return init_csr_matrix(jbjq__fop, hgcg__qgxi, ibkao__ngk, (
                iiyl__gekjl, cdu__uzwhx))
        return impl
    raise BodoError(
        f'getitem for CSR matrix with index type {idx} not supported yet.')
