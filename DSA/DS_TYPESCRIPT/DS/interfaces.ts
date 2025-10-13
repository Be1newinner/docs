// Stack interface (LIFO)
export interface StackInterface<T> {
    push(item: T): void;    // push an item, no return value
    pop(): T | undefined;   // pop and return top item, or undefined if empty
    peek(): T | undefined;  // return top item without removing
    isEmpty(): boolean;     // check if stack is empty
    size(): number;         // get number of items
}


// Queue interface (FIFO)
export interface QueueInterface<T> {
    enqueue(item: T): void;          // Add to the back
    dequeue(): T | undefined;        // Remove from the front
    peek(): T | undefined;           // Get front element without removing
    isEmpty(): boolean;              // Check if empty
    size(): number;                  // Number of items
}

// Deque interface (double-ended queue)
export interface DequeInterface<T> {
    addFront(item: T): void;         // Add to front
    addBack(item: T): void;          // Add to back
    removeFront(): T | undefined;    // Remove from front
    removeBack(): T | undefined;     // Remove from back
    peekFront(): T | undefined;      // Look at front
    peekBack(): T | undefined;       // Look at back
    isEmpty(): boolean;              // Check if empty
    size(): number;                  // Number of items
}

export interface PriorityQueueInterface<T> {
    enqueue(item: T, priority: number): void;
    dequeue(): T | undefined;
    peek(): T | undefined;
    isEmpty(): boolean;
    size(): number;
}


export interface ListNodeInterface<T> {
    val: T;
    next: ListNodeInterface<T> | null;
}

export interface LinkedListInterface<T> {
    append(item: T): void;
    prepend(item: T): void;
    delete(item: T): void;
    find(item: T): ListNodeInterface<T> | null;
    isEmpty(): boolean;
    size(): number;
}

export interface DoublyListNodeInterface<T> {
    val: T;
    next: DoublyListNodeInterface<T> | null;
    prev: DoublyListNodeInterface<T> | null;
}


export interface DoublyLinkedListInterface<T> {
    append(item: T): void;
    prepend(item: T): void;
    delete(item: T): void;
    deleteFront(): T | null;
    deleteBack(): T | null;
    find(item: T): DoublyListNodeInterface<T> | null;
    isEmpty(): boolean;
    size(): number;
    clear(): void;
    toArray(): T[];
}


export interface HashMapInterface<K, V> {
    set(key: K, value: V): void;
    get(key: K): V | undefined;
    has(key: K): boolean;
    delete(key: K): boolean;
    size(): number;
    clear(): void;
}


export interface SetDSInterface<T> {
    add(item: T): void;
    has(item: T): boolean;
    delete(item: T): boolean;
    clear(): void;
    size(): number;
    isEmpty(): boolean;
}


export interface BSTNodeInterface {
    val: number;
    left: BSTNodeInterface | null;
    right: BSTNodeInterface | null;
}


export interface BSTInterface {
    root: BSTNodeInterface | null;
    insert(val: number): void;
    delete(val: number): void;
    search(val: number): boolean;
    findMin(node: BSTNodeInterface): BSTNodeInterface | null;
    findMax(node: BSTNodeInterface): BSTNodeInterface | null;
    isEmpty(): boolean;
}

export interface GraphInterface<T> {
    addVertex(vertex: T): void;
    addEdge(vertex1: T, vertex2: T): void;
    removeVertex(vertex: T): void;
    removeEdge(vertex1: T, vertex2: T): void;
    getNeighbors(vertex: T): T[];
    hasVertex(vertex: T): boolean;
    hasEdge(vertex1: T, vertex2: T): boolean;
    vertices(): T[];
    edges(): Array<[T, T]>;
}

export interface IHeap<T> {
    size(): number;

    // Return top element without removal
    peek(): T | null;

    // Insert new element into heap
    insert(val: T): void;

    // Remove and return top element
    extractTop(): T | null;

    // Build heap from unsorted array
    buildHeap(arr: T[]): void;

    // Update element at given index with new value
    updateKey(index: number, newVal: T): void;

    // Remove element at specific index
    remove(index: number): void;

    // Heap sort: Returns sorted array from heap elements
    heapSort(): T[];

    // Optional for generic heaps: comparator function for custom order
    comparator?: (a: T, b: T) => number;
}
