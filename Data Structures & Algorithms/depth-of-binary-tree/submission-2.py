# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
# max = 0
# root
# max += 1
# go left
# max += 1
#

class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        
        max_left = self.maxDepth(root.left)
        max_right = self.maxDepth(root.right)

        max_d = 1 + max(max_left, max_right)

        return max_d
        