import operator
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, models, overload, overload_method, register_model
import bodo
import bodo.io
from bodo.libs.str_ext import std_str_to_unicode, std_str_type, string_type, unicode_to_utf8
from bodo.utils.typing import is_overload_none, parse_dtype
from bodo.utils.utils import numba_to_c_type
if bodo.utils.utils.has_supported_h5py():
    import h5py
    import llvmlite.binding as ll
    from bodo.io import _hdf5
    ll.add_symbol('h5_open', _hdf5.h5_open)
    ll.add_symbol('h5_open_dset_or_group_obj', _hdf5.h5_open_dset_or_group_obj)
    ll.add_symbol('h5_read', _hdf5.h5_read)
    ll.add_symbol('h5_create_group', _hdf5.h5_create_group)
    ll.add_symbol('h5_write', _hdf5.h5_write)
    ll.add_symbol('h5_close', _hdf5.h5_close)
    ll.add_symbol('h5g_get_num_objs', _hdf5.h5g_get_num_objs)
    ll.add_symbol('h5g_get_objname_by_idx', _hdf5.h5g_get_objname_by_idx)
    ll.add_symbol('h5g_close', _hdf5.h5g_close)
    ll.add_symbol('h5_read_filter', _hdf5.h5_read_filter)
    ll.add_symbol('h5_size', _hdf5.h5_size)
    ll.add_symbol('h5_create_dset', _hdf5.h5_create_dset)


class H5FileType(types.Opaque):

    def __init__(self):
        super(H5FileType, self).__init__(name='H5FileType')


h5file_type = H5FileType()


class H5DatasetType(types.Opaque):

    def __init__(self):
        super(H5DatasetType, self).__init__(name='H5DatasetType')


h5dataset_type = H5DatasetType()


class H5GroupType(types.Opaque):

    def __init__(self):
        super(H5GroupType, self).__init__(name='H5GroupType')


h5group_type = H5GroupType()


class H5DatasetOrGroupType(types.Opaque):

    def __init__(self):
        super(H5DatasetOrGroupType, self).__init__(name='H5DatasetOrGroupType')


h5dataset_or_group_type = H5DatasetOrGroupType()
h5file_data_type = types.int64


@register_model(H5FileType)
@register_model(H5DatasetType)
@register_model(H5GroupType)
@register_model(H5DatasetOrGroupType)
class H5FileModel(models.IntegerModel):

    def __init__(self, dmm, fe_type):
        super(H5FileModel, self).__init__(dmm, h5file_data_type)


string_list_type = types.List(string_type)


@intrinsic
def unify_h5_id(typingctx, tp=None):

    def codegen(context, builder, sig, args):
        return args[0]
    return h5file_type(tp), codegen


@intrinsic
def cast_to_h5_dset(typingctx, tp=None):
    assert tp in (h5dataset_type, h5dataset_or_group_type)

    def codegen(context, builder, sig, args):
        return args[0]
    return h5dataset_type(tp), codegen


h5_open = types.ExternalFunction('h5_open', h5file_type(types.voidptr,
    types.voidptr, types.int64))
if bodo.utils.utils.has_supported_h5py():

    @overload(h5py.File)
    def overload_h5py_file(name, mode=None, driver=None, libver=None,
        userblock_size=None, swmr=False, rdcc_nslots=None, rdcc_nbytes=None,
        rdcc_w0=None, track_order=None, _is_parallel=0):

        def impl(name, mode=None, driver=None, libver=None, userblock_size=
            None, swmr=False, rdcc_nslots=None, rdcc_nbytes=None, rdcc_w0=
            None, track_order=None, _is_parallel=0):
            if mode is None:
                mode = 'a'
            f = h5_open(unicode_to_utf8(name), unicode_to_utf8(mode),
                _is_parallel)
            return f
        return impl
h5_close = types.ExternalFunction('h5_close', types.int32(h5file_type))


@overload_method(H5FileType, 'close', no_unliteral=True)
def overload_h5_file(f):

    def impl(f):
        h5_close(f)
    return impl


@overload_method(H5FileType, 'keys', no_unliteral=True)
@overload_method(H5DatasetOrGroupType, 'keys', no_unliteral=True)
def overload_h5_file_keys(obj_id):

    def h5f_keys_impl(obj_id):
        yhtj__msmta = []
        bxk__fju = h5g_get_num_objs(obj_id)
        for bdthf__lrpby in range(bxk__fju):
            ipcxs__tji = h5g_get_objname_by_idx(obj_id, bdthf__lrpby)
            yhtj__msmta.append(ipcxs__tji)
        return yhtj__msmta
    return h5f_keys_impl


h5_create_dset = types.ExternalFunction('h5_create_dset', h5dataset_type(
    h5file_type, types.voidptr, types.int32, types.voidptr, types.int32))


@overload_method(H5FileType, 'create_dataset', no_unliteral=True)
@overload_method(H5GroupType, 'create_dataset', no_unliteral=True)
def overload_h5_file_create_dataset(obj_id, name, shape=None, dtype=None,
    data=None):
    assert is_overload_none(data)
    wdvsp__cin = parse_dtype(dtype)
    zrrh__tvdke = np.int32(numba_to_c_type(wdvsp__cin))
    ndim = np.int32(len(shape))

    def impl(obj_id, name, shape=None, dtype=None, data=None):
        counts = np.asarray(shape)
        return h5_create_dset(unify_h5_id(obj_id), unicode_to_utf8(name),
            ndim, counts.ctypes, zrrh__tvdke)
    return impl


h5_create_group = types.ExternalFunction('h5_create_group', h5group_type(
    h5file_type, types.voidptr))


@overload_method(H5FileType, 'create_group', no_unliteral=True)
@overload_method(H5GroupType, 'create_group', no_unliteral=True)
def overload_h5_file_create_group(obj_id, name, track_order=None):
    assert is_overload_none(track_order)

    def impl(obj_id, name, track_order=None):
        return h5_create_group(unify_h5_id(obj_id), unicode_to_utf8(name))
    return impl


h5_open_dset_or_group_obj = types.ExternalFunction('h5_open_dset_or_group_obj',
    h5dataset_or_group_type(h5file_type, types.voidptr))


@overload(operator.getitem)
def overload_getitem_file(in_f, in_idx):
    if in_f in (h5file_type, h5dataset_or_group_type
        ) and in_idx == string_type:

        def impl(in_f, in_idx):
            wxjt__vjl = h5_open_dset_or_group_obj(unify_h5_id(in_f),
                unicode_to_utf8(in_idx))
            return wxjt__vjl
        return impl


@infer_global(operator.setitem)
class SetItemH5Dset(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if args[0] == h5dataset_type:
            return signature(types.none, *args)


h5g_close = types.ExternalFunction('h5g_close', types.none(h5group_type))
_h5g_get_num_objs = types.ExternalFunction('h5g_get_num_objs', types.int64(
    h5file_type))


@numba.njit
def h5g_get_num_objs(obj_id):
    return _h5g_get_num_objs(unify_h5_id(obj_id))


_h5g_get_objname_by_idx = types.ExternalFunction('h5g_get_objname_by_idx',
    std_str_type(h5file_type, types.int64))


@numba.njit
def h5g_get_objname_by_idx(obj_id, ind):
    return std_str_to_unicode(_h5g_get_objname_by_idx(unify_h5_id(obj_id), ind)
        )


_h5_read = types.ExternalFunction('h5_read', types.int32(h5dataset_type,
    types.int32, types.voidptr, types.voidptr, types.int64, types.voidptr,
    types.int32))


@numba.njit
def h5read(dset_id, ndim, starts, counts, is_parallel, out_arr):
    ogrjs__vsrur = tuple_to_ptr(starts)
    qrcoz__tlvs = tuple_to_ptr(counts)
    fuf__jdx = bodo.libs.distributed_api.get_type_enum(out_arr)
    return _h5_read(cast_to_h5_dset(dset_id), ndim, ogrjs__vsrur,
        qrcoz__tlvs, is_parallel, out_arr.ctypes, fuf__jdx)


_h5_write = types.ExternalFunction('h5_write', types.int32(h5dataset_type,
    types.int32, types.voidptr, types.voidptr, types.int64, types.voidptr,
    types.int32))


@numba.njit
def h5write(dset_id, ndim, starts, counts, is_parallel, out_arr):
    ogrjs__vsrur = tuple_to_ptr(starts)
    qrcoz__tlvs = tuple_to_ptr(counts)
    fuf__jdx = bodo.libs.distributed_api.get_type_enum(out_arr)
    return _h5_write(cast_to_h5_dset(dset_id), ndim, ogrjs__vsrur,
        qrcoz__tlvs, is_parallel, out_arr.ctypes, fuf__jdx)


def h5_read_dummy():
    return


@infer_global(h5_read_dummy)
class H5ReadType(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        ndim = args[1].literal_value
        dtype = getattr(types, args[2].literal_value)
        okue__xft = types.Array(dtype, ndim, 'C')
        uklb__eapfi = args[3]
        okue__xft = self.context.resolve_function_type(operator.getitem, [
            okue__xft, uklb__eapfi], {}).return_type.copy(layout='C')
        return signature(okue__xft, *args)


H5ReadType._no_unliteral = True
_h5size = types.ExternalFunction('h5_size', types.int64(h5dataset_type,
    types.int32))


@numba.njit
def h5size(obj_id, dim_ind):
    return _h5size(cast_to_h5_dset(obj_id), dim_ind)


sum_op = bodo.libs.distributed_api.Reduce_Type.Sum.value


@numba.njit
def get_filter_read_indices(bool_arr):
    tfq__iqle = bool_arr.nonzero()[0]
    wwa__hhyn = bodo.libs.distributed_api.get_rank()
    cekwz__hhr = bodo.libs.distributed_api.get_size()
    qynnr__epgae = np.empty(cekwz__hhr, np.int64)
    gsf__ttrwj = len(bool_arr)
    bodo.libs.distributed_api.allgather(qynnr__epgae, gsf__ttrwj)
    kxg__nvi = qynnr__epgae.cumsum()[wwa__hhyn] - gsf__ttrwj
    tfq__iqle += kxg__nvi
    lcj__xhko = bodo.libs.distributed_api.dist_reduce(len(tfq__iqle), np.
        int32(sum_op))
    clkgh__cjce = bodo.libs.distributed_api.gatherv(tfq__iqle)
    if wwa__hhyn == 0:
        kcohn__zcldl = clkgh__cjce
    else:
        kcohn__zcldl = np.empty(lcj__xhko, tfq__iqle.dtype)
    bodo.libs.distributed_api.bcast(kcohn__zcldl)
    eahv__bxrx = bodo.libs.distributed_api.get_start(lcj__xhko, cekwz__hhr,
        wwa__hhyn)
    kow__sxpk = bodo.libs.distributed_api.get_end(lcj__xhko, cekwz__hhr,
        wwa__hhyn)
    return kcohn__zcldl[eahv__bxrx:kow__sxpk]


@intrinsic
def tuple_to_ptr(typingctx, tuple_tp=None):

    def codegen(context, builder, sig, args):
        fctk__yabt = cgutils.alloca_once(builder, args[0].type)
        builder.store(args[0], fctk__yabt)
        return builder.bitcast(fctk__yabt, lir.IntType(8).as_pointer())
    return signature(types.voidptr, tuple_tp), codegen


_h5read_filter = types.ExternalFunction('h5_read_filter', types.int32(
    h5dataset_type, types.int32, types.voidptr, types.voidptr, types.intp,
    types.voidptr, types.int32, types.voidptr, types.int32))


@numba.njit
def h5read_filter(dset_id, ndim, starts, counts, is_parallel, out_arr,
    read_indices):
    ogrjs__vsrur = tuple_to_ptr(starts)
    qrcoz__tlvs = tuple_to_ptr(counts)
    fuf__jdx = bodo.libs.distributed_api.get_type_enum(out_arr)
    return _h5read_filter(cast_to_h5_dset(dset_id), ndim, ogrjs__vsrur,
        qrcoz__tlvs, is_parallel, out_arr.ctypes, fuf__jdx, read_indices.
        ctypes, len(read_indices))
