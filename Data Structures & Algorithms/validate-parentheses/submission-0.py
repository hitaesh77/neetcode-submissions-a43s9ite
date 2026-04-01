class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        pairing = {')' : '(', '}' : '{', ']' : '['}

        for c in s:
            if c in pairing:
                if stack and stack[-1] == pairing[c]:
                    stack.pop()
                else: 
                    return False
            else:
                stack.append(c)
        
        if not stack:
            return True
        else:
            return False
        