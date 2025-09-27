class Solution(object):
    def isPrefixAndSuffix(self, str1, str2):
        """
        :type str1: str
        :type str2: str
        :rtype: bool
        """
        if str2.startswith(str1) and str2.endswith(str1):
            return True
        else:
            return False
    
    def countPrefixSuffixPairs(self, words):
        """
        :type words: List[str]
        :rtype: int
        """
        count = 0
        
        if len(words) < 2:
            return 0
        
        for i in range(len(words) - 1):
            for j in range(i+1, len(words)):
                if self.isPrefixAndSuffix(words[i], words[j]):
                    count += 1 
        return count
            
words = ["a","aba","ababa","aa"]

data = Solution()

print(data.countPrefixSuffixPairs(words=words))
