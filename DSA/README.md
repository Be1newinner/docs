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

## PATTERNS

### 1. Prefix Sum

Use when frequent range-sum queries or subarray-sum conditions appear; compute cumulative sums to answer ranges in O(1) or to detect target sums with a hash map.

```typescript
// 1) Range sum query (immutable array)
function buildPrefix(nums: number[]): number[] {
  const pref = new Array(nums.length + 1).fill(0);
  for (let i = 0; i < nums.length; i++) pref[i + 1] = pref[i] + nums[i];
  return pref;
}
// sum over [l, r] inclusive
function rangeSum(pref: number[], l: number, r: number): number {
  return pref[r + 1] - pref[l];
}

// 2) Count subarrays with sum = k (handles negatives)
function countSubarraysSumK(nums: number[], k: number): number {
  const freq = new Map<number, number>();
  freq.set(0, 1); // empty prefix
  let cur = 0,
    ans = 0;
  for (const x of nums) {
    cur += x;
    ans += freq.get(cur - k) ?? 0;
    freq.set(cur, (freq.get(cur) ?? 0) + 1);
  }
  return ans;
}
```

- Intuition: prefix[i] holds sum up to index i-1; range sums become subtraction; for target k, if curSum - k existed before, a subarray sums to k.
- Complexity: building prefix is O(n); each query O(1); hash-map variant is O(n) time, O(n) space.
- Dry-run (countSubarraysSumK on , k=3): cur=1 (need -2 none), cur=3 (need 0 exists → +1), cur=6 (need 3 exists once → +1) → answer 2.

### 2. Two Pointers

Use on sorted arrays/strings, or when scanning from both ends to meet a condition (pair sum, dedup, partition). Eliminates nested loops by coordinated pointer moves.

```typescript
// Pair sum in sorted array: return indices or [-1,-1]
function twoSumSorted(nums: number[], target: number): [number, number] {
  let l = 0,
    r = nums.length - 1;
  while (l < r) {
    const s = nums[l] + nums[r];
    if (s === target) return [l, r];
    if (s < target) l++;
    else r--;
  }
  return [-1, -1];
}

// Remove duplicates in-place (sorted), return new length
function dedupeSorted(nums: number[]): number {
  if (nums.length === 0) return 0;
  let w = 1; // write pointer
  for (let r = 1; r < nums.length; r++) {
    if (nums[r] !== nums[r - 1]) nums[w++] = nums[r];
  }
  return w;
}
```

- Intuition: in ascending arrays, moving left rightward increases sum, moving right leftward decreases sum; this monotonicity drives pointer updates.
- Complexity: O(n) time, O(1) space.
- Dry-run (twoSumSorted on , target=9): l=0,r=4 sum=12>9 → r=3 sum=8<9 → l=1 sum=9 → return.

### 3. Sliding Window

Use for subarray/substring best-of problems: fixed window (size k) or variable window (maintain a constraint like at most K distinct). Keep aggregated state as window slides.

```typescript
// Fixed-size: max sum of any k-length subarray
function maxSumFixedWindow(nums: number[], k: number): number {
  if (k > nums.length) return 0;
  let sum = 0;
  for (let i = 0; i < k; i++) sum += nums[i];
  let best = sum;
  for (let r = k; r < nums.length; r++) {
    sum += nums[r] - nums[r - k];
    if (sum > best) best = sum;
  }
  return best;
}

// Variable-size: length of longest substring with at most K distinct chars
function lengthOfLongestSubstringKDistinct(s: string, k: number): number {
  if (k === 0) return 0;
  let l = 0,
    best = 0;
  const cnt = new Map<string, number>();
  for (let r = 0; r < s.length; r++) {
    cnt.set(s[r], (cnt.get(s[r]) ?? 0) + 1);
    while (cnt.size > k) {
      const ch = s[l];
      const v = (cnt.get(ch) ?? 0) - 1;
      if (v === 0) cnt.delete(ch);
      else cnt.set(ch, v);
      l++;
    }
    best = Math.max(best, r - l + 1);
  }
  return best;
}
```

- Intuition: fixed window updates by adding one element and removing one; variable window expands right and shrinks left to restore constraints while tracking best.
- Complexity: both patterns are O(n) time, O(1) or O(\sigma) space for counts.
- Dry-run (maxSumFixedWindow on , k=3): initial 8; slide to sums 7,9,6 → best 9.

### 4. Fast & Slow Pointers

Use on linked lists to detect cycles, find cycle start, or find middle node; fast moves 2x, slow moves 1x (Floyd’s algorithm).

```typescript
class ListNode {
  val: number;
  next: ListNode | null = null;
  constructor(val: number) {
    this.val = val;
  }
}

// Detect cycle existence
function hasCycle(head: ListNode | null): boolean {
  let slow = head,
    fast: ListNode | null = head;
  while (fast && fast.next) {
    slow = slow!.next;
    fast = fast.next.next;
    if (slow === fast) return true;
  }
  return false;
}

// Find middle node (for even length returns second middle)
function middleNode(head: ListNode | null): ListNode | null {
  let slow = head,
    fast = head;
  while (fast && fast.next) {
    slow = slow!.next;
    fast = fast.next.next;
  }
  return slow ?? null;
}
```

- Intuition: if a cycle exists, fast laps slow and they meet; otherwise fast hits null; similarly, fast jumping two steps makes slow land at middle when fast finishes.
- Complexity: O(n) time, O(1) space.
- Dry-run (hasCycle): with a 3-node cycle, after steps, pointers meet at some cycle node, returning true.

### 5. Linked List In-place Reversal

Reverse a sublist or entire list by rewiring next pointers; cornerstone for many LL problems (k-group reversals, palindrome check second half)

```typescript
// Reverse entire list
function reverseList(head: ListNode | null): ListNode | null {
  let prev: ListNode | null = null,
    cur = head;
  while (cur) {
    const nxt = cur.next;
    cur.next = prev;
    prev = cur;
    cur = nxt;
  }
  return prev;
}

// Reverse sublist [m, n] (1-indexed) in-place
function reverseBetween(
  head: ListNode | null,
  m: number,
  n: number
): ListNode | null {
  if (!head || m === n) return head;
  const dummy = new ListNode(0);
  dummy.next = head;
  let pre = dummy;
  for (let i = 1; i < m; i++) pre = pre.next!;
  let cur = pre.next!;
  for (let i = 0; i < n - m; i++) {
    const move = cur.next!;
    cur.next = move.next;
    move.next = pre.next;
    pre.next = move;
  }
  return dummy.next;
}
```

- Intuition: iterative reverse uses three pointers (prev, cur, next); sublist reverse uses head-insertion within the subrange to rotate nodes to the front.
- Complexity: O(n) time, O(1) space.
- Dry-run (reverseBetween on 1→2→3→4→5, m=2, n=4): repeatedly move node after cur to pre.next, transforming to 1→4→3→2→5.

Interview usage notes

- Start with brute force and articulate why it’s O(n^2) then introduce the pattern and show how it becomes O(n)
- Call out edge cases explicitly: empty inputs, window size > n, negatives for prefix-sum counting, and off-by-one in ranges.
- Choose patterns by constraints: sorted inputs → two pointers; substring/stream constraints → sliding window; many range queries → prefix sums; linked list structure → fast/slow and in-place reversal.

### 6. Monotonic Stack

```typescript
// 1) Next Greater Element (to the right) — monotonic decreasing stack
// Returns for each i: first value to the right that is > nums[i], or -1
export function nextGreaterElementsRight(nums: number[]): number[] {
  const n = nums.length;
  const ans = Array(n).fill(-1);
  const st: number[] = []; // stack of indices, values decreasing

  for (let i = 0; i < n; i++) {
    while (st.length && nums[i] > nums[st[st.length - 1]]) {
      const j = st.pop()!;
      ans[j] = nums[i];
    }
    st.push(i);
  }
  return ans;
}

// 2) Next Smaller Element (to the right) — monotonic increasing stack
// Returns for each i: first value to the right that is < nums[i], or -1
export function nextSmallerElementsRight(nums: number[]): number[] {
  const n = nums.length;
  const ans = Array(n).fill(-1);
  const st: number[] = []; // increasing values

  for (let i = 0; i < n; i++) {
    while (st.length && nums[i] < nums[st[st.length - 1]]) {
      const j = st.pop()!;
      ans[j] = nums[i];
    }
    st.push(i);
  }
  return ans;
}

// 3) Previous Greater/Smaller (to the left)
// Same idea but sweep left->right and fill using stack top when needed
export function prevGreaterIndexLeft(nums: number[]): number[] {
  const n = nums.length,
    ans = Array(n).fill(-1);
  const st: number[] = []; // decreasing values
  for (let i = 0; i < n; i++) {
    while (st.length && nums[st[st.length - 1]] <= nums[i]) st.pop();
    ans[i] = st.length ? st[st.length - 1] : -1; // index of previous greater
    st.push(i);
  }
  return ans;
}

// 4) Circular Next Greater Element (LeetCode 503 style)
// Sweep twice; use modulo to simulate wrap-around
export function nextGreaterCircular(nums: number[]): number[] {
  const n = nums.length;
  const ans = Array(n).fill(-1);
  const st: number[] = []; // stack holds values (or indices); use values for simplicity

  for (let t = 2 * n - 1; t >= 0; t--) {
    const i = t % n;
    while (st.length && st[st.length - 1] <= nums[i]) st.pop();
    if (t < n && st.length) ans[i] = st[st.length - 1];
    st.push(nums[i]);
  }
  return ans;
}

// 5) Daily Temperatures (distance to next greater value)
// Return distances instead of values
export function dailyTemperatures(temperatures: number[]): number[] {
  const n = temperatures.length;
  const ans = Array(n).fill(0);
  const st: number[] = []; // indices with decreasing temperatures

  for (let i = 0; i < n; i++) {
    while (st.length && temperatures[i] > temperatures[st[st.length - 1]]) {
      const j = st.pop()!;
      ans[j] = i - j; // distance to next warmer
    }
    st.push(i);
  }
  return ans;
}
```

### 7. Top K Elements

#### USING HEAPS

```typescript
function topKFrequentUsingHeaps(nums: number[], k: number): number[] {
  const freqMap: Map<number, number> = new Map();

  // Step 1: Count frequency of each element
  for (const num of nums) {
    freqMap.set(num, (freqMap.get(num) || 0) + 1);
  }

  // Step 2: Use a MinHeap to keep top k frequent elements
  const minHeap = new MinHeap();
  for (const [num, freq] of freqMap.entries()) {
    minHeap.insert([freq, num]);
    if (minHeap.size() > k) {
      minHeap.extractMin();
    }
  }

  // Step 3: Extract elements from heap
  const result: number[] = [];
  while (minHeap.size() > 0) {
    const [freq, num] = minHeap.extractMin()!;
    result.push(num);
  }
  return result.reverse();
}
```

#### Quick Select Using Tree (SIMPLE)

```typescript
class TreeNode {
  val: number;
  left: TreeNode | null;
  right: TreeNode | null;
  constructor(val: number) {
    this.val = val;
    this.left = null;
    this.right = null;
  }
}

function topKLargestInBST(root: TreeNode | null, k: number): number[] {
  const result: number[] = [];
  function reverseInorder(node: TreeNode | null) {
    if (!node || result.length >= k) return;
    reverseInorder(node.right);
    if (result.length < k) {
      result.push(node.val);
      reverseInorder(node.left);
    }
  }
  reverseInorder(root);
  return result;
}
```

#### Quick Select Using Arrays (SIMPLE)

```typescript
function topKFrequentUsingArray(nums: number[], k: number): number[] {
  // Step 1: Frequency Map - Count frequency of each element
  const frequencyMap: Map<number, number> = new Map();
  for (const num of nums) {
    frequencyMap.set(num, (frequencyMap.get(num) || 0) + 1);
  }

  // Step 2: Create array of [num, frequency] pairs
  const freqArray: [number, number][] = Array.from(frequencyMap.entries());

  // Step 3: Sort the freqArray by frequency in descending order
  freqArray.sort((a, b) => b[1] - a[1]);

  // Step 4: Extract top k elements
  const result: number[] = [];
  for (let i = 0; i < k; i++) {
    result.push(freqArray[i][0]);
  }

  return result;
}
```

### 8. Overlapping Intervals

#### Iterative Merging with a Stack or List

```typescript
type Interval = [number, number];

function mergeWithList(intervals: Interval[]): Interval[] {
  if (intervals.length === 0) return [];

  intervals.sort((a, b) => a[0] - b[0]);

  const merged: Interval[] = [];
  merged.push(intervals[0]);

  for (let i = 1; i < intervals.length; i++) {
    const last = merged[merged.length - 1];
    const current = intervals[i];

    if (current[0] <= last[1]) {
      last[1] = Math.max(last[1], current[1]);
    } else {
      merged.push(current);
    }
  }
  return merged;
}
```

#### Two-Pointer Approach or In

```typescript
function mergeWithTwoPointers(intervals: Interval[]): Interval[] {
  if (intervals.length === 0) return [];

  intervals.sort((a, b) => a[0] - b[0]);

  let write = 0; // index for placing merged intervals

  for (let read = 1; read < intervals.length; read++) {
    if (intervals[write][1] >= intervals[read][0]) {
      // Merge
      intervals[write][1] = Math.max(intervals[write][1], intervals[read][1]);
    } else {
      write++;
      intervals[write] = intervals[read];
    }
  }
  return intervals.slice(0, write + 1);
}
```

### 9. Modified Binary Search

```typescript
function search(nums: number[], target: number): number {
  let left = 0;
  let right = nums.length - 1;

  while (left <= right) {
    const mid = Math.floor((left + right) / 2);

    if (nums[mid] === target) return mid;

    // Check if left half is sorted
    if (nums[left] <= nums[mid]) {
      // Target lies within left half
      if (nums[left] <= target && target < nums[mid]) {
        right = mid - 1;
      } else {
        left = mid + 1;
      }
    } else {
      // Right half is sorted
      if (nums[mid] < target && target <= nums[right]) {
        left = mid + 1;
      } else {
        right = mid - 1;
      }
    }
  }

  return -1;
}
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

#### Row-wise Traversal

- Question: Print all elements row by row (left to right). \*

```typescript
function rowWiseTraversal(matrix: number[][]): void {
  if (matrix.length === 0) return;

  for (let i = 0; i < matrix.length; i++) {
    for (let j = 0; j < matrix[i].length; j++) {
      console.log(matrix[i][j]);
    }
  }
}
// Output: elements printed row-wise → 1, 2, 3, 4, 5, 6, 7, 8, 9
```

#### Column-wise Traversal

- Question: Print all elements column by column (top to bottom).

```typescript
function columnWiseTraversal(matrix: number[][]): void {
  if (matrix.length === 0) return;
  const rows = matrix.length;
  const cols = matrix[0].length;
  for (let j = 0; j < cols; j++) {
    for (let i = 0; i < rows; i++) {
      console.log(matrix[i][j]);
    }
  }
}

// Output: elements printed column-wise → 1, 4, 7, 2, 5, 8, 3, 6, 9
```

#### Spiral Traversal

- Question: Print elements in a spiral order(clockwise).

```typescript
function spiralTraversal(matrix: number[][]): number[] {
  const result: number[] = [];
  if (matrix.length === 0) return result;

  let top = 0;
  let bottom = matrix.length - 1;
  let left = 0;
  let right = matrix[0].length - 1;

  while (top <= bottom && left <= right) {
    // Traverse from left to right
    for (let col = left; col <= right; col++) {
      result.push(matrix[top][col]);
    }
    top++;

    // Traverse downwards
    for (let row = top; row <= bottom; row++) {
      result.push(matrix[row][right]);
    }
    right--;

    if (top <= bottom) {
      // Traverse from right to left
      for (let col = right; col >= left; col--) {
        result.push(matrix[bottom][col]);
      }
      bottom--;
    }

    if (left <= right) {
      // Traverse upwards
      for (let row = bottom; row >= top; row--) {
        result.push(matrix[row][left]);
      }
      left++;
    }
  }
  return result;
}

// Output: spiral order → 1, 2, 3, 6, 9, 8, 7, 4, 5
// const matrix2: matrix = [
// [1, 2, 3, 4],
// [5, 6, 7, 8],
// [9, 10, 11, 12],
// [13, 14, 15, 16],
// [17, 18, 19, 20],
// ];
```

#### Diagonal Traversal

- Question: Print all elements diagonally from top - left to bottom - right.

```typescript
function diagonalTraversal(matrix: number[][]): number[] {
  const rows = matrix.length;
  const cols = matrix[0].length;
  const result: number[] = [];

  for (let diag = 0; diag < rows + cols - 1; diag++) {
    let r = diag < cols ? 0 : diag - cols + 1;
    let c = diag < cols ? diag : cols - 1;
    while (r < rows && c >= 0) {
      result.push(matrix[r][c]);
      r++;
      c--;
    }
  }

  return result;
}

// Output: diagonal order → 1, 2, 4, 3, 5, 7, 6, 8, 9
```

#### Zigzag Traversal

- Question: Print elements zigzag row by row (left to right, then right to left, alternately).

```typescript
function zigzagTraversal(matrix: number[][]): void {
  for (let i = 0; i < matrix.length; i++) {
    if (i % 2 === 0) {
      // Left to right
      for (let j = 0; j < matrix[i].length; j++) {
        console.log(matrix[i][j]);
      }
    } else {
      // Right to left
      for (let j = matrix[i].length - 1; j >= 0; j--) {
        console.log(matrix[i][j]);
      }
    }
  }
}

// Output: zigzag order → 1, 2, 3, 6, 5, 4, 7, 8, 9
```

#### BFS Traversal on Matrix

- Question: Given a grid, traverse neighbors level - by - level starting from the top - left.

```typescript
function bfsMatrixTraversal(grid: number[][]): void {
  const rows = grid.length;
  const cols = grid[0].length;
  const visited = Array.from({ length: rows }, () => Array(cols).fill(false));
  const queue: [number, number][] = [];

  const directions = [
    [0, 1],
    [1, 0],
    [0, -1],
    [-1, 0],
  ]; // right, down, left, up

  queue.push([0, 0]);
  visited[0][0] = true;

  while (queue.length > 0) {
    const [r, c] = queue.shift()!;
    console.log(grid[r][c]);

    for (const [dr, dc] of directions) {
      const nr = r + dr;
      const nc = c + dc;
      if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && !visited[nr][nc]) {
        visited[nr][nc] = true;
        queue.push([nr, nc]);
      }
    }
  }
}

`
input : [
[1,2,3],
[4,5,6],
[7,8,9]
]

`;
// Output: BFS traversal → 1, 2, 4, 3, 5, 7, 6, 8, 9
```

### 14. Backtracking

Backtracking builds solutions incrementally, undoing choices that violate constraints to explore only valid paths; think “DFS on a decision tree with prune-and-undo.” It shines for subsets, combinations, permutations, N-Queens, and phone keypad problems.

### Core template

- Define choices, constraints (validity/pruning), and goal (when to record a solution). Maintain a path, choose a candidate, recurse, then undo the choice.

```typescript
// Generic backtracking template
type Path<T> = T[];

function backtrack<T>(
  state: any, // problem-specific state
  choices: () => T[], // generate next choices
  isValid: (choice: T) => boolean, // optional pruning
  apply: (choice: T) => void, // make choice (mutate state/path)
  undo: (choice: T) => void, // undo choice
  isGoal: () => boolean, // record condition
  onAnswer: () => void // push deep copy of result
): void {
  if (isGoal()) {
    onAnswer();
    return;
  }
  for (const choice of choices()) {
    if (!isValid(choice)) continue;
    apply(choice);
    backtrack(state, choices, isValid, apply, undo, isGoal, onAnswer);
    undo(choice);
  }
}
```

### Subsets (power set)

- Choice: include/exclude next element. Constraint: none. Goal: reached end.

```typescript
export function subsets(nums: number[]): number[][] {
  const res: number[][] = [];
  const path: number[] = [];

  function dfs(i: number) {
    if (i === nums.length) {
      res.push([...path]);
      return;
    }
    dfs(i + 1); // exclude
    path.push(nums[i]); // include
    dfs(i + 1);
    path.pop(); // undo
  }
  dfs(0);
  return res;
}
```

### Combinations k-of-n

- Choice: pick next index starting from start; prune if not enough elements remain.

```typescript
export function combine(n: number, k: number): number[][] {
  const res: number[][] = [];
  const path: number[] = [];

  function dfs(start: number) {
    if (path.length === k) {
      res.push([...path]);
      return;
    }
    // pruning: i <= n - (k - path.length) + 1
    for (let i = start; i <= n - (k - path.length) + 1; i++) {
      path.push(i);
      dfs(i + 1);
      path.pop();
    }
  }
  dfs(1);
  return res;
}
```

### Permutations (distinct)

- Choice: pick any unused element. Constraint: cannot reuse an element; use visited. Goal: path length equals n.

```typescript
export function permute(nums: number[]): number[][] {
  const res: number[][] = [];
  const path: number[] = [];
  const used = new Array(nums.length).fill(false);

  function dfs() {
    if (path.length === nums.length) {
      res.push([...path]);
      return;
    }
    for (let i = 0; i < nums.length; i++) {
      if (used[i]) continue;
      used[i] = true;
      path.push(nums[i]);
      dfs();
      path.pop();
      used[i] = false;
    }
  }
  dfs();
  return res;
}
```

### Combination Sum (allow reuse)

- Choice: try candidates from index onward; constraint: sum cannot exceed target; reuse by staying on i after pick.

```typescript
export function combinationSum(
  candidates: number[],
  target: number
): number[][] {
  candidates.sort((a, b) => a - b);
  const res: number[][] = [];
  const path: number[] = [];

  function dfs(start: number, remain: number) {
    if (remain === 0) {
      res.push([...path]);
      return;
    }
    for (let i = start; i < candidates.length; i++) {
      const x = candidates[i];
      if (x > remain) break; // prune by sorted order
      path.push(x);
      dfs(i, remain - x); // allow reuse: i, not i+1
      path.pop();
    }
  }
  dfs(0, target);
  return res;
}
```

### N-Queens (constraint-heavy)

- Choices: place a queen in any column per row; constraints: same column or diagonals forbidden using sets for cols and diagonals.

```typescript
export function solveNQueens(n: number): string[][] {
  const res: string[][] = [];
  const cols = new Set<number>();
  const diag1 = new Set<number>(); // r - c
  const diag2 = new Set<number>(); // r + c
  const board = Array.from({ length: n }, () => Array(n).fill("."));

  function dfs(r: number) {
    if (r === n) {
      res.push(board.map((row) => row.join("")));
      return;
    }
    for (let c = 0; c < n; c++) {
      if (cols.has(c) || diag1.has(r - c) || diag2.has(r + c)) continue;
      cols.add(c);
      diag1.add(r - c);
      diag2.add(r + c);
      board[r][c] = "Q";
      dfs(r + 1);
      board[r][c] = ".";
      cols.delete(c);
      diag1.delete(r - c);
      diag2.delete(r + c);
    }
  }
  dfs(0);
  return res;
}
```

### Pattern selection guide

- Subsets/combinations: advance index, avoid revisiting earlier indices.
- Permutations: iterate all indices with a visited array.
- Sum problems: sort, prune when remaining < 0 or candidate > remaining.
- Constraint problems: keep fast-lookup sets for invalid states to prune early.

### Complexity notes

- Backtracking explores an implicit tree; worst-case nodes are exponential, but pruning makes many interview tasks pass within constraints.

Quick dry-run permute

- Path [], choose 1 → , choose 2 → , choose 3 → record; backtrack to , try others; systematically covers all 6 permutations.

### 15. Dynamic Programming

Dynamic programming solves problems by breaking them into overlapping subproblems with optimal substructure, using either top-down memoization or bottom-up tabulation to avoid recomputation. It’s ideal for counting paths, min/max cost, sequence alignment, knapsack-like choices, and string edits.

### Template playbook

- Identify state, transition, base cases, and iteration order; choose top-down for quicker correctness or bottom-up to avoid recursion and enable space optimization.

```typescript
// Top-down (memoization) template
function dpTopDown<Key, Val>(
  key: Key,
  solve: (key: Key) => Val,
  memo: Map<Key, Val> = new Map()
): Val {
  if (memo.has(key)) return memo.get(key)!;
  const val = solve(key);
  memo.set(key, val);
  return val;
}

// Bottom-up (tabulation) skeleton
// Fill dp in an order so dependencies are already computed.
function dpBottomUp<T>(
  size: number,
  init: (i: number) => T,
  trans: (i: number) => void
): T[] {
  const dp: T[] = Array(size);
  for (let i = 0; i < size; i++) dp[i] = init(i);
  for (let i = 0; i < size; i++) trans(i);
  return dp;
}
```

### 1D DP: Climbing Stairs (Fibonacci)

- State: dp[i] = ways to reach step i, transitions dp[i] = dp[i-1] + dp[i-2], bases dp=1, dp=1. Space can be reduced to two variables.

```typescript
export function climbStairs(n: number): number {
  let a = 1,
    b = 1; // dp[0], dp[1]
  for (let i = 2; i <= n; i++) {
    const c = a + b; // dp[i] = dp[i-1] + dp[i-2]
    a = b;
    b = c;
  }
  return b;
}
```

- Dry-run: n=4 → sequence 1,1,2,3,5 → return 5.

### 2D DP: Longest Common Subsequence (LCS) with space optimization

- State: dp[i][j] = LCS length for text1[0..i-1], text2[0..j-1]; transition uses diagonal on match else max of top/left; optimize space to O(min(n,m)).

```typescript
export function lcsLength(a: string, b: string): number {
  if (a.length < b.length) [a, b] = [b, a]; // ensure b is shorter
  const m = a.length,
    n = b.length;
  let prev = new Array(n + 1).fill(0);
  let curr = new Array(n + 1).fill(0);

  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (a[i - 1] === b[j - 1]) curr[j] = prev[j - 1] + 1;
      else curr[j] = Math.max(prev[j], curr[j - 1]);
    }
    [prev, curr] = [curr, prev]; // reuse arrays
  }
  return prev[n];
}
```

- Dry-run: a="ABC", b="AC" → dp progresses to 2.

### Unbounded knapsack: Coin Change (min coins)

- State: dp[x] = min coins to make x; transition dp[x] = min(dp[x], dp[x - coin] + 1) for each coin; base dp=0; unreachable as Infinity.

```typescript
export function coinChange(coins: number[], amount: number): number {
  const dp = Array(amount + 1).fill(Infinity);
  dp[0] = 0;
  for (const c of coins) {
    for (let x = c; x <= amount; x++) {
      dp[x] = Math.min(dp[x], dp[x - c] + 1);
    }
  }
  return dp[amount] === Infinity ? -1 : dp[amount];
}
```

- Dry-run: coins , amount 6 → dp=2 via 3+3.

### 0/1 Knapsack: maximize value under capacity

- State: dp[w] = best value at capacity w; iterate items once, update backwards to avoid reuse.

```typescript
export function knapsack01(
  weights: number[],
  values: number[],
  W: number
): number {
  const dp = new Array(W + 1).fill(0);
  for (let i = 0; i < weights.length; i++) {
    const w = weights[i],
      v = values[i];
    for (let cap = W; cap >= w; cap--) {
      dp[cap] = Math.max(dp[cap], dp[cap - w] + v);
    }
  }
  return dp[W];
}
```

- Dry-run: weights , values , W=5 → dp=9 by taking both.

### Edit Distance (Levenshtein)

- State: dp[i][j] = min edits to convert a[0..i)→b[0..j); transitions: replace/insert/delete.

```typescript
export function editDistance(a: string, b: string): number {
  const m = a.length,
    n = b.length;
  const dp = Array.from({ length: m + 1 }, (_, i) => Array(n + 1).fill(0));
  for (let i = 0; i <= m; i++) dp[i][0] = i;
  for (let j = 0; j <= n; j++) dp[0][j] = j;

  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (a[i - 1] === b[j - 1]) dp[i][j] = dp[i - 1][j - 1];
      else
        dp[i][j] = Math.min(
          dp[i - 1][j] + 1, // delete
          dp[i][j - 1] + 1, // insert
          dp[i - 1][j - 1] + 1 // replace
        );
    }
  }
  return dp[m][n];
}
```

- Dry-run: a="horse", b="ros" → dp ends at 3.

### Choosing approach and optimizing space

- Prefer top-down to discover states quickly and add pruning; switch to bottom-up for iterative control and when stack depth might overflow.
- Many 2D DPs depend only on previous row/column and can be rolled to O(min(n,m)) space using two rows or a single row with careful order.

Interview checklist

- Define state in one sentence, write the recurrence, identify base cases, pick iteration order, and test on a tiny example; then consider space optimization.
- Recognize patterns: Fibonacci/house-robber (1D), knapsack/coin change (1D/2D), sequences (LCS/LIS/Edit), grids (unique paths/min path), strings (palindromes/partition).

### 16. Union Find (Disjoint Set)

- Already Done in Data Structure

### 17. Trie (Prefix Tree)

```typescript
class TrieNode {
  children: Map<string, TrieNode>;
  isEndOfWord: boolean;

  constructor() {
    this.children = new Map();
    this.isEndOfWord = false;
  }
}

class Trie {
  root: TrieNode;

  constructor() {
    this.root = new TrieNode();
  }

  // Insert a word into the trie
  insert(word: string): void {
    let node = this.root;
    for (const char of word) {
      if (!node.children.has(char)) {
        node.children.set(char, new TrieNode());
      }
      node = node.children.get(char)!;
    }
    node.isEndOfWord = true;
  }

  // Search for a full word in the trie
  search(word: string): boolean {
    let node = this.root;
    for (const char of word) {
      if (!node.children.has(char)) {
        return false;
      }
      node = node.children.get(char)!;
    }
    return node.isEndOfWord;
  }

  // Check if any word in the trie starts with the given prefix
  startsWith(prefix: string): boolean {
    let node = this.root;
    for (const char of prefix) {
      if (!node.children.has(char)) {
        return false;
      }
      node = node.children.get(char)!;
    }
    return true;
  }
}
```

```text
Dry-Run Example
Suppose we do the following:
Insert: "car", "care"
Search: "car", "cap"
StartsWith: "ca"
Step-by-step:
Insert "car" creates path c→a→r, and marks r as end-of-word.
Insert "care" follows c→a→r (already exists), then adds e—marks e as end-of-word.
Search "car": finds the path and sees r is end-of-word → returns true.
Search "cap": path exists for c→a, but not for p → returns false.
StartsWith "ca": path exists for c→a → returns true.

```

### 18. Greedy Algorithms

Greedy algorithms build a solution step by step by always making the locally optimal choice, which is provably optimal for certain structures like interval scheduling and some scheduling/covering problems. Typical patterns include sorting by an appropriate key (end time, ratio, or value), then scanning once to select or merge.

### When greedy works

- Problems with an exchange argument or matroid-like structure: interval scheduling by earliest finish, minimizing arrows to burst balloons by end coordinate, or canonical coin systems for change.

### TypeScript templates

```typescript
// 1) Interval scheduling: select max non-overlapping intervals
// Sort by earliest finish time; pick next interval whose start >= lastFinish.
export function maxNonOverlappingIntervals(
  intervals: Array<[number, number]>
): number {
  if (intervals.length === 0) return 0;
  intervals.sort((a, b) => a[1] - b[1]); // by end time
  let count = 0;
  let lastEnd = -Infinity;
  for (const [s, e] of intervals) {
    if (s >= lastEnd) {
      count++;
      lastEnd = e;
    }
  }
  return count;
}
```

```typescript
// 2) Minimum arrows to burst balloons (LC 452)
// Greedy: sort by end; shoot at current end when next start > arrowPos.
export function findMinArrowShots(points: Array<[number, number]>): number {
  if (points.length === 0) return 0;
  points.sort((a, b) => a[1] - b[1]); // by x_end
  let arrows = 0;
  let arrowPos = -Infinity;
  for (const [start, end] of points) {
    if (start > arrowPos) {
      // need a new arrow
      arrows++;
      arrowPos = end; // place at the current end
    }
  }
  return arrows;
}
```

```typescript
// 3) Merge intervals (greedy by start)
// Sort by start; extend the current interval while overlapping.
export function mergeIntervals(
  intervals: Array<[number, number]>
): Array<[number, number]> {
  if (intervals.length === 0) return [];
  intervals.sort((a, b) => a[0] - b[0]); // by start
  const res: Array<[number, number]> = [];
  let [cs, ce] = intervals[0];
  for (let i = 1; i < intervals.length; i++) {
    const [s, e] = intervals[i];
    if (s <= ce) ce = Math.max(ce, e); // overlap: extend
    else {
      res.push([cs, ce]);
      [cs, ce] = [s, e];
    }
  }
  res.push([cs, ce]);
  return res;
}
```

```typescript
// 4) Fractional knapsack (ratio sort)
// Pick items by value/weight descending until capacity is filled.
export function fractionalKnapsack(
  weights: number[],
  values: number[],
  capacity: number
): number {
  const items = weights.map((w, i) => ({ w, v: values[i], r: values[i] / w }));
  items.sort((a, b) => b.r - a.r); // highest ratio first
  let cap = capacity,
    best = 0;
  for (const it of items) {
    if (cap <= 0) break;
    const take = Math.min(cap, it.w);
    best += it.v * (take / it.w);
    cap -= take;
  }
  return best;
}
```

```typescript
// 5) Canonical coin change (greedy heuristic)
// Works optimally only for canonical coin systems (e.g., USD). Otherwise use DP.
export function greedyCoinChange(coins: number[], amount: number): number[] {
  coins.sort((a, b) => b - a); // largest first
  const res: number[] = [];
  let x = amount;
  for (const c of coins) {
    const k = Math.floor(x / c);
    if (k > 0) res.push(...Array(k).fill(c));
    x -= k * c;
  }
  return x === 0 ? res : []; // empty means not exact with greedy
}
```

### Intuition and proof sketches

- Interval scheduling: choosing the earliest finishing compatible interval leaves maximum room for the rest; an exchange argument shows any optimal solution can be transformed to this choice.
- Arrows/balloons: placing an arrow at the rightmost end of the current interval group hits as many subsequent overlapping intervals as possible.
- Fractional knapsack: with divisibility allowed, value/weight ratio sorting is optimal by a cut-and-paste argument; contrast with 0/1 variant requiring DP.

### Complexity

- Sorting dominates: O(n \log n); each greedy scan is O(n); space O(1) or O(n) for outputs.

### Dry-run (arrows)

For points [,,,] → sort by end → [,,,]; arrow at 6 bursts first two; next start 7 > 6, arrow at 12 bursts last two → answer 2.

Interview guidance

- Validate greedy with a counterexample search; if any exists, switch to DP. Common green flags: interval-like problems, exchange argument, matroid properties, or fractional choices.

### 19. Topological Sort

Topological sort orders nodes of a directed acyclic graph so every edge u→v places u before v; it’s essential for scheduling with dependencies, build systems, and course prerequisites. Two standard approaches are Kahn’s algorithm (BFS on indegrees) and DFS postorder; both run in O(V+E).

### Kahn’s algorithm (BFS)

- Compute indegree of each node, queue all with 0 indegree, pop and append to order, decrement neighbors’ indegrees, enqueue new zeros; if not all nodes processed, a cycle exists.

```typescript
// Graph as adjacency list: 0..n-1 with edges u -> v
export function topoSortKahn(
  n: number,
  edges: Array<[number, number]>
): number[] {
  const adj: number[][] = Array.from({ length: n }, () => []);
  const indeg = new Array(n).fill(0);

  for (const [u, v] of edges) {
    adj[u].push(v);
    indeg[v]++;
  }

  const q: number[] = [];
  for (let i = 0; i < n; i++) if (indeg[i] === 0) q.push(i);

  const order: number[] = [];
  let qi = 0; // pointer for queue
  while (qi < q.length) {
    const u = q[qi++];
    order.push(u);
    for (const v of adj[u]) {
      if (--indeg[v] === 0) q.push(v);
    }
  }

  if (order.length !== n) return []; // cycle detected, no topo order
  return order;
}
```

- Dry-run: edges 2→3,3→1,4→0,4→1,5→0,5→2 → output like depending on zero-indegree tie order.

### DFS postorder approach

- DFS from unvisited nodes, push node to stack after exploring neighbors; reversing postorder yields a valid topological order; detect cycles using a recursion stack.

```typescript
export function topoSortDFS(
  n: number,
  edges: Array<[number, number]>
): number[] {
  const adj: number[][] = Array.from({ length: n }, () => []);
  for (const [u, v] of edges) adj[u].push(v);

  const vis = new Array(n).fill(0); // 0=unvisited,1=visiting,2=done
  const stack: number[] = [];
  let hasCycle = false;

  function dfs(u: number): void {
    if (hasCycle) return;
    vis[u] = 1;
    for (const v of adj[u]) {
      if (vis[v] === 0) dfs(v);
      else if (vis[v] === 1) {
        hasCycle = true;
        return;
      } // back edge
    }
    vis[u] = 2;
    stack.push(u); // postorder
  }

  for (let i = 0; i < n; i++) if (vis[i] === 0) dfs(i);
  if (hasCycle) return [];
  stack.reverse();
  return stack;
}
```

### When to use which

- Kahn’s is intuitive for dependency resolution and explicit cycle detection by count; DFS is handy when recursion suits and postorder is natural. Both are correct for DAGs.

### Course schedule pattern

- Build directed graph from prerequisite pairs, run topological sort; any cycle means it’s impossible to finish all courses, otherwise the order is the answer.

Complexity and tips

- Time O(V+E), space O(V+E); use arrays for graphs indexed 0..n-1, Maps for sparse labeled graphs; for deterministic outputs, use stable ordering when enqueuing or sorting neighbors.

### 20. Bit Manipulation

Bit manipulation uses constant-time bitwise ops to check, set, clear, toggle, and aggregate flags, enabling elegant O(1) tricks for parity, XOR-unique elements, counting bits, and subset iteration. It’s common in interviews for Single Number, subsets via bitmasks, and optimized counters

### Core helpers

```typescript
// Get, set, clear, toggle the i-th bit (0-indexed)
export const getBit = (x: number, i: number) => (x >>> i) & 1; // unsigned shift
export const setBit = (x: number, i: number) => x | (1 << i);
export const clearBit = (x: number, i: number) => x & ~(1 << i);
export const toggleBit = (x: number, i: number) => x ^ (1 << i);

// Check power of two: exactly one bit set and x > 0
export const isPowerOfTwo = (x: number) => x > 0 && (x & (x - 1)) === 0;

// Isolate rightmost set bit
export const lowbit = (x: number) => x & -x;
```

### Counting set bits (Brian Kernighan)

```typescript
export function popcount(x: number): number {
  let cnt = 0;
  while (x !== 0) {
    x &= x - 1;
    cnt++;
  } // clears lowest set bit each loop
  return cnt;
}
```

- Runs in O(k) where k is number of 1-bits, faster than checking all 32 bits

### XOR patterns

```typescript
// Single Number: every element appears twice except one
export function singleNumber(nums: number[]): number {
  let ans = 0;
  for (const v of nums) ans ^= v;
  return ans;
}

// Find missing number in [0..n] given n elements
export function missingNumber(nums: number[]): number {
  let ans = nums.length;
  for (let i = 0; i < nums.length; i++) ans ^= i ^ nums[i];
  return ans;
}
```

- Uses XOR properties: a^a=0, a^0=a, commutative/associative; cancels pairs, leaving the unique value

### Bitmask subsets

```typescript
// Generate all subsets (power set) using bit masks
export function subsetsBitmask<T>(arr: T[]): T[][] {
  const n = arr.length,
    total = 1 << n;
  const res: T[][] = [];
  for (let mask = 0; mask < total; mask++) {
    const cur: T[] = [];
    for (let i = 0; i < n; i++) if (mask & (1 << i)) cur.push(arr[i]);
    res.push(cur);
  }
  return res;
}

// Iterate only submasks of a given mask (useful in DP over subsets)
export function iterateSubmasks(mask: number, fn: (sub: number) => void): void {
  let sub = mask;
  while (sub) {
    fn(sub);
    sub = (sub - 1) & mask;
  }
  fn(0); // include empty submask
}
```

- Power set loops masks 0..2^n-1; submask iteration uses the identity sub = (sub-1) & mask to visit all subsets efficiently

### Common interview tricks

```typescript
// Swap without temp using XOR (works for distinct references)
export function xorSwap(a: number, b: number): [number, number] {
  a ^= b;
  b ^= a;
  a ^= b;
  return [a, b];
}

// Reverse bits of a 32-bit number
export function reverseBits(x: number): number {
  let y = 0;
  for (let i = 0; i < 32; i++) {
    y = (y << 1) | (x & 1);
    x >>>= 1;
  }
  return y >>> 0; // keep unsigned
}

// Compute XOR of [1..n] in O(1) using pattern of n%4
export function xorOneToN(n: number): number {
  switch (
    n & 3 // n % 4
  ) {
    case 0:
      return n;
    case 1:
      return 1;
    case 2:
      return n + 1;
    default:
      return 0; // case 3
  }
}
```

- XOR swap illustrates toggling with ^; reverseBits shifts/accumulates; 1^2^...^n cycles every 4 values by parity of set bits

### Dry-runs

- popcount(13): 1101 → clear lowbits 1101→1100→1000→0000 → count 3
- singleNumber(): ((((0^2)^2)^1)^4)^4 = 1
- subsetsBitmask([a,b]): masks 00→[], 01→[a], 10→[b], 11→[a,b]

Interview guidance

- Prefer unsigned right shift (>>> in TS) to avoid sign bit issues for bit-level iteration.
- For flags, pack booleans into a number; test with getBit and mutate with set/clear/toggle
- Know when XOR tricks are valid and when to use DP or hashing instead; bitmasks shine for n ≤ 20–25 in subset DP.

Sliding Window Maximum uses a monotonic deque that stores indices of elements in decreasing value order so the front is always the current window’s maximum in O(1); as the window moves, drop out-of-window indices and pop smaller values from the back to maintain the invariant. This achieves O(n) time and O(k) space for window size k.

### TypeScript template (monotonic deque)

```typescript
// Returns the maximum in each window of size k
export function maxSlidingWindow(nums: number[], k: number): number[] {
  if (k <= 0 || nums.length === 0) return [];
  const n = nums.length;
  if (k === 1) return nums.slice();

  const dq: number[] = []; // stores indices, nums[dq[0]] >= nums[dq[1]] >= ...
  const res: number[] = [];

  for (let i = 0; i < n; i++) {
    // 1) Remove indices out of the window (left bound is i - k + 1)
    if (dq.length && dq[0] < i - k + 1) dq.shift();

    // 2) Maintain decreasing deque by value
    while (dq.length && nums[dq[dq.length - 1]] <= nums[i]) dq.pop();

    // 3) Push current index
    dq.push(i);

    // 4) Record answer once first window is formed
    if (i >= k - 1) res.push(nums[dq[0]]);
  }
  return res;
}
```

### Intuition and invariants

- The deque holds only indices that can still be maximum for some future window; any smaller-or-equal elements behind a larger new element can never become max later and are removed
- The head is always within the current window and is the maximum; if it falls out, pop from the front.

### Complexity

- Each index is pushed and popped at most once → O(n) time; deque holds at most k indices → O(k) space

### Dry-run

For nums = [1,3,-1,-3,5,3,6,7], k = 3:

- Windows: [1,3,-1]→3, [3,-1,-3]→3, [-1,-3,5]→5, [-3,5,3]→5, →6, →7; output.

Interview tips

- Store indices, not values, to efficiently evict out-of-window elements.
- Prefer deque over heap for O(n) vs O(n log k) and explain the trade-off if asked.
- Handle edge cases: k=1 returns a copy, k>n returns [], empty input returns [].

### 22. Segment Tree & Fenwick Tree (BIT)

Segment Tree and Fenwick Tree both support fast range queries with updates; use Fenwick Tree for prefix sums and point updates with a compact, simple structure, and Segment Tree for flexible operations (min/max/sum) and lazy propagation for range updates. Both achieve O(log n) per update/query.

### When to choose which

- Fenwick Tree: prefix sums, point updates, sometimes range updates via tricks; simpler and smaller memory.
- Segment Tree: supports arbitrary associative ops, range queries, range updates, and lazy propagation patterns.

### Fenwick Tree (BIT) — point update, prefix/range sum

```typescript
// 1-indexed Fenwick Tree for prefix sums
export class Fenwick {
  private bit: number[];
  private n: number;

  constructor(n: number) {
    this.n = n;
    this.bit = new Array(n + 1).fill(0);
  }

  // add delta at index i (1-based)
  add(i: number, delta: number): void {
    for (; i <= this.n; i += i & -i) this.bit[i] += delta;
  }

  // prefix sum [1..i]
  sum(i: number): number {
    let res = 0;
    for (; i > 0; i -= i & -i) res += this.bit[i];
    return res;
  }

  // range sum [l..r]
  rangeSum(l: number, r: number): number {
    if (l > r) return 0;
    return this.sum(r) - this.sum(l - 1);
  }

  // build from 0-based array in O(n)
  static fromArray(arr: number[]): Fenwick {
    const ft = new Fenwick(arr.length);
    for (let i = 0; i < arr.length; i++) ft.bit[i + 1] = arr[i];
    for (let i = 1; i <= arr.length; i++) {
      const j = i + (i & -i);
      if (j <= arr.length) ft.bit[j] += ft.bit[i];
    }
    return ft;
  }
}
```

Range updates with BIT

- Use two BITs to support add val to [l,r] and query point/prefix; or transform with difference arrays for range sum queries.

```typescript
// Range add [l..r] and point query using one BIT on difference array
export class FenwickRangeAddPointQuery {
  private ft: Fenwick;
  constructor(n: number) {
    this.ft = new Fenwick(n);
  }
  addRange(l: number, r: number, val: number): void {
    this.ft.add(l, val);
    this.ft.add(r + 1, -val);
  }
  pointQuery(i: number): number {
    return this.ft.sum(i);
  }
}
```

### Segment Tree — range query, point update

```typescript
// Segment Tree for range sum, point update
export class SegmentTree {
  private n: number;
  private tree: number[];

  constructor(arr: number[]) {
    this.n = arr.length;
    this.tree = new Array(4 * this.n).fill(0);
    this.build(arr, 1, 0, this.n - 1);
  }

  private build(arr: number[], idx: number, l: number, r: number): void {
    if (l === r) {
      this.tree[idx] = arr[l];
      return;
    }
    const m = (l + r) >> 1;
    this.build(arr, idx << 1, l, m);
    this.build(arr, (idx << 1) | 1, m + 1, r);
    this.tree[idx] = this.tree[idx << 1] + this.tree[(idx << 1) | 1];
  }

  // query sum on [ql, qr]
  query(ql: number, qr: number): number {
    return this._query(1, 0, this.n - 1, ql, qr);
  }
  private _query(
    idx: number,
    l: number,
    r: number,
    ql: number,
    qr: number
  ): number {
    if (qr < l || r < ql) return 0;
    if (ql <= l && r <= qr) return this.tree[idx];
    const m = (l + r) >> 1;
    return (
      this._query(idx << 1, l, m, ql, qr) +
      this._query((idx << 1) | 1, m + 1, r, ql, qr)
    );
  }

  // point update: set arr[pos] to val
  update(pos: number, val: number): void {
    this._update(1, 0, this.n - 1, pos, val);
  }
  private _update(
    idx: number,
    l: number,
    r: number,
    pos: number,
    val: number
  ): void {
    if (l === r) {
      this.tree[idx] = val;
      return;
    }
    const m = (l + r) >> 1;
    if (pos <= m) this._update(idx << 1, l, m, pos, val);
    else this._update((idx << 1) | 1, m + 1, r, pos, val);
    this.tree[idx] = this.tree[idx << 1] + this.tree[(idx << 1) | 1];
  }
}
```

### Segment Tree with Lazy Propagation — range add, range sum

```typescript
export class LazySegTree {
  private n: number;
  private tree: number[];
  private lazy: number[];

  constructor(arr: number[]) {
    this.n = arr.length;
    this.tree = new Array(4 * this.n).fill(0);
    this.lazy = new Array(4 * this.n).fill(0);
    this.build(arr, 1, 0, this.n - 1);
  }

  private build(arr: number[], idx: number, l: number, r: number): void {
    if (l === r) {
      this.tree[idx] = arr[l];
      return;
    }
    const m = (l + r) >> 1;
    this.build(arr, idx << 1, l, m);
    this.build(arr, (idx << 1) | 1, m + 1, r);
    this.tree[idx] = this.tree[idx << 1] + this.tree[(idx << 1) | 1];
  }

  private push(idx: number, l: number, r: number): void {
    if (this.lazy[idx] !== 0 && l !== r) {
      const m = (l + r) >> 1;
      const v = this.lazy[idx];
      // apply to children
      this.lazy[idx << 1] += v;
      this.lazy[(idx << 1) | 1] += v;
      this.tree[idx << 1] += v * (m - l + 1);
      this.tree[(idx << 1) | 1] += v * (r - m);
      this.lazy[idx] = 0;
    } else if (l === r) {
      this.lazy[idx] = 0;
    }
  }

  // add val to [ql, qr]
  updateRange(ql: number, qr: number, val: number): void {
    this._updateRange(1, 0, this.n - 1, ql, qr, val);
  }
  private _updateRange(
    idx: number,
    l: number,
    r: number,
    ql: number,
    qr: number,
    val: number
  ): void {
    if (qr < l || r < ql) return;
    if (ql <= l && r <= qr) {
      this.tree[idx] += val * (r - l + 1);
      this.lazy[idx] += val;
      return;
    }
    this.push(idx, l, r);
    const m = (l + r) >> 1;
    this._updateRange(idx << 1, l, m, ql, qr, val);
    this._updateRange((idx << 1) | 1, m + 1, r, ql, qr, val);
    this.tree[idx] = this.tree[idx << 1] + this.tree[(idx << 1) | 1];
  }

  // query sum on [ql, qr]
  query(ql: number, qr: number): number {
    return this._query(1, 0, this.n - 1, ql, qr);
  }
  private _query(
    idx: number,
    l: number,
    r: number,
    ql: number,
    qr: number
  ): number {
    if (qr < l || r < ql) return 0;
    if (ql <= l && r <= qr) return this.tree[idx];
    this.push(idx, l, r);
    const m = (l + r) >> 1;
    return (
      this._query(idx << 1, l, m, ql, qr) +
      this._query((idx << 1) | 1, m + 1, r, ql, qr)
    );
  }
}
```

### Intuition and use-cases

- Fenwick uses binary lifting with lowbit x \& -x to jump across ranges representing aggregated prefix chunks; great for live counters, inversion counts, and frequency tables.
- Segment Trees store aggregates per interval; lazy tags defer pushing updates to children, turning range updates and queries both into O(\log n).

### Complexity

- Build: Fenwick O(n), Segment Tree O(n). Point update/range sum: both O(\log n). Range update/range query: Segment Tree with lazy O(\log n); BIT requires two BITs or difference tricks.

Dry-run idea

- For Fenwick.fromArray(), sum(3)=1+2+3=6; add(2, +5) increases positions 2,4,8... Then rangeSum(2,4)=2+5+3+4=14.
- For LazySegTree, after updateRange(1,3,+2) on , query(0,3)=1+(2+2)+(3+2)+(4+2)=16; push happens only when needed
