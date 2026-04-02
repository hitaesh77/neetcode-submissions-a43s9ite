class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        # thought process:
        # run a dfs everytime we see a 1, keepign track of coords
        # ignore 0s
        # everytime we complete a dfs, add 1]
        
        count = 0
        visited_coords = set()

        for i in range(len(grid)):
            for j in range(len(grid[0])):

                if grid[i][j] == "0" or grid[i][j] == "-1":
                    continue
                
                else: # must be "1"
                    q = deque()
                    q.append([i,j])

                    while q:
                        curr = q.popleft()
                        
                        x = curr[0]
                        y = curr[1]

                        grid[x][y] = "-1"

                        if (x+1) < len(grid) and grid[x+1][y] != "0" and grid[x+1][y] != "-1":
                            q.append([x+1,y])
                        if (x-1) >= 0 and grid[x-1][y] != "0" and grid[x-1][y] != "-1":
                            q.append([x-1,y])
                        if (y + 1) < len(grid[0]) and grid[x][y+1] != "0" and grid[x][y+1] != "-1":
                            q.append([x,y+1])
                        if (y - 1) >= 0 and grid[x][y-1] != "0" and grid[x][y-1] != "-1":
                            q.append([x,y-1])

                    count += 1
        
        return count

        