class Solution:
    def isPalindrome(self, s: str) -> bool:
        s = s.lower()
        full_s = s.split()

        for i, fs in enumerate(full_s):
            if not fs.isalnum():
                temp_fs = []
                for char in fs:
                    if char.isalnum():
                        temp_fs.append(char)
                fs = "".join(temp_fs)
                full_s[i] = fs
        
        full_s = "".join(full_s)
        reverse_s = "".join(reversed(full_s))
        return (full_s == reverse_s)
        