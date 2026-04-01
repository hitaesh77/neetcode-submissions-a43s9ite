class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        running = set()
        l = 0
        max_s = 0

        for r in range(len(s)):
            while s[r] in running:
                running.remove(s[l])
                l += 1
            
            running.add(s[r])
            max_s = max(max_s, r - l + 1)

        
        return max_s
            
        