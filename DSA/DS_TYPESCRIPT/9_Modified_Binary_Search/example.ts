// Sample Question: Search in Rotated Sorted Array
// Problem:
// You are given a sorted array that has been rotated at an unknown pivot(e.g.,).Write an algorithm to find the index of a given target value.If the target does not exist in the array, return -1.

// Example:
// Input: nums = [4,5,6,7,0,1,2], target = 0
// Output: 4

// Input: nums = [4,5,6,7,0,1,2], target = 3
// Output: -1

// Input: nums = [10,15,20,0,5], target = 5
// Output: 4

// Input: nums = [30,40,50,10,20], target = 10
// Output: 3

// Input: nums = [6,7,8,1,2,3,4,5], target = 8
// Output: 2

// Input: nums = [2,3,4,5,6,7,8,9,1], target = 1
// Output: 8

// Input: nums = [15,18,2,3,6,12], target = 3
// Output: 3

// Constraints:
// Array contains no duplicates.
// Time complexity must be O(log n).


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
