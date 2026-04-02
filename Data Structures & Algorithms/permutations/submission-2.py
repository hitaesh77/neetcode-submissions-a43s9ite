class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        res = []
        seen = []

        for k in range(len(nums)):
            seen.append(False)

        def backtrack(i, path, length, seen):
            if (length == len(nums)):
                res.append(path[:])
                return
            
            for j in range(len(nums)):
                if i < len(nums) and (not seen[j]):
                    path.append(nums[j])
                    seen[j] = True
                    backtrack(i+1, path, length + 1, seen)
                    path.pop()
                    seen[j] = False
                    backtrack(i+1, path, length, seen)

                # if i < len(nums) and nums[j] not in path:
                #     path.append(nums[j])
                #     backtrack(i + 1, path, length + 1)
                #     path.pop()
                #     backtrack(i + 1, path, length)

        backtrack(0, [], 0, seen)
             

        return res
        # res = []

        # for i in nums:
        #     temp = []
        #     temp.append(i)
        #     for j in nums:
        #         if j not in temp:
        #             temp.append(j)
        #         for k in nums:
        #             if k not in temp:
        #                 temp.append(k)
        #             if temp not in res:
        #                 res.append(temp)
        #                 while len(temp) > 1:
        #                     temp.pop()
        #                 continue
        
        # return res

        