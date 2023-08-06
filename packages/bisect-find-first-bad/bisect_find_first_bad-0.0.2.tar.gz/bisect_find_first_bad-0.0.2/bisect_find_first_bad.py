import bisect
import abc
from typing import Any, Sequence
import sys


if sys.version_info >= (3, 10):
    bisect_left = bisect.bisect_left
else:
    # hardcode fallback
    # https://github.com/python/cpython/blob/3.10/Lib/bisect.py#L68-L99
    # https://github.com/python/cpython/pull/20556
    def bisect_left(a, x, lo=0, hi=None, *, key=None):
        """Return the index where to insert item x in list a, assuming a is sorted.
        The return value i is such that all e in a[:i] have e < x, and all e in
        a[i:] have e >= x.  So if x already appears in the list, a.insert(i, x) will
        insert just before the leftmost x already there.
        Optional args lo (default 0) and hi (default len(a)) bound the
        slice of a to be searched.
        """

        if lo < 0:
            raise ValueError('lo must be non-negative')
        if hi is None:
            hi = len(a)
        # Note, the comparison uses "<" to match the
        # __lt__() logic in list.sort() and in heapq.
        if key is None:
            while lo < hi:
                mid = (lo + hi) // 2
                if a[mid] < x:
                    lo = mid + 1
                else:
                    hi = mid
        else:
            while lo < hi:
                mid = (lo + hi) // 2
                if key(a[mid]) < x:
                    lo = mid + 1
                else:
                    hi = mid
        return lo


class color:
    RED       = lambda s: '\033[31m' + str(s) + '\033[0m'
    GREEN     = lambda s: '\033[32m' + str(s) + '\033[0m'


class BisectFindFirstBad(abc.ABC):
    def __init__(self, options: Sequence[Any]):
        self.options = options

    def _is_bad(self, op: Any) -> bool:
        """
        False/0 means good/old/left
        True/1 means bad/new/right
        """
        print(op, 'start')
        is_bad = self.is_bad(op)
        if is_bad:
            print(color.RED(f'{op}: BAD'))
        else:
            print(color.GREEN(f'{op}: GOOD'))
        return is_bad

    @abc.abstractmethod
    def is_bad(sel, op: Any) -> bool: ...

    def __call__(self):
        """
        https://docs.python.org/3/library/bisect.html#searching-sorted-lists
        Locate the leftmost value exactly equal to x
        """
        a = self.options
        x = True  # True means bad
        i = bisect_left(a, x, key=self._is_bad)
        if i != len(a) and self.is_bad(a[i]) == x:
            print('=' * 100)
            print(f'first bad option is: {a[i]}')
            return a[i]
        raise ValueError('all options are bad')
