class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        result = [0] * len(temperatures)
        stack = []

        for i, temp in enumerate(temperatures):
            while stack and stack[-1][1] < temp:
                stack_idx, stack_temp = stack.pop()
                result[stack_idx] = i - stack_idx
            stack.append((i, temp))

        return result