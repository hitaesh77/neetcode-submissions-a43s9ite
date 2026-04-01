class Solution:
    def search(self, nums: List[int], target: int) -> int:
        def bsearch(nums, target, start, end):
            if(end < start):
                return -1
            
            mid = (start + end) // 2
            if (nums[mid] == target):
                return mid
            elif (nums[mid] < target):
                return bsearch(nums, target, mid + 1, end)
            else:
                return bsearch(nums, target, start, mid - 1)
        
        return bsearch(nums, target, 0, len(nums) - 1)