### 13. Greedy Algorithms

#### Core Concepts

A **Greedy Algorithm** is an algorithmic paradigm that makes the locally optimal choice at each stage with the hope of finding a global optimum. It never reconsiders its choices once made. The core idea is to build a solution incrementally, taking the best available option at each step without regard for future consequences.

**When does a Greedy Algorithm work? (The Two Properties):**

For a greedy algorithm to yield a globally optimal solution, the problem must exhibit two key properties:

1.  **Greedy Choice Property:**

      * A globally optimal solution can be reached by making a locally optimal (greedy) choice.
      * This means that there exists an optimal solution that contains the greedy choice. Making the greedy choice at each step does not prevent finding the overall optimal solution.
      * **Intuition:** "What seems like the best decision right now, will lead to the best overall result." This is the critical, and often hardest, property to prove.

2.  **Optimal Substructure:**

      * An optimal solution to the problem contains optimal solutions to subproblems. (This property is also shared with Dynamic Programming).
      * After making a greedy choice, the remaining subproblem is also an optimal subproblem.

**Distinguishing from Dynamic Programming:**

While both Greedy algorithms and Dynamic Programming rely on **Optimal Substructure**, they differ fundamentally in how they build the solution:

| Feature           | Greedy Algorithms                             | Dynamic Programming                          |
| :---------------- | :-------------------------------------------- | :------------------------------------------- |
| **Approach** | Makes a locally optimal choice at each step; never revisits. | Explores multiple options for subproblems and combines them optimally (memoization/tabulation). |
| **Subproblems** | Remaining subproblem is always *one specific* optimal subproblem. | Overlapping subproblems are solved once and results stored. |
| **Decision** | Always "take the best now".                    | "Take the best overall" (considering all future implications). |
| **Guarantees** | Only works for specific problems where greedy choice property holds (often harder to prove). | Works for any problem with optimal substructure and overlapping subproblems. |
| **Complexity** | Often simpler, faster ($O(N)$ or $O(N \\log N)$ after sorting) | Often more complex, typically polynomial ($O(N^2)$, $O(N^3)$, etc.) |
| **Exploration** | Single path exploration.                       | Multi-path exploration.                      |

**Analogy:**

  * **Greedy:** Imagine navigating a maze. At each junction, you take the path that *looks* like it leads directly to the exit, without looking ahead or considering other branches. If this works, the problem has the greedy choice property.
  * **Dynamic Programming:** You map out all possible paths from each junction to the exit, considering all options, and then choose the best overall path based on those calculations.

#### Python 3.11 Examples

Greedy algorithms are often simple to implement once the greedy choice is identified. Sorting is frequently a preprocessing step.

**Example: Coin Change (Minimum Coins - assuming standard denominations)**

Given an amount `target` and a list of coin denominations `coins` (e.g., `[1, 5, 10, 25]`), find the minimum number of coins to make the `target` amount.
*This greedy strategy works for standard coin systems (e.g., US currency) but NOT for arbitrary coin systems (e.g., `coins = [1, 3, 4]`, `target = 6` -\> greedy gives `4+1+1=3` coins, optimal is `3+3=2` coins).*

```python
def greedy_coin_change(coins, amount):
    # For greedy to work, coins must be sorted in descending order
    # (or you iterate from largest to smallest)
    coins.sort(reverse=True)
    
    num_coins = 0
    remaining_amount = amount
    
    print(f"Making change for {amount} with coins: {coins}")
    
    for coin in coins:
        if remaining_amount == 0:
            break
        
        # Take as many of the current coin as possible
        count = remaining_amount // coin
        num_coins += count
        remaining_amount -= count * coin
        
        print(f"  Used {count} x {coin}, Remaining: {remaining_amount}, Total coins: {num_coins}")
        
    if remaining_amount == 0:
        return num_coins
    else:
        # This part indicates greedy failed if remaining_amount > 0,
        # but for standard denominations, it will always be 0.
        return -1 # Cannot make exact change (only for non-standard coins)

print(f"Min coins for 63 with [1, 5, 10, 25]: {greedy_coin_change([1, 5, 10, 25], 63)}")
# Output:
# Making change for 63 with coins: [25, 10, 5, 1]
#   Used 2 x 25, Remaining: 13, Total coins: 2
#   Used 1 x 10, Remaining: 3, Total coins: 3
#   Used 0 x 5, Remaining: 3, Total coins: 3
#   Used 3 x 1, Remaining: 0, Total coins: 6
# Min coins for 63 with [1, 5, 10, 25]: 6

# Example where greedy FAILS (needs DP):
print(f"\nMin coins for 6 with [1, 3, 4] (Greedy attempt): {greedy_coin_change([1, 3, 4], 6)}")
# Output:
# Making change for 6 with coins: [4, 3, 1]
#   Used 1 x 4, Remaining: 2, Total coins: 1
#   Used 0 x 3, Remaining: 2, Total coins: 1
#   Used 2 x 1, Remaining: 0, Total coins: 3
# Min coins for 6 with [1, 3, 4] (Greedy attempt): 3 (Incorrect, optimal is 2 using 3+3)
```

#### Problem-Solving Patterns

1.  **Activity Selection Problem:**

      * **Concept:** Given a set of activities, each with a start and finish time, select the maximum number of non-overlapping activities.
      * **Greedy Choice:** Sort activities by their finish times. Always pick the activity that finishes earliest among the compatible ones.
      * **Why it works:** Choosing the earliest finishing activity leaves the maximum amount of time available for subsequent activities.

2.  **Huffman Coding:**

      * **Concept:** Build a prefix code (binary tree) to represent characters such that frequently occurring characters have shorter codes, leading to optimal data compression.
      * **Greedy Choice:** Repeatedly combine the two nodes with the smallest frequencies until only one node remains (the root of the Huffman tree).
      * **Why it works:** Placing less frequent characters deeper in the tree, and more frequent characters closer to the root, minimizes the total weighted path length, which is the total compressed size.

3.  **Minimum Spanning Tree (MST) Algorithms (Kruskal's and Prim's):**

      * **Concept:** Find a subset of edges that connects all vertices in a connected, undirected, weighted graph, with the minimum possible total edge weight, and no cycles.
      * **Kruskal's Algorithm (Greedy Choice):** Repeatedly add the edge with the smallest weight that does not form a cycle with already added edges. (Requires Disjoint Set Union for efficient cycle detection).
      * **Prim's Algorithm (Greedy Choice):** Start from an arbitrary vertex. Repeatedly add the edge with the smallest weight that connects a vertex in the MST to a vertex outside the MST. (Typically uses a min-priority queue).
      * **Why they work:** Both rely on properties like the "Cut Property" (which essentially states that making locally optimal choices at certain points leads to a global MST).

4.  **Fractional Knapsack Problem:**

      * **Concept:** Given items with weights and values, and a knapsack with a maximum capacity, select items to maximize total value. Items can be taken fractionally.
      * **Greedy Choice:** Sort items by their value-to-weight ratio in descending order. Take items with the highest ratio first until the knapsack is full.
      * **Why it works:** By prioritizing items that give the most value per unit of weight, you maximize the total value. (Note: For 0/1 Knapsack, where items cannot be taken fractionally, a greedy approach does NOT work; DP is required).

#### Handling Large Inputs / Constraints

  * **Sorting Preprocessing:** Many greedy algorithms require the input to be sorted (e.g., by finish time, weight, value-to-weight ratio). This adds an $O(N \\log N)$ complexity.
  * **Data Structures for Efficiency:** For problems like Kruskal's or Prim's, efficient data structures (Disjoint Set Union, Priority Queues/Heaps) are crucial to maintain the $O(E \\log V)$ or $O(E \\log E)$ complexities. A naive implementation without these could degrade to $O(V^2)$ or $O(E^2)$.
  * **Proving Correctness:** The most challenging part of a greedy algorithm is often proving that the greedy choice property holds. In an interview, if you identify a greedy strategy, be prepared to briefly justify *why* you think it works or argue its correctness. A common way is a "proof by exchange argument" – showing that if an optimal solution doesn't make the greedy choice, you can modify it to include the greedy choice without making it worse.

#### Typical FAANG Problem Example

Let's consider a common greedy problem that involves sorting.

**Problem Description: "Assign Cookies"** (LeetCode Easy)

Assume you are an awesome parent and want to give some cookies to your children. You have a list of `children` where `g[i]` is the greed factor of the `i`-th child (the minimum size cookie that child will accept). You also have a list of `cookies` where `s[j]` is the size of the `j`-th cookie.

If `s[j] >= g[i]`, then you can assign the cookie `j` to child `i`, and the child `i` will be content. Your goal is to maximize the number of content children.

**Constraints:**

  * `1 <= g.length, s.length <= 3 * 10^4`
  * `1 <= g[i], s[j] <= 10^9`

**Thought Process & Hints:**

1.  **Understanding the Goal:** Maximize contented children, given their greed factors and cookie sizes. Each child gets at most one cookie, each cookie is used at most once.

2.  **Greedy Intuition:**

      * How should we match children and cookies? Should we give large cookies to greedy children? Or small cookies to less greedy children?
      * Consider the smallest cookie: To whom should we give it?
          * If we give it to a very greedy child, it might not satisfy them.
          * If we give it to the *least greedy child* that it *can* satisfy, then we've used the smallest possible cookie to satisfy that child, leaving larger cookies for more greedy children. This seems like a promising greedy strategy.
      * Alternatively, consider the child with the *least greed*: Which cookie should they get? The *smallest cookie that can satisfy them*. This leaves larger cookies for other, possibly greedier, children.

3.  **Greedy Strategy Formulation:**

      * **Sort both `g` (greed factors) and `s` (cookie sizes) in ascending order.** This is crucial.
      * Iterate through the sorted children. For each child, try to assign the smallest available cookie that can satisfy them.
      * Maintain two pointers: one for children (`child_idx`) and one for cookies (`cookie_idx`).

4.  **Algorithm Sketch:**

      * Sort `g` in ascending order.
      * Sort `s` in ascending order.
      * `child_idx = 0`
      * `cookie_idx = 0`
      * `content_children = 0`
      * While `child_idx < len(g)` AND `cookie_idx < len(s)`:
          * If `s[cookie_idx] >= g[child_idx]` (the current cookie can satisfy the current child):
              * `content_children += 1`
              * `child_idx += 1` (Move to the next child)
              * `cookie_idx += 1` (Move to the next cookie, as this one is used)
          * Else (`s[cookie_idx] < g[child_idx]`, the current cookie is too small for the current child):
              * This cookie cannot satisfy the current child (or any subsequent, greedier child). Discard it.
              * `cookie_idx += 1` (Try the next larger cookie)
      * Return `content_children`.

5.  **Why this greedy approach works (Proof sketch):**

      * Suppose there is an optimal solution that differs from the greedy solution.
      * In the optimal solution, if the least greedy child `C` is satisfied by cookie `X`, and in the greedy solution, `C` is satisfied by cookie `Y` (where `Y` is the smallest cookie that can satisfy `C`, so `Y <= X`), then we can swap `X` with `Y` (if `Y` was given to some other child or not used).
      * If `Y` was given to some other child `C'`, since `Y` is the smallest that satisfies `C`, `Y` also satisfies `C'`. So, giving `Y` to `C` and `X` to `C'` (if `X` still satisfies `C'`) or keeping `X` for another child does not reduce the number of contented children. This "exchange argument" can be formalized to show that the greedy choice is always part of an optimal solution.

6.  **Complexity Analysis:**

      * Time Complexity: $O(G \\log G + S \\log S)$ for sorting, where $G$ is `len(g)` and $S$ is `len(s)`. The two-pointer scan is $O(G + S)$. Overall, dominated by sorting.
      * Space Complexity: $O(1)$ if sorting is in-place, or $O(G + S)$ if `sorted()` creates new lists.

#### System Design Relevance

  * **Resource Allocation:** In scenarios where you need to assign limited resources (e.g., servers to tasks, bandwidth to requests, time slots to jobs) based on some priority or efficiency metric, greedy algorithms can be a starting point.
  * **Scheduling Systems:** Task schedulers in operating systems or cloud platforms might employ greedy strategies (e.g., shortest job first, earliest deadline first) to optimize throughput or latency.
  * **Network Routing:** Simple routing protocols might use a greedy approach to pick the next hop. More complex ones might involve Dijkstra's/Prim's (which are greedy at their core).
  * **Data Compression (Huffman):** Used in file formats and communication protocols.
  * **Financial Algorithms:** Some simplified trading strategies can be greedy (e.g., always buy at lowest, sell at highest, though real-world finance is far more complex).
  * **Load Balancing:** Distributing incoming requests to the least loaded server can be a greedy choice.

**Challenge to the Reader:**
Consider the "Jump Game" problem (LeetCode Medium). You are given an integer array `nums`. You are initially positioned at `nums[0]`. Each element `nums[i]` represents your maximum jump length from that position. Determine if you can reach the last index. How can you solve this using a greedy approach by keeping track of the "farthest reachable point"? (Hint: Think about iterating through the array and updating a `max_reach` variable).
