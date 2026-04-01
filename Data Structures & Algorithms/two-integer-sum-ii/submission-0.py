class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        i = 0
        j = len(numbers) - 1
        while (j > i):
            temp = numbers[i] + numbers[j]
            if (temp == target):
                return [i + 1, j + 1]
            elif (temp < target):
                i += 1
            else:
                j -= 1
        return []