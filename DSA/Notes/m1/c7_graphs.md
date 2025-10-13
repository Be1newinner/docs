### 7. Heaps (Priority Queues)

#### Core Concepts

A heap is a specialized tree-based data structure that satisfies the **heap property**. It's essentially a complete binary tree (all levels are fully filled except possibly the last, and nodes are filled from left to right) where the value of a parent node is compared to the values of its children nodes and organized accordingly.

Heaps are most commonly used to implement **Priority Queues**, where elements are served based on their priority, not necessarily their insertion order (unlike a standard queue).

**Types of Heaps:**

1.  **Min-Heap:**

      * The value of each node is less than or equal to the values of its children.
      * The smallest element is always at the root.
      * Ideal for efficiently retrieving the minimum element.

2.  **Max-Heap:**

      * The value of each node is greater than or equal to the values of its children.
      * The largest element is always at the root.
      * Ideal for efficiently retrieving the maximum element.

**Heap Property:**

  * **Min-Heap Property:** `Parent Node <= Child Node`
  * **Max-Heap Property:** `Parent Node >= Child Node`

**Structure (Implicit Array Representation):**
Heaps are typically implemented using an array (or Python list) because of their complete binary tree nature.

  * If a node is at index `i`:
      * Its left child is at `2*i + 1`.
      * Its right child is at `2*i + 2`.
      * Its parent is at `(i - 1) // 2`.
  * This array representation allows for efficient navigation without explicit pointers.

**Key Operations:**

  * **Insert (Push/heappush):** Add a new element. The element is added to the end of the array and then "bubbled up" (swapped with its parent) until the heap property is restored. Time: $O(\\log N)$.
  * **Extract Min/Max (Pop/heappop):** Remove and return the root element (min for min-heap, max for max-heap). The last element in the array replaces the root, and then "bubbled down" (swapped with its smallest/largest child) until the heap property is restored. Time: $O(\\log N)$.
  * **Peek Min/Max:** Return the root element without removing it. Time: $O(1)$.
  * **Heapify:** Build a heap from an arbitrary array of elements. Time: $O(N)$ (surprisingly, not $N \\log N$ for building from scratch).

**Practical Intuition:**
Imagine a management hierarchy where the "boss" (root) is always the person with the lowest/highest priority task. When a new task comes in, it's added, and then people shuffle around until the "boss" has the correct priority again. When the "boss" finishes their task, someone else becomes the new boss, and the shuffling continues.

**Use Cases:**

  * **Priority Queues:** The primary application. Used in operating system schedulers, event simulators, network routers.
  * **Heap Sort:** An efficient $O(N \\log N)$ sorting algorithm.
  * **Graph Algorithms:**
      * **Dijkstra's Algorithm:** For finding shortest paths in weighted graphs, a min-priority queue efficiently extracts the vertex with the smallest tentative distance.
      * **Prim's Algorithm:** For finding Minimum Spanning Trees, a min-priority queue selects the edge with the minimum weight.
  * **Finding K-th Smallest/Largest Elements:** Efficiently finding top K elements from a large stream or array.
  * **Median of a Stream:** Maintaining the median of dynamically arriving data.

**Time and Space Complexity:**

| Operation       | Time Complexity (Average & Worst) | Notes                                                                             |
| :-------------- | :-------------------------------- | :-------------------------------------------------------------------------------- |
| Insert          | $O(\\log N)$                       | `heapq.heappush()`                                                                |
| Extract Min/Max | $O(\\log N)$                       | `heapq.heappop()`                                                                 |
| Peek Min/Max    | $O(1)$                            | `heap[0]`                                                                         |
| Heapify (build) | $O(N)$                            | `heapq.heapify()` - for building from existing list.                              |
| Decrease/Increase Key | $O(\\log N)$ (if index known) | Not directly supported by `heapq`, would involve delete + insert for arbitrary nodes. |

**Space Complexity:** $O(N)$ to store $N$ elements in the underlying array.

#### Python 3.11 Usage (`heapq`)

Python's `heapq` module provides an implementation of the heap queue algorithm. Importantly, it implements a **min-heap** by default. There is no built-in max-heap. To simulate a max-heap, you store elements as their negative values.

```python
import heapq

# --- Min-Heap Operations ---

# 1. Initialize an empty list (will be used as a heap)
min_heap = []

# 2. Insert elements (heappush)
heapq.heappush(min_heap, 4)
heapq.heappush(min_heap, 1)
heapq.heappush(min_heap, 7)
heapq.heappush(min_heap, 2)
print(f"Min-heap after pushes: {min_heap}") # Output: [1, 2, 7, 4] (internal array, not necessarily sorted)
                                            # Note: only heap[0] is guaranteed to be min

# 3. Peek minimum element (access the first element of the list)
if min_heap:
    print(f"Min element (peek): {min_heap[0]}") # Output: 1

# 4. Extract minimum element (heappop)
smallest = heapq.heappop(min_heap)
print(f"Extracted smallest: {smallest}, Heap now: {min_heap}") # Output: Extracted smallest: 1, Heap now: [2, 4, 7]

heapq.heappush(min_heap, 0)
print(f"Min-heap after another push: {min_heap}") # Output: [0, 4, 7, 2]

# 5. Heapify an existing list (build a heap in-place)
data = [3, 1, 4, 1, 5, 9, 2, 6]
heapq.heapify(data) # Transforms list into a min-heap in O(N) time
print(f"Heapified list: {data}") # Output: [1, 1, 2, 3, 5, 9, 4, 6]

# 6. Get N smallest/largest elements (nlargest, nsmallest)
print(f"3 smallest elements from original data: {heapq.nsmallest(3, [3, 1, 4, 1, 5, 9, 2, 6])}") # Output: [1, 1, 2]
print(f"3 largest elements from original data: {heapq.nlargest(3, [3, 1, 4, 1, 5, 9, 2, 6])}")   # Output: [9, 6, 5]

# --- Simulating a Max-Heap ---
# Store elements as their negative values.
max_heap = []

heapq.heappush(max_heap, -4)
heapq.heappush(max_heap, -1)
heapq.heappush(max_heap, -7)
heapq.heappush(max_heap, -2)
print(f"Internal max-heap (stored as negatives): {max_heap}") # Output: [-7, -4, -1, -2]

# Peek max element
if max_heap:
    print(f"Max element (peek): {-max_heap[0]}") # Output: 7

# Extract max element
largest = -heapq.heappop(max_heap) # Pop the smallest negative (which is largest positive) and negate it
print(f"Extracted largest: {largest}, Max-heap now: {max_heap}") # Output: Extracted largest: 7, Max-heap now: [-4, -2, -1]

# Pushing tuples for custom priority (e.g., (priority, value))
# heapq compares tuples lexicographically (first element, then second, etc.)
priority_queue = []
heapq.heappush(priority_queue, (2, "Task B"))
heapq.heappush(priority_queue, (1, "Task A"))
heapq.heappush(priority_queue, (3, "Task C"))
print(f"Priority queue: {priority_queue}") # Output: [(1, 'Task A'), (2, 'Task B'), (3, 'Task C')]
print(f"Highest priority task: {heapq.heappop(priority_queue)}") # Output: (1, 'Task A')
```

**Best Practices:**

  * **`heapq` for Heaps/Priority Queues:** Always use the `heapq` module for heap implementations in Python. Don't try to roll your own unless it's a specific interview challenge to implement `heappush`/`heappop` from scratch.
  * **Min-Heap by Default:** Remember `heapq` is a min-heap. If you need a max-heap, negate the values you store and negate them back when you retrieve. For objects, you can define `__lt__` (less than) in a wrapper class or use tuples where the first element is the priority.
  * **Tuples for Custom Priority:** When elements have multiple attributes and you need to prioritize based on one or more, store them as `(priority_value, actual_data)`. If priority values are tied, the next elements in the tuple are used for comparison.

#### Problem-Solving Patterns

Heaps are excellent for problems requiring efficient retrieval of the minimum or maximum element, or for maintaining order in a dynamic collection.

1.  **Top K Elements:**

      * **Concept:** Find the $k$ smallest/largest elements from a collection (array, stream, etc.).
      * **Method:** Use a min-heap of size $k$ to find $k$ largest elements (or a max-heap of size $k$ for $k$ smallest).
          * For $k$ largest: Iterate through items. If heap size is less than $k$, push. Else, if current item is larger than `heap[0]`, pop `heap[0]` and push current item.
      * **Examples:** Top K Frequent Elements, Kth Largest Element in an Array, K Closest Points to Origin.

2.  **Median of a Stream:**

      * **Concept:** Maintain the median of a dynamically growing sequence of numbers.
      * **Method:** Use two heaps: a max-heap for the lower half of numbers and a min-heap for the upper half. Ensure their sizes are balanced (differ by at most 1).
      * **Examples:** Find Median from Data Stream.

3.  **Scheduling/Event Simulators:**

      * **Concept:** Process events or tasks in order of their priority or time.
      * **Method:** Store events in a min-heap ordered by their timestamp/priority. Always process the minimum.

4.  **Graph Algorithms (Dijkstra's, Prim's):**

      * **Concept:** As mentioned, heaps are crucial for optimizing these algorithms from $O(V^2)$ to $O(E \\log V)$ by efficiently selecting the next vertex/edge.

#### Handling Large Inputs / Constraints

  * **Memory Usage:** Heaps are $O(N)$ space. For very large datasets, this might still be a concern. However, for "top K" problems, they offer an advantage over sorting ($O(N \\log N)$) by only requiring $O(K)$ space.
  * **Time Complexity:** The $O(\\log N)$ factor for push/pop means that even for $N=10^5$ or $10^6$, operations are fast. $N \\log N$ operations are generally acceptable for $N \\le 10^6$.
  * **Custom Objects:** When storing custom objects in a heap, ensure they are comparable (implement `__lt__` method in your class) or wrap them in tuples with a comparable priority value as the first element.

#### Typical FAANG Problem Example

Let's look at the "Top K Frequent Elements" problem, a quintessential heap application.

**Problem Description: "Top K Frequent Elements"** (LeetCode Medium)

Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in any order.

**Constraints:**

  * `1 <= nums.length <= 10^5`
  * `k` is in the range `[1, the number of unique elements in the array]`.
  * It is guaranteed that the answer is unique, meaning there is only one set of `k` most frequent elements.

**Thought Process & Hints:**

1.  **Understanding the Goal:** We need the $k$ elements that appear most often.

2.  **Initial Thoughts (and why a simple sort might be inefficient):**

      * Count frequencies: Use a hash map (`Counter`) to get frequency of each number. $O(N)$.
      * Sort based on frequencies: Convert the hash map into a list of (number, frequency) tuples, then sort this list in descending order of frequency. This would be $O(U \\log U)$ where $U$ is the number of unique elements. Then take the top $k$. Overall $O(N + U \\log U)$. If $U \\approx N$, this is $O(N \\log N)$. This is acceptable, but can we do better if $K$ is much smaller than $N$?

3.  **Optimization with a Min-Heap (for Top K Largest):**

      * We want the "largest" frequencies. To get the largest $k$ elements, we use a *min-heap* of size $k$.
      * Why a min-heap? Because the smallest element in the min-heap will be at the root. If we find an element with a frequency larger than this smallest element, we can replace it, ensuring the heap always contains the $k$ largest frequencies seen so far.

4.  **Algorithm Sketch:**

    1.  **Frequency Count:** Use `collections.Counter` (or a `dict`) to count the frequency of each number in `nums`. This takes $O(N)$ time.
          * Example: `nums = [1,1,1,2,2,3], k = 2` -\> `counts = {1:3, 2:2, 3:1}`
    2.  **Build a Min-Heap:** Initialize an empty min-heap.
    3.  **Populate Heap:** Iterate through the `(number, frequency)` pairs from the `counts` map:
          * For each `(num, freq)` pair, push `(freq, num)` onto the min-heap. (Push `freq` first so `heapq` orders by frequency).
          * If the size of the min-heap exceeds `k`, `heappop` the smallest element (which will be the item with the smallest frequency among the current top `k`). This ensures the heap always maintains at most `k` elements, and those are the ones with the largest frequencies encountered so far.
    4.  **Extract Results:** Once all elements are processed, the min-heap contains the `k` most frequent elements. Pop all elements from the heap and extract their numbers.
          * Note: The order doesn't matter, so popping them will give them in increasing order of frequency, but that's fine.

5.  **Complexity Analysis:**

      * **Time Complexity:**
          * Frequency Counting: $O(N)$.
          * Populating Heap: For each of the $U$ unique elements, we do a `heappush` ($O(\\log k)$) and potentially a `heappop` ($O(\\log k)$). Total for this step: $O(U \\log k)$.
          * Extracting Results: $k$ `heappop` operations, $O(k \\log k)$.
          * Total: $O(N + U \\log k)$. Since $U \\le N$, this is $O(N + N \\log k)$. If $k$ is small, this is closer to $O(N)$.
      * **Space Complexity:**
          * Frequency map: $O(U)$.
          * Min-heap: $O(k)$.
          * Total: $O(U + k)$.

This heap-based approach is superior to full sorting when $k$ is significantly smaller than $N$.

#### System Design Relevance

  * **Load Balancing & Task Prioritization:** In a system with many tasks or requests, a priority queue (implemented with a heap) can ensure that critical or time-sensitive tasks are processed first.
  * **Network Packet Schedulers:** Routers might use priority queues to prioritize certain types of network traffic (e.g., voice data over file downloads).
  * **Operating System Schedulers:** Managing processes based on their priority or remaining time slice often involves a priority queue.
  * **Event-Driven Simulations:** Simulating complex systems (e.g., queuing systems, traffic simulations) uses an event queue ordered by time, often implemented with a heap.
  * **Graph Algorithms in Distributed Systems:** While the core algorithms run locally, the concepts of finding shortest paths or minimum spanning trees are relevant for network topology, message routing, or resource allocation in distributed environments.
  * **Log Processing/Monitoring:** Identifying the "top N" most frequent errors, slowest queries, or highest-traffic endpoints from large streams of logs.

**Challenge to the Reader:**
The "Find Median from Data Stream" problem (LeetCode Hard) is a classic example of using two heaps to maintain a balanced data structure. How would you design a data structure that efficiently supports adding numbers and finding the median, using a min-heap and a max-heap? What is the logic for balancing their sizes?