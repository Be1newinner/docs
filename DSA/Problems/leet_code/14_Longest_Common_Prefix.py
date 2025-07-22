# Write a function to find the longest common prefix string amongst an array of strings.

# If there is no common prefix, return an empty string "".

# Example 1:

# Input: strs = ["flower","flow","flight"]
# Output: "fl"
# Example 2:

# Input: strs = ["dog","racecar","car"]
# Output: ""
# Explanation: There is no common prefix among the input strings.
 
# Constraints:

# 1 <= strs.length <= 200
# 0 <= strs[i].length <= 200
# strs[i] consists of only lowercase English letters.

class Solution:
    def longestCommonPrefix(self, strs):
        count = 0
        long_curr_word = ""
        first_len = len(strs[0])
        for i in range(first_len):
            count_temp = 0
            curr_word = strs[0][:first_len - i]
            for word in strs:
                if word.startswith(curr_word):
                    count_temp += 1
            if len(strs) == count_temp and count < count_temp:
              long_curr_word = curr_word
              count = count_temp
        if len(strs) == 1:
            return strs[0]
        if count <= 1:
            return ""
        else :
            return long_curr_word

    
data = ["floower","flow","floight"]
# data = ["a"]
# data = ["a","a","b"]

solution = Solution()
print(solution.longestCommonPrefix(data))