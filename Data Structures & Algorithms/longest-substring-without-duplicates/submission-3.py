class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        if not s:
            return 0

        start, end = 0, 1
        max_len = 1
        seen = set()
        seen.add(s[start])
        length = 1

        while end < len(s):
            if s[end] not in seen:
                seen.add(s[end])
                length += 1
            else:
                while s[start] != s[end]:
                    seen.remove(s[start])
                    start += 1
                    length -= 1
                    # seen.remove(s[start])
                start += 1
            max_len = max(max_len, length)
            end += 1
        
        return max_len

