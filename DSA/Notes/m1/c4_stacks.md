### 4. Stacks

#### Core Concepts

A stack is a linear data structure that follows the **Last-In, First-Out (LIFO)** principle. Imagine a stack of plates: you can only add a new plate on top, and you can only remove the top-most plate. The last plate you put on is the first one you can take off.

**Key Operations:**

1.  **Push:** Adds an element to the top of the stack.
2.  **Pop:** Removes and returns the top-most element from the stack.
3.  **Peek (or Top):** Returns the top-most element without removing it.
4.  **isEmpty:** Checks if the stack is empty.
5.  **size:** Returns the number of elements in the stack.

**Practical Intuition:**

  * A stack of physical items (plates, books, trays).
  * The "Undo" button in software: the last action performed is the first one to be undone.
  * Browser history (back button): the last page visited is the first one you go back to.
  * Function call stack: when functions are called, they are pushed onto the stack; when they return, they are popped. This is fundamental to how programs execute.

**Use Cases:**

  * **Function Call Management:** Managing function calls in a program (call stack).
  * **Expression Evaluation:** Converting infix to postfix expressions, evaluating postfix expressions.
  * **Backtracking Algorithms:** Used to keep track of previous states (e.g., in DFS, maze solving).
  * **Undo/Redo Functionality:** Storing states to revert or reapply actions.
  * **Syntax Parsing:** Checking for balanced parentheses, curly braces, and square brackets.

**Time and Space Complexity:**

| Operation       | Time Complexity (Average & Worst) | Notes                                           |
| :-------------- | :-------------------------------- | :---------------------------------------------- |
| Push            | $O(1)$                            | If using Python `list.append()` or `deque.append()` |
| Pop             | $O(1)$                            | If using Python `list.pop()` or `deque.pop()`     |
| Peek/Top        | $O(1)$                            | Accessing the last element.                     |
| isEmpty/size    | $O(1)$                            |                                                 |

**Space Complexity:** $O(N)$ where $N$ is the number of elements in the stack.

#### Python 3.11 Usage (`list`, `collections.deque`)

While you *can* implement a stack using a simple Python `list`, the `collections.deque` (double-ended queue) is generally preferred for its $O(1)$ performance guarantees for additions and removals from *both* ends, which perfectly suits stack (and queue) operations.

**Using `list` as a Stack:**
Treat the end of the list as the "top" of the stack.

```python
# Using Python list as a Stack
my_stack_list = []

# Push operation: use append()
my_stack_list.append(10)
my_stack_list.append(20)
my_stack_list.append(30)
print(f"Stack after pushes: {my_stack_list}") # Output: [10, 20, 30]

# Peek operation: access last element
if my_stack_list:
    print(f"Top element (peek): {my_stack_list[-1]}") # Output: 30

# Pop operation: use pop()
popped_item = my_stack_list.pop()
print(f"Popped item: {popped_item}, Stack now: {my_stack_list}") # Output: Popped item: 30, Stack now: [10, 20]

# Check if empty
print(f"Is stack empty? {not my_stack_list}") # Output: False

# Push again
my_stack_list.append(40)
print(f"Stack after another push: {my_stack_list}") # Output: [10, 20, 40]

# Pop all elements
while my_stack_list:
    print(f"Popping: {my_stack_list.pop()}")
# Output:
# Popping: 40
# Popping: 20
# Popping: 10
print(f"Is stack empty? {not my_stack_list}") # Output: True
```

**Note on `list` performance:** While `append()` and `pop()` from the end of a list are amortized $O(1)$, `list` is still an array internally. Operations like `insert(0, item)` or `pop(0)` (which would simulate a stack from the beginning of the list) are $O(N)$ because they require shifting all other elements. Always use `append()` and `pop()` from the end for stack-like behavior with lists.

**Using `collections.deque` as a Stack (Recommended):**
`deque` (double-ended queue) is implemented as a doubly linked list, providing true $O(1)$ performance for additions and removals from both ends.

```python
from collections import deque

# Using collections.deque as a Stack
my_stack_deque = deque()

# Push operation: use append()
my_stack_deque.append(10)
my_stack_deque.append(20)
my_stack_deque.append(30)
print(f"Stack after pushes: {my_stack_deque}") # Output: deque([10, 20, 30])

# Peek operation: access last element
if my_stack_deque:
    print(f"Top element (peek): {my_stack_deque[-1]}") # Output: 30

# Pop operation: use pop()
popped_item = my_stack_deque.pop()
print(f"Popped item: {popped_item}, Stack now: {my_stack_deque}") # Output: Popped item: 30, Stack now: deque([10, 20])

# Check if empty
print(f"Is stack empty? {not my_stack_deque}") # Output: False

# Push again
my_stack_deque.append(40)
print(f"Stack after another push: {my_stack_deque}") # Output: deque([10, 20, 40])
```

**Why `deque` is preferred:** For stack usage, the performance difference between `list.append()`/`list.pop()` and `deque.append()`/`deque.pop()` (from the right end) is negligible for most practical purposes, as `list` operations are amortized $O(1)$. However, `deque` offers true $O(1)$ guarantees without the potential for $O(N)$ reallocations, making it theoretically more robust for very large or sensitive applications. For queue implementations where `popleft()` is needed, `deque` is significantly better.

#### Problem-Solving Patterns

Stacks are fundamental for problems that involve reverse order processing or maintaining context.

1.  **Parentheses/Bracket Matching:**

      * **Concept:** Use a stack to check if parentheses, brackets, or braces are balanced and correctly nested. When an opening bracket is encountered, push it onto the stack. When a closing bracket is encountered, pop from the stack and check if it matches the opening bracket.
      * **Examples:** Valid Parentheses, Longest Valid Parentheses.

2.  **Monotonic Stack:**

      * **Concept:** A stack where the elements are always kept in a strictly increasing or strictly decreasing order. When a new element comes, elements violating the monotonic property are popped until the property is restored, and then the new element is pushed.
      * **Use Cases:** Finding next greater/smaller element, daily temperatures, largest rectangle in histogram. This pattern is very powerful for finding "nearest" elements that satisfy a certain condition to the left or right.

3.  **Backtracking/DFS Simulation:**

      * **Concept:** Stacks can explicitly manage the states or nodes to visit in a Depth-First Search (DFS) or backtracking problem, offering an iterative alternative to recursion (which implicitly uses the call stack).
      * **Examples:** Maze solving, graph traversal (DFS), permutation generation (often easier with recursion but can be done with stack).

4.  **Expression Evaluation:**

      * **Concept:** Used to convert infix to postfix notation or evaluate postfix expressions (Reverse Polish Notation). Operands are pushed, and operators pop operands, perform calculations, and push results.

#### Handling Large Inputs / Constraints

  * **Stack Overflow (Recursion Limit):** If your stack-based solution is actually a recursive algorithm, Python has a default recursion depth limit (typically 1000-3000). For problems with very deep recursion (e.g., deeply nested structures, long paths in DFS), an iterative solution using an explicit stack is necessary to avoid `RecursionError`.
  * **Memory Usage:** Stacks consume $O(N)$ space. For very large inputs, be mindful of the total memory consumed if elements are complex objects.
  * **Empty Stack Access:** Always handle cases where you try to `pop()` or `peek()` from an empty stack. Python's `list.pop()` raises an `IndexError`, and `deque.pop()` raises an `IndexError`. Explicit checks (`if stack:`) or `try-except` blocks are crucial.

#### Typical FAANG Problem Example

Let's take a look at a classic stack problem, one of the recommended LeetCode problems:

**Problem Description: "Valid Parentheses"** (LeetCode Easy)

Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.

An input string is valid if:

1.  Open brackets must be closed by the same type of brackets.
2.  Open brackets must be closed in the correct order.
3.  Every close bracket has a corresponding open bracket of the same type.

**Constraints:**

  * $1 \\le len(s) \\le 10^4$
  * `s` consists of parentheses only `'()[]{}'`.

**Thought Process & Hints:**

1.  **Understanding the Goal:** Verify if the sequence of brackets is correctly nested and matched.

2.  **Initial Thoughts (and why a stack is ideal):**

      * When we see an opening bracket, we need to remember it for a *future* closing bracket.
      * When we see a closing bracket, it must correspond to the *most recently opened, unclosed* bracket.
      * This "last opened, first closed" behavior is the direct definition of LIFO, making a stack the perfect data structure.

3.  **Algorithm Sketch:**

      * Create an empty stack (`deque` is good here).
      * Create a mapping of closing brackets to their corresponding opening brackets (e.g., `')': '('`, `'}': '{'`, `']': '['`). This makes lookup easy.
      * Iterate through each character `char` in the input string `s`:
          * **If `char` is an opening bracket:** Push `char` onto the stack.
          * **If `char` is a closing bracket:**
              * Check if the stack is empty. If it is, it means a closing bracket appeared without a corresponding opening bracket. Return `False`.
              * Pop the top element from the stack. Let's call it `top_char`.
              * Check if `top_char` matches the required opening bracket for `char` (using your mapping). If they don't match, return `False`.
      * **After iterating through the entire string:**
          * If the stack is empty, it means all opening brackets found their corresponding closing brackets. Return `True`.
          * If the stack is *not* empty, it means there are unclosed opening brackets left. Return `False`.

4.  **Example Walkthrough (`s = "([{}])"`)**

      * Stack: `[]`
      * `char = '('`: Push `(` -\> Stack: `[`(`]`.
      * `char = '['`: Push `[` -\> Stack: `[(` `[` `]`
      * `char = '{'`: Push `{` -\> Stack: `[(` `[` `{` `]`
      * `char = '}'`: Pop `{`. Matches opening `{`. Stack: `[(` `[` `]`
      * `char = ']'`: Pop `[`. Matches opening `[`. Stack: `[`(`]`.
      * `char = ')'`: Pop `(`. Matches opening `(`. Stack: `[]`.
      * End of string. Stack is empty. Return `True`.

**Example Walkthrough (`s = "([)]"`)**
\* Stack: `[]`
\* `char = '('`: Push `(` -\> Stack: `[`(`]`.
\* `char = '['`: Push `[` -\> Stack: `[(` `[` `]`
\* `char = ')'`: Pop `[`. Does NOT match opening `(`. Return `False`.

5.  **Complexity Analysis:**
      * Time Complexity: $O(N)$ because each character in the string is processed exactly once, and stack operations (push, pop, peek) are $O(1)$.
      * Space Complexity: $O(N)$ in the worst case (e.g., `(((((((())))))))`) where the stack could hold up to $N/2$ opening brackets. In the case of `()()()`, space is $O(1)$.

#### System Design Relevance

  * **Compiler/Interpreter Design:** Stacks are fundamental for parsing code, managing function calls, and evaluating expressions. The call stack is the most direct example.
  * **Web Development (Browser History):** The "Back" button in web browsers conceptually uses a stack to store previously visited pages.
  * **Text Editors (Undo/Redo):** Each edit operation can be pushed onto an "undo stack." Redo functionality can use a second stack.
  * **Operating Systems (Interrupt Handling):** When an interrupt occurs, the current CPU state (registers, program counter) is pushed onto a stack so that the interrupt handler can execute, and then the original state can be restored.
  * **Network Packet Processing:** Stacks can be used to process protocol layers, where each layer pushes its header/data onto the "packet stack" before transmission, and pops them off upon reception.

**Challenge to the Reader:**
Consider the "Daily Temperatures" problem (LeetCode Medium). How can a **monotonic stack** be used to efficiently solve this problem, where for each day, you need to find how many days you have to wait until a warmer temperature? Think about what information you need to store in the stack and when you should pop elements.