from random import randint
import sys
import math
import time

data = []
NUM = int(sys.argv[1]) 
choose = int(sys.argv[2])

def generateNumber():
    data.clear()
    for i in range(NUM):
        data.append(randint(0, 2 ** 32 - 1))    

def insertionsort(t, l, r): #! [l, r)
    auxiliary = 0
    for i in range(l + 1, r):
        if t[i] < t[i - 1]:
            auxiliary = t[i]
            j = i - 1
            while j >= l and t[j] > auxiliary:
                t[j + 1] = t[j]
                j -= 1
            t[j + 1] = auxiliary

def shellsort(t, l, r): #! [l, r)
    step = r - l
    while step > 1:
        auxiliary = 0
        step //= 2
        for i in range(l + step, r):
            if t[i] < t[i - step]:
                auxiliary = t[i]
                j = i - step
                while j >= l and t[j] > auxiliary:
                    t[j + step] = t[j]
                    j -= step
                t[j + step] = auxiliary

def quicksort(t, l, r): # ! [l, r]
    if l >= r: #! learn from it!
        return 
    k = t[r]
    x = l
    y = r
    while l < r:
        while t[l] < k and l < r:
            l += 1
        if l < r:
            t[r] = t[l]
            r -= 1
        while t[r] > k and l < r:
            r -= 1
        if l < r:
            t[l] = t[r]
            l += 1
    t[l] = k
    quicksort(t, x, l - 1)
    quicksort(t, l + 1, y)

def mergesort(t, l, r): # ! [l, r)
    def merge(l, mid, r): #! [l, mid - 1] [mid, r - 1]
        x, y = l, mid
        ls = []
        while x < mid and y < r:
            if t[x] < t[y]:
                ls.append(t[x])
                x += 1
            else:
                ls.append(t[y])
                y += 1
        while x < mid:
            ls.append(t[x])
            x += 1
        while y < r:
            ls.append(t[y])
            y += 1
        for i in range(l, r):
            t[i] = ls[i - l]
    if r - l <= 1:
        return
    mid = (l + r) // 2
    mergesort(t, l, mid)
    mergesort(t, mid, r)
    merge(l, mid, r)

def radixsort(t, l, r): # ! [l, r)
    def getNumber(d, i):
        d >>= 8 * (i - 1)
        d &= 255
        return d
    ls = []
    for i in range(1, 5):
        ls.clear()
        for k in range(256):
            ls.append(0)
        for j in range(l, r):
            ls[getNumber(t[j], i)] += 1
        for k in range(1, 256):
            ls[k] += ls[k - 1]
        tmp = [0 for k in range(len(t))]
        for k in range(len(t) - 1, -1, -1):
            tmp[ls[getNumber(t[k], i)] - 1] = t[k]
            ls[getNumber(t[k], i)] -= 1
        for i in range(len(t)):
            t[i] = tmp[i]

def timsort(t, l, r): # ! [l, r)
    MinMerge = 32
    MinGallop = 7
    minGallop = MinGallop
    runBase = []
    runLen = []
    tmpBase = 0
    tmp = []
    def countRunAndMakeAscending(lo, hi):
        assert lo < hi
        runHi = lo + 1
        if runHi == hi:
            return 1
        
        if t[runHi] < t[lo]:
            runHi += 1
            while runHi < hi and t[runHi] < t[runHi - 1]:
                runHi += 1
            reverseRange(lo, runHi)
        else:
            runHi += 1
            while runHi < hi and t[runHi] >= t[runHi - 1]:
                runHi += 1
        return runHi - lo
    def reverseRange(lo, hi):
        hi -= 1
        while lo < hi:
            num = t[lo]
            t[lo] = t[hi]
            lo += 1
            t[hi] = num
            hi -= 1
    def binarySort(lo, hi, start):
        assert lo <= start and start <= hi
        if start == lo:
            start += 1
        
        while start < hi:
            pivot = t[start]
            left = lo
            right = start
            assert left <= right
            while left < right:
                mid = (left + right) // 2
                if pivot < t[mid]:
                    right = mid
                else:
                    left = mid + 1
            assert left == right
            n = start - left
            for i in range(start, right, -1):
                t[i] = t[i - 1]
            t[right] = pivot
            start += 1
    def minRunLength(n):
        assert n >= 0
        nonlocal MinMerge
        r = 0
        while n >= MinMerge:
            r |= (n & 1)
            n >>= 1
        return n + r
    def pushRun(Base, Len):
        runBase.append(Base)
        runLen.append(Len)
    def mergeCollapse():
        while len(runBase) > 1:
            n = len(runBase) - 2
            if n > 0 and runLen[n - 1] <= runLen[n] + runLen[n + 1]:
                if runLen[n - 1] < runLen[n + 1]:
                    n -= 1
                mergeAt(n)
            elif runLen[n] <= runLen[n + 1]:
                mergeAt(n)
            else:
                break
    def mergeAt(i):
        assert len(runLen) >= 2
        assert i >= 0
        assert i == len(runLen) - 2 or i == len(runLen) - 3
        base1 = runBase[i]
        len1 = runLen[i]
        base2 = runBase[i + 1]
        len2 = runLen[i + 1]
        assert len1 > 0 and len2 > 0
        assert base1 + len1 == base2
        runLen[i] = len1 + len2
        if i == len(runLen) - 3:
            runBase[i + 1] = runBase[i + 2]
            runLen[i + 1] = runLen[i + 2]
        runBase.pop()
        runLen.pop()
        k = gallopRight(t[base2], t, base1, len1, 0)
        base1 += k
        len1 -= k
        if len1 == 0:
            return
        len2 = gallopLeft(t[base1 + len1  - 1], t, base2, len2, len2 - 1)
        assert len2 >= 0
        if len2 == 0:
            return
        if len1 <= len2:
            mergeLo(base1, len1, base2, len2)
        else:
            mergeHi(base1, len1, base2, len2)

    def gallopRight(key, t, base, len, hint):
        assert len > 0 and hint >= 0 and hint < len
        ofs = 1
        lastOfs = 0
        if key < t[base + hint]:
            maxOfs = hint + 1
            while ofs < maxOfs and key < t[base + hint - ofs]:
                lastOfs = ofs
                ofs = (ofs << 1) + 1
                if ofs <= 0: #! this maybe useless
                    print("how")
                    ofs = maxOfs
            if ofs > maxOfs:
                ofs = maxOfs
            tmp = lastOfs
            lastOfs = hint - ofs
            ofs = hint - tmp
        else:
            maxOfs = len - hint
            while ofs < maxOfs and key >= t[base + hint + ofs]:
                lastOfs = ofs
                ofs = (ofs << 1) + 1
                if ofs <= 0:  #! this maybe useless
                    print("how")
                    ofs = maxOfs
            if ofs > maxOfs:
                ofs = maxOfs
            lastOfs += hint
            ofs += hint
        assert -1 <= lastOfs and lastOfs < ofs and ofs <= len
        lastOfs += 1
        while lastOfs < ofs:
            m = lastOfs + ((ofs - lastOfs) // 2)
            if key < t[base + m]:
                ofs = m
            else:
                lastOfs = m + 1
        assert lastOfs == ofs
        return ofs

    def gallopLeft(key, t, base, len, hint):
        lastOfs = 0
        ofs = 1
        if key > t[base + hint]:
            maxOfs = len - hint
            while ofs < maxOfs and key > t[base + hint + ofs]:
                lastOfs = ofs
                ofs = (ofs << 1) + 1
                if ofs <= 0: # ! this maybe useless
                    ofs = maxOfs
            if ofs > maxOfs:
                ofs = maxOfs
            lastOfs += hint
            ofs += hint
        else:
            maxOfs = hint + 1
            while ofs < maxOfs and key <= t[base + hint - ofs]:
                lastOfs = ofs
                ofs = (ofs << 1) + 1
                if ofs <= 0: #! this maybe useless
                    ofs = maxOfs
            if ofs > maxOfs:
                ofs = maxOfs
            tmp = lastOfs
            lastOfs = hint - ofs
            ofs = hint - tmp
        assert -1 <= lastOfs and lastOfs < ofs and ofs <= len
        lastOfs += 1
        while lastOfs  < ofs:
            m = lastOfs + ((ofs - lastOfs) // 2)
            if key > t[base + m]:
                lastOfs = m + 1
            else:
                ofs = m
        assert lastOfs == ofs
        return ofs

    def mergeLo(base1, len1, base2, len2):
        nonlocal minGallop, MinGallop, tmpBase, tmp, runBase, runLen
        assert len1 > 0 and len2 > 0 and base1 + len1 == base2
        cursor1 = tmpBase
        cursor2 = base2
        dest = base1
        tmp.clear()
        for i in range(base1, base1 + len1):
            tmp.append(t[i])
        t[dest] = t[cursor2]
        dest += 1
        cursor2 += 1
        len2 -= 1
        if len2 == 0: # ! right, can add tmp.clear() maybe
            for i in range(cursor1, cursor1 + len1):
                t[dest] = tmp[i]
                dest += 1
            return
        if len1 == 1: # ! right
            for i in range(cursor2, cursor2 + len2):
                t[dest] = t[i]
                dest += 1
            t[dest] = tmp[cursor1]
            return
        try:
            while True:
                count1 = 0
                count2 = 0
                while True:
                    assert len1 > 1 and len2 > 0
                    if t[cursor2] < tmp[cursor1]:
                        t[dest] = t[cursor2]
                        dest += 1
                        cursor2 += 1
                        count2 += 1
                        count1 = 0
                        len2 -= 1
                        if len2 == 0:
                            raise Getoutofloop()
                    else:
                        t[dest] = tmp[cursor1]
                        dest += 1
                        cursor1 += 1
                        count1 += 1
                        count2 = 0
                        len1 -= 1
                        if len1 == 1:
                            raise Getoutofloop()
                    if not ((count1 | count2) < minGallop):
                        break
                while True:
                    assert len1 > 1 and len2 > 0
                    count1 = gallopRight(t[cursor2], tmp, cursor1, len1, 0)
                    if count1 != 0:
                        for i in range(cursor1, cursor1 + count1):
                            t[dest] = tmp[i]
                            dest += 1
                        cursor1 += count1
                        len1 -= count1
                        if len1 <= 1:
                            raise Getoutofloop()
                    t[dest] = t[cursor2]
                    dest += 1
                    cursor2 += 1
                    len2 -= 1
                    if len2 == 0:
                        raise Getoutofloop()
                    count2 = gallopLeft(tmp[cursor1], t, cursor2, len2, 0)
                    if count2 != 0:
                        for i in range(cursor2, cursor2 + count2):
                            t[dest] = t[i]
                            dest += 1
                        cursor2 += count2
                        len2 -= count2
                        if len2 == 0:
                            raise Getoutofloop()
                    t[dest] = tmp[cursor1]
                    dest += 1
                    cursor1 += 1
                    len1 -= 1
                    if len1 == 1:
                        raise Getoutofloop()
                    minGallop -= 1
                    if not (count1 >= MinGallop | count2 >= MinGallop):
                        break
                if minGallop < 0:
                    minGallop = 0
                minGallop += 2
        except Getoutofloop:
            pass
        minGallop =  1 if minGallop < 1 else minGallop 
        if len1 == 1:
            assert len2 > 0
            for i in range(cursor2, cursor2 + len2):
                t[dest] = t[i]
                dest += 1
            t[dest] = tmp[cursor1]
        elif len1 == 0:
            print("what")
        else:
            assert len2 == 0
            assert len1 > 1
            for i in range(cursor1, cursor1 + len1):
                t[dest] = tmp[i]
                dest += 1
    def mergeHi(base1, len1, base2, len2):
        nonlocal minGallop, MinGallop, tmpBase, tmp, runBase, runLen
        tmp.clear()
        for i in range(base2, base2 + len2):
            tmp.append(t[i])
        cursor1 = base1 + len1 - 1
        cursor2 = tmpBase + len2 - 1
        dest = base2 + len2 - 1
        t[dest] = t[cursor1]
        dest -= 1
        cursor1 -= 1
        len1 -= 1
        if len1 == 0: #! right
            for i in range(cursor2, -1, -1):
                t[dest] = tmp[i]
                dest -= 1
            return
        if len2 == 1: #! right
            for i in range(cursor1, cursor1 - len1, -1):
                t[dest] = t[i]
                dest -= 1
            t[dest] = tmp[cursor2]
            return
        try:
            while True:
                count1 = 0
                count2 = 0
                while True:
                    assert len1 > 0 and len2 > 1
                    if tmp[cursor2] < t[cursor1]:
                        t[dest] = t[cursor1]
                        dest -= 1
                        cursor1 -= 1
                        count1 += 1
                        count2 = 0
                        len1 -= 1
                        if len1 == 0:
                            raise Getoutofloop()
                    else:
                        t[dest] = tmp[cursor2]
                        dest -= 1
                        cursor2 -=1
                        count2 += 1
                        count1 = 0
                        len2 -= 1
                        if len2 == 1:
                            raise Getoutofloop()
                    if not ((count1 | count2) < minGallop):
                        break
                while True:
                    assert len1 > 0 and len2 > 1
                    count1 = len1 - gallopRight(tmp[cursor2], t, base1, len1, len1 - 1)
                    if count1 != 0:
                        for i in range(cursor1, cursor1 - count1, -1):
                            t[dest] = t[i]
                            dest -= 1
                        cursor1 -= count1
                        len1 -= count1
                        if len1 == 0:
                            raise Getoutofloop()
                    t[dest] = tmp[cursor2]
                    dest -= 1
                    cursor2 -= 1
                    len2 -= 1
                    if len2 == 1:
                        raise Getoutofloop()
                    count2 = len2 - gallopLeft(t[cursor1], tmp, tmpBase, len2, len2 - 1)
                    if count2 != 0:
                        for i in range(cursor2, cursor2 - count2, -1):
                            t[dest] = tmp[i]
                            dest -= 1
                        cursor2 -= count2
                        len2 -= count2
                        if len2 <= 1:
                            raise Getoutofloop()
                    t[dest] = t[cursor1]
                    dest -= 1
                    cursor1 -= 1
                    len1 -= 1
                    if len1 == 0:
                        raise Getoutofloop()
                    minGallop -= 1
                    if not (count1 >= MinGallop | count2 >= MinGallop):
                        break
                if minGallop < 0:
                    minGallop = 0
                minGallop += 2
        except Getoutofloop:
            pass
        minGallop = 1 if minGallop < 1 else minGallop
        if len2 == 1:
            assert len1 > 0
            for i in range(cursor1, cursor1 - len1, -1):
                t[dest] = t[i]
                dest -= 1
            t[dest] = tmp[cursor2]
        elif len2 == 0:
            print("what")
        else:
            assert len1 == 0
            assert len2 > 0
            for i in range(cursor2, cursor2 - len2, -1):
                t[dest] = tmp[i]
                dest -= 1
    def mergeForceCollapse():
        while len(runLen) > 1:
            n = len(runLen) - 2
            if n > 0 and runLen[n - 1] < runLen[n + 1]:
                n -= 1
            mergeAt(n)

    def sort(lo, hi):
        assert lo >= 0 and lo <= hi and hi <= len(t)
        remain = hi - lo
        if remain < 2:
            return
        if remain < MinMerge:
            initRunLen = countRunAndMakeAscending(lo, hi)
            binarySort(lo, hi, lo + initRunLen)
            return
        
        minRun = minRunLength(remain)
        while True:
            runLen_ = countRunAndMakeAscending(lo, hi)
            if runLen_ < minRun:
                force = remain if remain <= minRun else minRun
                binarySort(lo, lo + force, lo + runLen_)
                runLen_ = force
            pushRun(lo, runLen_)
            mergeCollapse()
            lo += runLen_
            remain -= runLen_
            if remain <= 0:
                break
        assert lo == hi
        mergeForceCollapse()
        assert len(runLen) == 1
        return
    sort(l, r)

class Getoutofloop(Exception):
    pass

def main():
    generateNumber()
    starttime = time.time()
    if choose == 0:
        print("insertsort")
        insertionsort(data, 0, len(data))
    elif choose == 1:
        print("shellsort")
        shellsort(data, 0, len(data))
    elif choose == 2:
        print("quicksort")
        quicksort(data, 0, len(data) - 1)
    elif choose == 3:
        print("mergesort")
        mergesort(data, 0, len(data))
    elif choose == 4:
        print("radixsort")
        radixsort(data, 0, len(data))
    elif choose == 5:
        print("timsort")
        timsort(data, 0, len(data))
    t = time.time() - starttime
    print(t)

if __name__ == '__main__':
    main()