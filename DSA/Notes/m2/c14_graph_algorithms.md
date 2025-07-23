### 14\. Graph Algorithms (Advanced Topics)

Building upon our understanding of graph representations and basic BFS/DFS, these algorithms solve more complex problems related to paths, cycles, and connectivity in weighted and unweighted graphs.

#### 14.1. Shortest Path Algorithms

**14.1.1. Dijkstra's Algorithm (Single Source Shortest Path - Non-Negative Weights)**

  * **Intuition:** A greedy algorithm that finds the shortest paths from a single source vertex to all other vertices in a weighted graph with **non-negative** edge weights. It works like a wave, progressively extending the "known shortest path" region.
  * **How it Works:**
    1.  Initialize distances to all vertices as infinity, except the source vertex (distance 0).
    2.  Use a **Min-Priority Queue (Min-Heap)** to store `(distance, vertex)` pairs, initially containing `(0, source)`.
    3.  While the priority queue is not empty:
          * Extract the vertex `u` with the smallest distance.
          * If `u` has already been finalized (its shortest path found), skip.
          * Mark `u` as finalized.
          * For each neighbor `v` of `u`:
              * Calculate `new_dist = dist[u] + weight(u, v)`.
              * If `new_dist < dist[v]`, update `dist[v] = new_dist` and push `(new_dist, v)` to the priority queue.
  * **Use Cases:** GPS navigation (shortest route), network routing protocols (OSPF), finding cheapest flights.
  * **Time Complexity:**
      * Using a Binary Min-Heap (Python's `heapq`): $O(E \\log V)$ or $O(E + V \\log V)$. `V` insertions/extractions take $V \\log V$, and `E` relaxation steps (updates) take $E \\log V$. More precisely, if using adjacency list, it's $O(E \\log V)$ for sparse graphs.
      * Using an array for `dist` and linearly scanning for minimum: $O(V^2)$ (less efficient for sparse graphs).
  * **Space Complexity:** $O(V + E)$ for adjacency list and distance array/priority queue.
  * **Limitations:** Does not work correctly with negative edge weights (for that, use Bellman-Ford).

<!-- end list -->

```python
import heapq
from collections import defaultdict

def dijkstra(graph, start_vertex):
    """
    Finds the shortest path from start_vertex to all other vertices
    in a graph with non-negative edge weights using Dijkstra's algorithm.

    Args:
        graph (dict): Adjacency list representation, e.g., {u: [(v1, w1), (v2, w2)], ...}
        start_vertex: The starting vertex.

    Returns:
        dict: A dictionary of shortest distances from start_vertex to all reachable vertices.
    """
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start_vertex] = 0
    
    # Priority queue: stores (distance, vertex) tuples
    # heapq is a min-heap, so it will always pop the vertex with the smallest distance
    priority_queue = [(0, start_vertex)] 
    
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        
        # If we found a shorter path to current_vertex already, skip
        if current_distance > distances[current_vertex]:
            continue
            
        for neighbor, weight in graph.get(current_vertex, []):
            distance = current_distance + weight
            
            # If a shorter path to neighbor is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
                
    return distances

# Example Usage:
# Graph represented as an adjacency list with weights
weighted_graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('A', 1), ('C', 2), ('D', 5)],
    'C': [('A', 4), ('B', 2), ('D', 1)],
    'D': [('B', 5), ('C', 1)]
}

print("--- Dijkstra's Algorithm ---")
shortest_paths = dijkstra(weighted_graph, 'A')
print(f"Shortest paths from A: {shortest_paths}") 
# Expected: {'A': 0, 'B': 1, 'C': 3, 'D': 4}
# (A->B:1, A->B->C:1+2=3, A->B->C->D:1+2+1=4)
```

**14.1.2. Bellman-Ford Algorithm (Single Source Shortest Path - Handles Negative Weights)**

  * **Intuition:** Relaxes all edges $V-1$ times. Since the shortest path in a graph with $V$ vertices can have at most $V-1$ edges (to avoid cycles), this ensures all paths are relaxed sufficiently. An additional $V$-th pass can detect negative cycles.
  * **Time Complexity:** $O(V \\cdot E)$. Slower than Dijkstra's but handles negative weights.
  * **Space Complexity:** $O(V)$ for distances, $O(E)$ for edges if stored separately.
  * **Use Cases:** Distributed routing protocols (RIP), graphs with negative edge weights.

**14.1.3. Floyd-Warshall Algorithm (All-Pairs Shortest Path)**

  * **Intuition:** A Dynamic Programming algorithm that finds the shortest paths between all pairs of vertices in a weighted graph (can handle negative weights, but not negative cycles). It considers all intermediate vertices `k` one by one.
  * **How it Works:** Uses a 3D DP table (conceptually `dp[k][i][j]`) or 2D (iteratively): `dp[i][j]` represents the shortest path from `i` to `j` using only vertices `0` to `k-1` as intermediate vertices. The update rule is `dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j])`.
  * **Time Complexity:** $O(V^3)$.
  * **Space Complexity:** $O(V^2)$ for the distance matrix.
  * **Use Cases:** Small dense graphs where all-pairs shortest paths are needed, detecting transitive closure.

#### 14.2. Minimum Spanning Tree (MST) Algorithms

A **Minimum Spanning Tree (MST)** of a connected, undirected, weighted graph is a subgraph that is a tree, connects all the vertices together, and has the minimum possible total edge weight.

**14.2.1. Prim's Algorithm**

  * **Intuition:** A greedy algorithm that builds the MST by growing it from an arbitrary starting vertex. It always adds the cheapest edge that connects a vertex in the MST to a vertex outside the MST.
  * **How it Works:**
    1.  Start with an arbitrary vertex in the MST.
    2.  Maintain a min-priority queue of edges, prioritized by weight, that connect a vertex inside the MST to a vertex outside.
    3.  Repeatedly extract the minimum-weight edge from the priority queue that connects to a new vertex. Add the vertex and edge to the MST.
    4.  Add all edges from the newly added vertex to its unvisited neighbors to the priority queue.
  * **Time Complexity:** $O(E \\log V)$ or $O(E + V \\log V)$ using a binary min-heap (similar to Dijkstra's).
  * **Space Complexity:** $O(V + E)$.
  * **Use Cases:** Network design, cluster analysis.

**14.2.2. Kruskal's Algorithm**

  * **Intuition:** Another greedy algorithm that builds the MST by considering edges in increasing order of weight. It adds an edge if it connects two previously disconnected components.
  * **How it Works:**
    1.  Sort all edges in non-decreasing order of their weights.
    2.  Initialize each vertex as its own disjoint set.
    3.  Iterate through the sorted edges:
          * For each edge `(u, v)` with weight `w`:
              * If `u` and `v` are in different sets (i.e., adding this edge won't form a cycle), add the edge to the MST and union the sets of `u` and `v`.
    <!-- end list -->
      * Stop when $V-1$ edges have been added to the MST.
  * **Key Data Structure:** **Disjoint Set Union (DSU)** for efficient `find` (checking if in same set) and `union` (merging sets) operations.
  * **Time Complexity:** $O(E \\log E)$ (dominated by sorting edges) or $O(E \\log V)$ if using a DSU data structure (since $E \\le V^2$, $\\log E \\approx 2 \\log V$).
  * **Space Complexity:** $O(V + E)$.
  * **Use Cases:** Network design, solving maze problems.

#### 14.3. Topological Sort

  * **Intuition:** A linear ordering of vertices in a **Directed Acyclic Graph (DAG)** such that for every directed edge `u -> v`, vertex `u` comes before vertex `v` in the ordering. It's like finding a valid sequence of tasks where some tasks depend on others.
  * **Existence:** A topological sort is possible **if and only if** the graph is a DAG (contains no directed cycles).
  * **Algorithms:**
    1.  **Kahn's Algorithm (BFS-based):**
          * Find all vertices with an in-degree of 0. Add them to a queue.
          * While the queue is not empty:
              * Dequeue a vertex `u`, add it to the topological order.
              * For each neighbor `v` of `u`: decrement `v`'s in-degree. If `v`'s in-degree becomes 0, enqueue `v`.
          * If the final topological order contains fewer than $V$ vertices, a cycle exists.
    2.  **DFS-based Algorithm:**
          * Perform a DFS. When a recursive call returns from a vertex (i.e., all its descendants have been visited), add the vertex to the front of a list (or push to a stack). The final list/stack will be the topological order.
          * Cycles can be detected if DFS encounters a visited node that is currently in the recursion stack.
  * **Time Complexity:** $O(V + E)$ (similar to BFS/DFS).
  * **Space Complexity:** $O(V + E)$.
  * **Use Cases:** Task scheduling (dependencies), course prerequisite systems, build systems (compiling modules in order), dependency resolution (e.g., in package managers).

<!-- end list -->

```python
# --- Topological Sort (Kahn's Algorithm - BFS based) ---
from collections import defaultdict, deque

def topological_sort(num_vertices, edges):
    """
    Performs topological sort using Kahn's algorithm.
    Returns a list representing a valid topological order, or empty list if cycle detected.
    """
    # Build adjacency list and in-degrees
    adj = defaultdict(list)
    in_degree = [0] * num_vertices # Assuming vertices are 0 to num_vertices-1
    
    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1
    
    # Initialize queue with all vertices having in-degree 0
    q = deque([i for i in range(num_vertices) if in_degree[i] == 0])
    
    topo_order = []
    
    while q:
        u = q.popleft()
        topo_order.append(u)
        
        # For each neighbor, decrement in-degree and add to queue if it becomes 0
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                q.append(v)
                
    # If topo_order contains all vertices, it's a valid topological sort
    # Otherwise, a cycle exists
    if len(topo_order) == num_vertices:
        return topo_order
    else:
        return [] # Cycle detected

# Example Usage: Course Schedule (0: Course, 1: Prereq of 0)
# Graph: 1 -> 0, 2 -> 0, 3 -> 1, 3 -> 2
# Possible orders: [3, 2, 1, 0] or [3, 1, 2, 0]
num_courses = 4
prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]] # (course, prereq) means prereq must be taken before course
# Convert to u -> v edges (prereq -> course)
edges = [[p[1], p[0]] for p in prerequisites] 

print("\n--- Topological Sort (Kahn's Algorithm) ---")
order = topological_sort(num_courses, edges)
if order:
    print(f"Topological order: {order}") # e.g., [3, 1, 2, 0] or [3, 2, 1, 0]
else:
    print("Cycle detected, no topological order.")

# Example with a cycle: 0 -> 1, 1 -> 0
print("\n--- Topological Sort (with Cycle) ---")
order_with_cycle = topological_sort(2, [[0, 1], [1, 0]])
if order_with_cycle:
    print(f"Topological order: {order_with_cycle}")
else:
    print("Cycle detected, no topological order.") # Output: Cycle detected, no topological order.
```

#### Handling Large Inputs / Constraints

  * **Graph Representation:** Adjacency lists (using `defaultdict(list)`) are almost always preferred over adjacency matrices for these algorithms, especially for sparse graphs, due to better space complexity ($O(V+E)$ vs $O(V^2)$).
  * **Priority Queues (`heapq`):** Essential for efficient implementations of Dijkstra's and Prim's.
  * **Disjoint Set Union (DSU):** Crucial for an efficient Kruskal's algorithm. Understanding its `find` (with path compression) and `union` (by rank/size) operations is key.
  * **Edge Cases:** Disconnected graphs (Dijkstra's will only find paths in the component of the source), graphs with 1 or 2 vertices, empty graphs, handling self-loops or parallel edges (usually ignored or handled as single edge).
  * **Negative Cycles:** Algorithms like Dijkstra's and Floyd-Warshall (for all-pairs) don't work with negative cycles. Bellman-Ford can detect them.

#### Typical FAANG Problem Example

Let's consider a problem requiring **Dijkstra's Algorithm**.

**Problem Description: "Network Delay Time"** (LeetCode Medium)

You are given a network of `n` nodes labeled from `1` to `n`. You are also given `times`, a list of travel times as directed edges `times[i] = (u_i, v_i, w_i)`, where `u_i` is the source node, `v_i` is the target node, and `w_i` is the time it takes for a signal to travel from `u_i` to `v_i`.

We will send a signal from a given node `k`. Return the minimum time it takes for all `n` nodes to receive the signal. If it is impossible for all `n` nodes to receive the signal, return `-1`.

**Constraints:**

  * `1 <= n <= 100` (Small `n` suggests $V^2$ or $V^3$ might pass, but $E \\log V$ is optimal)
  * `1 <= k <= n`
  * `1 <= times.length <= 6000`
  * `times[i].length == 3`
  * `1 <= u_i, v_i <= n`
  * `u_i != v_i`
  * `0 <= w_i <= 100` (Crucial: non-negative weights\!)
  * All the pairs `(u_i, v_i)` are unique.

**Thought Process & Hints:**

1.  **Understanding the Goal:** Find the time it takes for a signal from node `k` to reach *all* other nodes. This is equivalent to finding the maximum of the shortest path times from `k` to every other node. If any node is unreachable, return -1.

2.  **Identify the Algorithm:**

      * "Shortest path from a single source" (node `k`)? Yes.
      * "Weighted graph"? Yes.
      * "Non-negative edge weights"? Yes (`0 <= w_i <= 100`).
      * **Conclusion: Dijkstra's Algorithm** is perfect for this.

3.  **Graph Representation:**

      * Convert the `times` list into an adjacency list. Since nodes are 1-indexed, use a `defaultdict(list)` where keys are nodes and values are lists of `(neighbor, weight)` tuples.

4.  **Algorithm Steps (Dijkstra Adaptation):**

    1.  Build the adjacency list from `times`.
    2.  Initialize `distances` dictionary (or array) where `distances[i]` stores the shortest time for signal to reach node `i` from `k`. Set `distances[k] = 0` and others to `infinity`.
    3.  Use a min-priority queue (`heapq`) to store `(time, node)` pairs, initially `[(0, k)]`.
    4.  Implement Dijkstra's core logic:
          * Pop `(current_time, u)` from heap.
          * If `current_time > distances[u]`, continue (already found a shorter path).
          * For each `v, travel_time` in `adj[u]`:
              * If `distances[u] + travel_time < distances[v]`:
                  * `distances[v] = distances[u] + travel_time`
                  * `heapq.heappush(pq, (distances[v], v))`
    5.  After Dijkstra's finishes, iterate through `distances`.
          * If any node `i` still has `distances[i] == infinity`, it means that node is unreachable. Return `-1`.
          * Otherwise, the answer is the maximum value in `distances` (this is the time when the *last* node receives the signal).

5.  **Complexity Analysis:**

      * Time: $O(E \\log V)$, where $V=n$ (nodes) and $E=\\text{times.length}$ (edges). Given $N=100, E=6000$, $6000 \\times \\log 100 \\approx 6000 \\times 7 = 42000$, which is very efficient.
      * Space: $O(V + E)$ for adjacency list, distances, and priority queue.

#### System Design Relevance

  * **Network Routing:** Core of how data packets find their way across the internet (e.g., OSPF uses Dijkstra's).
  * **GPS Navigation / Mapping Services:** Finding the shortest or fastest routes between locations.
  * **Dependency Resolution:** Topological sort is used in build systems (e.g., Makefiles, Maven, Gradle) to determine the order in which modules should be compiled or tasks executed based on dependencies.
  * **Task Scheduling:** Scheduling jobs in a distributed system, especially with dependencies, can use topological sort.
  * **Resource Provisioning:** Determining minimum cost connections in a cloud network (MST).
  * **Supply Chain Optimization:** Finding optimal routes for delivery or managing inventory flow.
  * **Social Network Analysis:** Finding shortest paths between users, detecting communities (based on graph properties).

**Challenge to the Reader:**
Consider the "Course Schedule II" problem (LeetCode Medium). You are given `numCourses` and `prerequisites` (e.g., `[0,1]` means you must take course `1` before course `0`). Return the ordering of courses you should take to finish all courses. If it's impossible to finish all courses (due to a cycle), return an empty array. How does this problem relate directly to **Topological Sort**, and how would you adapt Kahn's algorithm (BFS-based) to solve it?
