import math

class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        max_speed = max(piles)
        min_speed = 1
        result = max_speed

        while min_speed <= max_speed:
            test_speed = (min_speed + max_speed) // 2

            total_hours = 0
            for pile in piles:
                total_hours += math.ceil(pile / test_speed)
            
            if total_hours <= h:
                result = test_speed
                max_speed = test_speed - 1
            else:
                min_speed = test_speed + 1
        
        return result