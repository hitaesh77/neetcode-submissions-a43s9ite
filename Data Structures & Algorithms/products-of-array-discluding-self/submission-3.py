class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        product = 1
        zero_cnt = 0
        for n in nums:
            if n == 0:
                zero_cnt += 1
            else:
                product *= n
        
        res = []

        if zero_cnt > 1:
            return ([0] * len(nums))

        for i in range(len(nums)):
            if zero_cnt:
                if nums[i] != 0:
                    res.append(0)
                else:
                    res.append(product)
            else:
                res.append(product // nums[i])
            
        return res
