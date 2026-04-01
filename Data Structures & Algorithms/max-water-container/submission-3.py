class Solution:
    def maxArea(self, heights: List[int]) -> int:
        mx_area = 0
        start, end = 0, len(heights) - 1

        while start < end:
            area = min(heights[start], heights[end]) * (end - start)
            mx_area = max(mx_area, area)
            
            if heights[start] < heights[end]:
                start += 1
            else:
                end -= 1
        
        return mx_area