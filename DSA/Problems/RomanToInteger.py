# Symbol       Value
# I             1
# V             5
# X             10
# L             50
# C             100
# D             500
# M             1000

class Solution:
    def romanToInt(self, s: str) -> int:
      num = 0
      s = s.upper()
      for i in s:
          if i == "I":
              num += 1
          if i == "V":
              num += 5
          if i == "X":
              num += 10
          if i == "L":
              num += 50
          if i == "C":
              num += 100
          if i == "D":
              num += 500
          if i == "M":
              num += 1000
      return num
        
sol = Solution()
print(sol.romanToInt("LXvII"))
