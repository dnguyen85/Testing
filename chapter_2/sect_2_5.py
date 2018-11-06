#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
import itertools

# 2.5.4 practice: return a sorted and non-duplicated-item list
def dedup(lst):
    """
    Returns a non-duplicate list
    """
    new_lst = []
    seen = set()
    for elem in lst:
        if elem not in seen:
            new_lst.append(elem)
            seen.add(elem)

    return new_lst

# 2.5.19 practice: kendall tau distance algo. impl.
class KendallTau(object):
    """
    A class to compute the Kendall tau distances between two lists
    >>> klt = KendallTau()
    >>> klt.kendall_tau_count((0, 3, 1, 6, 2, 5, 4), (1, 0, 3, 6, 4, 2, 5))
    4
    """

def knuth_shuffle_backward(arr):
    """
    Shuffle an array in place, from end to beginning
    """
    for i in reversed(range(1, len(arr))): # i from n-1 downto 1
        j = random.randint(0, i)           # Pick randomly 0 <= j <= i     
        arr[j], arr[i] = arr[i], arr[j]    # exchange     

def knuth_shuffle_foward(arr):
    """
    Shuffle an array in place, from beginning to end
    """
    for i in range(0, len(arr)-2):          # i from 0..n-2 
        j = random.randint(i, len(arr)-1)   # Pick randomly i <= j < n
        arr[i], arr[j] = arr[j], arr[i]

def count_inversions_brute_force(arr):
    """
    Count number of inversions in a near-sorted array
    """
    inversions = 0
    for i, j in itertools.combinations(range(len(arr)), 2):
        if arr[i] > arr[j]:
            inversions += 1
    return inversions

def kendall_tau_brute_force(ranking1, ranking2):
    """
    Count the Kendall tau distances btw 2 rankings
    """
    distance = 0

    for i, j in itertools.combinations(range(len(ranking1)), 2):
        a = ranking1[i] - ranking1[j]
        b = ranking2[i] - ranking2[j]

        # If discordant (different signs)
        if a * b < 0:
            distance += 1

    return distance

if __name__ == '__main__':
    doctest.testmod()

