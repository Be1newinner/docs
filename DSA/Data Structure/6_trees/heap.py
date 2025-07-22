from typing import List

# ✅ What is a Heap?
# A Heap is a specialized binary tree-based data structure that satisfies the Heap Property:

# Min-Heap: Every parent node is less than or equal to its children.

# Max-Heap: Every parent node is greater than or equal to its children.

# 🔧 Properties:
# It's a complete binary tree (every level filled except maybe the last).

# It's usually implemented using an array, not TreeNode objects.

# ✅ Why Use Heaps?
# Efficient for priority queues.

# Common in greedy algorithms.

# Optimal for Top K problems, Median finding, Dijkstra's algorithm, and Heap Sort.

# 🛠️ Core Operations in Min/Max Heap
# Operation	                    Time Complexity
# insert -------------------------- O(log n)
# get_min/max --------------------- O(1)
# remove_min/max (extract) -------- O(log n)
# heapify ------------------------- O(n)


class MinHeap:
    def __init__(self):
        self.heap: List[int] = []

    def parent(self, index: int):
        if index < 3:
            return 0
        return (index - 1) // 2

    def leftChild(self, index: int):
        return 2 * index + 1

    def rightChild(self, index: int):
        return 2 * index + 2

    def insert(self, key: int):
        self.heap.append(key)
        new_child_index = len(self.heap) - 1

        while new_child_index > 0:
            parent_index = self.parent(new_child_index)

            if self.heap[parent_index] > self.heap[new_child_index]:
                self.heap[parent_index], self.heap[new_child_index] = (
                    self.heap[new_child_index],
                    self.heap[parent_index],
                )
                new_child_index = parent_index
            else:
                break

    def extract_min(self):
            if not self.heap:
                return None
            if len(self.heap) == 1:
                return self.heap.pop()

            min_val = self.heap[0]
            # Move last element to root and remove last
            self.heap[0] = self.heap.pop()

            index = 0
            size = len(self.heap)

            # Bubble down manually
            while True:
                left = self.leftChild(index)
                right = self.rightChild(index)
                smallest = index

                if left < size and self.heap[left] < self.heap[smallest]:
                    smallest = left
                if right < size and self.heap[right] < self.heap[smallest]:
                    smallest = right

                if smallest != index:
                    self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                    index = smallest
                else:
                    break

            return min_val
        

h = MinHeap()
for x in [10, 4, 20, 0, 2]:
    h.insert(x)
print(h.heap)

print(h.extract_min())

print(h.heap)
