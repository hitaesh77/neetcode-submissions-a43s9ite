import heapq

class KthLargest:

    def __init__(self, k: int, nums: List[int]):
        self.k = k

        for i in range(len(nums)):
            nums[i] *= -1

        self.nums_heap = nums
        heapq.heapify(self.nums_heap)
        

    def add(self, val: int) -> int:
        heapq.heappush(self.nums_heap, (val * -1))

        temp = []
        for _ in range(self.k):
            temp.append((-1 * heapq.heappop(self.nums_heap)))
        
        kth_largest = temp[-1]

        for t in temp:
            heapq.heappush(self.nums_heap, (t * -1))
        
        print (temp)
        
        return kth_largest
        
