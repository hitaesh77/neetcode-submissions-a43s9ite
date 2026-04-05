class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        # strategy: go through grid once and find all rotten fruit.
        # do bfs at mulitple points starting at the rotten fruit
        # track the "mins" buy having an iterations flag
        # rotten fruit will have a 0 flag
        # every append will have a flag of prev flag + 1
        # 

        def print_grid(grid):
            for i in range(len(grid)):
                print(grid[i])

        rows = len(grid)
        cols = len(grid[0])
        seen = [[-1 for _ in range(cols)] for _ in range(rows)]

        print("beg:")
        print_grid(grid)
        print_grid(seen)

        q = deque()

        def is_valid(i, j):
            # check in bounds
            # check grid is frehs fruit
            # check not seen yet
            return ((i < rows) and (j < cols) and (i >= 0) and (j>=0) and (grid[i][j] == 1) and seen[i][j] == -1)

        # populate q with 0's
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 2:
                    seen[i][j] = 0
                    q.append((i,j))
                if grid[i][j] == 1:
                    seen[i][j] = -1
                if grid[i][j] == 0:
                    seen[i][j] = 0
        
        # run bfs
        while(q):
            print("iter:")
            print_grid(seen)
            curr_i, curr_j = q.popleft()
            curr_val = seen[curr_i][curr_j]

            if(is_valid(curr_i+1, curr_j)):
                q.append((curr_i+1,curr_j))
                seen[curr_i+1][curr_j] = curr_val + 1
            
            if(is_valid(curr_i-1, curr_j)):
                q.append((curr_i-1,curr_j))
                seen[curr_i-1][curr_j] = curr_val + 1
            
            if(is_valid(curr_i, curr_j+1)):
                q.append((curr_i,curr_j+1))
                seen[curr_i][curr_j+1] = curr_val + 1
            
            if(is_valid(curr_i, curr_j-1)):
                q.append((curr_i,curr_j-1))
                seen[curr_i][curr_j-1] = curr_val + 1

        print("end:")
        print_grid(grid)
        print_grid(seen)
        
        for i in range(rows):
            for j in range(cols):
                if seen[i][j] == -1:
                    return -1
        
        return max(max(row) for row in seen)

            



        