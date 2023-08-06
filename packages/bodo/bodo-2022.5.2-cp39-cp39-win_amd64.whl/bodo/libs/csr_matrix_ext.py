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
        qjuiq__rjk = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'indices', types.Array(fe_type.idx_dtype, 1, 'C')), ('indptr',
            types.Array(fe_type.idx_dtype, 1, 'C')), ('shape', types.
            UniTuple(types.int64, 2))]
        models.StructModel.__init__(self, dmm, fe_type, qjuiq__rjk)


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
        abjgd__vopxd, mvww__uockq, uekds__ezc, inl__fto = args
        zgk__qrpi = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        zgk__qrpi.data = abjgd__vopxd
        zgk__qrpi.indices = mvww__uockq
        zgk__qrpi.indptr = uekds__ezc
        zgk__qrpi.shape = inl__fto
        context.nrt.incref(builder, signature.args[0], abjgd__vopxd)
        context.nrt.incref(builder, signature.args[1], mvww__uockq)
        context.nrt.incref(builder, signature.args[2], uekds__ezc)
        return zgk__qrpi._getvalue()
    osro__osxyj = CSRMatrixType(data_t.dtype, indices_t.dtype)
    bpyj__fjr = osro__osxyj(data_t, indices_t, indptr_t, types.UniTuple(
        types.int64, 2))
    return bpyj__fjr, codegen


if bodo.utils.utils.has_scipy():
    import scipy.sparse

    @typeof_impl.register(scipy.sparse.csr_matrix)
    def _typeof_csr_matrix(val, c):
        dtype = numba.from_dtype(val.dtype)
        idx_dtype = numba.from_dtype(val.indices.dtype)
        return CSRMatrixType(dtype, idx_dtype)


@unbox(CSRMatrixType)
def unbox_csr_matrix(typ, val, c):
    zgk__qrpi = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    geuv__pwj = c.pyapi.object_getattr_string(val, 'data')
    thbg__ruzx = c.pyapi.object_getattr_string(val, 'indices')
    zxudr__pjl = c.pyapi.object_getattr_string(val, 'indptr')
    kemkc__gvbzk = c.pyapi.object_getattr_string(val, 'shape')
    zgk__qrpi.data = c.pyapi.to_native_value(types.Array(typ.dtype, 1, 'C'),
        geuv__pwj).value
    zgk__qrpi.indices = c.pyapi.to_native_value(types.Array(typ.idx_dtype, 
        1, 'C'), thbg__ruzx).value
    zgk__qrpi.indptr = c.pyapi.to_native_value(types.Array(typ.idx_dtype, 1,
        'C'), zxudr__pjl).value
    zgk__qrpi.shape = c.pyapi.to_native_value(types.UniTuple(types.int64, 2
        ), kemkc__gvbzk).value
    c.pyapi.decref(geuv__pwj)
    c.pyapi.decref(thbg__ruzx)
    c.pyapi.decref(zxudr__pjl)
    c.pyapi.decref(kemkc__gvbzk)
    hkoh__wlm = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(zgk__qrpi._getvalue(), is_error=hkoh__wlm)


@box(CSRMatrixType)
def box_csr_matrix(typ, val, c):
    dmsn__qazz = c.context.insert_const_string(c.builder.module, 'scipy.sparse'
        )
    ztb__nqrp = c.pyapi.import_module_noblock(dmsn__qazz)
    zgk__qrpi = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Array(typ.dtype, 1, 'C'),
        zgk__qrpi.data)
    geuv__pwj = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        zgk__qrpi.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        zgk__qrpi.indices)
    thbg__ruzx = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1,
        'C'), zgk__qrpi.indices, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        zgk__qrpi.indptr)
    zxudr__pjl = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1,
        'C'), zgk__qrpi.indptr, c.env_manager)
    kemkc__gvbzk = c.pyapi.from_native_value(types.UniTuple(types.int64, 2),
        zgk__qrpi.shape, c.env_manager)
    cspn__szpk = c.pyapi.tuple_pack([geuv__pwj, thbg__ruzx, zxudr__pjl])
    ghz__jgdsc = c.pyapi.call_method(ztb__nqrp, 'csr_matrix', (cspn__szpk,
        kemkc__gvbzk))
    c.pyapi.decref(cspn__szpk)
    c.pyapi.decref(geuv__pwj)
    c.pyapi.decref(thbg__ruzx)
    c.pyapi.decref(zxudr__pjl)
    c.pyapi.decref(kemkc__gvbzk)
    c.pyapi.decref(ztb__nqrp)
    c.context.nrt.decref(c.builder, typ, val)
    return ghz__jgdsc


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
    vgmb__ctn = A.dtype
    enz__pyn = A.idx_dtype
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):

        def impl(A, idx):
            dfqad__pqmgl, xryc__hzpx = A.shape
            rxa__wdspv = numba.cpython.unicode._normalize_slice(idx[0],
                dfqad__pqmgl)
            iqnm__nzj = numba.cpython.unicode._normalize_slice(idx[1],
                xryc__hzpx)
            if rxa__wdspv.step != 1 or iqnm__nzj.step != 1:
                raise ValueError(
                    'CSR matrix slice getitem only supports step=1 currently')
            zfhy__icr = rxa__wdspv.start
            vmfv__puw = rxa__wdspv.stop
            hpli__fylgl = iqnm__nzj.start
            nuzk__wxqmt = iqnm__nzj.stop
            ukm__kmvsx = A.indptr
            mrh__dstl = A.indices
            sulpw__nahfb = A.data
            tflq__emto = vmfv__puw - zfhy__icr
            lwzt__sra = nuzk__wxqmt - hpli__fylgl
            fkebc__dzl = 0
            waor__zhl = 0
            for ajvt__nhrd in range(tflq__emto):
                lqoi__kam = ukm__kmvsx[zfhy__icr + ajvt__nhrd]
                huym__cbpwt = ukm__kmvsx[zfhy__icr + ajvt__nhrd + 1]
                for ypf__gbyuc in range(lqoi__kam, huym__cbpwt):
                    if mrh__dstl[ypf__gbyuc] >= hpli__fylgl and mrh__dstl[
                        ypf__gbyuc] < nuzk__wxqmt:
                        fkebc__dzl += 1
            lacp__xsr = np.empty(tflq__emto + 1, enz__pyn)
            ozwz__nifc = np.empty(fkebc__dzl, enz__pyn)
            ezacf__njsl = np.empty(fkebc__dzl, vgmb__ctn)
            lacp__xsr[0] = 0
            for ajvt__nhrd in range(tflq__emto):
                lqoi__kam = ukm__kmvsx[zfhy__icr + ajvt__nhrd]
                huym__cbpwt = ukm__kmvsx[zfhy__icr + ajvt__nhrd + 1]
                for ypf__gbyuc in range(lqoi__kam, huym__cbpwt):
                    if mrh__dstl[ypf__gbyuc] >= hpli__fylgl and mrh__dstl[
                        ypf__gbyuc] < nuzk__wxqmt:
                        ozwz__nifc[waor__zhl] = mrh__dstl[ypf__gbyuc
                            ] - hpli__fylgl
                        ezacf__njsl[waor__zhl] = sulpw__nahfb[ypf__gbyuc]
                        waor__zhl += 1
                lacp__xsr[ajvt__nhrd + 1] = waor__zhl
            return init_csr_matrix(ezacf__njsl, ozwz__nifc, lacp__xsr, (
                tflq__emto, lwzt__sra))
        return impl
    raise BodoError(
        f'getitem for CSR matrix with index type {idx} not supported yet.')
