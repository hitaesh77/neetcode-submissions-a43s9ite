class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        k_dict = dict()

        for n in nums:
            if n in k_dict:
                k_dict[n] += 1
            else:
                k_dict[n] = 1
            
        sorted_vals = sorted(k_dict.items(), key=lambda item: item[1], reverse=True)

        res = []

        for i in range(k):
            res.append(sorted_vals[i][0])
        
        return res