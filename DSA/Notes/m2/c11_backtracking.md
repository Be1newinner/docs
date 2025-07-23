### 11\. Recursion and Backtracking

#### Core Concepts

**Recursion:**
Recursion is a problem-solving technique where the solution to a problem depends on solutions to smaller instances of the same problem. A recursive function calls itself directly or indirectly.

  * **Base Case:** The simplest instance of the problem that can be solved directly without further recursion. This is crucial; without a base case, recursion leads to an infinite loop (and ultimately a stack overflow).
  * **Recursive Step:** The part where the function calls itself with a modified (usually smaller) input, moving closer to the base case.

**Intuition:** Imagine a set of Russian dolls. To open the largest doll, you find a slightly smaller doll inside. To open that one, you find an even smaller doll, and so on, until you reach the smallest doll, which you can simply open (base case). Then you close them all back up in reverse order.

**Backtracking:**
Backtracking is an algorithmic technique for solving problems, typically combinatorial problems (finding all solutions or one solution among many), by trying to build a solution incrementally. Whenever a choice leads to a dead end, or a solution is found, the algorithm "backtracks" (undoes its last choice) and tries an alternative.

  * **Decision Tree:** Backtracking problems can often be visualized as exploring a decision tree. Each node represents a choice, and each path from the root to a leaf represents a potential solution.
  * **Choices, Constraints, Goal:**
      * **Choices:** At each step, what are the possible options we can take?
      * **Constraints:** What conditions must be met for a choice to be valid? What makes a path invalid?
      * **Goal:** What defines a valid complete solution? When do we stop exploring a path and record a result?
  * **Explore & Undo:** The essence of backtracking: make a choice, recurse (explore the consequences), then undo the choice (backtrack) to explore other possibilities.

**Relationship:** Backtracking is almost always implemented using recursion. The recursive calls represent exploring different paths in the decision tree, and returning from a recursive call is the "backtracking" step.

**Time and Space Complexity:**
Backtracking algorithms often have exponential time complexity, $O(2^N)$ or $O(N\!)$, because they explore all (or many) possible combinations.

  * **Time Complexity:** Varies widely, but typically exponential:
      * $O(2^N)$ for problems like subset generation, combinations (each element can either be in or out).
      * $O(N\!)$ for problems like permutations (choosing an element from remaining $N$ options, then $N-1$, etc.).
  * **Space Complexity:** Dominated by the recursion stack depth, which can be $O(N)$ for $N$ levels of recursion. Additional space might be needed for storing the current path/solution elements.

#### Python 3.11 Implementation & Common Patterns

Backtracking functions typically follow a template:

```python
# General Backtracking Template

def backtrack(current_path, choices_remaining, other_parameters):
    # 1. Base Case / Goal Check:
    #    If current_path represents a valid complete solution:
    #        Add current_path to results
    #        Return (or continue if more solutions are needed)

    # 2. Pruning / Constraint Check (Optional, but important for efficiency):
    #    If current_path or choices_remaining violate constraints:
    #        Return (don't explore this path further)

    # 3. Explore Choices:
    #    For each possible choice from choices_remaining:
    #        a. Make the choice (add to current_path, update choices_remaining)
    #        b. Recursive Call: backtrack(updated_path, updated_choices, ...)
    #        c. Undo the choice (backtrack): Remove from current_path, restore choices_remaining
    #           (This is crucial for exploring other branches without interference)
```

**Example: Generating Permutations of a List**

Given a list of distinct numbers, return all possible permutations.
Input: `[1, 2, 3]`
Output: `[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]`

```python
def permutations(nums):
    results = []
    
    def backtrack(current_permutation, remaining_nums):
        # Base Case: If the current permutation is complete
        if not remaining_nums:
            results.append(list(current_permutation)) # Append a copy!
            return

        # Explore Choices: Iterate through available numbers
        for i in range(len(remaining_nums)):
            # Choose: Pick a number
            num_to_add = remaining_nums[i]
            current_permutation.append(num_to_add)
            
            # Constraints: Create new remaining_nums without the chosen one
            # (Python slicing creates a copy, effective for 'undoing')
            new_remaining = remaining_nums[:i] + remaining_nums[i+1:]
            
            # Recurse: Explore further with the chosen number
            backtrack(current_permutation, new_remaining)
            
            # Undo: Backtrack by removing the last chosen number
            current_permutation.pop()

    backtrack([], nums) # Start with an empty permutation and all numbers
    return results

print(f"Permutations of [1,2,3]: {permutations([1,2,3])}")
# Output: [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]

print(f"Permutations of [4]: {permutations([4])}")
# Output: [[4]]

print(f"Permutations of []: {permutations([])}")
# Output: []
```

**Alternative (More common for permutations/combinations using `used` array/set):**
This approach avoids list slicing which can be $O(N)$, potentially making the overall permutation generation $O(N \\cdot N\!)$. Using a `visited` array or set gives $O(N\! \\cdot N)$ for deep copy + appending.

```python
def permutations_optimized(nums):
    results = []
    n = len(nums)
    # Use a boolean array to track used elements for O(1) lookup
    used = [False] * n 
    
    def backtrack(current_permutation):
        if len(current_permutation) == n:
            results.append(list(current_permutation))
            return
        
        for i in range(n):
            if not used[i]: # If number at index i has not been used
                used[i] = True
                current_permutation.append(nums[i])
                
                backtrack(current_permutation)
                
                current_permutation.pop() # Backtrack
                used[i] = False           # Backtrack
                
    backtrack([])
    return results

print(f"Permutations (Optimized) of [1,2,3]: {permutations_optimized([1,2,3])}")
```

#### Handling Large Inputs / Constraints

  * **Stack Overflow:** As recursion uses the call stack, deep recursion (e.g., $N \> 1000$ in Python's default limit) can lead to `RecursionError`.
      * **Mitigation:** For problems with very deep recursion, consider converting to an iterative solution using an explicit stack, or increase Python's recursion limit (`sys.setrecursionlimit`). For backtracking, iterative solutions are generally more complex to write, so increasing the limit is sometimes the pragmatic choice if the maximum depth is known to be within reasonable bounds.
  * **Time Complexity:** The exponential nature of backtracking means it quickly becomes infeasible for large $N$ (e.g., $N \> 20-30$ for $2^N$, or $N \> 10-12$ for $N\!$).
      * **Optimization Strategies:**
          * **Pruning:** The most crucial optimization for backtracking. If you can determine early that a current path cannot lead to a valid solution, stop exploring that path. This prunes branches of the decision tree. Examples:
              * In N-Queens, if placing a queen creates an immediate conflict.
              * In Sudoku solver, if a number violates rules.
              * In combination sum, if the current sum exceeds target.
          * **Memoization (Dynamic Programming):** If overlapping subproblems are detected (i.e., the same recursive calls with the same arguments are made multiple times), memoization can store and reuse results. This transitions a pure recursive solution into Dynamic Programming. (More on this in the DP section).
          * **Iterative Solutions:** Sometimes possible, but often harder to implement for complex backtracking.

#### Typical FAANG Problem Example

Let's pick a common backtracking problem: **"Subsets"** (LeetCode Medium).

**Problem Description: "Subsets"**

Given an integer array `nums` of unique elements, return all possible subsets (the power set). The solution set must not contain duplicate subsets. Return the solution in any order.

**Example:**
Input: `nums = [1,2,3]`
Output: `[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]`

**Constraints:**

  * `1 <= nums.length <= 10` (Notice how small N is, hinting at exponential complexity\!)
  * `-10 <= nums[i] <= 10`
  * All the numbers in `nums` are unique.

**Thought Process & Hints:**

1.  **Understanding the Goal:** Generate all combinations of elements, including the empty set. Each element can either be "included" or "excluded" from a subset.

2.  **Decision Tree / Backtracking Intuition:**

      * For each number in `nums`, we have two choices:
        1.  Include the number in the current subset.
        2.  Do not include the number in the current subset.
      * We explore all these choices.

3.  **Algorithm Sketch (Recursive Backtracking):**

      * `results = []` (to store all generated subsets)
      * Define a helper `backtrack(start_index, current_subset)`:
          * **Base Case:**
              * At each call, `current_subset` represents a valid subset found so far. Add a **copy** of `current_subset` to `results`. (Crucial: add a copy because `current_subset` will be modified later).
              * There's no explicit "return" base case like in permutations. We add to results at every step.
          * **Recursive Step / Choices:**
              * Iterate from `start_index` to the end of `nums`. This ensures we only pick elements to the right of the current one, avoiding duplicate subsets (`[1,2]` vs `[2,1]`) and managing distinct subsets.
              * For each `i` from `start_index` to `len(nums) - 1`:
                  * **Choose:** Add `nums[i]` to `current_subset`.
                  * **Explore:** Make a recursive call: `backtrack(i + 1, current_subset)`. `i + 1` ensures we don't re-use `nums[i]` at the same level and move to the next distinct element for the next choice.
                  * **Undo (Backtrack):** Remove `nums[i]` from `current_subset` before the next iteration.

4.  **Initial Call:** `backtrack(0, [])` (start with index 0 and an empty current subset).

5.  **Example Walkthrough (`nums = [1,2,3]`)**
    `backtrack(0, [])`

      * `results = [[]]` (add empty set)
      * `i=0, num=1`:
          * `current_subset = [1]`
          * `backtrack(1, [1])`
              * `results = [[], [1]]` (add `[1]`)
              * `i=1, num=2`:
                  * `current_subset = [1,2]`
                  * `backtrack(2, [1,2])`
                      * `results = [[], [1], [1,2]]` (add `[1,2]`)
                      * `i=2, num=3`:
                          * `current_subset = [1,2,3]`
                          * `backtrack(3, [1,2,3])`
                              * `results = [[], [1], [1,2], [1,2,3]]` (add `[1,2,3]`)
                              * Loop ends (i=3 is out of bounds)
                          * `current_subset.pop()` -\> `[1,2]`
                      * Loop ends
                  * `current_subset.pop()` -\> `[1]`
              * `i=2, num=3`:
                  * `current_subset = [1,3]`
                  * `backtrack(3, [1,3])`
                      * `results = [[], [1], [1,2], [1,2,3], [1,3]]` (add `[1,3]`)
                      * Loop ends
                  * `current_subset.pop()` -\> `[1]`
              * Loop ends
          * `current_subset.pop()` -\> `[]`
      * `i=1, num=2`:
          * `current_subset = [2]`
          * `backtrack(2, [2])`
              * `results = [..., [2]]` (add `[2]`)
              * `i=2, num=3`:
                  * `current_subset = [2,3]`
                  * `backtrack(3, [2,3])`
                      * `results = [..., [2,3]]` (add `[2,3]`)
                      * Loop ends
                  * `current_subset.pop()` -\> `[2]`
              * Loop ends
          * `current_subset.pop()` -\> `[]`
      * `i=2, num=3`:
          * `current_subset = [3]`
          * `backtrack(3, [3])`
              * `results = [..., [3]]` (add `[3]`)
              * Loop ends
          * `current_subset.pop()` -\> `[]`
      * Outer loop ends.

6.  **Complexity Analysis:**

      * Time Complexity: $O(N \\cdot 2^N)$. There are $2^N$ possible subsets. For each subset, copying it to `results` takes $O(N)$ time.
      * Space Complexity: $O(N)$ for the recursion stack depth (corresponding to the longest subset `N`) and $O(N \\cdot 2^N)$ for storing all results.

#### System Design Relevance

While less directly tied to everyday system components like databases or networks, understanding recursion and backtracking is crucial for:

  * **Configuration Management/Dependency Resolution:** Solving problems where you have choices and constraints (e.g., finding a valid set of compatible software packages).
  * **Game AI:** Exploring game trees (e.g., Minimax algorithm for chess) to find optimal moves.
  * **Constraint Satisfaction Problems:** Solving puzzles like Sudoku, N-Queens, or logic problems.
  * **Parser Generators/Compilers:** Recursive descent parsers often implicitly use recursion to match grammar rules.
  * **Routing Algorithms (complex networks):** While BFS/DFS cover basic pathfinding, more complex routing or resource allocation problems with constraints might use variations of backtracking.
  * **Code Generation:** Exploring different ways to generate code or optimize sequences of operations.

**Challenge to the Reader:**
Consider the "Combination Sum" problem (LeetCode Medium). Given a list of distinct integers `candidates` and a target integer `target`, return a list of all unique combinations of `candidates` where the chosen numbers sum to `target`. Each number may be used an unlimited number of times. How would you adapt the backtracking template, specifically focusing on how to allow repeated numbers and how to handle pruning when the sum exceeds the target?