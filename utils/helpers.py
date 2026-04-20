"""helpers.py
Utility functions: sorting and searching algorithms examples used by the AI and move utilities.

DSA Concepts:
- Sorting Algorithms: Quick Sort implemented for sorting move lists by heuristic.
  # Sorting moves by heuristic score using Quick Sort.
- Searching Algorithms: Binary search & Linear search examples.
  # Binary search used to quickly find a specific move in a sorted move list.
  # Linear search used when list is unsorted or for small datasets.
"""

from typing import List, Callable, Any

def quicksort(arr: List[Any], key: Callable[[Any], int]) -> List[Any]:
    """Simple quicksort that returns a new sorted list by key.
    """
    # for small lists Python's Timsort is better; implemented explicitly for education.

    if len(arr) <= 1:
        return arr[:]
    pivot = key(arr[len(arr) // 2])
    left = [x for x in arr if key(x) < pivot]
    mid = [x for x in arr if key(x) == pivot]
    right = [x for x in arr if key(x) > pivot]
    return quicksort(left, key) + mid + quicksort(right, key)


def linear_search(arr: List[Any], predicate: Callable[[Any], bool]) -> int:
    """Linear search returns index of first element matching predicate or -1.

    # Linear search used for small or unsorted datasets.
    """
    for i, v in enumerate(arr):
        if predicate(v):
            return i
    return -1


def binary_search(arr: List[Any], target: Any, key: Callable[[Any], Any]) -> int:
    """Binary search on arr sorted by key; returns index or -1.

    # Binary search used to quickly find a specific move in a sorted move list.
    """
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        k = key(arr[mid])
        if k == target:
            return mid
        elif k < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
