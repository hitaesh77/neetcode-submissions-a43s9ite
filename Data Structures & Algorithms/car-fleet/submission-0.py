class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        pair = [(p, s) for p, s in zip(position, speed)]
        pair.sort(reverse=True)

        fleets = []

        for p, s in pair:
            time = (target - p) / s
            fleets.append(time)

            if len(fleets) >= 2 and fleets[-1] <= fleets[-2]:
                fleets.pop()
            
        return len(fleets)
        

        
        