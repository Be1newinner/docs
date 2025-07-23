## FAANG SDE 1 Full Stack Developer Interview Prep: Data Structures & Algorithms Index

---

#### **Module 1: Foundational Data Structures & Their Associated Algorithms/Problems**

1.  **Arrays (Python Lists)**
    * Core Concepts
    * Python 3.11 Usage
    * Problem-Solving Patterns (Two Pointers, Sliding Window, Prefix Sums)
    * **Handling Large Inputs / Constraints**
    * Typical FAANG Problem Example
    * System Design Relevance
    * **Recommended LeetCode Problems:**
        * Two Sum (Easy)
        * Container With Most Water (Medium)
        * 3Sum (Medium)
        * Maximum Subarray (Easy)
        * Rotate Array (Medium)
        * Merge Intervals (Medium)

2.  **Hash Maps / Hash Tables (Python Dictionaries)**
    * Core Concepts
    * Python 3.11 Usage (`dict`, `defaultdict`, `Counter`)
    * Problem-Solving Patterns (Frequency Counting, Optimization)
    * **Handling Large Inputs / Constraints**
    * Typical FAANG Problem Example
    * System Design Relevance
    * **Recommended LeetCode Problems:**
        * Valid Anagram (Easy)
        * Longest Substring Without Repeating Characters (Medium)
        * Top K Frequent Elements (Medium)
        * Subarray Sum Equals K (Medium)

3.  **Linked Lists**
    * Core Concepts (Singly, Doubly, Circular)
    * Python 3.11 Implementation
    * Problem-Solving Patterns (Fast & Slow Pointers, Reversal)
    * **Handling Large Inputs / Constraints**
    * Typical FAANG Problem Example
    * System Design Relevance
    * **Recommended LeetCode Problems:**
        * Reverse Linked List (Easy)
        * Merge Two Sorted Lists (Easy)
        * Linked List Cycle (Easy)
        * Remove Nth Node From End of List (Medium)

4.  **Stacks**
    * Core Concepts (LIFO)
    * Python 3.11 Usage (`list`, `collections.deque`)
    * Problem-Solving Patterns (Parentheses, Monotonic Stack)
    * **Handling Large Inputs / Constraints**
    * Typical FAANG Problem Example
    * System Design Relevance
    * **Recommended LeetCode Problems:**
        * Valid Parentheses (Easy)
        * Min Stack (Medium)
        * Daily Temperatures (Medium)
        * Implement Queue using Stacks (Easy)

5.  **Queues**
    * Core Concepts (FIFO)
    * Python 3.11 Usage (`collections.deque`, `queue.Queue`)
    * Problem-Solving Patterns (BFS Traversal)
    * **Handling Large Inputs / Constraints**
    * Typical FAANG Problem Example
    * System Design Relevance
    * **Recommended LeetCode Problems:**
        * Implement Queue using Stacks (Easy) - *revisit from Stack perspective too*
        * Walls and Gates (Medium) - *BFS application*
        * Number of Recent Calls (Easy)

6.  **Trees**
    * Core Concepts (Binary, BST, Terminology)
    * Python 3.11 Implementation & Traversals (DFS, BFS)
    * Problem-Solving Patterns (Recursion)
    * **Handling Large Inputs / Constraints**
    * Typical FAANG Problem Example
    * System Design Relevance
    * **Recommended LeetCode Problems:**
        * Maximum Depth of Binary Tree (Easy)
        * Validate Binary Search Tree (Medium)
        * Binary Tree Level Order Traversal (Medium)
        * Symmetric Tree (Easy)
        * Invert Binary Tree (Easy)

7.  **Heaps (Priority Queues)**
    * Core Concepts (Min-Heap, Max-Heap)
    * Python 3.11 Usage (`heapq`)
    * Problem-Solving Patterns (Top K, Median Stream)
    * **Handling Large Inputs / Constraints**
    * Typical FAANG Problem Example
    * System Design Relevance
    * **Recommended LeetCode Problems:**
        * Kth Largest Element in an Array (Medium)
        * Top K Frequent Elements (Medium) - *revisit with Heap*
        * Find Median from Data Stream (Hard - *stretch*)

8.  **Graphs**
    * Core Concepts (Vertices, Edges, Directed/Undirected, Weighted)
    * Representations (Adjacency Matrix, Adjacency List)
    * Python 3.11 Implementation (Adjacency List)
    * Basic Traversal (BFS, DFS)
    * **Handling Large Inputs / Constraints**
    * Typical FAANG Problem Example
    * System Design Relevance
    * **Recommended LeetCode Problems:**
        * Number of Islands (Medium)
        * Clone Graph (Medium)
        * Course Schedule (Medium)
        * Rotting Oranges (Medium)
        * Pacific Atlantic Water Flow (Medium)
#### **Module 2: Essential Algorithms & General Problem-Solving Techniques (Cross-Cutting)**

This section covers algorithms and techniques that are often applied across various data structures, or represent a general approach to problem-solving.

9.  **Sorting Algorithms**
    * Concepts (Comparison vs. Non-Comparison, Stability)
    * Merge Sort ($O(N \log N)$)
    * Quick Sort ($O(N \log N)$ average)
    * Heap Sort ($O(N \log N)$)
    * Python 3.11 Usage (`list.sort()`, `sorted()`)
    * **Handling Large Inputs / Constraints**
    * **Recommended LeetCode Problems:**
        * Sort an Array (Medium)
        * K Closest Points to Origin (Medium)
        * Meeting Rooms II (Medium)

10.  **Binary Search**
    * Core Concepts (Iterative/Recursive)
    * Binary Search Variants (First/Last Occurrence, on Answer/Properties)
    * **Handling Large Inputs / Constraints**
    * **Recommended LeetCode Problems:**
        * Search in Rotated Sorted Array (Medium)
        * Find Minimum in Rotated Sorted Array (Medium)
        * Sqrt(x) (Easy)
        * Koko Eating Bananas (Medium)

11.  **Recursion & Backtracking**
    * Core Concepts (Base Cases, Call Stack, Choice/Explore/Unchoose)
    * Backtracking Paradigm
    * Python 3.11 Implementation
    * **Handling Large Inputs / Constraints**
    * **Recommended LeetCode Problems:**
        * Subsets (Medium)
        * Permutations (Medium)
        * Combinations (Medium)
        * Generate Parentheses (Medium)
        * N-Queens (Hard - *conceptual for SDE1*)

12.  **Dynamic Programming (DP)**
    * Core Concepts (Overlapping Subproblems, Optimal Substructure)
    * Memoization (Top-Down)
    * Tabulation (Bottom-Up)
    * Python 3.11 Usage (`functools.lru_cache`)
    * **Handling Large Inputs / Constraints**
    * **Recommended LeetCode Problems:**
        * Climbing Stairs (Easy)
        * Coin Change (Medium)
        * Longest Increasing Subsequence (Medium)
        * House Robber (Medium)
        * Word Break (Medium)
        * Edit Distance (Hard - *conceptual for SDE1*)

13.  **Greedy Algorithms**
    * Core Concepts (Local vs. Global Optimum, When Applicable)
    * **Handling Large Inputs / Constraints**
    * **Recommended LeetCode Problems:**
        * Best Time to Buy and Sell Stock (Easy)
        * Jump Game (Medium)
        * Gas Station (Medium)
        * Activity Selection Problem (Classic)

14.  **Advanced Graph Algorithms (Conceptual for SDE1, Focus on intuition)**
    * Dijkstra's Algorithm (Single-Source Shortest Path - Non-Negative Weights)
    * Floyd-Warshall Algorithm (All-Pairs Shortest Path)
    * Minimum Spanning Tree (Kruskal's, Prim's)
    * Union-Find (Disjoint Set Union)
    * **Handling Large Inputs / Constraints**
    * **Recommended LeetCode Problems:**
        * Number of Provinces (Medium) - *Union-Find or DFS/BFS*
        * Network Delay Time (Medium) - *Dijkstra's*

15.  **Advanced Recursion Backtracking**
    * Deeper Insights into State Management
    * Advanced Pruning Techniques
    * Relationship with State-Space Search
    * Python 3.11 Implementation Nuances
    * Handling Large Inputs / Constraints (Revisited)
    * Typical FAANG Problem Example
    * System Design Relevance

16.  **Bit Manipulation (Basic)**
    * Core Operations (`&`, `|`, `^`, `~`, `<<`, `>>`)
    * Use Cases (Space Optimization, Flags, Specific Problem Types)
    * **Handling Large Inputs / Constraints**
    * **Recommended LeetCode Problems:**
        * Single Number (Easy)
        * Number of 1 Bits (Easy)
        * Missing Number (Easy)
        * Power of Two (Easy)