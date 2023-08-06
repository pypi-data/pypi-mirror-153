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
        exka__kkdm = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'indices', types.Array(fe_type.idx_dtype, 1, 'C')), ('indptr',
            types.Array(fe_type.idx_dtype, 1, 'C')), ('shape', types.
            UniTuple(types.int64, 2))]
        models.StructModel.__init__(self, dmm, fe_type, exka__kkdm)


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
        ypkhp__tmr, bnfi__qgpg, yxsd__lfbey, byc__zvhbg = args
        hukep__aujca = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        hukep__aujca.data = ypkhp__tmr
        hukep__aujca.indices = bnfi__qgpg
        hukep__aujca.indptr = yxsd__lfbey
        hukep__aujca.shape = byc__zvhbg
        context.nrt.incref(builder, signature.args[0], ypkhp__tmr)
        context.nrt.incref(builder, signature.args[1], bnfi__qgpg)
        context.nrt.incref(builder, signature.args[2], yxsd__lfbey)
        return hukep__aujca._getvalue()
    adcw__ltz = CSRMatrixType(data_t.dtype, indices_t.dtype)
    ijva__vzlo = adcw__ltz(data_t, indices_t, indptr_t, types.UniTuple(
        types.int64, 2))
    return ijva__vzlo, codegen


if bodo.utils.utils.has_scipy():
    import scipy.sparse

    @typeof_impl.register(scipy.sparse.csr_matrix)
    def _typeof_csr_matrix(val, c):
        dtype = numba.from_dtype(val.dtype)
        idx_dtype = numba.from_dtype(val.indices.dtype)
        return CSRMatrixType(dtype, idx_dtype)


@unbox(CSRMatrixType)
def unbox_csr_matrix(typ, val, c):
    hukep__aujca = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    mceq__ualny = c.pyapi.object_getattr_string(val, 'data')
    vzxg__zuz = c.pyapi.object_getattr_string(val, 'indices')
    jsn__iiho = c.pyapi.object_getattr_string(val, 'indptr')
    hmrba__gph = c.pyapi.object_getattr_string(val, 'shape')
    hukep__aujca.data = c.pyapi.to_native_value(types.Array(typ.dtype, 1,
        'C'), mceq__ualny).value
    hukep__aujca.indices = c.pyapi.to_native_value(types.Array(typ.
        idx_dtype, 1, 'C'), vzxg__zuz).value
    hukep__aujca.indptr = c.pyapi.to_native_value(types.Array(typ.idx_dtype,
        1, 'C'), jsn__iiho).value
    hukep__aujca.shape = c.pyapi.to_native_value(types.UniTuple(types.int64,
        2), hmrba__gph).value
    c.pyapi.decref(mceq__ualny)
    c.pyapi.decref(vzxg__zuz)
    c.pyapi.decref(jsn__iiho)
    c.pyapi.decref(hmrba__gph)
    iuscz__jxjh = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(hukep__aujca._getvalue(), is_error=iuscz__jxjh)


@box(CSRMatrixType)
def box_csr_matrix(typ, val, c):
    tot__rfgu = c.context.insert_const_string(c.builder.module, 'scipy.sparse')
    dojbi__zyqe = c.pyapi.import_module_noblock(tot__rfgu)
    hukep__aujca = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Array(typ.dtype, 1, 'C'),
        hukep__aujca.data)
    mceq__ualny = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        hukep__aujca.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        hukep__aujca.indices)
    vzxg__zuz = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1, 'C'
        ), hukep__aujca.indices, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        hukep__aujca.indptr)
    jsn__iiho = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1, 'C'
        ), hukep__aujca.indptr, c.env_manager)
    hmrba__gph = c.pyapi.from_native_value(types.UniTuple(types.int64, 2),
        hukep__aujca.shape, c.env_manager)
    ztlh__atsvn = c.pyapi.tuple_pack([mceq__ualny, vzxg__zuz, jsn__iiho])
    wjyum__rqt = c.pyapi.call_method(dojbi__zyqe, 'csr_matrix', (
        ztlh__atsvn, hmrba__gph))
    c.pyapi.decref(ztlh__atsvn)
    c.pyapi.decref(mceq__ualny)
    c.pyapi.decref(vzxg__zuz)
    c.pyapi.decref(jsn__iiho)
    c.pyapi.decref(hmrba__gph)
    c.pyapi.decref(dojbi__zyqe)
    c.context.nrt.decref(c.builder, typ, val)
    return wjyum__rqt


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
    jobap__glv = A.dtype
    puad__qfl = A.idx_dtype
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):

        def impl(A, idx):
            fbz__ltgn, zkyd__qmia = A.shape
            vjk__iwtet = numba.cpython.unicode._normalize_slice(idx[0],
                fbz__ltgn)
            hgimz__kcu = numba.cpython.unicode._normalize_slice(idx[1],
                zkyd__qmia)
            if vjk__iwtet.step != 1 or hgimz__kcu.step != 1:
                raise ValueError(
                    'CSR matrix slice getitem only supports step=1 currently')
            fvf__agc = vjk__iwtet.start
            qxg__kax = vjk__iwtet.stop
            lnvrg__pxwk = hgimz__kcu.start
            eefr__ofay = hgimz__kcu.stop
            oyw__uspx = A.indptr
            aca__qrscp = A.indices
            faux__tlxeg = A.data
            cpti__xgdh = qxg__kax - fvf__agc
            san__blb = eefr__ofay - lnvrg__pxwk
            wsxtp__jeo = 0
            iqo__novq = 0
            for kuuof__dddaz in range(cpti__xgdh):
                mtbcf__jmpty = oyw__uspx[fvf__agc + kuuof__dddaz]
                lpewz__ydxl = oyw__uspx[fvf__agc + kuuof__dddaz + 1]
                for ldau__gqo in range(mtbcf__jmpty, lpewz__ydxl):
                    if aca__qrscp[ldau__gqo] >= lnvrg__pxwk and aca__qrscp[
                        ldau__gqo] < eefr__ofay:
                        wsxtp__jeo += 1
            xxd__fdwnj = np.empty(cpti__xgdh + 1, puad__qfl)
            qmzl__aikll = np.empty(wsxtp__jeo, puad__qfl)
            hga__uyj = np.empty(wsxtp__jeo, jobap__glv)
            xxd__fdwnj[0] = 0
            for kuuof__dddaz in range(cpti__xgdh):
                mtbcf__jmpty = oyw__uspx[fvf__agc + kuuof__dddaz]
                lpewz__ydxl = oyw__uspx[fvf__agc + kuuof__dddaz + 1]
                for ldau__gqo in range(mtbcf__jmpty, lpewz__ydxl):
                    if aca__qrscp[ldau__gqo] >= lnvrg__pxwk and aca__qrscp[
                        ldau__gqo] < eefr__ofay:
                        qmzl__aikll[iqo__novq] = aca__qrscp[ldau__gqo
                            ] - lnvrg__pxwk
                        hga__uyj[iqo__novq] = faux__tlxeg[ldau__gqo]
                        iqo__novq += 1
                xxd__fdwnj[kuuof__dddaz + 1] = iqo__novq
            return init_csr_matrix(hga__uyj, qmzl__aikll, xxd__fdwnj, (
                cpti__xgdh, san__blb))
        return impl
    raise BodoError(
        f'getitem for CSR matrix with index type {idx} not supported yet.')
