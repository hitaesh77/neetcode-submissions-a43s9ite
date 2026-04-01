class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        n_count = defaultdict(int)
        for num in nums:
            n_count[num] += 1
        
        n_count = dict(sorted(n_count.items(), key=lambda item: item[1]))
        print(n_count)
        result = []
        for i in range(k):
            last = n_count.popitem()
            result.append(last[0])

        return result
        