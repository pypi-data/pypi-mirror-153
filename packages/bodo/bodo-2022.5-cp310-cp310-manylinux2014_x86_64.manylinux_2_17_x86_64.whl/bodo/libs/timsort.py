import numpy as np
import pandas as pd
import numba
from numba.extending import overload
from bodo.utils.utils import alloc_arr_tup
MIN_MERGE = 32


@numba.njit(no_cpython_wrapper=True, cache=True)
def sort(key_arrs, lo, hi, data):
    pxkw__vnq = hi - lo
    if pxkw__vnq < 2:
        return
    if pxkw__vnq < MIN_MERGE:
        qse__bmcem = countRunAndMakeAscending(key_arrs, lo, hi, data)
        binarySort(key_arrs, lo, hi, lo + qse__bmcem, data)
        return
    stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop = (
        init_sort_start(key_arrs, data))
    eouly__ftyv = minRunLength(pxkw__vnq)
    while True:
        clml__bfb = countRunAndMakeAscending(key_arrs, lo, hi, data)
        if clml__bfb < eouly__ftyv:
            xyfz__zaz = pxkw__vnq if pxkw__vnq <= eouly__ftyv else eouly__ftyv
            binarySort(key_arrs, lo, lo + xyfz__zaz, lo + clml__bfb, data)
            clml__bfb = xyfz__zaz
        stackSize = pushRun(stackSize, runBase, runLen, lo, clml__bfb)
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeCollapse(
            stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
            tmp_data, minGallop)
        lo += clml__bfb
        pxkw__vnq -= clml__bfb
        if pxkw__vnq == 0:
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
        pmpv__tpezu = getitem_arr_tup(key_arrs, start)
        ghgfy__bwe = getitem_arr_tup(data, start)
        fwc__gehk = lo
        bxlw__yxd = start
        assert fwc__gehk <= bxlw__yxd
        while fwc__gehk < bxlw__yxd:
            kre__ixpfd = fwc__gehk + bxlw__yxd >> 1
            if pmpv__tpezu < getitem_arr_tup(key_arrs, kre__ixpfd):
                bxlw__yxd = kre__ixpfd
            else:
                fwc__gehk = kre__ixpfd + 1
        assert fwc__gehk == bxlw__yxd
        n = start - fwc__gehk
        copyRange_tup(key_arrs, fwc__gehk, key_arrs, fwc__gehk + 1, n)
        copyRange_tup(data, fwc__gehk, data, fwc__gehk + 1, n)
        setitem_arr_tup(key_arrs, fwc__gehk, pmpv__tpezu)
        setitem_arr_tup(data, fwc__gehk, ghgfy__bwe)
        start += 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def countRunAndMakeAscending(key_arrs, lo, hi, data):
    assert lo < hi
    upvfg__hqxld = lo + 1
    if upvfg__hqxld == hi:
        return 1
    if getitem_arr_tup(key_arrs, upvfg__hqxld) < getitem_arr_tup(key_arrs, lo):
        upvfg__hqxld += 1
        while upvfg__hqxld < hi and getitem_arr_tup(key_arrs, upvfg__hqxld
            ) < getitem_arr_tup(key_arrs, upvfg__hqxld - 1):
            upvfg__hqxld += 1
        reverseRange(key_arrs, lo, upvfg__hqxld, data)
    else:
        upvfg__hqxld += 1
        while upvfg__hqxld < hi and getitem_arr_tup(key_arrs, upvfg__hqxld
            ) >= getitem_arr_tup(key_arrs, upvfg__hqxld - 1):
            upvfg__hqxld += 1
    return upvfg__hqxld - lo


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
    bygk__xtaty = 0
    while n >= MIN_MERGE:
        bygk__xtaty |= n & 1
        n >>= 1
    return n + bygk__xtaty


MIN_GALLOP = 7
INITIAL_TMP_STORAGE_LENGTH = 256


@numba.njit(no_cpython_wrapper=True, cache=True)
def init_sort_start(key_arrs, data):
    minGallop = MIN_GALLOP
    btxg__obda = len(key_arrs[0])
    tmpLength = (btxg__obda >> 1 if btxg__obda < 2 *
        INITIAL_TMP_STORAGE_LENGTH else INITIAL_TMP_STORAGE_LENGTH)
    tmp = alloc_arr_tup(tmpLength, key_arrs)
    tmp_data = alloc_arr_tup(tmpLength, data)
    stackSize = 0
    pmatg__xmzi = (5 if btxg__obda < 120 else 10 if btxg__obda < 1542 else 
        19 if btxg__obda < 119151 else 40)
    runBase = np.empty(pmatg__xmzi, np.int64)
    runLen = np.empty(pmatg__xmzi, np.int64)
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
    sywtv__bmry = gallopRight(getitem_arr_tup(key_arrs, base2), key_arrs,
        base1, len1, 0)
    assert sywtv__bmry >= 0
    base1 += sywtv__bmry
    len1 -= sywtv__bmry
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
    sqmi__xnq = 0
    asqhg__thflh = 1
    if key > getitem_arr_tup(arr, base + hint):
        mxlat__agg = _len - hint
        while asqhg__thflh < mxlat__agg and key > getitem_arr_tup(arr, base +
            hint + asqhg__thflh):
            sqmi__xnq = asqhg__thflh
            asqhg__thflh = (asqhg__thflh << 1) + 1
            if asqhg__thflh <= 0:
                asqhg__thflh = mxlat__agg
        if asqhg__thflh > mxlat__agg:
            asqhg__thflh = mxlat__agg
        sqmi__xnq += hint
        asqhg__thflh += hint
    else:
        mxlat__agg = hint + 1
        while asqhg__thflh < mxlat__agg and key <= getitem_arr_tup(arr, 
            base + hint - asqhg__thflh):
            sqmi__xnq = asqhg__thflh
            asqhg__thflh = (asqhg__thflh << 1) + 1
            if asqhg__thflh <= 0:
                asqhg__thflh = mxlat__agg
        if asqhg__thflh > mxlat__agg:
            asqhg__thflh = mxlat__agg
        tmp = sqmi__xnq
        sqmi__xnq = hint - asqhg__thflh
        asqhg__thflh = hint - tmp
    assert -1 <= sqmi__xnq and sqmi__xnq < asqhg__thflh and asqhg__thflh <= _len
    sqmi__xnq += 1
    while sqmi__xnq < asqhg__thflh:
        zdtct__zny = sqmi__xnq + (asqhg__thflh - sqmi__xnq >> 1)
        if key > getitem_arr_tup(arr, base + zdtct__zny):
            sqmi__xnq = zdtct__zny + 1
        else:
            asqhg__thflh = zdtct__zny
    assert sqmi__xnq == asqhg__thflh
    return asqhg__thflh


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopRight(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    asqhg__thflh = 1
    sqmi__xnq = 0
    if key < getitem_arr_tup(arr, base + hint):
        mxlat__agg = hint + 1
        while asqhg__thflh < mxlat__agg and key < getitem_arr_tup(arr, base +
            hint - asqhg__thflh):
            sqmi__xnq = asqhg__thflh
            asqhg__thflh = (asqhg__thflh << 1) + 1
            if asqhg__thflh <= 0:
                asqhg__thflh = mxlat__agg
        if asqhg__thflh > mxlat__agg:
            asqhg__thflh = mxlat__agg
        tmp = sqmi__xnq
        sqmi__xnq = hint - asqhg__thflh
        asqhg__thflh = hint - tmp
    else:
        mxlat__agg = _len - hint
        while asqhg__thflh < mxlat__agg and key >= getitem_arr_tup(arr, 
            base + hint + asqhg__thflh):
            sqmi__xnq = asqhg__thflh
            asqhg__thflh = (asqhg__thflh << 1) + 1
            if asqhg__thflh <= 0:
                asqhg__thflh = mxlat__agg
        if asqhg__thflh > mxlat__agg:
            asqhg__thflh = mxlat__agg
        sqmi__xnq += hint
        asqhg__thflh += hint
    assert -1 <= sqmi__xnq and sqmi__xnq < asqhg__thflh and asqhg__thflh <= _len
    sqmi__xnq += 1
    while sqmi__xnq < asqhg__thflh:
        zdtct__zny = sqmi__xnq + (asqhg__thflh - sqmi__xnq >> 1)
        if key < getitem_arr_tup(arr, base + zdtct__zny):
            asqhg__thflh = zdtct__zny
        else:
            sqmi__xnq = zdtct__zny + 1
    assert sqmi__xnq == asqhg__thflh
    return asqhg__thflh


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
        rdna__gifhq = 0
        vdx__ooik = 0
        while True:
            assert len1 > 1 and len2 > 0
            if getitem_arr_tup(arr, cursor2) < getitem_arr_tup(tmp, cursor1):
                copyElement_tup(arr, cursor2, arr, dest)
                copyElement_tup(arr_data, cursor2, arr_data, dest)
                cursor2 += 1
                dest += 1
                vdx__ooik += 1
                rdna__gifhq = 0
                len2 -= 1
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor1, arr, dest)
                copyElement_tup(tmp_data, cursor1, arr_data, dest)
                cursor1 += 1
                dest += 1
                rdna__gifhq += 1
                vdx__ooik = 0
                len1 -= 1
                if len1 == 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            if not rdna__gifhq | vdx__ooik < minGallop:
                break
        while True:
            assert len1 > 1 and len2 > 0
            rdna__gifhq = gallopRight(getitem_arr_tup(arr, cursor2), tmp,
                cursor1, len1, 0)
            if rdna__gifhq != 0:
                copyRange_tup(tmp, cursor1, arr, dest, rdna__gifhq)
                copyRange_tup(tmp_data, cursor1, arr_data, dest, rdna__gifhq)
                dest += rdna__gifhq
                cursor1 += rdna__gifhq
                len1 -= rdna__gifhq
                if len1 <= 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor2, arr, dest)
            copyElement_tup(arr_data, cursor2, arr_data, dest)
            cursor2 += 1
            dest += 1
            len2 -= 1
            if len2 == 0:
                return len1, len2, cursor1, cursor2, dest, minGallop
            vdx__ooik = gallopLeft(getitem_arr_tup(tmp, cursor1), arr,
                cursor2, len2, 0)
            if vdx__ooik != 0:
                copyRange_tup(arr, cursor2, arr, dest, vdx__ooik)
                copyRange_tup(arr_data, cursor2, arr_data, dest, vdx__ooik)
                dest += vdx__ooik
                cursor2 += vdx__ooik
                len2 -= vdx__ooik
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
            if not rdna__gifhq >= MIN_GALLOP | vdx__ooik >= MIN_GALLOP:
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
        rdna__gifhq = 0
        vdx__ooik = 0
        while True:
            assert len1 > 0 and len2 > 1
            if getitem_arr_tup(tmp, cursor2) < getitem_arr_tup(arr, cursor1):
                copyElement_tup(arr, cursor1, arr, dest)
                copyElement_tup(arr_data, cursor1, arr_data, dest)
                cursor1 -= 1
                dest -= 1
                rdna__gifhq += 1
                vdx__ooik = 0
                len1 -= 1
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor2, arr, dest)
                copyElement_tup(tmp_data, cursor2, arr_data, dest)
                cursor2 -= 1
                dest -= 1
                vdx__ooik += 1
                rdna__gifhq = 0
                len2 -= 1
                if len2 == 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            if not rdna__gifhq | vdx__ooik < minGallop:
                break
        while True:
            assert len1 > 0 and len2 > 1
            rdna__gifhq = len1 - gallopRight(getitem_arr_tup(tmp, cursor2),
                arr, base1, len1, len1 - 1)
            if rdna__gifhq != 0:
                dest -= rdna__gifhq
                cursor1 -= rdna__gifhq
                len1 -= rdna__gifhq
                copyRange_tup(arr, cursor1 + 1, arr, dest + 1, rdna__gifhq)
                copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1,
                    rdna__gifhq)
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor2, arr, dest)
            copyElement_tup(tmp_data, cursor2, arr_data, dest)
            cursor2 -= 1
            dest -= 1
            len2 -= 1
            if len2 == 1:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            vdx__ooik = len2 - gallopLeft(getitem_arr_tup(arr, cursor1),
                tmp, 0, len2, len2 - 1)
            if vdx__ooik != 0:
                dest -= vdx__ooik
                cursor2 -= vdx__ooik
                len2 -= vdx__ooik
                copyRange_tup(tmp, cursor2 + 1, arr, dest + 1, vdx__ooik)
                copyRange_tup(tmp_data, cursor2 + 1, arr_data, dest + 1,
                    vdx__ooik)
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
            if not rdna__gifhq >= MIN_GALLOP | vdx__ooik >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, tmp, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def ensureCapacity(tmpLength, tmp, tmp_data, key_arrs, data, minCapacity):
    qtfmw__ayzon = len(key_arrs[0])
    if tmpLength < minCapacity:
        wqbix__uxel = minCapacity
        wqbix__uxel |= wqbix__uxel >> 1
        wqbix__uxel |= wqbix__uxel >> 2
        wqbix__uxel |= wqbix__uxel >> 4
        wqbix__uxel |= wqbix__uxel >> 8
        wqbix__uxel |= wqbix__uxel >> 16
        wqbix__uxel += 1
        if wqbix__uxel < 0:
            wqbix__uxel = minCapacity
        else:
            wqbix__uxel = min(wqbix__uxel, qtfmw__ayzon >> 1)
        tmp = alloc_arr_tup(wqbix__uxel, key_arrs)
        tmp_data = alloc_arr_tup(wqbix__uxel, data)
        tmpLength = wqbix__uxel
    return tmpLength, tmp, tmp_data


def swap_arrs(data, lo, hi):
    for arr in data:
        pfgoi__nljp = arr[lo]
        arr[lo] = arr[hi]
        arr[hi] = pfgoi__nljp


@overload(swap_arrs, no_unliteral=True)
def swap_arrs_overload(arr_tup, lo, hi):
    lzdas__jno = arr_tup.count
    pyfl__lnrj = 'def f(arr_tup, lo, hi):\n'
    for i in range(lzdas__jno):
        pyfl__lnrj += '  tmp_v_{} = arr_tup[{}][lo]\n'.format(i, i)
        pyfl__lnrj += '  arr_tup[{}][lo] = arr_tup[{}][hi]\n'.format(i, i)
        pyfl__lnrj += '  arr_tup[{}][hi] = tmp_v_{}\n'.format(i, i)
    pyfl__lnrj += '  return\n'
    lne__vir = {}
    exec(pyfl__lnrj, {}, lne__vir)
    fsm__nrejd = lne__vir['f']
    return fsm__nrejd


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyRange(src_arr, src_pos, dst_arr, dst_pos, n):
    dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


def copyRange_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


@overload(copyRange_tup, no_unliteral=True)
def copyRange_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    lzdas__jno = src_arr_tup.count
    assert lzdas__jno == dst_arr_tup.count
    pyfl__lnrj = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):\n'
    for i in range(lzdas__jno):
        pyfl__lnrj += (
            '  copyRange(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos, n)\n'
            .format(i, i))
    pyfl__lnrj += '  return\n'
    lne__vir = {}
    exec(pyfl__lnrj, {'copyRange': copyRange}, lne__vir)
    frp__nyvg = lne__vir['f']
    return frp__nyvg


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyElement(src_arr, src_pos, dst_arr, dst_pos):
    dst_arr[dst_pos] = src_arr[src_pos]


def copyElement_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos] = src_arr[src_pos]


@overload(copyElement_tup, no_unliteral=True)
def copyElement_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    lzdas__jno = src_arr_tup.count
    assert lzdas__jno == dst_arr_tup.count
    pyfl__lnrj = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos):\n'
    for i in range(lzdas__jno):
        pyfl__lnrj += (
            '  copyElement(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos)\n'
            .format(i, i))
    pyfl__lnrj += '  return\n'
    lne__vir = {}
    exec(pyfl__lnrj, {'copyElement': copyElement}, lne__vir)
    frp__nyvg = lne__vir['f']
    return frp__nyvg


def getitem_arr_tup(arr_tup, ind):
    qjl__rlju = [arr[ind] for arr in arr_tup]
    return tuple(qjl__rlju)


@overload(getitem_arr_tup, no_unliteral=True)
def getitem_arr_tup_overload(arr_tup, ind):
    lzdas__jno = arr_tup.count
    pyfl__lnrj = 'def f(arr_tup, ind):\n'
    pyfl__lnrj += '  return ({}{})\n'.format(','.join(['arr_tup[{}][ind]'.
        format(i) for i in range(lzdas__jno)]), ',' if lzdas__jno == 1 else '')
    lne__vir = {}
    exec(pyfl__lnrj, {}, lne__vir)
    uil__sxfrb = lne__vir['f']
    return uil__sxfrb


def setitem_arr_tup(arr_tup, ind, val_tup):
    for arr, jgogl__sjrp in zip(arr_tup, val_tup):
        arr[ind] = jgogl__sjrp


@overload(setitem_arr_tup, no_unliteral=True)
def setitem_arr_tup_overload(arr_tup, ind, val_tup):
    lzdas__jno = arr_tup.count
    pyfl__lnrj = 'def f(arr_tup, ind, val_tup):\n'
    for i in range(lzdas__jno):
        if isinstance(val_tup, numba.core.types.BaseTuple):
            pyfl__lnrj += '  arr_tup[{}][ind] = val_tup[{}]\n'.format(i, i)
        else:
            assert arr_tup.count == 1
            pyfl__lnrj += '  arr_tup[{}][ind] = val_tup\n'.format(i)
    pyfl__lnrj += '  return\n'
    lne__vir = {}
    exec(pyfl__lnrj, {}, lne__vir)
    uil__sxfrb = lne__vir['f']
    return uil__sxfrb


def test():
    import time
    zddy__ypyjl = time.time()
    clk__otgjt = np.ones(3)
    data = np.arange(3), np.ones(3)
    sort((clk__otgjt,), 0, 3, data)
    print('compile time', time.time() - zddy__ypyjl)
    n = 210000
    np.random.seed(2)
    data = np.arange(n), np.random.ranf(n)
    mns__cvbac = np.random.ranf(n)
    okr__yhsn = pd.DataFrame({'A': mns__cvbac, 'B': data[0], 'C': data[1]})
    zddy__ypyjl = time.time()
    cgl__amswj = okr__yhsn.sort_values('A', inplace=False)
    fxyt__hhbqd = time.time()
    sort((mns__cvbac,), 0, n, data)
    print('Bodo', time.time() - fxyt__hhbqd, 'Numpy', fxyt__hhbqd - zddy__ypyjl
        )
    np.testing.assert_almost_equal(data[0], cgl__amswj.B.values)
    np.testing.assert_almost_equal(data[1], cgl__amswj.C.values)


if __name__ == '__main__':
    test()
