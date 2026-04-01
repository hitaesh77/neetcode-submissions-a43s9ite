class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        nums = set(nums)
        nums = list(nums)
        nums = sorted(nums)

        max_seq = 0
        temp_max = 0
        print(nums)
        for i,n in enumerate(nums):
            if (i == 0):
                max_seq += 1
                temp_max += 1
            else:
                print(i-1)
                if (n == (nums[i - 1] + 1)):
                    temp_max += 1
                else:
                    max_seq = max(max_seq, temp_max)
                    temp_max = 1
        max_seq = max(max_seq, temp_max)
        return max_seq

        