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

def knuth_shuffle_forward(arr):
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

class CountInversions(object):
    """
    Count the number of inversions in an array
    """
    def count_inversions_bisect(self, lstA, lstB):
        sum = 0
        for elemB in lstB:
            insertion_point = bisect.bisect_left(lstA, elemB)
            sum += len(lstA) - insertion_point

        return sum

    def merge_and_count_inversions(self, aux, lst, low, mid, high):
        """
        Merge lst[low..mid] and lst[mid+1..high], using aux[low..high] as auxiliary storage
            - precondition: a[low..mid] and a[mid+1..high] are sorted arrays
        """
        # Copy lst to aux
        for k in range(low, high+1):
            aux[k] = lst[k]

        # Merge aux[lo..mid] and aux[mid+1..high] back into lst[low..high]
        # 2 pointers i and j used to advance across 2 sub-lists
        inversion_cnt = 0
        i, j = low, mid+1

        for k in range(low, high+1):
            if i > mid: # left sequence exhausted, take right & no inversion
                lst[k] = aux[j]
                j += 1
            elif j > high: # right sequence exhausted, take left & all inversions had been counted
                lst[k] = aux[i]
                i += 1
            elif aux[i] <= aux[j]: # take left & no inversion
                lst[k] = aux[i]
                i += 1
            else: # take right & b_j is inverted w/ every elems left in A
                lst[k] = aux[j]
                j += 1
                inversion_cnt += (mid - i + 1)

        return inversion_cnt

    def __count_inversion_helper(self, aux, lst, low, high):
        if high <= low:
            return 0

        mid = (low + high) // 2
        left_count = self.__count_inversion_helper(aux, lst, low, mid)
        right_count = self.__count_inversion_helper(aux, lst, mid+1, high)
        merge_count = merge_and_count_inversion(aux, lst, low, mid, high)
        return left_count + right_count + merge_count

    def count_inversions(self, lst):
        aux = list(lst)
        return self.__count_inversion_helper(aux, lst, 0, len(lst)-1)



                

if __name__ == '__main__':
    doctest.testmod()

