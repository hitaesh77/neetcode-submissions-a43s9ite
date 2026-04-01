class Solution:
    def findMin(self, nums: List[int]) -> int:
        l, r = 0, len(nums) - 1
        res = 0
        
        while l < r:
            mid = (l + r) // 2
            curr = nums[mid]
            print(l, r, mid, nums[mid])

            if curr > nums[r]:
                l = mid + 1
            elif curr < nums[r]:
                r = mid
        
        return nums[r]