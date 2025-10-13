# Dynamic Programming: What and Why

Dynamic Programming (DP) is a method to solve complex problems by breaking them into smaller overlapping subproblems, solving each subproblem once, and storing their results for future use. This avoids repetitive calculations, making algorithms more efficient.

## Where and Why Use Dynamic Programming?

- **Use Cases:** DP is especially useful in optimization problems where you want the best or minimum/maximum solution, such as the Knapsack problem or finding the Longest Common Subsequence (LCS).
- **Why Use It?** Because these problems usually involve _overlapping subproblems_ (the same smaller problems appear multiple times) and _optimal substructure_ (an optimal solution can be built from optimal solutions of subproblems).

## How It Works

- Define your problem’s **state** (parameters describing a subproblem).
- Write a **recurrence relation** that expresses the solution of a problem in terms of its subproblems.
- Compute solutions either:
  - **Top-down (memoization):** Recursively solve subproblems and store their answers.
  - **Bottom-up (tabulation):** Iteratively solve smaller subproblems first and build up.

---

## In interviews, Dynamic Programming (DP) questions often test problem-solving skills by leveraging overlapping subproblems and optimal substructure properties. Here are common kinds of DP questions you can expect:

### Classic and Frequently Asked DP Interview Questions

- Fibonacci Sequence (counting with overlapping subproblems)
- Climbing Stairs (counting paths with recurrence like Fibonacci)
- Coin Change Problem (optimization for minimum coins or counting ways)
- Knapsack Problem (0/1 and unbounded variants for maximizing value)
- Longest Common Subsequence (LCS) (string comparison problems)
- Longest Increasing Subsequence (LIS) (array sequence optimization)
- Edit Distance (string transformation with minimum operations)
- Maximum Subarray (Kadane’s algorithm for max sum subarray)
- Partition Equal Subset Sum (checking if array subsets sum equally)
- Word Break Problem (string segmentation using dictionary)

### Other DP Problem Patterns Seen in Interviews

- Matrix Chain Multiplication (optimization on matrix operations order)
- Rod Cutting (maximizing profit from cutting rods)
- Egg Dropping Puzzle (minimizing worst-case attempts)
- Palindrome Partitioning (min cuts to partition palindrome substrings)
- Dice Throw Problem (counting ways to achieve sum with dice rolls)
- Boolean Parenthesization Problem (count valid parenthesizations for logic expressions)

---

## Dynamic Programming (DP) often involves combining with other problem-solving patterns to handle complex problems efficiently. Some common patterns used alongside DP are:

### Common Patterns Used with DP

- **Sliding Window:** Sometimes DP problems involve optimizing a range or window in arrays/strings. Sliding window can be combined to reduce complexity.
- **Two Pointers:** Useful for DP on sequences or arrays where simultaneous traversal or partition is needed, e.g., longest palindrome substring.

- **Backtracking with Memoization:** Exploring all possibilities but storing results of subproblems to avoid repeated work, useful in combinatorial DP problems.

- **Bitmasking:** To efficiently represent states especially when dealing with subsets or combinations, frequently used in DP on sets or graphs.

- **Greedy + DP:** Certain optimization problems start with greedy choices and DP verifies or improves upon them.

- **Graph Traversals (BFS/DFS) + DP:** When DP is applied over paths or states modeled as graph nodes, e.g., shortest path with DP, counting paths.

- **Divide and Conquer + DP (e.g., Memoized recursion):** Overlapping subproblems solved with recursive division plus caching.

These combined approaches help tailor DP to various problem types and constraints, making it a versatile and powerful technique for interviews and real-world problems. Understanding how DP interplays with these patterns boosts flexibility in solving challenges.
