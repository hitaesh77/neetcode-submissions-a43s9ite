class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        indices = {}
        for i, num in enumerate(nums):
            indices[num] = i
        
        for i, num in enumerate(nums):
            diff = target - num
            if diff in indices and indices[diff] != i:
                print([i, indices[diff]])
                return [i, indices[diff]]