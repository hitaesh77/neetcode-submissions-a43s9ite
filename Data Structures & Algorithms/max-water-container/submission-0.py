class Solution:
    def maxArea(self, heights: List[int]) -> int:
        start, end = 0, len(heights) - 1
        maxArea = 0
        while (end > start):
            tempArea = min(heights[start], heights[end]) * (end - start)
            maxArea = max(maxArea, tempArea)
            
            if heights[start] > heights[end]:
                end -= 1
            else:
                start += 1
        
        return maxArea