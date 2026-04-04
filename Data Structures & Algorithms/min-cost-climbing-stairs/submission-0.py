class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        # strategy: start at the top of the stairs (index len(cost))
        # iterate down from the top of the stairs and replace the current cost
        # with min(cost[curr_i] + cost[curr_i + 1],  cost[curr_2] + cost[curr_i + 2])
        # return min of index 0 or index 1
        # works since cost list is guaranteed to be len of 2 or greater

        size = len(cost)
        min_cost = []

        for i in range(size-1, -1, -1):
            print("not if i:", i)
            if i+1 < size and i+2 < size:
                curr_cost = cost[i]
                cost[i] = min(curr_cost + cost[i+1], curr_cost + cost[i+2])
                print("in if:", i, curr_cost, cost[i+1], cost[i+2])

        print(cost)
        return min(cost[0], cost[1])
        