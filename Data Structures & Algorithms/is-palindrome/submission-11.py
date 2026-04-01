class Solution:
    def isPalindrome(self, s: str) -> bool:
        cleaned = []
        for c in s:
            if c.isalpha() or c.isdigit():
                cleaned.append(c.lower())
        
        clean = "".join(cleaned)

        start, end = 0, len(clean) - 1

        while start < end:
            if clean[start] != clean[end]:
                print(clean[start], clean[end])
                return False
            
            start += 1
            end -= 1

        return True

        