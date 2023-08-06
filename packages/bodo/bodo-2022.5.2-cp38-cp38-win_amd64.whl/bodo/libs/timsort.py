import numpy as np
import pandas as pd
import numba
from numba.extending import overload
from bodo.utils.utils import alloc_arr_tup
MIN_MERGE = 32


@numba.njit(no_cpython_wrapper=True, cache=True)
def sort(key_arrs, lo, hi, data):
    sxczj__rlx = hi - lo
    if sxczj__rlx < 2:
        return
    if sxczj__rlx < MIN_MERGE:
        hmz__tbz = countRunAndMakeAscending(key_arrs, lo, hi, data)
        binarySort(key_arrs, lo, hi, lo + hmz__tbz, data)
        return
    stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop = (
        init_sort_start(key_arrs, data))
    zakdz__wvwo = minRunLength(sxczj__rlx)
    while True:
        uecn__onbps = countRunAndMakeAscending(key_arrs, lo, hi, data)
        if uecn__onbps < zakdz__wvwo:
            abwgh__ncj = (sxczj__rlx if sxczj__rlx <= zakdz__wvwo else
                zakdz__wvwo)
            binarySort(key_arrs, lo, lo + abwgh__ncj, lo + uecn__onbps, data)
            uecn__onbps = abwgh__ncj
        stackSize = pushRun(stackSize, runBase, runLen, lo, uecn__onbps)
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeCollapse(
            stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
            tmp_data, minGallop)
        lo += uecn__onbps
        sxczj__rlx -= uecn__onbps
        if sxczj__rlx == 0:
            break
    assert lo == hi
    stackSize, tmpLength, tmp, tmp_data, minGallop = mergeForceCollapse(
        stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
        tmp_data, minGallop)
    assert stackSize == 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def binarySort(key_arrs, lo, hi, start, data):
    assert lo <= start and start <= hi
    if start == lo:
        start += 1
    while start < hi:
        zqqj__esr = getitem_arr_tup(key_arrs, start)
        urtbd__vwn = getitem_arr_tup(data, start)
        wrdop__jmg = lo
        ughj__rpco = start
        assert wrdop__jmg <= ughj__rpco
        while wrdop__jmg < ughj__rpco:
            ioh__tjj = wrdop__jmg + ughj__rpco >> 1
            if zqqj__esr < getitem_arr_tup(key_arrs, ioh__tjj):
                ughj__rpco = ioh__tjj
            else:
                wrdop__jmg = ioh__tjj + 1
        assert wrdop__jmg == ughj__rpco
        n = start - wrdop__jmg
        copyRange_tup(key_arrs, wrdop__jmg, key_arrs, wrdop__jmg + 1, n)
        copyRange_tup(data, wrdop__jmg, data, wrdop__jmg + 1, n)
        setitem_arr_tup(key_arrs, wrdop__jmg, zqqj__esr)
        setitem_arr_tup(data, wrdop__jmg, urtbd__vwn)
        start += 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def countRunAndMakeAscending(key_arrs, lo, hi, data):
    assert lo < hi
    pexy__nhkul = lo + 1
    if pexy__nhkul == hi:
        return 1
    if getitem_arr_tup(key_arrs, pexy__nhkul) < getitem_arr_tup(key_arrs, lo):
        pexy__nhkul += 1
        while pexy__nhkul < hi and getitem_arr_tup(key_arrs, pexy__nhkul
            ) < getitem_arr_tup(key_arrs, pexy__nhkul - 1):
            pexy__nhkul += 1
        reverseRange(key_arrs, lo, pexy__nhkul, data)
    else:
        pexy__nhkul += 1
        while pexy__nhkul < hi and getitem_arr_tup(key_arrs, pexy__nhkul
            ) >= getitem_arr_tup(key_arrs, pexy__nhkul - 1):
            pexy__nhkul += 1
    return pexy__nhkul - lo


@numba.njit(no_cpython_wrapper=True, cache=True)
def reverseRange(key_arrs, lo, hi, data):
    hi -= 1
    while lo < hi:
        swap_arrs(key_arrs, lo, hi)
        swap_arrs(data, lo, hi)
        lo += 1
        hi -= 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def minRunLength(n):
    assert n >= 0
    gbi__vnljo = 0
    while n >= MIN_MERGE:
        gbi__vnljo |= n & 1
        n >>= 1
    return n + gbi__vnljo


MIN_GALLOP = 7
INITIAL_TMP_STORAGE_LENGTH = 256


@numba.njit(no_cpython_wrapper=True, cache=True)
def init_sort_start(key_arrs, data):
    minGallop = MIN_GALLOP
    tuzh__ygiu = len(key_arrs[0])
    tmpLength = (tuzh__ygiu >> 1 if tuzh__ygiu < 2 *
        INITIAL_TMP_STORAGE_LENGTH else INITIAL_TMP_STORAGE_LENGTH)
    tmp = alloc_arr_tup(tmpLength, key_arrs)
    tmp_data = alloc_arr_tup(tmpLength, data)
    stackSize = 0
    tbifr__tbso = (5 if tuzh__ygiu < 120 else 10 if tuzh__ygiu < 1542 else 
        19 if tuzh__ygiu < 119151 else 40)
    runBase = np.empty(tbifr__tbso, np.int64)
    runLen = np.empty(tbifr__tbso, np.int64)
    return stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def pushRun(stackSize, runBase, runLen, runBase_val, runLen_val):
    runBase[stackSize] = runBase_val
    runLen[stackSize] = runLen_val
    stackSize += 1
    return stackSize


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeCollapse(stackSize, runBase, runLen, key_arrs, data, tmpLength,
    tmp, tmp_data, minGallop):
    while stackSize > 1:
        n = stackSize - 2
        if n >= 1 and runLen[n - 1] <= runLen[n] + runLen[n + 1
            ] or n >= 2 and runLen[n - 2] <= runLen[n] + runLen[n - 1]:
            if runLen[n - 1] < runLen[n + 1]:
                n -= 1
        elif runLen[n] > runLen[n + 1]:
            break
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeAt(stackSize,
            runBase, runLen, key_arrs, data, tmpLength, tmp, tmp_data,
            minGallop, n)
    return stackSize, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeForceCollapse(stackSize, runBase, runLen, key_arrs, data,
    tmpLength, tmp, tmp_data, minGallop):
    while stackSize > 1:
        n = stackSize - 2
        if n > 0 and runLen[n - 1] < runLen[n + 1]:
            n -= 1
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeAt(stackSize,
            runBase, runLen, key_arrs, data, tmpLength, tmp, tmp_data,
            minGallop, n)
    return stackSize, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeAt(stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
    tmp_data, minGallop, i):
    assert stackSize >= 2
    assert i >= 0
    assert i == stackSize - 2 or i == stackSize - 3
    base1 = runBase[i]
    len1 = runLen[i]
    base2 = runBase[i + 1]
    len2 = runLen[i + 1]
    assert len1 > 0 and len2 > 0
    assert base1 + len1 == base2
    runLen[i] = len1 + len2
    if i == stackSize - 3:
        runBase[i + 1] = runBase[i + 2]
        runLen[i + 1] = runLen[i + 2]
    stackSize -= 1
    xsm__nno = gallopRight(getitem_arr_tup(key_arrs, base2), key_arrs,
        base1, len1, 0)
    assert xsm__nno >= 0
    base1 += xsm__nno
    len1 -= xsm__nno
    if len1 == 0:
        return stackSize, tmpLength, tmp, tmp_data, minGallop
    len2 = gallopLeft(getitem_arr_tup(key_arrs, base1 + len1 - 1), key_arrs,
        base2, len2, len2 - 1)
    assert len2 >= 0
    if len2 == 0:
        return stackSize, tmpLength, tmp, tmp_data, minGallop
    if len1 <= len2:
        tmpLength, tmp, tmp_data = ensureCapacity(tmpLength, tmp, tmp_data,
            key_arrs, data, len1)
        minGallop = mergeLo(key_arrs, data, tmp, tmp_data, minGallop, base1,
            len1, base2, len2)
    else:
        tmpLength, tmp, tmp_data = ensureCapacity(tmpLength, tmp, tmp_data,
            key_arrs, data, len2)
        minGallop = mergeHi(key_arrs, data, tmp, tmp_data, minGallop, base1,
            len1, base2, len2)
    return stackSize, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopLeft(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    xsta__lua = 0
    hxnjp__milz = 1
    if key > getitem_arr_tup(arr, base + hint):
        bslwc__wrbu = _len - hint
        while hxnjp__milz < bslwc__wrbu and key > getitem_arr_tup(arr, base +
            hint + hxnjp__milz):
            xsta__lua = hxnjp__milz
            hxnjp__milz = (hxnjp__milz << 1) + 1
            if hxnjp__milz <= 0:
                hxnjp__milz = bslwc__wrbu
        if hxnjp__milz > bslwc__wrbu:
            hxnjp__milz = bslwc__wrbu
        xsta__lua += hint
        hxnjp__milz += hint
    else:
        bslwc__wrbu = hint + 1
        while hxnjp__milz < bslwc__wrbu and key <= getitem_arr_tup(arr, 
            base + hint - hxnjp__milz):
            xsta__lua = hxnjp__milz
            hxnjp__milz = (hxnjp__milz << 1) + 1
            if hxnjp__milz <= 0:
                hxnjp__milz = bslwc__wrbu
        if hxnjp__milz > bslwc__wrbu:
            hxnjp__milz = bslwc__wrbu
        tmp = xsta__lua
        xsta__lua = hint - hxnjp__milz
        hxnjp__milz = hint - tmp
    assert -1 <= xsta__lua and xsta__lua < hxnjp__milz and hxnjp__milz <= _len
    xsta__lua += 1
    while xsta__lua < hxnjp__milz:
        pwad__zdvfo = xsta__lua + (hxnjp__milz - xsta__lua >> 1)
        if key > getitem_arr_tup(arr, base + pwad__zdvfo):
            xsta__lua = pwad__zdvfo + 1
        else:
            hxnjp__milz = pwad__zdvfo
    assert xsta__lua == hxnjp__milz
    return hxnjp__milz


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopRight(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    hxnjp__milz = 1
    xsta__lua = 0
    if key < getitem_arr_tup(arr, base + hint):
        bslwc__wrbu = hint + 1
        while hxnjp__milz < bslwc__wrbu and key < getitem_arr_tup(arr, base +
            hint - hxnjp__milz):
            xsta__lua = hxnjp__milz
            hxnjp__milz = (hxnjp__milz << 1) + 1
            if hxnjp__milz <= 0:
                hxnjp__milz = bslwc__wrbu
        if hxnjp__milz > bslwc__wrbu:
            hxnjp__milz = bslwc__wrbu
        tmp = xsta__lua
        xsta__lua = hint - hxnjp__milz
        hxnjp__milz = hint - tmp
    else:
        bslwc__wrbu = _len - hint
        while hxnjp__milz < bslwc__wrbu and key >= getitem_arr_tup(arr, 
            base + hint + hxnjp__milz):
            xsta__lua = hxnjp__milz
            hxnjp__milz = (hxnjp__milz << 1) + 1
            if hxnjp__milz <= 0:
                hxnjp__milz = bslwc__wrbu
        if hxnjp__milz > bslwc__wrbu:
            hxnjp__milz = bslwc__wrbu
        xsta__lua += hint
        hxnjp__milz += hint
    assert -1 <= xsta__lua and xsta__lua < hxnjp__milz and hxnjp__milz <= _len
    xsta__lua += 1
    while xsta__lua < hxnjp__milz:
        pwad__zdvfo = xsta__lua + (hxnjp__milz - xsta__lua >> 1)
        if key < getitem_arr_tup(arr, base + pwad__zdvfo):
            hxnjp__milz = pwad__zdvfo
        else:
            xsta__lua = pwad__zdvfo + 1
    assert xsta__lua == hxnjp__milz
    return hxnjp__milz


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeLo(key_arrs, data, tmp, tmp_data, minGallop, base1, len1, base2, len2
    ):
    assert len1 > 0 and len2 > 0 and base1 + len1 == base2
    arr = key_arrs
    arr_data = data
    copyRange_tup(arr, base1, tmp, 0, len1)
    copyRange_tup(arr_data, base1, tmp_data, 0, len1)
    cursor1 = 0
    cursor2 = base2
    dest = base1
    setitem_arr_tup(arr, dest, getitem_arr_tup(arr, cursor2))
    copyElement_tup(arr_data, cursor2, arr_data, dest)
    cursor2 += 1
    dest += 1
    len2 -= 1
    if len2 == 0:
        copyRange_tup(tmp, cursor1, arr, dest, len1)
        copyRange_tup(tmp_data, cursor1, arr_data, dest, len1)
        return minGallop
    if len1 == 1:
        copyRange_tup(arr, cursor2, arr, dest, len2)
        copyRange_tup(arr_data, cursor2, arr_data, dest, len2)
        copyElement_tup(tmp, cursor1, arr, dest + len2)
        copyElement_tup(tmp_data, cursor1, arr_data, dest + len2)
        return minGallop
    len1, len2, cursor1, cursor2, dest, minGallop = mergeLo_inner(key_arrs,
        data, tmp_data, len1, len2, tmp, cursor1, cursor2, dest, minGallop)
    minGallop = 1 if minGallop < 1 else minGallop
    if len1 == 1:
        assert len2 > 0
        copyRange_tup(arr, cursor2, arr, dest, len2)
        copyRange_tup(arr_data, cursor2, arr_data, dest, len2)
        copyElement_tup(tmp, cursor1, arr, dest + len2)
        copyElement_tup(tmp_data, cursor1, arr_data, dest + len2)
    elif len1 == 0:
        raise ValueError('Comparison method violates its general contract!')
    else:
        assert len2 == 0
        assert len1 > 1
        copyRange_tup(tmp, cursor1, arr, dest, len1)
        copyRange_tup(tmp_data, cursor1, arr_data, dest, len1)
    return minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeLo_inner(arr, arr_data, tmp_data, len1, len2, tmp, cursor1,
    cursor2, dest, minGallop):
    while True:
        qdoe__rls = 0
        kaxth__suh = 0
        while True:
            assert len1 > 1 and len2 > 0
            if getitem_arr_tup(arr, cursor2) < getitem_arr_tup(tmp, cursor1):
                copyElement_tup(arr, cursor2, arr, dest)
                copyElement_tup(arr_data, cursor2, arr_data, dest)
                cursor2 += 1
                dest += 1
                kaxth__suh += 1
                qdoe__rls = 0
                len2 -= 1
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor1, arr, dest)
                copyElement_tup(tmp_data, cursor1, arr_data, dest)
                cursor1 += 1
                dest += 1
                qdoe__rls += 1
                kaxth__suh = 0
                len1 -= 1
                if len1 == 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            if not qdoe__rls | kaxth__suh < minGallop:
                break
        while True:
            assert len1 > 1 and len2 > 0
            qdoe__rls = gallopRight(getitem_arr_tup(arr, cursor2), tmp,
                cursor1, len1, 0)
            if qdoe__rls != 0:
                copyRange_tup(tmp, cursor1, arr, dest, qdoe__rls)
                copyRange_tup(tmp_data, cursor1, arr_data, dest, qdoe__rls)
                dest += qdoe__rls
                cursor1 += qdoe__rls
                len1 -= qdoe__rls
                if len1 <= 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor2, arr, dest)
            copyElement_tup(arr_data, cursor2, arr_data, dest)
            cursor2 += 1
            dest += 1
            len2 -= 1
            if len2 == 0:
                return len1, len2, cursor1, cursor2, dest, minGallop
            kaxth__suh = gallopLeft(getitem_arr_tup(tmp, cursor1), arr,
                cursor2, len2, 0)
            if kaxth__suh != 0:
                copyRange_tup(arr, cursor2, arr, dest, kaxth__suh)
                copyRange_tup(arr_data, cursor2, arr_data, dest, kaxth__suh)
                dest += kaxth__suh
                cursor2 += kaxth__suh
                len2 -= kaxth__suh
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor1, arr, dest)
            copyElement_tup(tmp_data, cursor1, arr_data, dest)
            cursor1 += 1
            dest += 1
            len1 -= 1
            if len1 == 1:
                return len1, len2, cursor1, cursor2, dest, minGallop
            minGallop -= 1
            if not qdoe__rls >= MIN_GALLOP | kaxth__suh >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeHi(key_arrs, data, tmp, tmp_data, minGallop, base1, len1, base2, len2
    ):
    assert len1 > 0 and len2 > 0 and base1 + len1 == base2
    arr = key_arrs
    arr_data = data
    copyRange_tup(arr, base2, tmp, 0, len2)
    copyRange_tup(arr_data, base2, tmp_data, 0, len2)
    cursor1 = base1 + len1 - 1
    cursor2 = len2 - 1
    dest = base2 + len2 - 1
    copyElement_tup(arr, cursor1, arr, dest)
    copyElement_tup(arr_data, cursor1, arr_data, dest)
    cursor1 -= 1
    dest -= 1
    len1 -= 1
    if len1 == 0:
        copyRange_tup(tmp, 0, arr, dest - (len2 - 1), len2)
        copyRange_tup(tmp_data, 0, arr_data, dest - (len2 - 1), len2)
        return minGallop
    if len2 == 1:
        dest -= len1
        cursor1 -= len1
        copyRange_tup(arr, cursor1 + 1, arr, dest + 1, len1)
        copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1, len1)
        copyElement_tup(tmp, cursor2, arr, dest)
        copyElement_tup(tmp_data, cursor2, arr_data, dest)
        return minGallop
    len1, len2, tmp, cursor1, cursor2, dest, minGallop = mergeHi_inner(key_arrs
        , data, tmp_data, base1, len1, len2, tmp, cursor1, cursor2, dest,
        minGallop)
    minGallop = 1 if minGallop < 1 else minGallop
    if len2 == 1:
        assert len1 > 0
        dest -= len1
        cursor1 -= len1
        copyRange_tup(arr, cursor1 + 1, arr, dest + 1, len1)
        copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1, len1)
        copyElement_tup(tmp, cursor2, arr, dest)
        copyElement_tup(tmp_data, cursor2, arr_data, dest)
    elif len2 == 0:
        raise ValueError('Comparison method violates its general contract!')
    else:
        assert len1 == 0
        assert len2 > 0
        copyRange_tup(tmp, 0, arr, dest - (len2 - 1), len2)
        copyRange_tup(tmp_data, 0, arr_data, dest - (len2 - 1), len2)
    return minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeHi_inner(arr, arr_data, tmp_data, base1, len1, len2, tmp, cursor1,
    cursor2, dest, minGallop):
    while True:
        qdoe__rls = 0
        kaxth__suh = 0
        while True:
            assert len1 > 0 and len2 > 1
            if getitem_arr_tup(tmp, cursor2) < getitem_arr_tup(arr, cursor1):
                copyElement_tup(arr, cursor1, arr, dest)
                copyElement_tup(arr_data, cursor1, arr_data, dest)
                cursor1 -= 1
                dest -= 1
                qdoe__rls += 1
                kaxth__suh = 0
                len1 -= 1
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor2, arr, dest)
                copyElement_tup(tmp_data, cursor2, arr_data, dest)
                cursor2 -= 1
                dest -= 1
                kaxth__suh += 1
                qdoe__rls = 0
                len2 -= 1
                if len2 == 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            if not qdoe__rls | kaxth__suh < minGallop:
                break
        while True:
            assert len1 > 0 and len2 > 1
            qdoe__rls = len1 - gallopRight(getitem_arr_tup(tmp, cursor2),
                arr, base1, len1, len1 - 1)
            if qdoe__rls != 0:
                dest -= qdoe__rls
                cursor1 -= qdoe__rls
                len1 -= qdoe__rls
                copyRange_tup(arr, cursor1 + 1, arr, dest + 1, qdoe__rls)
                copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1,
                    qdoe__rls)
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor2, arr, dest)
            copyElement_tup(tmp_data, cursor2, arr_data, dest)
            cursor2 -= 1
            dest -= 1
            len2 -= 1
            if len2 == 1:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            kaxth__suh = len2 - gallopLeft(getitem_arr_tup(arr, cursor1),
                tmp, 0, len2, len2 - 1)
            if kaxth__suh != 0:
                dest -= kaxth__suh
                cursor2 -= kaxth__suh
                len2 -= kaxth__suh
                copyRange_tup(tmp, cursor2 + 1, arr, dest + 1, kaxth__suh)
                copyRange_tup(tmp_data, cursor2 + 1, arr_data, dest + 1,
                    kaxth__suh)
                if len2 <= 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor1, arr, dest)
            copyElement_tup(arr_data, cursor1, arr_data, dest)
            cursor1 -= 1
            dest -= 1
            len1 -= 1
            if len1 == 0:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            minGallop -= 1
            if not qdoe__rls >= MIN_GALLOP | kaxth__suh >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, tmp, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def ensureCapacity(tmpLength, tmp, tmp_data, key_arrs, data, minCapacity):
    pkzrx__znav = len(key_arrs[0])
    if tmpLength < minCapacity:
        ahiu__fkxhw = minCapacity
        ahiu__fkxhw |= ahiu__fkxhw >> 1
        ahiu__fkxhw |= ahiu__fkxhw >> 2
        ahiu__fkxhw |= ahiu__fkxhw >> 4
        ahiu__fkxhw |= ahiu__fkxhw >> 8
        ahiu__fkxhw |= ahiu__fkxhw >> 16
        ahiu__fkxhw += 1
        if ahiu__fkxhw < 0:
            ahiu__fkxhw = minCapacity
        else:
            ahiu__fkxhw = min(ahiu__fkxhw, pkzrx__znav >> 1)
        tmp = alloc_arr_tup(ahiu__fkxhw, key_arrs)
        tmp_data = alloc_arr_tup(ahiu__fkxhw, data)
        tmpLength = ahiu__fkxhw
    return tmpLength, tmp, tmp_data


def swap_arrs(data, lo, hi):
    for arr in data:
        gsc__wgdf = arr[lo]
        arr[lo] = arr[hi]
        arr[hi] = gsc__wgdf


@overload(swap_arrs, no_unliteral=True)
def swap_arrs_overload(arr_tup, lo, hi):
    cltbr__vwfm = arr_tup.count
    fcc__igdr = 'def f(arr_tup, lo, hi):\n'
    for i in range(cltbr__vwfm):
        fcc__igdr += '  tmp_v_{} = arr_tup[{}][lo]\n'.format(i, i)
        fcc__igdr += '  arr_tup[{}][lo] = arr_tup[{}][hi]\n'.format(i, i)
        fcc__igdr += '  arr_tup[{}][hi] = tmp_v_{}\n'.format(i, i)
    fcc__igdr += '  return\n'
    xdl__yyhcm = {}
    exec(fcc__igdr, {}, xdl__yyhcm)
    dpmnk__jwyz = xdl__yyhcm['f']
    return dpmnk__jwyz


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyRange(src_arr, src_pos, dst_arr, dst_pos, n):
    dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


def copyRange_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


@overload(copyRange_tup, no_unliteral=True)
def copyRange_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    cltbr__vwfm = src_arr_tup.count
    assert cltbr__vwfm == dst_arr_tup.count
    fcc__igdr = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):\n'
    for i in range(cltbr__vwfm):
        fcc__igdr += (
            '  copyRange(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos, n)\n'
            .format(i, i))
    fcc__igdr += '  return\n'
    xdl__yyhcm = {}
    exec(fcc__igdr, {'copyRange': copyRange}, xdl__yyhcm)
    ecd__dyub = xdl__yyhcm['f']
    return ecd__dyub


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyElement(src_arr, src_pos, dst_arr, dst_pos):
    dst_arr[dst_pos] = src_arr[src_pos]


def copyElement_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos] = src_arr[src_pos]


@overload(copyElement_tup, no_unliteral=True)
def copyElement_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    cltbr__vwfm = src_arr_tup.count
    assert cltbr__vwfm == dst_arr_tup.count
    fcc__igdr = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos):\n'
    for i in range(cltbr__vwfm):
        fcc__igdr += (
            '  copyElement(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos)\n'
            .format(i, i))
    fcc__igdr += '  return\n'
    xdl__yyhcm = {}
    exec(fcc__igdr, {'copyElement': copyElement}, xdl__yyhcm)
    ecd__dyub = xdl__yyhcm['f']
    return ecd__dyub


def getitem_arr_tup(arr_tup, ind):
    dvs__zna = [arr[ind] for arr in arr_tup]
    return tuple(dvs__zna)


@overload(getitem_arr_tup, no_unliteral=True)
def getitem_arr_tup_overload(arr_tup, ind):
    cltbr__vwfm = arr_tup.count
    fcc__igdr = 'def f(arr_tup, ind):\n'
    fcc__igdr += '  return ({}{})\n'.format(','.join(['arr_tup[{}][ind]'.
        format(i) for i in range(cltbr__vwfm)]), ',' if cltbr__vwfm == 1 else
        '')
    xdl__yyhcm = {}
    exec(fcc__igdr, {}, xdl__yyhcm)
    lhlej__oynav = xdl__yyhcm['f']
    return lhlej__oynav


def setitem_arr_tup(arr_tup, ind, val_tup):
    for arr, irqj__rsim in zip(arr_tup, val_tup):
        arr[ind] = irqj__rsim


@overload(setitem_arr_tup, no_unliteral=True)
def setitem_arr_tup_overload(arr_tup, ind, val_tup):
    cltbr__vwfm = arr_tup.count
    fcc__igdr = 'def f(arr_tup, ind, val_tup):\n'
    for i in range(cltbr__vwfm):
        if isinstance(val_tup, numba.core.types.BaseTuple):
            fcc__igdr += '  arr_tup[{}][ind] = val_tup[{}]\n'.format(i, i)
        else:
            assert arr_tup.count == 1
            fcc__igdr += '  arr_tup[{}][ind] = val_tup\n'.format(i)
    fcc__igdr += '  return\n'
    xdl__yyhcm = {}
    exec(fcc__igdr, {}, xdl__yyhcm)
    lhlej__oynav = xdl__yyhcm['f']
    return lhlej__oynav


def test():
    import time
    fmdvp__gcls = time.time()
    owujh__rtj = np.ones(3)
    data = np.arange(3), np.ones(3)
    sort((owujh__rtj,), 0, 3, data)
    print('compile time', time.time() - fmdvp__gcls)
    n = 210000
    np.random.seed(2)
    data = np.arange(n), np.random.ranf(n)
    ccx__pdmr = np.random.ranf(n)
    rajcs__qkdf = pd.DataFrame({'A': ccx__pdmr, 'B': data[0], 'C': data[1]})
    fmdvp__gcls = time.time()
    ogqz__lanw = rajcs__qkdf.sort_values('A', inplace=False)
    qirp__jzk = time.time()
    sort((ccx__pdmr,), 0, n, data)
    print('Bodo', time.time() - qirp__jzk, 'Numpy', qirp__jzk - fmdvp__gcls)
    np.testing.assert_almost_equal(data[0], ogqz__lanw.B.values)
    np.testing.assert_almost_equal(data[1], ogqz__lanw.C.values)


if __name__ == '__main__':
    test()
