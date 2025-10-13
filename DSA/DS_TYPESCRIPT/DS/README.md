### What is a Graph?

A **graph** is a data structure that models pairwise relationships between objects (called "vertices" or "nodes") connected by "edges" (links). Think of a city map: intersections are nodes, roads are edges.

#### Types of Graphs:
- **Directed vs. Undirected**: Edges have a direction (like a one-way street) or not (two-way).
- **Weighted vs. Unweighted**: Edges may have a value (like distance/cost) or all edges are equal.
- **Cyclic vs. Acyclic**: Whether cycles (loops) are allowed or not.

***

### How do we represent graphs?

The two main ways:
- **Adjacency List**: For each node, keep a list of connected nodes. Space-efficient if the graph is sparse. *Imagine a phonebook per person with their friends inside*
- **Adjacency Matrix**: 2D matrix where cell `[i][j]` is `1` (or weight) if there’s an edge from `i` to `j`, else `0`. Fast edge lookup but uses more space for sparse graphs.

***

### Graph Methods (Standard Operations)

| Operation           | What it does                                             |
|---------------------|---------------------------------------------------------|
| addVertex(node)     | Adds a new node                                         |
| addEdge(u, v)       | Adds edge between u and v                               |
| removeVertex(node)  | Removes a node and all its edges                        |
| removeEdge(u, v)    | Removes an edge                                         |
| neighbors(node)     | Lists all adjacent nodes                                |
| hasEdge(u, v)       | Checks if u and v are connected                         |
| traversal methods   | BFS (Breadth-First), DFS (Depth-First) for searching    |
| size/numVertices()  | Returns number of nodes                                 |
| numEdges()          | Returns number of edges                                 |

***

### Graph in TypeScript (Adjacency List Example)

```typescript
class Graph {
    private adjList: Map<number, Set<number>> = new Map();

    addVertex(v: number): void {
        if (!this.adjList.has(v)) this.adjList.set(v, new Set());
    }

    addEdge(u: number, v: number): void {
        this.addVertex(u);
        this.addVertex(v);
        this.adjList.get(u)!.add(v); // Directed, for undirected add both ways
        // this.adjList.get(v)!.add(u);
    }

    removeEdge(u: number, v: number): void {
        this.adjList.get(u)?.delete(v);
    }

    removeVertex(v: number): void {
        this.adjList.delete(v);
        for (let neighbors of this.adjList.values()) neighbors.delete(v);
    }

    neighbors(v: number): number[] {
        return Array.from(this.adjList.get(v) ?? []);
    }
}
```

***

### Real-World Interview Intuition

- **Why adjacency list?** Space-efficient for common, sparse graphs (like real-world networks—cities, users, flight routes).
- **Matrix?** Useful for dense or small graphs, or when you need ultra-fast edge existence checks.

***

### Graph Types and Real-World Analogy

| Type                    | Analogy                  | Description                                                     |
|-------------------------|--------------------------|-----------------------------------------------------------------|
| Undirected Graph        | Friendship network       | Connections go both ways, no arrow on edges.                    |
| Directed Graph (Digraph)| Twitter followers        | Each connection (edge) has a direction.                         |
| Weighted Graph          | Road network             | Each edge has a weight (cost, distance, etc.)                   |
| Unweighted Graph        | Board games              | All connections are equal, no extra info on edges.              |
| Cyclic vs. Acyclic      | Travel vs. task scheduler| Cyclic: loops possible; Acyclic: no loops allowed.              |

***

### Graph Implementation Strategies

#### 1. **Adjacency List**
- **Description:** Each node has a list/set of neighbors.
- **TypeScript:** Map of node to a Set of adjacent nodes.
- **Space:** $$O(V+E)$$ — great for sparse graphs.
- **Edge Lookup:** $$O(k)$$, where $$k$$ is the degree of the node (neighbors count).
- **Typically Used For:** Real-world graphs with far fewer edges than $$(V^2)$$ (e.g., most social networks, router maps).

#### 2. **Adjacency Matrix**
- **Description:** 2D Array; matrix[i][j] stores info for edge i → j (1/0 or weight).
- **Space:** $$O(V^2)$$ — can be very heavy for large or sparse graphs.
- **Edge Lookup:** $$O(1)$$ — direct access.
- **Typically Used For:** Small, dense graphs; algorithms needing fast edge existence checks; sometimes used for Floyd-Warshall shortest path.

***

### Directed vs. Undirected Implementation

- **Adjacency List:**
  - Directed: Only store neighbor in one direction.
  - Undirected: Store neighbor in both directions.

- **Adjacency Matrix:**
  - Directed: Asymmetric matrix.
  - Undirected: Symmetric matrix ($$matrix[i][j] = matrix[j][i]$$).

***

### Weighted Graph Implementation

- **Adjacency List with weights:** Store a Map of neighbors to weights or an array of `[neighbor, weight]`.
- **Adjacency Matrix:** Cell stores numeric weight or `Infinity`/`null` if absent.

***

### Efficiency Trade-Offs

| Implementation | Pros                       | Cons                                 | Best For                     |
|----------------|----------------------------|--------------------------------------|------------------------------|
| List           | Space-efficient, easy traversal| Slower edge lookup ($$O(k)$$)      | Sparse graphs, BFS/DFS search|
| Matrix         | Fast edge queries ($$O(1)$$)| High space cost, slow to traverse   | Dense graphs, small graphs   |

***

### Examples in TypeScript

**Weighted Adjacency List:**
```typescript
class WeightedGraph {
    private adjList: Map<number, Map<number, number>> = new Map();
    addVertex(v: number): void {
        if (!this.adjList.has(v)) this.adjList.set(v, new Map());
    }
    addEdge(u: number, v: number, w: number): void {
        this.addVertex(u);
        this.addVertex(v);
        this.adjList.get(u)!.set(v, w);
    }
}
```

**Weighted Adjacency Matrix:**
```typescript
class MatrixGraph {
    private matrix: number[][];
    constructor(size: number) {
        this.matrix = Array.from({length: size}, () => Array(size).fill(Infinity));
    }
    addEdge(u: number, v: number, w: number): void {
        this.matrix[u][v] = w; // For undirected, also set [v][u]
    }
}
```

***

### Interview Reflection: Choosing the Right Representation

- **Sparse graph + frequent edge traversal/search:** **Adjacency list** is best.
- **Need fast edge existence checks + dense graph:** **Adjacency matrix** is best.
- **Need to store weights:** Pick either, but clearly organize weights per edge.