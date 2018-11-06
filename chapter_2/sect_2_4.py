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


# Prob. 2.4.33, 2.4.34 practice probs 
class IndexMinPQ(object):
    """
    >>> test_data = 'testexmaple'
    >>> imp = IndexMinPQ(len(test_data))
    >>> imp.is_empty()
    True
    >>> for index, s in enumerate(test_data):
    ...     imp.insert(index, s)
    ...
    >>> imp.is_empty()
    False
    >>> imp.size()
    11
    >>> [imp.contains(i) for i in (12, -1, 1, 4, 10)]
    [False, False, True, True, True]
    >>> imp.min_index()
    7
    """

    def __init__(self, max_size):
        """
        Initialize an IndexMinPQ w/ fixed capacity, with possible fast-access
        indices btw 0..max_size-1
        """
        assert max_size > 0
        self._max_size = max_size               # Capacity of the queue
        self._N = 0                             # Number of items currently on the queue
        self._pq = [-1] * (max_size + 1)        # binary heap using 1-based indexing, priority idx -> fast-access idx
        self._qp = [-1] * (max_size + 1)        # Reverse index from fast-access idx -> priority_idx
                                                # qp[pq[i]] = pq[qp[i]] = i
        self._keys = [None] * (max_size + 1)    # storing items (w/ inherent priority) using fast-access indices

    # Aux APIs
    def is_empty(self):
        return self._N == 0

    def size(self):
        return self._N

    def contains(self, k):
        """
        Is fast-access idx k associated w/ some item on the queue?
        """
        if k < 0 or k >= self._N:
            return False

        return self._qp[k] != -1

    def swim(self, pos):
        """
        Swim up from the current priority idx at `pos`. Use helpers method
        less() and exch()
        """
        while pos > 1 and less(pos, pos // 2):
            self.exch(pos, pos // 2)
            pos //= 2

    def sink(self, pos):
        """
        Sink elem down from the current priority idx at `pos`, use helper method
        less() and exch()
        """
        while 2 * pos <= self._N:
            left_child, right_child = 2 * pos, 2 * pos + 1
            swapped_child = left_child
            if right_child <= self._N and less(right_child, left_child):
                swapped_child = right_child
            # Should we stop iterations?
            if not less(swapped_child, pos):
                break

            # If not, sink
            exch(swapped_child, pos)
            pos = swapped_child

    def less(self, pos1, pos2):
        """
        Compare 2 items on PQ at pos1 and pos2
        """
        return self.keys[self._pq[pos1]] < self.keys[self._pq[pos2]]

    def exch(self, pos1, pos2):
        """
        Exchange 2 items @ priority idx pos1 and pos2 on the queue
        """
        # Record new priorities for fast-access idxs @ pos1 and pos2
        self._qp[self._pq[pos1]] = pos2
        self._qp[self._qp[pos2]] = pos1
        # Record new fast-access idxs for the 2 priorities
        self._pq[pos1], self._pq[pos2] = self._pq[pos2], self._pq[pos1]

    # Main APIs
    def insert(self, k, elem):
        """
        Insert elem at fast-access idx k on the priority queue
        """
        if k < 0 or k >= self._max_size or self.contains(k):
            return

        self._N += 1
        self._keys[k] = elem
        # Initial indexing for elem at queue end, before reheapifying
        self._pq[self._N] = k
        self._qp[k] = self._N
        # Swim the elem
        self.swim(self._N)

    def delMin(self):
        """
        Remove min item on PQ and returns its fast-access index
        """
        if self._N == 0:
            return -1
        
        # Get the fast-access idx of min elem on PQ
        min_idx = self._pq[1]

        # Swap min elem w/ last elem on PQ
        self.exch(1, self._N)

        # Delete the last elem on PQ (prev min)
        self._N -= 1
        self._pq[self._N + 1] = -1
        self._qp[min_idx] = -1
        self._keys[min_idx] = None

        # Reheapify
        self.sink(1)
        return min_idx
        
    def change_key(self, k, elem):
        if k < 0 or k >= self._N or not self.contains(k):
            return

        self._keys[k] = elem
        # Reheapify kth element priority
        self.swim(self._qp[k])
        self.sink(self._qp[k])

    def min_key(self):
        """
        Return the minium element
        """
        return None if self._N == 0 else self._keys[self._pq[1]]

def heap_sort(arr):
    """
    Assume a 1-based array for sorting
    Heap-sort implementation, using priority queue sink() method as util function,
    first build the maximum priority queue, and exchange list[0] and lst[size], then size minus one,
    and sink the list[0] again, util size equals zero.
    >>> lst = []
    >>> lst = [i for i in range(10)]
    >>> random.shuffle(lst)
    >>> heap_sort(lst)
    >>> lst
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    """ 
    def sink(arr, idx, N):
        """
        sink() helper method to restore the heap invariant for element @ idx 
        """
        while 2 * idx <= N:
            left_child, right_child = 2 * idx, 2 * idx + 1
            swapped_child = left_child
            if 2 * idx < N and arr[left_child] < arr[right_child]:
                swapped_child = right_child

            # If not, keep sinking
            arr[idx], arr[swapped_child] = arr[swapped_child], arr[idx]
            idx = swapped_child

    # Method implementation 
    _N = len(arr)

    # first build a MaxPQ heap for arr[1..N]
    for i in range(_N // 2, 0, -1):
        # Sink the top half of the array inductively
        sink(arr, i, _N)

    # Sort down 
    while _N > 1:
        # Swap max elem w/ last elem
        arr[1], arr[_N] = arr[_N], arr[1]
        # Reduce PQ size:
        _N -= 1
        # Reheapify
        sink(arr, 1, _N)
    
if __name__ == '__main__':
    doctest.testmod()



