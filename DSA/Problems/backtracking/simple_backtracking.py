"""
TOPIC:
Back Tracking , Permutations

Problem Description:
Given an array nums of distinct integers, return all possible permutations. You may return the answer in any order.

"""

# Input = [1, 2, 3]
# Output = [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]

# result = []
# current_permutation = []
# used = set()
# Nested Loop Method ( Not Scalable )
# for ls in Input:
#     for ls1 in Input:
#         for ls2 in Input:
#            if ls != ls1 and ls != ls2 and ls1 != ls2:
#                result.append([ls, ls1, ls2])
# print(result)


# def backtrack():
#     if len(current_permutation) == len(Input):
#         result.append(current_permutation.copy())
#         return

#     for num in Input:
#         if num not in used:
#             used.add(num)

# Very Simple 
result = []
nums = [1,2,3]

def backtrack(index, current_subset):
    # Base Case: We've considered all elements up to this point.
    # The current_subset is a valid subset. Add a COPY of it to result.
    result.append(list(current_subset)) # Or current_subset[:]

    # Recursive Step: Iterate through the remaining elements
    for i in range(index, len(nums)):
        # Choice 1: Include nums[i]
        current_subset.append(nums[i])

        # Explore: Go deeper with the next element (i+1)
        backtrack(i + 1, current_subset)

        # Backtrack: Undo Choice 1 (remove nums[i])
        current_subset.pop()


# Input = [1, 2]

# def permute(nums: list[int]) -> list[list[int]]:
#     result = []
#     current_permutation = []
#     used = set()

#     def backtrack():
#         for n in nums:
#             current_permutation.append(n)

#             if len(current_permutation) == len(nums):
#                 result.append(current_permutation[:])
#                 current_permutation.clear()
#                 used.add(n)
#                 return result

#             if n not in used:
#                 used.add(n)
#                 backtrack()
#                 current_permutation.pop()
#             else:
#                 used.remove(n)
#         return result

#     return backtrack()


print(backtrack(0,[0,1,2]))
