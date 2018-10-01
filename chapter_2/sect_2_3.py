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
        pivot = arr[lo]
        i, j = lo, hi + 1   # Left and right indices for scanning

        while True:
            # Left scan
            while True:
                i += 1
                if arr[i] > pivot or i == hi:    
                    break;

            # Right scan
            while True:
                j -= 1
                if arr[j] < pivot or j == lo:
                    break;

            # Check if pointers cross - we're done partitioning
            if i >= j:
                break

            # If not, exchange out-of-place items
            arr[i], arr[j] = arr[j], arr[i]
        
        # Put pivot into position
        arr[lo], arr[j] = arr[j], arr[lo]

        # return index of pivot
        return j

    def __sort(self, arr, lo, hi):
        """
        Top-level sort recursive helper routine to sort an array inplace, with
        parameterized args
        """
        # Exit when size drop below insertion sort threshold
        if hi <= lo + INSERTION_SORT_LENGTH:
            self.insertion_sort(arr, lo, hi)
            return

        # Put pivot into final position & partition array
        pivot_idx = self.partition(arr, lo, hi)
        # Sort left and right pieces recursively
        self.__sort(arr, lo, pivot_idx - 1)
        self.__sort(arr, pivot_idx + 1, hi)

    def sort(self, arr):
        """
        Top-level quiksort API
        """
        # Shuffle array
        random.shuffle(arr)
        
        # Call recursive helper func:
        self.__sort(arr, 0, len(arr) - 1)

    def insertion_sort(self, arr, lo, hi):
        """
        Use insertion sort to sort the array in place
        """
        # Start sorting from next element up
        for i in range(lo+1, hi+1):
            j = i
            while j > lo and arr[j] < arr[j-1]:
                # Swap j with its predecessor
                arr[j], arr[j-1] = arr[j-1], arr[j]
                j -= 1


if __name__ == '__main__':
    doctest.testmod()
