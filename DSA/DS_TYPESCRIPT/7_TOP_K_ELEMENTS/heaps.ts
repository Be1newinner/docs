`
Questions:

LEVEL: EASY

### Easy Question 1: "Top K Frequent Elements"

**Question:** Given an integer array 'nums' and an integer 'k', return the 'k' most frequent elements.

**Example:**

Input: nums = [1,1,1,2,2,3], k = 2
Output: [1,2]
`

class MinHeap {
    heap: [number, number][] = [];

    private swap(i: number, j: number) {
        [this.heap[i], this.heap[j]] = [this.heap[j], this.heap[i]];
    }

    private bubbleUp(index: number) {
        while (index > 0) {
            let parentIndex = Math.floor((index - 1) / 2);
            if (this.heap[parentIndex][0] <= this.heap[index][0]) break;
            this.swap(parentIndex, index);
            index = parentIndex;
        }
    }

    private bubbleDown(index: number) {
        let lastIndex = this.heap.length - 1;
        while (true) {
            let left = 2 * index + 1;
            let right = 2 * index + 2;
            let smallest = index;

            if (left <= lastIndex && this.heap[left][0] < this.heap[smallest][0]) {
                smallest = left;
            }
            if (right <= lastIndex && this.heap[right][0] < this.heap[smallest][0]) {
                smallest = right;
            }
            if (smallest === index) break;
            this.swap(index, smallest);
            index = smallest;
        }
    }

    insert(value: [number, number]) {
        this.heap.push(value);
        this.bubbleUp(this.heap.length - 1);
    }

    extractMin(): [number, number] | null {
        if (this.heap.length === 0) return null;
        const min = this.heap[0];
        const end = this.heap.pop()!;
        if (this.heap.length > 0) {
            this.heap[0] = end;
            this.bubbleDown(0);
        }
        return min;
    }

    size(): number {
        return this.heap.length;
    }

    peek(): [number, number] | null {
        return this.heap.length > 0 ? this.heap[0] : null;
    }
}

function topKFrequent(nums: number[], k: number): number[] {
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


`
Solution using Sorting Approach
Idea:

Count frequencies using a hash map.
Convert frequency map entries to an array.
Sort the array by frequency in descending order.

Return the top K elements.

Trade-off:
This approach takes 
O(N log N )
O(NlogN) time due to sorting, where N is the number of unique elements. It's straightforward and easy to implement.
`

function topKFrequentSort(nums: number[], k: number): number[] {
    const freqMap: Map<number, number> = new Map();

    // Count frequencies
    for (const num of nums) {
        freqMap.set(num, (freqMap.get(num) || 0) + 1);
    }

    // Convert map to array and sort by frequency descending
    const freqArray = Array.from(freqMap.entries());
    freqArray.sort((a, b) => b[1] - a[1]);

    // Extract top K elements
    return freqArray.slice(0, k).map(([num, freq]) => num);
}

`
2. Quickselect Approach

Idea:
Count frequencies as above.
Use quickselect (a selection algorithm related to quicksort) to partition array by frequencies such that the top K frequent elements are on one side.

This runs on average in  O ( N ) time which is faster than sorting on larger inputs.
`

function topKFrequentQuickselect(nums: number[], k: number): number[] {
    const freqMap: Map<number, number> = new Map();
    for (const num of nums) {
        freqMap.set(num, (freqMap.get(num) || 0) + 1);
    }

    const freqArray = Array.from(freqMap.entries());

    // Quickselect helper functions:
    function swap(i: number, j: number) {
        [freqArray[i], freqArray[j]] = [freqArray[j], freqArray[i]];
    }

    function partition(left: number, right: number, pivotIndex: number): number {
        const pivotFreq = freqArray[pivotIndex][1];
        swap(pivotIndex, right);
        let storeIndex = left;
        for (let i = left; i < right; i++) {
            if (freqArray[i][1] > pivotFreq) {
                swap(storeIndex, i);
                storeIndex++;
            }
        }
        swap(storeIndex, right);
        return storeIndex;
    }

    function quickselect(left: number, right: number, kSmallest: number) {
        if (left === right) return;
        let pivotIndex = Math.floor(Math.random() * (right - left + 1)) + left;
        pivotIndex = partition(left, right, pivotIndex);

        if (kSmallest === pivotIndex) {
            return;
        } else if (kSmallest < pivotIndex) {
            quickselect(left, pivotIndex - 1, kSmallest);
        } else {
            quickselect(pivotIndex + 1, right, kSmallest);
        }
    }

    quickselect(0, freqArray.length - 1, k - 1);

    return freqArray.slice(0, k).map(([num, freq]) => num);
}


`
Method       |  Time Complexity |  Space Complexity |  Use Case                                   
-------------+--------------------------------+--------------------+---------------------------------------------
Min-Heap     |  O(Nlogk)        |       O(N)        |  Efficient for large streams or N≫k
Sorting      |  O(NlogN)        |       O(N)        |  Simple implementation for moderate size    
Quickselect  |  O(N)Average     |       O(N)        |  Optimized for large datasets               

`