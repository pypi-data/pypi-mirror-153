import numpy as np
import pandas as pd
import numba
from numba.extending import overload
from bodo.utils.utils import alloc_arr_tup
MIN_MERGE = 32


@numba.njit(no_cpython_wrapper=True, cache=True)
def sort(key_arrs, lo, hi, data):
    firf__gwm = hi - lo
    if firf__gwm < 2:
        return
    if firf__gwm < MIN_MERGE:
        ghb__dcx = countRunAndMakeAscending(key_arrs, lo, hi, data)
        binarySort(key_arrs, lo, hi, lo + ghb__dcx, data)
        return
    stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop = (
        init_sort_start(key_arrs, data))
    opdtz__wre = minRunLength(firf__gwm)
    while True:
        vviqm__oyn = countRunAndMakeAscending(key_arrs, lo, hi, data)
        if vviqm__oyn < opdtz__wre:
            bydqo__rgplp = firf__gwm if firf__gwm <= opdtz__wre else opdtz__wre
            binarySort(key_arrs, lo, lo + bydqo__rgplp, lo + vviqm__oyn, data)
            vviqm__oyn = bydqo__rgplp
        stackSize = pushRun(stackSize, runBase, runLen, lo, vviqm__oyn)
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeCollapse(
            stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
            tmp_data, minGallop)
        lo += vviqm__oyn
        firf__gwm -= vviqm__oyn
        if firf__gwm == 0:
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
        rtisy__qszc = getitem_arr_tup(key_arrs, start)
        thchb__nmcm = getitem_arr_tup(data, start)
        drylx__vpirz = lo
        mfsig__jqw = start
        assert drylx__vpirz <= mfsig__jqw
        while drylx__vpirz < mfsig__jqw:
            avijh__rirw = drylx__vpirz + mfsig__jqw >> 1
            if rtisy__qszc < getitem_arr_tup(key_arrs, avijh__rirw):
                mfsig__jqw = avijh__rirw
            else:
                drylx__vpirz = avijh__rirw + 1
        assert drylx__vpirz == mfsig__jqw
        n = start - drylx__vpirz
        copyRange_tup(key_arrs, drylx__vpirz, key_arrs, drylx__vpirz + 1, n)
        copyRange_tup(data, drylx__vpirz, data, drylx__vpirz + 1, n)
        setitem_arr_tup(key_arrs, drylx__vpirz, rtisy__qszc)
        setitem_arr_tup(data, drylx__vpirz, thchb__nmcm)
        start += 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def countRunAndMakeAscending(key_arrs, lo, hi, data):
    assert lo < hi
    cle__uyb = lo + 1
    if cle__uyb == hi:
        return 1
    if getitem_arr_tup(key_arrs, cle__uyb) < getitem_arr_tup(key_arrs, lo):
        cle__uyb += 1
        while cle__uyb < hi and getitem_arr_tup(key_arrs, cle__uyb
            ) < getitem_arr_tup(key_arrs, cle__uyb - 1):
            cle__uyb += 1
        reverseRange(key_arrs, lo, cle__uyb, data)
    else:
        cle__uyb += 1
        while cle__uyb < hi and getitem_arr_tup(key_arrs, cle__uyb
            ) >= getitem_arr_tup(key_arrs, cle__uyb - 1):
            cle__uyb += 1
    return cle__uyb - lo


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
    jusau__cohiw = 0
    while n >= MIN_MERGE:
        jusau__cohiw |= n & 1
        n >>= 1
    return n + jusau__cohiw


MIN_GALLOP = 7
INITIAL_TMP_STORAGE_LENGTH = 256


@numba.njit(no_cpython_wrapper=True, cache=True)
def init_sort_start(key_arrs, data):
    minGallop = MIN_GALLOP
    rhrq__pug = len(key_arrs[0])
    tmpLength = (rhrq__pug >> 1 if rhrq__pug < 2 *
        INITIAL_TMP_STORAGE_LENGTH else INITIAL_TMP_STORAGE_LENGTH)
    tmp = alloc_arr_tup(tmpLength, key_arrs)
    tmp_data = alloc_arr_tup(tmpLength, data)
    stackSize = 0
    ujeh__kvl = (5 if rhrq__pug < 120 else 10 if rhrq__pug < 1542 else 19 if
        rhrq__pug < 119151 else 40)
    runBase = np.empty(ujeh__kvl, np.int64)
    runLen = np.empty(ujeh__kvl, np.int64)
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
    qkcwr__sfoo = gallopRight(getitem_arr_tup(key_arrs, base2), key_arrs,
        base1, len1, 0)
    assert qkcwr__sfoo >= 0
    base1 += qkcwr__sfoo
    len1 -= qkcwr__sfoo
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
    hqpbf__wqyt = 0
    bafor__imhja = 1
    if key > getitem_arr_tup(arr, base + hint):
        ykl__foji = _len - hint
        while bafor__imhja < ykl__foji and key > getitem_arr_tup(arr, base +
            hint + bafor__imhja):
            hqpbf__wqyt = bafor__imhja
            bafor__imhja = (bafor__imhja << 1) + 1
            if bafor__imhja <= 0:
                bafor__imhja = ykl__foji
        if bafor__imhja > ykl__foji:
            bafor__imhja = ykl__foji
        hqpbf__wqyt += hint
        bafor__imhja += hint
    else:
        ykl__foji = hint + 1
        while bafor__imhja < ykl__foji and key <= getitem_arr_tup(arr, base +
            hint - bafor__imhja):
            hqpbf__wqyt = bafor__imhja
            bafor__imhja = (bafor__imhja << 1) + 1
            if bafor__imhja <= 0:
                bafor__imhja = ykl__foji
        if bafor__imhja > ykl__foji:
            bafor__imhja = ykl__foji
        tmp = hqpbf__wqyt
        hqpbf__wqyt = hint - bafor__imhja
        bafor__imhja = hint - tmp
    assert -1 <= hqpbf__wqyt and hqpbf__wqyt < bafor__imhja and bafor__imhja <= _len
    hqpbf__wqyt += 1
    while hqpbf__wqyt < bafor__imhja:
        kpzs__xvw = hqpbf__wqyt + (bafor__imhja - hqpbf__wqyt >> 1)
        if key > getitem_arr_tup(arr, base + kpzs__xvw):
            hqpbf__wqyt = kpzs__xvw + 1
        else:
            bafor__imhja = kpzs__xvw
    assert hqpbf__wqyt == bafor__imhja
    return bafor__imhja


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopRight(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    bafor__imhja = 1
    hqpbf__wqyt = 0
    if key < getitem_arr_tup(arr, base + hint):
        ykl__foji = hint + 1
        while bafor__imhja < ykl__foji and key < getitem_arr_tup(arr, base +
            hint - bafor__imhja):
            hqpbf__wqyt = bafor__imhja
            bafor__imhja = (bafor__imhja << 1) + 1
            if bafor__imhja <= 0:
                bafor__imhja = ykl__foji
        if bafor__imhja > ykl__foji:
            bafor__imhja = ykl__foji
        tmp = hqpbf__wqyt
        hqpbf__wqyt = hint - bafor__imhja
        bafor__imhja = hint - tmp
    else:
        ykl__foji = _len - hint
        while bafor__imhja < ykl__foji and key >= getitem_arr_tup(arr, base +
            hint + bafor__imhja):
            hqpbf__wqyt = bafor__imhja
            bafor__imhja = (bafor__imhja << 1) + 1
            if bafor__imhja <= 0:
                bafor__imhja = ykl__foji
        if bafor__imhja > ykl__foji:
            bafor__imhja = ykl__foji
        hqpbf__wqyt += hint
        bafor__imhja += hint
    assert -1 <= hqpbf__wqyt and hqpbf__wqyt < bafor__imhja and bafor__imhja <= _len
    hqpbf__wqyt += 1
    while hqpbf__wqyt < bafor__imhja:
        kpzs__xvw = hqpbf__wqyt + (bafor__imhja - hqpbf__wqyt >> 1)
        if key < getitem_arr_tup(arr, base + kpzs__xvw):
            bafor__imhja = kpzs__xvw
        else:
            hqpbf__wqyt = kpzs__xvw + 1
    assert hqpbf__wqyt == bafor__imhja
    return bafor__imhja


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
        tsmo__qbqa = 0
        slf__lin = 0
        while True:
            assert len1 > 1 and len2 > 0
            if getitem_arr_tup(arr, cursor2) < getitem_arr_tup(tmp, cursor1):
                copyElement_tup(arr, cursor2, arr, dest)
                copyElement_tup(arr_data, cursor2, arr_data, dest)
                cursor2 += 1
                dest += 1
                slf__lin += 1
                tsmo__qbqa = 0
                len2 -= 1
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor1, arr, dest)
                copyElement_tup(tmp_data, cursor1, arr_data, dest)
                cursor1 += 1
                dest += 1
                tsmo__qbqa += 1
                slf__lin = 0
                len1 -= 1
                if len1 == 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            if not tsmo__qbqa | slf__lin < minGallop:
                break
        while True:
            assert len1 > 1 and len2 > 0
            tsmo__qbqa = gallopRight(getitem_arr_tup(arr, cursor2), tmp,
                cursor1, len1, 0)
            if tsmo__qbqa != 0:
                copyRange_tup(tmp, cursor1, arr, dest, tsmo__qbqa)
                copyRange_tup(tmp_data, cursor1, arr_data, dest, tsmo__qbqa)
                dest += tsmo__qbqa
                cursor1 += tsmo__qbqa
                len1 -= tsmo__qbqa
                if len1 <= 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor2, arr, dest)
            copyElement_tup(arr_data, cursor2, arr_data, dest)
            cursor2 += 1
            dest += 1
            len2 -= 1
            if len2 == 0:
                return len1, len2, cursor1, cursor2, dest, minGallop
            slf__lin = gallopLeft(getitem_arr_tup(tmp, cursor1), arr,
                cursor2, len2, 0)
            if slf__lin != 0:
                copyRange_tup(arr, cursor2, arr, dest, slf__lin)
                copyRange_tup(arr_data, cursor2, arr_data, dest, slf__lin)
                dest += slf__lin
                cursor2 += slf__lin
                len2 -= slf__lin
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
            if not tsmo__qbqa >= MIN_GALLOP | slf__lin >= MIN_GALLOP:
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
        tsmo__qbqa = 0
        slf__lin = 0
        while True:
            assert len1 > 0 and len2 > 1
            if getitem_arr_tup(tmp, cursor2) < getitem_arr_tup(arr, cursor1):
                copyElement_tup(arr, cursor1, arr, dest)
                copyElement_tup(arr_data, cursor1, arr_data, dest)
                cursor1 -= 1
                dest -= 1
                tsmo__qbqa += 1
                slf__lin = 0
                len1 -= 1
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor2, arr, dest)
                copyElement_tup(tmp_data, cursor2, arr_data, dest)
                cursor2 -= 1
                dest -= 1
                slf__lin += 1
                tsmo__qbqa = 0
                len2 -= 1
                if len2 == 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            if not tsmo__qbqa | slf__lin < minGallop:
                break
        while True:
            assert len1 > 0 and len2 > 1
            tsmo__qbqa = len1 - gallopRight(getitem_arr_tup(tmp, cursor2),
                arr, base1, len1, len1 - 1)
            if tsmo__qbqa != 0:
                dest -= tsmo__qbqa
                cursor1 -= tsmo__qbqa
                len1 -= tsmo__qbqa
                copyRange_tup(arr, cursor1 + 1, arr, dest + 1, tsmo__qbqa)
                copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1,
                    tsmo__qbqa)
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor2, arr, dest)
            copyElement_tup(tmp_data, cursor2, arr_data, dest)
            cursor2 -= 1
            dest -= 1
            len2 -= 1
            if len2 == 1:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            slf__lin = len2 - gallopLeft(getitem_arr_tup(arr, cursor1), tmp,
                0, len2, len2 - 1)
            if slf__lin != 0:
                dest -= slf__lin
                cursor2 -= slf__lin
                len2 -= slf__lin
                copyRange_tup(tmp, cursor2 + 1, arr, dest + 1, slf__lin)
                copyRange_tup(tmp_data, cursor2 + 1, arr_data, dest + 1,
                    slf__lin)
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
            if not tsmo__qbqa >= MIN_GALLOP | slf__lin >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, tmp, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def ensureCapacity(tmpLength, tmp, tmp_data, key_arrs, data, minCapacity):
    njrtc__nbx = len(key_arrs[0])
    if tmpLength < minCapacity:
        jbuv__hqprg = minCapacity
        jbuv__hqprg |= jbuv__hqprg >> 1
        jbuv__hqprg |= jbuv__hqprg >> 2
        jbuv__hqprg |= jbuv__hqprg >> 4
        jbuv__hqprg |= jbuv__hqprg >> 8
        jbuv__hqprg |= jbuv__hqprg >> 16
        jbuv__hqprg += 1
        if jbuv__hqprg < 0:
            jbuv__hqprg = minCapacity
        else:
            jbuv__hqprg = min(jbuv__hqprg, njrtc__nbx >> 1)
        tmp = alloc_arr_tup(jbuv__hqprg, key_arrs)
        tmp_data = alloc_arr_tup(jbuv__hqprg, data)
        tmpLength = jbuv__hqprg
    return tmpLength, tmp, tmp_data


def swap_arrs(data, lo, hi):
    for arr in data:
        zmcrh__zqim = arr[lo]
        arr[lo] = arr[hi]
        arr[hi] = zmcrh__zqim


@overload(swap_arrs, no_unliteral=True)
def swap_arrs_overload(arr_tup, lo, hi):
    auj__opzve = arr_tup.count
    cwt__utuu = 'def f(arr_tup, lo, hi):\n'
    for i in range(auj__opzve):
        cwt__utuu += '  tmp_v_{} = arr_tup[{}][lo]\n'.format(i, i)
        cwt__utuu += '  arr_tup[{}][lo] = arr_tup[{}][hi]\n'.format(i, i)
        cwt__utuu += '  arr_tup[{}][hi] = tmp_v_{}\n'.format(i, i)
    cwt__utuu += '  return\n'
    cjpu__jjrq = {}
    exec(cwt__utuu, {}, cjpu__jjrq)
    obqn__pnjd = cjpu__jjrq['f']
    return obqn__pnjd


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyRange(src_arr, src_pos, dst_arr, dst_pos, n):
    dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


def copyRange_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


@overload(copyRange_tup, no_unliteral=True)
def copyRange_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    auj__opzve = src_arr_tup.count
    assert auj__opzve == dst_arr_tup.count
    cwt__utuu = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):\n'
    for i in range(auj__opzve):
        cwt__utuu += (
            '  copyRange(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos, n)\n'
            .format(i, i))
    cwt__utuu += '  return\n'
    cjpu__jjrq = {}
    exec(cwt__utuu, {'copyRange': copyRange}, cjpu__jjrq)
    hhtoh__hdvoz = cjpu__jjrq['f']
    return hhtoh__hdvoz


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyElement(src_arr, src_pos, dst_arr, dst_pos):
    dst_arr[dst_pos] = src_arr[src_pos]


def copyElement_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos] = src_arr[src_pos]


@overload(copyElement_tup, no_unliteral=True)
def copyElement_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    auj__opzve = src_arr_tup.count
    assert auj__opzve == dst_arr_tup.count
    cwt__utuu = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos):\n'
    for i in range(auj__opzve):
        cwt__utuu += (
            '  copyElement(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos)\n'
            .format(i, i))
    cwt__utuu += '  return\n'
    cjpu__jjrq = {}
    exec(cwt__utuu, {'copyElement': copyElement}, cjpu__jjrq)
    hhtoh__hdvoz = cjpu__jjrq['f']
    return hhtoh__hdvoz


def getitem_arr_tup(arr_tup, ind):
    rhshx__mdxy = [arr[ind] for arr in arr_tup]
    return tuple(rhshx__mdxy)


@overload(getitem_arr_tup, no_unliteral=True)
def getitem_arr_tup_overload(arr_tup, ind):
    auj__opzve = arr_tup.count
    cwt__utuu = 'def f(arr_tup, ind):\n'
    cwt__utuu += '  return ({}{})\n'.format(','.join(['arr_tup[{}][ind]'.
        format(i) for i in range(auj__opzve)]), ',' if auj__opzve == 1 else '')
    cjpu__jjrq = {}
    exec(cwt__utuu, {}, cjpu__jjrq)
    mck__xsat = cjpu__jjrq['f']
    return mck__xsat


def setitem_arr_tup(arr_tup, ind, val_tup):
    for arr, nuqr__hrdq in zip(arr_tup, val_tup):
        arr[ind] = nuqr__hrdq


@overload(setitem_arr_tup, no_unliteral=True)
def setitem_arr_tup_overload(arr_tup, ind, val_tup):
    auj__opzve = arr_tup.count
    cwt__utuu = 'def f(arr_tup, ind, val_tup):\n'
    for i in range(auj__opzve):
        if isinstance(val_tup, numba.core.types.BaseTuple):
            cwt__utuu += '  arr_tup[{}][ind] = val_tup[{}]\n'.format(i, i)
        else:
            assert arr_tup.count == 1
            cwt__utuu += '  arr_tup[{}][ind] = val_tup\n'.format(i)
    cwt__utuu += '  return\n'
    cjpu__jjrq = {}
    exec(cwt__utuu, {}, cjpu__jjrq)
    mck__xsat = cjpu__jjrq['f']
    return mck__xsat


def test():
    import time
    afit__ngkk = time.time()
    vual__csd = np.ones(3)
    data = np.arange(3), np.ones(3)
    sort((vual__csd,), 0, 3, data)
    print('compile time', time.time() - afit__ngkk)
    n = 210000
    np.random.seed(2)
    data = np.arange(n), np.random.ranf(n)
    qyev__tpt = np.random.ranf(n)
    bwxn__shci = pd.DataFrame({'A': qyev__tpt, 'B': data[0], 'C': data[1]})
    afit__ngkk = time.time()
    wrqef__gju = bwxn__shci.sort_values('A', inplace=False)
    xaqk__akels = time.time()
    sort((qyev__tpt,), 0, n, data)
    print('Bodo', time.time() - xaqk__akels, 'Numpy', xaqk__akels - afit__ngkk)
    np.testing.assert_almost_equal(data[0], wrqef__gju.B.values)
    np.testing.assert_almost_equal(data[1], wrqef__gju.C.values)


if __name__ == '__main__':
    test()
