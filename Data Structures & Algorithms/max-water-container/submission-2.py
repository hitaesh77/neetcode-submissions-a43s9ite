class Solution:
    def maxArea(self, heights: List[int]) -> int:
        l, r = 0, len(heights) - 1
        max_water = 0

        while r >= l:
            temp_max = min(heights[l], heights[r]) * (r - l)
            max_water = max(max_water, temp_max)

            if(heights[l] > heights[r]):
                r -= 1
            else:
                l += 1
        
        return max_water