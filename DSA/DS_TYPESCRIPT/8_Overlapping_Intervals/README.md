# Overlapping Intervals Pattern Explained

## What is it?

This pattern helps solve problems involving **intervals** — ranges with a start and an end, like time slots or numeric ranges.

## Key Insight:

First, **sort all intervals by their start time**. Once sorted, overlapping intervals will be adjacent or close, making them easier to spot and merge.

## How does it work?

- Start with the first interval after sorting.
- Compare it to the next interval:
  - **If the next interval's start is less than or equal to the current interval’s end:**
    - These intervals overlap.
    - Merge them by updating the current interval’s end to the maximum of both ends.
  - **Otherwise:**
    - There is no overlap.
    - Add the current interval to your merged list and move to the next.

## Why sort first?

Sorting brings intervals in order, allowing a simple linear scan to find overlaps without repeatedly checking all intervals against each other.

## Real-World Analogy:

Imagine scheduling meetings:

- If one meeting starts before another ends, you need to merge them because they conflict.
- If it starts after the last one ends, it's a separate meeting block.

## Why is it useful?

- Merging intervals reduces complex overlapping data into clear, non-overlapping segments.
- Applications: calendar booking, finding free time slots, CPU scheduling, range compression in data.

## Ways to Implement Overlapping Intervals Solutions

### 1. Iterative Merging with a Stack or List

- Sort intervals by start time.
- Use a stack or list to keep merged intervals.
- For each interval:
  - If it overlaps with the last merged, update the end.
  - Else, append it as a new separate interval.

This approach is straightforward and efficient with $$O(n \log n)$$ due to sorting and $$O(n)$$ for merging.

### 2. Two-Pointer Approach

- Sort intervals by start time.
- Use two pointers or indices:
  - One to track the current interval being merged,
  - One to scan next intervals.
- Similar logic: merge if overlapping else move pointer.

This is a variant of the iterative list approach but emphasized from a two-pointer angle, helping in certain variations of interval problems.

### 3. Priority Queue (Min-Heap)

- For some variants (like merging meeting rooms), build a min-heap of interval end times.
- Sort by start time.
- For each interval:
  - Compare with earliest finishing interval in the min-heap.
  - Decide to merge or add a new interval.

This shines in problems like scheduling minimal rooms, where tracking minimum end times is key.

### 4. In-place Modification (if allowed)

- Sort the intervals.
- Use the same interval array to update merged intervals,
- Keep a write index for merged intervals,
- Overwrite intervals that got merged.

This saves space but requires mutability and careful index handling.

---

## Example: Iterative Merge in Typescript

```typescript
type Interval = [number, number];

function mergeIntervals(intervals: Interval[]): Interval[] {
  if (intervals.length === 0) return [];

  // Step 1: Sort intervals by start time
  intervals.sort((a, b) => a[0] - b[0]);

  const merged: Interval[] = [];
  merged.push(intervals[0]);

  for (let i = 1; i < intervals.length; i++) {
    const last = merged[merged.length - 1];
    const current = intervals[i];

    if (current[0] <= last[1]) {
      // Overlaps
      last[1] = Math.max(last[1], current[1]); // Merge
    } else {
      merged.push(current); // No overlap, push new interval
    }
  }

  return merged;
}
```

### Dry-Run on Example

Input: [, , , ]

- After sort: same order here.
- Start with
- overlaps with , merge →
- no overlap → add new
- no overlap → add new
- Result: [, , ]

---

## Summary of Methods with Use Cases

| Method                   | Use Case                       | Space Complexity | Time Complexity                 |
| ------------------------ | ------------------------------ | ---------------- | ------------------------------- |
| Iterative List (default) | Most merging interval problems | O(n)             | O(n log n) sorting              |
| Two-Pointer              | When simplifying scan & merge  | O(n)             | O(n log n) sorting              |
| Min-Heap (PriorityQueue) | Room scheduling, min resources | O(n)             | O(n log n) sorting and heap ops |
| In-place Modification    | Space optimized, mutable input | O(1)             | O(n log n) sorting              |
