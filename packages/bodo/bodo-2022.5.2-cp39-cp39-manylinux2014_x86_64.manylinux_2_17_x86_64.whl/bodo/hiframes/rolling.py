"""implementations of rolling window functions (sequential and parallel)
"""
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.core.imputils import impl_ret_borrowed
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import lower_builtin, overload, register_jitable
import bodo
from bodo.libs.distributed_api import Reduce_Type
from bodo.utils.typing import BodoError, decode_if_dict_array, get_overload_const_func, get_overload_const_str, is_const_func_type, is_overload_constant_bool, is_overload_constant_str, is_overload_none, is_overload_true
from bodo.utils.utils import unliteral_all
supported_rolling_funcs = ('sum', 'mean', 'var', 'std', 'count', 'median',
    'min', 'max', 'cov', 'corr', 'apply')
unsupported_rolling_methods = ['skew', 'kurt', 'aggregate', 'quantile', 'sem']


def rolling_fixed(arr, win):
    return arr


def rolling_variable(arr, on_arr, win):
    return arr


def rolling_cov(arr, arr2, win):
    return arr


def rolling_corr(arr, arr2, win):
    return arr


@infer_global(rolling_cov)
@infer_global(rolling_corr)
class RollingCovType(AbstractTemplate):

    def generic(self, args, kws):
        arr = args[0]
        yap__ndn = arr.copy(dtype=types.float64)
        return signature(yap__ndn, *unliteral_all(args))


@lower_builtin(rolling_corr, types.VarArg(types.Any))
@lower_builtin(rolling_cov, types.VarArg(types.Any))
def lower_rolling_corr_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


@overload(rolling_fixed, no_unliteral=True)
def overload_rolling_fixed(arr, index_arr, win, minp, center, fname, raw=
    True, parallel=False):
    assert is_overload_constant_bool(raw
        ), 'raw argument should be constant bool'
    if is_const_func_type(fname):
        func = _get_apply_func(fname)
        return (lambda arr, index_arr, win, minp, center, fname, raw=True,
            parallel=False: roll_fixed_apply(arr, index_arr, win, minp,
            center, parallel, func, raw))
    assert is_overload_constant_str(fname)
    jof__fmn = get_overload_const_str(fname)
    if jof__fmn not in ('sum', 'mean', 'var', 'std', 'count', 'median',
        'min', 'max'):
        raise BodoError('invalid rolling (fixed window) function {}'.format
            (jof__fmn))
    if jof__fmn in ('median', 'min', 'max'):
        gxlo__prr = 'def kernel_func(A):\n'
        gxlo__prr += '  if np.isnan(A).sum() != 0: return np.nan\n'
        gxlo__prr += '  return np.{}(A)\n'.format(jof__fmn)
        sga__jhbfo = {}
        exec(gxlo__prr, {'np': np}, sga__jhbfo)
        kernel_func = register_jitable(sga__jhbfo['kernel_func'])
        return (lambda arr, index_arr, win, minp, center, fname, raw=True,
            parallel=False: roll_fixed_apply(arr, index_arr, win, minp,
            center, parallel, kernel_func))
    init_kernel, add_kernel, remove_kernel, calc_kernel = linear_kernels[
        jof__fmn]
    return (lambda arr, index_arr, win, minp, center, fname, raw=True,
        parallel=False: roll_fixed_linear_generic(arr, win, minp, center,
        parallel, init_kernel, add_kernel, remove_kernel, calc_kernel))


@overload(rolling_variable, no_unliteral=True)
def overload_rolling_variable(arr, on_arr, index_arr, win, minp, center,
    fname, raw=True, parallel=False):
    assert is_overload_constant_bool(raw)
    if is_const_func_type(fname):
        func = _get_apply_func(fname)
        return (lambda arr, on_arr, index_arr, win, minp, center, fname,
            raw=True, parallel=False: roll_variable_apply(arr, on_arr,
            index_arr, win, minp, center, parallel, func, raw))
    assert is_overload_constant_str(fname)
    jof__fmn = get_overload_const_str(fname)
    if jof__fmn not in ('sum', 'mean', 'var', 'std', 'count', 'median',
        'min', 'max'):
        raise BodoError('invalid rolling (variable window) function {}'.
            format(jof__fmn))
    if jof__fmn in ('median', 'min', 'max'):
        gxlo__prr = 'def kernel_func(A):\n'
        gxlo__prr += '  arr  = dropna(A)\n'
        gxlo__prr += '  if len(arr) == 0: return np.nan\n'
        gxlo__prr += '  return np.{}(arr)\n'.format(jof__fmn)
        sga__jhbfo = {}
        exec(gxlo__prr, {'np': np, 'dropna': _dropna}, sga__jhbfo)
        kernel_func = register_jitable(sga__jhbfo['kernel_func'])
        return (lambda arr, on_arr, index_arr, win, minp, center, fname,
            raw=True, parallel=False: roll_variable_apply(arr, on_arr,
            index_arr, win, minp, center, parallel, kernel_func))
    init_kernel, add_kernel, remove_kernel, calc_kernel = linear_kernels[
        jof__fmn]
    return (lambda arr, on_arr, index_arr, win, minp, center, fname, raw=
        True, parallel=False: roll_var_linear_generic(arr, on_arr, win,
        minp, center, parallel, init_kernel, add_kernel, remove_kernel,
        calc_kernel))


def _get_apply_func(f_type):
    func = get_overload_const_func(f_type, None)
    return bodo.compiler.udf_jit(func)


comm_border_tag = 22


@register_jitable
def roll_fixed_linear_generic(in_arr, win, minp, center, parallel,
    init_data, add_obs, remove_obs, calc_out):
    _validate_roll_fixed_args(win, minp)
    in_arr = prep_values(in_arr)
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    N = len(in_arr)
    offset = (win - 1) // 2 if center else 0
    if parallel:
        halo_size = np.int32(win // 2) if center else np.int32(win - 1)
        if _is_small_for_parallel(N, halo_size):
            return _handle_small_data(in_arr, win, minp, center, rank,
                n_pes, init_data, add_obs, remove_obs, calc_out)
        snpbt__djy = _border_icomm(in_arr, rank, n_pes, halo_size, True, center
            )
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            kdm__qtvvk) = snpbt__djy
    output, data = roll_fixed_linear_generic_seq(in_arr, win, minp, center,
        init_data, add_obs, remove_obs, calc_out)
    if parallel:
        _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, center)
        if center and rank != n_pes - 1:
            bodo.libs.distributed_api.wait(kdm__qtvvk, True)
            for sulr__elc in range(0, halo_size):
                data = add_obs(r_recv_buff[sulr__elc], *data)
                icmwk__wtg = in_arr[N + sulr__elc - win]
                data = remove_obs(icmwk__wtg, *data)
                output[N + sulr__elc - offset] = calc_out(minp, *data)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            data = init_data()
            for sulr__elc in range(0, halo_size):
                data = add_obs(l_recv_buff[sulr__elc], *data)
            for sulr__elc in range(0, win - 1):
                data = add_obs(in_arr[sulr__elc], *data)
                if sulr__elc > offset:
                    icmwk__wtg = l_recv_buff[sulr__elc - offset - 1]
                    data = remove_obs(icmwk__wtg, *data)
                if sulr__elc >= offset:
                    output[sulr__elc - offset] = calc_out(minp, *data)
    return output


@register_jitable
def roll_fixed_linear_generic_seq(in_arr, win, minp, center, init_data,
    add_obs, remove_obs, calc_out):
    data = init_data()
    N = len(in_arr)
    offset = (win - 1) // 2 if center else 0
    output = np.empty(N, dtype=np.float64)
    roth__mjc = max(minp, 1) - 1
    roth__mjc = min(roth__mjc, N)
    for sulr__elc in range(0, roth__mjc):
        data = add_obs(in_arr[sulr__elc], *data)
        if sulr__elc >= offset:
            output[sulr__elc - offset] = calc_out(minp, *data)
    for sulr__elc in range(roth__mjc, N):
        val = in_arr[sulr__elc]
        data = add_obs(val, *data)
        if sulr__elc > win - 1:
            icmwk__wtg = in_arr[sulr__elc - win]
            data = remove_obs(icmwk__wtg, *data)
        output[sulr__elc - offset] = calc_out(minp, *data)
    uhqji__nzq = data
    for sulr__elc in range(N, N + offset):
        if sulr__elc > win - 1:
            icmwk__wtg = in_arr[sulr__elc - win]
            data = remove_obs(icmwk__wtg, *data)
        output[sulr__elc - offset] = calc_out(minp, *data)
    return output, uhqji__nzq


def roll_fixed_apply(in_arr, index_arr, win, minp, center, parallel,
    kernel_func, raw=True):
    pass


@overload(roll_fixed_apply, no_unliteral=True)
def overload_roll_fixed_apply(in_arr, index_arr, win, minp, center,
    parallel, kernel_func, raw=True):
    assert is_overload_constant_bool(raw)
    return roll_fixed_apply_impl


def roll_fixed_apply_impl(in_arr, index_arr, win, minp, center, parallel,
    kernel_func, raw=True):
    _validate_roll_fixed_args(win, minp)
    in_arr = prep_values(in_arr)
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    N = len(in_arr)
    offset = (win - 1) // 2 if center else 0
    index_arr = fix_index_arr(index_arr)
    if parallel:
        halo_size = np.int32(win // 2) if center else np.int32(win - 1)
        if _is_small_for_parallel(N, halo_size):
            return _handle_small_data_apply(in_arr, index_arr, win, minp,
                center, rank, n_pes, kernel_func, raw)
        snpbt__djy = _border_icomm(in_arr, rank, n_pes, halo_size, True, center
            )
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            kdm__qtvvk) = snpbt__djy
        if raw == False:
            knq__mft = _border_icomm(index_arr, rank, n_pes, halo_size, 
                True, center)
            (l_recv_buff_idx, r_recv_buff_idx, yunsr__muu, faoul__poy,
                hpt__iaa, rho__yecyx) = knq__mft
    output = roll_fixed_apply_seq(in_arr, index_arr, win, minp, center,
        kernel_func, raw)
    if parallel:
        _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, center)
        if raw == False:
            _border_send_wait(faoul__poy, yunsr__muu, rank, n_pes, True, center
                )
        if center and rank != n_pes - 1:
            bodo.libs.distributed_api.wait(kdm__qtvvk, True)
            if raw == False:
                bodo.libs.distributed_api.wait(rho__yecyx, True)
            recv_right_compute(output, in_arr, index_arr, N, win, minp,
                offset, r_recv_buff, r_recv_buff_idx, kernel_func, raw)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            if raw == False:
                bodo.libs.distributed_api.wait(hpt__iaa, True)
            recv_left_compute(output, in_arr, index_arr, win, minp, offset,
                l_recv_buff, l_recv_buff_idx, kernel_func, raw)
    return output


def recv_right_compute(output, in_arr, index_arr, N, win, minp, offset,
    r_recv_buff, r_recv_buff_idx, kernel_func, raw):
    pass


@overload(recv_right_compute, no_unliteral=True)
def overload_recv_right_compute(output, in_arr, index_arr, N, win, minp,
    offset, r_recv_buff, r_recv_buff_idx, kernel_func, raw):
    assert is_overload_constant_bool(raw)
    if is_overload_true(raw):

        def impl(output, in_arr, index_arr, N, win, minp, offset,
            r_recv_buff, r_recv_buff_idx, kernel_func, raw):
            uhqji__nzq = np.concatenate((in_arr[N - win + 1:], r_recv_buff))
            bdgnl__mkuu = 0
            for sulr__elc in range(max(N - offset, 0), N):
                data = uhqji__nzq[bdgnl__mkuu:bdgnl__mkuu + win]
                if win - np.isnan(data).sum() < minp:
                    output[sulr__elc] = np.nan
                else:
                    output[sulr__elc] = kernel_func(data)
                bdgnl__mkuu += 1
        return impl

    def impl_series(output, in_arr, index_arr, N, win, minp, offset,
        r_recv_buff, r_recv_buff_idx, kernel_func, raw):
        uhqji__nzq = np.concatenate((in_arr[N - win + 1:], r_recv_buff))
        ocnkj__shbuh = np.concatenate((index_arr[N - win + 1:],
            r_recv_buff_idx))
        bdgnl__mkuu = 0
        for sulr__elc in range(max(N - offset, 0), N):
            data = uhqji__nzq[bdgnl__mkuu:bdgnl__mkuu + win]
            if win - np.isnan(data).sum() < minp:
                output[sulr__elc] = np.nan
            else:
                output[sulr__elc] = kernel_func(pd.Series(data,
                    ocnkj__shbuh[bdgnl__mkuu:bdgnl__mkuu + win]))
            bdgnl__mkuu += 1
    return impl_series


def recv_left_compute(output, in_arr, index_arr, win, minp, offset,
    l_recv_buff, l_recv_buff_idx, kernel_func, raw):
    pass


@overload(recv_left_compute, no_unliteral=True)
def overload_recv_left_compute(output, in_arr, index_arr, win, minp, offset,
    l_recv_buff, l_recv_buff_idx, kernel_func, raw):
    assert is_overload_constant_bool(raw)
    if is_overload_true(raw):

        def impl(output, in_arr, index_arr, win, minp, offset, l_recv_buff,
            l_recv_buff_idx, kernel_func, raw):
            uhqji__nzq = np.concatenate((l_recv_buff, in_arr[:win - 1]))
            for sulr__elc in range(0, win - offset - 1):
                data = uhqji__nzq[sulr__elc:sulr__elc + win]
                if win - np.isnan(data).sum() < minp:
                    output[sulr__elc] = np.nan
                else:
                    output[sulr__elc] = kernel_func(data)
        return impl

    def impl_series(output, in_arr, index_arr, win, minp, offset,
        l_recv_buff, l_recv_buff_idx, kernel_func, raw):
        uhqji__nzq = np.concatenate((l_recv_buff, in_arr[:win - 1]))
        ocnkj__shbuh = np.concatenate((l_recv_buff_idx, index_arr[:win - 1]))
        for sulr__elc in range(0, win - offset - 1):
            data = uhqji__nzq[sulr__elc:sulr__elc + win]
            if win - np.isnan(data).sum() < minp:
                output[sulr__elc] = np.nan
            else:
                output[sulr__elc] = kernel_func(pd.Series(data,
                    ocnkj__shbuh[sulr__elc:sulr__elc + win]))
    return impl_series


def roll_fixed_apply_seq(in_arr, index_arr, win, minp, center, kernel_func,
    raw=True):
    pass


@overload(roll_fixed_apply_seq, no_unliteral=True)
def overload_roll_fixed_apply_seq(in_arr, index_arr, win, minp, center,
    kernel_func, raw=True):
    assert is_overload_constant_bool(raw), "'raw' should be constant bool"

    def roll_fixed_apply_seq_impl(in_arr, index_arr, win, minp, center,
        kernel_func, raw=True):
        N = len(in_arr)
        output = np.empty(N, dtype=np.float64)
        offset = (win - 1) // 2 if center else 0
        for sulr__elc in range(0, N):
            start = max(sulr__elc - win + 1 + offset, 0)
            end = min(sulr__elc + 1 + offset, N)
            data = in_arr[start:end]
            if end - start - np.isnan(data).sum() < minp:
                output[sulr__elc] = np.nan
            else:
                output[sulr__elc] = apply_func(kernel_func, data, index_arr,
                    start, end, raw)
        return output
    return roll_fixed_apply_seq_impl


def apply_func(kernel_func, data, index_arr, start, end, raw):
    return kernel_func(data)


@overload(apply_func, no_unliteral=True)
def overload_apply_func(kernel_func, data, index_arr, start, end, raw):
    assert is_overload_constant_bool(raw), "'raw' should be constant bool"
    if is_overload_true(raw):
        return (lambda kernel_func, data, index_arr, start, end, raw:
            kernel_func(data))
    return lambda kernel_func, data, index_arr, start, end, raw: kernel_func(pd
        .Series(data, index_arr[start:end]))


def fix_index_arr(A):
    return A


@overload(fix_index_arr)
def overload_fix_index_arr(A):
    if is_overload_none(A):
        return lambda A: np.zeros(3)
    return lambda A: A


def get_offset_nanos(w):
    out = status = 0
    try:
        out = pd.tseries.frequencies.to_offset(w).nanos
    except:
        status = 1
    return out, status


def offset_to_nanos(w):
    return w


@overload(offset_to_nanos)
def overload_offset_to_nanos(w):
    if isinstance(w, types.Integer):
        return lambda w: w

    def impl(w):
        with numba.objmode(out='int64', status='int64'):
            out, status = get_offset_nanos(w)
        if status != 0:
            raise ValueError('Invalid offset value')
        return out
    return impl


@register_jitable
def roll_var_linear_generic(in_arr, on_arr_dt, win, minp, center, parallel,
    init_data, add_obs, remove_obs, calc_out):
    _validate_roll_var_args(minp, center)
    in_arr = prep_values(in_arr)
    win = offset_to_nanos(win)
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    on_arr = cast_dt64_arr_to_int(on_arr_dt)
    N = len(in_arr)
    left_closed = False
    right_closed = True
    if parallel:
        if _is_small_for_parallel_variable(on_arr, win):
            return _handle_small_data_variable(in_arr, on_arr, win, minp,
                rank, n_pes, init_data, add_obs, remove_obs, calc_out)
        snpbt__djy = _border_icomm_var(in_arr, on_arr, rank, n_pes, win)
        (l_recv_buff, l_recv_t_buff, r_send_req, yjw__wjnu, l_recv_req,
            kkd__jbwc) = snpbt__djy
    start, end = _build_indexer(on_arr, N, win, left_closed, right_closed)
    output = roll_var_linear_generic_seq(in_arr, on_arr, win, minp, start,
        end, init_data, add_obs, remove_obs, calc_out)
    if parallel:
        _border_send_wait(r_send_req, r_send_req, rank, n_pes, True, False)
        _border_send_wait(yjw__wjnu, yjw__wjnu, rank, n_pes, True, False)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            bodo.libs.distributed_api.wait(kkd__jbwc, True)
            num_zero_starts = 0
            for sulr__elc in range(0, N):
                if start[sulr__elc] != 0:
                    break
                num_zero_starts += 1
            if num_zero_starts == 0:
                return output
            recv_starts = _get_var_recv_starts(on_arr, l_recv_t_buff,
                num_zero_starts, win)
            data = init_data()
            for sska__rqt in range(recv_starts[0], len(l_recv_t_buff)):
                data = add_obs(l_recv_buff[sska__rqt], *data)
            if right_closed:
                data = add_obs(in_arr[0], *data)
            output[0] = calc_out(minp, *data)
            for sulr__elc in range(1, num_zero_starts):
                s = recv_starts[sulr__elc]
                frrc__qck = end[sulr__elc]
                for sska__rqt in range(recv_starts[sulr__elc - 1], s):
                    data = remove_obs(l_recv_buff[sska__rqt], *data)
                for sska__rqt in range(end[sulr__elc - 1], frrc__qck):
                    data = add_obs(in_arr[sska__rqt], *data)
                output[sulr__elc] = calc_out(minp, *data)
    return output


@register_jitable(cache=True)
def _get_var_recv_starts(on_arr, l_recv_t_buff, num_zero_starts, win):
    recv_starts = np.zeros(num_zero_starts, np.int64)
    halo_size = len(l_recv_t_buff)
    lkbvs__mkk = cast_dt64_arr_to_int(on_arr)
    left_closed = False
    xhld__mvnjk = lkbvs__mkk[0] - win
    if left_closed:
        xhld__mvnjk -= 1
    recv_starts[0] = halo_size
    for sska__rqt in range(0, halo_size):
        if l_recv_t_buff[sska__rqt] > xhld__mvnjk:
            recv_starts[0] = sska__rqt
            break
    for sulr__elc in range(1, num_zero_starts):
        xhld__mvnjk = lkbvs__mkk[sulr__elc] - win
        if left_closed:
            xhld__mvnjk -= 1
        recv_starts[sulr__elc] = halo_size
        for sska__rqt in range(recv_starts[sulr__elc - 1], halo_size):
            if l_recv_t_buff[sska__rqt] > xhld__mvnjk:
                recv_starts[sulr__elc] = sska__rqt
                break
    return recv_starts


@register_jitable
def roll_var_linear_generic_seq(in_arr, on_arr, win, minp, start, end,
    init_data, add_obs, remove_obs, calc_out):
    N = len(in_arr)
    output = np.empty(N, np.float64)
    data = init_data()
    for sska__rqt in range(start[0], end[0]):
        data = add_obs(in_arr[sska__rqt], *data)
    output[0] = calc_out(minp, *data)
    for sulr__elc in range(1, N):
        s = start[sulr__elc]
        frrc__qck = end[sulr__elc]
        for sska__rqt in range(start[sulr__elc - 1], s):
            data = remove_obs(in_arr[sska__rqt], *data)
        for sska__rqt in range(end[sulr__elc - 1], frrc__qck):
            data = add_obs(in_arr[sska__rqt], *data)
        output[sulr__elc] = calc_out(minp, *data)
    return output


def roll_variable_apply(in_arr, on_arr_dt, index_arr, win, minp, center,
    parallel, kernel_func, raw=True):
    pass


@overload(roll_variable_apply, no_unliteral=True)
def overload_roll_variable_apply(in_arr, on_arr_dt, index_arr, win, minp,
    center, parallel, kernel_func, raw=True):
    assert is_overload_constant_bool(raw)
    return roll_variable_apply_impl


def roll_variable_apply_impl(in_arr, on_arr_dt, index_arr, win, minp,
    center, parallel, kernel_func, raw=True):
    _validate_roll_var_args(minp, center)
    in_arr = prep_values(in_arr)
    win = offset_to_nanos(win)
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    on_arr = cast_dt64_arr_to_int(on_arr_dt)
    index_arr = fix_index_arr(index_arr)
    N = len(in_arr)
    left_closed = False
    right_closed = True
    if parallel:
        if _is_small_for_parallel_variable(on_arr, win):
            return _handle_small_data_variable_apply(in_arr, on_arr,
                index_arr, win, minp, rank, n_pes, kernel_func, raw)
        snpbt__djy = _border_icomm_var(in_arr, on_arr, rank, n_pes, win)
        (l_recv_buff, l_recv_t_buff, r_send_req, yjw__wjnu, l_recv_req,
            kkd__jbwc) = snpbt__djy
        if raw == False:
            knq__mft = _border_icomm_var(index_arr, on_arr, rank, n_pes, win)
            (l_recv_buff_idx, huio__jhrnu, faoul__poy, uvgbf__izy, hpt__iaa,
                ddr__rpio) = knq__mft
    start, end = _build_indexer(on_arr, N, win, left_closed, right_closed)
    output = roll_variable_apply_seq(in_arr, on_arr, index_arr, win, minp,
        start, end, kernel_func, raw)
    if parallel:
        _border_send_wait(r_send_req, r_send_req, rank, n_pes, True, False)
        _border_send_wait(yjw__wjnu, yjw__wjnu, rank, n_pes, True, False)
        if raw == False:
            _border_send_wait(faoul__poy, faoul__poy, rank, n_pes, True, False)
            _border_send_wait(uvgbf__izy, uvgbf__izy, rank, n_pes, True, False)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            bodo.libs.distributed_api.wait(kkd__jbwc, True)
            if raw == False:
                bodo.libs.distributed_api.wait(hpt__iaa, True)
                bodo.libs.distributed_api.wait(ddr__rpio, True)
            num_zero_starts = 0
            for sulr__elc in range(0, N):
                if start[sulr__elc] != 0:
                    break
                num_zero_starts += 1
            if num_zero_starts == 0:
                return output
            recv_starts = _get_var_recv_starts(on_arr, l_recv_t_buff,
                num_zero_starts, win)
            recv_left_var_compute(output, in_arr, index_arr,
                num_zero_starts, recv_starts, l_recv_buff, l_recv_buff_idx,
                minp, kernel_func, raw)
    return output


def recv_left_var_compute(output, in_arr, index_arr, num_zero_starts,
    recv_starts, l_recv_buff, l_recv_buff_idx, minp, kernel_func, raw):
    pass


@overload(recv_left_var_compute)
def overload_recv_left_var_compute(output, in_arr, index_arr,
    num_zero_starts, recv_starts, l_recv_buff, l_recv_buff_idx, minp,
    kernel_func, raw):
    assert is_overload_constant_bool(raw)
    if is_overload_true(raw):

        def impl(output, in_arr, index_arr, num_zero_starts, recv_starts,
            l_recv_buff, l_recv_buff_idx, minp, kernel_func, raw):
            for sulr__elc in range(0, num_zero_starts):
                hxnu__cmey = recv_starts[sulr__elc]
                upqvf__pni = np.concatenate((l_recv_buff[hxnu__cmey:],
                    in_arr[:sulr__elc + 1]))
                if len(upqvf__pni) - np.isnan(upqvf__pni).sum() >= minp:
                    output[sulr__elc] = kernel_func(upqvf__pni)
                else:
                    output[sulr__elc] = np.nan
        return impl

    def impl_series(output, in_arr, index_arr, num_zero_starts, recv_starts,
        l_recv_buff, l_recv_buff_idx, minp, kernel_func, raw):
        for sulr__elc in range(0, num_zero_starts):
            hxnu__cmey = recv_starts[sulr__elc]
            upqvf__pni = np.concatenate((l_recv_buff[hxnu__cmey:], in_arr[:
                sulr__elc + 1]))
            xskhb__pxm = np.concatenate((l_recv_buff_idx[hxnu__cmey:],
                index_arr[:sulr__elc + 1]))
            if len(upqvf__pni) - np.isnan(upqvf__pni).sum() >= minp:
                output[sulr__elc] = kernel_func(pd.Series(upqvf__pni,
                    xskhb__pxm))
            else:
                output[sulr__elc] = np.nan
    return impl_series


def roll_variable_apply_seq(in_arr, on_arr, index_arr, win, minp, start,
    end, kernel_func, raw):
    pass


@overload(roll_variable_apply_seq)
def overload_roll_variable_apply_seq(in_arr, on_arr, index_arr, win, minp,
    start, end, kernel_func, raw):
    assert is_overload_constant_bool(raw)
    if is_overload_true(raw):
        return roll_variable_apply_seq_impl
    return roll_variable_apply_seq_impl_series


def roll_variable_apply_seq_impl(in_arr, on_arr, index_arr, win, minp,
    start, end, kernel_func, raw):
    N = len(in_arr)
    output = np.empty(N, dtype=np.float64)
    for sulr__elc in range(0, N):
        s = start[sulr__elc]
        frrc__qck = end[sulr__elc]
        data = in_arr[s:frrc__qck]
        if frrc__qck - s - np.isnan(data).sum() >= minp:
            output[sulr__elc] = kernel_func(data)
        else:
            output[sulr__elc] = np.nan
    return output


def roll_variable_apply_seq_impl_series(in_arr, on_arr, index_arr, win,
    minp, start, end, kernel_func, raw):
    N = len(in_arr)
    output = np.empty(N, dtype=np.float64)
    for sulr__elc in range(0, N):
        s = start[sulr__elc]
        frrc__qck = end[sulr__elc]
        data = in_arr[s:frrc__qck]
        if frrc__qck - s - np.isnan(data).sum() >= minp:
            output[sulr__elc] = kernel_func(pd.Series(data, index_arr[s:
                frrc__qck]))
        else:
            output[sulr__elc] = np.nan
    return output


@register_jitable(cache=True)
def _build_indexer(on_arr, N, win, left_closed, right_closed):
    lkbvs__mkk = cast_dt64_arr_to_int(on_arr)
    start = np.empty(N, np.int64)
    end = np.empty(N, np.int64)
    start[0] = 0
    if right_closed:
        end[0] = 1
    else:
        end[0] = 0
    for sulr__elc in range(1, N):
        okoq__hevm = lkbvs__mkk[sulr__elc]
        xhld__mvnjk = lkbvs__mkk[sulr__elc] - win
        if left_closed:
            xhld__mvnjk -= 1
        start[sulr__elc] = sulr__elc
        for sska__rqt in range(start[sulr__elc - 1], sulr__elc):
            if lkbvs__mkk[sska__rqt] > xhld__mvnjk:
                start[sulr__elc] = sska__rqt
                break
        if lkbvs__mkk[end[sulr__elc - 1]] <= okoq__hevm:
            end[sulr__elc] = sulr__elc + 1
        else:
            end[sulr__elc] = end[sulr__elc - 1]
        if not right_closed:
            end[sulr__elc] -= 1
    return start, end


@register_jitable
def init_data_sum():
    return 0, 0.0


@register_jitable
def add_sum(val, nobs, sum_x):
    if not np.isnan(val):
        nobs += 1
        sum_x += val
    return nobs, sum_x


@register_jitable
def remove_sum(val, nobs, sum_x):
    if not np.isnan(val):
        nobs -= 1
        sum_x -= val
    return nobs, sum_x


@register_jitable
def calc_sum(minp, nobs, sum_x):
    return sum_x if nobs >= minp else np.nan


@register_jitable
def init_data_mean():
    return 0, 0.0, 0


@register_jitable
def add_mean(val, nobs, sum_x, neg_ct):
    if not np.isnan(val):
        nobs += 1
        sum_x += val
        if val < 0:
            neg_ct += 1
    return nobs, sum_x, neg_ct


@register_jitable
def remove_mean(val, nobs, sum_x, neg_ct):
    if not np.isnan(val):
        nobs -= 1
        sum_x -= val
        if val < 0:
            neg_ct -= 1
    return nobs, sum_x, neg_ct


@register_jitable
def calc_mean(minp, nobs, sum_x, neg_ct):
    if nobs >= minp:
        yya__xil = sum_x / nobs
        if neg_ct == 0 and yya__xil < 0.0:
            yya__xil = 0
        elif neg_ct == nobs and yya__xil > 0.0:
            yya__xil = 0
    else:
        yya__xil = np.nan
    return yya__xil


@register_jitable
def init_data_var():
    return 0, 0.0, 0.0


@register_jitable
def add_var(val, nobs, mean_x, ssqdm_x):
    if not np.isnan(val):
        nobs += 1
        krnez__siyu = val - mean_x
        mean_x += krnez__siyu / nobs
        ssqdm_x += (nobs - 1) * krnez__siyu ** 2 / nobs
    return nobs, mean_x, ssqdm_x


@register_jitable
def remove_var(val, nobs, mean_x, ssqdm_x):
    if not np.isnan(val):
        nobs -= 1
        if nobs != 0:
            krnez__siyu = val - mean_x
            mean_x -= krnez__siyu / nobs
            ssqdm_x -= (nobs + 1) * krnez__siyu ** 2 / nobs
        else:
            mean_x = 0.0
            ssqdm_x = 0.0
    return nobs, mean_x, ssqdm_x


@register_jitable
def calc_var(minp, nobs, mean_x, ssqdm_x):
    bckc__anl = 1.0
    yya__xil = np.nan
    if nobs >= minp and nobs > bckc__anl:
        if nobs == 1:
            yya__xil = 0.0
        else:
            yya__xil = ssqdm_x / (nobs - bckc__anl)
            if yya__xil < 0.0:
                yya__xil = 0.0
    return yya__xil


@register_jitable
def calc_std(minp, nobs, mean_x, ssqdm_x):
    nesr__omm = calc_var(minp, nobs, mean_x, ssqdm_x)
    return np.sqrt(nesr__omm)


@register_jitable
def init_data_count():
    return 0.0,


@register_jitable
def add_count(val, count_x):
    if not np.isnan(val):
        count_x += 1.0
    return count_x,


@register_jitable
def remove_count(val, count_x):
    if not np.isnan(val):
        count_x -= 1.0
    return count_x,


@register_jitable
def calc_count(minp, count_x):
    return count_x


@register_jitable
def calc_count_var(minp, count_x):
    return count_x if count_x >= minp else np.nan


linear_kernels = {'sum': (init_data_sum, add_sum, remove_sum, calc_sum),
    'mean': (init_data_mean, add_mean, remove_mean, calc_mean), 'var': (
    init_data_var, add_var, remove_var, calc_var), 'std': (init_data_var,
    add_var, remove_var, calc_std), 'count': (init_data_count, add_count,
    remove_count, calc_count)}


def shift():
    return


@overload(shift, jit_options={'cache': True})
def shift_overload(in_arr, shift, parallel):
    if not isinstance(parallel, types.Literal):
        return shift_impl


def shift_impl(in_arr, shift, parallel):
    N = len(in_arr)
    in_arr = decode_if_dict_array(in_arr)
    output = alloc_shift(N, in_arr, (-1,))
    send_right = shift > 0
    send_left = shift <= 0
    is_parallel_str = False
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        halo_size = np.int32(abs(shift))
        if _is_small_for_parallel(N, halo_size):
            return _handle_small_data_shift(in_arr, shift, rank, n_pes)
        snpbt__djy = _border_icomm(in_arr, rank, n_pes, halo_size,
            send_right, send_left)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            kdm__qtvvk) = snpbt__djy
        if send_right and is_str_binary_array(in_arr):
            is_parallel_str = True
            shift_left_recv(r_send_req, l_send_req, rank, n_pes, halo_size,
                l_recv_req, l_recv_buff, output)
    shift_seq(in_arr, shift, output, is_parallel_str)
    if parallel:
        if send_right:
            if not is_str_binary_array(in_arr):
                shift_left_recv(r_send_req, l_send_req, rank, n_pes,
                    halo_size, l_recv_req, l_recv_buff, output)
        else:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, False, True)
            if rank != n_pes - 1:
                bodo.libs.distributed_api.wait(kdm__qtvvk, True)
                for sulr__elc in range(0, halo_size):
                    if bodo.libs.array_kernels.isna(r_recv_buff, sulr__elc):
                        bodo.libs.array_kernels.setna(output, N - halo_size +
                            sulr__elc)
                        continue
                    output[N - halo_size + sulr__elc] = r_recv_buff[sulr__elc]
    return output


@register_jitable(cache=True)
def shift_seq(in_arr, shift, output, is_parallel_str=False):
    N = len(in_arr)
    deh__hccbu = 1 if shift > 0 else -1
    shift = deh__hccbu * min(abs(shift), N)
    if shift > 0 and (not is_parallel_str or bodo.get_rank() == 0):
        bodo.libs.array_kernels.setna_slice(output, slice(None, shift))
    start = max(shift, 0)
    end = min(N, N + shift)
    for sulr__elc in range(start, end):
        if bodo.libs.array_kernels.isna(in_arr, sulr__elc - shift):
            bodo.libs.array_kernels.setna(output, sulr__elc)
            continue
        output[sulr__elc] = in_arr[sulr__elc - shift]
    if shift < 0:
        bodo.libs.array_kernels.setna_slice(output, slice(shift, None))
    return output


@register_jitable
def shift_left_recv(r_send_req, l_send_req, rank, n_pes, halo_size,
    l_recv_req, l_recv_buff, output):
    _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, False)
    if rank != 0:
        bodo.libs.distributed_api.wait(l_recv_req, True)
        for sulr__elc in range(0, halo_size):
            if bodo.libs.array_kernels.isna(l_recv_buff, sulr__elc):
                bodo.libs.array_kernels.setna(output, sulr__elc)
                continue
            output[sulr__elc] = l_recv_buff[sulr__elc]


def is_str_binary_array(arr):
    return False


@overload(is_str_binary_array)
def overload_is_str_binary_array(arr):
    if arr in [bodo.string_array_type, bodo.binary_array_type]:
        return lambda arr: True
    return lambda arr: False


def is_supported_shift_array_type(arr_type):
    return isinstance(arr_type, types.Array) and (isinstance(arr_type.dtype,
        types.Number) or arr_type.dtype in [bodo.datetime64ns, bodo.
        timedelta64ns]) or isinstance(arr_type, (bodo.IntegerArrayType,
        bodo.DecimalArrayType)) or arr_type in (bodo.boolean_array, bodo.
        datetime_date_array_type, bodo.string_array_type, bodo.
        binary_array_type, bodo.dict_str_arr_type)


def pct_change():
    return


@overload(pct_change, jit_options={'cache': True})
def pct_change_overload(in_arr, shift, parallel):
    if not isinstance(parallel, types.Literal):
        return pct_change_impl


def pct_change_impl(in_arr, shift, parallel):
    N = len(in_arr)
    send_right = shift > 0
    send_left = shift <= 0
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        halo_size = np.int32(abs(shift))
        if _is_small_for_parallel(N, halo_size):
            return _handle_small_data_pct_change(in_arr, shift, rank, n_pes)
        snpbt__djy = _border_icomm(in_arr, rank, n_pes, halo_size,
            send_right, send_left)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            kdm__qtvvk) = snpbt__djy
    output = pct_change_seq(in_arr, shift)
    if parallel:
        if send_right:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, False)
            if rank != 0:
                bodo.libs.distributed_api.wait(l_recv_req, True)
                for sulr__elc in range(0, halo_size):
                    nsp__mzd = l_recv_buff[sulr__elc]
                    output[sulr__elc] = (in_arr[sulr__elc] - nsp__mzd
                        ) / nsp__mzd
        else:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, False, True)
            if rank != n_pes - 1:
                bodo.libs.distributed_api.wait(kdm__qtvvk, True)
                for sulr__elc in range(0, halo_size):
                    nsp__mzd = r_recv_buff[sulr__elc]
                    output[N - halo_size + sulr__elc] = (in_arr[N -
                        halo_size + sulr__elc] - nsp__mzd) / nsp__mzd
    return output


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_first_non_na(arr):
    if isinstance(arr.dtype, (types.Integer, types.Boolean)):
        zero = arr.dtype(0)
        return lambda arr: zero if len(arr) == 0 else arr[0]
    assert isinstance(arr.dtype, types.Float)
    zibyu__yyhkl = np.nan
    if arr.dtype == types.float32:
        zibyu__yyhkl = np.float32('nan')

    def impl(arr):
        for sulr__elc in range(len(arr)):
            if not bodo.libs.array_kernels.isna(arr, sulr__elc):
                return arr[sulr__elc]
        return zibyu__yyhkl
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_last_non_na(arr):
    if isinstance(arr.dtype, (types.Integer, types.Boolean)):
        zero = arr.dtype(0)
        return lambda arr: zero if len(arr) == 0 else arr[-1]
    assert isinstance(arr.dtype, types.Float)
    zibyu__yyhkl = np.nan
    if arr.dtype == types.float32:
        zibyu__yyhkl = np.float32('nan')

    def impl(arr):
        ckre__hhbyy = len(arr)
        for sulr__elc in range(len(arr)):
            bdgnl__mkuu = ckre__hhbyy - sulr__elc - 1
            if not bodo.libs.array_kernels.isna(arr, bdgnl__mkuu):
                return arr[bdgnl__mkuu]
        return zibyu__yyhkl
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_one_from_arr_dtype(arr):
    one = arr.dtype(1)
    return lambda arr: one


@register_jitable(cache=True)
def pct_change_seq(in_arr, shift):
    N = len(in_arr)
    output = alloc_pct_change(N, in_arr)
    deh__hccbu = 1 if shift > 0 else -1
    shift = deh__hccbu * min(abs(shift), N)
    if shift > 0:
        bodo.libs.array_kernels.setna_slice(output, slice(None, shift))
    else:
        bodo.libs.array_kernels.setna_slice(output, slice(shift, None))
    if shift > 0:
        ldlb__xwl = get_first_non_na(in_arr[:shift])
        zbtrg__mabkm = get_last_non_na(in_arr[:shift])
    else:
        ldlb__xwl = get_last_non_na(in_arr[:-shift])
        zbtrg__mabkm = get_first_non_na(in_arr[:-shift])
    one = get_one_from_arr_dtype(output)
    start = max(shift, 0)
    end = min(N, N + shift)
    for sulr__elc in range(start, end):
        nsp__mzd = in_arr[sulr__elc - shift]
        if np.isnan(nsp__mzd):
            nsp__mzd = ldlb__xwl
        else:
            ldlb__xwl = nsp__mzd
        val = in_arr[sulr__elc]
        if np.isnan(val):
            val = zbtrg__mabkm
        else:
            zbtrg__mabkm = val
        output[sulr__elc] = val / nsp__mzd - one
    return output


@register_jitable(cache=True)
def _border_icomm(in_arr, rank, n_pes, halo_size, send_right=True,
    send_left=False):
    zemp__uwb = np.int32(comm_border_tag)
    l_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr, (-1,))
    r_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr, (-1,))
    if send_right and rank != n_pes - 1:
        r_send_req = bodo.libs.distributed_api.isend(in_arr[-halo_size:],
            halo_size, np.int32(rank + 1), zemp__uwb, True)
    if send_right and rank != 0:
        l_recv_req = bodo.libs.distributed_api.irecv(l_recv_buff, halo_size,
            np.int32(rank - 1), zemp__uwb, True)
    if send_left and rank != 0:
        l_send_req = bodo.libs.distributed_api.isend(in_arr[:halo_size],
            halo_size, np.int32(rank - 1), zemp__uwb, True)
    if send_left and rank != n_pes - 1:
        kdm__qtvvk = bodo.libs.distributed_api.irecv(r_recv_buff, halo_size,
            np.int32(rank + 1), zemp__uwb, True)
    return (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
        kdm__qtvvk)


@register_jitable(cache=True)
def _border_icomm_var(in_arr, on_arr, rank, n_pes, win_size):
    zemp__uwb = np.int32(comm_border_tag)
    N = len(on_arr)
    halo_size = N
    end = on_arr[-1]
    for sska__rqt in range(-2, -N, -1):
        avmu__flk = on_arr[sska__rqt]
        if end - avmu__flk >= win_size:
            halo_size = -sska__rqt
            break
    if rank != n_pes - 1:
        bodo.libs.distributed_api.send(halo_size, np.int32(rank + 1), zemp__uwb
            )
        r_send_req = bodo.libs.distributed_api.isend(in_arr[-halo_size:],
            np.int32(halo_size), np.int32(rank + 1), zemp__uwb, True)
        yjw__wjnu = bodo.libs.distributed_api.isend(on_arr[-halo_size:], np
            .int32(halo_size), np.int32(rank + 1), zemp__uwb, True)
    if rank != 0:
        halo_size = bodo.libs.distributed_api.recv(np.int64, np.int32(rank -
            1), zemp__uwb)
        l_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr)
        l_recv_req = bodo.libs.distributed_api.irecv(l_recv_buff, np.int32(
            halo_size), np.int32(rank - 1), zemp__uwb, True)
        l_recv_t_buff = np.empty(halo_size, np.int64)
        kkd__jbwc = bodo.libs.distributed_api.irecv(l_recv_t_buff, np.int32
            (halo_size), np.int32(rank - 1), zemp__uwb, True)
    return (l_recv_buff, l_recv_t_buff, r_send_req, yjw__wjnu, l_recv_req,
        kkd__jbwc)


@register_jitable
def _border_send_wait(r_send_req, l_send_req, rank, n_pes, right, left):
    if right and rank != n_pes - 1:
        bodo.libs.distributed_api.wait(r_send_req, True)
    if left and rank != 0:
        bodo.libs.distributed_api.wait(l_send_req, True)


@register_jitable
def _is_small_for_parallel(N, halo_size):
    ellyj__kmgl = bodo.libs.distributed_api.dist_reduce(int(N <= 2 *
        halo_size + 1), np.int32(Reduce_Type.Sum.value))
    return ellyj__kmgl != 0


@register_jitable
def _handle_small_data(in_arr, win, minp, center, rank, n_pes, init_data,
    add_obs, remove_obs, calc_out):
    N = len(in_arr)
    xtb__dybod = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.
        int32(Reduce_Type.Sum.value))
    umyqe__gfc = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        hiab__ocrbl, kwzy__asna = roll_fixed_linear_generic_seq(umyqe__gfc,
            win, minp, center, init_data, add_obs, remove_obs, calc_out)
    else:
        hiab__ocrbl = np.empty(xtb__dybod, np.float64)
    bodo.libs.distributed_api.bcast(hiab__ocrbl)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return hiab__ocrbl[start:end]


@register_jitable
def _handle_small_data_apply(in_arr, index_arr, win, minp, center, rank,
    n_pes, kernel_func, raw=True):
    N = len(in_arr)
    xtb__dybod = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.
        int32(Reduce_Type.Sum.value))
    umyqe__gfc = bodo.libs.distributed_api.gatherv(in_arr)
    avujy__vyym = bodo.libs.distributed_api.gatherv(index_arr)
    if rank == 0:
        hiab__ocrbl = roll_fixed_apply_seq(umyqe__gfc, avujy__vyym, win,
            minp, center, kernel_func, raw)
    else:
        hiab__ocrbl = np.empty(xtb__dybod, np.float64)
    bodo.libs.distributed_api.bcast(hiab__ocrbl)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return hiab__ocrbl[start:end]


def bcast_n_chars_if_str_binary_arr(arr):
    pass


@overload(bcast_n_chars_if_str_binary_arr)
def overload_bcast_n_chars_if_str_binary_arr(arr):
    if arr in [bodo.binary_array_type, bodo.string_array_type]:

        def impl(arr):
            return bodo.libs.distributed_api.bcast_scalar(np.int64(bodo.
                libs.str_arr_ext.num_total_chars(arr)))
        return impl
    return lambda arr: -1


@register_jitable
def _handle_small_data_shift(in_arr, shift, rank, n_pes):
    N = len(in_arr)
    xtb__dybod = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.
        int32(Reduce_Type.Sum.value))
    umyqe__gfc = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        hiab__ocrbl = alloc_shift(len(umyqe__gfc), umyqe__gfc, (-1,))
        shift_seq(umyqe__gfc, shift, hiab__ocrbl)
        rrew__cspz = bcast_n_chars_if_str_binary_arr(hiab__ocrbl)
    else:
        rrew__cspz = bcast_n_chars_if_str_binary_arr(in_arr)
        hiab__ocrbl = alloc_shift(xtb__dybod, in_arr, (rrew__cspz,))
    bodo.libs.distributed_api.bcast(hiab__ocrbl)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return hiab__ocrbl[start:end]


@register_jitable
def _handle_small_data_pct_change(in_arr, shift, rank, n_pes):
    N = len(in_arr)
    xtb__dybod = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    umyqe__gfc = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        hiab__ocrbl = pct_change_seq(umyqe__gfc, shift)
    else:
        hiab__ocrbl = alloc_pct_change(xtb__dybod, in_arr)
    bodo.libs.distributed_api.bcast(hiab__ocrbl)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return hiab__ocrbl[start:end]


def cast_dt64_arr_to_int(arr):
    return arr


@infer_global(cast_dt64_arr_to_int)
class DtArrToIntType(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        assert args[0] == types.Array(types.NPDatetime('ns'), 1, 'C') or args[0
            ] == types.Array(types.int64, 1, 'C')
        return signature(types.Array(types.int64, 1, 'C'), *args)


@lower_builtin(cast_dt64_arr_to_int, types.Array(types.NPDatetime('ns'), 1,
    'C'))
@lower_builtin(cast_dt64_arr_to_int, types.Array(types.int64, 1, 'C'))
def lower_cast_dt64_arr_to_int(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@register_jitable
def _is_small_for_parallel_variable(on_arr, win_size):
    if len(on_arr) < 2:
        vpdkl__sbdz = 1
    else:
        start = on_arr[0]
        end = on_arr[-1]
        qxj__nmtxd = end - start
        vpdkl__sbdz = int(qxj__nmtxd <= win_size)
    ellyj__kmgl = bodo.libs.distributed_api.dist_reduce(vpdkl__sbdz, np.
        int32(Reduce_Type.Sum.value))
    return ellyj__kmgl != 0


@register_jitable
def _handle_small_data_variable(in_arr, on_arr, win, minp, rank, n_pes,
    init_data, add_obs, remove_obs, calc_out):
    N = len(in_arr)
    xtb__dybod = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    umyqe__gfc = bodo.libs.distributed_api.gatherv(in_arr)
    smn__vylbc = bodo.libs.distributed_api.gatherv(on_arr)
    if rank == 0:
        start, end = _build_indexer(smn__vylbc, xtb__dybod, win, False, True)
        hiab__ocrbl = roll_var_linear_generic_seq(umyqe__gfc, smn__vylbc,
            win, minp, start, end, init_data, add_obs, remove_obs, calc_out)
    else:
        hiab__ocrbl = np.empty(xtb__dybod, np.float64)
    bodo.libs.distributed_api.bcast(hiab__ocrbl)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return hiab__ocrbl[start:end]


@register_jitable
def _handle_small_data_variable_apply(in_arr, on_arr, index_arr, win, minp,
    rank, n_pes, kernel_func, raw):
    N = len(in_arr)
    xtb__dybod = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    umyqe__gfc = bodo.libs.distributed_api.gatherv(in_arr)
    smn__vylbc = bodo.libs.distributed_api.gatherv(on_arr)
    avujy__vyym = bodo.libs.distributed_api.gatherv(index_arr)
    if rank == 0:
        start, end = _build_indexer(smn__vylbc, xtb__dybod, win, False, True)
        hiab__ocrbl = roll_variable_apply_seq(umyqe__gfc, smn__vylbc,
            avujy__vyym, win, minp, start, end, kernel_func, raw)
    else:
        hiab__ocrbl = np.empty(xtb__dybod, np.float64)
    bodo.libs.distributed_api.bcast(hiab__ocrbl)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return hiab__ocrbl[start:end]


@register_jitable(cache=True)
def _dropna(arr):
    slyuo__elqk = len(arr)
    vsj__jxbrw = slyuo__elqk - np.isnan(arr).sum()
    A = np.empty(vsj__jxbrw, arr.dtype)
    atzx__fnqkp = 0
    for sulr__elc in range(slyuo__elqk):
        val = arr[sulr__elc]
        if not np.isnan(val):
            A[atzx__fnqkp] = val
            atzx__fnqkp += 1
    return A


def alloc_shift(n, A, s=None):
    return np.empty(n, A.dtype)


@overload(alloc_shift, no_unliteral=True)
def alloc_shift_overload(n, A, s=None):
    if not isinstance(A, types.Array):
        return lambda n, A, s=None: bodo.utils.utils.alloc_type(n, A, s)
    if isinstance(A.dtype, types.Integer):
        return lambda n, A, s=None: np.empty(n, np.float64)
    return lambda n, A, s=None: np.empty(n, A.dtype)


def alloc_pct_change(n, A):
    return np.empty(n, A.dtype)


@overload(alloc_pct_change, no_unliteral=True)
def alloc_pct_change_overload(n, A):
    if isinstance(A.dtype, types.Integer):
        return lambda n, A: np.empty(n, np.float64)
    return lambda n, A: np.empty(n, A.dtype)


def prep_values(A):
    return A.astype('float64')


@overload(prep_values, no_unliteral=True)
def prep_values_overload(A):
    if A == types.Array(types.float64, 1, 'C'):
        return lambda A: A
    return lambda A: A.astype(np.float64)


@register_jitable
def _validate_roll_fixed_args(win, minp):
    if win < 0:
        raise ValueError('window must be non-negative')
    if minp < 0:
        raise ValueError('min_periods must be >= 0')
    if minp > win:
        raise ValueError('min_periods must be <= window')


@register_jitable
def _validate_roll_var_args(minp, center):
    if minp < 0:
        raise ValueError('min_periods must be >= 0')
    if center:
        raise NotImplementedError(
            'rolling: center is not implemented for datetimelike and offset based windows'
            )
