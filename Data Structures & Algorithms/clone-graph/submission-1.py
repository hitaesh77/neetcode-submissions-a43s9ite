"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""

class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        # strategy: do a traversal fo the graph
        # add unseen nodes
        # if neighbor is in seen already, need to upadte neighbors for both nodes
        # lets run dfs to get better at it

        visited = {}
        
        def dfs(node):
            if node in visited:
                return visited[node]

            new_node = Node()
            new_node.val = node.val
            visited[node] = new_node
            
            if (node.neighbors):
                for n in node.neighbors:
                    new_node.neighbors.append(dfs(n))
                
            return new_node

        if node:
            return dfs(node) 
        else:
            return None          

            