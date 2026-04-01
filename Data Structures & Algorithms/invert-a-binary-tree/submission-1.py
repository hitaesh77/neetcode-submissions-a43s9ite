# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
# root node
# print root node
# swap left and right (use temp for this)
# recurse by calling function on left
# recurse by calling function on right

class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if (root):
            new_right = root.left
            new_left = root.right

            root.right = new_right
            root.left = new_left

            self.invertTree(root.left)
            self.invertTree(root.right)
            
            # return root
        
        return root

            
        
        