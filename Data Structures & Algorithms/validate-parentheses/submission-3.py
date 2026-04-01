class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        brackets = {')' : '(',
                    '}' : '{',
                    ']' : '['}

        open_c = {'(', '{', '['}
        close_c = {')', '}', ']'}

        for c in s:
            if c in open_c:
                stack.append(c)
            if c in close_c:
                if (len(stack) > 0) and stack[-1] == brackets[c]:
                    stack.pop()
                else:
                    return False
        
        return len(stack) == 0

