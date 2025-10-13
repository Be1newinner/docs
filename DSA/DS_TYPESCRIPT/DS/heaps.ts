import { IHeap } from "./interfaces";


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
        if (index < 0 || index >= this.size()) throw new Error("Index out of range");
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
        if (index < 0 || index >= this.size()) throw new Error("Index out of range");
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
        let index = startIndex ?? (this.size() - 1);
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

            if (leftChildIndex < length && this.heap[leftChildIndex] < this.heap[smallest]) {
                smallest = leftChildIndex;
            }
            if (rightChildIndex < length && this.heap[rightChildIndex] < this.heap[smallest]) {
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



class MinHeap2 implements IHeap<number> {
    private heap: number[];

    constructor() {
        this.heap = []
    }

    size(): number {
        return this.heap.length;
    };

    // Return top element without removal
    peek(): number | null {
        if (this.size() === 0) return null;
        return this.heap[0];
    };

    // Insert new element into heap
    insert(val: number): void {
        this.heap.push(val);
        const idx = this.heap.length - 1;
        this.heapifyUp(idx);
    };

    // Remove and return top element
    extractTop(): number | null {
        if (this.heap.length === 0) return null;
        if (this.heap.length === 1) return this.heap.pop()!;

        const item = this.heap[0];
        this.heap[0] = this.heap.pop()!;
        this.heapifyDown(0);
        return item;
    };

    // Build heap from unsorted array
    buildHeap(arr: number[]): void {
        for (const item of arr) {
            this.insert(item);
        }
    };

    // Update element at given index with new value
    updateKey(index: number, newVal: number): void {

    };

    // Remove element at specific index
    remove(index: number): void { };

    // Heap sort: Returns sorted array from heap elements
    heapSort(): number[] {

        return [];
    };

    // Optional for generic heaps: comparator function for custom order
    comparator(a: number, b: number): number {


        return 0;
    };

    // check the node to be inserted with its parent!
    private heapifyUp(idx: number): void {
        while (idx > 0) {
            const parentIdx = Math.floor((idx - 1) / 2);
            if (this.heap[idx] >= this.heap[parentIdx]) break;
            [this.heap[idx], this.heap[parentIdx]] = [this.heap[parentIdx], this.heap[idx]];
            idx = parentIdx;
        }
    }

    private heapifyDown(idx: number): void {
        const length = this.heap.length;

        while (true) {
            const leftChildIdx = 2 * idx + 1;
            const rightChildIdx = 2 * idx + 2;
            let smallest = idx;

            if (leftChildIdx < length && this.heap[smallest] > this.heap[leftChildIdx]) {
                smallest = leftChildIdx;
            }

            if (rightChildIdx < length && this.heap[smallest] > this.heap[rightChildIdx]) {
                smallest = rightChildIdx;
            }

            if (idx === smallest) {
                break;
            }

            [this.heap[idx], this.heap[smallest]] = [this.heap[smallest], this.heap[idx]];
            idx = smallest;
        }
    }
}