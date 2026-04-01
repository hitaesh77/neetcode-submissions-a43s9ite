class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        # check rows O(n^2)
        for row in board:
            rows = set()
            for n in row:
                if (n in rows) and (n != "."):
                    print("row false")
                    return False
                else:
                    rows.add(n)
        
        # check cols O(n^2)
        for i in range(9):
            cols = set()
            for j in range(9):
                if (board[j][i] in cols) and (board[j][i] != "."):
                    print("col false")
                    return False
                else:
                    cols.add(board[j][i])

        # check squares
        for idx_r in range(3):
            for idx_c in range(3):
                sqrs = set()
                for k in range(3):
                    for l in range(3):
                        n = board[idx_r*3 + k][idx_c*3 + l]
                        if (n in sqrs) and (n != "."):
                            print("square false")
                            return False
                        else:
                            sqrs.add(n)
                        l += 1
                    k += 1
                idx_c += 1
            idx_r += 1

        return True

