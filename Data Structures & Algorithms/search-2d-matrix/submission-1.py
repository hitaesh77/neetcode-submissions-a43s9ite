class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        start_r, start_c = 0, 0
        end_r, end_c = len(matrix) - 1, len(matrix[0]) - 1

        while (start_r <= end_r) and (start_c <= end_c):
            mid_r = (start_r + end_r) // 2
            mid_c = (start_c + end_c) // 2

            curr = matrix[mid_r][mid_c]

            if curr == target:
                return True
            elif curr < target:
                start_c = mid_c + 1
                if start_c == len(matrix[0]):
                    start_c = 0
                    start_r += 1
            else:
                end_c = mid_c - 1
                if end_c == -1:
                    end_c = len(matrix[0]) - 1
                    end_r -= 1

        return False
        