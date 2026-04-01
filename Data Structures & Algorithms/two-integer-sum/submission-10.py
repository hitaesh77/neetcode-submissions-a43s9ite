class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        ind_list = []
        for i,n in enumerate(nums):
            ind_list.append([n, i])
        
        ind_list.sort()
        j = 0
        k = len(nums) - 1

        while(k>=j):
            temp = ind_list[j][0] + ind_list[k][0]
            if temp == target:
                return [min(ind_list[j][1], ind_list[k][1]),
                        max(ind_list[j][1], ind_list[k][1])]
            elif temp > target:
                k -= 1
            else:
                j += 1
                
        return []