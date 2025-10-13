### 10\. Searching Algorithms (Binary Search)

Searching algorithms are used to find the location of a target element within a data structure. While linear search (iterating through all elements) is simple, it's inefficient for large datasets. Binary Search offers significantly faster performance when its prerequisites are met.

#### Core Concepts

**Binary Search** is an efficient algorithm for finding an item from a **sorted** list of items. It works by repeatedly dividing the search interval in half.

**Prerequisites:**
The fundamental requirement for Binary Search is that the data collection (array or list) **must be sorted** (either in ascending or descending order).

**Intuition (Guessing Game):**
Imagine you're trying to guess a number between 1 and 100. Instead of guessing randomly or starting from 1 (linear search), you'd likely guess 50. If 50 is too high, you know the number is between 1 and 49. If it's too low, it's between 51 and 100. You've eliminated half the possibilities with one guess. Binary search applies this exact strategy.

**Algorithm Steps:**

1.  Start with the entire sorted array/list as the search space.
2.  Find the middle element of the search space.
3.  Compare the middle element with the target value:
      * If they are equal, you've found the target.
      * If the target is smaller than the middle element, discard the right half and continue searching in the left half.
      * If the target is larger than the middle element, discard the left half and continue searching in the right half.
4.  Repeat steps 2-3 until the target is found or the search space becomes empty.

**Key Pointers/Variables:**

  * `low`: Index of the start of the current search space.
  * `high`: Index of the end of the current search space.
  * `mid`: Index of the middle element (`(low + high) // 2`).

**Time and Space Complexity:**

  * **Time Complexity:** $O(\\log N)$
      * In each step, the search space is halved. This logarithmic behavior makes it extremely fast for large inputs.
  * **Space Complexity:**
      * Iterative: $O(1)$ (constant extra space for variables).
      * Recursive: $O(\\log N)$ for the recursion call stack. While recursive is elegant, iterative is usually preferred in production for large $N$ to avoid potential stack overflow.

#### Python 3.11 Implementation (Iterative & Recursive)

```python
# --- Binary Search (Iterative) ---
def binary_search_iterative(arr, target):
    """
    Performs binary search iteratively on a sorted array.
    Returns the index of the target if found, otherwise -1.
    """
    low = 0
    high = len(arr) - 1

    while low <= high: # Important: use <= to include single-element range
        mid = low + (high - low) // 2 # Avoids potential overflow for very large low+high

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1 # Target is in the right half
        else: # arr[mid] > target
            high = mid - 1 # Target is in the left half

    return -1 # Target not found

# --- Binary Search (Recursive) ---
def binary_search_recursive(arr, target, low, high):
    """
    Performs binary search recursively on a sorted array.
    Returns the index of the target if found, otherwise -1.
    """
    if low > high: # Base case: search space is empty
        return -1

    mid = low + (high - low) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, high)
    else: # arr[mid] > target
        return binary_search_recursive(arr, target, low, mid - 1)

# --- Example Usage ---
sorted_numbers = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]

print("--- Iterative Binary Search ---")
print(f"Target 12 found at index: {binary_search_iterative(sorted_numbers, 12)}") # Output: 3
print(f"Target 56 found at index: {binary_search_iterative(sorted_numbers, 56)}") # Output: 7
print(f"Target 2 found at index: {binary_search_iterative(sorted_numbers, 2)}")   # Output: 0
print(f"Target 91 found at index: {binary_search_iterative(sorted_numbers, 91)}") # Output: 9
print(f"Target 10 not found (expected -1): {binary_search_iterative(sorted_numbers, 10)}") # Output: -1
print(f"Target 100 not found (expected -1): {binary_search_iterative(sorted_numbers, 100)}") # Output: -1

print("\n--- Recursive Binary Search ---")
print(f"Target 12 found at index: {binary_search_recursive(sorted_numbers, 12, 0, len(sorted_numbers) - 1)}") # Output: 3
print(f"Target 10 not found (expected -1): {binary_search_recursive(sorted_numbers, 10, 0, len(sorted_numbers) - 1)}") # Output: -1
```

**Common Pitfalls in Implementation:**

  * **`low <= high` vs. `low < high`:** This is crucial. Use `low <= high` if `mid` might be the answer and your range can shrink to a single element. If `low < high`, it's for problems where `mid` itself is not a candidate (e.g., finding first/last occurrence).
  * **`mid = (low + high) // 2` vs. `mid = low + (high - low) // 2`:** The latter avoids integer overflow if `low` and `high` are very large (not typically an issue in Python, but good practice from other languages).
  * **Updating `low`/`high`:** `mid + 1` and `mid - 1` are used to exclude the `mid` element from the next search space, as it has already been checked.
  * **Edge Cases:** Empty array, single-element array, target at boundaries (first/last element), target not present.

#### Problem-Solving Patterns

Binary Search is a powerful pattern not just for finding an element, but for reducing a search space.

1.  **Standard Search (Exact Match):**

      * Finding a specific value in a sorted array.

2.  **Finding First/Last Occurrence:**

      * When duplicates exist, adapt binary search to find the very first or very last index of a target. This involves continuing the search even after a match is found, but adjusting `high` or `low` carefully.

3.  **Finding Element Closest to Target / Smallest/Largest Greater Than/Less Than:**

      * Binary search can be adapted to find elements that meet certain criteria around the target, even if the exact target isn't present.

4.  **Binary Search on Answers (or on Result Space):**

      * **Concept:** This is a very important and non-obvious application. When the problem asks for a minimum maximum value, or a maximum minimum value, or some optimal value that satisfies a `check()` function, and the possible answer space is monotonic, you can binary search on the *answers* instead of the array elements.
      * The `check()` function determines if a given candidate "answer" is feasible. If it is, you might try a smaller/larger answer; if not, a larger/smaller answer.
      * **Prerequisite:** The "property" you are searching for must be monotonic (e.g., if X is a valid answer, then all answers greater than X are also valid; or if X is not valid, all answers smaller than X are also not valid).
      * **Examples:**
          * Find the smallest capacity to ship packages within D days.
          * Find the largest minimum distance between K elements.
          * Find the smallest divisor given a threshold.
          * Square root of x.

#### Handling Large Inputs / Constraints

  * **Sorted Input:** The most critical constraint. If the input is not sorted, you must sort it first. This adds an $O(N \\log N)$ preprocessing step, making the overall solution $O(N \\log N)$, where the search itself is $O(\\log N)$.
  * **Integer Overflow:** While `low + (high - low) // 2` mitigates this for `mid` calculation in other languages, Python integers handle arbitrary size, so `(low + high) // 2` is fine.
  * **Recursion Depth:** Recursive binary search will have a recursion depth of $O(\\log N)$. For extremely large $N$ (e.g., arrays with $10^9$ elements), iterative is safer or necessary to avoid Python's recursion limit.
  * **Floating-Point Precision:** When binary searching on real numbers (e.g., `sqrt(x)`), you'll typically iterate a fixed number of times or until the search interval is smaller than a certain epsilon, rather than relying on exact equality.

#### Typical FAANG Problem Example

Let's look at a problem that uses **Binary Search on Answers**.

**Problem Description: "Koko Eating Bananas"** (LeetCode Medium)

Koko loves to eat bananas. There are `n` piles of bananas, the `i`-th pile has `piles[i]` bananas. The guards have gone and will come back in `h` hours.

Koko can decide her eating speed of `k` bananas per hour. Each hour, she chooses some pile of bananas and eats `k` bananas from it. If the pile has less than `k` bananas, she eats all of them instead and will not eat any more bananas during this hour.

Return the minimum integer `k` such that she can eat all the bananas within `h` hours.

**Constraints:**

  * `1 <= piles.length <= 10^4`
  * `1 <= piles[i] <= 10^9`
  * `piles.length <= h <= 10^9`

**Thought Process & Hints:**

1.  **Understanding the Goal:** Find the *minimum* eating speed `k` that allows Koko to finish all bananas within `h` hours. The `k` value is what we're searching for.

2.  **Why Binary Search?**

      * The problem asks for a "minimum" value that satisfies a condition. This often signals binary search on answers.
      * What's the range of possible `k` values?
          * Minimum `k`: Koko must eat at least 1 banana per hour to eventually finish. So, `low = 1`.
          * Maximum `k`: In the worst case, Koko might eat all bananas from the largest pile in one hour. So, `high = max(piles)`.
      * Is the property monotonic? If Koko can eat all bananas at speed `k`, she can certainly eat them at any speed `k'` where `k' > k`. This monotonicity means we can use binary search\!

3.  **The `check(k)` Function:**

      * We need a function `can_finish(k)` that takes an eating speed `k` and returns `True` if Koko can finish all bananas within `h` hours at that speed, `False` otherwise.
      * How to calculate hours needed for a given `k`?
          * For each pile `p`, hours needed for that pile is `ceil(p / k)`. In Python, this is `(p + k - 1) // k` for integer division, or `math.ceil(p / k)`.
          * Sum these hours for all piles. If `total_hours <= h`, then `can_finish(k)` is `True`.

4.  **Algorithm Sketch (Binary Search on Answers):**

      * Define `low = 1` (minimum possible speed).
      * Define `high = max(piles)` (maximum possible speed).
      * Initialize `ans = high` (or some sufficiently large value, or even `max(piles)`). This will store the smallest `k` that works.
      * While `low <= high`:
          * `mid = low + (high - low) // 2`
          * If `can_finish(mid)` is `True`:
              * `mid` is a possible answer. Try to find an even smaller `k`.
              * `ans = mid`
              * `high = mid - 1`
          * Else (`can_finish(mid)` is `False`):
              * `mid` is too slow. Need a faster `k`.
              * `low = mid + 1`
      * Return `ans`.

5.  **Complexity Analysis:**

      * **`can_finish(k)` function:** Iterates through all `N` piles, performs constant time arithmetic for each. So, $O(N)$.
      * **Binary Search loop:** The loop runs $O(\\log(\\text{Max\_K - Min\_K}))$ times. `Max_K` can be up to $10^9$. $\\log(10^9)$ is roughly 30.
      * **Total Time Complexity:** $O(N \\log(\\text{max\_pile\_size}))$. This is very efficient.
      * **Space Complexity:** $O(1)$ (for variables), plus input storage $O(N)$.

This problem perfectly showcases how binary search can be applied to a range of possible answers, transforming a seemingly complex optimization problem into a manageable one.

#### System Design Relevance

  * **Database Indexing:** B-trees and B+ trees (which rely on sorted data and binary search-like traversal) are fundamental for efficient data retrieval in databases.
  * **Search Engine Indexes:** When searching for keywords, inverted indexes are often used, which store sorted lists of document IDs. Binary search can then quickly find documents associated with a keyword.
  * **Resource Allocation/Scheduling:** When resources (e.g., servers, bandwidth, time slots) need to be allocated based on some criteria (e.g., minimum required capacity, earliest available time), binary search can find optimal allocation points within sorted resource pools.
  * **Load Balancing:** Finding the least loaded server in a sorted list of servers.
  * **Distributed Systems (Consistent Hashing):** While more complex, consistent hashing can conceptually use binary search on a sorted ring of hash values to map keys to nodes.
  * **Large Data Set Lookups:** Any system that needs fast lookups on static or infrequently updated large sorted datasets (e.g., IP address to geographical location mapping).

**Challenge to the Reader:**
Consider the "Search in Rotated Sorted Array" problem (LeetCode Medium). The input array is sorted but has been rotated at an unknown pivot. How would you adapt binary search to find a target element in such an array in $O(\\log N)$ time? (Hint: The key is to identify which half of the current search space is *still sorted* and use that knowledge).