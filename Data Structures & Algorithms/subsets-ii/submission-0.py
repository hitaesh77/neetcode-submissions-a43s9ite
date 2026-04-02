class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        res = []
        seen = set()

        def backtrack(i, path, length, seen):
            if length == len(nums):
                path_tuple = tuple(sorted(path))

                if path_tuple not in seen:
                    seen.add(path_tuple)
                    res.append(path[:])
                    return
            
            if i < len(nums):
                path.append(nums[i])
                backtrack(i + 1, path, length + 1, seen)
                path.pop()
                backtrack(i + 1, path, length + 1, seen)

        backtrack(0, [], 0, seen)

        return res


        