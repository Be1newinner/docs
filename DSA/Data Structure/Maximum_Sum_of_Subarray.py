class Solution():
    def maximum_sum_subarray(self, arr):
        sum = 0
        for item in arr:
            temp = 0
            for i in item:
              temp += i
            if temp > sum:
              sum = temp
        return sum
        
        
sol = Solution()

# arr is the array of array containing the subarrays of numbers

arr = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print(sol.maximum_sum_subarray(arr))