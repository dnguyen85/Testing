import doctest
import random

INSERTION_SORT_LENGTH = 8

class QuickSort(object):
    """
    >>> qs = QuickSort()
    >>> lst = [3, 2, 4, 7, 8, 9, 1, 0, 14, 11, 23, 50, 26]
    >>> qs.sort(lst)
    >>> lst
    [0, 1, 2, 3, 4, 7, 8, 9, 11, 14, 23, 26, 50]
    >>> lst2 = ['E', 'A', 'S', 'Y', 'Q', 'U', 'E', 'S', 'T', 'I', 'O', 'N']
    >>> qs.sort(lst2)
    >>> lst2
    ['A', 'E', 'E', 'I', 'N', 'O', 'Q', 'S', 'S', 'T', 'U', 'Y']
    """

    def partition(self, arr, lo, hi):
        """
        Partition the (assumed randomized) array w/ respect to a pivot, chosen
        to be the 1st elem of the array.
        Move the pivot into its final sorted position and return its final index
        """
