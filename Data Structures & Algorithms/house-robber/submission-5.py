class Solution:
    def rob(self, nums: List[int]) -> int:
        # revised strategy:
        # iterate through the list and somehow determine the highest return per house
        # NEED TO FIGURE OUT HOW TO DETYERMINE THAT
        # return max of the list

        # prefix sums approach?

        maxes = []

        if len(nums) == 1:
            return nums[0]
        if len(nums) == 2:
            return max(nums[0], nums[1])
        if len(nums) == 3:
            return max((nums[0] + nums[2]), nums[1])
        
        maxes = []

        idx = 0
        for n in nums:
            if idx == 0:
                maxes.append(nums[idx])

            elif idx == 1:
                maxes.append(max(nums[0], nums[1]))
                
            elif idx == 2:
                maxes.append(max((nums[0] + nums[2]), nums[1]))

            else:
                maxes.append(n + max(maxes[idx-2], maxes[idx-3]))

            idx += 1
        
        return max(maxes)

        # initial strategy: try addding odd and even indexes spearately and return max of both sums
        # should work for most row of houses
        # known drawback: max path may have an idx offset greater than 1 (testcase 23 here)
        