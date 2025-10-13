### 3. Linked Lists

#### Core Concepts

A linked list is a linear data structure where elements are not stored at contiguous memory locations. Instead, each element (called a **node**) explicitly stores a reference (or pointer) to the next element in the sequence. This structure allows for efficient insertions and deletions at any position once the insertion point is found, unlike arrays where these operations can be $O(N)$.

**Key Characteristics:**

  * **Nodes:** The fundamental building block. Each node typically contains:
      * **Data:** The actual value stored.
      * **Pointer/Reference:** A link to the next node in the sequence (and sometimes to the previous node).
  * **Non-Contiguous Memory:** Nodes can be scattered anywhere in memory. This is why direct, $O(1)$ indexed access is not possible.
  * **Dynamic Size:** Linked lists can easily grow or shrink by simply creating/deleting nodes and updating pointers, without needing re-allocations and copies like dynamic arrays.
  * **Head and Tail:** The `head` pointer points to the first node in the list. The `tail` pointer (often implicitly) refers to the last node. The last node's pointer usually points to `None` (or `null` in other languages) to signify the end of the list.

**Types of Linked Lists:**

1.  **Singly Linked List:**

      * Each node points only to the *next* node.
      * Traversal is strictly unidirectional (from head to tail).
      * Efficient for insertions/deletions at the head ($O(1)$) and tail ($O(1)$ if `tail` pointer is maintained, else $O(N)$). Deletion of a specific node requires traversing to its *predecessor* ($O(N)$).

2.  **Doubly Linked List:**

      * Each node points to both the *next* node and the *previous* node.
      * Allows bidirectional traversal.
      * More memory overhead per node (due to the extra pointer).
      * Efficient for insertions/deletions anywhere in the middle ($O(1)$ once the node is found), as you have access to both neighbors.

3.  **Circular Linked List:**

      * The last node's pointer points back to the first node (head), forming a circle.
      * Can be singly or doubly circular.
      * Useful for scenarios where you need to traverse indefinitely or easily cycle through elements (e.g., round-robin scheduling).

**Practical Intuition:**
Imagine a scavenger hunt where each clue (node) tells you where to find the *next* clue. You can't just jump to clue \#5; you have to follow the chain from clue \#1, then \#2, and so on. If you want to insert a new clue, you simply change the "next" pointer of the previous clue to point to your new clue, and your new clue's "next" pointer points to what was originally the next clue.

**Use Cases:**

  * **Implementing other data structures:** Stacks (using head for push/pop), Queues (head for dequeue, tail for enqueue).
  * **Dynamic Memory Allocation:** Used by some memory allocators.
  * **Web Browsers (Back/Forward functionality):** Doubly linked lists can represent the history of visited pages.
  * **Music Playlists:** Allowing next/previous song functionality.
  * **Undo/Redo Functionality:** A list of operations.
  * **Circular Buffers:** For data streams.

**Time and Space Complexity:**

| Operation               | Singly Linked List (Avg/Worst) | Doubly Linked List (Avg/Worst) | Notes                                                               |
| :---------------------- | :----------------------------- | :----------------------------- | :------------------------------------------------------------------ |
| Access by Index (`node[i]`) | $O(N)$                         | $O(N)$                         | Requires traversal from head.                                       |
| Search by Value         | $O(N)$                         | $O(N)$                         | Requires traversal.                                                 |
| Insert at Head          | $O(1)$                         | $O(1)$                         | Update head pointer.                                                |
| Insert at Tail          | $O(N)$ (no tail ptr) / $O(1)$ (w/ tail ptr) | $O(1)$                         | With a tail pointer, just update tail and its prev.                 |
| Insert after a Node     | $O(1)$ (given ref to prev node) | $O(1)$ (given ref to node)     | For Doubly, update `prev` of next node, `next` of prev node.       |
| Delete at Head          | $O(1)$                         | $O(1)$                         | Update head pointer.                                                |
| Delete at Tail          | $O(N)$                         | $O(1)$                         | For Singly, need to find second-to-last node. For Doubly, direct access to prev. |
| Delete a Specific Node  | $O(N)$ (need to find prev)     | $O(1)$ (given ref to node)     | For Doubly, just update neighbors' pointers.                        |

**Space Complexity:** $O(N)$ for $N$ nodes, plus $O(1)$ space per node for pointers.

#### Python 3.11 Implementation

Python does not have a built-in linked list type, so we typically implement it using classes.

```python
class Node:
    """
    Represents a single node in a linked list.
    """
    def __init__(self, data=None):
        self.data = data
        self.next = None # Pointer to the next node

class LinkedList:
    """
    Implements a Singly Linked List.
    """
    def __init__(self):
        self.head = None # The first node in the list

    def is_empty(self):
        """Checks if the list is empty."""
        return self.head is None

    def append(self, data):
        """Adds a new node with given data to the end of the list."""
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            return
        current = self.head
        while current.next: # Traverse to the last node
            current = current.next
        current.next = new_node

    def prepend(self, data):
        """Adds a new node with given data to the beginning of the list."""
        new_node = Node(data)
        new_node.next = self.head # New node points to old head
        self.head = new_node      # New node becomes the head

    def delete_node(self, key):
        """Deletes the first node found with the given key."""
        current = self.head

        # Case 1: Head node itself holds the key
        if current and current.data == key:
            self.head = current.next
            current = None # Good practice to dereference
            return

        # Case 2: Key is somewhere else in the list
        prev = None
        while current and current.data != key:
            prev = current
            current = current.next

        # If key was not present in list
        if current is None:
            print(f"Node with key {key} not found.")
            return

        # Unlink the node
        prev.next = current.next
        current = None

    def search(self, key):
        """Searches for a node with the given key."""
        current = self.head
        while current:
            if current.data == key:
                return True
            current = current.next
        return False

    def print_list(self):
        """Prints all elements in the list."""
        current = self.head
        elements = []
        while current:
            elements.append(str(current.data))
            current = current.next
        print(" -> ".join(elements) if elements else "List is empty")

# --- Doubly Linked List Implementation Sketch (Conceptual) ---
class DoublyNode:
    def __init__(self, data=None):
        self.data = data
        self.next = None
        self.prev = None # Pointer to the previous node

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None # Often useful to maintain a tail pointer for O(1) appends

    def append(self, data):
        new_node = DoublyNode(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    # ... other methods like prepend, delete, etc., would involve updating both next and prev pointers.
    # For example, to delete a node 'n':
    # if n.prev: n.prev.next = n.next
    # if n.next: n.next.prev = n.prev
    # handle head/tail updates if 'n' was head/tail
```

**Illustrative Examples:**

```python
# Singly Linked List Example
my_slist = LinkedList()
my_slist.print_list() # Output: List is empty

my_slist.append(10)
my_slist.append(20)
my_slist.prepend(5)
my_slist.print_list() # Output: 5 -> 10 -> 20

print(f"Is 10 in list? {my_slist.search(10)}") # Output: True
print(f"Is 30 in list? {my_slist.search(30)}") # Output: False

my_slist.delete_node(10)
my_slist.print_list() # Output: 5 -> 20

my_slist.delete_node(5)
my_slist.print_list() # Output: 20

my_slist.delete_node(20)
my_slist.print_list() # Output: List is empty

my_slist.delete_node(100) # Output: Node with key 100 not found.
```

#### Problem-Solving Patterns

Linked lists often involve specific pointer manipulation patterns.

1.  **Fast & Slow Pointers (Floyd's Tortoise and Hare):**

      * **Concept:** Use two pointers, one moving faster than the other (e.g., one moves by 1 step, the other by 2 steps).
      * **Examples:** Detecting cycles in a linked list, finding the middle of a linked list, finding the $N^{th}$ node from the end.
      * **Intuition:** If there's a cycle, the fast pointer will eventually catch up to the slow pointer. If no cycle, the fast pointer will reach the end (`None`) first.

2.  **Reversal:**

      * **Concept:** Iteratively or recursively change the direction of `next` pointers to reverse the order of nodes.
      * **Examples:** Reversing a linked list, reversing parts of a linked list, checking for palindrome linked list.
      * **Key variables:** `prev`, `current`, `next_node` (to save the next pointer before `current.next` is changed).

3.  **Dummy Node (or Sentinel Node):**

      * **Concept:** Create a dummy node that points to the actual head of the linked list. This simplifies handling edge cases, especially when the head of the list might change (e.g., inserting at the beginning, deleting the head).
      * **Benefit:** Avoids special checks for `head is None` or updating `self.head` in every operation, making code cleaner and less error-prone. You return `dummy.next` as the new head.

4.  **Two Pointers (General):**

      * Similar to arrays, but the pointers are node references. Often used for merging lists, deleting specific nodes, or finding intersections.

#### Handling Large Inputs / Constraints

  * **Memory Overhead:** Each node requires memory for its data and its pointer(s). For very small data types and extremely large lists, this overhead can be noticeable compared to arrays where elements are packed tightly.
  * **Traversal Time:** Operations that require traversing the list (e.g., searching, accessing by index, appending without a tail pointer in a singly list) will be $O(N)$. For very large $N$, this can be slow. Avoid linear scans within loops that also iterate linearly.
  * **Recursion Depth:** Recursive solutions for linked list problems (like recursive reversal or traversal) can hit Python's recursion depth limit for extremely long lists. Iterative solutions are often safer.
  * **Null Pointers/Edge Cases:** Always consider empty lists, single-node lists, and two-node lists. These are common sources of off-by-one errors or `None` pointer exceptions. A good practice is to draw out small examples to trace pointer movements.

#### Typical FAANG Problem Example

Let's explore a problem that utilizes the **Fast & Slow Pointers** pattern.

**Problem Description: "Linked List Cycle"** (LeetCode Easy)

Given the `head` of a linked list, determine if the linked list has a cycle in it.

There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the `next` pointers. Internally, `pos` is used to denote the index of the node that tail's `next` pointer is connected to. **Note that `pos` is not passed as a parameter.**

Return `True` if there is a cycle in the linked list. Otherwise, return `False`.

**Constraints:**

  * The number of nodes in the list is in the range $[0, 10^5]$.
  * $-10^5 \\le Node.val \\le 10^5$

**Thought Process & Hints:**

1.  **Understanding the Goal:** Determine if the list eventually loops back on itself.

2.  **Initial Thoughts (and why they might fail or be inefficient):**

      * **Using a Set/Hash Map:** Iterate through the list. For each node, add it to a `set` (or hash map). If you encounter a node that's already in the set, a cycle exists.
          * Time: $O(N)$ (each node visited once, set insertion/lookup is $O(1)$ average).
          * Space: $O(N)$ (in the worst case, if no cycle, all nodes are added to the set).
          * This is a valid solution, but the interviewer might ask for an $O(1)$ space solution.

3.  **Optimization - Fast & Slow Pointers (Tortoise and Hare) Intuition:**

      * Imagine two runners on a circular track. If one runs twice as fast as the other, they will eventually meet if they start at the same point (or if the faster one starts just ahead).
      * In a linked list, if there's a cycle, the fast pointer will eventually "lap" the slow pointer.
      * If there's no cycle, the fast pointer will reach the end of the list (`None`) before it can ever meet the slow pointer.

4.  **Algorithm Sketch:**

      * Handle edge cases: If `head` is `None` or `head.next` is `None` (list has 0 or 1 node), there cannot be a cycle. Return `False`.
      * Initialize `slow = head`.
      * Initialize `fast = head.next`. (Or `fast = head` and move both inside the loop for first iteration). Let's go with `fast = head.next` to ensure fast is always ahead if a cycle exists.
      * Loop `while fast is not None and fast.next is not None`:
          * If `slow == fast`, a cycle is detected. Return `True`.
          * Move `slow` one step: `slow = slow.next`.
          * Move `fast` two steps: `fast = fast.next.next`.
      * If the loop finishes, `fast` (or `fast.next`) became `None`, meaning no cycle was found. Return `False`.

5.  **Complexity Analysis of Optimized Solution:**

      * Time Complexity: $O(N)$. In the worst case (no cycle), fast pointer traverses the entire list. In the best case (cycle near start), it finds it quickly. The number of steps is proportional to $N$.
      * Space Complexity: $O(1)$ because we only use two pointers. This is the optimal solution for space.

This problem is a canonical example of where precise pointer manipulation, rather than auxiliary data structures, leads to an optimal solution.

#### System Design Relevance

  * **Garbage Collection:** Some garbage collection algorithms (e.g., mark-and-sweep) implicitly traverse linked lists of objects to identify reachable memory. Detecting cycles is crucial to prevent memory leaks in reference-counted systems.
  * **Operating Systems (Process Scheduling):** Ready queues or wait queues for processes/threads can be implemented using linked lists. Circular linked lists are suitable for round-robin scheduling.
  * **File Systems (Disk Allocation):** Linked allocation is a method of allocating disk blocks to files, where each block contains a pointer to the next block of the file. This is analogous to a linked list on disk.
  * **Low-Level Memory Management:** In languages like C/C++, linked lists are frequently used for custom memory allocators or managing free memory blocks.
  * **Web Servers (Request Queues):** Incoming requests might be placed into a linked list-based queue for processing.

**Challenge to the Reader:**
The "Linked List Cycle II" problem extends the cycle detection to finding the *start node* of the cycle. How would you modify the Fast & Slow Pointer algorithm to locate the cycle's entry point, using only $O(1)$ space? (Hint: Think about the distances traveled by the pointers when they meet).