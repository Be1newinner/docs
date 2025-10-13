### 6. Trees

#### Core Concepts

A tree is a non-linear hierarchical data structure that consists of nodes connected by edges. Unlike linked lists, where elements are arranged linearly, trees have a branching structure, resembling an inverted tree.

**Key Terminology:**

  * **Node:** A fundamental unit of a tree, containing data and references/pointers to its child nodes.
  * **Root:** The topmost node of a tree. It has no parent.
  * **Child:** A node directly connected to another node when moving away from the root.
  * **Parent:** A node directly connected to another node when moving towards the root.
  * **Siblings:** Nodes that share the same parent.
  * **Leaf (or External Node):** A node that has no children.
  * **Internal Node:** A node that has at least one child.
  * **Edge:** The connection between two nodes.
  * **Path:** A sequence of nodes along the edges from one node to another.
  * **Depth of a Node:** The length of the path from the root to that node. The root has a depth of 0.
  * **Height of a Node:** The length of the longest path from that node to a leaf. The height of a leaf node is 0.
  * **Height of a Tree:** The height of its root node.
  * **Subtree:** A node and all its descendants.

**Types of Trees (Commonly Encountered in Interviews):**

1.  **Binary Tree:**

      * A tree in which each node has at most two children, typically referred to as the left child and the right child.
      * Not necessarily ordered.

2.  **Binary Search Tree (BST):**

      * A special type of binary tree with an additional property that helps with efficient searching, insertion, and deletion.
      * For every node:
          * All values in its left subtree are less than the node's value.
          * All values in its right subtree are greater than the node's value.
          * Both the left and right subtrees are also BSTs.
      * **Advantages:** Efficient searching ($O(\\log N)$ average case), allows for ordered traversal.
      * **Disadvantages:** Can become skewed (degenerate) into a linked list in the worst case (e.g., inserting elements in strictly increasing order), leading to $O(N)$ performance for operations. This is where self-balancing BSTs (AVL, Red-Black trees) come in.

**Practical Intuition:**

  * **Family Tree:** A perfect analogy, with parents, children, siblings, and ancestors/descendants.
  * **File System:** Directories (nodes) containing files or other directories (children). The root directory is the root of the tree.
  * **Organization Chart:** Hierarchical structure of a company.
  * **Decision Tree:** Each node represents a decision, and branches lead to outcomes.

**Use Cases:**

  * **Hierarchical Data Representation:** File systems, XML/HTML documents (DOM tree), organizational structures.
  * **Efficient Searching/Sorting:** Binary Search Trees are used for efficient data retrieval.
  * **Database Indexing:** B-Trees, B+ Trees are widely used for efficient disk-based indexing.
  * **Syntax Trees:** In compilers, to represent the structure of programming code.
  * **Prefix Trees (Tries):** For fast string matching and auto-completion.
  * **Heaps:** A special kind of binary tree (complete binary tree) used for priority queues.

**Time and Space Complexity (for BSTs - Average Case):**

| Operation        | Time Complexity (Average) | Time Complexity (Worst) | Notes                                           |
| :--------------- | :------------------------ | :---------------------- | :---------------------------------------------- |
| Search           | $O(\\log N)$               | $O(N)$                  | Skewed tree (degenerate to linked list).        |
| Insertion        | $O(\\log N)$               | $O(N)$                  | Skewed tree.                                    |
| Deletion         | $O(\\log N)$               | $O(N)$                  | Skewed tree.                                    |
| Traversal (DFS/BFS) | $O(N)$                    | $O(N)$                  | Must visit every node.                          |

**Space Complexity:** $O(N)$ for $N$ nodes. Recursive traversals can use $O(H)$ space on the call stack, where $H$ is the height of the tree ($O(\\log N)$ average, $O(N)$ worst).

#### Python 3.11 Implementation & Traversals

Like linked lists, trees are typically implemented using custom classes in Python.

```python
from collections import deque

class TreeNode:
    """
    Represents a single node in a Binary Tree.
    """
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left   # Pointer to the left child
        self.right = right # Pointer to the right child

# --- Tree Traversals ---

# 1. Depth-First Search (DFS) Traversal
#   Explores as far as possible along each branch before backtracking.
#   Typically implemented recursively (implicit stack) or iteratively (explicit stack).

def inorder_traversal(root):
    """Left -> Root -> Right (Sorted order for BST)"""
    result = []
    if root:
        result.extend(inorder_traversal(root.left))
        result.append(root.val)
        result.extend(inorder_traversal(root.right))
    return result

def preorder_traversal(root):
    """Root -> Left -> Right"""
    result = []
    if root:
        result.append(root.val)
        result.extend(preorder_traversal(root.left))
        result.extend(preorder_traversal(root.right))
    return result

def postorder_traversal(root):
    """Left -> Right -> Root"""
    result = []
    if root:
        result.extend(postorder_traversal(root.left))
        result.extend(postorder_traversal(root.right))
        result.append(root.val)
    return result

# Iterative DFS (Preorder - example using explicit stack)
def preorder_iterative(root):
    if not root:
        return []
    result = []
    stack = [root] # Initialize stack with the root
    while stack:
        node = stack.pop() # Pop the current node
        result.append(node.val)
        # Push right child first, so left child is processed next (LIFO)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return result

# 2. Breadth-First Search (BFS) Traversal / Level Order Traversal
#   Explores all nodes at the current depth level before moving to the next level.
#   Always implemented iteratively using a queue.

def level_order_traversal(root):
    """Visits nodes level by level (top-down, left-to-right)"""
    result = []
    if not root:
        return result

    q = deque([root]) # Initialize queue with the root node

    while q:
        level_nodes = [] # To store nodes at the current level
        level_size = len(q) # Number of nodes at the current level

        for _ in range(level_size):
            node = q.popleft() # Dequeue node
            level_nodes.append(node.val)

            if node.left:
                q.append(node.left) # Enqueue left child
            if node.right:
                q.append(node.right) # Enqueue right child
        result.append(level_nodes) # Add current level's nodes to result

    return result

# --- Example Usage ---
# Construct a simple binary tree:
#        3
#       / \
#      9  20
#         / \
#        15  7

root = TreeNode(3)
root.left = TreeNode(9)
root.right = TreeNode(20)
root.right.left = TreeNode(15)
root.right.right = TreeNode(7)

print(f"Inorder Traversal (Recursive): {inorder_traversal(root)}")   # Output: [9, 3, 15, 20, 7] (for BST, this would be sorted)
print(f"Preorder Traversal (Recursive): {preorder_traversal(root)}")  # Output: [3, 9, 20, 15, 7]
print(f"Postorder Traversal (Recursive): {postorder_traversal(root)}") # Output: [9, 15, 7, 20, 3]
print(f"Preorder Traversal (Iterative): {preorder_iterative(root)}") # Output: [3, 9, 20, 15, 7]
print(f"Level Order Traversal (BFS): {level_order_traversal(root)}") # Output: [[3], [9, 20], [15, 7]]
```

#### Problem-Solving Patterns

Recursion is the natural paradigm for tree problems due to their inherently recursive definition (a tree is a root and two subtrees).

1.  **Recursion (Divide and Conquer):**

      * **Concept:** Solve a problem for a node by recursively solving it for its children and then combining the results.
      * **Examples:** Calculating tree height, maximum depth, checking if a tree is balanced, summing node values, path sums.
      * **Base Case:** Typically, an empty tree (or `None` node) is the base case.
      * **Recursive Step:** Process the current node, then make recursive calls for `root.left` and `root.right`.

2.  **DFS (Preorder, Inorder, Postorder):**

      * **Preorder:** Useful for creating a copy of a tree, or for parsing expressions where the operator comes first.
      * **Inorder:** Useful for getting elements in sorted order from a BST, or for converting an expression tree to an infix expression.
      * **Postorder:** Useful for deleting a tree (delete children first), or for evaluating an expression tree (evaluate operands first).

3.  **BFS (Level Order Traversal):**

      * **Concept:** Ideal for problems that ask about properties or actions on nodes level by level.
      * **Examples:** Finding the maximum width of a tree, level order traversal output, connecting nodes at the same level (e.g., "Populating Next Right Pointers in Each Node").

4.  **Tree DP (Dynamic Programming on Trees):**

      * **Concept:** Solving problems on trees by combining results from subproblems (children). Often involves passing information up or down the tree during traversal.
      * **Examples:** Diameter of Binary Tree, Maximum Path Sum.

#### Handling Large Inputs / Constraints

  * **Recursion Depth Limit:** As mentioned with stacks, deeply recursive solutions for trees can hit Python's default recursion limit (e.g., for very skewed trees or large heights). For trees with $N$ up to $10^5$, iterative DFS (using an explicit stack) or BFS (using a queue) might be necessary to avoid `RecursionError`. You can increase the recursion limit (`sys.setrecursionlimit`), but it's generally discouraged as a primary solution.
  * **Null Pointers/Edge Cases:** Always consider empty trees (`root is None`), single-node trees, and trees with only left or only right children when designing solutions. Drawing out small examples helps.
  * **Balancing:** While not directly part of basic tree implementation, understanding that unbalanced BSTs degrade to $O(N)$ performance is crucial. Mentioning self-balancing trees (AVL, Red-Black) shows deeper understanding, even if you don't implement them from scratch.

#### Typical FAANG Problem Example

Let's tackle a classic tree problem that can be solved with recursion (DFS).

**Problem Description: "Maximum Depth of Binary Tree"** (LeetCode Easy)

Given the `root` of a binary tree, return its maximum depth.

A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

**Constraints:**

  * The number of nodes in the tree is in the range $[0, 10^4]$.
  * $-100 \\le Node.val \\le 100$

**Thought Process & Hints:**

1.  **Understanding the Goal:** Find the longest path from the root to any leaf.

2.  **Recursive Intuition:**

      * The maximum depth of an empty tree is 0. This is our base case.
      * For any non-empty node, its maximum depth is 1 (for the node itself) plus the maximum depth of its left or right subtree, whichever is greater.
      * This is a perfect recursive definition.

3.  **Algorithm Sketch (Recursive DFS):**

      * **Base Case:** If `root` is `None`, return `0`.
      * **Recursive Step:**
          * Recursively calculate `max_depth_left = maxDepth(root.left)`.
          * Recursively calculate `max_depth_right = maxDepth(root.right)`.
          * The maximum depth for the current `root` is `1 + max(max_depth_left, max_depth_right)`.

4.  **Example Walkthrough:**

      * Tree: `[3,9,20,null,null,15,7]` (represented as a list, but visualize as a tree)
        ```
              3
             / \
            9  20
               / \
              15  7
        ```
      * `maxDepth(3)`:
          * `maxDepth(9)`:
              * `maxDepth(None)` -\> returns 0
              * `maxDepth(None)` -\> returns 0
              * Returns `1 + max(0, 0) = 1`
          * `maxDepth(20)`:
              * `maxDepth(15)`:
                  * `maxDepth(None)` -\> returns 0
                  * `maxDepth(None)` -\> returns 0
                  * Returns `1 + max(0, 0) = 1`
              * `maxDepth(7)`:
                  * `maxDepth(None)` -\> returns 0
                  * `maxDepth(None)` -\> returns 0
                  * Returns `1 + max(0, 0) = 1`
              * Returns `1 + max(1, 1) = 2`
          * Returns `1 + max(1, 2) = 3`

5.  **Alternative (Iterative BFS - Level Order):**

      * You can also solve this using BFS. The depth is simply the number of levels you traverse.
      * Initialize a queue with `(root, 1)` (node, current\_level).
      * Initialize `max_depth = 0`.
      * While queue is not empty:
          * Dequeue `(node, level)`.
          * `max_depth = max(max_depth, level)`.
          * Enqueue children: `(node.left, level + 1)`, `(node.right, level + 1)`.

6.  **Complexity Analysis:**

      * **Recursive DFS:**
          * Time Complexity: $O(N)$ as each node is visited exactly once.
          * Space Complexity: $O(H)$ due to the recursion call stack, where $H$ is the height of the tree. In the worst case (skewed tree), $H=N$, so $O(N)$. In the best/average case (balanced tree), $H = \\log N$, so $O(\\log N)$.
      * **Iterative BFS:**
          * Time Complexity: $O(N)$ as each node is visited and enqueued/dequeued once.
          * Space Complexity: $O(W)$ where $W$ is the maximum width of the tree. In the worst case (e.g., complete binary tree), $W=N/2$, so $O(N)$. For skewed tree, $W=1$, so $O(1)$.

#### System Design Relevance

  * **File Systems:** Tree structures are inherently used to organize files and directories.
  * **Domain Name System (DNS):** A hierarchical distributed naming system for computers, services, or any resource connected to the Internet. It's essentially a massive, distributed tree.
  * **Parsing (Compilers/Interpreters):** Abstract Syntax Trees (ASTs) are tree representations of the abstract syntactic structure of source code.
  * **Game AI (Decision Trees/Game Trees):** Representing possible moves and outcomes in games.
  * **Databases (Indexing):** B-Trees and B+ Trees are critical for efficiently querying large datasets on disk.
  * **Network Routing:** Sometimes conceptualized as traversing a network tree/graph.
  * **Data Compression:** Huffman trees are used in Huffman coding for lossless data compression.

**Challenge to the Reader:**
The "Validate Binary Search Tree" problem (LeetCode Medium) is a critical test of understanding BST properties and tree traversal. It's not enough to just check `root.val > root.left.val` and `root.val < root.right.val`. Why isn't this sufficient, and how can you use a range-based recursive approach or an iterative inorder traversal to correctly validate a BST?