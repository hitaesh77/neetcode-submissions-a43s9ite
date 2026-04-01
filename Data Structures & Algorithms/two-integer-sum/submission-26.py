class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        nums_dict = dict()

        for i, n in enumerate(nums):
            nums_dict[n] = i
        
        for i, n in enumerate(nums):
            goal = target - n
            if (goal in nums_dict) and (i != nums_dict[goal]):
                return [i, nums_dict[goal]]
        
        return []

        