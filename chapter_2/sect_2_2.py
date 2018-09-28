#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
import random
import collections

class MergeSort(object):
    """
      Top-bottom merge sort implementation, merge the two sub arrays
    of the whole list and make the list partial ordered,
    and the recursion process make sure the whole list is ordered.
    for a N-size array, top-bottom merge sort need 1/2NlgN to NlgN comparisons,
    and need to access array 6NlgN times at most.
    >>> ms = MergeSort()
    >>> lst = [4, 3, 2, 5, 7, 9, 0, 1, 8, 7, -1, 11, 13, 31, 24]
    >>> ms.sort(lst)
    >>> lst
    [-1, 0, 1, 2, 3, 4, 5, 7, 7, 8, 9, 11, 13, 24, 31]
    """ 

    def merge(self, aux, lst, low, mid, high):
        """
        Stably merge lst[low..mid] with lst[mid+1..hi], using aux[lo..hi] as
        auxiliary storage.
            - precondition: a[lo..mid] and a[mid+1..hi] are sorted arrays
        """
        # copy lst to aux - can we *avoid this*?
        for k in range(low, high+1):
            aux[k] = lst[k]

        # Merge aux[lo..mid] and aux[mid+1..hi] back into lst[lo..hi]
        # 2 pointers i and j to advance across 2 sublists
        i, j = low, mid+1

        for k in range(low, high+1):
            if i > mid: # left sequence exhausted, take element from right sequence
                lst[k] = aux[j]
                j += 1
            elif j > high: # right sequence exhausted
                lst[k] = aux[i]
                i += 1
            elif aux[j] < aux[i]: # take from right
                lst[k] = aux[j]
                j += 1
            else:                 # take from left
                lst[k] = aux[i]
                i += 1

    def sort(self, lst):
        """
        Actual API to do sorting of lst
        """
        # Allocated an aux array only once
        aux = list(lst)
        # Recursion calls
        self.__sort(lst, aux, 0, len(lst)-1)

    def __sort(self, lst, aux, low, high):
        """
        Helper function to carry out the recursion w/ a different signature
        """
        if high <= low:
            return

        # Get the midpoint
        mid = (low + high) // 2

        # Recursively sort both lists
        self.__sort(lst, aux, low, mid)
        self.__sort(lst, aux, mid+1, high)
        # Merge the 2 sorted halves
        self.merge(aux, lst, low, mid, high)

class MergeSortBU(object):
    """
    Bottom-up merge sort algorithm implementation, cut the whole N-size array into
    N/sz small arrays, then merge each two of them,
    the sz parameter will be twice after merge all the subarrays,
    util the sz parameter is larger than N.
    >>> ms = MergeSortBU()
    >>> lst = [4, 3, 2, 5, 7, 9, 0, 1, 8, 7, -1]
    >>> ms.sort(lst)
    >>> lst
    [-1, 0, 1, 2, 3, 4, 5, 7, 7, 8, 9] 
    """

    def sort(self, lst):
        """
        MergeSortBU
        """
        length = len(lst)
        # Allocate aux array for merging
        aux = [None] * length
        sz = 1 

        while sz < length:
            # Index traversing in stride sz, 0..
            for i in range(0, length-sz, sz*2):   # i stops at length-size-1
                # Merge 2 segments of (at most) sz elements
                # First is a[i]...a[i + sz-1]
                # 2nd is a[i+sz]...a[i + 2*sz-1]
                self.merge(aux, lst, i, i + sz-1, min(i + 2*sz-1, length-1))
            sz *= 2

    def merge(self, aux, lst, low, mid, high):
        """
        Stably merge lst[low..mid] with lst[mid+1..hi], using aux[lo..hi] as
        auxiliary storage.
            - precondition: a[lo..mid] and a[mid+1..hi] are sorted arrays
        """
        # copy lst to aux - can we *avoid this*?
        for k in range(low, high+1):
            aux[k] = lst[k]

        # Merge aux[lo..mid] and aux[mid+1..hi] back into lst[lo..hi]
        # 2 pointers i and j to advance across 2 sublists
        i, j = low, mid+1

        for k in range(low, high+1):
            if i > mid: # left sequence exhausted, take element from right sequence
                lst[k] = aux[j]
                j += 1
            elif j > high: # right sequence exhausted
                lst[k] = aux[i]
                i += 1
            elif aux[j] < aux[i]: # take from right
                lst[k] = aux[j]
                j += 1
            else:                 # take from left
                lst[k] = aux[i]
                i += 1

# 2.2.14 practice merge 2 sorted queues
def merge_queue(q1, q2):
    """
    Note: assume q1 and q2 are of type collections.deque()
    >>> merge_queue([1, 2, 3, 4], [])
    [1, 2, 3, 4]
    >>> merge_queue([], [1, 2, 3, 4])
    [1, 2, 3, 4]
    >>> merge_queue([1, 2, 3, 4], [4, 5, 6])
    [1, 2, 3, 4, 4, 5, 6]
    >>> merge_queue([1, 2, 3, 4], [1, 2, 3, 4])
    [1, 1, 2, 2, 3, 3, 4, 4]
    >>> merge_queue([1, 2], [5, 6, 7, 8])
    [1, 2, 5, 6, 7, 8]
    >>> merge_queue([2, 3, 5, 9], [2, 7, 11])
    [2, 2, 3, 5, 7, 9, 11]
    """
    new_queue = collections.deque()
    # 2 pointers
    i1, i2 = 0, 0

    for i in range(len(q1) + len(q2)):
        if i1 > len(q1) - 1:    # q1 exhausted
            new_queue.extend(q2[i2:])
            break
        elif i2 > len(q2) - 1:  # q2 exhausted
            new_queue.extend(q1[i1:])
            break
        elif q1[i1] < q2[i2]:   # Take elem from q1
            new_queue.append(q1[i1])
            i1 += 1
        else:                   # Take elem from q2
            new_queue.append(q2[i2])
            i2 += 1

    return list(new_queue)

# 2.2.15 practice bottom-up merge list using queue, make each element as sub queue,
# merge first two sub queue in the large queue and enqueue the result util
# there is only one sub queue.
def bu_merge_sort_q(lst):



if __name__ == '__main__':
    doctest.testmod()


