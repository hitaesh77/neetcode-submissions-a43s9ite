class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        l, r = 0, 1
        max_p = 0

        while r < len(prices):
            if prices[r] > prices[l]:
                curr_p = prices[r] - prices[l]
                max_p = max(max_p, curr_p)
            else:
                l = r
            
            r += 1
        
        print(l, r)
        return max_p
        