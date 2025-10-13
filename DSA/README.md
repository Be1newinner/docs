## Data Structures

### 1. BST

```typescript
class TreeNode implements BSTNodeInterface {
  val: number;
  left: TreeNode | null;
  right: TreeNode | null;

  constructor(val: number) {
    this.val = val;
    this.left = null;
    this.right = null;
  }
}

class BST implements BSTInterface {
  root: TreeNode | null;

  constructor(val?: number) {
    this.root = val === undefined ? null : new TreeNode(val);
  }

  private _postorder(node: TreeNode, nodeVals: number[]) {
    if (node.left) this._postorder(node.left, nodeVals);
    if (node.right) this._postorder(node.right, nodeVals);
    nodeVals.push(node.val);
  }

  private _deleteNode(node: TreeNode | null, val: number): TreeNode | null {
    if (!node) {
      return null;
    }

    if (val < node.val) {
      node.left = this._deleteNode(node.left, val);
    } else if (val > node.val) {
      node.right = this._deleteNode(node.right, val);
    } else {
      if (!node.left) {
        return node.right;
      } else if (!node.right) {
        return node.left;
      } else {
        const minRight = this.findMin(node.right);
        node.val = minRight!.val;
        node.right = this._deleteNode(node.right, minRight!.val);
      }
    }

    return node;
  }

  private _search(node: TreeNode | null, val: number): boolean {
    if (node == null) return false;

    if (node.val === val) return true;

    if (val < node.val) return this._search(node.left, val);

    // Last condition i.e. when val > node.val
    return this._search(node.right, val);
  }

  public insert(val: number) {
    const node = new TreeNode(val);

    if (this.root === null) {
      this.root = node;
      return;
    }

    let curr: TreeNode | null = this.root;
    let parent: TreeNode = curr;

    while (curr != null) {
      parent = curr;

      if (val < curr.val) {
        curr = curr.left;
      } else if (val > curr.val) {
        curr = curr.right;
      } else {
        // skip dublicates!
        return;
      }
    }

    if (val < parent.val) {
      parent.left = node;
    } else {
      parent.right = node;
    }
  }

  public preorder(): number[] {
    const nodeVals: number[] = [];

    if (!this.root) {
      return nodeVals;
    }

    function _preorder(node: TreeNode, nodeVals: number[]) {
      nodeVals.push(node.val);
      if (node.left) _preorder(node.left, nodeVals);
      if (node.right) _preorder(node.right, nodeVals);
    }

    _preorder(this.root, nodeVals);

    return nodeVals;
  }

  public inorder(): number[] {
    const nodeVals: number[] = [];

    if (!this.root) {
      return nodeVals;
    }

    function _inorder(node: TreeNode, nodeVals: number[]) {
      if (node.left) _inorder(node.left, nodeVals);
      nodeVals.push(node.val);
      if (node.right) _inorder(node.right, nodeVals);
    }

    _inorder(this.root, nodeVals);

    return nodeVals;
  }

  public postorder(): number[] {
    const nodeVals: number[] = [];

    if (!this.root) {
      return nodeVals;
    }

    this._postorder(this.root, nodeVals);
    return nodeVals;
  }

  public levelorder() {
    const result: number[] = [];
    if (!this.root) return result;

    const queue: TreeNode[] = [];
    queue.push(this.root);

    while (queue.length > 0) {
      const node = queue.shift()!;
      result.push(node?.val);

      if (node.left) queue.push(node.left);
      if (node.right) queue.push(node.right);
    }

    return queue;
  }

  public delete(val: number): TreeNode | null {
    this.root = this._deleteNode(this.root, val);
    return this.root;
  }

  public search(val: number): boolean {
    return this._search(this.root, val);
  }

  public findMin(node: TreeNode): TreeNode | null {
    while (node.left != null) {
      node = node.left;
    }
    return node;
  }

  public findMax(node: TreeNode): TreeNode {
    while (node.right) {
      node = node.right;
    }
    return node;
  }

  public getHeight(node: TreeNode | null = this.root): number {
    if (node === null) return -1;
    const leftHeight = this.getHeight(node.left);
    const rightHeight = this.getHeight(node.right);
    return Math.max(leftHeight, rightHeight) + 1;
  }
  public isValidBST(
    node: TreeNode | null = this.root,
    min: number | null = null,
    max: number | null = null
  ): boolean {
    if (node === null) return true;

    if (
      (min !== null && node.val <= min) ||
      (max !== null && node.val >= max)
    ) {
      return false;
    }

    if (!this.isValidBST(node.left, min, node.val)) return false;
    if (!this.isValidBST(node.right, node.val, max)) return false;

    return true;
  }

  public isEmpty(): boolean {
    return this.root === null;
  }
}

const bst = new BST(5);
bst.insert(2);
bst.insert(4);
bst.insert(1);
bst.insert(9);
bst.insert(5);
bst.insert(3);

console.log(bst.preorder());
```

### 2. Heaps

```typescript
class MinHeap implements IHeap<number> {
  private heap: number[];

  constructor() {
    this.heap = [];
  }

  size(): number {
    return this.heap.length;
  }

  peek(): number | null {
    if (this.size() === 0) return null;
    return this.heap[0];
  }

  insert(val: number): void {
    this.heap.push(val);
    this.heapifyUp();
  }

  extractMin(): number | null {
    if (this.size() === 0) return null;
    if (this.size() === 1) return this.heap.pop()!;

    const min = this.heap[0];
    this.heap[0] = this.heap.pop()!;
    this.heapifyDown();
    return min;
  }

  // Remove and return the top element (smallest in MinHeap)
  extractTop(): number | null {
    return this.extractMin();
  }

  // Build heap from an array (O(n) time)
  // suppose => [0,1,2,3,4,5] => i = (6 / 2) - 1 = 2
  buildHeap(arr: number[]): void {
    this.heap = arr.slice();
    for (let i = Math.floor(this.size() / 2) - 1; i >= 0; i--) {
      this.heapifyDown(i);
    }
  }

  // Update key at index and restore heap property
  updateKey(index: number, newVal: number): void {
    if (index < 0 || index >= this.size())
      throw new Error("Index out of range");
    const oldVal = this.heap[index];
    this.heap[index] = newVal;

    if (newVal < oldVal) {
      this.heapifyUp(index);
    } else {
      this.heapifyDown(index);
    }
  }

  // Remove element at index
  remove(index: number): void {
    if (index < 0 || index >= this.size())
      throw new Error("Index out of range");
    if (index === this.size() - 1) {
      this.heap.pop();
      return;
    }
    this.heap[index] = this.heap.pop()!;
    this.updateKey(index, this.heap[index]);
  }

  // Heap sort: returns a sorted array without modifying the original heap
  heapSort(): number[] {
    const copy = new MinHeap();
    copy.buildHeap(this.heap);
    const sorted: number[] = [];
    while (copy.size() > 0) {
      sorted.push(copy.extractMin()!);
    }
    return sorted;
  }

  // Overloaded heapify up to accept optional starting index (default last)
  private heapifyUp(startIndex?: number): void {
    let index = startIndex ?? this.size() - 1;
    while (index > 0) {
      let parentIndex = Math.floor((index - 1) / 2);
      if (this.heap[parentIndex] <= this.heap[index]) break;
      this.swap(index, parentIndex);
      index = parentIndex;
    }
  }

  // Overloaded heapify down to accept optional starting index (default root)
  private heapifyDown(startIndex = 0): void {
    let index = startIndex;
    const length = this.size();

    while (true) {
      let leftChildIndex = 2 * index + 1;
      let rightChildIndex = 2 * index + 2;
      let smallest = index;

      if (
        leftChildIndex < length &&
        this.heap[leftChildIndex] < this.heap[smallest]
      ) {
        smallest = leftChildIndex;
      }
      if (
        rightChildIndex < length &&
        this.heap[rightChildIndex] < this.heap[smallest]
      ) {
        smallest = rightChildIndex;
      }
      if (smallest === index) break;

      this.swap(index, smallest);
      index = smallest;
    }
  }

  private swap(i: number, j: number): void {
    [this.heap[i], this.heap[j]] = [this.heap[j], this.heap[i]];
  }
}
```

### 3. Stacks

```typescript
export class Stack implements StackInterface<number> {
  private data: number[] = [];
  push(item: number) {
    this.data.push(item);
  }
  pop(): number | undefined {
    return this.data.pop();
  }
  peek(): number | undefined {
    return this.data[this.size() - 1];
  }

  isEmpty(): boolean {
    return this.data.length === 0;
  }

  size(): number {
    return this.data.length;
  }
}
```

### 4. Queue

```typescript
export class StackQueue implements QueueInterface<number> {
  private stackIn: Stack = new Stack();
  private stackOut: Stack = new Stack();

  public enqueue(item: number) {
    this.stackIn.push(item);
  }

  public dequeue(): number | undefined {
    if (this.stackOut.size() === 0) {
      while (this.stackIn.size() > 0) {
        this.stackOut.push(this.stackIn.pop()!);
      }
    }
    return this.stackOut.pop();
  }

  public peek(): number | undefined {
    if (this.stackOut.size() === 0) {
      while (this.stackIn.size() > 0) {
        this.stackOut.push(this.stackIn.pop()!);
      }
    }
    return this.stackOut.peek();
  }

  public isEmpty(): boolean {
    return this.size() === 0;
  }

  public size(): number {
    return this.stackIn.size() + this.stackOut.size();
  }
}
```

### 5. Dequeue

```typescript

```

### 6. Circular Queue

```typescript

```

### 7. Singly Linked List

```typescript
class LLNode implements ListNodeInterface<number> {
  val: number;
  next: ListNodeInterface<number> | null;

  constructor(val: number) {
    this.val = val;
    this.next = null;
  }
}

export class LinkedList implements LinkedListInterface<number> {
  private head: ListNodeInterface<number> | null;
  private tail: ListNodeInterface<number> | null;

  constructor(val?: number) {
    this.head = val ? new LLNode(val) : null;
    this.tail = this.head;
  }

  append(item: number): void {
    const node = new LLNode(item);
    if (!this.head) {
      this.head = this.tail = node;
    } else {
      this.tail!.next = node;
      this.tail = this.tail!.next;
    }
  }

  prepend(item: number): void {
    const node = new LLNode(item);
    if (!this.head) {
      this.head = this.tail = node;
    } else {
      let curr = this.head;
      node.next = curr;
      this.head = node;
    }
  }

  delete(item: number): void {
    let curr = this.head;
    let parent: ListNodeInterface<number> | null = null;

    while (curr !== null) {
      if (curr.val === item) {
        if (!parent) {
          this.head = curr.next;
          if (this.tail === curr) {
            this.tail = this.head;
          }
        } else {
          parent.next = curr.next;
          if (this.tail === curr) {
            this.tail = parent;
          }
        }
        break;
      }
      parent = curr;
      curr = curr.next;
    }
  }

  find(item: number): ListNodeInterface<number> | null {
    let curr = this.head;

    while (curr != null) {
      if (curr.val === item) return curr;
      curr = curr.next;
    }

    return null;
  }

  isEmpty(): boolean {
    return this.head === null;
  }

  size(): number {
    let count = 0;
    let curr = this.head;

    while (curr != null) {
      count++;
      curr = curr.next;
    }

    return count;
  }
}
```

### 8. Doubly Linked List

```typescript
class DoublyLinkedListNode implements DoublyListNodeInterface<number> {
  public val: number;
  public next: DoublyListNodeInterface<number> | null;
  public prev: DoublyListNodeInterface<number> | null;

  constructor(val: number) {
    this.val = val;
    this.next = null;
    this.prev = null;
  }
}

export class DoublyLinkedList implements DoublyLinkedListInterface<number> {
  private head: DoublyListNodeInterface<number> | null;
  private tail: DoublyListNodeInterface<number> | null;

  constructor(val?: number) {
    this.head = val ? new DoublyLinkedListNode(val) : null;
    this.tail = this.head;
  }

  append(item: number): void {
    const node = new DoublyLinkedListNode(item);
    if (this.head === null) {
      this.head = this.tail = node;
    } else {
      this.tail!.next = node;
      node.prev = this.tail;
      this.tail = node;
    }
  }

  prepend(item: number): void {
    const node = new DoublyLinkedListNode(item);
    if (this.head === null) {
      this.head = this.tail = node;
    } else {
      this.head.prev = node;
      node.next = this.head;
      this.head = node;
    }
  }

  delete(item: number): void {
    if (this.head !== null) {
      let curr: DoublyListNodeInterface<number> | null = this.head;

      while (curr !== null) {
        if (curr.val === item) {
          if (curr.prev) {
            curr.prev.next = curr.next;
          }
          {
            this.head = curr.next;
          }

          if (curr.next) {
            curr.next.prev = curr.prev;
          } else {
            this.tail = curr.prev;
          }
          break;
        }

        curr = curr.next;
      }
    } else return;
  }

  deleteBack(): number | null {
    if (this.isEmpty()) {
      return null;
    } else {
      const nodeVal = this.tail!.val;
      if (this.tail === this.head) {
        this.tail = this.head = null;
      } else {
        this.tail = this.tail!.prev;
        this.tail!.next = null;
      }
      return nodeVal;
    }
  }

  deleteFront(): number | null {
    if (this.isEmpty()) {
      return null;
    } else {
      const nodeVal = this.head!.val;
      if (this.tail === this.head) {
        this.tail = this.head = null;
      } else {
        this.head = this.head!.next;
        this.head!.prev = null;
      }
      return nodeVal;
    }
  }

  find(item: number): DoublyListNodeInterface<number> | null {
    let curr = this.head;

    while (curr != null) {
      if (curr.val === item) return curr;
      curr = curr.next;
    }

    return null;
  }

  isEmpty(): boolean {
    return this.head === null;
  }

  size(): number {
    let count = 0;
    let curr = this.head;

    while (curr != null) {
      count++;
      curr = curr.next;
    }

    return count;
  }

  clear(): void {
    this.head = null;
    this.tail = null;
  }

  toArray(): number[] {
    const nodeVals: number[] = [];
    let curr = this.head;

    while (curr != null) {
      nodeVals.push(curr.val);
      curr = curr.next;
    }
    return nodeVals;
  }
}
```

### 9. Circular Linked List

```typescript

```

### 10. Bidirectional Graphs

```typescript
class BiDirectionalGraph implements GraphInterface<number> {
  data: number[][] = [];

  addVertex(): number {
    return this.data.push([]) - 1;
  }

  addEdge(vertex1: number, vertex2: number): void {
    if (!this.hasVertex(vertex1) || !this.hasVertex(vertex2))
      throw new Error("Vertexes doesn't exist");
    this.data[vertex1].push(vertex2);
    this.data[vertex2].push(vertex1);
  }

  removeVertex(vertex: number): void {
    if (!this.hasVertex(vertex)) throw new Error("Vertex doesn't exist");
    const edgesLength = this.data[vertex].length;
    this.data[vertex].splice(0, edgesLength);

    this.data.forEach((item) => {
      const vertexIdx = item.indexOf(vertex);
      if (vertexIdx >= 0) {
        item.splice(vertexIdx, 1);
      }
    });
  }

  removeEdge(vertex1: number, vertex2: number): void {
    if (!this.hasVertex(vertex1) || !this.hasVertex(vertex2))
      throw new Error("Vertexes doesn't exist");

    const vertex1Idx = this.data[vertex1].indexOf(vertex2);
    if (vertex1Idx >= 0) {
      this.data[vertex1].splice(vertex1Idx, 1);
    }

    const vertex2Idx = this.data[vertex2].indexOf(vertex1);
    if (vertex2Idx >= 0) {
      this.data[vertex2].splice(vertex2Idx, 1);
    }
  }

  getNeighbors(vertex: number): number[] {
    if (!this.hasVertex(vertex)) throw new Error("Vertex doesn't exist");
    return this.data[vertex];
  }

  hasVertex(vertex: number): boolean {
    return vertex < this.data.length;
  }

  hasEdge(vertex1: number, vertex2: number): boolean {
    return (
      this.data.length > Math.max(vertex1, vertex2) &&
      this.data[vertex1].includes(vertex2) &&
      this.data[vertex2].includes(vertex1)
    );
  }

  vertices(): number[] {
    return Array.from(this.data, (_, i) => i);
  }

  edges(): [number, number][] {
    const edges: [number, number][] = [];

    for (const i in this.data) {
      for (const j in this.data[i]) {
        const edge = [Number(i), this.data[i][j]];
        if (
          !edges.indexOf([edge[0], edge[1]]) ||
          !edges.includes([edge[1], edge[0]])
        )
          edges.push([Number(i), this.data[i][j]]);
      }
    }

    return edges;
  }
}
```

### 11. Bidirectional Graphs

```typescript
class DSU {
  parent: number[];
  size: number[];

  constructor(n: number) {
    this.parent = Array.from({ length: n }, (_, i) => i);
    this.size = Array(n).fill(1);
  }

  find(x: number): number {
    if (this.parent[x] !== x) {
      this.parent[x] = this.find(this.parent[x]); // path compression
    }
    return this.parent[x];
  }

  union(a: number, b: number): boolean {
    let ra = this.find(a),
      rb = this.find(b);
    if (ra === rb) return false; // already connected
    if (this.size[ra] < this.size[rb]) [ra, rb] = [rb, ra]; // union by size
    this.parent[rb] = ra;
    this.size[ra] += this.size[rb];
    return true;
  }

  connected(a: number, b: number): boolean {
    return this.find(a) === this.find(b);
  }
}

// Dry run:
// Start: 0,1,2,3 separate. union(0,1) -> {0,1}, union(2,3) -> {2,3}, connected(1,3)? false, union(1,3) -> {0,1,2,3}, connected(0,3)? true.
```

## Patterns

### 1. Prefix Sum

```typescript

```

### 2. Two Pointers

```typescript

```

### 3. Sliding Window

```typescript

```

### 4. Fast & Slow Pointers

```typescript

```

### 5. Linked List In-place Reversal

```typescript

```

### 6. Monotonic Stack

```typescript

```

### 7. Top K Elements

```typescript

```

### 8. Overlapping Intervals

```typescript

```

### 9. Modified Binary Search

```typescript

```

### 10. Binary Tree Traversal

```typescript

```

### 11. Depth First Search (DFS)

```typescript

```

### 12. Breadth First Search (BFS)

```typescript

```

### 13. Matrix Traversal

```typescript

```

### 14. Backtracking

```typescript

```

### 15. Dynamic Programming

```typescript

```

### 16. Union Find (Disjoint Set)

```typescript

```

### 17. Trie (Prefix Tree)

```typescript

```

### 18. Greedy Algorithms

```typescript

```

### 19. Topological Sort

```typescript

```

### 20. Bit Manipulation

```typescript

```

### 21. Sliding Window Maximum / Deque

```typescript

```

### 22. Segment Tree & Fenwick Tree (BIT)

```typescript

```
