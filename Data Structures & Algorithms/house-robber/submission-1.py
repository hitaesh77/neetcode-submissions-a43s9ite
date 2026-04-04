class Solution:
    def rob(self, nums: List[int]) -> int:
        # revised strategy:
        # iterate through the list and somehow determine the highest return per house
        # NEED TO FIGURE OUT HOW TO DETYERMINE THAT
        # return max of the list
        
        sum_idx_0 = 0
        sum_idx_1 = 0
        i = 0

        for n in nums:
            if (i % 2) == 0:
                sum_idx_0 += n
            else:
                sum_idx_1 += n
            
            i += 1
        
        return max(sum_idx_0, sum_idx_1)

        # initial strategy: try addding odd and even indexes spearately and return max of both sums
        # should work for most row of houses
        # known drawback: max path may have an idx offset greater than 1 (testcase 23 here)
        