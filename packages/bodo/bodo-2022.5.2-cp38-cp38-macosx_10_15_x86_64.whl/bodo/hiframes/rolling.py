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
        rfky__ncr = arr.copy(dtype=types.float64)
        return signature(rfky__ncr, *unliteral_all(args))


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
    ukf__omdwz = get_overload_const_str(fname)
    if ukf__omdwz not in ('sum', 'mean', 'var', 'std', 'count', 'median',
        'min', 'max'):
        raise BodoError('invalid rolling (fixed window) function {}'.format
            (ukf__omdwz))
    if ukf__omdwz in ('median', 'min', 'max'):
        wlcqe__mitg = 'def kernel_func(A):\n'
        wlcqe__mitg += '  if np.isnan(A).sum() != 0: return np.nan\n'
        wlcqe__mitg += '  return np.{}(A)\n'.format(ukf__omdwz)
        wvwjb__mwjc = {}
        exec(wlcqe__mitg, {'np': np}, wvwjb__mwjc)
        kernel_func = register_jitable(wvwjb__mwjc['kernel_func'])
        return (lambda arr, index_arr, win, minp, center, fname, raw=True,
            parallel=False: roll_fixed_apply(arr, index_arr, win, minp,
            center, parallel, kernel_func))
    init_kernel, add_kernel, remove_kernel, calc_kernel = linear_kernels[
        ukf__omdwz]
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
    ukf__omdwz = get_overload_const_str(fname)
    if ukf__omdwz not in ('sum', 'mean', 'var', 'std', 'count', 'median',
        'min', 'max'):
        raise BodoError('invalid rolling (variable window) function {}'.
            format(ukf__omdwz))
    if ukf__omdwz in ('median', 'min', 'max'):
        wlcqe__mitg = 'def kernel_func(A):\n'
        wlcqe__mitg += '  arr  = dropna(A)\n'
        wlcqe__mitg += '  if len(arr) == 0: return np.nan\n'
        wlcqe__mitg += '  return np.{}(arr)\n'.format(ukf__omdwz)
        wvwjb__mwjc = {}
        exec(wlcqe__mitg, {'np': np, 'dropna': _dropna}, wvwjb__mwjc)
        kernel_func = register_jitable(wvwjb__mwjc['kernel_func'])
        return (lambda arr, on_arr, index_arr, win, minp, center, fname,
            raw=True, parallel=False: roll_variable_apply(arr, on_arr,
            index_arr, win, minp, center, parallel, kernel_func))
    init_kernel, add_kernel, remove_kernel, calc_kernel = linear_kernels[
        ukf__omdwz]
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
        dqiqz__avv = _border_icomm(in_arr, rank, n_pes, halo_size, True, center
            )
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            wrqz__pjww) = dqiqz__avv
    output, data = roll_fixed_linear_generic_seq(in_arr, win, minp, center,
        init_data, add_obs, remove_obs, calc_out)
    if parallel:
        _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, center)
        if center and rank != n_pes - 1:
            bodo.libs.distributed_api.wait(wrqz__pjww, True)
            for iqr__yjdkz in range(0, halo_size):
                data = add_obs(r_recv_buff[iqr__yjdkz], *data)
                vwtyo__aue = in_arr[N + iqr__yjdkz - win]
                data = remove_obs(vwtyo__aue, *data)
                output[N + iqr__yjdkz - offset] = calc_out(minp, *data)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            data = init_data()
            for iqr__yjdkz in range(0, halo_size):
                data = add_obs(l_recv_buff[iqr__yjdkz], *data)
            for iqr__yjdkz in range(0, win - 1):
                data = add_obs(in_arr[iqr__yjdkz], *data)
                if iqr__yjdkz > offset:
                    vwtyo__aue = l_recv_buff[iqr__yjdkz - offset - 1]
                    data = remove_obs(vwtyo__aue, *data)
                if iqr__yjdkz >= offset:
                    output[iqr__yjdkz - offset] = calc_out(minp, *data)
    return output


@register_jitable
def roll_fixed_linear_generic_seq(in_arr, win, minp, center, init_data,
    add_obs, remove_obs, calc_out):
    data = init_data()
    N = len(in_arr)
    offset = (win - 1) // 2 if center else 0
    output = np.empty(N, dtype=np.float64)
    jjrh__fmv = max(minp, 1) - 1
    jjrh__fmv = min(jjrh__fmv, N)
    for iqr__yjdkz in range(0, jjrh__fmv):
        data = add_obs(in_arr[iqr__yjdkz], *data)
        if iqr__yjdkz >= offset:
            output[iqr__yjdkz - offset] = calc_out(minp, *data)
    for iqr__yjdkz in range(jjrh__fmv, N):
        val = in_arr[iqr__yjdkz]
        data = add_obs(val, *data)
        if iqr__yjdkz > win - 1:
            vwtyo__aue = in_arr[iqr__yjdkz - win]
            data = remove_obs(vwtyo__aue, *data)
        output[iqr__yjdkz - offset] = calc_out(minp, *data)
    zhhya__cdx = data
    for iqr__yjdkz in range(N, N + offset):
        if iqr__yjdkz > win - 1:
            vwtyo__aue = in_arr[iqr__yjdkz - win]
            data = remove_obs(vwtyo__aue, *data)
        output[iqr__yjdkz - offset] = calc_out(minp, *data)
    return output, zhhya__cdx


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
        dqiqz__avv = _border_icomm(in_arr, rank, n_pes, halo_size, True, center
            )
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            wrqz__pjww) = dqiqz__avv
        if raw == False:
            yqmcp__rpam = _border_icomm(index_arr, rank, n_pes, halo_size, 
                True, center)
            (l_recv_buff_idx, r_recv_buff_idx, egyw__esv, udx__vtvip,
                uvz__gqaq, amtfb__xtqu) = yqmcp__rpam
    output = roll_fixed_apply_seq(in_arr, index_arr, win, minp, center,
        kernel_func, raw)
    if parallel:
        _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, center)
        if raw == False:
            _border_send_wait(udx__vtvip, egyw__esv, rank, n_pes, True, center)
        if center and rank != n_pes - 1:
            bodo.libs.distributed_api.wait(wrqz__pjww, True)
            if raw == False:
                bodo.libs.distributed_api.wait(amtfb__xtqu, True)
            recv_right_compute(output, in_arr, index_arr, N, win, minp,
                offset, r_recv_buff, r_recv_buff_idx, kernel_func, raw)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            if raw == False:
                bodo.libs.distributed_api.wait(uvz__gqaq, True)
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
            zhhya__cdx = np.concatenate((in_arr[N - win + 1:], r_recv_buff))
            eytzx__eazv = 0
            for iqr__yjdkz in range(max(N - offset, 0), N):
                data = zhhya__cdx[eytzx__eazv:eytzx__eazv + win]
                if win - np.isnan(data).sum() < minp:
                    output[iqr__yjdkz] = np.nan
                else:
                    output[iqr__yjdkz] = kernel_func(data)
                eytzx__eazv += 1
        return impl

    def impl_series(output, in_arr, index_arr, N, win, minp, offset,
        r_recv_buff, r_recv_buff_idx, kernel_func, raw):
        zhhya__cdx = np.concatenate((in_arr[N - win + 1:], r_recv_buff))
        pkz__vxerg = np.concatenate((index_arr[N - win + 1:], r_recv_buff_idx))
        eytzx__eazv = 0
        for iqr__yjdkz in range(max(N - offset, 0), N):
            data = zhhya__cdx[eytzx__eazv:eytzx__eazv + win]
            if win - np.isnan(data).sum() < minp:
                output[iqr__yjdkz] = np.nan
            else:
                output[iqr__yjdkz] = kernel_func(pd.Series(data, pkz__vxerg
                    [eytzx__eazv:eytzx__eazv + win]))
            eytzx__eazv += 1
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
            zhhya__cdx = np.concatenate((l_recv_buff, in_arr[:win - 1]))
            for iqr__yjdkz in range(0, win - offset - 1):
                data = zhhya__cdx[iqr__yjdkz:iqr__yjdkz + win]
                if win - np.isnan(data).sum() < minp:
                    output[iqr__yjdkz] = np.nan
                else:
                    output[iqr__yjdkz] = kernel_func(data)
        return impl

    def impl_series(output, in_arr, index_arr, win, minp, offset,
        l_recv_buff, l_recv_buff_idx, kernel_func, raw):
        zhhya__cdx = np.concatenate((l_recv_buff, in_arr[:win - 1]))
        pkz__vxerg = np.concatenate((l_recv_buff_idx, index_arr[:win - 1]))
        for iqr__yjdkz in range(0, win - offset - 1):
            data = zhhya__cdx[iqr__yjdkz:iqr__yjdkz + win]
            if win - np.isnan(data).sum() < minp:
                output[iqr__yjdkz] = np.nan
            else:
                output[iqr__yjdkz] = kernel_func(pd.Series(data, pkz__vxerg
                    [iqr__yjdkz:iqr__yjdkz + win]))
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
        for iqr__yjdkz in range(0, N):
            start = max(iqr__yjdkz - win + 1 + offset, 0)
            end = min(iqr__yjdkz + 1 + offset, N)
            data = in_arr[start:end]
            if end - start - np.isnan(data).sum() < minp:
                output[iqr__yjdkz] = np.nan
            else:
                output[iqr__yjdkz] = apply_func(kernel_func, data,
                    index_arr, start, end, raw)
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
        dqiqz__avv = _border_icomm_var(in_arr, on_arr, rank, n_pes, win)
        (l_recv_buff, l_recv_t_buff, r_send_req, pqdl__wsczu, l_recv_req,
            ggfx__bxmpt) = dqiqz__avv
    start, end = _build_indexer(on_arr, N, win, left_closed, right_closed)
    output = roll_var_linear_generic_seq(in_arr, on_arr, win, minp, start,
        end, init_data, add_obs, remove_obs, calc_out)
    if parallel:
        _border_send_wait(r_send_req, r_send_req, rank, n_pes, True, False)
        _border_send_wait(pqdl__wsczu, pqdl__wsczu, rank, n_pes, True, False)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            bodo.libs.distributed_api.wait(ggfx__bxmpt, True)
            num_zero_starts = 0
            for iqr__yjdkz in range(0, N):
                if start[iqr__yjdkz] != 0:
                    break
                num_zero_starts += 1
            if num_zero_starts == 0:
                return output
            recv_starts = _get_var_recv_starts(on_arr, l_recv_t_buff,
                num_zero_starts, win)
            data = init_data()
            for obtj__bbu in range(recv_starts[0], len(l_recv_t_buff)):
                data = add_obs(l_recv_buff[obtj__bbu], *data)
            if right_closed:
                data = add_obs(in_arr[0], *data)
            output[0] = calc_out(minp, *data)
            for iqr__yjdkz in range(1, num_zero_starts):
                s = recv_starts[iqr__yjdkz]
                jou__hxzcy = end[iqr__yjdkz]
                for obtj__bbu in range(recv_starts[iqr__yjdkz - 1], s):
                    data = remove_obs(l_recv_buff[obtj__bbu], *data)
                for obtj__bbu in range(end[iqr__yjdkz - 1], jou__hxzcy):
                    data = add_obs(in_arr[obtj__bbu], *data)
                output[iqr__yjdkz] = calc_out(minp, *data)
    return output


@register_jitable(cache=True)
def _get_var_recv_starts(on_arr, l_recv_t_buff, num_zero_starts, win):
    recv_starts = np.zeros(num_zero_starts, np.int64)
    halo_size = len(l_recv_t_buff)
    ffgto__aek = cast_dt64_arr_to_int(on_arr)
    left_closed = False
    vdvy__ikwkw = ffgto__aek[0] - win
    if left_closed:
        vdvy__ikwkw -= 1
    recv_starts[0] = halo_size
    for obtj__bbu in range(0, halo_size):
        if l_recv_t_buff[obtj__bbu] > vdvy__ikwkw:
            recv_starts[0] = obtj__bbu
            break
    for iqr__yjdkz in range(1, num_zero_starts):
        vdvy__ikwkw = ffgto__aek[iqr__yjdkz] - win
        if left_closed:
            vdvy__ikwkw -= 1
        recv_starts[iqr__yjdkz] = halo_size
        for obtj__bbu in range(recv_starts[iqr__yjdkz - 1], halo_size):
            if l_recv_t_buff[obtj__bbu] > vdvy__ikwkw:
                recv_starts[iqr__yjdkz] = obtj__bbu
                break
    return recv_starts


@register_jitable
def roll_var_linear_generic_seq(in_arr, on_arr, win, minp, start, end,
    init_data, add_obs, remove_obs, calc_out):
    N = len(in_arr)
    output = np.empty(N, np.float64)
    data = init_data()
    for obtj__bbu in range(start[0], end[0]):
        data = add_obs(in_arr[obtj__bbu], *data)
    output[0] = calc_out(minp, *data)
    for iqr__yjdkz in range(1, N):
        s = start[iqr__yjdkz]
        jou__hxzcy = end[iqr__yjdkz]
        for obtj__bbu in range(start[iqr__yjdkz - 1], s):
            data = remove_obs(in_arr[obtj__bbu], *data)
        for obtj__bbu in range(end[iqr__yjdkz - 1], jou__hxzcy):
            data = add_obs(in_arr[obtj__bbu], *data)
        output[iqr__yjdkz] = calc_out(minp, *data)
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
        dqiqz__avv = _border_icomm_var(in_arr, on_arr, rank, n_pes, win)
        (l_recv_buff, l_recv_t_buff, r_send_req, pqdl__wsczu, l_recv_req,
            ggfx__bxmpt) = dqiqz__avv
        if raw == False:
            yqmcp__rpam = _border_icomm_var(index_arr, on_arr, rank, n_pes, win
                )
            (l_recv_buff_idx, hyvdv__gmwxn, udx__vtvip, umk__cvwne,
                uvz__gqaq, njnks__ifmwp) = yqmcp__rpam
    start, end = _build_indexer(on_arr, N, win, left_closed, right_closed)
    output = roll_variable_apply_seq(in_arr, on_arr, index_arr, win, minp,
        start, end, kernel_func, raw)
    if parallel:
        _border_send_wait(r_send_req, r_send_req, rank, n_pes, True, False)
        _border_send_wait(pqdl__wsczu, pqdl__wsczu, rank, n_pes, True, False)
        if raw == False:
            _border_send_wait(udx__vtvip, udx__vtvip, rank, n_pes, True, False)
            _border_send_wait(umk__cvwne, umk__cvwne, rank, n_pes, True, False)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            bodo.libs.distributed_api.wait(ggfx__bxmpt, True)
            if raw == False:
                bodo.libs.distributed_api.wait(uvz__gqaq, True)
                bodo.libs.distributed_api.wait(njnks__ifmwp, True)
            num_zero_starts = 0
            for iqr__yjdkz in range(0, N):
                if start[iqr__yjdkz] != 0:
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
            for iqr__yjdkz in range(0, num_zero_starts):
                txxw__pijca = recv_starts[iqr__yjdkz]
                yte__xuicy = np.concatenate((l_recv_buff[txxw__pijca:],
                    in_arr[:iqr__yjdkz + 1]))
                if len(yte__xuicy) - np.isnan(yte__xuicy).sum() >= minp:
                    output[iqr__yjdkz] = kernel_func(yte__xuicy)
                else:
                    output[iqr__yjdkz] = np.nan
        return impl

    def impl_series(output, in_arr, index_arr, num_zero_starts, recv_starts,
        l_recv_buff, l_recv_buff_idx, minp, kernel_func, raw):
        for iqr__yjdkz in range(0, num_zero_starts):
            txxw__pijca = recv_starts[iqr__yjdkz]
            yte__xuicy = np.concatenate((l_recv_buff[txxw__pijca:], in_arr[
                :iqr__yjdkz + 1]))
            majm__lih = np.concatenate((l_recv_buff_idx[txxw__pijca:],
                index_arr[:iqr__yjdkz + 1]))
            if len(yte__xuicy) - np.isnan(yte__xuicy).sum() >= minp:
                output[iqr__yjdkz] = kernel_func(pd.Series(yte__xuicy,
                    majm__lih))
            else:
                output[iqr__yjdkz] = np.nan
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
    for iqr__yjdkz in range(0, N):
        s = start[iqr__yjdkz]
        jou__hxzcy = end[iqr__yjdkz]
        data = in_arr[s:jou__hxzcy]
        if jou__hxzcy - s - np.isnan(data).sum() >= minp:
            output[iqr__yjdkz] = kernel_func(data)
        else:
            output[iqr__yjdkz] = np.nan
    return output


def roll_variable_apply_seq_impl_series(in_arr, on_arr, index_arr, win,
    minp, start, end, kernel_func, raw):
    N = len(in_arr)
    output = np.empty(N, dtype=np.float64)
    for iqr__yjdkz in range(0, N):
        s = start[iqr__yjdkz]
        jou__hxzcy = end[iqr__yjdkz]
        data = in_arr[s:jou__hxzcy]
        if jou__hxzcy - s - np.isnan(data).sum() >= minp:
            output[iqr__yjdkz] = kernel_func(pd.Series(data, index_arr[s:
                jou__hxzcy]))
        else:
            output[iqr__yjdkz] = np.nan
    return output


@register_jitable(cache=True)
def _build_indexer(on_arr, N, win, left_closed, right_closed):
    ffgto__aek = cast_dt64_arr_to_int(on_arr)
    start = np.empty(N, np.int64)
    end = np.empty(N, np.int64)
    start[0] = 0
    if right_closed:
        end[0] = 1
    else:
        end[0] = 0
    for iqr__yjdkz in range(1, N):
        ehib__zlq = ffgto__aek[iqr__yjdkz]
        vdvy__ikwkw = ffgto__aek[iqr__yjdkz] - win
        if left_closed:
            vdvy__ikwkw -= 1
        start[iqr__yjdkz] = iqr__yjdkz
        for obtj__bbu in range(start[iqr__yjdkz - 1], iqr__yjdkz):
            if ffgto__aek[obtj__bbu] > vdvy__ikwkw:
                start[iqr__yjdkz] = obtj__bbu
                break
        if ffgto__aek[end[iqr__yjdkz - 1]] <= ehib__zlq:
            end[iqr__yjdkz] = iqr__yjdkz + 1
        else:
            end[iqr__yjdkz] = end[iqr__yjdkz - 1]
        if not right_closed:
            end[iqr__yjdkz] -= 1
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
        eklmj__ewblr = sum_x / nobs
        if neg_ct == 0 and eklmj__ewblr < 0.0:
            eklmj__ewblr = 0
        elif neg_ct == nobs and eklmj__ewblr > 0.0:
            eklmj__ewblr = 0
    else:
        eklmj__ewblr = np.nan
    return eklmj__ewblr


@register_jitable
def init_data_var():
    return 0, 0.0, 0.0


@register_jitable
def add_var(val, nobs, mean_x, ssqdm_x):
    if not np.isnan(val):
        nobs += 1
        thlkp__tvbrb = val - mean_x
        mean_x += thlkp__tvbrb / nobs
        ssqdm_x += (nobs - 1) * thlkp__tvbrb ** 2 / nobs
    return nobs, mean_x, ssqdm_x


@register_jitable
def remove_var(val, nobs, mean_x, ssqdm_x):
    if not np.isnan(val):
        nobs -= 1
        if nobs != 0:
            thlkp__tvbrb = val - mean_x
            mean_x -= thlkp__tvbrb / nobs
            ssqdm_x -= (nobs + 1) * thlkp__tvbrb ** 2 / nobs
        else:
            mean_x = 0.0
            ssqdm_x = 0.0
    return nobs, mean_x, ssqdm_x


@register_jitable
def calc_var(minp, nobs, mean_x, ssqdm_x):
    leifc__tjx = 1.0
    eklmj__ewblr = np.nan
    if nobs >= minp and nobs > leifc__tjx:
        if nobs == 1:
            eklmj__ewblr = 0.0
        else:
            eklmj__ewblr = ssqdm_x / (nobs - leifc__tjx)
            if eklmj__ewblr < 0.0:
                eklmj__ewblr = 0.0
    return eklmj__ewblr


@register_jitable
def calc_std(minp, nobs, mean_x, ssqdm_x):
    wdeqb__rtna = calc_var(minp, nobs, mean_x, ssqdm_x)
    return np.sqrt(wdeqb__rtna)


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
        dqiqz__avv = _border_icomm(in_arr, rank, n_pes, halo_size,
            send_right, send_left)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            wrqz__pjww) = dqiqz__avv
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
                bodo.libs.distributed_api.wait(wrqz__pjww, True)
                for iqr__yjdkz in range(0, halo_size):
                    if bodo.libs.array_kernels.isna(r_recv_buff, iqr__yjdkz):
                        bodo.libs.array_kernels.setna(output, N - halo_size +
                            iqr__yjdkz)
                        continue
                    output[N - halo_size + iqr__yjdkz] = r_recv_buff[iqr__yjdkz
                        ]
    return output


@register_jitable(cache=True)
def shift_seq(in_arr, shift, output, is_parallel_str=False):
    N = len(in_arr)
    drqyo__tkzd = 1 if shift > 0 else -1
    shift = drqyo__tkzd * min(abs(shift), N)
    if shift > 0 and (not is_parallel_str or bodo.get_rank() == 0):
        bodo.libs.array_kernels.setna_slice(output, slice(None, shift))
    start = max(shift, 0)
    end = min(N, N + shift)
    for iqr__yjdkz in range(start, end):
        if bodo.libs.array_kernels.isna(in_arr, iqr__yjdkz - shift):
            bodo.libs.array_kernels.setna(output, iqr__yjdkz)
            continue
        output[iqr__yjdkz] = in_arr[iqr__yjdkz - shift]
    if shift < 0:
        bodo.libs.array_kernels.setna_slice(output, slice(shift, None))
    return output


@register_jitable
def shift_left_recv(r_send_req, l_send_req, rank, n_pes, halo_size,
    l_recv_req, l_recv_buff, output):
    _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, False)
    if rank != 0:
        bodo.libs.distributed_api.wait(l_recv_req, True)
        for iqr__yjdkz in range(0, halo_size):
            if bodo.libs.array_kernels.isna(l_recv_buff, iqr__yjdkz):
                bodo.libs.array_kernels.setna(output, iqr__yjdkz)
                continue
            output[iqr__yjdkz] = l_recv_buff[iqr__yjdkz]


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
        dqiqz__avv = _border_icomm(in_arr, rank, n_pes, halo_size,
            send_right, send_left)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            wrqz__pjww) = dqiqz__avv
    output = pct_change_seq(in_arr, shift)
    if parallel:
        if send_right:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, False)
            if rank != 0:
                bodo.libs.distributed_api.wait(l_recv_req, True)
                for iqr__yjdkz in range(0, halo_size):
                    myxt__tun = l_recv_buff[iqr__yjdkz]
                    output[iqr__yjdkz] = (in_arr[iqr__yjdkz] - myxt__tun
                        ) / myxt__tun
        else:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, False, True)
            if rank != n_pes - 1:
                bodo.libs.distributed_api.wait(wrqz__pjww, True)
                for iqr__yjdkz in range(0, halo_size):
                    myxt__tun = r_recv_buff[iqr__yjdkz]
                    output[N - halo_size + iqr__yjdkz] = (in_arr[N -
                        halo_size + iqr__yjdkz] - myxt__tun) / myxt__tun
    return output


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_first_non_na(arr):
    if isinstance(arr.dtype, (types.Integer, types.Boolean)):
        zero = arr.dtype(0)
        return lambda arr: zero if len(arr) == 0 else arr[0]
    assert isinstance(arr.dtype, types.Float)
    jhya__dghjq = np.nan
    if arr.dtype == types.float32:
        jhya__dghjq = np.float32('nan')

    def impl(arr):
        for iqr__yjdkz in range(len(arr)):
            if not bodo.libs.array_kernels.isna(arr, iqr__yjdkz):
                return arr[iqr__yjdkz]
        return jhya__dghjq
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_last_non_na(arr):
    if isinstance(arr.dtype, (types.Integer, types.Boolean)):
        zero = arr.dtype(0)
        return lambda arr: zero if len(arr) == 0 else arr[-1]
    assert isinstance(arr.dtype, types.Float)
    jhya__dghjq = np.nan
    if arr.dtype == types.float32:
        jhya__dghjq = np.float32('nan')

    def impl(arr):
        dfc__juarl = len(arr)
        for iqr__yjdkz in range(len(arr)):
            eytzx__eazv = dfc__juarl - iqr__yjdkz - 1
            if not bodo.libs.array_kernels.isna(arr, eytzx__eazv):
                return arr[eytzx__eazv]
        return jhya__dghjq
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_one_from_arr_dtype(arr):
    one = arr.dtype(1)
    return lambda arr: one


@register_jitable(cache=True)
def pct_change_seq(in_arr, shift):
    N = len(in_arr)
    output = alloc_pct_change(N, in_arr)
    drqyo__tkzd = 1 if shift > 0 else -1
    shift = drqyo__tkzd * min(abs(shift), N)
    if shift > 0:
        bodo.libs.array_kernels.setna_slice(output, slice(None, shift))
    else:
        bodo.libs.array_kernels.setna_slice(output, slice(shift, None))
    if shift > 0:
        qfdm__foky = get_first_non_na(in_arr[:shift])
        hhhf__xitm = get_last_non_na(in_arr[:shift])
    else:
        qfdm__foky = get_last_non_na(in_arr[:-shift])
        hhhf__xitm = get_first_non_na(in_arr[:-shift])
    one = get_one_from_arr_dtype(output)
    start = max(shift, 0)
    end = min(N, N + shift)
    for iqr__yjdkz in range(start, end):
        myxt__tun = in_arr[iqr__yjdkz - shift]
        if np.isnan(myxt__tun):
            myxt__tun = qfdm__foky
        else:
            qfdm__foky = myxt__tun
        val = in_arr[iqr__yjdkz]
        if np.isnan(val):
            val = hhhf__xitm
        else:
            hhhf__xitm = val
        output[iqr__yjdkz] = val / myxt__tun - one
    return output


@register_jitable(cache=True)
def _border_icomm(in_arr, rank, n_pes, halo_size, send_right=True,
    send_left=False):
    xlu__etw = np.int32(comm_border_tag)
    l_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr, (-1,))
    r_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr, (-1,))
    if send_right and rank != n_pes - 1:
        r_send_req = bodo.libs.distributed_api.isend(in_arr[-halo_size:],
            halo_size, np.int32(rank + 1), xlu__etw, True)
    if send_right and rank != 0:
        l_recv_req = bodo.libs.distributed_api.irecv(l_recv_buff, halo_size,
            np.int32(rank - 1), xlu__etw, True)
    if send_left and rank != 0:
        l_send_req = bodo.libs.distributed_api.isend(in_arr[:halo_size],
            halo_size, np.int32(rank - 1), xlu__etw, True)
    if send_left and rank != n_pes - 1:
        wrqz__pjww = bodo.libs.distributed_api.irecv(r_recv_buff, halo_size,
            np.int32(rank + 1), xlu__etw, True)
    return (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
        wrqz__pjww)


@register_jitable(cache=True)
def _border_icomm_var(in_arr, on_arr, rank, n_pes, win_size):
    xlu__etw = np.int32(comm_border_tag)
    N = len(on_arr)
    halo_size = N
    end = on_arr[-1]
    for obtj__bbu in range(-2, -N, -1):
        zokz__csy = on_arr[obtj__bbu]
        if end - zokz__csy >= win_size:
            halo_size = -obtj__bbu
            break
    if rank != n_pes - 1:
        bodo.libs.distributed_api.send(halo_size, np.int32(rank + 1), xlu__etw)
        r_send_req = bodo.libs.distributed_api.isend(in_arr[-halo_size:],
            np.int32(halo_size), np.int32(rank + 1), xlu__etw, True)
        pqdl__wsczu = bodo.libs.distributed_api.isend(on_arr[-halo_size:],
            np.int32(halo_size), np.int32(rank + 1), xlu__etw, True)
    if rank != 0:
        halo_size = bodo.libs.distributed_api.recv(np.int64, np.int32(rank -
            1), xlu__etw)
        l_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr)
        l_recv_req = bodo.libs.distributed_api.irecv(l_recv_buff, np.int32(
            halo_size), np.int32(rank - 1), xlu__etw, True)
        l_recv_t_buff = np.empty(halo_size, np.int64)
        ggfx__bxmpt = bodo.libs.distributed_api.irecv(l_recv_t_buff, np.
            int32(halo_size), np.int32(rank - 1), xlu__etw, True)
    return (l_recv_buff, l_recv_t_buff, r_send_req, pqdl__wsczu, l_recv_req,
        ggfx__bxmpt)


@register_jitable
def _border_send_wait(r_send_req, l_send_req, rank, n_pes, right, left):
    if right and rank != n_pes - 1:
        bodo.libs.distributed_api.wait(r_send_req, True)
    if left and rank != 0:
        bodo.libs.distributed_api.wait(l_send_req, True)


@register_jitable
def _is_small_for_parallel(N, halo_size):
    fgfq__imre = bodo.libs.distributed_api.dist_reduce(int(N <= 2 *
        halo_size + 1), np.int32(Reduce_Type.Sum.value))
    return fgfq__imre != 0


@register_jitable
def _handle_small_data(in_arr, win, minp, center, rank, n_pes, init_data,
    add_obs, remove_obs, calc_out):
    N = len(in_arr)
    vepbi__ydyx = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.
        int32(Reduce_Type.Sum.value))
    yxm__klhyi = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        hhekb__eeu, yirbs__vvulp = roll_fixed_linear_generic_seq(yxm__klhyi,
            win, minp, center, init_data, add_obs, remove_obs, calc_out)
    else:
        hhekb__eeu = np.empty(vepbi__ydyx, np.float64)
    bodo.libs.distributed_api.bcast(hhekb__eeu)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return hhekb__eeu[start:end]


@register_jitable
def _handle_small_data_apply(in_arr, index_arr, win, minp, center, rank,
    n_pes, kernel_func, raw=True):
    N = len(in_arr)
    vepbi__ydyx = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.
        int32(Reduce_Type.Sum.value))
    yxm__klhyi = bodo.libs.distributed_api.gatherv(in_arr)
    gwnpc__dft = bodo.libs.distributed_api.gatherv(index_arr)
    if rank == 0:
        hhekb__eeu = roll_fixed_apply_seq(yxm__klhyi, gwnpc__dft, win, minp,
            center, kernel_func, raw)
    else:
        hhekb__eeu = np.empty(vepbi__ydyx, np.float64)
    bodo.libs.distributed_api.bcast(hhekb__eeu)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return hhekb__eeu[start:end]


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
    vepbi__ydyx = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.
        int32(Reduce_Type.Sum.value))
    yxm__klhyi = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        hhekb__eeu = alloc_shift(len(yxm__klhyi), yxm__klhyi, (-1,))
        shift_seq(yxm__klhyi, shift, hhekb__eeu)
        qosxq__eykqe = bcast_n_chars_if_str_binary_arr(hhekb__eeu)
    else:
        qosxq__eykqe = bcast_n_chars_if_str_binary_arr(in_arr)
        hhekb__eeu = alloc_shift(vepbi__ydyx, in_arr, (qosxq__eykqe,))
    bodo.libs.distributed_api.bcast(hhekb__eeu)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return hhekb__eeu[start:end]


@register_jitable
def _handle_small_data_pct_change(in_arr, shift, rank, n_pes):
    N = len(in_arr)
    vepbi__ydyx = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    yxm__klhyi = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        hhekb__eeu = pct_change_seq(yxm__klhyi, shift)
    else:
        hhekb__eeu = alloc_pct_change(vepbi__ydyx, in_arr)
    bodo.libs.distributed_api.bcast(hhekb__eeu)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return hhekb__eeu[start:end]


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
        ufytl__bqtwh = 1
    else:
        start = on_arr[0]
        end = on_arr[-1]
        imjp__ufvr = end - start
        ufytl__bqtwh = int(imjp__ufvr <= win_size)
    fgfq__imre = bodo.libs.distributed_api.dist_reduce(ufytl__bqtwh, np.
        int32(Reduce_Type.Sum.value))
    return fgfq__imre != 0


@register_jitable
def _handle_small_data_variable(in_arr, on_arr, win, minp, rank, n_pes,
    init_data, add_obs, remove_obs, calc_out):
    N = len(in_arr)
    vepbi__ydyx = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    yxm__klhyi = bodo.libs.distributed_api.gatherv(in_arr)
    dutt__xvath = bodo.libs.distributed_api.gatherv(on_arr)
    if rank == 0:
        start, end = _build_indexer(dutt__xvath, vepbi__ydyx, win, False, True)
        hhekb__eeu = roll_var_linear_generic_seq(yxm__klhyi, dutt__xvath,
            win, minp, start, end, init_data, add_obs, remove_obs, calc_out)
    else:
        hhekb__eeu = np.empty(vepbi__ydyx, np.float64)
    bodo.libs.distributed_api.bcast(hhekb__eeu)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return hhekb__eeu[start:end]


@register_jitable
def _handle_small_data_variable_apply(in_arr, on_arr, index_arr, win, minp,
    rank, n_pes, kernel_func, raw):
    N = len(in_arr)
    vepbi__ydyx = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    yxm__klhyi = bodo.libs.distributed_api.gatherv(in_arr)
    dutt__xvath = bodo.libs.distributed_api.gatherv(on_arr)
    gwnpc__dft = bodo.libs.distributed_api.gatherv(index_arr)
    if rank == 0:
        start, end = _build_indexer(dutt__xvath, vepbi__ydyx, win, False, True)
        hhekb__eeu = roll_variable_apply_seq(yxm__klhyi, dutt__xvath,
            gwnpc__dft, win, minp, start, end, kernel_func, raw)
    else:
        hhekb__eeu = np.empty(vepbi__ydyx, np.float64)
    bodo.libs.distributed_api.bcast(hhekb__eeu)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return hhekb__eeu[start:end]


@register_jitable(cache=True)
def _dropna(arr):
    humyb__kgds = len(arr)
    jlq__bhr = humyb__kgds - np.isnan(arr).sum()
    A = np.empty(jlq__bhr, arr.dtype)
    xsqd__thc = 0
    for iqr__yjdkz in range(humyb__kgds):
        val = arr[iqr__yjdkz]
        if not np.isnan(val):
            A[xsqd__thc] = val
            xsqd__thc += 1
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
