import numpy as np
import pandas as pd
import numba
from numba.extending import overload
from bodo.utils.utils import alloc_arr_tup
MIN_MERGE = 32


@numba.njit(no_cpython_wrapper=True, cache=True)
def sort(key_arrs, lo, hi, data):
    phs__xhiz = hi - lo
    if phs__xhiz < 2:
        return
    if phs__xhiz < MIN_MERGE:
        xnmu__crqxd = countRunAndMakeAscending(key_arrs, lo, hi, data)
        binarySort(key_arrs, lo, hi, lo + xnmu__crqxd, data)
        return
    stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop = (
        init_sort_start(key_arrs, data))
    bxsby__gbg = minRunLength(phs__xhiz)
    while True:
        iauq__mydw = countRunAndMakeAscending(key_arrs, lo, hi, data)
        if iauq__mydw < bxsby__gbg:
            iecr__zlfo = phs__xhiz if phs__xhiz <= bxsby__gbg else bxsby__gbg
            binarySort(key_arrs, lo, lo + iecr__zlfo, lo + iauq__mydw, data)
            iauq__mydw = iecr__zlfo
        stackSize = pushRun(stackSize, runBase, runLen, lo, iauq__mydw)
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeCollapse(
            stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
            tmp_data, minGallop)
        lo += iauq__mydw
        phs__xhiz -= iauq__mydw
        if phs__xhiz == 0:
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
        pgukl__fgmnc = getitem_arr_tup(key_arrs, start)
        yqzj__bps = getitem_arr_tup(data, start)
        fcxfz__rni = lo
        dku__sqr = start
        assert fcxfz__rni <= dku__sqr
        while fcxfz__rni < dku__sqr:
            ttji__fujdr = fcxfz__rni + dku__sqr >> 1
            if pgukl__fgmnc < getitem_arr_tup(key_arrs, ttji__fujdr):
                dku__sqr = ttji__fujdr
            else:
                fcxfz__rni = ttji__fujdr + 1
        assert fcxfz__rni == dku__sqr
        n = start - fcxfz__rni
        copyRange_tup(key_arrs, fcxfz__rni, key_arrs, fcxfz__rni + 1, n)
        copyRange_tup(data, fcxfz__rni, data, fcxfz__rni + 1, n)
        setitem_arr_tup(key_arrs, fcxfz__rni, pgukl__fgmnc)
        setitem_arr_tup(data, fcxfz__rni, yqzj__bps)
        start += 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def countRunAndMakeAscending(key_arrs, lo, hi, data):
    assert lo < hi
    sycj__jqae = lo + 1
    if sycj__jqae == hi:
        return 1
    if getitem_arr_tup(key_arrs, sycj__jqae) < getitem_arr_tup(key_arrs, lo):
        sycj__jqae += 1
        while sycj__jqae < hi and getitem_arr_tup(key_arrs, sycj__jqae
            ) < getitem_arr_tup(key_arrs, sycj__jqae - 1):
            sycj__jqae += 1
        reverseRange(key_arrs, lo, sycj__jqae, data)
    else:
        sycj__jqae += 1
        while sycj__jqae < hi and getitem_arr_tup(key_arrs, sycj__jqae
            ) >= getitem_arr_tup(key_arrs, sycj__jqae - 1):
            sycj__jqae += 1
    return sycj__jqae - lo


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
    wqcps__idm = 0
    while n >= MIN_MERGE:
        wqcps__idm |= n & 1
        n >>= 1
    return n + wqcps__idm


MIN_GALLOP = 7
INITIAL_TMP_STORAGE_LENGTH = 256


@numba.njit(no_cpython_wrapper=True, cache=True)
def init_sort_start(key_arrs, data):
    minGallop = MIN_GALLOP
    sbken__rpo = len(key_arrs[0])
    tmpLength = (sbken__rpo >> 1 if sbken__rpo < 2 *
        INITIAL_TMP_STORAGE_LENGTH else INITIAL_TMP_STORAGE_LENGTH)
    tmp = alloc_arr_tup(tmpLength, key_arrs)
    tmp_data = alloc_arr_tup(tmpLength, data)
    stackSize = 0
    hufy__yfmt = (5 if sbken__rpo < 120 else 10 if sbken__rpo < 1542 else 
        19 if sbken__rpo < 119151 else 40)
    runBase = np.empty(hufy__yfmt, np.int64)
    runLen = np.empty(hufy__yfmt, np.int64)
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
    hvl__ntn = gallopRight(getitem_arr_tup(key_arrs, base2), key_arrs,
        base1, len1, 0)
    assert hvl__ntn >= 0
    base1 += hvl__ntn
    len1 -= hvl__ntn
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
    ygrdu__sghr = 0
    iuyrq__poall = 1
    if key > getitem_arr_tup(arr, base + hint):
        zprn__glkm = _len - hint
        while iuyrq__poall < zprn__glkm and key > getitem_arr_tup(arr, base +
            hint + iuyrq__poall):
            ygrdu__sghr = iuyrq__poall
            iuyrq__poall = (iuyrq__poall << 1) + 1
            if iuyrq__poall <= 0:
                iuyrq__poall = zprn__glkm
        if iuyrq__poall > zprn__glkm:
            iuyrq__poall = zprn__glkm
        ygrdu__sghr += hint
        iuyrq__poall += hint
    else:
        zprn__glkm = hint + 1
        while iuyrq__poall < zprn__glkm and key <= getitem_arr_tup(arr, 
            base + hint - iuyrq__poall):
            ygrdu__sghr = iuyrq__poall
            iuyrq__poall = (iuyrq__poall << 1) + 1
            if iuyrq__poall <= 0:
                iuyrq__poall = zprn__glkm
        if iuyrq__poall > zprn__glkm:
            iuyrq__poall = zprn__glkm
        tmp = ygrdu__sghr
        ygrdu__sghr = hint - iuyrq__poall
        iuyrq__poall = hint - tmp
    assert -1 <= ygrdu__sghr and ygrdu__sghr < iuyrq__poall and iuyrq__poall <= _len
    ygrdu__sghr += 1
    while ygrdu__sghr < iuyrq__poall:
        xco__ake = ygrdu__sghr + (iuyrq__poall - ygrdu__sghr >> 1)
        if key > getitem_arr_tup(arr, base + xco__ake):
            ygrdu__sghr = xco__ake + 1
        else:
            iuyrq__poall = xco__ake
    assert ygrdu__sghr == iuyrq__poall
    return iuyrq__poall


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopRight(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    iuyrq__poall = 1
    ygrdu__sghr = 0
    if key < getitem_arr_tup(arr, base + hint):
        zprn__glkm = hint + 1
        while iuyrq__poall < zprn__glkm and key < getitem_arr_tup(arr, base +
            hint - iuyrq__poall):
            ygrdu__sghr = iuyrq__poall
            iuyrq__poall = (iuyrq__poall << 1) + 1
            if iuyrq__poall <= 0:
                iuyrq__poall = zprn__glkm
        if iuyrq__poall > zprn__glkm:
            iuyrq__poall = zprn__glkm
        tmp = ygrdu__sghr
        ygrdu__sghr = hint - iuyrq__poall
        iuyrq__poall = hint - tmp
    else:
        zprn__glkm = _len - hint
        while iuyrq__poall < zprn__glkm and key >= getitem_arr_tup(arr, 
            base + hint + iuyrq__poall):
            ygrdu__sghr = iuyrq__poall
            iuyrq__poall = (iuyrq__poall << 1) + 1
            if iuyrq__poall <= 0:
                iuyrq__poall = zprn__glkm
        if iuyrq__poall > zprn__glkm:
            iuyrq__poall = zprn__glkm
        ygrdu__sghr += hint
        iuyrq__poall += hint
    assert -1 <= ygrdu__sghr and ygrdu__sghr < iuyrq__poall and iuyrq__poall <= _len
    ygrdu__sghr += 1
    while ygrdu__sghr < iuyrq__poall:
        xco__ake = ygrdu__sghr + (iuyrq__poall - ygrdu__sghr >> 1)
        if key < getitem_arr_tup(arr, base + xco__ake):
            iuyrq__poall = xco__ake
        else:
            ygrdu__sghr = xco__ake + 1
    assert ygrdu__sghr == iuyrq__poall
    return iuyrq__poall


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
        efh__zjb = 0
        izt__fskk = 0
        while True:
            assert len1 > 1 and len2 > 0
            if getitem_arr_tup(arr, cursor2) < getitem_arr_tup(tmp, cursor1):
                copyElement_tup(arr, cursor2, arr, dest)
                copyElement_tup(arr_data, cursor2, arr_data, dest)
                cursor2 += 1
                dest += 1
                izt__fskk += 1
                efh__zjb = 0
                len2 -= 1
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor1, arr, dest)
                copyElement_tup(tmp_data, cursor1, arr_data, dest)
                cursor1 += 1
                dest += 1
                efh__zjb += 1
                izt__fskk = 0
                len1 -= 1
                if len1 == 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            if not efh__zjb | izt__fskk < minGallop:
                break
        while True:
            assert len1 > 1 and len2 > 0
            efh__zjb = gallopRight(getitem_arr_tup(arr, cursor2), tmp,
                cursor1, len1, 0)
            if efh__zjb != 0:
                copyRange_tup(tmp, cursor1, arr, dest, efh__zjb)
                copyRange_tup(tmp_data, cursor1, arr_data, dest, efh__zjb)
                dest += efh__zjb
                cursor1 += efh__zjb
                len1 -= efh__zjb
                if len1 <= 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor2, arr, dest)
            copyElement_tup(arr_data, cursor2, arr_data, dest)
            cursor2 += 1
            dest += 1
            len2 -= 1
            if len2 == 0:
                return len1, len2, cursor1, cursor2, dest, minGallop
            izt__fskk = gallopLeft(getitem_arr_tup(tmp, cursor1), arr,
                cursor2, len2, 0)
            if izt__fskk != 0:
                copyRange_tup(arr, cursor2, arr, dest, izt__fskk)
                copyRange_tup(arr_data, cursor2, arr_data, dest, izt__fskk)
                dest += izt__fskk
                cursor2 += izt__fskk
                len2 -= izt__fskk
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
            if not efh__zjb >= MIN_GALLOP | izt__fskk >= MIN_GALLOP:
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
        efh__zjb = 0
        izt__fskk = 0
        while True:
            assert len1 > 0 and len2 > 1
            if getitem_arr_tup(tmp, cursor2) < getitem_arr_tup(arr, cursor1):
                copyElement_tup(arr, cursor1, arr, dest)
                copyElement_tup(arr_data, cursor1, arr_data, dest)
                cursor1 -= 1
                dest -= 1
                efh__zjb += 1
                izt__fskk = 0
                len1 -= 1
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor2, arr, dest)
                copyElement_tup(tmp_data, cursor2, arr_data, dest)
                cursor2 -= 1
                dest -= 1
                izt__fskk += 1
                efh__zjb = 0
                len2 -= 1
                if len2 == 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            if not efh__zjb | izt__fskk < minGallop:
                break
        while True:
            assert len1 > 0 and len2 > 1
            efh__zjb = len1 - gallopRight(getitem_arr_tup(tmp, cursor2),
                arr, base1, len1, len1 - 1)
            if efh__zjb != 0:
                dest -= efh__zjb
                cursor1 -= efh__zjb
                len1 -= efh__zjb
                copyRange_tup(arr, cursor1 + 1, arr, dest + 1, efh__zjb)
                copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1,
                    efh__zjb)
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor2, arr, dest)
            copyElement_tup(tmp_data, cursor2, arr_data, dest)
            cursor2 -= 1
            dest -= 1
            len2 -= 1
            if len2 == 1:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            izt__fskk = len2 - gallopLeft(getitem_arr_tup(arr, cursor1),
                tmp, 0, len2, len2 - 1)
            if izt__fskk != 0:
                dest -= izt__fskk
                cursor2 -= izt__fskk
                len2 -= izt__fskk
                copyRange_tup(tmp, cursor2 + 1, arr, dest + 1, izt__fskk)
                copyRange_tup(tmp_data, cursor2 + 1, arr_data, dest + 1,
                    izt__fskk)
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
            if not efh__zjb >= MIN_GALLOP | izt__fskk >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, tmp, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def ensureCapacity(tmpLength, tmp, tmp_data, key_arrs, data, minCapacity):
    qowhc__ekow = len(key_arrs[0])
    if tmpLength < minCapacity:
        vci__cjuy = minCapacity
        vci__cjuy |= vci__cjuy >> 1
        vci__cjuy |= vci__cjuy >> 2
        vci__cjuy |= vci__cjuy >> 4
        vci__cjuy |= vci__cjuy >> 8
        vci__cjuy |= vci__cjuy >> 16
        vci__cjuy += 1
        if vci__cjuy < 0:
            vci__cjuy = minCapacity
        else:
            vci__cjuy = min(vci__cjuy, qowhc__ekow >> 1)
        tmp = alloc_arr_tup(vci__cjuy, key_arrs)
        tmp_data = alloc_arr_tup(vci__cjuy, data)
        tmpLength = vci__cjuy
    return tmpLength, tmp, tmp_data


def swap_arrs(data, lo, hi):
    for arr in data:
        hrq__fgiff = arr[lo]
        arr[lo] = arr[hi]
        arr[hi] = hrq__fgiff


@overload(swap_arrs, no_unliteral=True)
def swap_arrs_overload(arr_tup, lo, hi):
    maa__zsjw = arr_tup.count
    ftbxu__hyq = 'def f(arr_tup, lo, hi):\n'
    for i in range(maa__zsjw):
        ftbxu__hyq += '  tmp_v_{} = arr_tup[{}][lo]\n'.format(i, i)
        ftbxu__hyq += '  arr_tup[{}][lo] = arr_tup[{}][hi]\n'.format(i, i)
        ftbxu__hyq += '  arr_tup[{}][hi] = tmp_v_{}\n'.format(i, i)
    ftbxu__hyq += '  return\n'
    gwt__zohn = {}
    exec(ftbxu__hyq, {}, gwt__zohn)
    bpz__zhrkl = gwt__zohn['f']
    return bpz__zhrkl


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyRange(src_arr, src_pos, dst_arr, dst_pos, n):
    dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


def copyRange_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


@overload(copyRange_tup, no_unliteral=True)
def copyRange_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    maa__zsjw = src_arr_tup.count
    assert maa__zsjw == dst_arr_tup.count
    ftbxu__hyq = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):\n'
    for i in range(maa__zsjw):
        ftbxu__hyq += (
            '  copyRange(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos, n)\n'
            .format(i, i))
    ftbxu__hyq += '  return\n'
    gwt__zohn = {}
    exec(ftbxu__hyq, {'copyRange': copyRange}, gwt__zohn)
    ztaf__bthf = gwt__zohn['f']
    return ztaf__bthf


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyElement(src_arr, src_pos, dst_arr, dst_pos):
    dst_arr[dst_pos] = src_arr[src_pos]


def copyElement_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos] = src_arr[src_pos]


@overload(copyElement_tup, no_unliteral=True)
def copyElement_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    maa__zsjw = src_arr_tup.count
    assert maa__zsjw == dst_arr_tup.count
    ftbxu__hyq = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos):\n'
    for i in range(maa__zsjw):
        ftbxu__hyq += (
            '  copyElement(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos)\n'
            .format(i, i))
    ftbxu__hyq += '  return\n'
    gwt__zohn = {}
    exec(ftbxu__hyq, {'copyElement': copyElement}, gwt__zohn)
    ztaf__bthf = gwt__zohn['f']
    return ztaf__bthf


def getitem_arr_tup(arr_tup, ind):
    zzmg__onh = [arr[ind] for arr in arr_tup]
    return tuple(zzmg__onh)


@overload(getitem_arr_tup, no_unliteral=True)
def getitem_arr_tup_overload(arr_tup, ind):
    maa__zsjw = arr_tup.count
    ftbxu__hyq = 'def f(arr_tup, ind):\n'
    ftbxu__hyq += '  return ({}{})\n'.format(','.join(['arr_tup[{}][ind]'.
        format(i) for i in range(maa__zsjw)]), ',' if maa__zsjw == 1 else '')
    gwt__zohn = {}
    exec(ftbxu__hyq, {}, gwt__zohn)
    hwwf__bri = gwt__zohn['f']
    return hwwf__bri


def setitem_arr_tup(arr_tup, ind, val_tup):
    for arr, xfkbf__qnl in zip(arr_tup, val_tup):
        arr[ind] = xfkbf__qnl


@overload(setitem_arr_tup, no_unliteral=True)
def setitem_arr_tup_overload(arr_tup, ind, val_tup):
    maa__zsjw = arr_tup.count
    ftbxu__hyq = 'def f(arr_tup, ind, val_tup):\n'
    for i in range(maa__zsjw):
        if isinstance(val_tup, numba.core.types.BaseTuple):
            ftbxu__hyq += '  arr_tup[{}][ind] = val_tup[{}]\n'.format(i, i)
        else:
            assert arr_tup.count == 1
            ftbxu__hyq += '  arr_tup[{}][ind] = val_tup\n'.format(i)
    ftbxu__hyq += '  return\n'
    gwt__zohn = {}
    exec(ftbxu__hyq, {}, gwt__zohn)
    hwwf__bri = gwt__zohn['f']
    return hwwf__bri


def test():
    import time
    abfov__tkxy = time.time()
    vtmo__drxe = np.ones(3)
    data = np.arange(3), np.ones(3)
    sort((vtmo__drxe,), 0, 3, data)
    print('compile time', time.time() - abfov__tkxy)
    n = 210000
    np.random.seed(2)
    data = np.arange(n), np.random.ranf(n)
    bujn__wyu = np.random.ranf(n)
    pvdeb__prxiq = pd.DataFrame({'A': bujn__wyu, 'B': data[0], 'C': data[1]})
    abfov__tkxy = time.time()
    iwfkx__whbp = pvdeb__prxiq.sort_values('A', inplace=False)
    fpip__plqep = time.time()
    sort((bujn__wyu,), 0, n, data)
    print('Bodo', time.time() - fpip__plqep, 'Numpy', fpip__plqep - abfov__tkxy
        )
    np.testing.assert_almost_equal(data[0], iwfkx__whbp.B.values)
    np.testing.assert_almost_equal(data[1], iwfkx__whbp.C.values)


if __name__ == '__main__':
    test()
