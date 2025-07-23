### 12\. Dynamic Programming (DP)

#### Core Concepts

Dynamic Programming is an optimization technique used primarily for problems that can be broken down into subproblems, where the solutions to these subproblems can be reused multiple times. It's about remembering past results to avoid redundant calculations.

**Two Core Properties for DP Applicability:**

1.  **Overlapping Subproblems:**

      * The problem can be divided into smaller subproblems that are not independent; they share common sub-subproblems.
      * **Example:** In computing Fibonacci sequence, `fib(5)` needs `fib(4)` and `fib(3)`. `fib(4)` needs `fib(3)` and `fib(2)`. Notice `fib(3)` is computed twice. DP aims to compute `fib(3)` only once and store its result.
      * If there are no overlapping subproblems, a simple divide-and-conquer (like Merge Sort) might be sufficient.

2.  **Optimal Substructure:**

      * An optimal solution to the problem can be constructed from optimal solutions of its subproblems.
      * **Example:** The shortest path from A to C through B. If the path A-B-C is the shortest path from A to C, then the path A-B must be the shortest path from A to B.
      * If a problem doesn't have optimal substructure, then solving subproblems optimally doesn't guarantee an optimal solution for the main problem (e.g., finding the longest path in a graph with cycles).

**Two Main Approaches to DP:**

1.  **Memoization (Top-Down DP):**

      * This is a recursive approach combined with caching.
      * You start with the original problem and recursively break it down.
      * Before computing a subproblem, check if its result is already stored (memoized). If yes, return the stored result.
      * If not, compute the result, store it, and then return it.
      * **Analogy:** You need to solve a big puzzle. You try to solve it recursively. If you encounter a smaller piece you've already solved and recorded, you just grab the solution. Otherwise, you solve it, record it, and then use it.

2.  **Tabulation (Bottom-Up DP):**

      * This is an iterative approach.
      * You build up the solution from the base cases (smallest subproblems) to the final solution.
      * You typically use an array (DP table) to store the results of subproblems.
      * **Analogy:** You need to build a tower. You start by building the foundation (base cases), then build the next layer using the foundation, then the next layer using the previous, until the entire tower is built.

#### Python 3.11 Implementation (Top-down (Memoization) and Bottom-up (Tabulation))

Let's use the classic Fibonacci sequence to illustrate both approaches.

**Problem: Fibonacci Number**
`F(0) = 0`, `F(1) = 1`
`F(n) = F(n - 1) + F(n - 2)`, for `n > 1`.

```python
# --- 1. Memoization (Top-Down DP) ---
# Uses a dictionary (or list/array) to store computed results.
# @functools.lru_cache is a convenient decorator for memoization in Python.
import functools

# Using a dictionary for memoization
def fib_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    
    result = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    memo[n] = result # Store the result
    return result

# Using functools.lru_cache (cleaner for simple functions)
@functools.lru_cache(None) # None means unlimited cache size
def fib_lru_cache(n):
    if n <= 1:
        return n
    return fib_lru_cache(n - 1) + fib_lru_cache(n - 2)

print("--- Fibonacci (Memoization / Top-Down) ---")
print(f"fib_memo(10): {fib_memo(10)}") # Output: 55
print(f"fib_lru_cache(10): {fib_lru_cache(10)}") # Output: 55
# Clear cache if you reuse function for different tests or with different constraints
fib_lru_cache.cache_clear()


# --- 2. Tabulation (Bottom-Up DP) ---
# Builds up the solution iteratively from base cases.
def fib_tab(n):
    if n <= 1:
        return n

    # Create a DP table (array) to store results
    # dp[i] will store fib(i)
    dp = [0] * (n + 1) # Size n+1 because we need up to dp[n]

    # Base cases
    dp[0] = 0
    dp[1] = 1

    # Fill the DP table iteratively
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    
    return dp[n]

print("\n--- Fibonacci (Tabulation / Bottom-Up) ---")
print(f"fib_tab(10): {fib_tab(10)}") # Output: 55
print(f"fib_tab(0): {fib_tab(0)}")   # Output: 0
print(f"fib_tab(1): {fib_tab(1)}")   # Output: 1

# --- Space-Optimized Tabulation (for Fibonacci) ---
# Notice fib(i) only depends on fib(i-1) and fib(i-2).
# We only need to store the two previous values.
def fib_space_optimized(n):
    if n <= 1:
        return n
    
    a, b = 0, 1 # Represents fib(i-2) and fib(i-1) respectively
    for _ in range(2, n + 1):
        # Calculate current fib, then update for next iteration
        next_fib = a + b
        a = b
        b = next_fib
    return b

print("\n--- Fibonacci (Space-Optimized Tabulation) ---")
print(f"fib_space_optimized(10): {fib_space_optimized(10)}") # Output: 55
print(f"fib_space_optimized(0): {fib_space_optimized(0)}")   # Output: 0
print(f"fib_space_optimized(1): {fib_space_optimized(1)}")   # Output: 1
```

**Complexity Analysis (for Fibonacci):**

  * **Time Complexity:**
      * Naive Recursive: $O(2^N)$
      * Memoization (Top-Down DP): $O(N)$ - Each subproblem computed once.
      * Tabulation (Bottom-Up DP): $O(N)$ - Loop runs $N$ times.
  * **Space Complexity:**
      * Naive Recursive: $O(N)$ for recursion stack.
      * Memoization (Top-Down DP): $O(N)$ for recursion stack + $O(N)$ for memoization dictionary.
      * Tabulation (Bottom-Up DP): $O(N)$ for DP table.
      * Space-Optimized Tabulation: $O(1)$ (constant extra space).

#### Problem-Solving Patterns

DP problems often fall into several common categories:

1.  **1D DP:**

      * Problems where the state only depends on a single variable (e.g., `dp[i]` depends on `dp[i-1]`, `dp[i-2]`).
      * **Examples:** Fibonacci, Climbing Stairs, House Robber, Coin Change (if target is 1D).

2.  **2D DP:**

      * Problems where the state depends on two variables (e.g., `dp[i][j]` depends on neighbors in a 2D grid/matrix).
      * **Examples:** Unique Paths, Longest Common Subsequence, Edit Distance, Knapsack (unbounded/0/1).

3.  **DP on Strings:**

      * Often involve operations like finding subsequences, substrings, or transformations between strings.
      * **Examples:** Longest Palindromic Substring, Regular Expression Matching.

4.  **DP on Trees:**

      * Solving problems on trees by combining results from subtrees. Often uses memoization.
      * **Examples:** Diameter of Binary Tree, Maximum Path Sum.

5.  **Interval DP:**

      * Problems where the solution for an interval `[i, j]` depends on solutions for sub-intervals.
      * **Examples:** Burst Balloons, Palindromic Partitioning.

6.  **Bitmask DP:**

      * When the state involves subsets of elements, and $N$ is small (e.g., $N \\le 20$), a bitmask can represent the subset.
      * **Examples:** Traveling Salesperson Problem (TSP variants), problems involving unique combinations or sets of items.

**Steps to Approach a DP Problem:**

1.  **Identify if DP is applicable:** Look for overlapping subproblems and optimal substructure. Can you define the problem recursively?
2.  **Define the DP State:** What information do you need to store to solve subproblems? `dp[i]`, `dp[i][j]`, `dp[i][j][k]`? What does each state represent?
3.  **Define the Base Cases:** What are the smallest, simplest subproblems that can be solved directly?
4.  **Define the Recurrence Relation (Transition):** How do you calculate the current state `dp[i]` (or `dp[i][j]`) using previously computed states?
5.  **Determine the Order of Computation:**
      * **Memoization:** The order is implicit through recursion.
      * **Tabulation:** Determine the loops and their order to ensure all dependencies are met before computing a state.
6.  **Consider Space Optimization (Optional but good):** Can you reduce the DP table size if `dp[i]` only depends on a few previous states?

#### Handling Large Inputs / Constraints

  * **Recursion Depth (`RecursionError`):** For top-down DP, if `N` is very large, the recursion stack can overflow. In such cases, prefer the iterative (tabulation) approach.
  * **Time Complexity:** DP transforms exponential brute-force solutions into polynomial time (e.g., $O(N)$, $O(N^2)$, $O(N^3)$). This makes solutions feasible for $N$ up to $10^3$ or $10^4$.
  * **Space Complexity:** DP tables often require $O(N)$, $O(N^2)$ or more space.
      * For $O(N^2)$ space, $N$ can typically go up to $2000-3000$ without exceeding common memory limits (e.g., $2000^2 \\times 4$ bytes for ints is 16MB, which is fine).
      * If space is a concern, always look for **space optimization** (e.g., reducing $O(N)$ from $O(N^2)$ by only keeping track of the previous row in 2D DP).

#### Typical FAANG Problem Example

Let's use a 2D DP problem that is frequently encountered: **"Unique Paths"** (LeetCode Medium).

**Problem Description: "Unique Paths"**

There is a robot on an `m x n` grid. The robot is initially located at the top-left corner (`grid[0][0]`). The robot can only move either down or right at any point in time. The robot is trying to reach the bottom-right corner (`grid[m - 1][n - 1]`).

Given the two integers `m` and `n`, return the number of possible unique paths that the robot can take to reach the bottom-right corner.

**Constraints:**

  * `1 <= m, n <= 100` (Small enough for $O(M \\times N)$ or $O(M \\times N \\times \\text{some\_constant})$)

**Thought Process & Hints:**

1.  **Understanding the Goal:** Count paths from `(0,0)` to `(m-1, n-1)` moving only down or right.

2.  **Identify DP Properties:**

      * **Optimal Substructure:** To reach `(r, c)`, the robot must have come from either `(r-1, c)` (moving down) or `(r, c-1)` (moving right). The number of paths to `(r, c)` is the sum of paths to `(r-1, c)` and `(r, c-1)`. This is a clear recursive relationship.
      * **Overlapping Subproblems:** When computing paths to `(r,c)`, you'll need paths to `(r-1,c)` and `(r,c-1)`. These subproblems might be needed again for other paths (e.g., `(r-1,c)` is also a subproblem for `(r-1, c+1)`).

3.  **Define DP State:**

      * Let `dp[r][c]` be the number of unique paths from `(0,0)` to `(r,c)`.

4.  **Define Base Cases:**

      * `dp[0][0] = 1` (There's one way to reach the starting cell: by being there).
      * Any cell in the first row (`dp[0][c]`) can only be reached by moving right from `(0, c-1)`. So, `dp[0][c] = 1` for all `0 <= c < n`.
      * Any cell in the first column (`dp[r][0]`) can only be reached by moving down from `(r-1, 0)`. So, `dp[r][0] = 1` for all `0 <= r < m`.

5.  **Define Recurrence Relation:**

      * For any cell `(r, c)` where `r > 0` and `c > 0`:
          * `dp[r][c] = dp[r-1][c] + dp[r][c-1]`

6.  **Order of Computation (Tabulation):**

      * We need `dp[r-1][c]` and `dp[r][c-1]` to compute `dp[r][c]`.
      * This means we should iterate `r` from `0` to `m-1` and `c` from `0` to `n-1`.

<!-- end list -->

```python
def unique_paths(m, n):
    # Create a 2D DP table initialized with zeros
    dp = [[0] * n for _ in range(m)]

    # Base cases: First row and first column have only 1 path to reach them
    # (by moving only right for first row, or only down for first column)
    for r in range(m):
        dp[r][0] = 1
    for c in range(n):
        dp[0][c] = 1

    # Fill the DP table using the recurrence relation
    for r in range(1, m): # Start from 1 because row 0 is base case
        for c in range(1, n): # Start from 1 because col 0 is base case
            dp[r][c] = dp[r-1][c] + dp[r][c-1]
    
    # The result is in the bottom-right corner
    return dp[m-1][n-1]

print(f"Unique Paths (3x7 grid): {unique_paths(3, 7)}") # Output: 28
print(f"Unique Paths (2x2 grid): {unique_paths(2, 2)}") # Output: 2
print(f"Unique Paths (1x1 grid): {unique_paths(1, 1)}") # Output: 1
```

**Complexity Analysis:**

  * **Time Complexity:** $O(M \\times N)$ because we fill an $M \\times N$ DP table, and each cell takes $O(1)$ time.
  * **Space Complexity:** $O(M \\times N)$ for the DP table.

**Space Optimization for Unique Paths:**
Notice that `dp[r][c]` only depends on the current row (`dp[r][c-1]`) and the previous row (`dp[r-1][c]`). This means we can optimize space to $O(N)$ (if we iterate row by row) or $O(M)$ (if we iterate column by column).

```python
def unique_paths_space_optimized(m, n):
    # We only need the previous row's information.
    # dp_row[c] will store paths to (current_r, c)
    # The current value of dp_row[c] will use the previous row's dp_row[c] (which is dp[r-1][c])
    # and the current row's dp_row[c-1] (which is dp[r][c-1])
    
    dp_row = [1] * n # Initialize the first row (all 1s)

    for r in range(1, m): # Iterate for rows starting from the second row
        for c in range(1, n): # Iterate for columns starting from the second column
            # dp_row[c] (current cell) = dp_row[c] (value from previous row) + dp_row[c-1] (value from current row, prev column)
            dp_row[c] = dp_row[c] + dp_row[c-1]
            
    return dp_row[n-1]

print(f"Unique Paths (Space Optimized) (3x7 grid): {unique_paths_space_optimized(3, 7)}") # Output: 28
```

#### System Design Relevance

  * **Caching & Memoization:** The concept of memoization is directly applicable to caching frequently accessed or computationally expensive results in real-world systems. Examples include web server caches, database query caches, or function result caches.
  * **Resource Optimization:** DP principles can be used in optimizing resource allocation, scheduling tasks, or minimizing costs in various systems where subproblems overlap.
  * **Algorithm Design in Core Systems:** Algorithms for network routing, compiler optimization (code generation, instruction scheduling), bioinformatics (sequence alignment), and financial modeling often leverage DP principles.
  * **State Machines:** Problems modeled as state transitions can sometimes be solved with DP, where each state's properties are computed based on previous states.

**Challenge to the Reader:**
Consider the "Longest Common Subsequence" (LCS) problem. Given two strings `text1` and `text2`, return the length of their longest common subsequence. If there is no common subsequence, return 0. This is a classic 2D DP problem. How would you define `dp[i][j]`, its base cases, and its recurrence relation? How can this be adapted to find the actual subsequence, not just its length?