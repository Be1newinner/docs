"""
🔹 1. Bubble Sort

Concept: Repeatedly swap adjacent elements if they are in the wrong order.
Use Case: Educational; rarely used in production.
Issues: Very inefficient for large lists — O(n²) time.

🔹 2. Selection Sort

Concept: Select the smallest (or largest) element and place it at the beginning.
Use Case: Educational; not used in production.
Issues: O(n²) time, even when the list is mostly sorted.

🔹 3. Insertion Sort

Concept: Build sorted list one item at a time.
Use Case: Efficient for small or nearly sorted datasets.
Time Complexity: Worst-case O(n²), best case O(n).

🔹 4. Merge Sort

Concept: Divide the array into halves, sort recursively, and merge.
Use Case: Large datasets; stable sort; external sorting.
Time Complexity: Always O(n log n).
Space: O(n) extra.

🔹 5. Quick Sort

Concept: Pick a pivot, partition array, and recursively sort partitions.
Use Case: Preferred for in-place sorting.
Time Complexity: Avg O(n log n), Worst O(n²) (can be fixed with good pivoting).
Space: O(log n) auxiliary.

🔹 6. Heap Sort

Concept: Use a binary heap to repeatedly extract min/max.
Use Case: When memory is a concern, and you need guaranteed O(n log n).
Time: O(n log n), not stable.

🔹 7. Counting Sort

Concept: Count occurrences of elements (integers).
Use Case: Works for small range integers (like 0-100).
Time: O(n + k), where k is range.

🔹 8. Radix Sort

Concept: Sort digits from least to most significant using counting sort.
Use Case: Efficient for large numbers with small digit length.
Time: O(nk), where k = digit length.

🔹 9. Bucket Sort

Concept: Distribute into buckets, then sort individually.
Use Case: Uniformly distributed floating-point numbers.
Time: O(n + k) average.

"""

from typing import List

# ls = [10, 2, 5, 99, 14, 154, 22, 1, 5, 3, 9, 14]
ls = [99, 98, 97, 96, 95, 94, 93, 92, 91, 90]
# ls = [99, 98, 97, 96, 95, 94, 93, 92, 91]
# ls = [99, 98, 97, 96, 95, 94, 93, 92]
# ls = [99, 98, 97, 96, 95, 94, 93]
# ls = [99, 98, 97, 96, 95, 94]

# ✅ Bubble Sort – Intuition

# Bubble Sort is a comparison-based algorithm that:
# Repeatedly swaps adjacent elements if they are in the wrong order.
# With each full pass, the largest unsorted element "bubbles up" to its correct position.


def bubble_sort(ls: list[int]):
    for i in range(len(ls) - 1):
        swapped = False
        for j in range(len(ls) - i - 1):
            if ls[j] > ls[j + 1]:
                ls[j], ls[j + 1] = ls[j + 1], ls[j]
                swapped = True
        if not swapped:
            break
    return ls


# print(bubble_sort(ls))

"""
✅ Selection Sort – Intuition

Selection Sort divides the array into two parts:
The sorted part (beginning)
The unsorted part (rest of the array)
At each step:
Find the minimum element in the unsorted part
Swap it with the first element of the unsorted part
So it keeps selecting the smallest element and moves it to its correct position.

📌 Time & Space Complexity
Case	    Time
Best	    O(n²)
Average	O(n²)
Worst	    O(n²)

Space Complexity: O(1) (in-place)
Stable? No ❌ (can break the order of equal elements)

Len = Steps ( n*(n+1) / 2)
10 = 45
9 = 36
8 = 28
7 = 21
6 = 15
"""


def selection_sort(list: List[int]):
    if not list or not len(list):
        return None

    n = len(list)
    steps = 0

    for i in range(n):
        minimum = i
        for j in range(i + 1, n):
            steps += 1
            if list[j] < list[minimum]:
                minimum = j
        if i != minimum:
            list[i], list[minimum] = list[minimum], list[i]
    print(steps)
    return list

# print(selection_sort(ls))

# 📌 Merge Sort: Concept
# What it does:
# Divides the list into halves recursively
# Sorts each half
# Merges them back together in sorted order

def merge(left: List[int], right: List[int]) -> List[int]:
    i = j = 0
    merged_list = []

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            merged_list.append(left[i])
            i += 1
        else:
            merged_list.append(right[j])
            j += 1

    merged_list.extend(left[i:])
    merged_list.extend(right[j:])

    return merged_list

def merge_sort(arr: List[int]) -> List[int]:

    if len(arr) <= 1:
        return arr

    mid_arr_index = len(arr) // 2
    left_arr = merge_sort(arr[mid_arr_index:])
    right_arr = merge_sort(arr[:mid_arr_index])

    return merge(left_arr, right_arr)

# print(merge_sort(ls))


def insertion_sort(arr: List[int]) -> List[int]:
    pass


def quick_sort(arr: List[int]) -> List[int]:
    pass


def heap_sort(arr: List[int]) -> List[int]:
    pass


def counting_sort(arr: List[int]) -> List[int]:
    pass


def radix_sort(arr: List[int]) -> List[int]:
    pass


def bucket_sort(arr: List[int]) -> List[int]:
    pass
