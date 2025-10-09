# PATTERNS

## 1. Prefix Sum
**What:** Pahele se cumulative sum array bna lo.  
**Use:** Fast range sum queries; subarray sums without recalculating.  
**How:** prefix[i] = prefix[i-1] + arr[i]; query = prefix[j] - prefix[i-1].

## 2. Two Pointers  ( DONE )
**What:** Do pointer start aur end se aage badhte hain.  
**Use:** Sorted arrays, pairs, substrings problems.  
**How:** Ek pointer start, dusra end; move based on condition (sum, comparison).

## 3. Sliding Window  ( DONE )
**What:** Fixed ya variable size window slide karke problem solve karo.  
**Use:** Longest/shortest substring/subarray, max sum fixed window.  
**How:** Expand right pointer, shrink left pointer condition ke hisaab se.

## 4. Fast & Slow Pointers  ( DONE )
**What:** Fast pointer 2 steps, slow pointer 1 step aage.  
**Use:** Cycle detection, middle element find karna linked lists mein.  
**How:** Speed difference se cycle ya meet point detect karo.

## 5. Linked List In-place Reversal  ( DONE )
**What:** Pointers ko reverse karke list ulta karo without extra space.  
**Use:** Reverse a linked list efficiently.  
**How:** 3 pointers (prev, current, next), link current to prev, move pointers forward.

## 6. Monotonic Stack  
**What:** Stack maintain karo increasing ya decreasing order mein.  
**Use:** Next greater/smaller element, histogram problems.  
**How:** Push with pops to maintain order.

## 7. Top K Elements  
**What:** Find top k largest/smallest/frequent elements efficiently.  
**Use:** Priority problems, frequency sorting.  
**How:** Use Min/Max heap of size k for O(n log k).

## 8. Overlapping Intervals  
**What:** Intervals ko start time se sort karo, phir merge karo.  
**Use:** Merge intervals, find conflicts.  
**How:** If current start ≤ last merged end → merge else new interval.

## 9. Modified Binary Search  
**What:** Classic BS with tweak to solve rotated arrays, search conditions.  
**Use:** Search in rotated/special sorted arrays.  
**How:** Adapt mid check conditions to skip sorted half.

## 10. Binary Tree Traversal  
**What:** DFS (In, Pre, Post) or BFS level order.  
**Use:** Tree processing tasks, path, printing.  
**How:** Recursion (DFS) or Queue (BFS).

## 11. Depth First Search (DFS)  
**What:** Explore depth wise nodes/graph paths using recursion or stack.  
**Use:** Graph traversal, connected components.  
**How:** Push neighbours, recurse deep.

## 12. Breadth First Search (BFS)  
**What:** Level wise traversal using queue.  
**Use:** Shortest path unweighted graph, level order.  
**How:** Enqueue start, dequeue and enqueue neighbours.

## 13. Matrix Traversal  
**What:** Row-column wise matrix traversal.  
**Use:** Matrix problems like search, path finding.  
**How:** Nested loops or BFS/DFS on grid.

## 14. Backtracking  
**What:** Try all options, undo if wrong (DFS with undo).  
**Use:** Permutations, subsets, sudoku.  
**How:** Choose, recurse, unchoose.

## 15. Dynamic Programming  
**What:** Store results of subproblems to avoid recomputation.  
**Use:** Optimization problems (knapsack, LCS).  
**How:** Define state, recurrence; build bottom up or memo top down.

## 16. Union Find (Disjoint Set)  
**What:** Efficiently merge sets and find representatives.  
**Use:** Connectivity, cycle detection in graph.  
**How:** Union by rank, path compression.

## 17. Trie (Prefix Tree)  
**What:** Tree of characters for prefix based queries.  
**Use:** Auto-complete, word search.  
**How:** Each node points to next char nodes.

## 18. Greedy Algorithms  
**What:** Choose locally optimal choice at each step.  
**Use:** Scheduling, interval selection, Huffman coding.  
**How:** Sort input, pick best immediate choice.

## 19. Topological Sort  
**What:** Linear order of DAG nodes with dependencies.  
**Use:** Job scheduling, course prerequisite order.  
**How:** DFS postorder or Kahn’s Algorithm (BFS + indegrees).

## 20. Bit Manipulation  
**What:** Use bitwise ops for fast computation.  
**Use:** Check bits, power of two, toggles.  
**How:** &, |, ^, <<, >> etc.

## 21. Sliding Window Maximum / Deque  
**What:** Find max in sliding window with deque to keep max candidates.  
**Use:** Fast max in subarrays.  
**How:** Remove out of window & smaller elements for max at front.

## 22. Segment Tree & Fenwick Tree (BIT)  
**What:** Data structure for fast range queries and updates.  
**Use:** Range sum/min/max queries dynamic array.  
**How:** Segment tree binary breaks, Fenwick tree bit tricks.