import numpy as np
import pandas as pd
import numba
from numba.extending import overload
from bodo.utils.utils import alloc_arr_tup
MIN_MERGE = 32


@numba.njit(no_cpython_wrapper=True, cache=True)
def sort(key_arrs, lo, hi, data):
    eluo__ajxoh = hi - lo
    if eluo__ajxoh < 2:
        return
    if eluo__ajxoh < MIN_MERGE:
        bdkf__frxm = countRunAndMakeAscending(key_arrs, lo, hi, data)
        binarySort(key_arrs, lo, hi, lo + bdkf__frxm, data)
        return
    stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop = (
        init_sort_start(key_arrs, data))
    uio__mhy = minRunLength(eluo__ajxoh)
    while True:
        aiivq__ulfnj = countRunAndMakeAscending(key_arrs, lo, hi, data)
        if aiivq__ulfnj < uio__mhy:
            ctqzr__vbi = eluo__ajxoh if eluo__ajxoh <= uio__mhy else uio__mhy
            binarySort(key_arrs, lo, lo + ctqzr__vbi, lo + aiivq__ulfnj, data)
            aiivq__ulfnj = ctqzr__vbi
        stackSize = pushRun(stackSize, runBase, runLen, lo, aiivq__ulfnj)
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeCollapse(
            stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
            tmp_data, minGallop)
        lo += aiivq__ulfnj
        eluo__ajxoh -= aiivq__ulfnj
        if eluo__ajxoh == 0:
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
        fuls__uvkfo = getitem_arr_tup(key_arrs, start)
        ivue__uwv = getitem_arr_tup(data, start)
        hzh__mpu = lo
        asug__ola = start
        assert hzh__mpu <= asug__ola
        while hzh__mpu < asug__ola:
            ewao__qspd = hzh__mpu + asug__ola >> 1
            if fuls__uvkfo < getitem_arr_tup(key_arrs, ewao__qspd):
                asug__ola = ewao__qspd
            else:
                hzh__mpu = ewao__qspd + 1
        assert hzh__mpu == asug__ola
        n = start - hzh__mpu
        copyRange_tup(key_arrs, hzh__mpu, key_arrs, hzh__mpu + 1, n)
        copyRange_tup(data, hzh__mpu, data, hzh__mpu + 1, n)
        setitem_arr_tup(key_arrs, hzh__mpu, fuls__uvkfo)
        setitem_arr_tup(data, hzh__mpu, ivue__uwv)
        start += 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def countRunAndMakeAscending(key_arrs, lo, hi, data):
    assert lo < hi
    fnsq__czk = lo + 1
    if fnsq__czk == hi:
        return 1
    if getitem_arr_tup(key_arrs, fnsq__czk) < getitem_arr_tup(key_arrs, lo):
        fnsq__czk += 1
        while fnsq__czk < hi and getitem_arr_tup(key_arrs, fnsq__czk
            ) < getitem_arr_tup(key_arrs, fnsq__czk - 1):
            fnsq__czk += 1
        reverseRange(key_arrs, lo, fnsq__czk, data)
    else:
        fnsq__czk += 1
        while fnsq__czk < hi and getitem_arr_tup(key_arrs, fnsq__czk
            ) >= getitem_arr_tup(key_arrs, fnsq__czk - 1):
            fnsq__czk += 1
    return fnsq__czk - lo


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
    hrwkq__jyfr = 0
    while n >= MIN_MERGE:
        hrwkq__jyfr |= n & 1
        n >>= 1
    return n + hrwkq__jyfr


MIN_GALLOP = 7
INITIAL_TMP_STORAGE_LENGTH = 256


@numba.njit(no_cpython_wrapper=True, cache=True)
def init_sort_start(key_arrs, data):
    minGallop = MIN_GALLOP
    ueiy__yqw = len(key_arrs[0])
    tmpLength = (ueiy__yqw >> 1 if ueiy__yqw < 2 *
        INITIAL_TMP_STORAGE_LENGTH else INITIAL_TMP_STORAGE_LENGTH)
    tmp = alloc_arr_tup(tmpLength, key_arrs)
    tmp_data = alloc_arr_tup(tmpLength, data)
    stackSize = 0
    ovn__vuqhg = (5 if ueiy__yqw < 120 else 10 if ueiy__yqw < 1542 else 19 if
        ueiy__yqw < 119151 else 40)
    runBase = np.empty(ovn__vuqhg, np.int64)
    runLen = np.empty(ovn__vuqhg, np.int64)
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
    yzx__hza = gallopRight(getitem_arr_tup(key_arrs, base2), key_arrs,
        base1, len1, 0)
    assert yzx__hza >= 0
    base1 += yzx__hza
    len1 -= yzx__hza
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
    phz__omgyw = 0
    htrfz__vbf = 1
    if key > getitem_arr_tup(arr, base + hint):
        uvdhw__nctu = _len - hint
        while htrfz__vbf < uvdhw__nctu and key > getitem_arr_tup(arr, base +
            hint + htrfz__vbf):
            phz__omgyw = htrfz__vbf
            htrfz__vbf = (htrfz__vbf << 1) + 1
            if htrfz__vbf <= 0:
                htrfz__vbf = uvdhw__nctu
        if htrfz__vbf > uvdhw__nctu:
            htrfz__vbf = uvdhw__nctu
        phz__omgyw += hint
        htrfz__vbf += hint
    else:
        uvdhw__nctu = hint + 1
        while htrfz__vbf < uvdhw__nctu and key <= getitem_arr_tup(arr, base +
            hint - htrfz__vbf):
            phz__omgyw = htrfz__vbf
            htrfz__vbf = (htrfz__vbf << 1) + 1
            if htrfz__vbf <= 0:
                htrfz__vbf = uvdhw__nctu
        if htrfz__vbf > uvdhw__nctu:
            htrfz__vbf = uvdhw__nctu
        tmp = phz__omgyw
        phz__omgyw = hint - htrfz__vbf
        htrfz__vbf = hint - tmp
    assert -1 <= phz__omgyw and phz__omgyw < htrfz__vbf and htrfz__vbf <= _len
    phz__omgyw += 1
    while phz__omgyw < htrfz__vbf:
        xlzic__pfs = phz__omgyw + (htrfz__vbf - phz__omgyw >> 1)
        if key > getitem_arr_tup(arr, base + xlzic__pfs):
            phz__omgyw = xlzic__pfs + 1
        else:
            htrfz__vbf = xlzic__pfs
    assert phz__omgyw == htrfz__vbf
    return htrfz__vbf


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopRight(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    htrfz__vbf = 1
    phz__omgyw = 0
    if key < getitem_arr_tup(arr, base + hint):
        uvdhw__nctu = hint + 1
        while htrfz__vbf < uvdhw__nctu and key < getitem_arr_tup(arr, base +
            hint - htrfz__vbf):
            phz__omgyw = htrfz__vbf
            htrfz__vbf = (htrfz__vbf << 1) + 1
            if htrfz__vbf <= 0:
                htrfz__vbf = uvdhw__nctu
        if htrfz__vbf > uvdhw__nctu:
            htrfz__vbf = uvdhw__nctu
        tmp = phz__omgyw
        phz__omgyw = hint - htrfz__vbf
        htrfz__vbf = hint - tmp
    else:
        uvdhw__nctu = _len - hint
        while htrfz__vbf < uvdhw__nctu and key >= getitem_arr_tup(arr, base +
            hint + htrfz__vbf):
            phz__omgyw = htrfz__vbf
            htrfz__vbf = (htrfz__vbf << 1) + 1
            if htrfz__vbf <= 0:
                htrfz__vbf = uvdhw__nctu
        if htrfz__vbf > uvdhw__nctu:
            htrfz__vbf = uvdhw__nctu
        phz__omgyw += hint
        htrfz__vbf += hint
    assert -1 <= phz__omgyw and phz__omgyw < htrfz__vbf and htrfz__vbf <= _len
    phz__omgyw += 1
    while phz__omgyw < htrfz__vbf:
        xlzic__pfs = phz__omgyw + (htrfz__vbf - phz__omgyw >> 1)
        if key < getitem_arr_tup(arr, base + xlzic__pfs):
            htrfz__vbf = xlzic__pfs
        else:
            phz__omgyw = xlzic__pfs + 1
    assert phz__omgyw == htrfz__vbf
    return htrfz__vbf


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
        bxcvz__vavj = 0
        pgqj__hteg = 0
        while True:
            assert len1 > 1 and len2 > 0
            if getitem_arr_tup(arr, cursor2) < getitem_arr_tup(tmp, cursor1):
                copyElement_tup(arr, cursor2, arr, dest)
                copyElement_tup(arr_data, cursor2, arr_data, dest)
                cursor2 += 1
                dest += 1
                pgqj__hteg += 1
                bxcvz__vavj = 0
                len2 -= 1
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor1, arr, dest)
                copyElement_tup(tmp_data, cursor1, arr_data, dest)
                cursor1 += 1
                dest += 1
                bxcvz__vavj += 1
                pgqj__hteg = 0
                len1 -= 1
                if len1 == 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            if not bxcvz__vavj | pgqj__hteg < minGallop:
                break
        while True:
            assert len1 > 1 and len2 > 0
            bxcvz__vavj = gallopRight(getitem_arr_tup(arr, cursor2), tmp,
                cursor1, len1, 0)
            if bxcvz__vavj != 0:
                copyRange_tup(tmp, cursor1, arr, dest, bxcvz__vavj)
                copyRange_tup(tmp_data, cursor1, arr_data, dest, bxcvz__vavj)
                dest += bxcvz__vavj
                cursor1 += bxcvz__vavj
                len1 -= bxcvz__vavj
                if len1 <= 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor2, arr, dest)
            copyElement_tup(arr_data, cursor2, arr_data, dest)
            cursor2 += 1
            dest += 1
            len2 -= 1
            if len2 == 0:
                return len1, len2, cursor1, cursor2, dest, minGallop
            pgqj__hteg = gallopLeft(getitem_arr_tup(tmp, cursor1), arr,
                cursor2, len2, 0)
            if pgqj__hteg != 0:
                copyRange_tup(arr, cursor2, arr, dest, pgqj__hteg)
                copyRange_tup(arr_data, cursor2, arr_data, dest, pgqj__hteg)
                dest += pgqj__hteg
                cursor2 += pgqj__hteg
                len2 -= pgqj__hteg
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
            if not bxcvz__vavj >= MIN_GALLOP | pgqj__hteg >= MIN_GALLOP:
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
        bxcvz__vavj = 0
        pgqj__hteg = 0
        while True:
            assert len1 > 0 and len2 > 1
            if getitem_arr_tup(tmp, cursor2) < getitem_arr_tup(arr, cursor1):
                copyElement_tup(arr, cursor1, arr, dest)
                copyElement_tup(arr_data, cursor1, arr_data, dest)
                cursor1 -= 1
                dest -= 1
                bxcvz__vavj += 1
                pgqj__hteg = 0
                len1 -= 1
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor2, arr, dest)
                copyElement_tup(tmp_data, cursor2, arr_data, dest)
                cursor2 -= 1
                dest -= 1
                pgqj__hteg += 1
                bxcvz__vavj = 0
                len2 -= 1
                if len2 == 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            if not bxcvz__vavj | pgqj__hteg < minGallop:
                break
        while True:
            assert len1 > 0 and len2 > 1
            bxcvz__vavj = len1 - gallopRight(getitem_arr_tup(tmp, cursor2),
                arr, base1, len1, len1 - 1)
            if bxcvz__vavj != 0:
                dest -= bxcvz__vavj
                cursor1 -= bxcvz__vavj
                len1 -= bxcvz__vavj
                copyRange_tup(arr, cursor1 + 1, arr, dest + 1, bxcvz__vavj)
                copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1,
                    bxcvz__vavj)
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor2, arr, dest)
            copyElement_tup(tmp_data, cursor2, arr_data, dest)
            cursor2 -= 1
            dest -= 1
            len2 -= 1
            if len2 == 1:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            pgqj__hteg = len2 - gallopLeft(getitem_arr_tup(arr, cursor1),
                tmp, 0, len2, len2 - 1)
            if pgqj__hteg != 0:
                dest -= pgqj__hteg
                cursor2 -= pgqj__hteg
                len2 -= pgqj__hteg
                copyRange_tup(tmp, cursor2 + 1, arr, dest + 1, pgqj__hteg)
                copyRange_tup(tmp_data, cursor2 + 1, arr_data, dest + 1,
                    pgqj__hteg)
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
            if not bxcvz__vavj >= MIN_GALLOP | pgqj__hteg >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, tmp, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def ensureCapacity(tmpLength, tmp, tmp_data, key_arrs, data, minCapacity):
    wqj__pym = len(key_arrs[0])
    if tmpLength < minCapacity:
        bpsa__giq = minCapacity
        bpsa__giq |= bpsa__giq >> 1
        bpsa__giq |= bpsa__giq >> 2
        bpsa__giq |= bpsa__giq >> 4
        bpsa__giq |= bpsa__giq >> 8
        bpsa__giq |= bpsa__giq >> 16
        bpsa__giq += 1
        if bpsa__giq < 0:
            bpsa__giq = minCapacity
        else:
            bpsa__giq = min(bpsa__giq, wqj__pym >> 1)
        tmp = alloc_arr_tup(bpsa__giq, key_arrs)
        tmp_data = alloc_arr_tup(bpsa__giq, data)
        tmpLength = bpsa__giq
    return tmpLength, tmp, tmp_data


def swap_arrs(data, lo, hi):
    for arr in data:
        ncvbw__fsus = arr[lo]
        arr[lo] = arr[hi]
        arr[hi] = ncvbw__fsus


@overload(swap_arrs, no_unliteral=True)
def swap_arrs_overload(arr_tup, lo, hi):
    uhr__pcjvs = arr_tup.count
    azcyp__fascx = 'def f(arr_tup, lo, hi):\n'
    for i in range(uhr__pcjvs):
        azcyp__fascx += '  tmp_v_{} = arr_tup[{}][lo]\n'.format(i, i)
        azcyp__fascx += '  arr_tup[{}][lo] = arr_tup[{}][hi]\n'.format(i, i)
        azcyp__fascx += '  arr_tup[{}][hi] = tmp_v_{}\n'.format(i, i)
    azcyp__fascx += '  return\n'
    jra__himkb = {}
    exec(azcyp__fascx, {}, jra__himkb)
    gsvm__emz = jra__himkb['f']
    return gsvm__emz


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyRange(src_arr, src_pos, dst_arr, dst_pos, n):
    dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


def copyRange_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


@overload(copyRange_tup, no_unliteral=True)
def copyRange_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    uhr__pcjvs = src_arr_tup.count
    assert uhr__pcjvs == dst_arr_tup.count
    azcyp__fascx = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):\n'
    for i in range(uhr__pcjvs):
        azcyp__fascx += (
            '  copyRange(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos, n)\n'
            .format(i, i))
    azcyp__fascx += '  return\n'
    jra__himkb = {}
    exec(azcyp__fascx, {'copyRange': copyRange}, jra__himkb)
    rxyjg__ucjpu = jra__himkb['f']
    return rxyjg__ucjpu


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyElement(src_arr, src_pos, dst_arr, dst_pos):
    dst_arr[dst_pos] = src_arr[src_pos]


def copyElement_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos] = src_arr[src_pos]


@overload(copyElement_tup, no_unliteral=True)
def copyElement_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    uhr__pcjvs = src_arr_tup.count
    assert uhr__pcjvs == dst_arr_tup.count
    azcyp__fascx = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos):\n'
    for i in range(uhr__pcjvs):
        azcyp__fascx += (
            '  copyElement(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos)\n'
            .format(i, i))
    azcyp__fascx += '  return\n'
    jra__himkb = {}
    exec(azcyp__fascx, {'copyElement': copyElement}, jra__himkb)
    rxyjg__ucjpu = jra__himkb['f']
    return rxyjg__ucjpu


def getitem_arr_tup(arr_tup, ind):
    mvf__lygii = [arr[ind] for arr in arr_tup]
    return tuple(mvf__lygii)


@overload(getitem_arr_tup, no_unliteral=True)
def getitem_arr_tup_overload(arr_tup, ind):
    uhr__pcjvs = arr_tup.count
    azcyp__fascx = 'def f(arr_tup, ind):\n'
    azcyp__fascx += '  return ({}{})\n'.format(','.join(['arr_tup[{}][ind]'
        .format(i) for i in range(uhr__pcjvs)]), ',' if uhr__pcjvs == 1 else ''
        )
    jra__himkb = {}
    exec(azcyp__fascx, {}, jra__himkb)
    dld__qbnxs = jra__himkb['f']
    return dld__qbnxs


def setitem_arr_tup(arr_tup, ind, val_tup):
    for arr, oxvk__bthfd in zip(arr_tup, val_tup):
        arr[ind] = oxvk__bthfd


@overload(setitem_arr_tup, no_unliteral=True)
def setitem_arr_tup_overload(arr_tup, ind, val_tup):
    uhr__pcjvs = arr_tup.count
    azcyp__fascx = 'def f(arr_tup, ind, val_tup):\n'
    for i in range(uhr__pcjvs):
        if isinstance(val_tup, numba.core.types.BaseTuple):
            azcyp__fascx += '  arr_tup[{}][ind] = val_tup[{}]\n'.format(i, i)
        else:
            assert arr_tup.count == 1
            azcyp__fascx += '  arr_tup[{}][ind] = val_tup\n'.format(i)
    azcyp__fascx += '  return\n'
    jra__himkb = {}
    exec(azcyp__fascx, {}, jra__himkb)
    dld__qbnxs = jra__himkb['f']
    return dld__qbnxs


def test():
    import time
    fdyk__dzk = time.time()
    qeeky__yre = np.ones(3)
    data = np.arange(3), np.ones(3)
    sort((qeeky__yre,), 0, 3, data)
    print('compile time', time.time() - fdyk__dzk)
    n = 210000
    np.random.seed(2)
    data = np.arange(n), np.random.ranf(n)
    ghhnx__jcny = np.random.ranf(n)
    jfm__imuxp = pd.DataFrame({'A': ghhnx__jcny, 'B': data[0], 'C': data[1]})
    fdyk__dzk = time.time()
    uyfmq__vew = jfm__imuxp.sort_values('A', inplace=False)
    mmisx__pah = time.time()
    sort((ghhnx__jcny,), 0, n, data)
    print('Bodo', time.time() - mmisx__pah, 'Numpy', mmisx__pah - fdyk__dzk)
    np.testing.assert_almost_equal(data[0], uyfmq__vew.B.values)
    np.testing.assert_almost_equal(data[1], uyfmq__vew.C.values)


if __name__ == '__main__':
    test()
