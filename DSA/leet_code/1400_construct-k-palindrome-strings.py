# Given a string s and an integer k, return true if you can use all the characters in s to construct k palindrome strings or false otherwise.

# Example 1:
# Input: s = "annabelle", k = 2
# Output: true
# Explanation: You can construct two palindromes using all characters in s.
# Some possible constructions "anna" + "elble", "anbna" + "elle", "anellena" + "b"

# Example 2:
# Input: s = "leetcode", k = 3
# Output: false
# Explanation: It is impossible to construct 3 palindromes using all the characters of s.

# Example 3:
# Input: s = "true", k = 4
# Output: true
# Explanation: The only possible solution is to put each character in a separate string.
 

# Constraints:
# 1 <= s.length <= 105
# s consists of lowercase English letters.
# 1 <= k <= 105
# Link https://leetcode.com/problems/construct-k-palindrome-strings/description/


class Solution:
    def canConstruct(self, s: str, k: int) -> bool:
        if len(s) == k:
            return True
        num_of_palindrome = 0
        char_count = {}
        for char in s:
            char_count[char] = char_count.get(char, 0) + 1
        
        if len(char_count.keys()) == k:
            return True


        # a = 9
        ####
        # [9]
        # [8,1]
        # [7,2] 
        # [7,1,1]
        # [6,3]
        # [6,2,1]
        # [6,1,1,1]
        # [5,4]
        # [5,3,1]
        # [5,2,2]
        # [5,2,1,1]
        # [5,1,1,1,1]
        # [4,4,1]
        # [4,3,2]
        # [4,3,1,1]
        # [4,2,2,1]
        # [4,2,1,1,1]
        # [4,1,1,1,1,1]
        # [3,3,3]
        # [3,3,2,1]
        # [3,3,1,1,1]
        # [3,2,1,1,1,1]
        # [3,1,1,1,1,1,1]
        # [2,2,2,2,1]
        # [2,2,2,1,1,1]
        # [2,2,1,1,1,1,1]
        # [2,1,1,1,1,1,1,1]
        # [1,1,1,1,1,1,1,1,1] 
        # ###
        

        # aaaaaaaa => 8 = 21
        
        # aaaaaaaa
        # aaaaaaa a
        # aaaaaa aa
        # aaaaaa a a
        # aaaaa aaa
        # aaaaa aa a
        # aaaaa a a a
        # aaaa aaaa
        # aaaa aaa a
        # aaaa aa a a
        # aaaa a a a a
        # aaa aaa aa
        # aaa aaa a a
        # aaa aa aa a
        # aaa aa a a a
        # aaa a a a a a
        # aa aa aa aa
        # aa aa aa a a
        # aa aa a a a a
        # aa a a a a a a 
        # a a a a a a a a

        # aaaaaaa => 7 = 15
        
        # aaaaaaa
        # aaaaaa a
        # aaaaa aa
        # aaaaa a a
        # aaaa aaa
        # aaaa aa a
        # aaaa a a a
        # aaa aaa a
        # aaa aa aa
        # aaa aa a a
        # aaa a a a a
        # aa aa aa a
        # aa aa a a a
        # aa a a a a a
        # a a a a a a a
        
        # aaaaaa => 6 = 11
        
        # aaaaaa
        # aaaaa a
        # aaaa aa
        # aaaa a a
        # aaa aaa
        # aaa a a a
        # aaa aa a
        # aa aa aa 
        # aa aa a a
        # aa a a a a
        # a a a a a a
        
        # aaaaa => 5 = 7
        # aaaa a
        # aaa aa
        # aaa a a
        # aa aa a
        # aa a a a
        # a a a a a
    
        # aaaa => 4 = 4
        # aaa a
        # aa aa
        # a a a a
        
        # aaa => 3 = 3
        # aa a
        # a a a
        
        # aa => 2 = 2
        # a
        
        # a => 1 = 1
    
s = "annabelle", k = 2
s = "leetcode", k = 3
s = "true", k = 4


solution = Solution()
print(solution.canConstruct(s,k))
