#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
import random
import bisect

class MaxPQ(object):
    """
    Max priority-queue implementation
    >>> mpq = MaxPQ(10)
    >>> lst = [i for i in range(10)]
    >>> random.shuffle(lst)
    >>> for i in lst:
    ...     mpq.insert_effective(i)
    ...
    >>> mpq.min_val()
    0
    >>> print_lst = []
    >>> while not mpq.is_empty():
    ...     print_lst.append(str(mpq.del_max()))
    ...
    >>> ' '.join(print_lst)
    '9 8 7 6 5 4 3 2 1 0'
    """

    # Constructor
    def __init__(self, size):
        self._pq = [None] * (size + 1)  # Array impl - heap-ordered complete binary tree
        self._size = 0                  # pq[1.._size], w/ pq[0] unused
        self._min = None                # keep track of min value seen

    def is_empty(self):
        return self._size == 0

    def size(self):
        return self._size

    def swim(self, pos):
        """
        Bottom-up reheapify the elem @ pos
        """
        # Repeated compare with parent and swap if necessary, until reaching root
        parent_idx = pos // 2
        while pos > 1 and self._pq[pos] > self._pq[parent_idx]:
            self._pq[pos], self._pq[parent_idx] = self._pq[parent_idx], self._pq[pos]
            pos = parent_idx

    def sink(self, pos):
        """
        Top-down reheapify the elem @ pos
        """
        # Repeatedly compare with children, if any:
        left_child, right_child = 2 * pos, 2 * pos + 1
        while left_child <= self._size:
            # Swap left child by default - if need be
            swapped_child = left_child

            # check if we should swap the other child instead - if need be
            if left_child < self._size and self._pq[left_child] < self._pq[right_child]:
                swapped_child = right_child

            # Should we sink?
            if self._pq[pos] >= self._pq[swapped_child]:
                break

            self._pq[pos], self._pq[swapped_child] = self._pq[swapped_child], self._pq[pos]
            pos = swapped_child

    def insert(self, val): 
        # Add the elem at the end
        self._size += 1
        self._pq[self._size] = val
        if not self._min or self._min > val:
            self._min = val
        self.swim(self._size)

    def min_val(self):
        return self._min

    def del_max(self):
        """
        Delete the max item from the pq
        """
        # Extract root key and exchange last element up
        _max = self._pq[1]
        self._pq[1], self._pq[_size] = self._pq[size], self._pq[1]
        # Reduce size
        self._size -= 1
        # Clean up mem
        self._pq[_size+1] = None
        # Reheapify
        self.sink(1)
        return _max

    def max_val(self):
        return self._pq[1]

class MinPQ(object):

    """
    >>> mpq = MinPQ(10)
    >>> lst = [i for i in range(10)]
    >>> random.shuffle(lst)
    >>> for i in lst:
    ...     mpq.insert(i)
    ...
    >>> print_lst = []
    >>> while not mpq.is_empty():
    ...     print_lst.append(str(mpq.del_min()))
    ...
    >>> ' '.join(print_lst)
    '0 1 2 3 4 5 6 7 8 9'
    """

    def __init__(self, size):
        self._pq = [None] * (size + 1)
        self._size = 0

    def is_empty(self):
        return self._size == 0

    def size(self):
        return self._size

    def swim(self, pos):
        while pos > 1 and self._pq[int(pos / 2)] > self._pq[pos]:
            self._pq[int(pos / 2)], self._pq[pos] = self._pq[pos], self._pq[int(pos / 2)]
            pos //= 2

    def sink(self, pos):
        while 2 * pos <= self._size:
            index = 2 * pos
            if index < self._size and self._pq[index] > self._pq[index + 1]:
                index += 1
            if self._pq[pos] <= self._pq[index]:
                break
            self._pq[index], self._pq[pos] = self._pq[pos], self._pq[index]
            pos = index

    def insert(self, val):
        self._size += 1
        self._pq[self._size] = val
        self.swim(self._size)

    def del_min(self):
        min_val = self._pq[1]
        self._pq[1], self._pq[self._size] = self._pq[self._size], self._pq[1]
        self._pq[self._size] = None
        self._size -= 1
        self.sink(1)
        return min_val

    def min_val(self):
        return self._pq[1]





