### 5. Queues

#### Core Concepts

A queue is a linear data structure that follows the **First-In, First-Out (FIFO)** principle. Imagine a line of people waiting to buy tickets: the first person to join the line is the first person to get served. New people join the back of the line, and people are served from the front.

**Key Operations:**

1.  **Enqueue (or Add/Offer):** Adds an element to the rear (back) of the queue.
2.  **Dequeue (or Remove/Poll):** Removes and returns the element from the front of the queue.
3.  **Front (or Peek):** Returns the element at the front of the queue without removing it.
4.  **isEmpty:** Checks if the queue is empty.
5.  **size:** Returns the number of elements in the queue.

**Practical Intuition:**

  * A waiting line at a bank, supermarket, or ticket counter.
  * A printer queue: documents are printed in the order they were submitted.
  * Customer service call center: calls are answered in the order they are received.
  * Message brokers/queues: messages are processed in the order they arrive.

**Use Cases:**

  * **Breadth-First Search (BFS):** Fundamental for graph and tree traversal.
  * **Task Scheduling:** Managing tasks in an operating system, print jobs, or CPU scheduling.
  * **Asynchronous Data Transfer:** Buffering data between processes that operate at different speeds.
  * **Web Server Request Handling:** Processing incoming client requests in order.
  * **Simulations:** Modeling real-world queuing systems.

**Time and Space Complexity:**

| Operation       | Time Complexity (Average & Worst) | Notes                                           |
| :-------------- | :-------------------------------- | :---------------------------------------------- |
| Enqueue         | $O(1)$                            | Using `collections.deque.append()`            |
| Dequeue         | $O(1)$                            | Using `collections.deque.popleft()`           |
| Front/Peek      | $O(1)$                            | Accessing `deque[0]`                          |
| isEmpty/size    | $O(1)$                            |                                                 |

**Space Complexity:** $O(N)$ where $N$ is the number of elements in the queue.

#### Python 3.11 Usage (`collections.deque`, `queue.Queue`)

Python provides excellent built-in options for queues.

1.  **`collections.deque` (Recommended for general algorithm problems):**
      * As discussed with stacks, `deque` (double-ended queue) is implemented as a doubly linked list. This makes adding/removing elements from *both* ends an $O(1)$ operation, which is perfect for queue functionality (`append` for enqueue, `popleft` for dequeue).
      * It's highly efficient and generally preferred in competitive programming.

<!-- end list -->

```python
from collections import deque

# Using collections.deque as a Queue
my_queue_deque = deque()

# Enqueue operation: use append()
my_queue_deque.append("Task A")
my_queue_deque.append("Task B")
my_queue_deque.append("Task C")
print(f"Queue after enqueues: {my_queue_deque}") # Output: deque(['Task A', 'Task B', 'Task C'])

# Front/Peek operation: access first element
if my_queue_deque:
    print(f"Front element (peek): {my_queue_deque[0]}") # Output: Task A

# Dequeue operation: use popleft()
served_task = my_queue_deque.popleft()
print(f"Served task: {served_task}, Queue now: {my_queue_deque}") # Output: Served task: Task A, Queue now: deque(['Task B', 'Task C'])

served_task = my_queue_deque.popleft()
print(f"Served task: {served_task}, Queue now: {my_queue_deque}") # Output: Served task: Task B, Queue now: deque(['Task C'])

# Check if empty
print(f"Is queue empty? {not my_queue_deque}") # Output: False

# Enqueue another task
my_queue_deque.append("Task D")
print(f"Queue after another enqueue: {my_queue_deque}") # Output: deque(['Task C', 'Task D'])

# Pop all elements
while my_queue_deque:
    print(f"Serving: {my_queue_deque.popleft()}")
# Output:
# Serving: Task C
# Serving: Task D
print(f"Is queue empty? {not my_queue_deque}") # Output: True
```

2.  **`queue.Queue` (Thread-safe, for multi-threading/concurrency):**
      * This module provides several queue implementations (`Queue`, `LifoQueue`, `PriorityQueue`) that are specifically designed for **thread-safe** inter-thread communication.
      * It includes built-in locking mechanisms to prevent race conditions when multiple threads access the same queue.
      * For *single-threaded* algorithmic problems, `collections.deque` is generally preferred because `queue.Queue` adds overhead for thread safety, which is unnecessary in that context.

<!-- end list -->

```python
import queue

# Using queue.Queue (thread-safe, typically for concurrent programming)
my_thread_safe_queue = queue.Queue()

# Enqueue: put()
my_thread_safe_queue.put("Message 1")
my_thread_safe_queue.put("Message 2")
print(f"Queue size after puts: {my_thread_safe_queue.qsize()}") # Output: 2

# Dequeue: get()
msg = my_thread_safe_queue.get()
print(f"Received message: {msg}, Queue size now: {my_thread_safe_queue.qsize()}") # Output: Received message: Message 1, Queue size now: 1

# Check if empty
print(f"Is queue empty? {my_thread_safe_queue.empty()}") # Output: False

# put_nowait() / get_nowait() can be used for non-blocking operations
# put(item, block=True, timeout=None) / get(block=True, timeout=None)
# 'block' parameter controls blocking behavior if queue is full (for fixed-size queues) or empty
```

**Best Practices:**

  * **Use `collections.deque` for DSA problems:** It's efficient ($O(1)$) and idiomatic for single-threaded scenarios.
  * **Use `queue.Queue` for concurrent programming:** When multiple threads or processes need to safely communicate via queues, the `queue` module provides the necessary synchronization primitives.
  * **Handle empty queue access:** Always check if a queue is empty before attempting to `popleft()` or `get()`, or handle the resulting `IndexError` (for `deque`) or `Empty` exception (for `queue.Queue`).

#### Problem-Solving Patterns

Queues are synonymous with **Breadth-First Search (BFS)** and level-order traversals.

1.  **Breadth-First Search (BFS) Traversal:**

      * **Concept:** Used to traverse or search tree or graph data structures. It explores all the neighbor nodes at the present depth level before moving on to the nodes at the next depth level. A queue is used to keep track of the nodes to visit.
      * **Algorithm Sketch:**
        1.  Start with a root/start node. Add it to the queue.
        2.  While the queue is not empty:
              * Dequeue a node.
              * Process/visit the node.
              * Enqueue all its unvisited neighbors.
              * Crucially, keep track of visited nodes (e.g., using a set) to avoid infinite loops in graphs with cycles.
      * **Examples:** Shortest path in an unweighted graph, level order tree traversal, finding all reachable nodes.

2.  **Level-Order Traversal (Trees):**

      * **Concept:** A specific application of BFS where you visit all nodes at a given level before moving to the next level. The queue naturally facilitates this.

3.  **Simulation Problems:**

      * **Concept:** Problems that mimic real-world processes where entities wait in line for service (e.g., bank queues, printer queues).

#### Handling Large Inputs / Constraints

  * **Memory Usage:** Like stacks, queues consume $O(N)$ space. For very wide graphs (many neighbors at a level) or long chains in BFS, the queue can grow very large. Be mindful of memory limits.
  * **Time Complexity:** BFS is $O(V + E)$ for graphs (Vertices + Edges) or $O(N)$ for trees (Nodes). For large graphs, ensuring your graph representation and visited set lookups are efficient is key.
  * **Edge Cases:** Empty queues, single-element queues, graphs with disconnected components (BFS from a single start node won't find them all).

#### Typical FAANG Problem Example

Let's look at a problem that is a direct application of Queue and BFS.

**Problem Description: "Walls and Gates"** (LeetCode Medium)

You are given an `m x n` grid `rooms` initialized with these three possible values:

  * `-1` (a wall or an obstacle)
  * `0` (a gate)
  * `INF` (Infinity, representing an empty room). We use `2^31 - 1` = `2147483647` to represent `INF` as you may assume that the distance to a gate is less than `2147483647`.

Fill each empty room with the distance to its nearest gate. If it is impossible to reach a gate, it should remain `INF`.

**Constraints:**

  * `m == rooms.length`
  * `n == rooms[i].length`
  * `1 <= m, n <= 250`

**Thought Process & Hints:**

1.  **Understanding the Goal:** For every `INF` cell, find the shortest distance to a `0` (gate). Shortest path in an unweighted grid immediately screams **BFS**.

2.  **BFS Approach:**

      * **Multiple Sources:** Notice that there can be multiple gates (`0`s). A standard BFS starts from a single source. How do we handle multiple sources?
          * Instead of running BFS from *each* `INF` cell (which would be $O(M \\times N \\times (M \\times N))$ and too slow), we can run a **multi-source BFS**.
          * Initialize the queue with *all* gate locations.
          * The distance for these initial gate cells is `0`.
      * **Distance Calculation:** Each time we dequeue a cell `(r, c)` with distance `d`, its unvisited neighbors will be at distance `d + 1`.

3.  **Algorithm Sketch (Multi-Source BFS):**

      * Initialize a `queue = collections.deque()`.
      * Iterate through the entire `rooms` grid.
      * For every cell `(r, c)` that contains a `0` (gate):
          * Add `(r, c)` to the `queue`.
          * The distance in `rooms[r][c]` is already `0`.
      * Define `directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]` for moving up, down, left, right.
      * While `queue` is not empty:
          * Dequeue `(r, c)`.
          * `current_distance = rooms[r][c]`.
          * For each `dr, dc` in `directions`:
              * `nr, nc = r + dr, c + dc` (neighbor row, neighbor column).
              * **Boundary Check:** Check if `(nr, nc)` is within the grid boundaries (`0 <= nr < m` and `0 <= nc < n`).
              * **Valid Move Check:** Check if `rooms[nr][nc]` is `INF` (meaning it's an empty, unvisited room).
              * If valid:
                  * Set `rooms[nr][nc] = current_distance + 1`. This marks it as visited and records its shortest distance.
                  * Enqueue `(nr, nc)`.

4.  **Complexity Analysis:**

      * Time Complexity: $O(M \\times N)$. Each cell is visited and enqueued at most once. Each cell has a constant number of neighbors.
      * Space Complexity: $O(M \\times N)$ in the worst case, if the entire grid is empty rooms, all cells might be in the queue simultaneously during BFS.

This problem is a perfect illustration of how BFS naturally finds the shortest path in unweighted graphs (like a grid), and how a multi-source BFS can be used when starting points are not singular.

#### System Design Relevance

  * **Message Queues / Brokers:** Fundamental in distributed systems (e.g., Kafka, RabbitMQ, SQS). They enable asynchronous communication, decoupling services, buffering messages, and ensuring reliable delivery.
  * **Load Balancing:** Incoming requests are often put into a queue before being distributed to available servers, ensuring fairness and preventing server overload.
  * **Operating System Schedulers:** CPU scheduling algorithms often use queues (e.g., ready queue for processes waiting for CPU, I/O queues for processes waiting for I/O).
  * **Event Handling:** Event loops in GUI applications or network servers use queues to process events (e.g., button clicks, incoming network packets) in the order they occur.
  * **Print Spoolers:** Manages print jobs in a FIFO manner.
  * **Traffic Management:** Simulating traffic flow, managing packets in network routers.

**Challenge to the Reader:**
Think about the "Implement Queue using Stacks" problem (LeetCode Easy). How can you use two stacks to simulate a FIFO queue? Consider the operations `push`, `pop`, `peek`, and `empty`. What are the time complexities for each of these operations in your two-stack implementation?