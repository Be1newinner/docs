class Solution():
    def sliding_window_sum_subarray(self, arr, window):
        if window < 1 or window > len(arr):
          return 0
      
        max_sum = 0
        window_sum = 0
        for i in range(len(arr)):
          window_sum  += arr[i]
          if i >= window - 1:
           max_sum = max(max_sum, window_sum)
           window_sum -= arr[i - window + 1]
           
        return max_sum
        
        
sol = Solution()

# Quesiton. Find the maximum sum of subarray with window = k

k = 3

# arr = [ 15,2,8,9,5,6,7,8]
# arr = [2, 1, 5, 1, 3, 2]
# arr = [1, 2, 3]
arr = []


print(sol.sliding_window_sum_subarray(arr, k))