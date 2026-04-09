import heapq
from collections import Counter, deque

class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        # strategy: use a heap to keep track of the most frequent task
        # this is because we have to prioritize these tasks
        # pop from heap, then start incrementing time
        # append the end of buffer time for the curr val popped from heap to queue
        # pop the next frequent form heap
        # when it is finally time for a value in the q to be used, the value gets pushed onto the heap after being used
        # this way it can be used again
        # if heap is empty, just take time from queue: should accoutn for idle

        count = Counter(tasks)

        heap = [-cnt for cnt in count.values()]
        heapq.heapify(heap)

        time = 0
        q = deque()
        while heap or q:
            time += 1

            if heap:
                cnt = (-1 * heapq.heappop(heap)) - 1
                if cnt:
                    q.append([cnt, time+n])
            else:
                time = q[0][1]
            
            if q and q[0][1] == time:
                curr_task = -1 * q.popleft()[0]
                heapq.heappush(heap, curr_task)

        return time        