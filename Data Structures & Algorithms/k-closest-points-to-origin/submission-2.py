import heapq

class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        # traverse 2d array
        # push onto heap
        # can push tuples onto heap, sorted by first index as primary key

        dist_heap = []
        for point in points:
            x1 = point[0]
            y1 = point[1]
            distance = (x1 ** 2) + (y1 ** 2)

            heapq.heappush(dist_heap, (distance, point))

        print(dist_heap)

        res = []
        for i in range(k):
            res.append(heapq.heappop(dist_heap)[1])

        return res
        