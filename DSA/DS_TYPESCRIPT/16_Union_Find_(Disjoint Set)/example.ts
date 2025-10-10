`
## Interview Question: Number of Connected Components in an Undirected Graph

**Problem:**

Given n nodes labeled from 0 to n - 1 and a list of undirected edges (each edge is a pair of nodes), find how many connected components there are in the graph.

**Example:**

Input:
n = 5
edges = [[0,1], [1,2], [3,4]]

Output: 2

Explanation: There are two connected components: {0,1,2} and {3,4}.


### Approach:
- Initialize Union Find with each node in its own set.
- For each edge, union the sets of the two nodes connected by the edge.
- At the end, the number of unique set leaders = number of connected components.
`

class UnionFind {
    parent: number[];
    rank: number[];
    count: number; // Number of connected components

    constructor(size: number) {
        this.parent = new Array(size);
        this.rank = new Array(size).fill(0);
        this.count = size;

        for (let i = 0; i < size; i++) {
            this.parent[i] = i; // Each node is its own parent initially
        }
    }

    find(x: number): number {
        if (this.parent[x] !== x) {
            // Path compression:
            this.parent[x] = this.find(this.parent[x]);
        }
        return this.parent[x];
    }

    union(x: number, y: number): void {
        let rootX = this.find(x);
        let rootY = this.find(y);

        if (rootX !== rootY) {
            // Union by rank to keep tree shallow
            if (this.rank[rootX] > this.rank[rootY]) {
                this.parent[rootY] = rootX;
            } else if (this.rank[rootX] < this.rank[rootY]) {
                this.parent[rootX] = rootY;
            } else {
                this.parent[rootY] = rootX;
                this.rank[rootX]++;
            }
            this.count--; // Two sets merged, so reduce component count
        }
    }

    getCount(): number {
        return this.count;
    }
}

function countComponents(n: number, edges: number[][]): number {
    const uf = new UnionFind(n);

    for (let [a, b] of edges) {
        uf.union(a, b);
    }

    return uf.getCount();
}

// Example dry run
const n = 5;
const edges = [[0, 1], [1, 2], [3, 4]];
console.log(countComponents(n, edges)); // Output: 2

`
## Explanation:

- We start with 5 nodes, each in their own component.
- Union(0,1) merges {0} and {1} → components reduced from 5 to 4.
- Union(1,2) merges {0,1} and {2} → components reduced to 3.
- Union(3,4) merges {3} and {4} → components reduced to 2.
- The final count is 2 connected components.
`