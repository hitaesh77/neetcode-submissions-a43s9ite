# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        curr = head
        nodes = []
        while curr:
            nodes.append(curr)
            curr = curr.next
        
        i = len(nodes) - n
        if i == 0:
            return head.next
        
        nodes[i - 1].next = nodes[i].next
        return head        