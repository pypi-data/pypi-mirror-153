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
        orsip__iagb = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'indices', types.Array(fe_type.idx_dtype, 1, 'C')), ('indptr',
            types.Array(fe_type.idx_dtype, 1, 'C')), ('shape', types.
            UniTuple(types.int64, 2))]
        models.StructModel.__init__(self, dmm, fe_type, orsip__iagb)


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
        jpo__jtuj, aij__kgcay, daiu__sidex, hopb__undt = args
        ozhky__trpuo = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        ozhky__trpuo.data = jpo__jtuj
        ozhky__trpuo.indices = aij__kgcay
        ozhky__trpuo.indptr = daiu__sidex
        ozhky__trpuo.shape = hopb__undt
        context.nrt.incref(builder, signature.args[0], jpo__jtuj)
        context.nrt.incref(builder, signature.args[1], aij__kgcay)
        context.nrt.incref(builder, signature.args[2], daiu__sidex)
        return ozhky__trpuo._getvalue()
    vtf__qavbf = CSRMatrixType(data_t.dtype, indices_t.dtype)
    lcmot__kuahx = vtf__qavbf(data_t, indices_t, indptr_t, types.UniTuple(
        types.int64, 2))
    return lcmot__kuahx, codegen


if bodo.utils.utils.has_scipy():
    import scipy.sparse

    @typeof_impl.register(scipy.sparse.csr_matrix)
    def _typeof_csr_matrix(val, c):
        dtype = numba.from_dtype(val.dtype)
        idx_dtype = numba.from_dtype(val.indices.dtype)
        return CSRMatrixType(dtype, idx_dtype)


@unbox(CSRMatrixType)
def unbox_csr_matrix(typ, val, c):
    ozhky__trpuo = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    qalq__sbu = c.pyapi.object_getattr_string(val, 'data')
    kkiv__webm = c.pyapi.object_getattr_string(val, 'indices')
    nkzq__rgex = c.pyapi.object_getattr_string(val, 'indptr')
    pij__jddm = c.pyapi.object_getattr_string(val, 'shape')
    ozhky__trpuo.data = c.pyapi.to_native_value(types.Array(typ.dtype, 1,
        'C'), qalq__sbu).value
    ozhky__trpuo.indices = c.pyapi.to_native_value(types.Array(typ.
        idx_dtype, 1, 'C'), kkiv__webm).value
    ozhky__trpuo.indptr = c.pyapi.to_native_value(types.Array(typ.idx_dtype,
        1, 'C'), nkzq__rgex).value
    ozhky__trpuo.shape = c.pyapi.to_native_value(types.UniTuple(types.int64,
        2), pij__jddm).value
    c.pyapi.decref(qalq__sbu)
    c.pyapi.decref(kkiv__webm)
    c.pyapi.decref(nkzq__rgex)
    c.pyapi.decref(pij__jddm)
    qbyb__tmf = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ozhky__trpuo._getvalue(), is_error=qbyb__tmf)


@box(CSRMatrixType)
def box_csr_matrix(typ, val, c):
    yss__crsqa = c.context.insert_const_string(c.builder.module, 'scipy.sparse'
        )
    aqy__xhw = c.pyapi.import_module_noblock(yss__crsqa)
    ozhky__trpuo = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Array(typ.dtype, 1, 'C'),
        ozhky__trpuo.data)
    qalq__sbu = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        ozhky__trpuo.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        ozhky__trpuo.indices)
    kkiv__webm = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1,
        'C'), ozhky__trpuo.indices, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        ozhky__trpuo.indptr)
    nkzq__rgex = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1,
        'C'), ozhky__trpuo.indptr, c.env_manager)
    pij__jddm = c.pyapi.from_native_value(types.UniTuple(types.int64, 2),
        ozhky__trpuo.shape, c.env_manager)
    qpdhx__ugii = c.pyapi.tuple_pack([qalq__sbu, kkiv__webm, nkzq__rgex])
    djlke__eqhe = c.pyapi.call_method(aqy__xhw, 'csr_matrix', (qpdhx__ugii,
        pij__jddm))
    c.pyapi.decref(qpdhx__ugii)
    c.pyapi.decref(qalq__sbu)
    c.pyapi.decref(kkiv__webm)
    c.pyapi.decref(nkzq__rgex)
    c.pyapi.decref(pij__jddm)
    c.pyapi.decref(aqy__xhw)
    c.context.nrt.decref(c.builder, typ, val)
    return djlke__eqhe


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
    nmz__ntt = A.dtype
    sbkx__djrh = A.idx_dtype
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):

        def impl(A, idx):
            sazug__jfsh, too__awn = A.shape
            jcdyj__pvqg = numba.cpython.unicode._normalize_slice(idx[0],
                sazug__jfsh)
            jefb__ujog = numba.cpython.unicode._normalize_slice(idx[1],
                too__awn)
            if jcdyj__pvqg.step != 1 or jefb__ujog.step != 1:
                raise ValueError(
                    'CSR matrix slice getitem only supports step=1 currently')
            pyf__gmez = jcdyj__pvqg.start
            esewh__ixcx = jcdyj__pvqg.stop
            xpc__mnsk = jefb__ujog.start
            iacj__unjg = jefb__ujog.stop
            txt__flj = A.indptr
            uwbo__knrv = A.indices
            hxk__vkz = A.data
            arikm__nctsy = esewh__ixcx - pyf__gmez
            ucj__xiet = iacj__unjg - xpc__mnsk
            dxpby__hcn = 0
            diqzt__sjw = 0
            for lkq__boyyc in range(arikm__nctsy):
                hje__yei = txt__flj[pyf__gmez + lkq__boyyc]
                wqg__rrfvo = txt__flj[pyf__gmez + lkq__boyyc + 1]
                for atdg__lvgke in range(hje__yei, wqg__rrfvo):
                    if uwbo__knrv[atdg__lvgke] >= xpc__mnsk and uwbo__knrv[
                        atdg__lvgke] < iacj__unjg:
                        dxpby__hcn += 1
            qnrtp__ane = np.empty(arikm__nctsy + 1, sbkx__djrh)
            mefa__njdxo = np.empty(dxpby__hcn, sbkx__djrh)
            kad__tikl = np.empty(dxpby__hcn, nmz__ntt)
            qnrtp__ane[0] = 0
            for lkq__boyyc in range(arikm__nctsy):
                hje__yei = txt__flj[pyf__gmez + lkq__boyyc]
                wqg__rrfvo = txt__flj[pyf__gmez + lkq__boyyc + 1]
                for atdg__lvgke in range(hje__yei, wqg__rrfvo):
                    if uwbo__knrv[atdg__lvgke] >= xpc__mnsk and uwbo__knrv[
                        atdg__lvgke] < iacj__unjg:
                        mefa__njdxo[diqzt__sjw] = uwbo__knrv[atdg__lvgke
                            ] - xpc__mnsk
                        kad__tikl[diqzt__sjw] = hxk__vkz[atdg__lvgke]
                        diqzt__sjw += 1
                qnrtp__ane[lkq__boyyc + 1] = diqzt__sjw
            return init_csr_matrix(kad__tikl, mefa__njdxo, qnrtp__ane, (
                arikm__nctsy, ucj__xiet))
        return impl
    raise BodoError(
        f'getitem for CSR matrix with index type {idx} not supported yet.')
