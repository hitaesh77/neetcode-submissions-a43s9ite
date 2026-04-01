class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        chars_s = dict()
        chars_t = dict()

        for cs in s:
            if cs in chars_s:
                chars_s[cs] += 1
            else:
                chars_s[cs] = 1

        for ct in t:
            if ct in chars_t:
                chars_t[ct] += 1
            else:
                chars_t[ct] = 1
        print(chars_s)
        print(chars_t)
        return chars_s == chars_t