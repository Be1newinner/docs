# Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

# An input string is valid if:

# Open brackets must be closed by the same type of brackets.
# Open brackets must be closed in the correct order.
# Every close bracket has a corresponding open bracket of the same type.

# Example 1:
# Input: s = "()"
# Output: true

# Example 2:
# Input: s = "()[]{}"
# Output: true

# Example 3:
# Input: s = "(]"
# Output: false

# Example 4:
# Input: s = "([])"
# Output: true

# Constraints:

# 1 <= s.length <= 104
# s consists of parentheses only '()[]{}'.

#Leet Code URL :- https://leetcode.com/problems/valid-parentheses/description/

class Solution:
    def isValid(self, s: str) -> bool:
        if len(s) % 2 != 0:
            return False
        s_list = [char for char in s] 
        valid_start = ['(', '{', '[']
        valid_end = [')', '}', ']']
        container = []
        for char in s_list:
            if char in valid_start:
                container.append(char)
            else: 
                if not container:
                    return False
                start = container.pop()
                if (valid_start.index(start) == valid_end.index(char)):
                    continue
                else:
                    return False
        if len(container) > 0:
            return False
        return True
            
    
sol = Solution
print(sol.isValid(sol, "({})([])[]"))