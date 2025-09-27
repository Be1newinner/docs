"""
35. Search Insert Position

Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.

You must write an algorithm with O(log n) runtime complexity.

Example 1:

Input: nums = [1,3,5,6], target = 5
Output: 2
Example 2:

Input: nums = [1,3,5,6], target = 2
Output: 1
Example 3:

Input: nums = [1,3,5,6], target = 7
Output: 4


Constraints:

1 <= nums.length <= 104
-104 <= nums[i] <= 104
nums contains distinct values sorted in ascending order.
-104 <= target <= 104

URL = https://leetcode.com/problems/search-insert-position/description/?envType=problem-list-v2&envId=nh6i5742

"""


class Solution:
    def searchInsert2(self, nums: list[int], target: int) -> int:
        left, right = 0, len(nums)
        while left < right:
            mid = (left + right) // 2
            if nums[mid] >= target:
                right = mid
            else:
                left = mid + 1
        return left

    def searchInsert(self, nums: list[int], target: int) -> int:
        start = 0
        end = len(nums) - 1

        if target < nums[0]:
            return 0

        if target > nums[end]:
            return end + 1

        while start <= end:
            mid = (start + end) // 2

            if nums[mid] == target:
                return mid
            elif target < nums[mid]:
                end = mid - 1
            else:
                start = mid + 1

            if abs(mid - end) == 1:
                if target > nums[mid] and target < nums[end]:
                    return mid + 1

            if abs(start - mid) == 1:
                if target < nums[mid] and target > nums[start]:
                    return mid

            if abs(start - end) == 1:
                if target == nums[start]:
                    return start

                if target == nums[end]:
                    return end

                if target > nums[start] and target < nums[end]:
                    return start + 1
                elif target < nums[start]:
                    return start
                else:
                    return end + 1

        return -1
