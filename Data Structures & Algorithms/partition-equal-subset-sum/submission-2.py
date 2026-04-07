class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        # initial strategy:
        # since all nums must be used, we need to have the subsets equal half of the total
        # this also means that if the len(sub1) < len, then there are guarnateed 2 subarrays that fulfill the requirements
        # we can try this with dp. every nin nums we can either use or not use
        # if we do not use, then we do someting, if we use we do something
        
        total = 0
        for n in nums:
            total += n
        
        if total % 2 != 0:
            return False
        
        half = total // 2
        length = len(nums)

        cache = {}

        def backtrack(curr_sum, i):
            state = (curr_sum, i)
            if state in cache:
                return cache[state]

            if curr_sum == half:
                return True
            if i >= length or curr_sum > half:
                return False

            include = backtrack(curr_sum + nums[i], i + 1) 
            exclude = backtrack(curr_sum, i + 1)

            cache[state] = include or exclude
            return cache[state]
        
        return backtrack(0, 0)
