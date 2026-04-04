class Solution:
    def climbStairs(self, n: int) -> int:
        if n == 0:
            return 0
        
        if n == 1:
            return 1

        if n == 2:
            return 2

        cnt = 0
        prev_1 = 1
        prev_2 = 2

        for i in range(3,n+1):
            cnt = (prev_1 + prev_2)
            prev_1 = prev_2
            prev_2 = cnt
            print(cnt, prev_1, prev_2)
        
        return cnt
            

        
        