/*
 * @lc app=leetcode id=56 lang=typescript
 *
 * [56] Merge Intervals
 */

// @lc code=start
function merge(intervals: number[][]): number[][] {
    const merged: number[][] = [];
    intervals.sort((a, b) => a[0] - b[0]);

    if (intervals.length === 0) return []
    merged.push(intervals[0])

    for (let i = 1; i < intervals.length; i++) {
        const last = merged[merged.length - 1];
        const current = intervals[i];
        if (current[0] < last[1]) {
            merged[merged.length - 1][1] = Math.max(current[1], last[1]);
        } else {
            merged.push(intervals[i])
        }
    }

    return merged;
};
// @lc code=end

