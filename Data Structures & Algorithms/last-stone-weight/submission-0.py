import heapq

class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        for i in range(len(stones)):
            stones[i] *= -1

        heapq.heapify(stones)

        while len(stones) > 1:
            first = -1 * heapq.heappop(stones)
            second = -1 * heapq.heappop(stones)

            if first == second:
                continue
            
            first -= second

            heapq.heappush(stones, (first * -1))
        
        if stones:
            return (stones[-1] * -1)
        
        return 0

        