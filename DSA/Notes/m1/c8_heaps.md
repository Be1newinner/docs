### 8\. Graphs

#### Core Concepts

A graph is a non-linear data structure consisting of a finite set of **vertices** (or nodes) and a set of **edges** (or links) that connect pairs of vertices. Graphs are used to model pairwise relationships between objects.

**Key Terminology:**

  * **Vertex (Node):** A fundamental entity in a graph. Can represent anything (cities, people, web pages, states in a problem).
  * **Edge (Link/Arc):** A connection between two vertices.
  * **Directed Graph (Digraph):** Edges have a direction. If an edge goes from A to B, it doesn't necessarily mean you can go from B to A. Represented as `A -> B`.
      * **In-degree:** Number of incoming edges to a vertex.
      * **Out-degree:** Number of outgoing edges from a vertex.
  * **Undirected Graph:** Edges have no direction. If an edge connects A and B, you can traverse from A to B and from B to A. Represented as `A - B`.
      * **Degree:** Number of edges connected to a vertex.
  * **Weighted Graph:** Each edge has a numerical value (weight/cost) associated with it, representing distance, time, cost, etc.
  * **Unweighted Graph:** Edges have no associated weight; typically implies all edges have a weight of 1.
  * **Path:** A sequence of distinct vertices where each consecutive pair is connected by an edge.
  * **Cycle:** A path that starts and ends at the same vertex.
  * **Connected Graph:** In an undirected graph, every vertex is reachable from every other vertex.
  * **Strongly Connected Graph:** In a directed graph, every vertex is reachable from every other vertex.
  * **Component:** A maximal connected subgraph.
  * **Dense Graph:** A graph with many edges, approaching the maximum possible number of edges ($O(V^2)$).
  * **Sparse Graph:** A graph with relatively few edges (closer to $O(V)$ or $O(V \\log V)$).

**Practical Intuition:**

  * **Social Networks:** People (vertices) connected by friendships (edges).
  * **Road Networks:** Cities (vertices) connected by roads (edges). Weights could be distance or travel time.
  * **Flight Routes:** Airports (vertices) connected by direct flights (directed edges).
  * **Web Pages:** Pages (vertices) linked by hyperlinks (directed edges).
  * **Dependencies:** Tasks (vertices) that depend on other tasks (directed edges).

**Use Cases:**

  * **Modeling Relationships:** Social networks, citation networks, biological networks.
  * **Pathfinding:** GPS navigation (shortest path), network routing.
  * **Network Flow:** Optimizing resource allocation.
  * **Dependency Management:** Build systems, task scheduling.
  * **Web Crawlers:** Exploring the internet by following links.
  * **State-Space Search:** AI planning, game trees.

#### Representations

How a graph is stored in memory significantly impacts the efficiency of different operations.

1.  **Adjacency Matrix:**

      * An $V \\times V$ matrix (where $V$ is the number of vertices).
      * `matrix[i][j] = 1` (or weight) if there's an edge from `i` to `j`, `0` (or `INF`) otherwise.
      * For undirected graphs, the matrix is symmetric (`matrix[i][j] = matrix[j][i]`).
      * **Pros:**
          * Checking if an edge exists between `i` and `j` is $O(1)$.
          * Easy to implement.
      * **Cons:**
          * Space complexity: $O(V^2)$. Inefficient for sparse graphs.
          * Finding all neighbors of a vertex: $O(V)$ (must iterate through a row/column).
      * **Best for:** Dense graphs, small number of vertices.

2.  **Adjacency List:**

      * An array or dictionary where each index/key represents a vertex.
      * Each entry stores a list (or set) of vertices adjacent to that vertex.
      * For weighted graphs, the list would store `(neighbor, weight)` pairs.
      * **Pros:**
          * Space complexity: $O(V + E)$ (where $E$ is the number of edges). Much more space-efficient for sparse graphs.
          * Finding all neighbors of a vertex: $O(\\text{degree of vertex})$.
      * **Cons:**
          * Checking if an edge exists between `i` and `j`: $O(\\text{degree of } i)$ (potentially $O(V)$ in worst case for specific edge, but $O(1)$ on average if using a hash set for neighbors).
      * **Best for:** Sparse graphs, large number of vertices, most common choice in algorithms.

#### Python 3.11 Implementation (Adjacency List)

The adjacency list using a `dict` (or `defaultdict`) is the most Pythonic and common way to represent graphs for algorithmic problems.

```python
from collections import defaultdict, deque

# --- Graph Representation using Adjacency List (Python dict/defaultdict) ---

class Graph:
    def __init__(self, num_vertices, is_directed=False):
        self.num_vertices = num_vertices
        self.adj_list = defaultdict(list) # Key: vertex, Value: list of neighbors
        self.is_directed = is_directed

    def add_edge(self, u, v, weight=1):
        """Adds an edge between vertex u and v.
           For weighted graphs, store (neighbor, weight) tuples.
           For unweighted, just neighbor.
        """
        # For unweighted, we just append the neighbor
        self.adj_list[u].append(v)
        if not self.is_directed:
            self.adj_list[v].append(u) # Add reverse edge for undirected graph

    def get_neighbors(self, u):
        """Returns the list of neighbors for vertex u."""
        return self.adj_list[u]

    def print_graph(self):
        """Prints the adjacency list representation of the graph."""
        print("Graph Adjacency List:")
        for vertex in sorted(self.adj_list.keys()):
            neighbors_str = ", ".join(map(str, self.adj_list[vertex]))
            print(f"{vertex}: [{neighbors_str}]")

# --- Basic Graph Traversal Algorithms ---

def dfs_recursive(graph, start_node, visited=None):
    """
    Depth-First Search (DFS) - Recursive implementation.
    Explores as far as possible along each branch before backtracking.
    """
    if visited is None:
        visited = set()

    visited.add(start_node)
    print(start_node, end=" ") # Process/visit the node

    for neighbor in graph.get_neighbors(start_node):
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)

def dfs_iterative(graph, start_node):
    """
    Depth-First Search (DFS) - Iterative implementation using an explicit stack.
    """
    visited = set()
    stack = [start_node] # Use a list as a stack (LIFO)
    visited.add(start_node) # Mark as visited when adding to stack

    print("\nDFS (Iterative):")
    while stack:
        vertex = stack.pop()
        print(vertex, end=" ") # Process/visit the node

        # Get neighbors and add unvisited ones to stack
        # Important: Add neighbors in reverse order if you want to match recursive output
        # (e.g., process smaller neighbors first)
        # Or, simply iterate and accept the order based on list pop.
        for neighbor in sorted(graph.get_neighbors(vertex), reverse=True):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)

def bfs_traversal(graph, start_node):
    """
    Breadth-First Search (BFS) - Iterative implementation using a queue.
    Explores all neighbors at the current depth before moving to the next level.
    """
    visited = set()
    q = deque([start_node]) # Use a deque as a queue (FIFO)
    visited.add(start_node) # Mark as visited when adding to queue

    print("\nBFS:")
    while q:
        vertex = q.popleft()
        print(vertex, end=" ") # Process/visit the node

        for neighbor in graph.get_neighbors(vertex):
            if neighbor not in visited:
                visited.add(neighbor)
                q.append(neighbor)


# --- Example Usage ---
print("--- Undirected Graph Example ---")
# Create an undirected graph with 5 vertices
# Edges: (0,1), (0,2), (1,3), (2,3), (2,4)
undirected_g = Graph(5, is_directed=False)
undirected_g.add_edge(0, 1)
undirected_g.add_edge(0, 2)
undirected_g.add_edge(1, 3)
undirected_g.add_edge(2, 3)
undirected_g.add_edge(2, 4)

undirected_g.print_graph()
# Expected Output:
# 0: [1, 2]
# 1: [0, 3]
# 2: [0, 3, 4]
# 3: [1, 2]
# 4: [2]

print("DFS (Recursive) starting from 0:")
dfs_recursive(undirected_g, 0) # e.g., 0 1 3 2 4

dfs_iterative(undirected_g, 0) # e.g., 0 2 4 3 1

print("\nBFS starting from 0:")
bfs_traversal(undirected_g, 0) # e.g., 0 1 2 3 4

print("\n\n--- Directed Graph Example ---")
# Create a directed graph with 4 vertices
# Edges: (0,1), (0,2), (1,3), (2,3)
directed_g = Graph(4, is_directed=True)
directed_g.add_edge(0, 1)
directed_g.add_edge(0, 2)
directed_g.add_edge(1, 3)
directed_g.add_edge(2, 3)

directed_g.print_graph()
# Expected Output:
# 0: [1, 2]
# 1: [3]
# 2: [3]
# 3: []

print("DFS (Recursive) starting from 0:")
dfs_recursive(directed_g, 0) # e.g., 0 1 3 2

print("\nBFS starting from 0:")
bfs_traversal(directed_g, 0) # e.g., 0 1 2 3
```

#### Basic Traversal (DFS, BFS)

**1. Depth-First Search (DFS):**

  * **Strategy:** Explore as far as possible along each branch before backtracking. It goes deep into the graph before exploring other branches.
  * **Implementation:**
      * **Recursive:** Natural fit due to its recursive nature. Uses the implicit call stack.
      * **Iterative:** Uses an explicit stack (Python `list` with `append`/`pop`).
  * **Use Cases:**
      * Finding a path between two nodes.
      * Detecting cycles in a graph.
      * Topological sorting.
      * Finding connected components.
  * **Complexity:**
      * Time: $O(V + E)$ because each vertex and each edge is visited once.
      * Space: $O(V)$ for the recursion stack (recursive DFS) or explicit stack (iterative DFS) in the worst case (e.g., a long path graph), plus $O(V)$ for the `visited` set.

**2. Breadth-First Search (BFS):**

  * **Strategy:** Explore all the neighbor nodes at the present depth level before moving on to the nodes at the next depth level. It explores layer by layer.
  * **Implementation:** Always uses a queue (Python `collections.deque`).
  * **Use Cases:**
      * Finding the shortest path in an **unweighted** graph.
      * Finding all nodes within a certain distance from a source node.
      * Level order traversal of a tree (which is a special kind of graph).
      * Finding connected components.
  * **Complexity:**
      * Time: $O(V + E)$ because each vertex and each edge is visited once.
      * Space: $O(V)$ for the queue in the worst case (e.g., a wide graph where many nodes are in the same level), plus $O(V)$ for the `visited` set.

#### Handling Large Inputs / Constraints

  * **Graph Representation Choice:** For typical interview problems, stick to **Adjacency Lists** (`defaultdict(list)`). They are memory-efficient for sparse graphs (most common in interviews) and good for traversal. Adjacency matrices are only efficient for very dense graphs or when $V$ is very small.
  * **`visited` Set:** Always use a `set` to keep track of visited nodes during traversals (DFS/BFS) to prevent infinite loops in graphs with cycles and to ensure each node is processed only once. Failure to do so is a common bug.
  * **Disconnected Components:** If the problem requires processing all nodes in a graph, and the graph might be disconnected, you'll need an outer loop that iterates through all vertices and calls DFS/BFS on unvisited ones.
    ```python
    # Example for handling disconnected components
    # for vertex in range(graph.num_vertices): # Assuming vertices are 0 to N-1
    #     if vertex not in visited:
    #         dfs_recursive(graph, vertex, visited)
    ```
  * **Recursion Depth:** For large graphs and deep paths, recursive DFS can hit Python's recursion limit. In such cases, convert your DFS to an iterative one using an explicit stack.
  * **Weighted Graphs:** For weighted graphs, simple BFS/DFS don't guarantee shortest paths. You'll need algorithms like Dijkstra's (for non-negative weights) or Bellman-Ford (for negative weights).

#### Typical FAANG Problem Example

Let's pick a common graph traversal problem: **"Number of Islands"** (LeetCode Medium).

**Problem Description: "Number of Islands"**

Given an `m x n` 2D binary grid `grid` which represents a map of `'1'`s (land) and `'0'`s (water), return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.

**Constraints:**

  * `m == grid.length`
  * `n == grid[i].length`
  * `1 <= m, n <= 300`
  * `grid[i][j]` is `'0'` or `'1'`.

**Thought Process & Hints:**

1.  **Understanding the Goal:** Count distinct "landmasses" where land cells are connected horizontally or vertically. This is a classic **connected components** problem on a grid, which can be modeled as a graph.

2.  **Graph Analogy:**

      * Each `'1'` (land) cell is a **vertex**.
      * An edge exists between two land cells if they are **adjacent** (horizontally or vertically).
      * An "island" is a **connected component** of land cells.

3.  **Approach (DFS or BFS):**

      * Both DFS and BFS are suitable for finding connected components. Let's outline with DFS.
      * Iterate through each cell `(r, c)` in the grid.
      * If `grid[r][c]` is `'1'`:
          * We've found a new piece of land that belongs to an *uncounted* island. Increment `island_count`.
          * Start a traversal (DFS or BFS) from `(r, c)` to explore this entire island. During traversal, mark all visited land cells (e.g., by changing their value to `'0'` in the grid, or by adding them to a `visited` set) to ensure they are not counted again for another island.

4.  **Algorithm Sketch (DFS):**

      * Initialize `island_count = 0`.
      * Get `rows = len(grid)`, `cols = len(grid[0])`.
      * Define `directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]` for 4-directional movement.
      * Define a helper `dfs(r, c)` function:
          * **Base Cases/Boundary Conditions:**
              * If `r` or `c` is out of bounds.
              * If `grid[r][c]` is `'0'` (water).
              * Return (stop exploration).
          * **Mark Visited:** Change `grid[r][c]` to `'0'` (or add `(r, c)` to a `visited` set).
          * **Recurse Neighbors:** For each `(dr, dc)` in `directions`:
              * `dfs(r + dr, c + dc)`.
      * Main loop:
          * For `r` from `0` to `rows - 1`:
              * For `c` from `0` to `cols - 1`:
                  * If `grid[r][c]` is `'1'`:
                      * `island_count += 1`
                      * Call `dfs(r, c)` to explore and mark this entire island as visited.
      * Return `island_count`.

5.  **Complexity Analysis:**

      * Time Complexity: $O(M \\times N)$ where $M$ is rows and $N$ is columns. Each cell is visited at most twice (once by the outer loop, and once by DFS/BFS if it's land), and processed once.
      * Space Complexity: $O(M \\times N)$ in the worst case for the recursion stack (if DFS explores a long, snake-like island) or the queue (for BFS, if a whole row/column is land). The `grid` modification is in-place, so auxiliary space is mainly for the call stack/queue.

This problem beautifully demonstrates how grid problems can be translated into graph problems, and how standard graph traversals (DFS/BFS) are key to solving them.

#### System Design Relevance

  * **Social Network Services (e.g., Facebook, LinkedIn):**
      * Users are nodes, connections are edges. Graph algorithms find friends-of-friends (BFS), detect communities, or recommend connections.
  * **Route Planning & GPS Systems (e.g., Google Maps, Uber):**
      * Locations/intersections are nodes, roads are weighted edges. Dijkstra's, A\*, or Floyd-Warshall are used for shortest path calculations.
  * **Network Topology & Routing Protocols:**
      * Computers/routers are nodes, network cables are edges. Graph algorithms are vital for finding efficient data paths and managing network failures.
  * **Recommendation Engines:**
      * Users and items (products, movies) are nodes, interactions (likes, purchases) are edges. Graph-based algorithms identify relationships for recommendations.
  * **Search Engines (PageRank):**
      * Web pages are nodes, hyperlinks are directed edges. Algorithms like PageRank (based on graph theory) determine the importance of pages.
  * **Dependency Management:**
      * Software modules/tasks are nodes, dependencies are directed edges. Topological sorting is used to determine build order.
  * **Fraud Detection:**
      * Transactions, accounts, individuals are nodes; relationships between them are edges. Graph analysis can uncover suspicious patterns or rings of fraudsters.

**Challenge to the Reader:**
Consider the "Course Schedule" problem (LeetCode Medium), where you are given a number of courses and their prerequisites. How would you model this problem as a directed graph, and how could you use graph traversal (DFS or BFS) to determine if it's possible to finish all courses (i.e., if there's no cycle in the prerequisite graph)?