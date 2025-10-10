// Simple Problem: Merge Meeting Times
// Problem:
// You have a list of meeting time intervals represented as pairs [start, end]. Some meetings may overlap. Your task is to merge all overlapping meetings and return a list of merged meeting intervals.

// Example:
// Input: [[1][4], [2][5], [7][9]]
// Output: [[1][5], [7][9]]
// Explanation: The first two meetings overlap and merge into [1][5]. The third meeting does not overlap.

// Why This is a Good Practice for the Pattern
// Sort intervals by start time.

// Merge overlapping intervals in a single pass.

// 1. Iterative Merging with a Stack or List

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

// 2. Two-Pointer Approach or In 
// Place Approach
// Here, we use two pointers: one for reading intervals, one for writing merged intervals to the same array (a variation akin to in-place).

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

`
Approach                   |  Time Complexity                  |  Space Complexity            |  Notes                                                
---------------------------+-----------------------------------------------------------------------+---------------------------------------------
I_M) Iterative Merging List     |  O(nlogn) (sort) + O(n) (merge)   |  O(n) (merged list)          |  Simple and easy to implement                         
Two-Pointer                |  O(nlogn) + O(n)                  |  O(1) to O(n) (reusing input)|  Uses pointers to do partial in-place merging         
Priority Queue (Min-Heap)  |  O(nlogn) + O(nlogn) (heap ops)   |  O(n)                        |  More suited for scheduling problems, overhead of heap
In-place Modification      |  O(nlogn) + O(n)                  |  O(1)                        |  Very space efficient but modifies input              
`
