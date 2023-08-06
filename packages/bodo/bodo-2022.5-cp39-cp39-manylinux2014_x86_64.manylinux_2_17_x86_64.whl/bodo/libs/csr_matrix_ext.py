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
        hro__xol = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'indices', types.Array(fe_type.idx_dtype, 1, 'C')), ('indptr',
            types.Array(fe_type.idx_dtype, 1, 'C')), ('shape', types.
            UniTuple(types.int64, 2))]
        models.StructModel.__init__(self, dmm, fe_type, hro__xol)


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
        dobxy__fsdwh, mewjo__dgp, lhah__xyosi, owmx__rcerf = args
        qgq__gddy = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        qgq__gddy.data = dobxy__fsdwh
        qgq__gddy.indices = mewjo__dgp
        qgq__gddy.indptr = lhah__xyosi
        qgq__gddy.shape = owmx__rcerf
        context.nrt.incref(builder, signature.args[0], dobxy__fsdwh)
        context.nrt.incref(builder, signature.args[1], mewjo__dgp)
        context.nrt.incref(builder, signature.args[2], lhah__xyosi)
        return qgq__gddy._getvalue()
    wug__kayz = CSRMatrixType(data_t.dtype, indices_t.dtype)
    bqoi__uvvex = wug__kayz(data_t, indices_t, indptr_t, types.UniTuple(
        types.int64, 2))
    return bqoi__uvvex, codegen


if bodo.utils.utils.has_scipy():
    import scipy.sparse

    @typeof_impl.register(scipy.sparse.csr_matrix)
    def _typeof_csr_matrix(val, c):
        dtype = numba.from_dtype(val.dtype)
        idx_dtype = numba.from_dtype(val.indices.dtype)
        return CSRMatrixType(dtype, idx_dtype)


@unbox(CSRMatrixType)
def unbox_csr_matrix(typ, val, c):
    qgq__gddy = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    icqay__cctl = c.pyapi.object_getattr_string(val, 'data')
    bbi__uvi = c.pyapi.object_getattr_string(val, 'indices')
    tlt__ebtv = c.pyapi.object_getattr_string(val, 'indptr')
    jtlvw__gcm = c.pyapi.object_getattr_string(val, 'shape')
    qgq__gddy.data = c.pyapi.to_native_value(types.Array(typ.dtype, 1, 'C'),
        icqay__cctl).value
    qgq__gddy.indices = c.pyapi.to_native_value(types.Array(typ.idx_dtype, 
        1, 'C'), bbi__uvi).value
    qgq__gddy.indptr = c.pyapi.to_native_value(types.Array(typ.idx_dtype, 1,
        'C'), tlt__ebtv).value
    qgq__gddy.shape = c.pyapi.to_native_value(types.UniTuple(types.int64, 2
        ), jtlvw__gcm).value
    c.pyapi.decref(icqay__cctl)
    c.pyapi.decref(bbi__uvi)
    c.pyapi.decref(tlt__ebtv)
    c.pyapi.decref(jtlvw__gcm)
    nirkr__glck = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(qgq__gddy._getvalue(), is_error=nirkr__glck)


@box(CSRMatrixType)
def box_csr_matrix(typ, val, c):
    bxh__kpjpk = c.context.insert_const_string(c.builder.module, 'scipy.sparse'
        )
    yecdg__qdpu = c.pyapi.import_module_noblock(bxh__kpjpk)
    qgq__gddy = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Array(typ.dtype, 1, 'C'),
        qgq__gddy.data)
    icqay__cctl = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        qgq__gddy.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        qgq__gddy.indices)
    bbi__uvi = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1, 'C'),
        qgq__gddy.indices, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        qgq__gddy.indptr)
    tlt__ebtv = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1, 'C'
        ), qgq__gddy.indptr, c.env_manager)
    jtlvw__gcm = c.pyapi.from_native_value(types.UniTuple(types.int64, 2),
        qgq__gddy.shape, c.env_manager)
    repb__vko = c.pyapi.tuple_pack([icqay__cctl, bbi__uvi, tlt__ebtv])
    isxmq__kftz = c.pyapi.call_method(yecdg__qdpu, 'csr_matrix', (repb__vko,
        jtlvw__gcm))
    c.pyapi.decref(repb__vko)
    c.pyapi.decref(icqay__cctl)
    c.pyapi.decref(bbi__uvi)
    c.pyapi.decref(tlt__ebtv)
    c.pyapi.decref(jtlvw__gcm)
    c.pyapi.decref(yecdg__qdpu)
    c.context.nrt.decref(c.builder, typ, val)
    return isxmq__kftz


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
    ipeh__fuu = A.dtype
    sxcp__ugv = A.idx_dtype
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):

        def impl(A, idx):
            lfghm__sog, etxa__gwpe = A.shape
            lctm__xffza = numba.cpython.unicode._normalize_slice(idx[0],
                lfghm__sog)
            dme__jhrl = numba.cpython.unicode._normalize_slice(idx[1],
                etxa__gwpe)
            if lctm__xffza.step != 1 or dme__jhrl.step != 1:
                raise ValueError(
                    'CSR matrix slice getitem only supports step=1 currently')
            fdttt__xafbg = lctm__xffza.start
            huk__vdvkn = lctm__xffza.stop
            xumrb__oerp = dme__jhrl.start
            akz__qzlgm = dme__jhrl.stop
            uzbu__ctpst = A.indptr
            rxmk__njblx = A.indices
            uljgk__yrjsz = A.data
            eitn__gupam = huk__vdvkn - fdttt__xafbg
            zkt__dkp = akz__qzlgm - xumrb__oerp
            atv__fjqm = 0
            vorqe__gold = 0
            for bddp__ddzso in range(eitn__gupam):
                ton__nmyat = uzbu__ctpst[fdttt__xafbg + bddp__ddzso]
                hiu__huh = uzbu__ctpst[fdttt__xafbg + bddp__ddzso + 1]
                for wtll__kjku in range(ton__nmyat, hiu__huh):
                    if rxmk__njblx[wtll__kjku] >= xumrb__oerp and rxmk__njblx[
                        wtll__kjku] < akz__qzlgm:
                        atv__fjqm += 1
            nrmjv__qbose = np.empty(eitn__gupam + 1, sxcp__ugv)
            mdu__dhd = np.empty(atv__fjqm, sxcp__ugv)
            evv__rqg = np.empty(atv__fjqm, ipeh__fuu)
            nrmjv__qbose[0] = 0
            for bddp__ddzso in range(eitn__gupam):
                ton__nmyat = uzbu__ctpst[fdttt__xafbg + bddp__ddzso]
                hiu__huh = uzbu__ctpst[fdttt__xafbg + bddp__ddzso + 1]
                for wtll__kjku in range(ton__nmyat, hiu__huh):
                    if rxmk__njblx[wtll__kjku] >= xumrb__oerp and rxmk__njblx[
                        wtll__kjku] < akz__qzlgm:
                        mdu__dhd[vorqe__gold] = rxmk__njblx[wtll__kjku
                            ] - xumrb__oerp
                        evv__rqg[vorqe__gold] = uljgk__yrjsz[wtll__kjku]
                        vorqe__gold += 1
                nrmjv__qbose[bddp__ddzso + 1] = vorqe__gold
            return init_csr_matrix(evv__rqg, mdu__dhd, nrmjv__qbose, (
                eitn__gupam, zkt__dkp))
        return impl
    raise BodoError(
        f'getitem for CSR matrix with index type {idx} not supported yet.')
