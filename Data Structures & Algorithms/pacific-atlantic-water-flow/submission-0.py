from collections import deque

class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        # initial strategy;
        # top right and bottom left cells should onyl be included
        # start at the pacific ocean and "climb" to neighboring cells
        # if we are able to access that cell, then mark it as accessible by that ocean
        # do that same for bnoth oceans
        # if a cell is accessible by both oceans, then add that cell to res

        if not heights or not heights[0]:
            return []

        r, c = len(heights), len(heights[0])
        pac_q = deque()
        atl_q = deque()
        
        # track how reachable cells are form ocean
        pac_reachable = set()
        atl_reachable = set()

        # load top and bottom rows
        for i in range(c):
            pac_q.append((0, i))
            pac_reachable.add((0, i))
            
            atl_q.append((r - 1, i))
            atl_reachable.add((r - 1, i))
        
        # load left and right cols
        for i in range(r):
            pac_q.append((i, 0))
            pac_reachable.add((i, 0))
            
            atl_q.append((i, c - 1))
            atl_reachable.add((i, c - 1))

        def bfs(queue, reachable_set):
            dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            while queue:
                curr_i, curr_j = queue.popleft()
                
                for di, dj in dirs:
                    ni, nj = curr_i + di, curr_j + dj
                    
                    if 0 <= ni < r and 0 <= nj < c:
                        if (ni, nj) not in reachable_set and heights[ni][nj] >= heights[curr_i][curr_j]:
                            reachable_set.add((ni, nj))
                            queue.append((ni, nj))

        bfs(pac_q, pac_reachable)
        bfs(atl_q, atl_reachable)

        res = []
        for row, col in pac_reachable:
            if (row, col) in atl_reachable:
                res.append([row, col])
        
        return res



