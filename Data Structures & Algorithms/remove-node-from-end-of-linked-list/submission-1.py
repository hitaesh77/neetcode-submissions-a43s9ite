# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        curr = head
        num = 0
        while curr:
            num += 1
            curr = curr.next

        i = num - n
        if i == 0:
            return head.next

        curr = head
        for j in range(num - 1):
            if i == (j + 1):
                curr.next = curr.next.next
                break
            curr = curr.next
        
        return head
            
            