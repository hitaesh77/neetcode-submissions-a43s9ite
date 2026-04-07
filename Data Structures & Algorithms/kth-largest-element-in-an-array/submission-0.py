import heapq

class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        for i in range(len(nums)):
            nums[i] *= -1

        heap = heapq.heapify(nums)

        res = []
        for i in range(k):
            res.append((-1 * heapq.heappop(nums)))
        
        return res[-1]