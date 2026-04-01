class Solution:
    def isPalindrome(self, s: str) -> bool:

        def clean(s):
            res = []
            for char in s:
                if (char.isalpha()) or (char.isdigit()):
                    res.append(char.lower())
            
            return ''.join(res)

        cleaned_s = clean(s)
        length = len(cleaned_s)
        start = 0
        end = length - 1

        while start < end:
            print(cleaned_s[start])
            print(cleaned_s[end])
            if cleaned_s[start] != cleaned_s[end]:
                return False
            
            start += 1
            end -= 1
    
        return True
    
        