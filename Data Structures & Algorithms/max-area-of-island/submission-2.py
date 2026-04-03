class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        # initial strategy:
        # similar to number of islands, but also need to keep track of area now
        # same algorithm, keep a runnign coutner everytime an island is detected
        # at the end, when we increment island counter, compare area to curr_max

        max_area = 0
        count = 0

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 0 or grid[i][j] == -1: # skip over water and islands already accoutned for
                    continue

                else: #guaranteed to be 1
                    running_area = 0

                    q = deque()
                    q.append((i,j))

                    while q:
                        x,y = q.popleft()
                        grid[x][y] = -1
                        running_area += 1

                        if ((x+1) < len(grid)) and (grid[x+1][y] == 1):
                            q.append((x+1,y))
                            grid[x+1][y] = -1
                        if ((x-1) >= 0) and (grid[x-1][y] == 1):
                            q.append((x-1,y))
                            grid[x-1][y] = -1
                        if ((y+1) < len(grid[0])) and (grid[x][y+1] == 1):
                            q.append((x,y+1))
                            grid[x][y+1] = -1
                        if ((y-1) >= 0) and (grid[x][y-1] == 1):
                            q.append((x,y-1))
                            grid[x][y-1] = -1
                        
                    count += 1
                    max_area = max(max_area, running_area)

        return max_area
        