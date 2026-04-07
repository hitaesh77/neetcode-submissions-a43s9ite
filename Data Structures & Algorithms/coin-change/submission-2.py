class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:


        # next strategy: learn 2d - dp, bottom up
        # using 2d array:
        n = len(coins)
        dp = [[amount+1] * (amount + 1) for _ in range(n + 1)]

        for i in range(n + 1):
            dp[i][0] = 0

        for i in range(1, n + 1):
            for j in range(1, amount + 1):
                curr_coin = coins[i - 1]

                # include curr coin path
                if j >= curr_coin:
                    include = 1 + dp[i][j - curr_coin]
                else:
                    include = amount + 1
                
                #exclude path
                exclude = dp[i-1][j]

                dp[i][j] = min(include, exclude)
        
        result = dp[n][amount]
        return result if result != (amount + 1) else -1

        

        # space optimized:
        dp = [amount + 1] * (amount + 1)
        dp[0] = 0

        for a in range(1, amount + 1):
            for c in coins:
                if a - c >= 0:
                    dp[a] = min(dp[a], 1 + dp[a-c])
        return dp[amount] if dp[amount] != amount + 1 else -1






        # initial strategy:
        # backtrackign would work well since we can make a decision, and see what happens if we dont
        # we can keep a runnign counter for each decision we make and return the min of the counter
        # however, this seems extremely slow, there must be a better way

        # simialr to backtrackign, we could do a brute force dfs, and use memoization to store results in a dict
        # shoudl be way faster
        # this strategy works but reaches python's recusrion depth limit (1000) ojn a test case
        # need to re-evaluate

        # if amount == 0:
        #     return 0
        
        # cache = {}

        # def dfs(amount):
        #     if amount == 0:
        #         return 0
        #     if amount in cache:
        #         return cache[amount]
            
        #     min_coins = -1
        #     # traverse neighbors:
        #     for coin in coins:
        #         if (amount - coin) >= 0:
        #             curr_count = dfs(amount - coin)

        #             if min_coins != -1 and curr_count != -1:
        #                 min_coins = min(min_coins, 1 + curr_count)
        #             if min_coins == -1 and curr_count != -1:
        #                 min_coins = 1 + curr_count

        #     cache[amount] = min_coins
        #     return min_coins
        
        # return dfs(amount)