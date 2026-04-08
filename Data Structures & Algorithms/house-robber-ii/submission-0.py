class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) == 0:
            return 0
        if len(nums) ==  1:
            return nums[0]
        if len(nums) == 2:
            return max(nums[0], nums[1])
        
        def linear_rob(nums):
            maxes = []
            maxes.append(nums[0])
            maxes.append(max(nums[0], nums[1]))

            for i in range(2, len(nums)):
                maxes.append(max(maxes[i-1], maxes[i-2] + nums[i]))
            print(maxes)
            return maxes[-1]

        return max(linear_rob(nums[1:]), linear_rob(nums[:-1]))
        