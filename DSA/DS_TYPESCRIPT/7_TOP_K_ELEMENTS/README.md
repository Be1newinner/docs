The "Top K Elements" problem is a common and important pattern in data structures usage, typically involving selecting the largest or smallest K elements from a collection of data.

## What is "Top K Elements"?

"Top K Elements" refers to the problem of finding either the K largest or K smallest elements in a dataset efficiently. Instead of sorting the entire dataset, which can be costly, specialized data structures or algorithms help in accessing the top K entries quickly.

## Which Data Structures are used?

1. **Heaps (Priority Queues):**

   - Commonly used because they efficiently maintain the top K elements.
   - Min-heap for top K largest elements (size limited to K so smaller elements get ejected).
   - Max-heap for top K smallest elements.

2. **Balanced Binary Search Trees (BSTs):**

   - Can keep elements in sorted order.
   - Useful if you require maintaining order while inserting or deleting dynamically.

3. **Arrays + Sorting:**

   - Simple approach for small datasets or when only one query is needed.
   - Sort the array and take the first or last K elements.

4. **Hash Maps with Heaps:**
   - For frequency-based "top K" problems (e.g., top K frequent elements), hashmap + heap combo is used.

## Why is it used?

- To optimize time complexity for selection problems.
- Avoid sorting the entire dataset.
- Used in real-world scenarios such as leaderboards, recommendation systems, finding most frequent items, data analytics, and streaming data processing.

## Examples Per Data Structure

| Data Structure            | Usage                             | Example Use Case                                 | Brief Example Concept                                             |
| ------------------------- | --------------------------------- | ------------------------------------------------ | ----------------------------------------------------------------- |
| Min-Heap (Priority Queue) | Find top K largest elements       | Find top 3 highest scores from a large exam      | Keep heap size K; push elements; pop smaller ones                 |
| Max-Heap                  | Find top K smallest elements      | Finding the smallest 3 elements in data          | Same as min-heap but reversed logic                               |
| Balanced BST (e.g., AVL)  | Dynamic top K with ordered access | Streaming top K elements with insert/delete      | Insert elements, maintain balanced tree and retrieve K max or min |
| Array + Sorting           | Static top K once                 | Small array where full sort is affordable        | Sort the array, pick top K                                        |
| HashMap + Heap            | Top K frequent elements           | Frequent search queries or trending hashtag list | Count frequencies with hashmap, store top K in heap               |

## EXTRA

Sometimes, using sorting or a quickselect algorithm (for k-th largest) can be easier to implement quickly and accepted by interviewers as a valid approach.
