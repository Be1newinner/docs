# https://leetcode.com/problems/3sum/description/

## Topics
# => Array
# => Two Pointers
# => Sorting

# Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

# Notice that the solution set must not contain duplicate triplets.

# Example 1:

# Input: nums = [-1,0,1,2,-1,-4]
# Output: [[-1,-1,2],[-1,0,1]]
# Explanation:
# nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
# nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
# nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
# The distinct triplets are [-1,0,1] and [-1,-1,2].
# Notice that the order of the output and the order of the triplets does not matter.
# Example 2:

# Input: nums = [0,1,1]
# Output: []
# Explanation: The only possible triplet does not sum up to 0.
# Example 3:

# Input: nums = [0,0,0]
# Output: [[0,0,0]]
# Explanation: The only possible triplet sums up to 0.


# Constraints:

# 3 <= nums.length <= 3000
# -105 <= nums[i] <= 105


# Answers

# if builtin sort not allowed
# def sort_list(self, ls: List[int]):
#     if ls[0] == ls[1] == ls[2]:
#         return

#     if ls[0] > ls[1]:
#         ls[0], ls[1] = ls[1], ls[0]

#     if ls[1] > ls[2]:
#         ls[1], ls[2] = ls[2], ls[1]

#     if ls[0] > ls[1]:
#         ls[0], ls[1] = ls[1], ls[0]


from typing import List


# [1,2,3,4,5,6]
# 1, 2, 3
# 2, 3, 4
# 3, 4, 5
# 4, 5, 6

# class Solution:
#     def threeSum(self, nums: List[int]) -> List[List[int]]:
#         nums.sort()
#         result_set = set()
#         nums_len = len(nums)

#         for i in range(nums_len - 2):
#             for j in range(i + 1, nums_len - 1):
#                 for k in range(j + 1, nums_len):
#                     if nums[i] + nums[j] + nums[k] == 0:
#                         scored_list = sorted([nums[i], nums[j], nums[k]])
#                         result_set.add(tuple(scored_list))
#         return [list(x) for x in list(result_set)]

L1 + L2,

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        result_set = set()
        nums_len = len(nums)

        for i in range(nums_len - 2):
            for j in range(i + 1, nums_len - 1):
                for k in range(j + 1, nums_len):
                    if nums[i] + nums[j] + nums[k] == 0:
                        scored_list = sorted([nums[i], nums[j], nums[k]])
                        result_set.add(tuple(scored_list))
        return [list(x) for x in list(result_set)]

data = [
    {"in": [-1, 0, 1, 2, -1, -4], "out": [[-1, -1, 2], [-1, 0, 1]]},
    {"in": [0, 1, 1], "out": []},
    {"in": [0, 0, 0], "out": [[0, 0, 0]]},
    {"in": [-1, 0, 1], "out": [[-1, 0, 1]]},
    {"in": [1, -1, -1, 0], "out": [[-1, 0, 1]]},
]


def is_list_same(list1, list2):
    return sorted([sorted(sublist) for sublist in list1]) == sorted(
        [sorted(sublist) for sublist in list2]
    )


sol = Solution()

cleared = 0

for x in data:
    res = sol.threeSum(x["in"])
    if not is_list_same(res, x["out"]):
        print(x["in"], " => ", x["out"], " => ", res)
    else:
        cleared += 1

print(f"{cleared}/{len(data)} tests cleared")
