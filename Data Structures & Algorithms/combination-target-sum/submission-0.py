class Solution:
    def combinationSum(self, nums: List[int], target: int) -> List[List[int]]:
        res = []

        def backtrack(i, path, total):
            if (total == target):
                res.append(path[:])
                return
            
            if (i >= len(nums)) or (total>target):
                return
            
            path.append(nums[i])
            backtrack(i, path, total + nums[i])
            path.pop()
            backtrack(i + 1, path, total)
            
        backtrack(0, [], 0)
        
        return res
        